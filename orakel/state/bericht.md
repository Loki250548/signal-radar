# Orakel – Stand 2026-10-13

Journal: 120 Eintraege, Hash-Kette OK, Kopf `3b312a1405c13d8d`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 10 | 179 | -0.39 % | -0.47 | -9.1 % | -7.9 % | -1.3 % | -0.19 |
| B Sektoren/Laender | 5 | 10 | 340 | -0.18 % | -0.24 | +1.2 % | -12.6 % | +13.8 % | 0.25 |
| C Einzeltitel | 5 | 10 | 460 | -0.46 % | -1.21 | -48.8 % | +17.4 % | -66.1 % | -1.36 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.30 % | 0.72 | +0.036 |
| A | 5 | turn_of_month | +0.07 % | 0.53 | -0.006 |
| A | 5 | vix_level | +0.15 % | 0.48 | +0.035 |
| A | 5 | dip_52w | +0.27 % | 0.37 | -0.033 |
| A | 5 | trend_200 | +0.22 % | 0.34 | -0.018 |
| A | 5 | low_vol | +0.01 % | 0.03 | +0.000 |
| A | 5 | mom_1m | -0.11 % | -0.26 | +0.048 |
| A | 5 | rsi2_oversold | -0.43 % | -1.83 | +0.033 |
| B | 5 | rev_1w | -0.00 % | -0.02 | +0.056 |
| B | 5 | dip_52w | -0.00 % | -0.17 | +0.023 |
| B | 5 | mom_12_1 | -0.10 % | -0.22 | +0.061 |
| B | 5 | low_vol | -0.17 % | -0.64 | -0.017 |
| B | 5 | trend_200 | -0.19 % | -0.94 | -0.019 |
| B | 5 | rsi2_oversold | -0.05 % | -1.69 | -0.030 |
| B | 5 | mom_1m | -0.15 % | -6.04 | +0.027 |
| C | 5 | rsi2_oversold | +0.06 % | 1.80 | -0.004 |
| C | 5 | rev_1w | +0.04 % | 0.25 | +0.043 |
| C | 5 | trend_200 | -0.10 % | -0.84 | -0.002 |
| C | 5 | mom_12_1 | -0.25 % | -0.85 | +0.030 |
| C | 5 | low_vol | -0.11 % | -0.93 | -0.010 |
| C | 5 | dip_52w | -0.01 % | -1.87 | -0.008 |
| C | 5 | mom_1m | -0.07 % | -4.00 | +0.007 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 569 | 0.486 | 0.534 |
| 0.50–0.55 | 349 | 0.515 | 0.430 |
| 0.55–0.60 | 61 | 0.567 | 0.475 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-13): oben UUP 53 % (+1.3), DBC 53 % (+0.6), EWJ 55 % (+0.4), QQQ 58 % (+0.1), USO 51 % (-0.1) · unten HYG 53 % (-4.9), LQD 51 % (-5.1), IEF 49 % (-5.2)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-13): oben UUP 52 % (+0.3), QQQ 65 % (-0.4), DBC 54 % (-0.8), SPY 66 % (-0.8), USO 51 % (-1.5) · unten SLV 46 % (-5.3), IWM 55 % (-5.6), HYG 57 % (-6.3)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-13): oben SMH 54 % (+4.4), EWY 54 % (+3.7), EWT 53 % (+2.9), XBI 52 % (+1.7), XLK 52 % (+1.6) · unten XLP 46 % (-3.8), XLRE 46 % (-4.1), XLF 45 % (-4.7)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-13): oben XLE 52 % (+2.1), EWY 52 % (+1.8), EWW 52 % (+1.5), EWP 52 % (+1.5), XBI 51 % (+0.9) · unten XLP 48 % (-2.5), XLRE 47 % (-2.7), XLF 46 % (-3.6)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-13): oben AMD 53 % (+2.9), INTC 53 % (+2.6), ASML 52 % (+2.2), TSM 52 % (+2.1), CAT 52 % (+1.9) · unten NKE 47 % (-2.6), SAP 47 % (-2.7), NFLX 47 % (-2.9)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-13): oben QCOM 52 % (+2.1), INTC 52 % (+2.0), AMD 52 % (+1.8), GOOGL 52 % (+1.6), TXN 51 % (+1.3) · unten JPM 47 % (-2.6), COST 47 % (-2.9), ABBV 47 % (-2.9)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 179): mom_12_1 +0.036, mom_1m +0.048, trend_200 -0.018, dip_52w -0.033, low_vol +0.000, rsi2_oversold +0.033, vix_level +0.035, turn_of_month -0.006
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 340): mom_12_1 +0.061, mom_1m +0.027, rev_1w +0.056, trend_200 -0.019, dip_52w +0.023, low_vol -0.017, rsi2_oversold -0.030
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 460): mom_12_1 +0.030, mom_1m +0.007, rev_1w +0.043, trend_200 -0.002, dip_52w -0.008, low_vol -0.010, rsi2_oversold -0.004
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 10 | -0.47 | zu früh |
| B | 5 | 10 | -0.24 | zu früh |
| C | 5 | 10 | -1.21 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| rsi2_oversold | C | 5 | 10 | 1.8 | zu früh |
| mom_12_1 | A | 5 | 10 | 0.72 | zu früh |
| turn_of_month | A | 5 | 10 | 0.53 | zu früh |
| vix_level | A | 5 | 10 | 0.48 | zu früh |
| dip_52w | A | 5 | 10 | 0.37 | zu früh |
| trend_200 | A | 5 | 10 | 0.34 | zu früh |
| rev_1w | C | 5 | 10 | 0.25 | zu früh |
| low_vol | A | 5 | 10 | 0.03 | zu früh |
| rev_1w | B | 5 | 10 | -0.02 | zu früh |
| dip_52w | B | 5 | 10 | -0.17 | zu früh |
| mom_12_1 | B | 5 | 10 | -0.22 | zu früh |
| mom_1m | A | 5 | 10 | -0.26 | zu früh |
| low_vol | B | 5 | 10 | -0.64 | zu früh |
| trend_200 | C | 5 | 10 | -0.84 | zu früh |
| mom_12_1 | C | 5 | 10 | -0.85 | zu früh |
| low_vol | C | 5 | 10 | -0.93 | zu früh |
| trend_200 | B | 5 | 10 | -0.94 | zu früh |
| rsi2_oversold | B | 5 | 10 | -1.69 | zu früh |
| rsi2_oversold | A | 5 | 10 | -1.83 | zu früh |
| dip_52w | C | 5 | 10 | -1.87 | zu früh |
| mom_1m | C | 5 | 10 | -4.0 | zu früh |
| mom_1m | B | 5 | 10 | -6.04 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

