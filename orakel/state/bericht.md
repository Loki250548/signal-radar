# Orakel – Stand 2026-10-19

Journal: 156 Eintraege, Hash-Kette OK, Kopf `6ca15b7ef6503b72`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 14 | 250 | -0.06 % | -0.08 | -6.5 % | -10.7 % | +4.2 % | 0.86 |
| B Sektoren/Laender | 5 | 14 | 476 | -1.32 % | -1.12 | -72.4 % | -10.6 % | -61.8 % | -0.75 |
| C Einzeltitel | 5 | 14 | 644 | -0.99 % | -1.83 | -103.9 % | +14.6 % | -118.4 % | -1.96 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.62 % | 1.86 | +0.047 |
| A | 5 | turn_of_month | +0.18 % | 1.50 | -0.001 |
| A | 5 | vix_level | +0.33 % | 1.28 | +0.039 |
| A | 5 | low_vol | +0.14 % | 1.09 | -0.005 |
| A | 5 | dip_52w | +0.46 % | 0.89 | -0.038 |
| A | 5 | trend_200 | +0.40 % | 0.88 | -0.024 |
| A | 5 | mom_1m | +0.00 % | 0.02 | +0.037 |
| A | 5 | rsi2_oversold | -0.20 % | -0.86 | +0.013 |
| B | 5 | dip_52w | -0.01 % | -0.65 | +0.024 |
| B | 5 | mom_12_1 | -0.52 % | -0.96 | +0.045 |
| B | 5 | rev_1w | -0.20 % | -1.07 | +0.038 |
| B | 5 | low_vol | -0.58 % | -1.37 | +0.015 |
| B | 5 | trend_200 | -0.30 % | -1.51 | -0.029 |
| B | 5 | rsi2_oversold | -0.08 % | -2.53 | -0.046 |
| B | 5 | mom_1m | -0.14 % | -8.26 | +0.010 |
| C | 5 | rev_1w | -0.09 % | -0.69 | +0.039 |
| C | 5 | rsi2_oversold | -0.09 % | -0.80 | -0.028 |
| C | 5 | dip_52w | -0.00 % | -0.91 | -0.002 |
| C | 5 | trend_200 | -0.18 % | -1.47 | -0.002 |
| C | 5 | mom_12_1 | -0.46 % | -1.48 | +0.013 |
| C | 5 | low_vol | -0.23 % | -1.60 | +0.020 |
| C | 5 | mom_1m | -0.07 % | -6.12 | -0.007 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 806 | 0.485 | 0.567 |
| 0.50–0.55 | 494 | 0.516 | 0.383 |
| 0.55–0.60 | 70 | 0.567 | 0.414 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-19): oben USO 55 % (+3.7), DBC 56 % (+3.3), UUP 52 % (+1.1), EWJ 55 % (-0.3), SPY 58 % (-1.0) · unten LQD 52 % (-3.9), GLD 50 % (-4.8), HYG 52 % (-5.4)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-19): oben USO 54 % (+0.8), UUP 53 % (+0.7), DBC 56 % (+0.5), SPY 66 % (-0.9), QQQ 64 % (-1.4) · unten IWM 56 % (-4.7), SLV 46 % (-4.8), HYG 58 % (-5.4)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-19): oben EWY 54 % (+4.4), XBI 52 % (+2.0), SMH 52 % (+1.9), KRE 51 % (+1.4), XLK 51 % (+0.8) · unten EWG 48 % (-2.3), XLV 48 % (-2.3), XLP 48 % (-2.4)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-19): oben EWY 55 % (+5.0), XBI 53 % (+3.4), SMH 53 % (+3.2), EWZ 52 % (+2.1), EWT 52 % (+1.9) · unten EWQ 47 % (-2.9), XLRE 47 % (-3.3), EWG 46 % (-3.7)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-19): oben BRK-B 51 % (+0.9), JNJ 51 % (+0.8), TSM 51 % (+0.7), BAC 51 % (+0.6), LIN 50 % (+0.4) · unten META 48 % (-1.7), CRM 48 % (-2.1), ADBE 48 % (-2.3)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-19): oben INTC 53 % (+2.7), AMZN 52 % (+1.6), AMD 51 % (+1.4), ASML 51 % (+1.1), TSM 51 % (+0.9) · unten PG 47 % (-2.8), JPM 47 % (-2.8), DIS 47 % (-3.3)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 250): mom_12_1 +0.047, mom_1m +0.037, trend_200 -0.024, dip_52w -0.038, low_vol -0.005, rsi2_oversold +0.013, vix_level +0.039, turn_of_month -0.001
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 476): mom_12_1 +0.045, mom_1m +0.010, rev_1w +0.038, trend_200 -0.029, dip_52w +0.024, low_vol +0.015, rsi2_oversold -0.046
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 644): mom_12_1 +0.013, mom_1m -0.007, rev_1w +0.039, trend_200 -0.002, dip_52w -0.002, low_vol +0.020, rsi2_oversold -0.028
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 14 | -0.08 | zu früh |
| B | 5 | 14 | -1.12 | zu früh |
| C | 5 | 14 | -1.83 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| mom_12_1 | A | 5 | 14 | 1.86 | zu früh |
| turn_of_month | A | 5 | 14 | 1.5 | zu früh |
| vix_level | A | 5 | 14 | 1.28 | zu früh |
| low_vol | A | 5 | 14 | 1.09 | zu früh |
| dip_52w | A | 5 | 14 | 0.89 | zu früh |
| trend_200 | A | 5 | 14 | 0.88 | zu früh |
| mom_1m | A | 5 | 14 | 0.02 | zu früh |
| dip_52w | B | 5 | 14 | -0.65 | zu früh |
| rev_1w | C | 5 | 14 | -0.69 | zu früh |
| rsi2_oversold | C | 5 | 14 | -0.8 | zu früh |
| rsi2_oversold | A | 5 | 14 | -0.86 | zu früh |
| dip_52w | C | 5 | 14 | -0.91 | zu früh |
| mom_12_1 | B | 5 | 14 | -0.96 | zu früh |
| rev_1w | B | 5 | 14 | -1.07 | zu früh |
| low_vol | B | 5 | 14 | -1.37 | zu früh |
| trend_200 | C | 5 | 14 | -1.47 | zu früh |
| mom_12_1 | C | 5 | 14 | -1.48 | zu früh |
| trend_200 | B | 5 | 14 | -1.51 | zu früh |
| low_vol | C | 5 | 14 | -1.6 | zu früh |
| rsi2_oversold | B | 5 | 14 | -2.53 | zu früh |
| mom_1m | C | 5 | 14 | -6.12 | zu früh |
| mom_1m | B | 5 | 14 | -8.26 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

