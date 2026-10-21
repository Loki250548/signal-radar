# Orakel – Stand 2026-10-20

Journal: 165 Eintraege, Hash-Kette OK, Kopf `490b923dc5fe7dea`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 15 | 268 | -0.29 % | -0.52 | -6.1 % | -8.6 % | +2.5 % | 0.65 |
| B Sektoren/Laender | 5 | 15 | 510 | -1.40 % | -1.24 | -75.8 % | -6.8 % | -69.0 % | -0.86 |
| C Einzeltitel | 5 | 15 | 690 | -1.08 % | -1.97 | -110.8 % | +15.9 % | -126.6 % | -2.12 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.57 % | 1.99 | +0.052 |
| A | 5 | turn_of_month | +0.15 % | 1.59 | -0.002 |
| A | 5 | vix_level | +0.27 % | 1.26 | +0.037 |
| A | 5 | low_vol | +0.11 % | 1.08 | -0.003 |
| A | 5 | dip_52w | +0.32 % | 0.71 | -0.033 |
| A | 5 | trend_200 | +0.27 % | 0.69 | -0.029 |
| A | 5 | mom_1m | -0.09 % | -0.29 | +0.033 |
| A | 5 | rsi2_oversold | -0.25 % | -1.23 | +0.003 |
| B | 5 | dip_52w | -0.01 % | -0.71 | +0.024 |
| B | 5 | mom_12_1 | -0.54 % | -1.06 | +0.041 |
| B | 5 | rev_1w | -0.23 % | -1.20 | +0.031 |
| B | 5 | low_vol | -0.59 % | -1.48 | +0.020 |
| B | 5 | trend_200 | -0.29 % | -1.58 | -0.030 |
| B | 5 | rsi2_oversold | -0.08 % | -2.71 | -0.046 |
| B | 5 | mom_1m | -0.13 % | -6.97 | +0.006 |
| C | 5 | dip_52w | -0.00 % | -0.52 | -0.003 |
| C | 5 | rsi2_oversold | -0.10 % | -0.87 | -0.024 |
| C | 5 | rev_1w | -0.15 % | -0.91 | +0.028 |
| C | 5 | trend_200 | -0.18 % | -1.59 | -0.000 |
| C | 5 | mom_12_1 | -0.47 % | -1.61 | +0.007 |
| C | 5 | low_vol | -0.23 % | -1.71 | +0.027 |
| C | 5 | mom_1m | -0.05 % | -2.82 | -0.016 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 861 | 0.485 | 0.570 |
| 0.50–0.55 | 533 | 0.516 | 0.385 |
| 0.55–0.60 | 74 | 0.567 | 0.405 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-20): oben USO 55 % (+3.8), DBC 56 % (+3.1), UUP 51 % (+0.4), EWJ 54 % (-0.7), DIA 57 % (-1.2) · unten LQD 52 % (-4.0), GLD 50 % (-4.6), HYG 52 % (-5.5)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-20): oben USO 53 % (+0.4), DBC 55 % (-0.1), UUP 52 % (-0.2), SPY 66 % (-1.3), DIA 64 % (-1.5) · unten SLV 46 % (-5.0), EEM 53 % (-5.5), HYG 57 % (-5.8)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-20): oben EWY 52 % (+2.1), EWI 51 % (+1.0), KRE 51 % (+1.0), EWH 51 % (+0.5), INDA 50 % (+0.4) · unten XLP 48 % (-2.3), XLC 48 % (-2.3), XLV 48 % (-2.5)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-20): oben EWY 53 % (+2.9), XBI 53 % (+2.7), EWZ 52 % (+2.4), EWW 51 % (+1.4), SMH 51 % (+1.3) · unten EWG 47 % (-2.7), EWU 47 % (-2.7), EWQ 47 % (-2.9)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-20): oben BAC 51 % (+0.9), BRK-B 51 % (+0.8), JPM 51 % (+0.7), V 51 % (+0.6), MA 50 % (+0.4) · unten CRM 48 % (-1.8), WMT 48 % (-2.1), ADBE 48 % (-2.2)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-20): oben INTC 53 % (+2.5), QCOM 52 % (+1.7), AMZN 51 % (+1.5), AMD 51 % (+1.4), MRK 51 % (+1.3) · unten JPM 48 % (-2.3), NFLX 48 % (-2.5), PG 47 % (-3.1)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 268): mom_12_1 +0.052, mom_1m +0.033, trend_200 -0.029, dip_52w -0.033, low_vol -0.003, rsi2_oversold +0.003, vix_level +0.037, turn_of_month -0.002
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 510): mom_12_1 +0.041, mom_1m +0.006, rev_1w +0.031, trend_200 -0.030, dip_52w +0.024, low_vol +0.020, rsi2_oversold -0.046
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 690): mom_12_1 +0.007, mom_1m -0.016, rev_1w +0.028, trend_200 -0.000, dip_52w -0.003, low_vol +0.027, rsi2_oversold -0.024
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 15 | -0.52 | zu früh |
| B | 5 | 15 | -1.24 | zu früh |
| C | 5 | 15 | -1.97 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| mom_12_1 | A | 5 | 15 | 1.99 | zu früh |
| turn_of_month | A | 5 | 15 | 1.59 | zu früh |
| vix_level | A | 5 | 15 | 1.26 | zu früh |
| low_vol | A | 5 | 15 | 1.08 | zu früh |
| dip_52w | A | 5 | 15 | 0.71 | zu früh |
| trend_200 | A | 5 | 15 | 0.69 | zu früh |
| mom_1m | A | 5 | 15 | -0.29 | zu früh |
| dip_52w | C | 5 | 15 | -0.52 | zu früh |
| dip_52w | B | 5 | 15 | -0.71 | zu früh |
| rsi2_oversold | C | 5 | 15 | -0.87 | zu früh |
| rev_1w | C | 5 | 15 | -0.91 | zu früh |
| mom_12_1 | B | 5 | 15 | -1.06 | zu früh |
| rev_1w | B | 5 | 15 | -1.2 | zu früh |
| rsi2_oversold | A | 5 | 15 | -1.23 | zu früh |
| low_vol | B | 5 | 15 | -1.48 | zu früh |
| trend_200 | B | 5 | 15 | -1.58 | zu früh |
| trend_200 | C | 5 | 15 | -1.59 | zu früh |
| mom_12_1 | C | 5 | 15 | -1.61 | zu früh |
| low_vol | C | 5 | 15 | -1.71 | zu früh |
| rsi2_oversold | B | 5 | 15 | -2.71 | zu früh |
| mom_1m | C | 5 | 15 | -2.82 | zu früh |
| mom_1m | B | 5 | 15 | -6.97 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

