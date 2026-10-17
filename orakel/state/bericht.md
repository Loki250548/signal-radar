# Orakel – Stand 2026-10-16

Journal: 147 Eintraege, Hash-Kette OK, Kopf `59af0c11f9580676`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 13 | 233 | -0.38 % | -0.61 | -7.0 % | -9.4 % | +2.4 % | 0.55 |
| B Sektoren/Laender | 5 | 13 | 442 | -1.12 % | -0.98 | -63.9 % | -8.9 % | -55.0 % | -0.65 |
| C Einzeltitel | 5 | 13 | 598 | -0.90 % | -1.69 | -94.9 % | +17.2 % | -112.1 % | -1.81 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.48 % | 1.62 | +0.046 |
| A | 5 | turn_of_month | +0.10 % | 1.16 | -0.005 |
| A | 5 | vix_level | +0.20 % | 0.86 | +0.035 |
| A | 5 | low_vol | +0.06 % | 0.62 | -0.001 |
| A | 5 | dip_52w | +0.27 % | 0.48 | -0.032 |
| A | 5 | trend_200 | +0.21 % | 0.43 | -0.024 |
| A | 5 | mom_1m | -0.17 % | -0.47 | +0.038 |
| A | 5 | rsi2_oversold | -0.29 % | -1.44 | +0.017 |
| B | 5 | dip_52w | -0.00 % | -0.15 | +0.028 |
| B | 5 | mom_12_1 | -0.46 % | -0.83 | +0.049 |
| B | 5 | rev_1w | -0.13 % | -0.87 | +0.044 |
| B | 5 | low_vol | -0.54 % | -1.25 | +0.011 |
| B | 5 | trend_200 | -0.30 % | -1.40 | -0.025 |
| B | 5 | rsi2_oversold | -0.07 % | -2.44 | -0.044 |
| B | 5 | mom_1m | -0.15 % | -7.53 | +0.015 |
| C | 5 | rev_1w | -0.03 % | -0.31 | +0.043 |
| C | 5 | rsi2_oversold | -0.06 % | -0.59 | -0.025 |
| C | 5 | dip_52w | -0.00 % | -1.11 | -0.006 |
| C | 5 | mom_12_1 | -0.43 % | -1.34 | +0.015 |
| C | 5 | trend_200 | -0.18 % | -1.35 | -0.002 |
| C | 5 | low_vol | -0.23 % | -1.49 | +0.013 |
| C | 5 | mom_1m | -0.07 % | -6.31 | -0.007 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 742 | 0.485 | 0.562 |
| 0.50–0.55 | 462 | 0.515 | 0.398 |
| 0.55–0.60 | 69 | 0.567 | 0.420 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-16): oben USO 55 % (+3.5), DBC 56 % (+3.3), UUP 53 % (+1.9), EWJ 56 % (+0.6), SPY 59 % (-0.2) · unten LQD 53 % (-3.3), GLD 51 % (-3.8), HYG 53 % (-4.5)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-16): oben USO 54 % (+1.4), DBC 56 % (+1.0), UUP 53 % (+0.9), SPY 66 % (-0.6), TLT 52 % (-1.2) · unten SLV 47 % (-4.3), EEM 54 % (-4.5), HYG 58 % (-5.1)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-16): oben EWY 53 % (+2.7), EWI 51 % (+1.2), XBI 51 % (+0.9), SMH 51 % (+0.7), KRE 51 % (+0.6) · unten XLV 48 % (-2.4), XLC 48 % (-2.5), XLP 47 % (-2.6)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-16): oben EWY 52 % (+2.4), XBI 51 % (+1.3), EWW 51 % (+1.1), SMH 51 % (+1.0), XLE 51 % (+1.0) · unten EWQ 48 % (-2.0), XLF 48 % (-2.2), INDA 47 % (-2.7)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-16): oben JNJ 51 % (+1.0), JPM 51 % (+0.7), CSCO 51 % (+0.6), AMD 51 % (+0.6), INTC 51 % (+0.6) · unten SAP 48 % (-2.1), CRM 48 % (-2.4), NKE 48 % (-2.4)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-16): oben INTC 52 % (+2.0), AMD 51 % (+1.3), ASML 51 % (+1.3), QCOM 51 % (+1.2), MRK 51 % (+0.9) · unten UNH 48 % (-1.9), V 48 % (-2.0), COST 48 % (-2.4)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 233): mom_12_1 +0.046, mom_1m +0.038, trend_200 -0.024, dip_52w -0.032, low_vol -0.001, rsi2_oversold +0.017, vix_level +0.035, turn_of_month -0.005
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 442): mom_12_1 +0.049, mom_1m +0.015, rev_1w +0.044, trend_200 -0.025, dip_52w +0.028, low_vol +0.011, rsi2_oversold -0.044
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 598): mom_12_1 +0.015, mom_1m -0.007, rev_1w +0.043, trend_200 -0.002, dip_52w -0.006, low_vol +0.013, rsi2_oversold -0.025
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 13 | -0.61 | zu früh |
| B | 5 | 13 | -0.98 | zu früh |
| C | 5 | 13 | -1.69 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| mom_12_1 | A | 5 | 13 | 1.62 | zu früh |
| turn_of_month | A | 5 | 13 | 1.16 | zu früh |
| vix_level | A | 5 | 13 | 0.86 | zu früh |
| low_vol | A | 5 | 13 | 0.62 | zu früh |
| dip_52w | A | 5 | 13 | 0.48 | zu früh |
| trend_200 | A | 5 | 13 | 0.43 | zu früh |
| dip_52w | B | 5 | 13 | -0.15 | zu früh |
| rev_1w | C | 5 | 13 | -0.31 | zu früh |
| mom_1m | A | 5 | 13 | -0.47 | zu früh |
| rsi2_oversold | C | 5 | 13 | -0.59 | zu früh |
| mom_12_1 | B | 5 | 13 | -0.83 | zu früh |
| rev_1w | B | 5 | 13 | -0.87 | zu früh |
| dip_52w | C | 5 | 13 | -1.11 | zu früh |
| low_vol | B | 5 | 13 | -1.25 | zu früh |
| mom_12_1 | C | 5 | 13 | -1.34 | zu früh |
| trend_200 | C | 5 | 13 | -1.35 | zu früh |
| trend_200 | B | 5 | 13 | -1.4 | zu früh |
| rsi2_oversold | A | 5 | 13 | -1.44 | zu früh |
| low_vol | C | 5 | 13 | -1.49 | zu früh |
| rsi2_oversold | B | 5 | 13 | -2.44 | zu früh |
| mom_1m | C | 5 | 13 | -6.31 | zu früh |
| mom_1m | B | 5 | 13 | -7.53 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

