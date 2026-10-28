# Orakel – Stand 2026-10-27

Journal: 225 Eintraege, Hash-Kette OK, Kopf `36fe7aabd156e7ac`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 20 | 358 | +0.08 % | 0.18 | +15.0 % | -9.2 % | +24.2 % | 1.34 |
| A Markt | 20 | 5 | 90 | +2.84 % | 10.31 | +0.0 % | -10.2 % | +10.2 % | 10.06 |
| B Sektoren/Laender | 5 | 20 | 680 | -1.12 % | -1.33 | -64.0 % | -7.3 % | -56.8 % | -0.97 |
| B Sektoren/Laender | 20 | 5 | 170 | -2.40 % | -34.44 | -76.3 % | -6.9 % | -69.4 % | -16.55 |
| C Einzeltitel | 5 | 20 | 920 | -0.94 % | -2.28 | -90.4 % | +14.2 % | -104.6 % | -2.30 |
| C Einzeltitel | 20 | 5 | 230 | -2.02 % | -49.56 | -63.7 % | +18.6 % | -82.4 % | -22.32 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.65 % | 2.70 | +0.059 |
| A | 5 | turn_of_month | +0.16 % | 2.31 | -0.001 |
| A | 5 | low_vol | +0.13 % | 1.66 | -0.003 |
| A | 5 | vix_level | +0.25 % | 1.60 | +0.038 |
| A | 5 | dip_52w | +0.47 % | 1.26 | -0.039 |
| A | 5 | trend_200 | +0.39 % | 1.20 | -0.034 |
| A | 5 | mom_1m | +0.04 % | 0.17 | +0.036 |
| A | 5 | rsi2_oversold | -0.12 % | -0.65 | -0.004 |
| A | 20 | trend_200 | +1.14 % | 17.60 | +0.000 |
| A | 20 | turn_of_month | +0.65 % | 16.04 | -0.030 |
| A | 20 | mom_12_1 | +0.50 % | 15.27 | -0.015 |
| A | 20 | vix_level | +1.04 % | 14.32 | +0.050 |
| A | 20 | rsi2_oversold | +0.80 % | 13.20 | -0.004 |
| A | 20 | mom_1m | +2.08 % | 12.88 | +0.064 |
| A | 20 | dip_52w | +1.19 % | 12.66 | -0.055 |
| A | 20 | low_vol | +0.81 % | 10.44 | -0.043 |
| B | 5 | rsi2_oversold | -0.01 % | -0.09 | -0.055 |
| B | 5 | mom_12_1 | -0.42 % | -1.08 | +0.035 |
| B | 5 | low_vol | -0.43 % | -1.40 | +0.017 |
| B | 5 | dip_52w | -0.06 % | -1.40 | +0.013 |
| B | 5 | trend_200 | -0.24 % | -1.67 | -0.030 |
| B | 5 | rev_1w | -0.26 % | -1.72 | +0.028 |
| B | 5 | mom_1m | -0.15 % | -6.55 | +0.017 |
| B | 20 | dip_52w | +0.09 % | 6.63 | +0.011 |
| B | 20 | trend_200 | -0.14 % | -6.14 | +0.002 |
| B | 20 | rev_1w | -0.39 % | -9.08 | +0.010 |
| B | 20 | mom_12_1 | -0.53 % | -15.99 | +0.015 |
| B | 20 | low_vol | -0.87 % | -27.97 | -0.016 |
| B | 20 | rsi2_oversold | -0.98 % | -60.92 | -0.024 |
| B | 20 | mom_1m | -0.01 % | -70.47 | -0.031 |
| C | 5 | dip_52w | +0.01 % | 0.62 | +0.009 |
| C | 5 | low_vol | -0.13 % | -1.04 | +0.042 |
| C | 5 | rsi2_oversold | -0.09 % | -1.11 | -0.031 |
| C | 5 | rev_1w | -0.25 % | -1.42 | +0.018 |
| C | 5 | trend_200 | -0.14 % | -1.59 | +0.008 |
| C | 5 | mom_12_1 | -0.41 % | -1.82 | -0.003 |
| C | 5 | mom_1m | -0.09 % | -3.58 | -0.008 |
| C | 20 | rev_1w | -0.05 % | -1.12 | +0.001 |
| C | 20 | dip_52w | -0.01 % | -2.56 | +0.015 |
| C | 20 | rsi2_oversold | -0.20 % | -9.13 | -0.039 |
| C | 20 | trend_200 | -0.10 % | -36.74 | -0.003 |
| C | 20 | mom_12_1 | -0.55 % | -49.50 | +0.018 |
| C | 20 | low_vol | -1.18 % | -52.08 | -0.007 |
| C | 20 | mom_1m | -0.01 % | -83.67 | -0.018 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 1431 | 0.486 | 0.563 |
| 0.50–0.55 | 864 | 0.515 | 0.402 |
| 0.55–0.60 | 138 | 0.567 | 0.370 |
| 0.60–1.00 | 15 | 0.642 | 0.467 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-27): oben USO 55 % (+3.5), DBC 55 % (+2.7), UUP 52 % (+0.6), EWJ 54 % (-0.8), IWM 53 % (-1.3) · unten FXI 49 % (-3.7), GLD 49 % (-4.8), HYG 53 % (-4.9)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-27): oben USO 54 % (+1.0), TLT 54 % (+0.8), DBC 56 % (+0.4), UUP 52 % (+0.0), LQD 61 % (-0.2) · unten FXI 49 % (-4.7), SLV 45 % (-6.2), EEM 51 % (-7.1)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-27): oben EWI 52 % (+1.7), EWY 51 % (+1.3), EWH 51 % (+1.3), EWD 51 % (+1.1), EWN 51 % (+0.8) · unten ITB 47 % (-2.6), XLE 47 % (-2.7), XLF 47 % (-2.7)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-27): oben EWY 53 % (+2.8), SMH 53 % (+2.6), EWT 52 % (+2.0), XBI 51 % (+1.4), EWI 51 % (+1.3) · unten EWL 47 % (-2.7), XLP 47 % (-2.7), XLF 47 % (-2.8)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-27): oben JPM 51 % (+1.4), LIN 51 % (+0.8), GE 51 % (+0.7), GOOGL 51 % (+0.6), ABBV 51 % (+0.6) · unten ADBE 48 % (-2.2), PLTR 48 % (-2.5), CRM 47 % (-3.0)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-27): oben INTC 53 % (+2.8), AMD 52 % (+2.2), CAT 52 % (+2.1), QCOM 52 % (+2.0), ASML 52 % (+1.9) · unten DIS 47 % (-2.6), V 47 % (-3.0), MA 47 % (-3.1)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 358): mom_12_1 +0.059, mom_1m +0.036, trend_200 -0.034, dip_52w -0.039, low_vol -0.003, rsi2_oversold -0.004, vix_level +0.038, turn_of_month -0.001
- A20 (Vorwaertsdaten: 90): mom_12_1 -0.015, mom_1m +0.064, trend_200 +0.000, dip_52w -0.055, low_vol -0.043, rsi2_oversold -0.004, vix_level +0.050, turn_of_month -0.030
- B5 (Vorwaertsdaten: 680): mom_12_1 +0.035, mom_1m +0.017, rev_1w +0.028, trend_200 -0.030, dip_52w +0.013, low_vol +0.017, rsi2_oversold -0.055
- B20 (Vorwaertsdaten: 170): mom_12_1 +0.015, mom_1m -0.031, rev_1w +0.010, trend_200 +0.002, dip_52w +0.011, low_vol -0.016, rsi2_oversold -0.024
- C5 (Vorwaertsdaten: 920): mom_12_1 -0.003, mom_1m -0.008, rev_1w +0.018, trend_200 +0.008, dip_52w +0.009, low_vol +0.042, rsi2_oversold -0.031
- C20 (Vorwaertsdaten: 230): mom_12_1 +0.018, mom_1m -0.018, rev_1w +0.001, trend_200 -0.003, dip_52w +0.015, low_vol -0.007, rsi2_oversold -0.039

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 20 | 0.18 | zu früh |
| A | 20 | 5 | 10.31 | zu früh |
| B | 5 | 20 | -1.33 | zu früh |
| B | 20 | 5 | -34.44 | zu früh |
| C | 5 | 20 | -2.28 | zu früh |
| C | 20 | 5 | -49.56 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| trend_200 | A | 20 | 5 | 17.6 | zu früh |
| turn_of_month | A | 20 | 5 | 16.04 | zu früh |
| mom_12_1 | A | 20 | 5 | 15.27 | zu früh |
| vix_level | A | 20 | 5 | 14.32 | zu früh |
| rsi2_oversold | A | 20 | 5 | 13.2 | zu früh |
| mom_1m | A | 20 | 5 | 12.88 | zu früh |
| dip_52w | A | 20 | 5 | 12.66 | zu früh |
| low_vol | A | 20 | 5 | 10.44 | zu früh |
| dip_52w | B | 20 | 5 | 6.63 | zu früh |
| mom_12_1 | A | 5 | 20 | 2.7 | zu früh |
| turn_of_month | A | 5 | 20 | 2.31 | zu früh |
| low_vol | A | 5 | 20 | 1.66 | zu früh |
| vix_level | A | 5 | 20 | 1.6 | zu früh |
| dip_52w | A | 5 | 20 | 1.26 | zu früh |
| trend_200 | A | 5 | 20 | 1.2 | zu früh |
| dip_52w | C | 5 | 20 | 0.62 | zu früh |
| mom_1m | A | 5 | 20 | 0.17 | zu früh |
| rsi2_oversold | B | 5 | 20 | -0.09 | zu früh |
| rsi2_oversold | A | 5 | 20 | -0.65 | zu früh |
| low_vol | C | 5 | 20 | -1.04 | zu früh |
| mom_12_1 | B | 5 | 20 | -1.08 | zu früh |
| rsi2_oversold | C | 5 | 20 | -1.11 | zu früh |
| rev_1w | C | 20 | 5 | -1.12 | zu früh |
| low_vol | B | 5 | 20 | -1.4 | zu früh |
| dip_52w | B | 5 | 20 | -1.4 | zu früh |
| rev_1w | C | 5 | 20 | -1.42 | zu früh |
| trend_200 | C | 5 | 20 | -1.59 | zu früh |
| trend_200 | B | 5 | 20 | -1.67 | zu früh |
| rev_1w | B | 5 | 20 | -1.72 | zu früh |
| mom_12_1 | C | 5 | 20 | -1.82 | zu früh |
| dip_52w | C | 20 | 5 | -2.56 | zu früh |
| mom_1m | C | 5 | 20 | -3.58 | zu früh |
| trend_200 | B | 20 | 5 | -6.14 | zu früh |
| mom_1m | B | 5 | 20 | -6.55 | zu früh |
| rev_1w | B | 20 | 5 | -9.08 | zu früh |
| rsi2_oversold | C | 20 | 5 | -9.13 | zu früh |
| mom_12_1 | B | 20 | 5 | -15.99 | zu früh |
| low_vol | B | 20 | 5 | -27.97 | zu früh |
| trend_200 | C | 20 | 5 | -36.74 | zu früh |
| mom_12_1 | C | 20 | 5 | -49.5 | zu früh |
| low_vol | C | 20 | 5 | -52.08 | zu früh |
| rsi2_oversold | B | 20 | 5 | -60.92 | zu früh |
| mom_1m | B | 20 | 5 | -70.47 | zu früh |
| mom_1m | C | 20 | 5 | -83.67 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (5/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

