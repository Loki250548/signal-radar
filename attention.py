#!/usr/bin/env python3
"""
attention.py  —  Signal Radar / Screen 3 "Aufmerksamkeit" (Overlay, KEIN Signal)

Misst fuer jeden Kandidaten aus Screen 1 (Insider) und Screen 2 (Index-Wechsel),
wie viel oeffentliche Aufmerksamkeit er gerade bekommt:
  - Reddit (Aggregat ueber ApeWisdom: Erwaehnungen, Rang, Delta 24h)
  - StockTwits (Nachrichten der letzten 24h im Symbol-Stream)
  - News EN + DE via Google-News-RSS (deckt finanzen.net, boerse.de, onvista,
    Investing.com etc. ab), letzte 7 Tage, plus Top-Schlagzeilen mit Links
Lesart: hohe Aufmerksamkeit = ueberlaufen (Crowding-Risiko), stille Kandidaten
sind die interessanteren. Spike = heutiger Composite / Median der Vortage.
Nur Standardbibliothek. X/Twitter und Truth Social bewusst nicht enthalten
(keine freie API).
"""
import datetime as dt, json, os, re, statistics, sys, time, urllib.parse, urllib.request
from email.utils import parsedate_to_datetime

UA = os.environ.get("EDGAR_UA") or "Signal Radar Research kontakt@example.com"
OUT = "attention_data.json"
MAX_TICKERS = 90


def get(url, retries=2):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(1.0)


def load_json(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}


# ---------- Kandidaten ----------
def candidates():
    c = {}
    for s in load_json("radar_data.json").get("signals", []):
        c.setdefault(s["ticker"], {"company": s.get("company", ""), "from": set()})["from"].add("insider")
    for r in load_json("index_data.json").get("changes", []):
        if r.get("tracked"):
            c.setdefault(r["ticker"], {"company": r.get("company", ""), "from": set()})["from"].add("index")
    return dict(list(c.items())[:MAX_TICKERS])


# ---------- Quellen ----------
def reddit_map():
    m = {}
    for page in (1, 2, 3):
        try:
            for r in json.loads(get(f"https://apewisdom.io/api/v1.0/filter/all-stocks/page/{page}")).get("results", []):
                m[r["ticker"].upper()] = {"mentions": int(r.get("mentions") or 0),
                                          "rank": int(r.get("rank") or 0),
                                          "prev24": int(r.get("mentions_24h_ago") or 0)}
        except Exception:
            break
        time.sleep(0.4)
    return m


def stocktwits_24h(tk):
    try:
        msgs = json.loads(get(f"https://api.stocktwits.com/api/2/streams/symbol/{tk}.json")).get("messages", [])
    except Exception:
        return None
    cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=24)
    n = 0
    for m in msgs:
        try:
            if dt.datetime.fromisoformat(m["created_at"].replace("Z", "+00:00")) >= cut:
                n += 1
        except Exception:
            pass
    return n  # Stream liefert max. 30 -> Obergrenze 30


def news(tk, company, lang):
    q = f'"{company}" OR "{tk} stock"' if lang == "en" else f'"{company}" OR "{tk} Aktie"'
    loc = "hl=en-US&gl=US&ceid=US:en" if lang == "en" else "hl=de&gl=DE&ceid=DE:de"
    try:
        xml = get(f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&{loc}")
    except Exception:
        return 0, []
    cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)
    items, n = [], 0
    for it in re.findall(r"<item>(.*?)</item>", xml, re.S):
        t = re.search(r"<title>(.*?)</title>", it, re.S); l = re.search(r"<link>(.*?)</link>", it, re.S)
        s = re.search(r"<source[^>]*>(.*?)</source>", it, re.S); d = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        try:
            when = parsedate_to_datetime(d.group(1)) if d else None
        except Exception:
            when = None
        if when and when.tzinfo is None:
            when = when.replace(tzinfo=dt.timezone.utc)
        if when and when < cut:
            continue
        n += 1
        if len(items) < 3:
            title = re.sub(r"<!\[CDATA\[|\]\]>", "", t.group(1)).strip() if t else ""
            items.append({"t": title, "u": (l.group(1).strip() if l else ""),
                          "src": (s.group(1).strip() if s else ""), "d": when.date().isoformat() if when else ""})
    return n, items


# ---------- main ----------
def main():
    today = dt.date.today().isoformat()
    old = load_json(OUT).get("tickers", {})
    cands = candidates()
    rmap = reddit_map()
    out = {}
    for i, (tk, info) in enumerate(cands.items()):
        rd = rmap.get(tk, {"mentions": 0, "rank": None, "prev24": 0})
        st = stocktwits_24h(tk)
        n_en, h_en = news(tk, info["company"], "en"); time.sleep(0.25)
        n_de, h_de = news(tk, info["company"], "de"); time.sleep(0.25)
        composite = rd["mentions"] + (st or 0) + n_en + n_de
        hist = [h for h in old.get(tk, {}).get("history", []) if h.get("date") != today][-44:]
        prev = [h["composite"] for h in hist]
        spike = round(composite / statistics.median(prev), 2) if len(prev) >= 5 and statistics.median(prev) > 0 else None
        hist.append({"date": today, "composite": composite})
        out[tk] = {"company": info["company"], "from": sorted(info["from"]),
                   "reddit": rd["mentions"], "reddit_rank": rd["rank"], "reddit_prev24": rd["prev24"],
                   "stocktwits_24h": st, "news_en_7d": n_en, "news_de_7d": n_de,
                   "headlines": (h_de + h_en)[:4], "composite": composite, "spike": spike, "history": hist}
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(cands)}", file=sys.stderr)
    data = {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "source": "Reddit (ApeWisdom) · StockTwits · Google-News-RSS EN/DE (u. a. finanzen.net, boerse.de, onvista)",
            "as_of": today, "tickers": out}
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {len(out)} Ticker -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
