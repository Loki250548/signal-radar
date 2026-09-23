#!/usr/bin/env python3
"""core.py — Kernportfolio "Surfen mit Risiko", Papierbetrieb (Tests 9, 11 und v3 vom 21.09.2026).

Drei Linien je Instrument (S&P 500 = SPY, Nasdaq 100 = QQQ), Papierstart 01.10.2026:
  Halten          1x, nie handeln (Vergleichslinie)
  Trendfilter     LEV x, wenn der Index am Monatsende ueber seiner 200-Tage-Linie schliesst; sonst Ausweich
  Konjunkturfilter LEV x, ausser der Index liegt unter der 200-Tage-Linie UND die US-Arbeitslosenquote
                  (letzter veroeffentlichter Wert) liegt ueber ihrem 12-Monats-Schnitt; sonst Ausweich
Ausweich: Gold (GLD), falls Gold ueber 200-Tage-Linie und 12-Monats-Rendite > 0, sonst Cash (T-Bill).
Signal: Schluss des letzten Handelstags im Monat. Ausfuehrung: Schluss des ersten Handelstags danach.
Hebel taeglich angepasst (entspricht Hebel-ETF), Finanzierung T-Bill + 1 %, 0,1 % Kosten je Wechsel.
Kein Kapital, nur Papier. Schreibt core_data.json. Nur Standardbibliothek."""
import urllib.request, json, os, time, datetime as dt, statistics

LEV = 1.5                      # Platzhalter fuer den Papierbetrieb; Hebel ist Herwigs Entscheidung
START = os.environ.get("CORE_START", "2026-10-01")   # Papierstart
SPREAD = 0.01                  # Finanzierungsaufschlag p.a. ueber T-Bill
TC = 0.001                     # Kosten je Wechsel
UA = os.environ.get("EDGAR_UA") or "Signal Radar kontakt@example.com"
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "core_data.json")

def get(u):
    for i in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")
        except Exception:
            if i == 4: raise
            time.sleep(5 * (i + 1))   # Yahoo antwortet gelegentlich mit 429

def px(sym, years=3):
    p1 = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365 * years)).timestamp()); p2 = int(time.time())
    d = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1={p1}&period2={p2}&interval=1d&events=div"))["chart"]["result"][0]
    q = d["indicators"]["quote"][0]; adj = d["indicators"].get("adjclose", [{}])[0].get("adjclose")
    rows = [(dt.datetime.fromtimestamp(x, dt.timezone.utc).date().isoformat(), c, a if adj else c) for x, c, a in zip(d["timestamp"], q["close"], adj or q["close"]) if c]
    return rows  # (datum, schluss, adj. schluss)

def fred(series):
    out = {}
    for line in get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}").splitlines()[1:]:
        a, b = line.split(",")[:2]
        try: out[a] = float(b)
        except ValueError: pass
    return out

# ---------- Daten ----------
S = {k: px(v) for k, v in {"SPX": "SPY", "NDX": "QQQ", "GOLD": "GLD"}.items()}
dates = [r[0] for r in S["SPX"]]
close = {k: {r[0]: r[1] for r in v} for k, v in S.items()}
adj = {k: {r[0]: r[2] for r in v} for k, v in S.items()}
un = fred("UNRATE"); tb = fred("DTB3")
tbd = sorted(tb)

def tbill(d):                       # Tagessatz T-Bill (annualisiert / 252)
    i = max(0, min(len(tbd) - 1, __import__("bisect").bisect_right(tbd, d) - 1)); return tb[tbd[i]] / 100 / 252

def ma(k, d, n=200):
    ix = dates.index(d); w = [close[k][x] for x in dates[max(0, ix - n + 1):ix + 1] if x in close[k]]
    return statistics.mean(w) if len(w) >= n * 0.9 else None

def month_ends():
    """Abgeschlossene Monatsenden: letzter Handelstag, auf den ein Tag eines anderen Monats folgt."""
    return [d for i, d in enumerate(dates[:-1]) if dates[i + 1][:7] != d[:7]]

def unrate_state(d):
    """Zum Stichtag d bekannt: Werte, deren Monat mindestens ~5 Wochen zurueckliegt (Veroeffentlichung Anfang Folgemonat)."""
    cut = (dt.date.fromisoformat(d) - dt.timedelta(days=33)).isoformat()
    ks = [k for k in sorted(un) if k <= cut]
    if len(ks) < 12: return None
    last = un[ks[-1]]; avg = statistics.mean(un[k] for k in ks[-12:])
    return dict(monat=ks[-1][:7], wert=last, schnitt12=round(avg, 2), steigt=last > avg)

def gold_ok(d):
    m = ma("GOLD", d); ix = dates.index(d)
    back = dates[max(0, ix - 252)]
    return bool(m and close["GOLD"].get(d) and close["GOLD"][d] > m and back in close["GOLD"] and close["GOLD"][d] > close["GOLD"][back])

def signal(k, d, rule):
    m = ma(k, d); above = bool(m and close[k][d] > m); u = unrate_state(d)
    if rule == "halten": inv = True
    elif rule == "trend": inv = above
    else: inv = not ((not above) and bool(u and u["steigt"]))
    return inv, above, u

# ---------- Papier-Simulation ab START ----------
ME = month_ends()
def simulate(k, rule):
    lev = 1.0 if rule == "halten" else LEV
    start_ix = next((i for i, d in enumerate(dates) if d >= START), None)
    log = []; nav = 1.0; peak = 1.0; mdd = 0.0; pos = None; series = []
    if start_ix is None or start_ix == 0: return dict(nav=None, log=log, position=None, mdd=None, serie=[])
    # Signal, das fuer Tag i gilt: letztes Monatsende vor Tag i (Ausfuehrung am ersten Handelstag danach)
    for i in range(start_ix, len(dates)):
        d, dp = dates[i], dates[i - 1]
        sig_day = max([m for m in ME if m < d], default=None)
        if sig_day is None: continue
        inv, above, u = signal(k, sig_day, rule)
        want = k if inv else ("GOLD" if gold_ok(sig_day) else "CASH")
        if want != pos:
            if pos is not None: nav *= 1 - TC * lev
            pos = want; log.append(dict(ab=d, signal_vom=sig_day, position={"SPX": "S&P 500", "NDX": "Nasdaq 100", "GOLD": "Gold", "CASH": "Cash"}[want], ueber_200=above, arbeitslosigkeit_steigt=None if u is None else u["steigt"]))
        rf = tbill(dp)
        if pos == "CASH": r = rf
        elif pos == "GOLD": r = adj["GOLD"][d] / adj["GOLD"][dp] - 1 if d in adj["GOLD"] and dp in adj["GOLD"] else 0.0
        else: r = lev * (adj[k][d] / adj[k][dp] - 1) - (lev - 1) * (rf + SPREAD / 252)
        nav *= 1 + r; peak = max(peak, nav); mdd = min(mdd, nav / peak - 1); series.append((d, round(nav, 4)))
    return dict(nav=round(nav, 4), rendite=round((nav - 1) * 100, 2), mdd=round(mdd * 100, 2), position=log[-1]["position"] if log else None, log=log[-12:], serie=series[-260:])

# ---------- aktueller Stand ----------
today = dates[-1]; last_me = ME[-1]
# naechster Pruefstichtag: letzter Handelstag des laufenden Monats (Naeherung: letzter Kalendertag, Mo-Fr)
y, mth = int(today[:4]), int(today[5:7]); nxt = (dt.date(y + (mth == 12), (mth % 12) + 1, 1) - dt.timedelta(days=1))
while nxt.weekday() > 4: nxt -= dt.timedelta(days=1)
if nxt.isoformat() <= today:
    nxt = (dt.date(nxt.year + (nxt.month == 12), (nxt.month % 12) + 1, 1) + dt.timedelta(days=40)).replace(day=1) - dt.timedelta(days=1)
    while nxt.weekday() > 4: nxt -= dt.timedelta(days=1)
out = dict(stand=today, papierstart=START, hebel=LEV, naechste_pruefung=nxt.isoformat(), regeln=dict(
    halten="1x, nie handeln", trend=f"{LEV}x ueber der 200-Tage-Linie am Monatsende, sonst Gold/Cash",
    konjunktur=f"{LEV}x, ausser Index unter 200-Tage-Linie UND Arbeitslosenquote ueber 12-Monats-Schnitt; dann Gold/Cash",
    ausweich="Gold, wenn ueber 200-Tage-Linie und 12-Monats-Rendite positiv; sonst Cash (T-Bill)"), instrumente=[], arbeitslosigkeit=unrate_state(today), gold=dict(ausweich_aktiv=gold_ok(today), kurs=close["GOLD"].get(today), ma200=None if ma("GOLD", today) is None else round(ma("GOLD", today), 2)))
for k, nm in [("SPX", "S&P 500"), ("NDX", "Nasdaq 100")]:
    m = ma(k, today); ms = ma(k, last_me)
    inst = dict(key=k, name=nm, kurs=close[k][today], ma200=round(m, 2) if m else None, abstand_pct=round((close[k][today] / m - 1) * 100, 2) if m else None,
                heute_ueber=bool(m and close[k][today] > m), signal_monatsende=dict(datum=last_me, ueber_200=bool(ms and close[k][last_me] > ms)),
                linien={}, reihe=[])
    for rule in ("halten", "trend", "konjunktur"):
        inv, above, u = signal(k, last_me, rule)
        inst["linien"][rule] = dict(signal=("investiert" if inv else ("Gold" if gold_ok(last_me) else "Cash")), papier=simulate(k, rule))
    ix = dates.index(today); wk = dates[max(0, ix - 520):ix + 1][::5]
    inst["reihe"] = [dict(d=d, k=round(close[k][d], 2), m=(lambda v: None if v is None else round(v, 2))(ma(k, d))) for d in wk]
    out["instrumente"].append(inst)
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
print("core_data.json:", today, {i["name"]: {r: i["linien"][r]["signal"] for r in i["linien"]} for i in out["instrumente"]}, "Arbeitslosigkeit:", out["arbeitslosigkeit"])
