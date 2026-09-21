#!/usr/bin/env python3
"""
research/harness.py — generischer Backtest-Motor fuer den Thesen-Katalog.
Liest research/theses.json und research/events/<id>.json (ticker, date, side [, meta]),
holt Kurse (Cache research/prices/), berechnet Ueberrenditen vs SPY und IWM nach
+5/+20/+60/+120 Handelstagen, Vorlauf (pre10), wendet Thesen-Filter an und trennt
In-Sample (Events vor 'registered') von Out-of-Sample (ab 'registered').
Schreibt research_results.json fuer den Reiter 'Forschung'. Nur Standardbibliothek.
"""
import json, os, sys, time, math, bisect, statistics, datetime as dt, urllib.request
UA = os.environ.get("EDGAR_UA") or "Signal Radar Research kontakt@example.com"
ROOT = os.path.dirname(os.path.abspath(__file__)); PR = os.path.join(ROOT, "prices"); os.makedirs(PR, exist_ok=True)
H = (5, 20, 60, 120); BUDGET = float(os.environ.get("HARNESS_BUDGET", "1500")); T0 = time.time()
def yahoo(tk, years=6):
    p1 = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365 * years)).timestamp()); p2 = int(time.time())
    for i in range(3):
        try:
            d = json.loads(urllib.request.urlopen(urllib.request.Request(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?period1={p1}&period2={p2}&interval=1d",
                headers={"User-Agent": UA}), timeout=25).read())["chart"]["result"][0]
            return [(dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat(), c) for t, c in
                    zip(d["timestamp"], d["indicators"]["quote"][0]["close"]) if c]
        except Exception as e:
            if "404" in str(e): return []
            time.sleep(8 if "429" in str(e) else 0.5)
    return []
def prices(tk):
    fn = os.path.join(PR, f"{tk}.json")
    if os.path.exists(fn) and time.time() - os.path.getmtime(fn) < 6 * 86400:
        return json.load(open(fn))
    px = yahoo(tk); json.dump(px, open(fn, "w")); time.sleep(0.06); return px
def fwd(px, bm, d0, entry="before"):
    """entry='before': Referenz = Schluss vor dem (vorab bekannten) Stichtag, z.B. Index-Rebalancing.
       entry='after' : Referenz = Schluss des ersten Handelstags NACH dem Ereignis (Filings, News) – kein Look-ahead."""
    ds = [x[0] for x in px]
    if entry == "on":
        k = bisect.bisect_right(ds, d0) - 1       # Schluss des Event-Tages selbst (Nachrichtentag)
    elif entry == "after":
        k = bisect.bisect_right(ds, d0)           # erster Handelstag > Event-Datum
    else:
        k = bisect.bisect_left(ds, d0) - 1        # letzter Handelstag < Stichtag
    if k < 1 or k >= len(px): return None
    ref = px[k][1]; out = {"ref_date": px[k][0], "ref": ref, "entry": entry}
    out["pre10"] = round((ref / px[k - 10][1] - 1) * 100, 2) if k >= 10 else None
    for h in H:
        ok = k + h < len(px)
        out[f"r{h}"] = round((px[k + h][1] / ref - 1) * 100, 2) if ok else None
        for b, s in bm.items():
            bd = [x[0] for x in s]; j = bisect.bisect_right(bd, px[k][0]) - 1   # Benchmark am selben Referenztag
            out[f"x{h}_{b}"] = round(out[f"r{h}"] - (s[j + h][1] / s[j][1] - 1) * 100, 2) if ok and j >= 0 and j + h < len(s) else None
    return out
def stat(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 5: return {"n": len(xs)}
    m = statistics.mean(xs); s = statistics.pstdev(xs) or 1e-9
    return {"n": len(xs), "mean": round(m, 2), "median": round(statistics.median(xs), 2),
            "hit": round(100 * sum(x > 0 for x in xs) / len(xs), 1), "t": round(m / (s / math.sqrt(len(xs))), 2)}
def passes(ev, flt):
    f = ev.get("fwd") or {}; m = ev.get("meta") or {}
    if "pre10_gt" in flt and (f.get("pre10") is None or f["pre10"] <= flt["pre10_gt"]): return False
    if "regime_in" in flt and f.get("regime") not in flt["regime_in"]: return False
    for k, v in flt.get("meta_in", {}).items():
        if m.get(k) not in v: return False
    return True
def regime_fn(bm):
    vix = prices("^VIX"); vd = [x[0] for x in vix]; sd = [x[0] for x in bm["SPY"]]; sc = [x[1] for x in bm["SPY"]]
    def f(d):
        i = bisect.bisect_right(vd, d) - 1; j = bisect.bisect_right(sd, d) - 1
        if i < 0 or j < 0: return "?", "?"
        ma = statistics.mean(sc[max(0, j - 200):j]) if j > 200 else sc[j]
        v = vix[i][1]
        return ("auf" if sc[j] > ma else "ab"), ("ruhig" if v < 20 else "nervoes" if v < 30 else "stress")
    return f
REGIMES = ("auf/ruhig", "auf/nervoes", "auf/stress", "ab/ruhig", "ab/nervoes", "ab/stress")
def main():
    theses = json.load(open(os.path.join(ROOT, "theses.json")))
    bm = {b: prices(b) for b in ("SPY", "IWM")}
    reg = regime_fn(bm)
    results = {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "theses": []}
    for th in theses:
        fn = os.path.join(ROOT, "events", f"{th.get('events', th['id'])}.json")
        evs = json.load(open(fn)) if os.path.exists(fn) else []
        for e in evs:
            if time.time() - T0 > BUDGET: break
            if "fwd" in e and e["fwd"] and e["fwd"].get("entry") == th.get("entry", "before") and e["fwd"].get(f"x{H[-1]}_SPY") is not None: continue
            px = prices(e["ticker"]); e["fwd"] = fwd(px, bm, e["date"], th.get("entry", "before")) if px else None
        for e in evs:
            if e.get("fwd") and "regime" not in e["fwd"]:
                tr, vo = reg(e["fwd"]["ref_date"]); e["fwd"]["regime"] = f"{tr}/{vo}"
        json.dump(evs, open(fn, "w"))
        reg = th.get("registered", "2099-01-01"); flt = th.get("filters", {})
        use = [e for e in evs if e.get("fwd") and passes(e, flt)]
        sign = lambda e: (-1 if e.get("side") == "short" else 1)  # default long
        row = {"id": th["id"], "name": th["name"], "rule": th.get("rule", ""), "status": th.get("status", "beobachten"),
               "registered": reg, "n_events": len(use), "n_oos": sum(1 for e in use if e["date"] >= reg), "horizons": {}}
        for h in H:
            for b in ("SPY", "IWM"):
                row["horizons"][f"x{h}_{b}"] = {
                    "in": stat([sign(e) * e["fwd"][f"x{h}_{b}"] for e in use if e["date"] < reg and e["fwd"].get(f"x{h}_{b}") is not None]),
                    "oos": stat([sign(e) * e["fwd"][f"x{h}_{b}"] for e in use if e["date"] >= reg and e["fwd"].get(f"x{h}_{b}") is not None])}
        # Statistik je Regime (+20d und +60d vs SPY) — verschiedene Signale fuer verschiedene Szenarien
        row["regimes"] = {}
        for rg in REGIMES:
            sub = [e for e in use if (e["fwd"] or {}).get("regime") == rg]
            row["regimes"][rg] = {f"x{h}_SPY": stat([sign(e) * e["fwd"][f"x{h}_SPY"] for e in sub if e["fwd"].get(f"x{h}_SPY") is not None]) for h in (20, 60)}
        row["active_regimes"] = th.get("active_regimes", [])
        row["notes"] = th.get("notes", [])
        results["theses"].append(row)
        print(f"{th['id']:28} events={len(use):4} oos={row['n_oos']:3}", file=sys.stderr)
    json.dump(results, open(os.path.join(ROOT, "..", "research_results.json"), "w"), ensure_ascii=False, indent=1)
    print("OK research_results.json", file=sys.stderr)
if __name__ == "__main__": main()
