# Orakel – Stand 2026-10-07

Journal: 84 Eintraege, Hash-Kette OK, Kopf `3f6be40664a46e1c`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 6 | 108 | +0.45 % | 3.50 | -15.2 % | -19.1 % | +3.9 % | 0.79 |
| B Sektoren/Laender | 5 | 6 | 204 | +0.95 % | 5.13 | +83.6 % | -18.1 % | +101.7 % | 4.07 |
| C Einzeltitel | 5 | 6 | 276 | +0.10 % | 0.78 | +7.9 % | -3.1 % | +11.0 % | 1.87 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | trend_200 | +0.79 % | 2.79 | -0.017 |
| A | 5 | mom_12_1 | +0.69 % | 2.77 | +0.036 |
| A | 5 | dip_52w | +0.93 % | 2.52 | -0.039 |
| A | 5 | vix_level | +0.40 % | 1.36 | +0.044 |
| A | 5 | mom_1m | +0.26 % | 1.20 | +0.056 |
| A | 5 | turn_of_month | +0.13 % | 1.08 | +0.001 |
| A | 5 | low_vol | +0.09 % | 0.87 | +0.003 |
| A | 5 | rsi2_oversold | -0.61 % | -2.63 | +0.034 |
| B | 5 | low_vol | +0.22 % | 26.98 | -0.035 |
| B | 5 | mom_12_1 | +0.62 % | 8.92 | +0.072 |
| B | 5 | trend_200 | +0.13 % | 4.04 | -0.006 |
| B | 5 | rev_1w | -0.14 % | -0.74 | +0.050 |
| B | 5 | rsi2_oversold | -0.08 % | -1.82 | -0.021 |
| B | 5 | mom_1m | -0.13 % | -4.35 | +0.037 |
| B | 5 | dip_52w | -0.02 % | -6.02 | +0.023 |
| C | 5 | mom_12_1 | +0.24 % | 4.63 | +0.051 |
| C | 5 | trend_200 | +0.12 % | 4.42 | +0.002 |
| C | 5 | low_vol | +0.07 % | 3.09 | -0.022 |
| C | 5 | rsi2_oversold | -0.02 % | -0.25 | -0.005 |
| C | 5 | dip_52w | -0.01 % | -0.86 | +0.007 |
| C | 5 | rev_1w | -0.22 % | -2.35 | +0.036 |
| C | 5 | mom_1m | -0.10 % | -8.80 | +0.022 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 337 | 0.488 | 0.469 |
| 0.50–0.55 | 199 | 0.514 | 0.508 |
| 0.55–0.60 | 52 | 0.568 | 0.481 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-07): oben UUP 52 % (+1.1), USO 52 % (+0.5), DBC 53 % (+0.5), EWJ 55 % (-0.4), QQQ 57 % (-1.3) · unten IEF 48 % (-6.3), LQD 49 % (-6.8), HYG 50 % (-7.9)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-07): oben UUP 53 % (+0.7), QQQ 66 % (+0.6), SPY 66 % (-0.7), EWJ 58 % (-1.1), DBC 54 % (-1.7) · unten SLV 46 % (-5.8), IEF 51 % (-6.1), HYG 57 % (-6.3)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-07): oben EWY 54 % (+4.1), XBI 54 % (+3.5), SMH 53 % (+2.8), EWT 52 % (+2.2), EWZ 52 % (+1.8) · unten EWG 46 % (-3.5), INDA 46 % (-3.9), XLF 45 % (-4.6)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-07): oben EWZ 52 % (+2.0), EWT 52 % (+1.6), SMH 52 % (+1.5), XLE 52 % (+1.5), EWY 51 % (+1.5) · unten EWU 47 % (-3.0), EWQ 47 % (-3.1), INDA 46 % (-3.8)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-07): oben INTC 55 % (+4.7), ASML 53 % (+2.5), MRK 52 % (+2.1), AMD 52 % (+1.8), CAT 52 % (+1.5) · unten MCD 47 % (-2.6), MA 47 % (-3.0), ORCL 46 % (-3.7)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-07): oben AMZN 52 % (+2.3), INTC 52 % (+1.9), GOOGL 52 % (+1.7), AMD 52 % (+1.5), AVGO 51 % (+1.3) · unten JPM 47 % (-2.8), MCD 47 % (-3.0), PEP 47 % (-3.1)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 108): mom_12_1 +0.036, mom_1m +0.056, trend_200 -0.017, dip_52w -0.039, low_vol +0.003, rsi2_oversold +0.034, vix_level +0.044, turn_of_month +0.001
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 204): mom_12_1 +0.072, mom_1m +0.037, rev_1w +0.050, trend_200 -0.006, dip_52w +0.023, low_vol -0.035, rsi2_oversold -0.021
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 276): mom_12_1 +0.051, mom_1m +0.022, rev_1w +0.036, trend_200 +0.002, dip_52w +0.007, low_vol -0.022, rsi2_oversold -0.005
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 6 | 3.5 | zu früh |
| B | 5 | 6 | 5.13 | zu früh |
| C | 5 | 6 | 0.78 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| low_vol | B | 5 | 6 | 26.98 | zu früh |
| mom_12_1 | B | 5 | 6 | 8.92 | zu früh |
| mom_12_1 | C | 5 | 6 | 4.63 | zu früh |
| trend_200 | C | 5 | 6 | 4.42 | zu früh |
| trend_200 | B | 5 | 6 | 4.04 | zu früh |
| low_vol | C | 5 | 6 | 3.09 | zu früh |
| trend_200 | A | 5 | 6 | 2.79 | zu früh |
| mom_12_1 | A | 5 | 6 | 2.77 | zu früh |
| dip_52w | A | 5 | 6 | 2.52 | zu früh |
| vix_level | A | 5 | 6 | 1.36 | zu früh |
| mom_1m | A | 5 | 6 | 1.2 | zu früh |
| turn_of_month | A | 5 | 6 | 1.08 | zu früh |
| low_vol | A | 5 | 6 | 0.87 | zu früh |
| rsi2_oversold | C | 5 | 6 | -0.25 | zu früh |
| rev_1w | B | 5 | 6 | -0.74 | zu früh |
| dip_52w | C | 5 | 6 | -0.86 | zu früh |
| rsi2_oversold | B | 5 | 6 | -1.82 | zu früh |
| rev_1w | C | 5 | 6 | -2.35 | zu früh |
| rsi2_oversold | A | 5 | 6 | -2.63 | zu früh |
| mom_1m | B | 5 | 6 | -4.35 | zu früh |
| dip_52w | B | 5 | 6 | -6.02 | zu früh |
| mom_1m | C | 5 | 6 | -8.8 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

