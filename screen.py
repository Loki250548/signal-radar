#!/usr/bin/env python3
"""screen.py — Checklisten-Screen über 22 Börsen und drei Papier-Körbe (Test 19, Regel v2), Papier ab 01.10.2026.

Der Code vom 23.09. lag nie im Repo. Diese Fassung setzt die dokumentierte Regel neu um. Alles, was im Test-19-Protokoll
nicht festgelegt war, wurde am 25.09.2026 vor jedem Papierergebnis so bestimmt (steht auch im Dashboard):

Universum   22 Börsen (NYSE, Nasdaq, Shanghai, Shenzhen, Japan Exchange, HKEX, NSE Indien, Euronext, London, TSX, Tadawul,
            Deutsche Börse, KRX, SIX, TWSE, Nasdaq Nordic, ASX, BME, SGX, JSE, B3, Wiener Börse), Aktien ab 2 Mrd. USD
            Börsenwert (Yahoo-Screener). Doppelnotierungen: Depotscheine (ADR/CDR/BDR) und Auslandslinien an Xetra, Mailand,
            Wien, SIX, TSX, B3 und London (Fremdwährung) fallen weg; bleiben mehrere Linien mit gleichem Namen, zählt die in
            Berichtswährung, sonst die umsatzstärkste. Region = Land der Börse.
Momentum    12-1: Schluss am Ende des Vormonats gegen Schluss am Monatsende zwölf Monate vor dem Stichtag (Kursrendite in
            Landeswährung).
Körbe       je 10 Titel, gleichgewichtet, Rangfolge nach 12-1-Momentum über alle Regionen:
  alle      kein Kauf, wenn der Titel die Exit-Regel schon erfüllt; v1/v2 zusätzlich Mindestumsatz 5 Mio. USD je Tag
            (3-Monats-Schnitt), damit nichts Unhandelbares im Korb landet.
  v2        Top-Dezil je Region und Momentum > 0; Gates FCF > 0, ROE ≥ 15 %, Nettoschulden < 2 × EBITDA (fehlende Daten =
            nicht bestanden); kein 200-Tage-Filter beim Einstieg; max. 1 je Korrelations-Cluster (Wochenrenditen, 52
            ISO-Kalenderwochen, r ≥ 0,60), 1 je Branche, 2 je Sektor, mindestens 3 Mid Caps (2–10 Mrd. USD).
  v1        alte Regel: oberes Drittel je Region (ohne Momentum > 0), gleiche Gates, Einstieg nur über der 200-Tage-Linie,
            max. 2 je Sektor.
  pur       Top-Dezil je Region und Momentum > 0, keine Gates, keine Deckel: die 10 umsatzstärksten (Dollar-Umsatz).
Exit        täglich für alle Körbe: Schluss unter der 200-Tage-Linie UND mindestens 25 % unter dem 52-Wochen-Hoch
            (Schlusskurse) → verkaufen, Cash bis zum nächsten Monatswechsel.
Ablauf      Signal zum Monatsschluss (US-Handelstag). Der Nachtlauf danach rechnet den Screen und schreibt die Körbe in
            screen_log.jsonl fest (wächst nur). Kauf und Verkauf je Titel zum ersten Schlusskurs NACH dem Tag der
            Festschreibung (UTC), damit kein Markt vor der Entscheidung gehandelt wird. Kosten 0,3 % je Seite, Cash unverzinst,
            Bewertung in USD (Tageskurse der Währungen), Kursrenditen ohne Dividenden. Vergleich: MSCI World (URTH), SPY.
Grenzen     heutiges Universum (kein Survivorship-Problem vorwärts, aber Fundamentaldaten sind der aktuelle Yahoo-Stand, nicht
            punktgenau), Kursrenditen ohne Dividenden, Region nach Börse statt nach Firmensitz.

Aufruf:  python screen.py              Nachtlauf (Monatsscreen nur nach einem Monatsende, sonst Exit-Prüfung und Bewertung)
         python screen.py --vorschau   Screen zum letzten Handelstag als Vorschau (schreibt nichts ins Protokoll);
                                       bis zum ersten festgeschriebenen Korb macht der Nachtlauf das selbst (höchstens alle 6 Tage)
Nur Standardbibliothek."""
import datetime as dt
import http.cookiejar
import json
import math
import os
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "screen_data.json")
LOG = os.path.join(ROOT, "screen_log.jsonl")
START_SIGNAL = os.environ.get("SCREEN_START", "2026-09-30")     # erstes Signal-Monatsende
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}

CODES = {  # Yahoo-Börsencode: (Börse, Land, Hauptwährung)
    "NYQ": ("NYSE", "USA", "USD"), "ASE": ("NYSE", "USA", "USD"), "NMS": ("Nasdaq", "USA", "USD"), "NGM": ("Nasdaq", "USA", "USD"),
    "NCM": ("Nasdaq", "USA", "USD"), "SHH": ("Shanghai", "China", "CNY"), "SHZ": ("Shenzhen", "China", "CNY"),
    "JPX": ("Japan Exchange", "Japan", "JPY"), "HKG": ("HKEX", "Hongkong", "HKD"), "NSI": ("NSE", "Indien", "INR"),
    "PAR": ("Euronext", "Frankreich", "EUR"), "AMS": ("Euronext", "Niederlande", "EUR"), "BRU": ("Euronext", "Belgien", "EUR"),
    "LIS": ("Euronext", "Portugal", "EUR"), "MIL": ("Euronext", "Italien", "EUR"), "OSL": ("Euronext", "Norwegen", "NOK"),
    "LSE": ("London", "UK", "GBP"), "TOR": ("TSX", "Kanada", "CAD"), "SAU": ("Tadawul", "Saudi-Arabien", "SAR"),
    "GER": ("Deutsche Börse", "Deutschland", "EUR"), "KSC": ("KRX", "Südkorea", "KRW"), "EBS": ("SIX", "Schweiz", "CHF"),
    "TAI": ("TWSE", "Taiwan", "TWD"), "STO": ("Nasdaq Nordic", "Schweden", "SEK"), "CPH": ("Nasdaq Nordic", "Dänemark", "DKK"),
    "HEL": ("Nasdaq Nordic", "Finnland", "EUR"), "ASX": ("ASX", "Australien", "AUD"), "MCE": ("BME", "Spanien", "EUR"),
    "SES": ("SGX", "Singapur", "SGD"), "JNB": ("JSE", "Südafrika", "ZAR"), "SAO": ("B3", "Brasilien", "BRL"),
    "VIE": ("Wiener Börse", "Österreich", "EUR")}
STRICT = {"GER", "MIL", "VIE", "EBS", "TOR", "SAO"}      # hier nur Linien in Berichtswährung (sonst Auslandsnotierung)
MIN_USD, MID_MAX, MIN_ADV = 2e9, 10e9, 5e6
N_KORB, COST, R_CLUSTER = 10, 0.003, 0.60
KOERBE = {"v2": "v2 · Cluster-Deckel", "v1": "v1 · Sektor-Deckel", "pur": "Momentum-Dezil pur"}
BENCH = {"URTH": "MSCI World (URTH)", "SPY": "S&P 500 (SPY)"}


# ------------------------------------------------------------------ Datenzugang
class Yahoo:
    def __init__(self):
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.crumb = None

    def raw(self, url, data=None, tries=5):
        for i in range(tries):
            try:
                h = dict(UA, **({"Content-Type": "application/json"} if data else {}))
                return self.op.open(urllib.request.Request(url, data=data, headers=h), timeout=40).read()
            except urllib.error.HTTPError as e:
                if e.code == 404 or i == tries - 1:
                    raise
                time.sleep(3 * (i + 1))
            except Exception:
                if i == tries - 1:
                    raise
                time.sleep(3 * (i + 1))

    def auth(self):
        if self.crumb:
            return
        try:
            self.op.open(urllib.request.Request("https://fc.yahoo.com", headers=UA), timeout=20)
        except Exception:
            pass                                            # liefert 404, setzt aber das Cookie
        self.crumb = self.raw("https://query1.finance.yahoo.com/v1/test/getcrumb").decode().strip()

    def screener(self, code, min_local):
        self.auth()
        out, off = [], 0
        while True:
            body = json.dumps({"size": 250, "offset": off, "sortField": "intradaymarketcap", "sortType": "DESC", "quoteType": "EQUITY",
                               "query": {"operator": "AND", "operands": [{"operator": "eq", "operands": ["exchange", code]},
                                                                          {"operator": "gt", "operands": ["intradaymarketcap", min_local]}]}}).encode()
            r = json.loads(self.raw(f"https://query1.finance.yahoo.com/v1/finance/screener?crumb={urllib.parse.quote(self.crumb)}&lang=en-US&region=US", body))
            res = r["finance"]["result"][0]
            q = res.get("quotes") or []
            out += q
            off += len(q)
            if not q or off >= res.get("total", 0) or off >= 5000:
                return out
            time.sleep(0.25)

    def spark(self, symbols, rng="14mo"):
        """{symbol: [(datum, schluss)]} täglich; unvollständiger heutiger Balken fällt weg."""
        out = {}
        for i in range(0, len(symbols), 20):
            chunk = symbols[i:i + 20]
            try:
                r = json.loads(self.raw(f"https://query1.finance.yahoo.com/v7/finance/spark?symbols={urllib.parse.quote(','.join(chunk))}&range={rng}&interval=1d"))
            except Exception as e:
                print("spark-Fehler", chunk[:3], e)
                continue
            for x in (r.get("spark") or {}).get("result") or []:
                try:
                    rr = x["response"][0]
                    off = rr["meta"].get("gmtoffset") or 0
                    now_local = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=off)
                    rows = []
                    for t, c in zip(rr.get("timestamp") or [], rr["indicators"]["quote"][0]["close"]):
                        if c is None or c <= 0:
                            continue
                        d = (dt.datetime.fromtimestamp(t, dt.timezone.utc) + dt.timedelta(seconds=off)).date()
                        if d == now_local.date() and now_local.hour < 18:
                            continue
                        rows.append((d.isoformat(), float(c)))
                    dd = {}
                    for d, c in rows:
                        dd[d] = c
                    out[x["symbol"]] = sorted(dd.items())
                except Exception:
                    pass
            time.sleep(0.2)
        return out

    def fundamentals(self, sym):
        self.auth()
        try:
            r = json.loads(self.raw(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(sym)}"
                                    f"?modules=financialData,assetProfile&crumb={urllib.parse.quote(self.crumb)}", tries=3))
            q = r["quoteSummary"]["result"][0]
        except Exception:
            return None
        f, a = q.get("financialData") or {}, q.get("assetProfile") or {}
        v = lambda k: (f.get(k) or {}).get("raw") if isinstance(f.get(k), dict) else None
        return dict(fcf=v("freeCashflow"), roe=v("returnOnEquity"), debt=v("totalDebt"), cash=v("totalCash"), ebitda=v("ebitda"),
                    sektor=a.get("sector"), branche=a.get("industry"), sitz=a.get("country"))


def norm_cur(c):
    return {"GBp": "GBP", "ZAc": "ZAR", "ILA": "ILS"}.get(c, c)


def fx_rates(Y, curs, rng="14mo"):
    """{Währung: [(datum, Einheiten je USD)]}"""
    syms = {c: f"{c}=X" for c in curs if c != "USD"}
    data = Y.spark(list(syms.values()), rng)
    out = {"USD": [("1900-01-01", 1.0)]}
    for c, s in syms.items():
        if data.get(s):
            out[c] = data[s]
    return out


def at(series, date, max_back=7):
    """letzter Wert mit Datum ≤ date (höchstens max_back Tage alt)."""
    lo, hi = 0, len(series)
    while lo < hi:
        m = (lo + hi) // 2
        if series[m][0] <= date:
            lo = m + 1
        else:
            hi = m
    if lo == 0:
        return None
    d, v = series[lo - 1]
    if (dt.date.fromisoformat(date) - dt.date.fromisoformat(d)).days > max_back:
        return None
    return v


def month_end(d, back):
    """letzter Kalendertag des Monats, der „back“ Monate vor dem Monat von d liegt."""
    y, m = d.year, d.month - back
    while m <= 0:
        m += 12
        y -= 1
    return (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).isoformat()


def name_key(n):
    n = re.sub(r"[^a-z0-9 ]", " ", (n or "").lower())
    n = re.sub(r"\b(inc|corp|corporation|co|ltd|limited|plc|ag|se|sa|nv|n v|ab|asa|oyj|spa|s p a|group|holdings?|the|class [a-z])\b", " ", n)
    return re.sub(r"\s+", " ", n).strip()


# ------------------------------------------------------------------ Screen
def universe(Y, fx_now):
    rows, per_code = [], {}
    for code, (boerse, land, cur) in CODES.items():
        rate = fx_now.get(cur, 1.0)
        try:
            q = Y.screener(code, MIN_USD * rate * 0.9)
        except Exception as e:
            print("Screener-Fehler", code, e)
            per_code[code] = "Fehler"
            continue
        kept = 0
        for x in q:
            c, fc = norm_cur(x.get("currency")), x.get("financialCurrency")
            name = x.get("longName") or x.get("shortName") or x["symbol"]
            if re.search(r"\b(ADR|ADS|CDR|BDR|DRC|Depositary)\b", name, re.I) or re.search(r"\bCDR\b", x.get("shortName") or "", re.I):
                continue
            if code in STRICT and fc != c:
                continue
            if code == "LSE" and c != "GBP":
                continue
            r = fx_now.get(c)
            if not r or not x.get("marketCap"):
                continue
            mcap = x["marketCap"] / r
            if mcap < MIN_USD:
                continue
            px = (x.get("regularMarketPrice") or 0) / (100 if x.get("currency") in ("GBp", "ZAc", "ILA") else 1)
            adv = (x.get("averageDailyVolume3Month") or 0) * px / r
            rows.append(dict(sym=x["symbol"], name=name, boerse=boerse, land=land, code=code, cur=x.get("currency"), fcur=fc,
                             mcap_usd=mcap, adv_usd=adv, match=(fc == c)))
            kept += 1
        per_code[code] = kept
        time.sleep(0.3)
    best = {}
    for r in rows:                                          # Doppelnotierungen gleichen Namens
        k = name_key(r["name"])
        b = best.get(k)
        if b is None or (r["match"], r["adv_usd"]) > (b["match"], b["adv_usd"]):
            best[k] = r
    return list(best.values()), per_code


def weekly(series):
    wk = {}
    for d, c in series:
        y, w, _ = dt.date.fromisoformat(d).isocalendar()
        wk[(y, w)] = c
    ks = sorted(wk)
    return {ks[i]: wk[ks[i]] / wk[ks[i - 1]] - 1 for i in range(1, len(ks))}


def corr(a, b):
    ks = sorted(set(a) & set(b))[-52:]
    if len(ks) < 40:
        return None
    try:
        return statistics.correlation([a[k] for k in ks], [b[k] for k in ks])
    except statistics.StatisticsError:
        return None


def run_screen(Y, signal_date):
    D = dt.date.fromisoformat(signal_date)
    fx = fx_rates(Y, sorted({c for _, _, c in CODES.values()} | {"ILS"}))
    fx_now = {c: s[-1][1] for c, s in fx.items()}
    uni, per_code = universe(Y, fx_now)
    print("Universum:", len(uni), per_code)
    px = Y.spark([u["sym"] for u in uni])
    prev_me, base_me = month_end(D, 1), month_end(D, 12)
    for u in uni:
        s = [(d, c) for d, c in px.get(u["sym"], []) if d <= signal_date]
        a, b = at(s, prev_me), at(s, base_me)
        u["mom"] = a / b - 1 if a and b else None
        cl = [c for _, c in s]
        u["last"] = cl[-1] if cl else None
        u["sma200"] = statistics.mean(cl[-200:]) if len(cl) >= 200 else None
        u["hoch52"] = max(cl[-252:]) if len(cl) >= 200 else None
        u["ueber200"] = bool(u["sma200"] and u["last"] > u["sma200"])
        u["exit_jetzt"] = bool(u["sma200"] and u["last"] < u["sma200"] and u["last"] <= 0.75 * u["hoch52"])
        u["weekly"] = weekly(s[-300:]) if s else {}
    valid = [u for u in uni if u["mom"] is not None]
    regions = {}
    for u in valid:
        regions.setdefault(u["land"], []).append(u)
    dec, third = [], []
    for land, L in regions.items():
        L.sort(key=lambda u: -u["mom"])
        dec += [u for u in L[:math.ceil(len(L) / 10)] if u["mom"] > 0]
        third += L[:math.ceil(len(L) / 3)]
    fcache = {}

    def fund(u):
        if u["sym"] not in fcache:
            fcache[u["sym"]] = Y.fundamentals(u["sym"]) or {}
            time.sleep(0.15)
        return fcache[u["sym"]]

    def gates(u):
        f = fund(u)
        fcf, roe, debt, cash, e = f.get("fcf"), f.get("roe"), f.get("debt"), f.get("cash"), f.get("ebitda")
        nd = (debt or 0) - (cash or 0) if debt is not None or cash is not None else None
        ok_fcf = fcf is not None and fcf > 0
        ok_roe = roe is not None and roe >= 0.15
        ok_nd = nd is not None and ((nd <= 0) or (e is not None and e > 0 and nd < 2 * e))
        u.update(fcf=fcf, roe=roe, nd_ebitda=(nd / e if nd is not None and e and e > 0 else None), sektor=f.get("sektor"), branche=f.get("branche"))
        return ok_fcf and ok_roe and ok_nd, dict(fcf=ok_fcf, roe=ok_roe, nd=ok_nd)

    stat = {"universum": len(uni), "mit_momentum": len(valid), "regionen": {k: len(v) for k, v in sorted(regions.items())},
            "dezil": len(dec), "drittel": len(third), "boersen_codes": per_code}

    def pick(cands, need_mid, cluster, max_ind, max_sec, need_200):
        chosen, why, examined = [], {}, 0
        for u in sorted(cands, key=lambda u: -u["mom"]):
            if len(chosen) == N_KORB:
                break
            examined += 1
            if u["exit_jetzt"]:
                why["erfüllt schon die Exit-Regel"] = why.get("erfüllt schon die Exit-Regel", 0) + 1
                continue
            if u["adv_usd"] < MIN_ADV:
                why["Umsatz < 5 Mio. USD/Tag"] = why.get("Umsatz < 5 Mio. USD/Tag", 0) + 1
                continue
            if need_200 and not u["ueber200"]:
                why["unter 200-Tage-Linie"] = why.get("unter 200-Tage-Linie", 0) + 1
                continue
            ok, g = gates(u)
            if not ok:
                for k, v in g.items():
                    if not v:
                        why[f"Gate {k}"] = why.get(f"Gate {k}", 0) + 1
                continue
            mids = sum(c["mcap_usd"] < MID_MAX for c in chosen)
            if need_mid and N_KORB - len(chosen) <= need_mid - mids and u["mcap_usd"] >= MID_MAX:
                why["Platz für Mid Caps reserviert"] = why.get("Platz für Mid Caps reserviert", 0) + 1
                continue
            if max_sec and sum(c.get("sektor") == u.get("sektor") for c in chosen) >= max_sec:
                why["Sektor-Deckel"] = why.get("Sektor-Deckel", 0) + 1
                continue
            if max_ind and u.get("branche") and sum(c.get("branche") == u.get("branche") for c in chosen) >= max_ind:
                why["Branchen-Deckel"] = why.get("Branchen-Deckel", 0) + 1
                continue
            if cluster:
                hit = next((c for c in chosen if (corr(u["weekly"], c["weekly"]) or 0) >= R_CLUSTER), None)
                if hit:
                    u["cluster_mit"] = hit["sym"]
                    why["Korrelations-Cluster"] = why.get("Korrelations-Cluster", 0) + 1
                    continue
            chosen.append(u)
        return chosen, why, examined

    v2, why2, ex2 = pick(dec, 3, True, 1, 2, False)
    v1, why1, ex1 = pick(third, 0, False, 0, 2, True)
    pur = sorted([u for u in dec if not u["exit_jetzt"]], key=lambda u: -u["adv_usd"])[:N_KORB]
    for u in pur:
        fund(u)
        gates(u)
    stat.update(fundamentaldaten_abgerufen=len(fcache), v2_geprueft=ex2, v2_ausschluesse=why2, v1_geprueft=ex1, v1_ausschluesse=why1)
    keep = ("sym", "name", "boerse", "land", "cur", "mcap_usd", "adv_usd", "mom", "ueber200", "sektor", "branche", "fcf", "roe", "nd_ebitda")

    def slim(u):
        x = {k: u.get(k) for k in keep}
        x["mcap_usd"] = round(x["mcap_usd"] / 1e9, 2)
        x["adv_usd"] = round(x["adv_usd"] / 1e6, 1)
        x["mom"] = round(x["mom"] * 100, 1)
        x["roe"] = None if x["roe"] is None else round(x["roe"] * 100, 1)
        x["fcf"] = None if x["fcf"] is None else round(x["fcf"] / 1e9, 3)
        x["nd_ebitda"] = None if x["nd_ebitda"] is None else round(x["nd_ebitda"], 2)
        x["abstand_hoch_pct"] = round((u["last"] / u["hoch52"] - 1) * 100, 1) if u.get("hoch52") else None
        return x
    top_dec = [dict(sym=u["sym"], name=u["name"], land=u["land"], mom=round(u["mom"] * 100, 1))
               for u in sorted(dec, key=lambda u: -u["mom"])[:25]]
    return dict(signal_vom=signal_date, koerbe={"v2": [slim(u) for u in v2], "v1": [slim(u) for u in v1], "pur": [slim(u) for u in pur]},
                stat=stat, top_dezil=top_dec)


# ------------------------------------------------------------------ Protokoll und Bewertung
def read_log():
    return [json.loads(x) for x in open(LOG, encoding="utf-8") if x.strip()] if os.path.exists(LOG) else []


def append_log(recs):
    if recs:
        with open(LOG, "a", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def next_session(d):
    x = dt.date.fromisoformat(d) + dt.timedelta(days=1)
    while x.weekday() > 4:
        x += dt.timedelta(days=1)
    return x.isoformat()


def simulate(log, prices, fx, last_date):
    """NAV je Korb in USD. Kauf/Verkauf je Titel zum ersten Schluss nach dem Festschreibe-Tag."""
    korbs = sorted([r for r in log if r["typ"] == "korb"], key=lambda r: r["signal_vom"])
    exits = [r for r in log if r["typ"] == "exit"]
    dates = sorted({d for s in prices.values() for d, _ in s if d <= last_date})
    if not korbs or not dates:
        return {}
    idx = {s: dict(v) for s, v in prices.items()}
    curs = {}
    for r in korbs:
        for t in r["titel"]:
            curs[t["sym"]] = norm_cur(t["cur"])
    unit = {s: (100 if any(t["sym"] == s and t["cur"] in ("GBp", "ZAc", "ILA") for r in korbs for t in r["titel"]) else 1) for s in curs}
    res = {}
    for k in KOERBE:
        events = []                                          # (fest_datum, art, daten)
        for r in korbs:
            if r["korb"] == k:
                events.append((r["festgeschrieben"][:10], "korb", r))
        for e in exits:
            if e["korb"] == k:
                events.append((e["festgeschrieben"][:10], "exit", e))
        events.sort(key=lambda x: x[0])
        if not events:
            continue
        cash, units, pend_buy, pend_sell, nav_series, trades = 1.0, {}, {}, set(), [], []
        last_px = {}
        start = None
        ei = 0
        target = []
        for d in dates:
            # neue Festschreibungen, die VOR d liegen, werden ab d wirksam (Handel nur am ersten Schluss danach)
            while ei < len(events) and events[ei][0] < d:
                _, art, ev = events[ei]
                if art == "korb":
                    target = [t["sym"] for t in ev["titel"]]
                    for s in list(units):
                        if s not in target:
                            pend_sell.add(s)
                    held = set(units) | set(pend_buy)
                    for s in list(pend_buy):
                        if s not in target:
                            cash += pend_buy.pop(s)
                    newbies = [s for s in target if s not in held]
                    if newbies:
                        pend_buy.update({s: None for s in newbies})
                    start = start or d
                else:
                    s = ev["sym"]
                    if s in units:
                        pend_sell.add(s)
                    if s in pend_buy:
                        cash += pend_buy.pop(s) or 0.0
                ei += 1
            for s in list(units) + list(pend_buy):
                p = idx.get(s, {}).get(d)
                if p is not None:
                    r = at(fx.get(curs[s], [("1900-01-01", 1.0)]), d) or (last_px.get(("fx", s)) or 1.0)
                    last_px[s], last_px[("fx", s)] = p / unit[s], r
            # Verkäufe
            for s in list(pend_sell):
                if idx.get(s, {}).get(d) is not None:
                    val = units.pop(s) * last_px[s] / last_px[("fx", s)]
                    cash += val * (1 - COST)
                    trades.append(dict(datum=d, sym=s, art="Verkauf", wert=round(val, 5)))
                    pend_sell.discard(s)
            # Budget für neue Käufe: gleiche Gewichtung am Tag der Wirksamkeit
            if any(v is None for v in pend_buy.values()):
                nav = cash + sum(u * last_px[s] / last_px[("fx", s)] for s, u in units.items() if s in last_px) \
                      + sum(v for v in pend_buy.values() if v is not None)
                n_open = [s for s, v in pend_buy.items() if v is None]
                per = nav / N_KORB
                for s in n_open:
                    amt = min(per, cash)
                    pend_buy[s] = amt
                    cash -= amt
            for s in list(pend_buy):
                if idx.get(s, {}).get(d) is not None and s in last_px:
                    amt = pend_buy.pop(s) or 0.0
                    units[s] = units.get(s, 0) + amt * (1 - COST) / (last_px[s] / last_px[("fx", s)])
                    trades.append(dict(datum=d, sym=s, art="Kauf", wert=round(amt, 5)))
            if start:
                nav = cash + sum(v or 0 for v in pend_buy.values()) + sum(u * last_px[s] / last_px[("fx", s)] for s, u in units.items())
                nav_series.append((d, nav))
        res[k] = dict(reihe=nav_series, units=units, pend_buy=pend_buy, pend_sell=sorted(pend_sell), trades=trades[-40:], cash=cash)
    return res


def mdd(series):
    peak, m = -1, 0.0
    for _, v in series:
        peak = max(peak, v)
        m = min(m, v / peak - 1)
    return m


def nightly(preview_only=False):
    Y = Yahoo()
    spy = Y.spark(["SPY"], "1mo").get("SPY") or []
    if not spy:
        raise SystemExit("SPY-Kurse fehlen – Abbruch")
    last = spy[-1][0]
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    log = read_log()
    old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    add, fehler = [], []
    # 1. Monatsscreen nach einem Monatsende (höchstens 7 Tage nachholen)
    month_ends = [d for i, (d, _) in enumerate(spy) if (spy[i + 1][0][:7] != d[:7] if i + 1 < len(spy) else next_session(d)[:7] != d[:7])]
    due = [d for d in month_ends if d >= START_SIGNAL and not any(r["typ"] == "korb" and r["signal_vom"] == d for r in log)
           and (dt.date.fromisoformat(last) - dt.date.fromisoformat(d)).days <= 7]
    vorschau = old.get("vorschau")
    stale = not vorschau or (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(vorschau["erstellt"])).days >= 6
    if preview_only or (not due and not any(r["typ"] == "korb" for r in log) and stale):     # Vorschau bis zum ersten Korb
        try:
            vorschau = dict(run_screen(Y, last), erstellt=now)
        except Exception as e:
            fehler.append(f"Vorschau: {type(e).__name__}: {e}")
    elif due:
        d = due[-1]
        try:
            S = run_screen(Y, d)
            if all(len(v) == N_KORB for v in S["koerbe"].values()) and S["stat"]["universum"] > 3000:
                for k, titel in S["koerbe"].items():
                    add.append(dict(typ="korb", korb=k, signal_vom=d, titel=titel, festgeschrieben=now,
                                    stat=S["stat"] if k == "v2" else None))
                vorschau = None
                old["letzter_screen"] = dict(signal_vom=d, stat=S["stat"], top_dezil=S["top_dezil"])
            else:
                fehler.append(f"Screen {d} unvollständig (Universum {S['stat']['universum']}, Körbe "
                              f"{ {k: len(v) for k, v in S['koerbe'].items()} }) – nicht festgeschrieben, neuer Versuch nächste Nacht")
        except Exception as e:
            fehler.append(f"Screen {d}: {type(e).__name__}: {e} – neuer Versuch nächste Nacht")
    log_all = log + add
    # 2. Kurse der Korbtitel und Exit-Prüfung
    korbs = [r for r in log_all if r["typ"] == "korb"]
    syms = sorted({t["sym"] for r in korbs for t in r["titel"]})
    first = min((r["festgeschrieben"][:10] for r in korbs), default=None)
    rng = "2y" if not first else ("14mo" if (dt.date.today() - dt.date.fromisoformat(first)).days < 60 else
                                  "2y" if (dt.date.today() - dt.date.fromisoformat(first)).days < 300 else "5y")
    prices = Y.spark(syms + list(BENCH), rng) if syms else {}
    curs = sorted({norm_cur(t["cur"]) for r in korbs for t in r["titel"]})
    fx = fx_rates(Y, curs, rng) if curs else {}
    current = {}
    for k in KOERBE:
        ks = [r for r in korbs if r["korb"] == k]
        if ks:
            current[k] = max(ks, key=lambda r: r["signal_vom"])
    exited = {(e["korb"], e["sym"], e["signal_korb"]) for e in log_all if e["typ"] == "exit"}
    for k, r in current.items():
        for t in r["titel"]:
            s = [x for x in prices.get(t["sym"], [])]
            if len(s) < 200:
                continue
            if (k, t["sym"], r["signal_vom"]) in exited:
                continue
            # nur nach dem Einstieg prüfen
            if not any(d > r["festgeschrieben"][:10] for d, _ in s):
                continue
            cl = [c for _, c in s]
            sma, hi = statistics.mean(cl[-200:]), max(cl[-252:])
            if cl[-1] < sma and cl[-1] <= 0.75 * hi:
                add.append(dict(typ="exit", korb=k, sym=t["sym"], name=t["name"], signal_korb=r["signal_vom"], signal_vom=s[-1][0],
                                schluss=round(cl[-1], 4), sma200=round(sma, 4), hoch52=round(hi, 4), festgeschrieben=now))
    append_log(add)
    log_all = log + add
    # 3. Bewertung
    sim = simulate(log_all, prices, fx, last) if korbs else {}
    lines, members = {}, {}
    start_d = min((v["reihe"][0][0] for v in sim.values() if v["reihe"]), default=None)
    for k, v in sim.items():
        R = v["reihe"]
        if R:
            lines[k] = dict(name=KOERBE[k], nav=round(R[-1][1], 5), rendite=round((R[-1][1] / R[0][1] - 1) * 100, 2) if R[0][1] else None,
                            mdd=round(mdd(R) * 100, 2), start=R[0][0], cash_anteil=round(v["cash"] / R[-1][1] * 100, 1) if R[-1][1] else None)
    for b, nm in BENCH.items():
        s = [(d, c) for d, c in prices.get(b, []) if start_d and d >= start_d]
        if len(s) > 1:
            lines[b] = dict(name=nm, nav=round(s[-1][1] / s[0][1], 5), rendite=round((s[-1][1] / s[0][1] - 1) * 100, 2), mdd=round(mdd(s) * 100, 2), start=s[0][0])
    exits_by = {(e["korb"], e["sym"], e["signal_korb"]): e for e in log_all if e["typ"] == "exit"}
    for k, r in current.items():
        rows = []
        for t in r["titel"]:
            s = prices.get(t["sym"], [])
            ent = next((c for d, c in s if d > r["festgeschrieben"][:10]), None)
            cl = [c for _, c in s]
            e = exits_by.get((k, t["sym"], r["signal_vom"]))
            rows.append(dict(t, einstieg=ent, kurs=cl[-1] if cl else None, seit_pct=round((cl[-1] / ent - 1) * 100, 1) if ent and cl else None,
                             sma_abstand=round((cl[-1] / statistics.mean(cl[-200:]) - 1) * 100, 1) if len(cl) >= 200 else None,
                             hoch_abstand=round((cl[-1] / max(cl[-252:]) - 1) * 100, 1) if len(cl) >= 200 else None,
                             exit=e["signal_vom"] if e else None))
        members[k] = dict(signal_vom=r["signal_vom"], festgeschrieben=r["festgeschrieben"], titel=rows)
    step = 1
    series = {}
    for k, v in sim.items():
        series[k] = [[d, round(x, 5)] for d, x in v["reihe"]][::step][-400:]
    for b in BENCH:
        s = [(d, c) for d, c in prices.get(b, []) if start_d and d >= start_d]
        if s:
            series[b] = [[d, round(c / s[0][1], 5)] for d, c in s][-400:]
    out = dict(stand=last, erstellt=now, start_signal=START_SIGNAL, koerbe_namen=KOERBE, bench_namen=BENCH, linien=lines,
               aktuell=members, reihen=series, vorschau=vorschau, letzter_screen=old.get("letzter_screen"),
               naechster_screen=next_month(last), fehler=fehler, protokoll=[{k: v for k, v in r.items() if k not in ("titel", "stat")}
                                                                          for r in log_all][-40:],
               parameter=dict(n=N_KORB, kosten_pct=COST * 100, r_cluster=R_CLUSTER, min_mrd_usd=MIN_USD / 1e9, mid_max_mrd_usd=MID_MAX / 1e9,
                              min_umsatz_mio_usd=MIN_ADV / 1e6))
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("screen_data.json:", last, "| neu im Protokoll:", len(add), "| Linien:", {k: v.get("rendite") for k, v in lines.items()}, "| Fehler:", fehler)


def next_month(today):
    d = dt.date.fromisoformat(today)
    x = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1) - dt.timedelta(days=1)
    while x.weekday() > 4:
        x -= dt.timedelta(days=1)
    if x.isoformat() <= today:
        y = dt.date(x.year + (x.month == 12), x.month % 12 + 1, 28) + dt.timedelta(days=4)
        x = y - dt.timedelta(days=y.day)
        while x.weekday() > 4:
            x -= dt.timedelta(days=1)
    return x.isoformat()


if __name__ == "__main__":
    nightly(preview_only="--vorschau" in sys.argv)
