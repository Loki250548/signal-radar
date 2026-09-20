#!/usr/bin/env python3
"""
insider_screener.py  —  Signal Radar / These "Insider-Cluster"

Laeuft automatisch in GitHub Actions (kein Terminal noetig).
Holt Form-4-Filings von SEC EDGAR, filtert offene Marktkaeufe (Code P),
buendelt pro Titel und schreibt radar_data.json fuer index.html.

Nur Python-Standardbibliothek. Kein pip, kein API-Key.
"""
import argparse, datetime as dt, json, os, re, sys, time
import urllib.request, xml.etree.ElementTree as ET

# EDGAR verlangt einen Kontakt im User-Agent. Wird aus der GitHub-Variable
# EDGAR_UA gelesen; sonst greift der Platzhalter unten (bitte anpassen).
UA = os.environ.get("EDGAR_UA") or "Signal Radar Research kontakt@example.com"
BASE = "https://www.sec.gov/Archives/"


def get(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(1.0 + i)


def find_daily_index(start):
    d = start
    for _ in range(10):
        q = (d.month - 1) // 3 + 1
        url = (f"https://www.sec.gov/Archives/edgar/daily-index/"
               f"{d.year}/QTR{q}/form.{d.strftime('%Y%m%d')}.idx")
        try:
            txt = get(url)
            if re.search(r"^4\s+", txt, re.M):
                return d, txt
        except Exception:
            pass
        d -= dt.timedelta(days=1)
    return None, None


def form4_paths(idx_text):
    return re.findall(r"^4\s+.*?(edgar/data/\S+\.txt)\s*$", idx_text, re.M)


def flag(node, tag):
    return (node.findtext(tag) or "").strip().lower() in ("1", "true")


def parse_form4(raw):
    m = re.search(r"<ownershipDocument>.*?</ownershipDocument>", raw, re.S)
    if not m:
        return []
    try:
        root = ET.fromstring(m.group(0))
    except ET.ParseError:
        return []

    sym = (root.findtext(".//issuer/issuerTradingSymbol") or "").strip().upper()
    if sym in ("NONE", "N/A", "--"):
        sym = ""
    company = (root.findtext(".//issuer/issuerName") or "").strip()
    owner = (root.findtext(".//reportingOwner/reportingOwnerId/rptOwnerName") or "").strip()
    rel = root.find(".//reportingOwner/reportingOwnerRelationship")
    roles, title = [], ""
    if rel is not None:
        if flag(rel, "isDirector"):        roles.append("Dir")
        if flag(rel, "isOfficer"):         roles.append("Off")
        if flag(rel, "isTenPercentOwner"): roles.append("10%")
        title = (rel.findtext("officerTitle") or "").strip()
    role = "/".join(roles) or "-"
    # Filing-weites Flag: Kauf im Rahmen eines vorab geplanten 10b5-1-Plans
    plan = flag(root, "aff10b5One")

    out = []
    for t in root.findall(".//nonDerivativeTransaction"):
        if t.findtext(".//transactionCoding/transactionCode") != "P":
            continue
        try:
            shares = float(t.findtext(".//transactionShares/value"))
            price = float(t.findtext(".//transactionPricePerShare/value"))
        except (TypeError, ValueError):
            continue
        out.append({
            "ticker": sym or "?", "company": company, "owner": owner,
            "role": role, "title": title, "plan10b5_1": plan,
            "shares": shares, "price": price, "value": shares * price,
            "date": (t.findtext(".//transactionDate/value") or "").strip(),
        })
    return out


def aggregate(purchases, min_value):
    by = {}
    for p in purchases:
        by.setdefault(p["ticker"], []).append(p)
    signals = []
    for tk, rows in by.items():
        if tk in ("?", ""):
            continue
        total_value = sum(r["value"] for r in rows)
        if total_value < min_value:
            continue
        buyers = sorted({r["owner"] for r in rows})
        roles = sorted({r["role"] for r in rows if r["role"] != "-"})
        titles = sorted({r["title"] for r in rows if r["title"]})
        total_shares = sum(r["shares"] for r in rows)
        avg_price = total_value / total_shares if total_shares else 0.0
        latest = max((r["date"] for r in rows), default="")
        plan_share = sum(r["value"] for r in rows if r["plan10b5_1"]) / total_value
        # Sortierhilfe (NICHT validiert): Cluster > Volumen > Rolle;
        # geplante 10b5-1-Kaeufe werden abgewertet (weniger Aussagekraft).
        role_w = 1.3 if any(x in ("Dir", "Off") for x in roles) else 1.0
        plan_w = 1.0 - 0.5 * plan_share
        strength = round((len(buyers) * 2 + (total_value ** 0.5) / 50 * role_w) * plan_w, 1)
        signals.append({
            "thesis": "insider-cluster",
            "ticker": tk, "company": rows[0]["company"],
            "insiders": len(buyers), "buyers": buyers,
            "roles": roles, "titles": titles,
            "plan10b5_1": plan_share >= 0.5,
            "total_value": round(total_value, 2),
            "total_shares": int(total_shares),
            "avg_price": round(avg_price, 4),
            "latest_date": latest, "strength": strength,
        })
    signals.sort(key=lambda s: s["strength"], reverse=True)
    return signals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--limit", type=int, default=1500)   # ganzer Tag
    ap.add_argument("--min-value", type=float, default=10000.0)
    ap.add_argument("--out", default="radar_data.json")
    a = ap.parse_args()

    start = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    day, idx = find_daily_index(start)
    if not idx:
        print("Kein Daily-Index gefunden.", file=sys.stderr); sys.exit(1)

    paths = form4_paths(idx)
    n = min(len(paths), a.limit)
    print(f"[{day}] {len(paths)} Form-4-Filings, verarbeite {n}", file=sys.stderr)
    purchases = []
    for i, p in enumerate(paths[:n]):
        try:
            purchases += parse_form4(get(BASE + p))
        except Exception:
            pass
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{n}", file=sys.stderr)
        time.sleep(0.11)

    signals = aggregate(purchases, a.min_value)
    data = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "SEC EDGAR — Form 4 (Daily Index)",
        "filing_date": day.isoformat(),
        "filings_scanned": n, "purchases_found": len(purchases),
        "min_value": a.min_value, "signals": signals,
    }
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"OK {len(signals)} Titel -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
