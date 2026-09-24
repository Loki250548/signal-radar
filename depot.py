#!/usr/bin/env python3
"""depot.py — Papierbetrieb der Depot-Struktur 40/10/40/10 (von Herwig festgelegt am 24.09.2026). Kein Kapital, nur Papier.

Linien (Papierstart 01.10.2026):
  Kern 40 %      Führer-System (Tests 26, 28, 36). Monatsende: 41 US-Branchen-ETFs nach 12-1-Momentum, Top 5 gleichgewichtet,
                 max. 1 je Cluster. Cluster (am 24.09.2026 vor jeder Rechnung festgelegt): Ein Kandidat wird übersprungen, wenn
                 seine Tagesrenditen der letzten 252 Handelstage mit einem schon gewählten Führer zu >= 0,90 korrelieren
                 (praktisch dasselbe Engagement, z. B. OIH/IEZ); der Platz geht an den nächsten. Reichen die Kandidaten nicht,
                 wird mit den übersprungenen aufgefüllt.
                 Konjunkturfilter: raus nur, wenn SPY am Monatsende unter seiner 10-Monats-Linie liegt UND die US-Arbeitslosenquote
                 (Vormonat) über ihrem 12-Monats-Schnitt. Dann Gold (GLD), falls Gold über seiner 10-Monats-Linie, sonst Cash.
                 Rücksetzer-Zusatz: Schließt SPY über der 200-Tage-Linie und mindestens 5 % unter dem 20-Tage-Hoch, wird zur nächsten
                 Eröffnung zusätzlich 1x SPY auf das Kern-Kapital gekauft (finanziert zu T-Bill + 1 %). Ziel +5 %, Stop −5 %
                 (Stop-Order, Kurslücken zum Eröffnungskurs), spätestens nach 120 Handelstagen zum Schluss. Immer nur eine Position.
  Kern ohne Deckel  Vergleichslinie: dieselben Regeln ohne Cluster-Deckel und ohne Gold-Ausweich = Fassung aus Test 28
                 (Rückrechnung 2008–2026: 16,3 % p.a., max. DD −45 %).
  Gold 10 %      GLD, statisch.
  Intraday 40 %  noch nicht aktiv. Zahltag-Radar erst nach bestandenem 5-Jahres-Test (Test 37); bis dahin Cash (T-Bill).
  Lucky Punch 10 %  Nasdaq 100 dreifach (TQQQ), wenn der Nasdaq 100 am Monatsende über seiner 10-Monats-Linie schließt, sonst Cash
                 (Test 34/35).
  Gesamt         40/10/40/10, auf die Zielgewichte umgeschichtet zum Start und am ersten Handelstag jedes Jahres (wie Test 34).
  SPY halten     Vergleich.
Ausführung: Signal zum Schluss des letzten Handelstags im Monat, gehandelt zum Schluss des ersten Handelstags danach (der Nachtlauf
um 04:30 UTC kennt das Signal vor diesem Schluss). Kosten 0,10 % je Umschlag, Rücksetzer 0,05 % je Seite. Kurse dividendenbereinigt.
Protokoll: Jede Monatsentscheidung ab Papierstart wird in depot_log.jsonl festgeschrieben und danach nie neu berechnet
(Protokoll wächst nur). Festgeschrieben wird nur bei vollständigen Daten; sonst in der nächsten Nacht.

Aufruf:  python depot.py                  Nachtlauf, schreibt depot_data.json und ergänzt depot_log.jsonl
         python depot.py --rueckrechnung  Rückrechnung ab 2002 zur Kontrolle gegen die Tests (schreibt nichts)
Nur Standardbibliothek."""
import bisect
import datetime as dt
import json
import os
import statistics
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "depot_data.json")
LOG = os.path.join(ROOT, "depot_log.jsonl")
START = os.environ.get("DEPOT_START", "2026-10-01")
UA = os.environ.get("EDGAR_UA") or "Signal Radar kontakt@example.com"   # wie core.py; FRED blockt Browser-Kennungen

WEIGHTS = {"kern": 0.40, "gold": 0.10, "intraday": 0.40, "lucky": 0.10}
UNIV = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY", "IBB", "SMH", "KBE", "KRE", "XHB", "ITB", "IAK", "IHI",
        "IYT", "XRT", "XME", "XOP", "OIH", "GDX", "IGV", "ITA", "PBJ", "IYZ", "IYR", "PHO", "KIE", "IHF", "IEZ", "PBW", "XPH",
        "FDN", "VNQ", "SKYY", "XBI", "TAN", "ICLN", "LIT"]          # 41 ETFs wie Test 28 (ohne SOXX, XSD, IYW, IYE, IYH)
TOP = 5                # Anzahl Führer
MIN_VALID = 8          # mindestens so viele ETFs mit 12-1-Momentum, sonst keine Auswahl
CORR_MAX = 0.90        # Cluster-Deckel: Korrelation der Tagesrenditen, ab der zwei ETFs derselbe Cluster sind
CORR_DAYS = 252
TC = 0.001             # Kosten je Umschlag (ETFs, Lucky Punch, Umschichtung Gesamt)
OV_TC = 0.0005         # Rücksetzer je Seite
SPREAD = 0.01          # Finanzierungsaufschlag p.a. über T-Bill
OV_TP, OV_SL, OV_T = 0.05, 0.05, 120
LP_LEV, LP_FEE = 3.0, 0.0095    # nur Rückrechnung vor TQQQ: synthetisch 3x Nasdaq 100, Finanzierung T-Bill + 1 %, Gebühr 0,95 %
NAMES = {"gesamt": "Gesamt 40/10/40/10", "kern": "Kern: Führer-System", "kern_roh": "Kern ohne Cluster-Deckel (Test-28-Fassung)",
         "gold": "Gold (GLD)", "intraday": "Intraday (noch Cash)", "lucky": "Lucky Punch (TQQQ)", "spy": "SPY halten"}


# ---------------------------------------------------------------- Daten
def get(u):
    for i in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")
        except Exception:
            if i == 4:
                raise
            time.sleep(5 * (i + 1))   # Yahoo antwortet gelegentlich mit 429


def yahoo(sym, start):
    """{datum: (open, high, low, close)} dividendenbereinigt; unvollständiger heutiger Balken wird verworfen."""
    p1 = int(dt.datetime.fromisoformat(start).replace(tzinfo=dt.timezone.utc).timestamp())
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?period1={p1}&period2={int(time.time())}&interval=1d&events=div,split"
    r = json.loads(get(u))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    adj = (r["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    now = dt.datetime.now(dt.timezone.utc)
    out = {}
    for k, ts in enumerate(r.get("timestamp") or []):
        c = q["close"][k]
        if not c or c <= 0:
            continue
        d = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()
        if d == now.date() and now.hour < 21:
            continue
        f = (adj[k] / c) if adj and adj[k] else 1.0
        o, h, lo = q["open"][k], q["high"][k], q["low"][k]
        out[d.isoformat()] = (o * f if o else None, h * f if h else None, lo * f if lo else None, c * f)
    return out


def fred(series):
    out = {}
    for line in get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}").splitlines()[1:]:
        a, b = line.split(",")[:2]
        try:
            out[a] = float(b)
        except ValueError:
            pass
    return out


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e, f = b // 4, b % 4, (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return dt.date(y, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def next_session(d):
    """Nächster Börsentag nach d: Werktag, ohne die NYSE-Feiertage, die auf ein Monatsende fallen können
    (Memorial Day = letzter Montag im Mai, Karfreitag)."""
    x = dt.date.fromisoformat(d) + dt.timedelta(days=1)
    while x.weekday() > 4 or (x.month == 5 and x.weekday() == 0 and x.day > 24) or x == easter(x.year) - dt.timedelta(days=2):
        x += dt.timedelta(days=1)
    return x.isoformat()


class Data:
    def __init__(self, start):
        syms = ["SPY", "GLD", "^NDX", "TQQQ"] + UNIV
        raw, self.missing = {}, []
        for s in syms:
            try:
                raw[s] = yahoo(s, start)
            except Exception as e:
                print("Kursdaten fehlen:", s, e)
                raw[s] = {}
            if not raw[s]:
                self.missing.append(s)
            time.sleep(0.3)
        if not raw["SPY"]:
            raise SystemExit("SPY fehlt – Abbruch")
        self.dates = sorted(raw["SPY"])
        n = len(self.dates)
        self.C = {s: [raw[s].get(d, (None,) * 4)[3] for d in self.dates] for s in syms}
        self.O = [raw["SPY"][d][0] for d in self.dates]
        self.H = [raw["SPY"][d][1] for d in self.dates]
        self.L = [raw["SPY"][d][2] for d in self.dates]
        self.R = {}
        for s in syms:          # Tagesrendite gegen den letzten vorhandenen Schluss (höchstens 5 Tage zurück)
            c, rr, last = self.C[s], [None] * n, None
            for i in range(n):
                if c[i] is not None:
                    if last is not None and i - last <= 5:
                        rr[i] = c[i] / c[last] - 1
                    last = i
            self.R[s] = rr
        self.un = fred("UNRATE")
        tb = fred("DTB3")
        self.tbd = sorted(tb)
        self.tb = [tb[k] for k in self.tbd]
        self.me = [i for i in range(n) if self.is_me(i)]

    def is_me(self, i):
        """Letzter Handelstag des Monats. Am Datenende: wenn der nächste Börsentag in einen anderen Monat fällt."""
        d = self.dates[i]
        if i + 1 < len(self.dates):
            return self.dates[i + 1][:7] != d[:7]
        return next_session(d)[:7] != d[:7]

    def at(self, s, i, back=5):
        c = self.C[s]
        for k in range(i, max(-1, i - back - 1), -1):
            if c[k] is not None:
                return c[k]
        return None

    def rf(self, i):
        k = bisect.bisect_right(self.tbd, self.dates[i]) - 1
        return (self.tb[max(0, k)] if self.tb else 0.0) / 100 / 252

    def corr(self, a, b, i):
        x, y = [], []
        for k in range(max(1, i - CORR_DAYS + 1), i + 1):
            u, v = self.R[a][k], self.R[b][k]
            if u is not None and v is not None:
                x.append(u)
                y.append(v)
        if len(x) < 200:
            return None
        try:
            return statistics.correlation(x, y)
        except statistics.StatisticsError:
            return None

    def unrate(self, d):
        """Zum Monatsende d bekannt: Wert des Vormonats (bzw. letzter veröffentlichter) gegen den Schnitt seiner 12 Monate."""
        y, m = int(d[:4]), int(d[5:7])
        ref = f"{y - (m == 1):04d}-{(m - 2) % 12 + 1:02d}-01"
        ks = [k for k in sorted(self.un) if k <= ref]
        if len(ks) < 12:
            return None
        last, avg = self.un[ks[-1]], statistics.mean(self.un[k] for k in ks[-12:])
        return dict(monat=ks[-1][:7], wert=last, schnitt12=round(avg, 2), steigt=last > avg)


# ---------------------------------------------------------------- Entscheidung am Monatsende
def decide(D, i, provisional=False):
    """Entscheidung zum Schluss des Tages i (Monatsende). provisional: Vorschau, als wäre heute Monatsende."""
    before = [k for k in D.me if k < i]
    if len(before) < 12:
        return None
    prev, base = before[-1], before[-12]
    mom = {}
    for s in UNIV:
        a, b = D.at(s, prev), D.at(s, base)
        if a and b:
            mom[s] = a / b - 1
    rank = sorted(mom, key=lambda s: -mom[s])
    ok = len(rank) >= MIN_VALID
    raw = rank[:TOP] if ok else []
    chosen, skipped, filled = [], [], []
    if ok:
        for s in rank:
            if len(chosen) == TOP:
                break
            hit = None
            for c in chosen:
                r = D.corr(s, c, i)
                if r is not None and r >= CORR_MAX:
                    hit = [s, c, round(r, 3)]
                    break
            if hit:
                skipped.append(hit)
            else:
                chosen.append(s)
        for s, _, _ in skipped:
            if len(chosen) < TOP:
                chosen.append(s)
                filled.append(s)

    def ma10(s):
        v = [D.at(s, k) for k in before[-9:] + [i]]
        return None if any(x is None for x in v) or len(v) < 10 else statistics.mean(v)
    spy, spy_ma = D.at("SPY", i), ma10("SPY")
    gld, gld_ma = D.at("GLD", i), ma10("GLD")
    ndx, ndx_ma = D.at("^NDX", i), ma10("^NDX")
    u = D.unrate(D.dates[i])
    below = bool(spy and spy_ma and spy < spy_ma)
    out = below and bool(u and u["steigt"])
    gold_up = bool(gld and gld_ma and gld > gld_ma)
    lucky = bool(ndx and ndx_ma and ndx > ndx_ma)
    kern = ({"GLD": 1.0} if gold_up else {}) if out else {s: 1.0 / TOP for s in chosen}
    kern_roh = {} if out else {s: 1.0 / TOP for s in raw}
    complete = (not provisional) and not [s for s in D.missing] and all(x is not None for x in (spy_ma, gld_ma, ndx_ma)) and u is not None
    return dict(typ="monat", signal_vom=D.dates[i], fuehrer=chosen, fuehrer_ohne_deckel=raw,
                rangliste=[[s, round(mom[s] * 100, 1)] for s in rank[:12]], uebersprungen=skipped, aufgefuellt=filled,
                spy=r2(spy), spy_ma10=r2(spy_ma), spy_unter_ma10=below, arbeitslosigkeit=u, filter_raus=out,
                gold=r2(gld), gold_ma10=r2(gld_ma), gold_trend=gold_up, ndx=r2(ndx), ndx_ma10=r2(ndx_ma), lucky_investiert=lucky,
                ziel_kern=kern, ziel_kern_roh=kern_roh, vollstaendig=complete)


def r2(x):
    return None if x is None else round(x, 2)


# ---------------------------------------------------------------- Rücksetzer-Zusatz (SPY)
def overlay(D, i0, i1):
    """Tägliche Zusatzrendite (auf das Kern-Kapital) und Handelsliste; Signale ab i0-1, Einstiege ab i0."""
    C, n = D.C["SPY"], len(D.dates)
    ov, trades, pos, pending = {}, [], None, False
    s = OV_TC

    def signal(k):
        if k < 199 or C[k] is None:
            return False
        w = [x for x in C[k - 199:k + 1] if x is not None]
        hi = max(x for x in C[k - 19:k + 1] if x is not None)
        return len(w) >= 190 and C[k] > statistics.mean(w) and C[k] <= 0.95 * hi
    pending = signal(i0 - 1)
    for k in range(i0, min(i1, n)):
        rf, fin = D.rf(k), SPREAD / 252
        o, h, lo, c = D.O[k], D.H[k], D.L[k], C[k]
        r = 0.0
        if pending and o:
            pos = dict(e=k, px=o, tp=o * (1 + OV_TP), sl=o * (1 - OV_SL), signal=D.dates[k - 1])
            pending = False
            x = pos["sl"] if lo is not None and lo <= pos["sl"] else (pos["tp"] if h is not None and h >= pos["tp"] else None)
            if x is not None:
                r = (1 - s) ** 2 * x / o - 1 - fin
                trades.append(dict(pos, x=k, xpx=x, grund="Stop" if x == pos["sl"] else "Ziel"))
                pos = None
            else:
                r = (1 - s) * c / o - 1 - rf - fin
        elif pos:
            j, pc = k - pos["e"], C[k - 1]
            x, why = None, None
            if o is not None and o <= pos["sl"]:
                x, why = o, "Stop (Lücke)"
            elif o is not None and o >= pos["tp"]:
                x, why = o, "Ziel (Lücke)"
            elif lo is not None and lo <= pos["sl"]:
                x, why = pos["sl"], "Stop"
            elif h is not None and h >= pos["tp"]:
                x, why = pos["tp"], "Ziel"
            elif j >= OV_T - 1:
                x, why = c, "Zeit"
            if x is not None:
                r = (1 - s) * x / pc - 1 - fin
                trades.append(dict(pos, x=k, xpx=x, grund=why))
                pos = None
            else:
                r = c / pc - 1 - rf - fin
        ov[k] = r
        if pos is None and not pending and signal(k):
            pending = True
    return ov, trades, pos, pending


# ---------------------------------------------------------------- Simulation
def simulate(D, start, frozen=None, lag=1, daily_rebal=False, synth_lp=False):
    """Alle Linien ab start (NAV 1 zum Schluss des Vortags). frozen: {signal_vom: Entscheidung} aus dem Protokoll."""
    n = len(D.dates)
    i0 = next((k for k, d in enumerate(D.dates) if d >= start), None)
    if i0 is None or i0 == 0:
        return None
    frozen = frozen or {}
    dec = {}
    for m in D.me:
        x = m + lag
        if x < i0 or x >= n:
            continue
        z = frozen.get(D.dates[m]) or decide(D, m)
        if z:
            dec[x] = z
    ov, trades, open_pos, pending = overlay(D, i0, n)

    def run_kern(key):
        cash, hold, tgt, navs = 1.0, {}, {}, [1.0]
        for k in range(i0, n):
            for s in list(hold):
                r = D.R[s][k] if s in D.R else None
                hold[s] *= 1 + (r or 0.0)
            cash *= 1 + D.rf(k)
            cash += ov.get(k, 0.0) * navs[-1]
            nav = cash + sum(hold.values())
            if k in dec:
                tgt = dec[k][key]
                new_hold = {s: w * nav for s, w in tgt.items()}
                to = sum(abs(new_hold.get(s, 0) - hold.get(s, 0)) for s in set(new_hold) | set(hold))
                nav -= to * TC
                hold = {s: w * nav for s, w in tgt.items()}
                cash = nav - sum(hold.values())
            elif daily_rebal and tgt:
                hold = {s: w * nav for s, w in tgt.items()}
                cash = nav - sum(hold.values())
            navs.append(cash + sum(hold.values()))
        return navs[1:], hold

    def run_lucky():
        inv, nav, navs = False, 1.0, []
        for k in range(i0, n):
            rf = D.rf(k)
            if inv:
                if synth_lp:
                    r = LP_LEV * (D.R["^NDX"][k] or 0.0) - (LP_LEV - 1) * (rf + SPREAD / 252) - LP_FEE / 252
                else:
                    r = D.R["TQQQ"][k] or 0.0
            else:
                r = rf
            nav *= 1 + r
            if k in dec and dec[k]["lucky_investiert"] != inv:
                inv = dec[k]["lucky_investiert"]
                nav *= 1 - TC
            navs.append(nav)
        return navs, inv

    kern, kern_hold = run_kern("ziel_kern")
    kern_roh, kern_roh_hold = run_kern("ziel_kern_roh")
    lucky, lucky_inv = run_lucky()
    idx = range(i0, n)
    gold, spy, cashl = [], [], []
    g = s_ = c_ = 1.0
    for k in idx:
        g *= 1 + (D.R["GLD"][k] or 0.0)
        s_ *= 1 + (D.R["SPY"][k] or 0.0)
        c_ *= 1 + D.rf(k)
        gold.append(g)
        spy.append(s_)
        cashl.append(c_)
    sub = {"kern": kern, "gold": gold, "intraday": cashl, "lucky": lucky}
    tot, alloc, basev, navg, prevnav = [], None, None, 1.0, 1.0
    for j, k in enumerate(idx):
        if alloc is None:
            alloc = {p: w for p, w in WEIGHTS.items()}
            basev = {p: 1.0 for p in WEIGHTS}
        navg = sum(alloc[p] * sub[p][j] / basev[p] for p in WEIGHTS)
        if j > 0 and D.dates[k][:4] != D.dates[idx[j - 1]][:4]:     # erster Handelstag im neuen Jahr: Umschichtung zum Schluss
            cur = {p: alloc[p] * sub[p][j] / basev[p] for p in WEIGHTS}
            to = sum(abs(cur[p] - WEIGHTS[p] * navg) for p in WEIGHTS)
            navg -= to * TC
            alloc = {p: WEIGHTS[p] * navg for p in WEIGHTS}
            basev = {p: sub[p][j] for p in WEIGHTS}
        tot.append(navg)
    lines = {"gesamt": tot, "kern": kern, "kern_roh": kern_roh, "gold": gold, "intraday": cashl, "lucky": lucky, "spy": spy}
    return dict(i0=i0, dates=[D.dates[k] for k in idx], lines=lines, dec=dec, trades=trades, open=open_pos,
                pending=pending, kern_hold=kern_hold, kern_roh_hold=kern_roh_hold, lucky_inv=lucky_inv)


def stats(dates, nav, a=None, b=None):
    pts = [(d, v) for d, v in zip(dates, nav) if (a is None or d >= a) and (b is None or d <= b)]
    if len(pts) < 2:
        return None
    # Basis: NAV am Vortag des ersten Punkts
    k0 = dates.index(pts[0][0])
    v0 = nav[k0 - 1] if k0 > 0 else 1.0
    vals = [v0] + [v for _, v in pts]
    yrs = len(pts) / 252
    peak, mdd = vals[0], 0.0
    for v in vals:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    by_year, prev = {}, v0
    for d, v in pts:
        by_year.setdefault(d[:4], [prev, v])[1] = v
        prev = v
    yr = {y: e / s - 1 for y, (s, e) in by_year.items()}
    return dict(cagr=(vals[-1] / v0) ** (1 / yrs) - 1 if yrs > 0 else None, mdd=mdd, worst_year=min(yr.values()), years=yr,
                total=vals[-1] / v0 - 1)


# ---------------------------------------------------------------- Protokoll
def read_log():
    if not os.path.exists(LOG):
        return []
    return [json.loads(x) for x in open(LOG, encoding="utf-8") if x.strip()]


def append_log(recs):
    if recs:
        with open(LOG, "a", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


# ---------------------------------------------------------------- Nachtlauf
def next_month_end(today):
    y, m = int(today[:4]), int(today[5:7])
    x = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    while x.weekday() > 4:
        x -= dt.timedelta(days=1)
    if x.isoformat() <= today:
        x = (dt.date(x.year + (x.month == 12), x.month % 12 + 1, 1) + dt.timedelta(days=40)).replace(day=1) - dt.timedelta(days=1)
        while x.weekday() > 4:
            x -= dt.timedelta(days=1)
    return x.isoformat()


def exec_date(D, m):
    """Ausführungstag der Entscheidung vom Monatsende m: nächster Handelstag (am Datenende: nächster Börsentag)."""
    return D.dates[m + 1] if m + 1 < len(D.dates) else next_session(D.dates[m])


def nightly():
    s0 = (dt.date.fromisoformat(min(START, dt.date.today().isoformat())) - dt.timedelta(days=760)).isoformat()
    D = Data(s0)
    today, n = D.dates[-1], len(D.dates)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    log = read_log()
    frozen = {r["signal_vom"]: r for r in log if r.get("typ") == "monat"}
    add = []
    # 1. Monatsentscheidungen festschreiben, deren Ausführung am oder nach dem Papierstart liegt (schon in der Nacht vor der Ausführung)
    for m in D.me:
        if exec_date(D, m) >= START and D.dates[m] not in frozen:
            z = decide(D, m)
            if z and z["vollstaendig"]:
                z = dict(z, ausfuehrung=exec_date(D, m), festgeschrieben=now)
                add.append(z)
                frozen[z["signal_vom"]] = z
    # 2. Papier-Simulation mit den festgeschriebenen Entscheidungen
    S = simulate(D, START, frozen=frozen) if today >= START else None
    if S:
        seen = {(r.get("typ"), r.get("einstieg"), r.get("ausstieg")) for r in log + add}
        for t in S["trades"]:
            rec = dict(typ="ruecksetzer", signal_vom=t["signal"], einstieg=D.dates[t["e"]], kurs_einstieg=r2(t["px"]),
                       ausstieg=D.dates[t["x"]], kurs_ausstieg=r2(t["xpx"]), rendite_pct=round((t["xpx"] / t["px"] - 1) * 100, 2),
                       grund=t["grund"], festgeschrieben=now)
            if ("ruecksetzer", rec["einstieg"], rec["ausstieg"]) not in seen:
                add.append(rec)
        p = S["open"]
        if p and ("ruecksetzer_einstieg", D.dates[p["e"]], None) not in seen:
            add.append(dict(typ="ruecksetzer_einstieg", signal_vom=p["signal"], einstieg=D.dates[p["e"]], kurs_einstieg=r2(p["px"]),
                            ziel=r2(p["tp"]), stop=r2(p["sl"]), festgeschrieben=now))
    append_log(add)
    log += add
    # 3. Anzeige: letzte Monatsentscheidung, ob schon ausgeführt, Vorschau
    last_me = n - 1 if D.is_me(n - 1) else max(k for k in D.me if k < n - 1)
    cur = frozen.get(D.dates[last_me]) or decide(D, last_me)
    done = exec_date(D, last_me) <= today
    prev_me = max(k for k in D.me if k < last_me)
    held = None if done else (frozen.get(D.dates[prev_me]) or decide(D, prev_me))
    preview = None if D.is_me(n - 1) else decide(D, n - 1, provisional=True)
    C = D.C["SPY"]
    sma200 = statistics.mean([x for x in C[-200:] if x is not None])
    hi20 = max(x for x in C[-20:] if x is not None)
    rs = dict(spy=r2(C[-1]), sma200=r2(sma200), hoch20=r2(hi20), ausloeser=r2(0.95 * hi20), ueber_sma200=C[-1] > sma200,
              abstand_hoch20_pct=round((C[-1] / hi20 - 1) * 100, 2))
    if S and S["open"]:
        p = S["open"]
        rs.update(status="offen", einstieg=D.dates[p["e"]], kurs_einstieg=r2(p["px"]), ziel=r2(p["tp"]), stop=r2(p["sl"]),
                  tage=n - 1 - p["e"] + 1, seit_pct=round((C[-1] / p["px"] - 1) * 100, 2))
    elif rs["ueber_sma200"] and C[-1] <= 0.95 * hi20:
        rs.update(status="Signal: Kauf zur nächsten Eröffnung" if today >= START or exec_date(D, n - 1) >= START else "Signal (vor Papierstart)")
    else:
        rs.update(status="keine Position")
    out = dict(stand=today, papierstart=START, gestartet=bool(S), naechste_pruefung=next_month_end(today), gewichte=WEIGHTS,
               namen=NAMES, fehlende_kurse=D.missing, entscheidung=cur, ausgefuehrt=done, ausfuehrung=exec_date(D, last_me),
               gehalten_bis_ausfuehrung=held, vorschau=preview, ruecksetzer=rs, linien={}, reihe=[], protokoll=log[-24:],
               parameter=dict(top=TOP, korrelation_max=CORR_MAX, korrelation_tage=CORR_DAYS, kosten=TC, ruecksetzer_ziel=OV_TP,
                              ruecksetzer_stop=OV_SL, ruecksetzer_tage=OV_T))
    if S:
        L = S["lines"]
        pos = {"kern": (", ".join(sorted(S["kern_hold"])) or "Cash") + (" + SPY-Rücksetzer" if S["open"] else ""),
               "kern_roh": (", ".join(sorted(S["kern_roh_hold"])) or "Cash") + (" + SPY-Rücksetzer" if S["open"] else ""), "gold": "GLD", "intraday": "Cash (T-Bill)", "lucky": "TQQQ" if S["lucky_inv"] else "Cash",
               "spy": "SPY", "gesamt": "40/10/40/10"}
        for k, v in L.items():
            st = stats(S["dates"], v)
            out["linien"][k] = dict(name=NAMES[k], nav=round(v[-1], 4), rendite=round((v[-1] - 1) * 100, 2),
                                    mdd=round(st["mdd"] * 100, 2) if st else 0.0, position=pos.get(k))
        step = max(1, len(S["dates"]) // 260)
        out["reihe"] = [dict(d=d, **{k: round(L[k][j], 4) for k in ("gesamt", "kern", "kern_roh", "lucky", "spy")})
                        for j, d in enumerate(S["dates"]) if j % step == 0 or j == len(S["dates"]) - 1]
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    e = cur or {}
    print("depot_data.json:", today, "| Führer", e.get("fuehrer"), "| Filter", "raus" if e.get("filter_raus") else "investiert",
          "| Lucky", "investiert" if e.get("lucky_investiert") else "Cash", "| Rücksetzer", rs["status"],
          "| neu festgeschrieben:", len(add), "| fehlend:", D.missing)


# ---------------------------------------------------------------- Rückrechnung (Kontrolle)
def backtest():
    D = Data("2000-06-01")
    pct = lambda x: "–" if x is None else f"{x * 100:6.1f} %"
    def show(title, S, keys, periods):
        print(f"\n{title}")
        for a, b in periods:
            print(f"  {a[:4]}–{b[:4]}:")
            for k in keys:
                st = stats(S["dates"], S["lines"][k], a, b)
                if st:
                    print(f"    {NAMES[k]:<44} CAGR {pct(st['cagr'])}  max. DD {pct(st['mdd'])}  schlechtestes Jahr {pct(st['worst_year'])}")
    P = [("2002-02-01", "2026-12-31"), ("2008-01-02", "2026-09-22"), ("2002-02-01", "2013-12-31"), ("2014-01-01", "2026-12-31")]
    A = simulate(D, "2002-02-01", lag=0, daily_rebal=True, synth_lp=True)
    show("Wie im Research gerechnet (Ausführung zum Monatsschluss, Gewichte täglich konstant):", A, ["kern_roh", "kern", "lucky", "spy"], P)
    B = simulate(D, "2002-02-01", lag=1, daily_rebal=False, synth_lp=True)
    show("Wie im Papierbetrieb (Ausführung Schluss erster Handelstag, Positionen laufen im Monat frei):", B,
         ["gesamt", "kern", "kern_roh", "gold", "lucky", "spy"], P)
    print("\nReferenz Research: Test 28 Führer 1x 2008–2026 16,3 % / −45 %; 2002–2026 15,4 %; Test 36 Kern mit Gold-Ausweich 2005–2026 "
          "16,6 % / −45 %; Test 34 Nasdaq 3x mit Filter ab 2000 siehe t34.")
    tr = B["trades"]
    if tr:
        rets = [t["xpx"] / t["px"] - 1 for t in tr]
        print(f"Rücksetzer: {len(tr)} Trades, Treffer {sum(r > 0 for r in rets) / len(rets) * 100:.0f} %, Ø {statistics.mean(rets) * 100:+.2f} %")
    return D, A, B


if __name__ == "__main__":
    if "--rueckrechnung" in sys.argv:
        backtest()
    else:
        nightly()
