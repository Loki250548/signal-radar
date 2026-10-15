# Orakel – Stand 2026-10-14

Journal: 129 Eintraege, Hash-Kette OK, Kopf `90f7ccb8f2af2a83`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 11 | 197 | -0.37 % | -0.51 | -8.3 % | -8.5 % | +0.2 % | 0.04 |
| B Sektoren/Laender | 5 | 11 | 374 | -0.48 % | -0.54 | -18.0 % | -10.4 % | -7.6 % | -0.12 |
| C Einzeltitel | 5 | 11 | 506 | -0.57 % | -1.39 | -61.9 % | +18.4 % | -80.3 % | -1.51 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.33 % | 0.90 | +0.040 |
| A | 5 | turn_of_month | +0.05 % | 0.45 | -0.006 |
| A | 5 | vix_level | +0.13 % | 0.42 | +0.034 |
| A | 5 | dip_52w | +0.23 % | 0.34 | -0.031 |
| A | 5 | trend_200 | +0.19 % | 0.31 | -0.020 |
| A | 5 | low_vol | +0.00 % | -0.01 | +0.001 |
| A | 5 | mom_1m | -0.13 % | -0.32 | +0.048 |
| A | 5 | rsi2_oversold | -0.40 % | -1.85 | +0.031 |
| B | 5 | dip_52w | -0.00 % | -0.05 | +0.028 |
| B | 5 | rev_1w | -0.02 % | -0.14 | +0.057 |
| B | 5 | mom_12_1 | -0.25 % | -0.48 | +0.058 |
| B | 5 | low_vol | -0.32 % | -0.92 | -0.006 |
| B | 5 | trend_200 | -0.25 % | -1.11 | -0.020 |
| B | 5 | rsi2_oversold | -0.06 % | -2.07 | -0.038 |
| B | 5 | mom_1m | -0.15 % | -6.62 | +0.026 |
| C | 5 | rsi2_oversold | +0.05 % | 1.93 | -0.008 |
| C | 5 | rev_1w | +0.07 % | 0.46 | +0.046 |
| C | 5 | mom_12_1 | -0.31 % | -1.00 | +0.026 |
| C | 5 | trend_200 | -0.14 % | -1.05 | -0.002 |
| C | 5 | low_vol | -0.18 % | -1.18 | -0.002 |
| C | 5 | dip_52w | -0.01 % | -2.09 | -0.008 |
| C | 5 | mom_1m | -0.08 % | -5.26 | +0.002 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 624 | 0.486 | 0.543 |
| 0.50–0.55 | 390 | 0.515 | 0.423 |
| 0.55–0.60 | 63 | 0.567 | 0.460 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-14): oben DBC 54 % (+1.8), UUP 52 % (+1.1), EWJ 56 % (+0.8), USO 52 % (+0.4), SPY 59 % (+0.2) · unten HYG 53 % (-4.3), IEF 49 % (-4.4), LQD 51 % (-4.8)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-14): oben UUP 53 % (+1.2), QQQ 64 % (-0.6), SPY 66 % (-0.7), DBC 54 % (-0.9), USO 52 % (-1.1) · unten IWM 56 % (-5.4), SLV 46 % (-5.5), HYG 57 % (-5.9)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-14): oben SMH 54 % (+3.9), EWY 53 % (+3.2), EWT 52 % (+2.3), XBI 52 % (+1.7), XLK 51 % (+1.4) · unten XLP 47 % (-2.8), XLRE 46 % (-3.6), XLF 46 % (-4.4)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-14): oben XLE 52 % (+2.3), EWY 52 % (+2.0), XBI 51 % (+1.3), EWW 51 % (+1.0), SMH 51 % (+1.0) · unten EWS 48 % (-2.0), XLRE 47 % (-2.7), XLF 46 % (-3.6)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-14): oben AMD 52 % (+2.2), INTC 52 % (+2.0), ASML 52 % (+1.6), TSM 52 % (+1.5), CSCO 51 % (+1.4) · unten ADBE 48 % (-2.3), PEP 48 % (-2.4), SAP 47 % (-2.5)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-14): oben INTC 52 % (+1.8), AMD 51 % (+1.3), MRK 51 % (+1.0), QCOM 51 % (+0.9), XOM 51 % (+0.7) · unten PLTR 48 % (-1.9), MA 48 % (-2.4), V 47 % (-2.9)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 197): mom_12_1 +0.040, mom_1m +0.048, trend_200 -0.020, dip_52w -0.031, low_vol +0.001, rsi2_oversold +0.031, vix_level +0.034, turn_of_month -0.006
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 374): mom_12_1 +0.058, mom_1m +0.026, rev_1w +0.057, trend_200 -0.020, dip_52w +0.028, low_vol -0.006, rsi2_oversold -0.038
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 506): mom_12_1 +0.026, mom_1m +0.002, rev_1w +0.046, trend_200 -0.002, dip_52w -0.008, low_vol -0.002, rsi2_oversold -0.008
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 11 | -0.51 | zu früh |
| B | 5 | 11 | -0.54 | zu früh |
| C | 5 | 11 | -1.39 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| rsi2_oversold | C | 5 | 11 | 1.93 | zu früh |
| mom_12_1 | A | 5 | 11 | 0.9 | zu früh |
| rev_1w | C | 5 | 11 | 0.46 | zu früh |
| turn_of_month | A | 5 | 11 | 0.45 | zu früh |
| vix_level | A | 5 | 11 | 0.42 | zu früh |
| dip_52w | A | 5 | 11 | 0.34 | zu früh |
| trend_200 | A | 5 | 11 | 0.31 | zu früh |
| low_vol | A | 5 | 11 | -0.01 | zu früh |
| dip_52w | B | 5 | 11 | -0.05 | zu früh |
| rev_1w | B | 5 | 11 | -0.14 | zu früh |
| mom_1m | A | 5 | 11 | -0.32 | zu früh |
| mom_12_1 | B | 5 | 11 | -0.48 | zu früh |
| low_vol | B | 5 | 11 | -0.92 | zu früh |
| mom_12_1 | C | 5 | 11 | -1.0 | zu früh |
| trend_200 | C | 5 | 11 | -1.05 | zu früh |
| trend_200 | B | 5 | 11 | -1.11 | zu früh |
| low_vol | C | 5 | 11 | -1.18 | zu früh |
| rsi2_oversold | A | 5 | 11 | -1.85 | zu früh |
| rsi2_oversold | B | 5 | 11 | -2.07 | zu früh |
| dip_52w | C | 5 | 11 | -2.09 | zu früh |
| mom_1m | C | 5 | 11 | -5.26 | zu früh |
| mom_1m | B | 5 | 11 | -6.62 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

