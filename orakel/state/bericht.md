# Orakel – Stand 2026-10-02

Journal: 57 Eintraege, Hash-Kette OK, Kopf `1b9ef3999817be86`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 3 | 54 | +0.22 % | 0.93 | -44.4 % | -47.4 % | +3.0 % | 0.41 |
| B Sektoren/Laender | 5 | 3 | 102 | +0.76 % | 2.85 | -4.1 % | -58.3 % | +54.2 % | 2.69 |
| C Einzeltitel | 5 | 3 | 138 | +0.30 % | 7.87 | -32.8 % | -44.4 % | +11.6 % | 3.31 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | trend_200 | +1.15 % | 49.03 | -0.019 |
| A | 5 | dip_52w | +1.52 % | 14.86 | -0.036 |
| A | 5 | mom_1m | +0.62 % | 10.07 | +0.050 |
| A | 5 | vix_level | +0.90 % | 9.90 | +0.043 |
| A | 5 | mom_12_1 | +1.01 % | 9.35 | +0.034 |
| A | 5 | low_vol | +0.29 % | 7.42 | +0.004 |
| A | 5 | turn_of_month | +0.33 % | 3.79 | -0.004 |
| A | 5 | rsi2_oversold | -1.02 % | -4.50 | +0.027 |
| B | 5 | low_vol | +0.22 % | 25.33 | -0.021 |
| B | 5 | mom_12_1 | +0.78 % | 19.58 | +0.064 |
| B | 5 | trend_200 | +0.13 % | 2.15 | -0.003 |
| B | 5 | rsi2_oversold | -0.13 % | -2.41 | -0.016 |
| B | 5 | rev_1w | -0.45 % | -2.44 | +0.040 |
| B | 5 | dip_52w | -0.02 % | -6.66 | +0.022 |
| B | 5 | mom_1m | -0.19 % | -11.80 | +0.028 |
| C | 5 | trend_200 | +0.06 % | 11.49 | +0.008 |
| C | 5 | low_vol | +0.10 % | 9.35 | -0.010 |
| C | 5 | rsi2_oversold | +0.12 % | 3.52 | -0.004 |
| C | 5 | mom_12_1 | +0.21 % | 1.95 | +0.050 |
| C | 5 | rev_1w | -0.04 % | -0.51 | +0.039 |
| C | 5 | mom_1m | -0.10 % | -5.61 | +0.020 |
| C | 5 | dip_52w | -0.02 % | -34.64 | +0.022 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 168 | 0.488 | 0.470 |
| 0.50–0.55 | 104 | 0.514 | 0.481 |
| 0.55–0.60 | 22 | 0.568 | 0.182 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-02): oben UUP 52 % (+0.5), USO 52 % (+0.4), DBC 53 % (+0.3), EWJ 54 % (-1.0), QQQ 56 % (-1.9) · unten GLD 49 % (-5.4), LQD 50 % (-5.6), HYG 51 % (-6.8)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-02): oben QQQ 66 % (+1.1), EWJ 59 % (+0.1), UUP 52 % (+0.0), DBC 54 % (-0.8), SPY 66 % (-0.8) · unten SLV 46 % (-5.3), IEF 51 % (-5.8), HYG 57 % (-6.7)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-02): oben EWY 53 % (+3.5), SMH 52 % (+2.1), EWT 52 % (+1.9), EWP 52 % (+1.7), EWZ 51 % (+1.4) · unten XLRE 47 % (-3.0), XLF 47 % (-3.2), XLU 47 % (-3.3)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-02): oben EWY 53 % (+3.5), SMH 53 % (+3.2), EWZ 53 % (+2.6), EWT 53 % (+2.6), XLK 52 % (+2.2) · unten XLRE 47 % (-3.0), EWS 47 % (-3.2), XLF 46 % (-3.8)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-02): oben INTC 54 % (+3.7), QCOM 52 % (+2.2), MRK 52 % (+1.6), AMD 52 % (+1.5), JNJ 51 % (+1.3) · unten BRK-B 48 % (-2.4), ORCL 47 % (-3.0), ADBE 47 % (-3.2)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-02): oben AMD 53 % (+3.0), CSCO 52 % (+2.4), INTC 52 % (+2.3), CAT 52 % (+2.3), ASML 52 % (+2.1) · unten PG 47 % (-2.9), PEP 47 % (-3.0), KO 47 % (-3.0)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 54): mom_12_1 +0.034, mom_1m +0.050, trend_200 -0.019, dip_52w -0.036, low_vol +0.004, rsi2_oversold +0.027, vix_level +0.043, turn_of_month -0.004
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 102): mom_12_1 +0.064, mom_1m +0.028, rev_1w +0.040, trend_200 -0.003, dip_52w +0.022, low_vol -0.021, rsi2_oversold -0.016
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 138): mom_12_1 +0.050, mom_1m +0.020, rev_1w +0.039, trend_200 +0.008, dip_52w +0.022, low_vol -0.010, rsi2_oversold -0.004
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 3 | 0.93 | zu früh |
| B | 5 | 3 | 2.85 | zu früh |
| C | 5 | 3 | 7.87 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| trend_200 | A | 5 | 3 | 49.03 | zu früh |
| low_vol | B | 5 | 3 | 25.33 | zu früh |
| mom_12_1 | B | 5 | 3 | 19.58 | zu früh |
| dip_52w | A | 5 | 3 | 14.86 | zu früh |
| trend_200 | C | 5 | 3 | 11.49 | zu früh |
| mom_1m | A | 5 | 3 | 10.07 | zu früh |
| vix_level | A | 5 | 3 | 9.9 | zu früh |
| mom_12_1 | A | 5 | 3 | 9.35 | zu früh |
| low_vol | C | 5 | 3 | 9.35 | zu früh |
| low_vol | A | 5 | 3 | 7.42 | zu früh |
| turn_of_month | A | 5 | 3 | 3.79 | zu früh |
| rsi2_oversold | C | 5 | 3 | 3.52 | zu früh |
| trend_200 | B | 5 | 3 | 2.15 | zu früh |
| mom_12_1 | C | 5 | 3 | 1.95 | zu früh |
| rev_1w | C | 5 | 3 | -0.51 | zu früh |
| rsi2_oversold | B | 5 | 3 | -2.41 | zu früh |
| rev_1w | B | 5 | 3 | -2.44 | zu früh |
| rsi2_oversold | A | 5 | 3 | -4.5 | zu früh |
| mom_1m | C | 5 | 3 | -5.61 | zu früh |
| dip_52w | B | 5 | 3 | -6.66 | zu früh |
| mom_1m | B | 5 | 3 | -11.8 | zu früh |
| dip_52w | C | 5 | 3 | -34.64 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

