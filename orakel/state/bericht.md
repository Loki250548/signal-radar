# Orakel – Stand 2026-10-22

Journal: 189 Eintraege, Hash-Kette OK, Kopf `a6d766d5e47a7b1b`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 17 | 304 | -0.15 % | -0.28 | -3.0 % | -7.9 % | +4.9 % | 1.08 |
| A Markt | 20 | 2 | 36 | +3.60 % | nan | +0.0 % | -14.7 % | +nan % | nan |
| B Sektoren/Laender | 5 | 17 | 578 | -1.27 % | -1.31 | -65.4 % | -4.1 % | -61.3 % | -0.89 |
| B Sektoren/Laender | 20 | 2 | 68 | -2.33 % | nan | -54.3 % | -4.0 % | +nan % | nan |
| C Einzeltitel | 5 | 17 | 782 | -1.04 % | -2.21 | -102.6 % | +15.9 % | -118.5 % | -2.33 |
| C Einzeltitel | 20 | 2 | 92 | -1.96 % | nan | -40.8 % | +19.3 % | +nan % | nan |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.64 % | 2.28 | +0.060 |
| A | 5 | turn_of_month | +0.13 % | 1.71 | -0.003 |
| A | 5 | vix_level | +0.24 % | 1.30 | +0.036 |
| A | 5 | low_vol | +0.09 % | 1.08 | -0.005 |
| A | 5 | dip_52w | +0.30 % | 0.76 | -0.033 |
| A | 5 | trend_200 | +0.27 % | 0.75 | -0.030 |
| A | 5 | mom_1m | -0.14 % | -0.50 | +0.030 |
| A | 5 | rsi2_oversold | -0.20 % | -1.03 | +0.003 |
| A | 20 | vix_level | +1.15 % | -99.00 | +0.043 |
| A | 20 | turn_of_month | +0.71 % | -99.00 | -0.026 |
| A | 20 | trend_200 | +1.14 % | -99.00 | +0.001 |
| A | 20 | rsi2_oversold | +0.97 % | -99.00 | -0.005 |
| A | 20 | mom_1m | +2.61 % | -99.00 | +0.051 |
| A | 20 | mom_12_1 | +0.51 % | -99.00 | -0.022 |
| A | 20 | low_vol | +1.01 % | -99.00 | -0.044 |
| A | 20 | dip_52w | +1.52 % | -99.00 | -0.058 |
| B | 5 | mom_12_1 | -0.48 % | -1.08 | +0.038 |
| B | 5 | dip_52w | -0.03 % | -1.17 | +0.016 |
| B | 5 | rev_1w | -0.23 % | -1.38 | +0.032 |
| B | 5 | low_vol | -0.51 % | -1.48 | +0.016 |
| B | 5 | trend_200 | -0.26 % | -1.57 | -0.030 |
| B | 5 | rsi2_oversold | -0.06 % | -2.37 | -0.047 |
| B | 5 | mom_1m | -0.13 % | -6.44 | +0.009 |
| B | 20 | trend_200 | -0.01 % | -99.00 | +0.007 |
| B | 20 | rsi2_oversold | -1.03 % | -99.00 | -0.042 |
| B | 20 | rev_1w | -0.57 % | -99.00 | +0.020 |
| B | 20 | mom_1m | -0.01 % | -99.00 | -0.013 |
| B | 20 | mom_12_1 | -0.41 % | -99.00 | +0.027 |
| B | 20 | low_vol | -0.77 % | -99.00 | -0.029 |
| B | 20 | dip_52w | +0.05 % | -99.00 | +0.016 |
| C | 5 | dip_52w | +0.00 % | 0.17 | +0.000 |
| C | 5 | rsi2_oversold | -0.10 % | -1.04 | -0.026 |
| C | 5 | rev_1w | -0.22 % | -1.17 | +0.022 |
| C | 5 | low_vol | -0.18 % | -1.47 | +0.034 |
| C | 5 | trend_200 | -0.17 % | -1.64 | -0.000 |
| C | 5 | mom_12_1 | -0.45 % | -1.76 | +0.003 |
| C | 5 | mom_1m | -0.06 % | -4.29 | -0.013 |
| C | 20 | trend_200 | -0.08 % | -99.00 | -0.006 |
| C | 20 | rsi2_oversold | -0.23 % | -99.00 | -0.050 |
| C | 20 | rev_1w | -0.28 % | -99.00 | +0.017 |
| C | 20 | mom_1m | -0.01 % | -99.00 | -0.009 |
| C | 20 | mom_12_1 | -0.49 % | -99.00 | +0.031 |
| C | 20 | low_vol | -1.26 % | -99.00 | -0.026 |
| C | 20 | dip_52w | -0.03 % | -99.00 | +0.013 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 1079 | 0.485 | 0.565 |
| 0.50–0.55 | 677 | 0.515 | 0.397 |
| 0.55–0.60 | 98 | 0.568 | 0.398 |
| 0.60–1.00 | 6 | 0.644 | 0.500 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-22): oben USO 56 % (+4.9), DBC 57 % (+4.0), UUP 52 % (+0.7), EWJ 55 % (-0.2), IWM 54 % (-0.9) · unten LQD 53 % (-3.3), GLD 50 % (-4.0), HYG 53 % (-5.0)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-22): oben USO 55 % (+2.1), DBC 56 % (+0.7), TLT 54 % (+0.6), IEF 57 % (+0.1), DIA 66 % (-0.1) · unten HYG 58 % (-5.2), SLV 45 % (-6.0), EEM 51 % (-7.1)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-22): oben EWY 52 % (+2.1), INDA 51 % (+0.8), EWI 51 % (+0.8), EWQ 51 % (+0.8), XLI 51 % (+0.7) · unten EWZ 48 % (-1.9), XLE 48 % (-2.0), XLP 48 % (-2.2)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-22): oben EWY 53 % (+2.6), XBI 52 % (+2.4), SMH 52 % (+2.3), EWT 52 % (+2.0), XLK 52 % (+1.7) · unten XLRE 48 % (-1.9), XLF 48 % (-2.0), EWD 48 % (-2.3)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-22): oben JPM 51 % (+1.1), BRK-B 51 % (+0.9), MA 51 % (+0.8), BAC 51 % (+0.8), COST 51 % (+0.6) · unten AMZN 48 % (-1.9), MSFT 48 % (-1.9), ADBE 48 % (-2.3)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-22): oben INTC 52 % (+1.7), AMD 52 % (+1.7), ASML 51 % (+1.1), QCOM 51 % (+1.0), CAT 51 % (+1.0) · unten UNH 48 % (-1.9), MSFT 48 % (-2.4), PG 48 % (-2.5)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 304): mom_12_1 +0.060, mom_1m +0.030, trend_200 -0.030, dip_52w -0.033, low_vol -0.005, rsi2_oversold +0.003, vix_level +0.036, turn_of_month -0.003
- A20 (Vorwaertsdaten: 36): mom_12_1 -0.022, mom_1m +0.051, trend_200 +0.001, dip_52w -0.058, low_vol -0.044, rsi2_oversold -0.005, vix_level +0.043, turn_of_month -0.026
- B5 (Vorwaertsdaten: 578): mom_12_1 +0.038, mom_1m +0.009, rev_1w +0.032, trend_200 -0.030, dip_52w +0.016, low_vol +0.016, rsi2_oversold -0.047
- B20 (Vorwaertsdaten: 68): mom_12_1 +0.027, mom_1m -0.013, rev_1w +0.020, trend_200 +0.007, dip_52w +0.016, low_vol -0.029, rsi2_oversold -0.042
- C5 (Vorwaertsdaten: 782): mom_12_1 +0.003, mom_1m -0.013, rev_1w +0.022, trend_200 -0.000, dip_52w +0.000, low_vol +0.034, rsi2_oversold -0.026
- C20 (Vorwaertsdaten: 92): mom_12_1 +0.031, mom_1m -0.009, rev_1w +0.017, trend_200 -0.006, dip_52w +0.013, low_vol -0.026, rsi2_oversold -0.050

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 17 | -0.28 | zu früh |
| A | 20 | 2 | None | zu früh |
| B | 5 | 17 | -1.31 | zu früh |
| B | 20 | 2 | None | zu früh |
| C | 5 | 17 | -2.21 | zu früh |
| C | 20 | 2 | None | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| mom_12_1 | A | 5 | 17 | 2.28 | zu früh |
| turn_of_month | A | 5 | 17 | 1.71 | zu früh |
| vix_level | A | 5 | 17 | 1.3 | zu früh |
| low_vol | A | 5 | 17 | 1.08 | zu früh |
| dip_52w | A | 5 | 17 | 0.76 | zu früh |
| trend_200 | A | 5 | 17 | 0.75 | zu früh |
| dip_52w | C | 5 | 17 | 0.17 | zu früh |
| mom_1m | A | 5 | 17 | -0.5 | zu früh |
| rsi2_oversold | A | 5 | 17 | -1.03 | zu früh |
| rsi2_oversold | C | 5 | 17 | -1.04 | zu früh |
| mom_12_1 | B | 5 | 17 | -1.08 | zu früh |
| rev_1w | C | 5 | 17 | -1.17 | zu früh |
| dip_52w | B | 5 | 17 | -1.17 | zu früh |
| rev_1w | B | 5 | 17 | -1.38 | zu früh |
| low_vol | C | 5 | 17 | -1.47 | zu früh |
| low_vol | B | 5 | 17 | -1.48 | zu früh |
| trend_200 | B | 5 | 17 | -1.57 | zu früh |
| trend_200 | C | 5 | 17 | -1.64 | zu früh |
| mom_12_1 | C | 5 | 17 | -1.76 | zu früh |
| rsi2_oversold | B | 5 | 17 | -2.37 | zu früh |
| mom_1m | C | 5 | 17 | -4.29 | zu früh |
| mom_1m | B | 5 | 17 | -6.44 | zu früh |
| mom_12_1 | A | 20 | 2 | None | zu früh |
| mom_1m | A | 20 | 2 | None | zu früh |
| trend_200 | A | 20 | 2 | None | zu früh |
| dip_52w | A | 20 | 2 | None | zu früh |
| low_vol | A | 20 | 2 | None | zu früh |
| rsi2_oversold | A | 20 | 2 | None | zu früh |
| vix_level | A | 20 | 2 | None | zu früh |
| turn_of_month | A | 20 | 2 | None | zu früh |
| mom_12_1 | B | 20 | 2 | None | zu früh |
| mom_1m | B | 20 | 2 | None | zu früh |
| rev_1w | B | 20 | 2 | None | zu früh |
| trend_200 | B | 20 | 2 | None | zu früh |
| dip_52w | B | 20 | 2 | None | zu früh |
| low_vol | B | 20 | 2 | None | zu früh |
| rsi2_oversold | B | 20 | 2 | None | zu früh |
| mom_12_1 | C | 20 | 2 | None | zu früh |
| mom_1m | C | 20 | 2 | None | zu früh |
| rev_1w | C | 20 | 2 | None | zu früh |
| trend_200 | C | 20 | 2 | None | zu früh |
| dip_52w | C | 20 | 2 | None | zu früh |
| low_vol | C | 20 | 2 | None | zu früh |
| rsi2_oversold | C | 20 | 2 | None | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (2/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

