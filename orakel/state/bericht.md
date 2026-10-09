# Orakel – Stand 2026-10-08

Journal: 93 Eintraege, Hash-Kette OK, Kopf `1d3ad92e47a300dd`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 7 | 126 | +0.93 % | 2.36 | -13.0 % | -19.4 % | +6.4 % | 1.56 |
| B Sektoren/Laender | 5 | 7 | 238 | +0.71 % | 3.16 | +66.8 % | -16.7 % | +83.5 % | 4.39 |
| C Einzeltitel | 5 | 7 | 322 | -0.12 % | -0.46 | -12.0 % | +2.5 % | -14.5 % | -0.62 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | trend_200 | +1.10 % | 6.38 | -0.011 |
| A | 5 | mom_12_1 | +0.88 % | 6.09 | +0.034 |
| A | 5 | dip_52w | +1.26 % | 5.54 | -0.045 |
| A | 5 | mom_1m | +0.59 % | 3.20 | +0.058 |
| A | 5 | turn_of_month | +0.27 % | 2.89 | -0.001 |
| A | 5 | low_vol | +0.22 % | 2.85 | -0.002 |
| A | 5 | vix_level | +0.53 % | 2.81 | +0.048 |
| A | 5 | rsi2_oversold | -0.47 % | -1.67 | +0.029 |
| B | 5 | low_vol | +0.16 % | 3.65 | -0.035 |
| B | 5 | mom_12_1 | +0.41 % | 1.95 | +0.069 |
| B | 5 | trend_200 | +0.04 % | 0.62 | -0.011 |
| B | 5 | rev_1w | -0.07 % | -0.34 | +0.054 |
| B | 5 | rsi2_oversold | -0.06 % | -1.51 | -0.023 |
| B | 5 | mom_1m | -0.13 % | -4.00 | +0.034 |
| B | 5 | dip_52w | -0.02 % | -5.64 | +0.018 |
| C | 5 | rsi2_oversold | +0.03 % | 0.74 | -0.000 |
| C | 5 | mom_12_1 | +0.08 % | 0.61 | +0.050 |
| C | 5 | trend_200 | +0.01 % | 0.12 | -0.003 |
| C | 5 | low_vol | -0.00 % | -0.01 | -0.014 |
| C | 5 | dip_52w | -0.01 % | -1.01 | +0.008 |
| C | 5 | rev_1w | -0.17 % | -2.73 | +0.032 |
| C | 5 | mom_1m | -0.08 % | -4.63 | +0.020 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 395 | 0.488 | 0.484 |
| 0.50–0.55 | 235 | 0.514 | 0.481 |
| 0.55–0.60 | 56 | 0.568 | 0.464 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-08): oben UUP 53 % (+1.8), DBC 53 % (+0.2), USO 51 % (-0.2), EWJ 55 % (-0.2), QQQ 58 % (-0.5) · unten GLD 47 % (-7.3), LQD 49 % (-7.6), HYG 49 % (-8.4)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-08): oben UUP 53 % (+0.6), QQQ 65 % (-0.0), SPY 66 % (-0.8), DBC 54 % (-1.1), EWJ 58 % (-1.6) · unten IWM 56 % (-5.4), SLV 45 % (-6.0), HYG 57 % (-6.2)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-08): oben SMH 55 % (+4.9), EWY 54 % (+4.3), XBI 54 % (+3.5), EWT 53 % (+2.6), XLK 52 % (+2.3) · unten XLU 46 % (-3.6), INDA 46 % (-3.7), XLF 45 % (-4.6)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-08): oben XLE 52 % (+2.2), EWZ 52 % (+1.9), EWY 52 % (+1.5), XBI 51 % (+1.1), ITB 51 % (+0.8) · unten EWG 47 % (-2.9), EWQ 47 % (-3.0), INDA 46 % (-4.0)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-08): oben INTC 53 % (+3.4), ASML 53 % (+2.8), AMD 53 % (+2.8), CAT 53 % (+2.5), TSM 52 % (+1.9) · unten DIS 47 % (-2.9), HD 47 % (-3.3), NFLX 46 % (-3.5)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-08): oben INTC 51 % (+1.1), CRM 51 % (+1.0), MRK 51 % (+1.0), WMT 51 % (+0.8), CAT 51 % (+0.8) · unten PG 48 % (-2.3), MSFT 48 % (-2.4), LIN 47 % (-3.0)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 126): mom_12_1 +0.034, mom_1m +0.058, trend_200 -0.011, dip_52w -0.045, low_vol -0.002, rsi2_oversold +0.029, vix_level +0.048, turn_of_month -0.001
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 238): mom_12_1 +0.069, mom_1m +0.034, rev_1w +0.054, trend_200 -0.011, dip_52w +0.018, low_vol -0.035, rsi2_oversold -0.023
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 322): mom_12_1 +0.050, mom_1m +0.020, rev_1w +0.032, trend_200 -0.003, dip_52w +0.008, low_vol -0.014, rsi2_oversold -0.000
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 7 | 2.36 | zu früh |
| B | 5 | 7 | 3.16 | zu früh |
| C | 5 | 7 | -0.46 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| trend_200 | A | 5 | 7 | 6.38 | zu früh |
| mom_12_1 | A | 5 | 7 | 6.09 | zu früh |
| dip_52w | A | 5 | 7 | 5.54 | zu früh |
| low_vol | B | 5 | 7 | 3.65 | zu früh |
| mom_1m | A | 5 | 7 | 3.2 | zu früh |
| turn_of_month | A | 5 | 7 | 2.89 | zu früh |
| low_vol | A | 5 | 7 | 2.85 | zu früh |
| vix_level | A | 5 | 7 | 2.81 | zu früh |
| mom_12_1 | B | 5 | 7 | 1.95 | zu früh |
| rsi2_oversold | C | 5 | 7 | 0.74 | zu früh |
| trend_200 | B | 5 | 7 | 0.62 | zu früh |
| mom_12_1 | C | 5 | 7 | 0.61 | zu früh |
| trend_200 | C | 5 | 7 | 0.12 | zu früh |
| low_vol | C | 5 | 7 | -0.01 | zu früh |
| rev_1w | B | 5 | 7 | -0.34 | zu früh |
| dip_52w | C | 5 | 7 | -1.01 | zu früh |
| rsi2_oversold | B | 5 | 7 | -1.51 | zu früh |
| rsi2_oversold | A | 5 | 7 | -1.67 | zu früh |
| rev_1w | C | 5 | 7 | -2.73 | zu früh |
| mom_1m | B | 5 | 7 | -4.0 | zu früh |
| mom_1m | C | 5 | 7 | -4.63 | zu früh |
| dip_52w | B | 5 | 7 | -5.64 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

