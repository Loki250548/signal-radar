#!/usr/bin/env python3
"""
index_changes.py  —  Signal Radar / These "Index-Wechsel" (erzwungener Fluss)

Findet neue S&P-Dow-Jones-Pressemitteilungen zu Indexaenderungen, parst
Aufnahmen/Streichungen (S&P 500, 100, MidCap 400, SmallCap 600) und trackt
jeden Titel ab dem Stichtag: Referenzkurs = Schluss am letzten Handelstag
VOR dem Stichtag (da handeln die Indexfonds), dann Rendite seit Referenz
sowie nach +5 / +20 / +60 Handelstagen. Misst die Umkehr-These.

Nur Standardbibliothek. Kurse: Yahoo (keylos), Fallback Stooq.
"""
import datetime as dt, json, os, re, sys, time, urllib.request

UA = os.environ.get("EDGAR_UA") or "Signal Radar Research kontakt@example.com"
ARCHIVE = "https://press.spglobal.com/index.php?s=2429"
OUT = "index_data.json"
SECTORS = ("Information Technology|Industrials|Consumer Staples|Consumer Discretionary|"
           "Health Care|Financials|Energy|Materials|Utilities|Real Estate|Communication Services")


def get(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(1.5 + i)


# ---------- 1) Mitteilungen finden & parsen ----------
def find_releases():
    html = get(ARCHIVE)
    links = re.findall(r'href="(https://press\.spglobal\.com/20\d\d-\d\d-\d\d-[^"]+)"', html)
    keep = []
    for u in dict.fromkeys(links):
        slug = u.lower()
        if re.search(r"s-p-500|s-and-p-500|s-p-midcap|s-p-smallcap|set-to-join|to-join-s-p", slug):
            keep.append(u)
    return keep[:12]


MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def parse_date(s):
    m = re.match(r"([A-Za-z]+)\.? (\d{1,2}), (\d{4})", s)
    return dt.date(int(m.group(3)), MONTHS[m.group(1)[:3].lower()], int(m.group(2))).isoformat()


def parse_release(url):
    txt = re.sub(r"<[^>]+>", " ", get(url))
    txt = re.sub(r"\s+", " ", txt)
    announced = re.match(r"https://press\.spglobal\.com/(\d{4}-\d{2}-\d{2})", url).group(1)
    pat = re.compile(
        r"([A-Z][a-z]+\.? \d{1,2}, \d{4}) (S&P 100|S&P 500|S&P MidCap 400|S&P SmallCap 600) "
        r"(Addition|Deletion) (.+?) ([A-Z][A-Z.\-]{0,6}) (" + SECTORS + r")")
    rows = []
    low = txt.lower()
    def reason_for(company):
        name = re.escape(company.split(",")[0].split(" Inc")[0].strip())
        b = " ".join(x for x in re.split(r"(?<=[.!?]) ", txt) if re.search(name, x, re.I)).lower()
        if re.search(r"acqui|merger|merge|purchase|buyout|take-private", b): return "M&A"
        if re.search(r"bankrupt|chapter 11|delist", b): return "Insolvenz"
        if re.search(r"no longer representative|market capitalization|better reflect|more representative", b + " " + low[:600]): return "Marktkap."
        return "-"
    for m in pat.finditer(txt):
        rows.append({"reason": reason_for(m.group(4)),
            "effective": parse_date(m.group(1)), "index": m.group(2),
            "action": "in" if m.group(3) == "Addition" else "out",
            "company": m.group(4).strip(), "ticker": m.group(5),
            "sector": m.group(6), "announced": announced, "source": url,
        })
    return rows


# ---------- 2) Kurse ----------
def prices_yahoo(tk):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?range=1y&interval=1d"
    d = json.loads(get(u))["chart"]["result"][0]
    q = d["indicators"]["quote"][0]; ts, cl, vo = d["timestamp"], q["close"], q["volume"]
    return [(dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat(), round(c, 4), v or 0)
            for t, c, v in zip(ts, cl, vo) if c is not None]


def prices_stooq(tk):
    csv = get(f"https://stooq.com/q/d/l/?s={tk.lower()}.us&i=d")
    out = []
    for line in csv.splitlines()[1:]:
        p = line.split(",")
        if len(p) >= 5 and p[4] not in ("", "N/D"):
            out.append((p[0], round(float(p[4]), 4), float(p[5]) if len(p) > 5 and p[5] not in ("", "N/D") else 0))
    return out


def prices(tk):
    for fn in (prices_yahoo, prices_stooq):
        try:
            p = fn(tk)
            if p:
                return p
        except Exception:
            pass
        time.sleep(0.5)
    return []


def track(row):
    px = prices(row["ticker"])
    if not px:
        return {**row, "tracked": False}
    eff = row["effective"]
    before = [p for p in px if p[0] < eff]
    after = [p for p in px if p[0] >= eff]
    if not before:
        return {**row, "tracked": False}
    ref_date, ref = before[-1][0], before[-1][1]
    last_date, last = px[-1][0], px[-1][1]
    pre10 = round((ref / before[-11][1] - 1) * 100, 2) if len(before) >= 11 else None
    vols = [p[2] for p in before[-61:-1]]
    volspike = round(before[-1][2] / (sum(vols) / len(vols)), 1) if vols and sum(vols) > 0 else None
    def ret_at(n):
        return round((after[n - 1][1] / ref - 1) * 100, 2) if len(after) >= n else None
    return {**row, "tracked": True,
            "ref_date": ref_date, "ref_close": ref, "pre10": pre10, "volspike": volspike,
            "last_date": last_date, "last_close": last,
            "days_since": len(after),
            "ret_since_ref": round((last / ref - 1) * 100, 2) if after else None,
            "ret_5d": ret_at(5), "ret_20d": ret_at(20), "ret_60d": ret_at(60)}


# ---------- 3) main ----------
def main():
    old = {}
    if os.path.exists(OUT):
        try:
            for r in json.load(open(OUT, encoding="utf-8")).get("changes", []):
                old[(r["ticker"], r["effective"], r["index"], r["action"])] = r
        except Exception:
            pass

    new_rows = []
    for u in find_releases():
        try:
            new_rows += parse_release(u)
        except Exception as e:
            print("skip", u, e, file=sys.stderr)
        time.sleep(0.4)
    for r in new_rows:
        old.setdefault((r["ticker"], r["effective"], r["index"], r["action"]), r)

    today = dt.date.today().isoformat()
    horizon = (dt.date.today() - dt.timedelta(days=120)).isoformat()
    changes = sorted(old.values(), key=lambda r: (r["effective"], r["index"], r["action"]), reverse=True)
    out_rows = []
    for r in changes:
        if r["effective"] >= horizon:
            out_rows.append(track(r)); time.sleep(0.3)
        else:
            out_rows.append({k: v for k, v in r.items()})  # alt: nicht mehr tracken
    RANK = {"S&P 500": 3, "S&P 100": 3, "S&P MidCap 400": 2, "S&P SmallCap 600": 1}
    adds = {(r["ticker"], r["effective"]): r["index"] for r in out_rows if r["action"] == "in"}
    for r in out_rows:
        a = adds.get((r["ticker"], r["effective"])) if r["action"] == "out" else None
        r["typ"] = ("Aufstieg" if a and RANK[a] > RANK[r["index"]] else "Abstieg" if a else "Exit") if r["action"] == "out" else "Aufnahme"
        r["watch"] = bool(r["action"] == "out" and r["index"] != "S&P 100" and r["typ"] in ("Abstieg", "Exit")
                          and r.get("reason") not in ("M&A", "Insolvenz") and r.get("pre10") is not None and r["pre10"] > -5)
    data = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "rule": "Watchlist = Streichung (Abstieg/Exit), nicht S&P 100, nicht M&A/Insolvenz, Vorlauf 10 HT > -5 %; Haltedauer ~20 HT",
        "source": "S&P Dow Jones Indices — Pressemitteilungen",
        "as_of": today, "changes": out_rows,
    }
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    n_tr = sum(1 for r in out_rows if r.get("tracked"))
    print(f"OK {len(out_rows)} Aenderungen, {n_tr} getrackt -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
