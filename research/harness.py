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
COST = float(os.environ.get("COST_PCT", "1.0"))   # Kosten je Umschlag in % (Small Caps: 1–2)
def stat(xs, dates=None):
    """xs: Ueberrenditen (%), bereits nach Kosten; dates: Ereignisdaten fuer gebuendelten t-Wert (ein Cluster je Datum)."""
    pairs = [(x, d) for x, d in zip(xs, dates or [None] * len(xs)) if x is not None]
    xs = [p[0] for p in pairs]
    if len(xs) < 5: return {"n": len(xs)}
    m = statistics.mean(xs); s = statistics.pstdev(xs) or 1e-9
    out = {"n": len(xs), "mean": round(m, 2), "median": round(statistics.median(xs), 2),
           "hit": round(100 * sum(x > 0 for x in xs) / len(xs), 1), "t": round(m / (s / math.sqrt(len(xs))), 2)}
    if dates:
        by = {}
        for x, d in pairs: by.setdefault(d, []).append(x)
        cm = [statistics.mean(v) for v in by.values()]
        if len(cm) >= 3:
            cs = statistics.pstdev(cm) or 1e-9
            out["clusters"] = len(cm); out["t_clustered"] = round(statistics.mean(cm) / (cs / math.sqrt(len(cm))), 2)
    return out
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
import random
def z_for_trials(trials):
    """Bonferroni-angepasste t-Schwelle: 0.05/trials einseitig; Basis 3.0 fuer einen Versuch (Harvey/Liu/Zhu)."""
    return round(max(3.0, 3.0 + 0.55 * math.log(max(1, trials))), 2)
def protocol(th, use, evs_all, bm, reg, key, entry, cost):
    """Placebo: regime-gleiche Zufallstage, Ticker aus dem Pool der These. Zwei Haelften. Verteilung. Top-5."""
    real = [sign_of(e) * e["fwd"][key] - cost for e in use if e["fwd"].get(key) is not None]
    if len(real) < 5: return {}
    out = {}
    # Verteilung ueber Jahre
    yrs = {}
    for e in use: yrs[e["date"][:4]] = yrs.get(e["date"][:4], 0) + 1
    out["max_year_share"] = round(100 * max(yrs.values()) / len(use), 1)
    # zwei Haelften
    ds = sorted(e["date"] for e in use); mid = ds[len(ds) // 2]
    h1 = [sign_of(e) * e["fwd"][key] - cost for e in use if e["date"] < mid and e["fwd"].get(key) is not None]
    h2 = [sign_of(e) * e["fwd"][key] - cost for e in use if e["date"] >= mid and e["fwd"].get(key) is not None]
    out["half1"] = round(statistics.mean(h1), 2) if h1 else None; out["half2"] = round(statistics.mean(h2), 2) if h2 else None
    # Top-5 gestrichen
    srt = sorted(real, reverse=True); out["mean_wo_top5"] = round(statistics.mean(srt[5:]), 2) if len(srt) > 10 else None
    # Placebo
    pool = sorted({e["ticker"] for e in evs_all}); sd = [x[0] for x in bm["SPY"]]
    regimes = [(e["fwd"] or {}).get("regime") for e in use]
    days_by_reg = {}
    for d in sd[260:]:
        tr, vo = reg(d); days_by_reg.setdefault(f"{tr}/{vo}", []).append(d)
    rnd = random.Random(42); means = []; hits = []; draws = int(os.environ.get("PLACEBO_DRAWS", "200"))
    for _ in range(draws):
        xs = []
        for rg in regimes:
            cands = days_by_reg.get(rg) or sd[260:]
            for _try in range(4):
                d = rnd.choice(cands); tk = rnd.choice(pool); px = prices(tk)
                f = fwd(px, bm, d, entry) if px else None
                if f and f.get(key) is not None: xs.append(f[key] - cost); break
        if len(xs) >= 5: means.append(statistics.mean(xs)); hits.append(100 * sum(x > 0 for x in xs) / len(xs))
    if means:
        means.sort(); m_real = statistics.mean(real)
        out["placebo_mean"] = round(statistics.mean(means), 2); out["placebo_p95"] = round(means[int(0.95 * (len(means) - 1))], 2)
        out["placebo_rank"] = round(100 * sum(1 for m in means if m < m_real) / len(means), 1); out["placebo_draws"] = len(means)
    return out
def verdict(row, key):
    s = row["horizons"].get(key, {}).get("in", {}); p = row.get("protocol", {}); tr = row.get("trials", 1)
    need = z_for_trials(tr); row["t_required"] = need
    checks = {"t_clustered": (s.get("t_clustered") or 0) >= need,
              "halves_same_sign": p.get("half1") is not None and p.get("half2") is not None and p["half1"] > 0 and p["half2"] > 0,
              "beats_placebo": (p.get("placebo_rank") or 0) >= 95,
              "robust_wo_top5": (p.get("mean_wo_top5") or 0) > 0,
              "spread_over_time": (p.get("max_year_share") or 100) < 40}
    row["checks"] = checks
    return "bestätigt" if all(checks.values()) else ("kandidat" if sum(checks.values()) >= 3 else "unbestätigt")
def sign_of(e): return -1 if e.get("side") == "short" else 1
def main():
    theses = json.load(open(os.path.join(ROOT, "theses.json")))
    bm = {b: prices(b) for b in ("SPY", "IWM")}
    regf = regime_fn(bm)
    results = {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "cost_pct": COST, "note": "Ueberrenditen nach Kosten; t_clustered = t-Wert nach Ereignisdatum gebuendelt", "theses": []}
    for th in theses:
        fn = os.path.join(ROOT, "events", f"{th.get('events', th['id'])}.json")
        evs = json.load(open(fn)) if os.path.exists(fn) else []
        for e in evs:
            if time.time() - T0 > BUDGET: break
            if "fwd" in e and e["fwd"] and e["fwd"].get("entry") == th.get("entry", "before") and e["fwd"].get(f"x{H[-1]}_SPY") is not None: continue
            px = prices(e["ticker"]); e["fwd"] = fwd(px, bm, e["date"], th.get("entry", "before")) if px else None
        for e in evs:
            if e.get("fwd") and "regime" not in e["fwd"]:
                tr, vo = regf(e["fwd"]["ref_date"]); e["fwd"]["regime"] = f"{tr}/{vo}"
        json.dump(evs, open(fn, "w"))
        reg = th.get("registered", "2099-01-01"); flt = th.get("filters", {})
        use = [e for e in evs if e.get("fwd") and passes(e, flt)]
        sign = lambda e: (-1 if e.get("side") == "short" else 1)  # default long
        row = {"id": th["id"], "name": th["name"], "rule": th.get("rule", ""), "status": th.get("status", "beobachten"),
               "registered": reg, "n_events": len(use), "n_oos": sum(1 for e in use if e["date"] >= reg), "horizons": {}}
        for h in H:
            for b in ("SPY", "IWM"):
                ins_ = [e for e in use if e["date"] < reg and e["fwd"].get(f"x{h}_{b}") is not None]
                oos_ = [e for e in use if e["date"] >= reg and e["fwd"].get(f"x{h}_{b}") is not None]
                row["horizons"][f"x{h}_{b}"] = {
                    "in": stat([sign(e) * e["fwd"][f"x{h}_{b}"] - COST for e in ins_], [e["date"] for e in ins_]),
                    "oos": stat([sign(e) * e["fwd"][f"x{h}_{b}"] - COST for e in oos_], [e["date"] for e in oos_])}
        # Statistik je Regime (+20d und +60d vs SPY) — verschiedene Signale fuer verschiedene Szenarien
        row["regimes"] = {}
        for rg in REGIMES:
            sub = [e for e in use if (e["fwd"] or {}).get("regime") == rg]
            row["regimes"][rg] = {f"x{h}_SPY": stat([sign(e) * e["fwd"][f"x{h}_SPY"] - COST for e in sub if e["fwd"].get(f"x{h}_SPY") is not None], [e["date"] for e in sub if e["fwd"].get(f"x{h}_SPY") is not None]) for h in (20, 60)}
        row["active_regimes"] = th.get("active_regimes", []); row["trials"] = th.get("trials", 1)
        key = th.get("key", "x20_SPY")
        if use and th.get("status") not in ("tot", "widerlegt"):
            row["protocol"] = protocol(th, use, evs, bm, regf, key, th.get("entry", "before"), COST)
            row["verdict"] = verdict(row, key)
        else:
            row["verdict"] = th.get("status", "")
        row["notes"] = th.get("notes", []) + ([f"Protokoll ({key}, {COST} % Kosten): Urteil {row['verdict']} · " + " · ".join(f"{k}={'✔' if v else '✘'}" for k, v in row.get("checks", {}).items())] if row.get("checks") else [])
        results["theses"].append(row)
        print(f"{th['id']:28} events={len(use):4} oos={row['n_oos']:3}", file=sys.stderr)
    json.dump(results, open(os.path.join(ROOT, "..", "research_results.json"), "w"), ensure_ascii=False, indent=1)
    print("OK research_results.json", file=sys.stderr)
if __name__ == "__main__": main()
