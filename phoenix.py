"""Phönix-Korb — Papierbetrieb (Test 56/56b, Vorab-Festlegung claude/phoenix_korb_vorab.md vom 26.09.2026)

Signal      zum Monatsschluss: Kurs ≥ 50 % unter dem höchsten Monatsschluss der letzten 36 Monate UND Monatsschluss ≥ höchster
            Schluss der vorherigen 11 Monate (erstes neues 12-Monats-Hoch nach einem Absturz). „streng“: ≥ 70 % unter dem Hoch.
Universum   32 Börsen wie screen.py, Börsenwert ≥ 300 Mio. USD, Tagesumsatz ≥ 1 Mio. USD, ohne Finanzen, Basiskonsum, Versorger,
            Immobilien.
Körbe       „Gewinn“ (Nettogewinn der letzten 12 Monate > 0, Yahoo-Stand zum Signal) und „Verlust“ (≤ 0). Je Korb höchstens 30
            Positionen, je 1/30 des Korbwerts beim Einstieg; mehr Signale als freie Plätze → tiefster Absturz zuerst.
Handel      Einstieg zum ersten Schluss nach der Festschreibung (UTC-Datum), Ausstieg nach 365 Tagen (Hauptlinie). Vergleichslinie:
            zusätzlich Exit, sobald der Schluss unter der 200-Tage-Linie UND ≥ 25 % unter dem 52-Wochen-Hoch liegt. 0,3 % je Seite,
            Bewertung in USD ohne Dividenden, freies Geld unverzinst. Vergleich: MSCI World (URTH).
Marktlage   zum Signal gekennzeichnet („Krise“: S&P unter 10-Monats-Linie oder ≥ 20 % unter 12-Monats-Hoch oder VIX ≥ 30).
Protokoll   phoenix_log.jsonl wächst nur; Signale und Einstiegskurse werden festgeschrieben und nie neu berechnet.

Aufruf:  python phoenix.py              Nachtlauf (Monatsscreen nach einem Monatsende ab START_SIGNAL, sonst Bewertung)
         python phoenix.py --vorschau   Screen zum letzten vollständigen Monat als Vorschau (schreibt nichts ins Protokoll)
Nur Standardbibliothek; nutzt Datenzugang und Universum aus screen.py."""
import datetime as dt
import json
import os
import sys
import time
import urllib.parse

import screen as S

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "phoenix_data.json")
LOG = os.path.join(ROOT, "phoenix_log.jsonl")
START_SIGNAL = os.environ.get("PHOENIX_START", "2026-09-30")
MIN_USD, MIN_ADV, MAX_POS, COST, HOLD_DAYS = 3e8, 1e6, 30, 0.003, 365
DD_MIN, DD_STRENG = -0.50, -0.70
EXCL = {"Financial Services", "Consumer Defensive", "Utilities", "Real Estate"}
KOERBE = {"gewinn": "Phönix Gewinn", "verlust": "Phönix Verlust"}


def now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_log():
    return [json.loads(x) for x in open(LOG, encoding="utf-8") if x.strip()] if os.path.exists(LOG) else []


def append_log(recs):
    if recs:
        with open(LOG, "a", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def last_complete_month(today):
    """Letzter Monat, dessen Monatsende vor heute liegt (YYYY-MM) und das Datum seines letzten Werktags."""
    first = today.replace(day=1)
    me = first - dt.timedelta(days=1)
    d = me
    while d.weekday() > 4:
        d -= dt.timedelta(days=1)
    return me.strftime("%Y-%m"), d.isoformat()


def spark_monthly(Y, symbols):
    """{symbol: [(YYYY-MM, schluss)]} Monatsschlüsse der letzten 5 Jahre."""
    out = {}
    for i in range(0, len(symbols), 20):
        chunk = symbols[i:i + 20]
        try:
            r = json.loads(Y.raw("https://query1.finance.yahoo.com/v7/finance/spark?symbols=" + urllib.parse.quote(",".join(chunk)) + "&range=5y&interval=1mo"))
        except Exception as e:
            print("spark-Fehler", chunk[:3], e)
            continue
        for x in (r.get("spark") or {}).get("result") or []:
            try:
                rr = x["response"][0]
                out[x["symbol"]] = [(dt.datetime.utcfromtimestamp(t).strftime("%Y-%m"), float(c))
                                    for t, c in zip(rr.get("timestamp") or [], rr["indicators"]["quote"][0]["close"]) if c]
            except Exception:
                pass
        time.sleep(0.15)
    return out


def profile(Y, sym):
    Y.auth()
    try:
        r = json.loads(Y.raw(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(sym)}"
                             f"?modules=assetProfile,defaultKeyStatistics,financialData&crumb={urllib.parse.quote(Y.crumb)}", tries=3))
        q = r["quoteSummary"]["result"][0]
    except Exception:
        return None
    a, k, f = q.get("assetProfile") or {}, q.get("defaultKeyStatistics") or {}, q.get("financialData") or {}
    raw = lambda d, key: (d.get(key) or {}).get("raw") if isinstance(d.get(key), dict) else None
    ni = raw(k, "netIncomeToCommon")
    if ni is None:
        pm = raw(f, "profitMargins")
        ni = None if pm is None else pm
    return dict(sektor=a.get("sector"), branche=a.get("industry"), gewinn=None if ni is None else ni > 0)


def marktlage(Y):
    d = Y.spark(["^GSPC", "^VIX"], "14mo")
    spx, vix = d.get("^GSPC") or [], d.get("^VIX") or []
    if not spx:
        return None
    months = {}
    for day, c in spx:
        months[day[:7]] = c
    closes = [months[m] for m in sorted(months)]
    ma10 = sum(closes[-10:]) / min(10, len(closes))
    hi = max(c for _, c in spx[-252:])
    last, v = spx[-1][1], (vix[-1][1] if vix else None)
    krise = last < ma10 or last <= 0.8 * hi or (v is not None and v >= 30)
    return dict(datum=spx[-1][0], sp500=round(last, 2), ma10=round(ma10, 2), abstand_hoch_pct=round((last / hi - 1) * 100, 1),
                vix=None if v is None else round(v, 2), krise=krise)


def run_screen(Y, month):
    """Signale zum Monat „month“ (YYYY-MM)."""
    S.MIN_USD = MIN_USD
    curs = sorted({v[2] for v in S.CODES.values()} | {"GBP", "ZAR", "ILS"})
    fx = S.fx_rates(Y, curs, "5d")
    fx_now = {c: s[-1][1] for c, s in fx.items()}
    uni, per_code = S.universe(Y, fx_now)
    uni = [u for u in uni if u["adv_usd"] >= MIN_ADV]
    M = spark_monthly(Y, [u["sym"] for u in uni])
    cands = []
    for u in uni:
        ser = [(m, c) for m, c in M.get(u["sym"], []) if m <= month]
        if len(ser) < 37 or ser[-1][0] != month:
            continue
        p = [c for _, c in ser]
        hi36 = max(p[-37:])
        dd = p[-1] / hi36 - 1
        if dd <= DD_MIN and p[-1] >= max(p[-12:-1]):
            cands.append(dict(sym=u["sym"], name=u["name"], land=u["land"], cur=u["cur"], mcap_usd=round(u["mcap_usd"] / 1e9, 3),
                              adv_usd=round(u["adv_usd"] / 1e6, 2), schluss=round(p[-1], 4), abstand_36m_hoch_pct=round(dd * 100, 1),
                              vom_24m_tief_pct=round((p[-1] / min(p[-25:]) - 1) * 100, 1), streng=dd <= DD_STRENG))
    out = []
    for c in cands:
        pr = profile(Y, c["sym"]) or {}
        c.update(sektor=pr.get("sektor"), branche=pr.get("branche"), gewinn=pr.get("gewinn"))
        if c["sektor"] in EXCL:
            continue
        c["korb"] = "gewinn" if c["gewinn"] is True else ("verlust" if c["gewinn"] is False else None)
        out.append(c)
        time.sleep(0.1)
    out.sort(key=lambda c: c["abstand_36m_hoch_pct"])
    stat = dict(universum=len(uni), mit_kursen=len(M), signale_roh=len(cands), signale=len(out))
    return out, stat


# ------------------------------------------------------------------ Bewertung
def daily_usd(Y, syms_cur):
    """{sym: [(datum, schluss_usd)]} täglich, 2 Jahre."""
    data = Y.spark(sorted(syms_cur), "2y")
    curs = sorted({S.norm_cur(c) for c in syms_cur.values()} - {"USD"})
    fx = S.fx_rates(Y, curs, "2y") if curs else {"USD": [("1900-01-01", 1.0)]}
    out = {}
    for s, ser in data.items():
        c = syms_cur.get(s, "USD")
        div = 100 if c in ("GBp", "ZAc", "ILA") else 1
        fc = S.norm_cur(c)
        rows = []
        for d, v in ser:
            r = 1.0 if fc == "USD" else S.at(fx.get(fc, []), d)
            if r:
                rows.append((d, v / div / r))
        out[s] = rows
    return out


def simulate(log, px, urth, today):
    sig = [r for r in log if r.get("typ") == "signal"]
    ent = {(r["korb"], r["sym"], r["signal_vom"]): r for r in log if r.get("typ") == "einstieg"}
    if not sig:
        return {}, [], []
    cal = sorted({d for ser in px.values() for d, _ in ser} | {d for d, _ in urth})
    first = min(r["festgeschrieben"][:10] for r in sig)
    cal = [d for d in cal if d > first]
    lines, positions, new_entries = {}, [], []
    for korb in KOERBE:
        for variante in ("haupt", "exit"):
            cash, pos, navs = 1.0, [], []
            queue = [(r["festgeschrieben"][:10], r["signal_vom"], s) for r in sig for s in r["neu"].get(korb, [])]
            for d in cal:
                for p in pos:                                     # Bewertung
                    v = S.at(px.get(p["sym"], []), d)
                    if v:
                        p["wert"] = p["stk"] * v
                        p["letzt"] = v
                        p["hist"].append(v)
                nav = cash + sum(p["wert"] for p in pos)
                for p in list(pos):                               # Ausstiege
                    held = (dt.date.fromisoformat(d) - dt.date.fromisoformat(p["ein_datum"])).days
                    h = p["hist"]
                    rule = variante == "exit" and len(h) >= 200 and h[-1] < sum(h[-200:]) / 200 and h[-1] <= 0.75 * max(h[-252:])
                    if held >= HOLD_DAYS or rule:
                        cash += p["wert"] * (1 - COST)
                        p.update(aus_datum=d, grund="12 Monate" if held >= HOLD_DAYS else "Exit-Regel")
                        pos.remove(p)
                        if variante == "haupt":
                            positions.append(p)
                nav = cash + sum(p["wert"] for p in pos)
                for q in [q for q in queue if q[0] < d]:              # Einstiege
                    queue.remove(q)
                    ser = px.get(q[2], [])
                    first_px = next(((dd, v) for dd, v in ser if dd > q[0]), None)
                    if not first_px or first_px[0] != d or len(pos) >= MAX_POS:
                        if first_px and first_px[0] > d:
                            queue.append(q)
                        continue
                    key = (korb, q[2], q[1])
                    e = ent.get(key)
                    kurs = e["kurs_usd"] if e else first_px[1]
                    if not e and variante == "haupt":
                        new_entries.append(dict(typ="einstieg", korb=korb, sym=q[2], signal_vom=q[1], datum=d, kurs_usd=round(kurs, 6), festgeschrieben=now_iso()))
                    hist = [v for dd, v in ser if dd <= d]
                    if variante == "exit" and len(hist) >= 200 and hist[-1] < sum(hist[-200:]) / 200 and hist[-1] <= 0.75 * max(hist[-252:]):
                        continue                                  # wie screen.py: kein Kauf bei erfüllter Exit-Regel
                    amt = min(cash, nav / MAX_POS)
                    if amt <= 0:
                        continue
                    cash -= amt
                    pos.append(dict(sym=q[2], korb=korb, signal_vom=q[1], ein_datum=d, ein_kurs=kurs, stk=amt * (1 - COST) / kurs,
                                    wert=amt * (1 - COST), letzt=kurs, hist=hist))
                navs.append((d, round(cash + sum(p["wert"] for p in pos), 5)))
            lines[f"{korb}_{variante}"] = navs
            if variante == "haupt":
                positions += [dict(p, offen=True) for p in pos]
    b0 = S.at(urth, cal[0]) if cal else None
    if b0:
        lines["URTH"] = [(d, round(S.at(urth, d) / b0, 5)) for d in cal if S.at(urth, d)]
    return lines, positions, new_entries


def nightly(preview_only=False):
    Y = S.Yahoo()
    today = dt.date.today()
    month, month_end = last_complete_month(today)
    log = read_log()
    add, fehler = [], []
    out = dict(stand=today.isoformat(), start_signal=START_SIGNAL, regel=__doc__.split("\n\n")[0], koerbe=KOERBE, fehler=fehler)
    prev = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    have = {r["signal_vom"] for r in log if r.get("typ") == "signal"}
    due = month_end >= START_SIGNAL and month_end not in have and not preview_only
    want_preview = preview_only or (not have and (not prev.get("vorschau") or (today - dt.date.fromisoformat(prev["vorschau"]["erstellt"][:10])).days >= 6))
    if due or want_preview:
        try:
            cands, stat = run_screen(Y, month)
            ml = marktlage(Y)
            if due:
                held = {k: set() for k in KOERBE}
                for r in log:
                    if r.get("typ") == "signal":
                        for k in KOERBE:
                            held[k] |= set(r["neu"].get(k, []))
                neu = {}
                open_n = {k: 0 for k in KOERBE}
                for r in log:
                    if r.get("typ") == "einstieg" and (today - dt.date.fromisoformat(r["datum"])).days < HOLD_DAYS:
                        open_n[r["korb"]] += 1
                for k in KOERBE:
                    free = MAX_POS - open_n[k]
                    neu[k] = [c["sym"] for c in cands if c["korb"] == k][:max(0, free)]
                rec = dict(typ="signal", signal_vom=month_end, monat=month, festgeschrieben=now_iso(), marktlage=ml, stat=stat,
                           kandidaten=cands, neu=neu, cur={c["sym"]: c["cur"] for c in cands})
                add.append(rec)
                log.append(rec)
            else:
                out["vorschau"] = dict(erstellt=now_iso(), monat=month, marktlage=ml, stat=stat, kandidaten=cands)
        except Exception as e:
            fehler.append(f"Screen: {e}")
    if "vorschau" not in out and prev.get("vorschau") and not have:
        out["vorschau"] = prev["vorschau"]
    sig = [r for r in log if r.get("typ") == "signal"]
    if sig and not preview_only:
        try:
            syms = {}
            for r in sig:
                for k in KOERBE:
                    for s in r["neu"].get(k, []):
                        syms[s] = r["cur"].get(s, "USD")
            px = daily_usd(Y, syms)
            urth = (Y.spark(["URTH"], "2y").get("URTH")) or []
            lines, positions, new_entries = simulate(log, px, urth, today.isoformat())
            add += new_entries
            names = {c["sym"]: c for r in sig for c in r["kandidaten"]}
            out["linien"] = {k: dict(name=(KOERBE.get(k.split("_")[0], k) + (" + Exit-Regel" if k.endswith("_exit") else "")) if k != "URTH" else "MSCI World (URTH)",
                                     rendite=round((v[-1][1] - 1) * 100, 2) if v else None,
                                     mdd=round(S.mdd(v) * 100, 2) if v else None, start=v[0][0] if v else None) for k, v in lines.items()}
            out["reihen"] = {k: (lambda t: t + ([v[-1]] if v and t[-1] != v[-1] else []))(v[::max(1, len(v) // 260)]) if v else [] for k, v in lines.items()}
            out["positionen"] = [dict(korb=p["korb"], sym=p["sym"], name=names.get(p["sym"], {}).get("name"), land=names.get(p["sym"], {}).get("land"),
                                      sektor=names.get(p["sym"], {}).get("sektor"), signal_vom=p["signal_vom"], einstieg=p["ein_datum"],
                                      seit_pct=round((p["letzt"] / p["ein_kurs"] - 1) * 100, 1), ausstieg=p.get("aus_datum"), grund=p.get("grund"),
                                      offen=bool(p.get("offen"))) for p in positions]
        except Exception as e:
            fehler.append(f"Bewertung: {e}")
    append_log(add)
    out["signale"] = [dict(signal_vom=r["signal_vom"], festgeschrieben=r["festgeschrieben"], marktlage=r["marktlage"], stat=r["stat"],
                           kandidaten=r["kandidaten"], neu=r["neu"]) for r in sig][-12:]
    out["protokoll"] = [dict(typ=r["typ"], festgeschrieben=r["festgeschrieben"], signal_vom=r.get("signal_vom"), korb=r.get("korb"), sym=r.get("sym"),
                             datum=r.get("datum"), anzahl=(sum(len(v) for v in r["neu"].values()) if r.get("typ") == "signal" else None)) for r in log + [a for a in add if a not in log]][-40:]
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = out.get("vorschau")
    print("phoenix_data.json:", today, "| Signale festgeschrieben:", len(sig), "| Vorschau:", (v or {}).get("stat"), "| neu im Protokoll:", len(add), "| Fehler:", fehler)


if __name__ == "__main__":
    nightly(preview_only="--vorschau" in sys.argv)
