"""Hypothesen-Register des Orakels.

Jede Hypothese ist ein Experte mit Mechanismus. Regeln:
- Ein Experte darf nur Daten bis einschliesslich des Prognosetags verwenden.
- Bestehende Experten werden nie geaendert. Eine Verbesserung ist ein NEUER Experte mit neuem Namen.
- Ausmustern: retired = "JJJJ-MM-TT" setzen (bleibt im Code, wird nicht mehr prognostiziert).
- born: Tag der Aufnahme. Experten, die nach dem Orakel-Start (START) geboren werden, bekommen
  KEINEN Prior aus der Historie: Ihr Gewicht entsteht nur aus Vorwaertsdaten, weil ihre Idee
  mit Kenntnis der Vergangenheit entstanden ist.
Signatur: fn(D, h) -> DataFrame (Datum x Ticker), roh. Normierung macht das Orakel.
"""
import numpy as np
import pandas as pd

START = "2026-09-23"  # Tag, ab dem das Orakel vorwaerts prognostiziert


def _rsi(close, n=2):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def mom_12_1(D, h):
    c = D["close"]
    return c.shift(21) / c.shift(252) - 1


def mom_1m(D, h):
    c = D["close"]
    return c / c.shift(21) - 1


def rev_1w(D, h):
    c = D["close"]
    return -(c / c.shift(5) - 1)


def trend_200(D, h):
    c = D["close"]
    return np.log(c / c.rolling(200, min_periods=200).mean())


def dip_52w(D, h):
    c = D["close"]
    return -(c / c.rolling(252, min_periods=200).max() - 1)  # je tiefer unter dem Hoch, desto hoeher


def low_vol(D, h):
    r = D["close"].pct_change()
    return -r.rolling(60, min_periods=50).std()


def rsi2_oversold(D, h):
    return (50 - _rsi(D["close"], 2)) / 50


def vix_level(D, h):
    v = np.log(D["vix"])
    z = (v - v.rolling(252, min_periods=200).mean()) / v.rolling(252, min_periods=200).std()
    return pd.DataFrame({t: z for t in D["close"].columns})


def turn_of_month(D, h):
    cal = D["cal"]  # erweiterter Handelskalender inkl. Zukunft
    s = pd.Series(cal, index=cal)
    ym = s.dt.to_period("M")
    pos = s.groupby(ym).cumcount()
    last = s.groupby(ym).transform("count") - 1
    flag = ((pos == last) | (pos <= 2)).astype(float).values
    # Anteil der Tage t+1..t+h im Monatswechsel-Fenster
    fut = pd.Series(flag).shift(-1).rolling(h).mean().shift(-(h - 1)).values
    ser = pd.Series(fut, index=cal).reindex(D["close"].index)
    return pd.DataFrame({t: ser for t in D["close"].columns})


REGISTRY = [
    dict(name="mom_12_1", fn=mom_12_1, styles=["ts", "xs"], born="2026-09-23", retired=None,
         mechanism="Momentum 12-1: Anleger reagieren zu langsam auf neue Information, Trends setzen sich fort "
                   "(Jegadeesh/Titman 1993). Verlierer: wer zu frueh gegen den Trend verkauft."),
    dict(name="mom_1m", fn=mom_1m, styles=["ts", "xs"], born="2026-09-23", retired=None,
         mechanism="Kurzfristiges Momentum: Fluesse (ETF-Zufluesse, Rebalancing) laufen ueber Wochen nach."),
    dict(name="rev_1w", fn=rev_1w, styles=["xs"], born="2026-09-23", retired=None,
         mechanism="Wochen-Umkehr: Liquiditaetsgeber werden fuer Ueberreaktionen bezahlt (Lehmann 1990). "
                   "Verlierer: wer auf Kursbewegung hin kauft/verkauft."),
    dict(name="trend_200", fn=trend_200, styles=["ts", "xs"], born="2026-09-23", retired=None,
         mechanism="Trend ueber 200-Tage-Linie: Regime-Persistenz; ueber der Linie sind Renditen hoeher und Crashs seltener."),
    dict(name="dip_52w", fn=dip_52w, styles=["ts", "xs"], born="2026-09-23", retired=None,
         mechanism="Buy the Dip: Abstand zum 52-Wochen-Hoch. Gegenthese zu George/Hwang (Naehe zum Hoch = Staerke). "
                   "Positives Gewicht = Dip kaufen lohnt, negatives = Naehe zum Hoch lohnt."),
    dict(name="low_vol", fn=low_vol, styles=["ts", "xs"], born="2026-09-23", retired=None,
         mechanism="Niedrige Volatilitaet: Hebelbeschraenkte Anleger ueberzahlen riskante Titel (Frazzini/Pedersen)."),
    dict(name="rsi2_oversold", fn=rsi2_oversold, styles=["ts", "xs"], born="2026-09-23", retired=None,
         mechanism="RSI(2)-Ueberverkauft: kurzfristige Uebertreibung kehrt um (Connors). Test 29B: nach Kosten tot bei Einzeltiteln."),
    dict(name="vix_level", fn=vix_level, styles=["ts"], born="2026-09-23", retired=None,
         mechanism="Angstpraemie: hoher VIX gegen sein Jahresmittel = hohe Risikopraemie, spaetere Renditen hoeher."),
    dict(name="turn_of_month", fn=turn_of_month, styles=["ts"], born="2026-09-23", retired=None,
         mechanism="Monatswechsel: Gehalts-/Pensionszufluesse und Fonds-Rebalancing am Monatsanfang (Ariel 1987)."),
]


def active(style, on_date=None):
    out = []
    for e in REGISTRY:
        if style not in e["styles"]:
            continue
        if e["retired"] and (on_date is None or str(on_date) >= e["retired"]):
            continue
        if on_date is not None and str(on_date) < e["born"] and e["born"] > START:
            continue
        out.append(e)
    return out
