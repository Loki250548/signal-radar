# Orakel – Stand 2026-10-06

Journal: 75 Eintraege, Hash-Kette OK, Kopf `c3e049bbf343b7dd`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 5 | 90 | +0.50 % | 3.19 | -18.2 % | -23.2 % | +4.9 % | 0.87 |
| B Sektoren/Laender | 5 | 5 | 170 | +1.01 % | 4.20 | +69.0 % | -26.8 % | +95.7 % | 3.54 |
| C Einzeltitel | 5 | 5 | 230 | +0.22 % | 3.31 | +8.0 % | -14.4 % | +22.5 % | 3.31 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | trend_200 | +1.05 % | 8.75 | -0.014 |
| A | 5 | mom_12_1 | +0.89 % | 6.57 | +0.036 |
| A | 5 | dip_52w | +1.17 % | 4.50 | -0.036 |
| A | 5 | mom_1m | +0.42 % | 3.00 | +0.058 |
| A | 5 | vix_level | +0.58 % | 2.74 | +0.045 |
| A | 5 | low_vol | +0.16 % | 1.92 | +0.001 |
| A | 5 | turn_of_month | +0.20 % | 1.90 | -0.003 |
| A | 5 | rsi2_oversold | -0.73 % | -3.62 | +0.031 |
| B | 5 | low_vol | +0.22 % | 23.11 | -0.030 |
| B | 5 | mom_12_1 | +0.66 % | 12.96 | +0.071 |
| B | 5 | trend_200 | +0.13 % | 3.51 | -0.004 |
| B | 5 | rev_1w | -0.14 % | -0.63 | +0.048 |
| B | 5 | rsi2_oversold | -0.07 % | -1.47 | -0.018 |
| B | 5 | dip_52w | -0.03 % | -7.15 | +0.028 |
| B | 5 | mom_1m | -0.16 % | -7.60 | +0.037 |
| C | 5 | low_vol | +0.11 % | 12.65 | -0.021 |
| C | 5 | trend_200 | +0.11 % | 4.44 | +0.005 |
| C | 5 | mom_12_1 | +0.24 % | 3.80 | +0.051 |
| C | 5 | rsi2_oversold | +0.02 % | 0.45 | -0.005 |
| C | 5 | dip_52w | -0.01 % | -1.47 | +0.012 |
| C | 5 | rev_1w | -0.15 % | -2.24 | +0.038 |
| C | 5 | mom_1m | -0.10 % | -8.82 | +0.020 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 280 | 0.488 | 0.457 |
| 0.50–0.55 | 166 | 0.514 | 0.512 |
| 0.55–0.60 | 44 | 0.569 | 0.432 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-06): oben UUP 53 % (+1.5), USO 52 % (+0.6), DBC 53 % (+0.5), EWJ 54 % (-1.6), QQQ 56 % (-1.9) · unten GLD 47 % (-7.0), LQD 49 % (-7.4), HYG 49 % (-8.7)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-06): oben QQQ 66 % (+0.8), UUP 52 % (-0.0), EWJ 59 % (-0.5), SPY 66 % (-0.6), DBC 54 % (-1.0) · unten SLV 46 % (-5.3), HYG 57 % (-5.9), IEF 51 % (-6.0)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-06): oben EWY 55 % (+4.9), XBI 53 % (+3.3), SMH 52 % (+2.2), EWT 52 % (+2.0), EWZ 52 % (+1.5) · unten XLU 47 % (-2.9), INDA 46 % (-3.8), XLF 46 % (-4.1)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-06): oben EWZ 53 % (+2.5), XLK 52 % (+2.1), XLE 52 % (+1.9), SMH 52 % (+1.7), EWJ 51 % (+1.3) · unten EWG 47 % (-2.7), EWU 47 % (-2.7), EWQ 47 % (-3.0)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-06): oben INTC 55 % (+4.7), MRK 53 % (+2.7), ASML 52 % (+2.2), AMD 52 % (+1.6), LLY 52 % (+1.6) · unten MA 47 % (-2.7), ADBE 47 % (-3.0), ORCL 47 % (-3.0)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-06): oben CAT 52 % (+2.4), AMD 52 % (+2.3), AMZN 52 % (+2.2), CSCO 52 % (+2.1), TXN 52 % (+1.7) · unten TMO 48 % (-2.4), MCD 48 % (-2.5), PEP 47 % (-3.3)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 90): mom_12_1 +0.036, mom_1m +0.058, trend_200 -0.014, dip_52w -0.036, low_vol +0.001, rsi2_oversold +0.031, vix_level +0.045, turn_of_month -0.003
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 170): mom_12_1 +0.071, mom_1m +0.037, rev_1w +0.048, trend_200 -0.004, dip_52w +0.028, low_vol -0.030, rsi2_oversold -0.018
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 230): mom_12_1 +0.051, mom_1m +0.020, rev_1w +0.038, trend_200 +0.005, dip_52w +0.012, low_vol -0.021, rsi2_oversold -0.005
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 5 | 3.19 | zu früh |
| B | 5 | 5 | 4.2 | zu früh |
| C | 5 | 5 | 3.31 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| low_vol | B | 5 | 5 | 23.11 | zu früh |
| mom_12_1 | B | 5 | 5 | 12.96 | zu früh |
| low_vol | C | 5 | 5 | 12.65 | zu früh |
| trend_200 | A | 5 | 5 | 8.75 | zu früh |
| mom_12_1 | A | 5 | 5 | 6.57 | zu früh |
| dip_52w | A | 5 | 5 | 4.5 | zu früh |
| trend_200 | C | 5 | 5 | 4.44 | zu früh |
| mom_12_1 | C | 5 | 5 | 3.8 | zu früh |
| trend_200 | B | 5 | 5 | 3.51 | zu früh |
| mom_1m | A | 5 | 5 | 3.0 | zu früh |
| vix_level | A | 5 | 5 | 2.74 | zu früh |
| low_vol | A | 5 | 5 | 1.92 | zu früh |
| turn_of_month | A | 5 | 5 | 1.9 | zu früh |
| rsi2_oversold | C | 5 | 5 | 0.45 | zu früh |
| rev_1w | B | 5 | 5 | -0.63 | zu früh |
| rsi2_oversold | B | 5 | 5 | -1.47 | zu früh |
| dip_52w | C | 5 | 5 | -1.47 | zu früh |
| rev_1w | C | 5 | 5 | -2.24 | zu früh |
| rsi2_oversold | A | 5 | 5 | -3.62 | zu früh |
| dip_52w | B | 5 | 5 | -7.15 | zu früh |
| mom_1m | B | 5 | 5 | -7.6 | zu früh |
| mom_1m | C | 5 | 5 | -8.82 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

