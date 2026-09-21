#!/usr/bin/env python3
"""sympathy.py — Sympathie-Schock-Detektor (Test 13, 21.09.2026).
Regel: Blue Chip (Top 100 nach Dollar-Umsatz im S&P 500) faellt an einem Tag >= 8 % gegen SPY bei Volumen >= 3x (20-T-Schnitt),
waehrend der Median seiner GICS-Sektor-Peers <= -3 % gegen SPY liegt (Branchenverkauf, keine eigene Nachricht).
Einstieg: Schluss des Folgetags. Haltedauer: 60 Handelstage. Papierbetrieb; Kontrolle: idiosynkratische Schocks (Peers > -1 %) werden nur gelistet.
Schreibt sympathy_data.json (Dashboard) und research/events/sympathy_bluechip.json (Harness, OOS). Nur Standardbibliothek."""
import urllib.request, re, json, os, time, datetime as dt, html, statistics, bisect
UA = os.environ.get("EDGAR_UA") or "Signal Radar kontakt@example.com"
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "sympathy_data.json")
EV = os.path.join(ROOT, "research", "events", "sympathy_bluechip.json"); LOOK = 60
def get(u):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")
        except Exception:
            if i == 2: raise
            time.sleep(2)
# 1) Universum + Sektoren (Wikipedia, Tabelle 1: Symbol, Security, GICS Sector)
w = get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"); t = re.findall(r"<table[^>]*>(.*?)</table>", w, re.S)[0]
sec = {}
for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S)[1:]:
    cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
    if len(cells) >= 3 and re.fullmatch(r"[A-Z.\-]{1,6}", cells[0]): sec[cells[0].replace(".", "-")] = cells[2]
# 2) Kurse ~130 Kalendertage
p1 = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=130)).timestamp()); p2 = int(time.time())
def px(s):
    for i in range(2):
        try:
            d = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1={p1}&period2={p2}&interval=1d"))["chart"]["result"][0]
            q = d["indicators"]["quote"][0]
            return [(dt.datetime.fromtimestamp(x, dt.timezone.utc).date().isoformat(), c, v or 0) for x, c, v in zip(d["timestamp"], q["close"], q["volume"]) if c]
        except Exception: time.sleep(1)
    return []
spy = px("SPY"); sd = [x[0] for x in spy]; sc = {x[0]: x[1] for x in spy}
P = {}
for s in sec:
    r = px(s)
    if len(r) > 30: P[s] = {x[0]: (x[1], x[2]) for x in r}
    time.sleep(0.04)
days = sd[-LOOK - 1:]
# Blue Chips: Top 100 nach mittlerem Dollar-Umsatz im Fenster
dv = {s: statistics.mean(c * v for c, v in m.values()) for s, m in P.items()}
blue = set(sorted(dv, key=dv.get, reverse=True)[:100])
# 3) Ereignisse je Tag
def excess(s, d, dp):
    m = P[s]
    if d not in m or dp not in m or dp not in sc or d not in sc: return None
    return ((m[d][0] / m[dp][0] - 1) - (sc[d] / sc[dp] - 1)) * 100
signals, control = [], []
for i in range(1, len(days)):
    d, dp = days[i], days[i - 1]; ex = {}; vr = {}
    for s in P:
        e = excess(s, d, dp)
        if e is None: continue
        ex[s] = e
        hist = [P[s][x][1] for x in sd[max(0, sd.index(d) - 20):sd.index(d)] if x in P[s]]
        vr[s] = P[s][d][1] / statistics.mean(hist) if hist and statistics.mean(hist) > 0 else 0
    for s, e in ex.items():
        if e > -8 or vr.get(s, 0) < 3: continue
        peers = [ex[o] for o in ex if o != s and sec.get(o) == sec.get(s)]
        pm = statistics.median(peers) if len(peers) >= 3 else None
        rec = {"ticker": s, "sector": sec.get(s), "date": d, "excess": round(e, 1), "vol_ratio": round(vr[s], 1), "peer_median": round(pm, 1) if pm is not None else None, "blue_chip": s in blue}
        if s in blue and pm is not None and pm <= -3: signals.append(rec)
        elif s in blue and pm is not None and pm > -1: control.append(rec)
# 4) Papier-Positionen fortschreiben
old = json.load(open(OUT)) if os.path.exists(OUT) else {"positions": []}
pos = {(p["ticker"], p["signal_date"]): p for p in old.get("positions", [])}
for r in signals:
    k = (r["ticker"], r["date"])
    if k not in pos:
        pos[k] = {"ticker": r["ticker"], "sector": r["sector"], "signal_date": r["date"], "excess_signal": r["excess"], "peer_median": r["peer_median"], "vol_ratio": r["vol_ratio"], "status": "pending"}
for p in pos.values():
    j = bisect.bisect_right(sd, p["signal_date"])                # Folgetag
    if p.get("status") == "closed" or j >= len(sd): continue
    e_d = sd[j]; m = P.get(p["ticker"], {})
    if e_d not in m: continue
    p["entry_date"] = e_d; p["entry"] = round(m[e_d][0], 2); p["spy_entry"] = round(sc[e_d], 2)
    x_i = min(j + LOOK, len(sd) - 1); x_d = sd[x_i]; last_d = max(x for x in m if x <= x_d)
    p["last_date"] = last_d; p["last"] = round(m[last_d][0], 2)
    p["excess_now"] = round(((m[last_d][0] / m[e_d][0] - 1) - (sc[last_d] / sc[e_d] - 1)) * 100, 2)
    p["days_held"] = sd.index(last_d) - j; p["exit_date"] = sd[j + LOOK] if j + LOOK < len(sd) else None
    p["status"] = "closed" if p["days_held"] >= LOOK else "open"
positions = sorted(pos.values(), key=lambda p: p["signal_date"], reverse=True)
closed = [p["excess_now"] for p in positions if p["status"] == "closed"]
out = {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "asof": days[-1], "rule": "Blue Chip ≥8 % unter SPY bei Volumen ≥3×, Sektor-Peers Median ≤ −3 % → Einstieg Folgetag, 60 HT halten (Papier)",
       "universe": len(P), "blue_chips": sorted(blue), "signals_today": [r for r in signals if r["date"] == days[-1]], "control_today": [r for r in control if r["date"] == days[-1]],
       "positions": positions, "stats": {"open": sum(1 for p in positions if p["status"] == "open"), "closed": len(closed), "avg_excess_closed": round(statistics.mean(closed), 2) if closed else None,
       "hit_closed": round(100 * sum(1 for x in closed if x > 0) / len(closed), 1) if closed else None}}
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
# 5) Harness-Events (OOS)
ev = json.load(open(EV)) if os.path.exists(EV) else []
have = {(e["ticker"], e["date"]) for e in ev}
for p in positions:
    if (p["ticker"], p["signal_date"]) not in have: ev.append({"ticker": p["ticker"], "date": p["signal_date"], "side": "long", "meta": {"sector": p["sector"], "peer_median": p["peer_median"], "excess": p["excess_signal"]}})
os.makedirs(os.path.dirname(EV), exist_ok=True); json.dump(sorted(ev, key=lambda e: e["date"]), open(EV, "w"), ensure_ascii=False, indent=1)
print(f"sympathy: {len(P)} Titel, {len(signals)} Signale in {LOOK} HT ({sum(1 for r in signals if r['date']==days[-1])} heute), Kontrolle {len(control)}, Positionen {len(positions)}")
