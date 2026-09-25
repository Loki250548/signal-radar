#!/usr/bin/env python3
"""funding.py — Cash-and-Carry-Ampel BTC/ETH (Test 15), Papierbetrieb ab 01.10.2026. Kein Kapital, nur Papier.

Idee: Spot kaufen und denselben Betrag als Perpetual short verkaufen. Die Position ist marktneutral und kassiert die
Funding Rate, die Long-Positionen im Bullenmarkt an die Shorts zahlen. Test 15 (Deribit, 2019–2026): BTC 7,7 % p.a. roh,
über der 200-Tage-Linie 12,7 %, darunter −0,7 % → die Regel ist regime-geschaltet.

Regel (festgelegt am 25.09.2026, vor jedem Papierergebnis):
  - je Instrument (BTC, ETH) eigene Regel: in Position, solange der Tagesschluss (Deribit-Tageskerze des Perpetuals) über
    seiner 200-Tage-Linie liegt; sonst Cash. Wechsel gilt ab der ersten vollen Stunde nach Schluss der Tageskerze.
  - Ertrag in Position = Summe der stündlichen Funding-Sätze (interest_1h), Kosten 0,13 % je Ein- oder Ausstieg
    (0,26 % Round-Trip wie Test 15). Rendite auf den Nominalbetrag; auf das Kapital bei 30 % Puffer für die Short-Seite
    (Kapital = 1,3 × Nominal, Puffer unverzinst).
  - Nicht in der Rechnung: Liquidationsrisiko der Short-Seite, Gegenparteirisiko der Börse (FTX), Basis-Schwankung.
Ampel: grün = über 200-Tage-Linie und Funding der letzten 7 Tage > 0; gelb = über der Linie, Funding ≤ 0;
rot = unter der Linie (Papier in Cash).
Quelle: Deribit Public API (ohne Schlüssel). Protokoll: funding_log.jsonl, nur Ampelwechsel, wächst nur.
Aufruf: python funding.py. Nur Standardbibliothek."""
import datetime as dt
import json
import os
import statistics
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "funding_data.json")
LOG = os.path.join(ROOT, "funding_log.jsonl")
START = os.environ.get("FUNDING_START", "2026-10-01")
API = "https://www.deribit.com/api/v2/public/"
UA = os.environ.get("EDGAR_UA") or "Signal Radar kontakt@example.com"
INSTR = {"BTC": "BTC-PERPETUAL", "ETH": "ETH-PERPETUAL"}
SMA = 200
SWITCH_COST = 0.0013
BUFFER = 0.30
HOUR, DAY = 3600_000, 86_400_000


def get(method, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    for i in range(5):
        try:
            r = urllib.request.urlopen(urllib.request.Request(f"{API}{method}?{q}", headers={"User-Agent": UA}), timeout=40)
            return json.loads(r.read())["result"]
        except Exception:
            if i == 4:
                raise
            time.sleep(4 * (i + 1))


def funding_history(instr, start_ms, end_ms):
    """Stündliche Funding-Sätze; die API liefert höchstens 744 Einträge je Abruf → rückwärts blättern."""
    out, end = {}, end_ms
    while end > start_ms:
        r = get("get_funding_rate_history", instrument_name=instr, start_timestamp=max(start_ms, end - 744 * HOUR), end_timestamp=end)
        if not r:
            break
        for x in r:
            out[x["timestamp"]] = x["interest_1h"]
        first = min(x["timestamp"] for x in r)
        if first >= end:
            break
        end = first - 1
        time.sleep(0.2)
    return dict(sorted((t, v) for t, v in out.items() if t >= start_ms))


def candles(instr, days, now_ms):
    r = get("get_tradingview_chart_data", instrument_name=instr, start_timestamp=now_ms - days * DAY, end_timestamp=now_ms, resolution="1D")
    rows = [(t, c) for t, c in zip(r["ticks"], r["close"]) if t + DAY <= now_ms]      # nur abgeschlossene Tageskerzen
    return rows


def regime_series(rows):
    """[(Schlusszeit der Kerze, Schluss, SMA200, über?)]"""
    out = []
    for i in range(len(rows)):
        if i + 1 < SMA:
            continue
        sma = statistics.mean(c for _, c in rows[i + 1 - SMA:i + 1])
        out.append((rows[i][0] + DAY, rows[i][1], sma, rows[i][1] > sma))
    return out


def analyse(key, now_ms):
    instr = INSTR[key]
    rows = candles(instr, 620, now_ms)
    reg = regime_series(rows)
    start_ms = int(dt.datetime.fromisoformat(START).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
    hist_from = min(start_ms, now_ms - 400 * DAY)
    fh = funding_history(instr, hist_from, now_ms)
    hours = sorted(fh)
    rates = [fh[h] for h in hours]

    def ann(n):
        x = rates[-n:]
        return statistics.mean(x) * 8760 if x else None

    # Regime je Funding-Stunde: letzte Tageskerze, die vor Beginn der Stunde geschlossen hat
    ri, state, pos = 0, None, []
    for h in hours:
        while ri < len(reg) and reg[ri][0] <= h - HOUR:
            state = reg[ri][3]
            ri += 1
        pos.append(state)

    # Papier ab START und Rückblick 12 Monate (gleiche Regel)
    def paper(from_ms):
        nav, peak, mdd, inpos, switches, series, day_nav = 1.0, 1.0, 0.0, False, 0, [], {}
        for h, r, p in zip(hours, rates, pos):
            if h < from_ms or p is None:
                continue
            if p != inpos:
                nav *= 1 - SWITCH_COST
                switches += 1
                inpos = p
            if inpos:
                nav *= 1 + r
            peak = max(peak, nav)
            mdd = min(mdd, nav / peak - 1)
            day_nav[dt.datetime.fromtimestamp(h / 1000, dt.timezone.utc).date().isoformat()] = nav
        days = sorted(day_nav)
        yrs = max((now_ms - from_ms) / DAY / 365, 1e-9)
        return dict(nav=round(nav, 5), rendite=round((nav - 1) * 100, 3), rendite_kapital=round((nav - 1) / (1 + BUFFER) * 100, 3),
                    p_a=round(((nav ** (1 / yrs)) - 1) * 100, 2) if yrs >= 0.25 else None, mdd=round(mdd * 100, 3), wechsel=switches,
                    in_position=inpos, reihe=[[d, round(day_nav[d], 5)] for d in days][-400:])
    started = now_ms >= start_ms
    last = reg[-1] if reg else None
    f7 = ann(168)
    if not last:
        ampel, text = "grau", "zu wenig Kursdaten für die 200-Tage-Linie"
    elif not last[3]:
        ampel, text = "rot", "unter der 200-Tage-Linie → Papier in Cash (Test 15: im Bärenmarkt −0,7 % p.a.)"
    elif f7 is not None and f7 > 0:
        ampel, text = "grün", "über der 200-Tage-Linie, Funding positiv → Papier in Position"
    else:
        ampel, text = "gelb", "über der 200-Tage-Linie, aber Funding der letzten 7 Tage ≤ 0 → Position kostet gerade"
    # Tageswerte (Summe der Stundensätze) für die Grafik, letzte 365 Tage
    daily = {}
    for h, r in zip(hours, rates):
        d = dt.datetime.fromtimestamp(h / 1000, dt.timezone.utc).date().isoformat()
        daily[d] = daily.get(d, 0.0) + r
    dser = [[d, round(v * 365 * 100, 2)] for d, v in sorted(daily.items())][-365:]
    return dict(instrument=instr, kurs=last[1] if last else None, sma200=round(last[2], 2) if last else None,
                abstand_pct=round((last[1] / last[2] - 1) * 100, 2) if last else None, ueber_200=last[3] if last else None,
                kerze_bis=dt.datetime.fromtimestamp(last[0] / 1000, dt.timezone.utc).isoformat(timespec="minutes") if last else None,
                funding_7d_pa=round(f7 * 100, 2) if f7 is not None else None, funding_30d_pa=round(ann(720) * 100, 2) if ann(720) is not None else None,
                funding_365d_pa=round(ann(8760) * 100, 2) if ann(8760) is not None else None,
                letzte_stunde=dt.datetime.fromtimestamp(hours[-1] / 1000, dt.timezone.utc).isoformat(timespec="minutes") if hours else None,
                ampel=ampel, text=text, papier=paper(start_ms) if started else None, rueckblick_12m=paper(now_ms - 365 * DAY),
                tage_funding_pa=dser)


def main():
    now_ms = int(time.time() * 1000)
    out = dict(stand=dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), papierstart=START, puffer=BUFFER,
               kosten_wechsel_pct=SWITCH_COST * 100, instrumente={}, fehler=[])
    for k in INSTR:
        try:
            out["instrumente"][k] = analyse(k, now_ms)
        except Exception as e:
            out["fehler"].append(f"{k}: {type(e).__name__}: {e}")
    # Protokoll: Ampelwechsel festschreiben
    log = [json.loads(x) for x in open(LOG, encoding="utf-8")] if os.path.exists(LOG) else []
    last = {}
    for r in log:
        last[r["instrument"]] = r["ampel"]
    add = []
    for k, v in out["instrumente"].items():
        if v["ampel"] != last.get(k):
            add.append(dict(instrument=k, ampel=v["ampel"], ueber_200=v["ueber_200"], kurs=v["kurs"], sma200=v["sma200"],
                            funding_7d_pa=v["funding_7d_pa"], kerze_bis=v["kerze_bis"], festgeschrieben=out["stand"]))
    if add:
        with open(LOG, "a", encoding="utf-8") as f:
            for r in add:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    out["protokoll"] = (log + add)[-30:]
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("funding_data.json:", {k: (v["ampel"], v["funding_7d_pa"], v["abstand_pct"]) for k, v in out["instrumente"].items()},
          "Fehler:", out["fehler"], "neu im Protokoll:", len(add))


if __name__ == "__main__":
    main()
