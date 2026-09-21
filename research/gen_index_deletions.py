#!/usr/bin/env python3
"""Generator: alle S&P-Streichungen (Abstieg/Exit, ohne S&P 100) aus dem Pressearchiv -> research/events/idx_del.json"""
import urllib.request, re, json, os, time, datetime as dt, html
UA = os.environ.get("EDGAR_UA") or "Signal Radar Research kontakt@example.com"
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "events", "idx_del.json")
def get(u):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read().decode("utf-8", "replace")
        except Exception:
            if i == 2: raise
            time.sleep(2)
SECT = "Information Technology|Industrials|Consumer Staples|Consumer Discretionary|Health Care|Financials|Energy|Materials|Utilities|Real Estate|Communication Services"
MON = {m: i for i, m in enumerate(["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], 1)}
pat = re.compile(r"([A-Z][a-z]+\.? \d{1,2}, \d{4}) (S&P 100|S&P 500|S&P MidCap 400|S&P SmallCap 600) (Addition|Deletion) (.+?) ([A-Z][A-Z.\-]{0,6}) (" + SECT + r")")
RANK = {"S&P 500": 3, "S&P 100": 3, "S&P MidCap 400": 2, "S&P SmallCap 600": 1}
old = {(e["ticker"], e["date"]): e for e in (json.load(open(OUT)) if os.path.exists(OUT) else [])}
rels = set(); y0 = dt.date.today().year
for y in range(y0 - 13, y0 + 1):   # 2013 ff. – volle Historie
    for o in range(0, 600, 100):
        f = re.findall(r'href="(https://press\.spglobal\.com/20\d\d-\d\d-\d\d-[^"]+)"', get(f"https://press.spglobal.com/index.php?s=2429&year={y}&l=100&o={o}"))
        if not f: break
        rels.update(u for u in f if re.search(r"s-p-500|s-and-p-500|s-p-midcap|s-p-smallcap|set-to-join|to-join-s-p|join-s-p", u.lower())); time.sleep(0.25)
rows = []
for u in sorted(rels):
    try: txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", get(u))))
    except Exception: continue
    low = txt.lower()
    for m in pat.finditer(txt):
        mm = re.match(r"([A-Za-z]+)\.? (\d{1,2}), (\d{4})", m.group(1)); eff = dt.date(int(mm.group(3)), MON[mm.group(1)[:3].lower()], int(mm.group(2))).isoformat()
        name = re.escape(m.group(4).split(",")[0].split(" Inc")[0].strip()); b = " ".join(x for x in re.split(r"(?<=[.!?]) ", txt) if re.search(name, x, re.I)).lower()
        reason = "M&A" if re.search(r"acqui|merger|merge|purchase|buyout", b) else ("Insolvenz" if re.search(r"bankrupt|chapter 11|delist", b) else "-")
        rows.append({"ticker": m.group(5), "date": eff, "index": m.group(2), "action": m.group(3), "reason": reason, "announced": u.split("/")[3][:10]})
    time.sleep(0.25)
adds = {(r["ticker"], r["date"]): r["index"] for r in rows if r["action"] == "Addition"}
for r in rows:
    if r["action"] != "Deletion": continue
    a = adds.get((r["ticker"], r["date"])); typ = "Aufstieg" if a and RANK[a] > RANK[r["index"]] else ("Abstieg" if a else "Exit")
    e = {"ticker": r["ticker"], "date": r["date"], "side": "long", "meta": {"index": r["index"], "typ": typ, "reason": r["reason"], "announced": r["announced"]}}
    k = (e["ticker"], e["date"])
    if k in old: old[k]["meta"] = e["meta"]
    else: old[k] = e
json.dump(sorted(old.values(), key=lambda e: e["date"]), open(OUT, "w"), indent=1); print(f"idx_del: {len(old)} Events")
