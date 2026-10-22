# Orakel – Stand 2026-10-21

Journal: 177 Eintraege, Hash-Kette OK, Kopf `050f6727b369fdb3`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 16 | 286 | -0.19 % | -0.36 | -5.7 % | -6.0 % | +0.3 % | 0.09 |
| A Markt | 20 | 1 | 18 | +3.52 % | nan | +0.0 % | -10.2 % | +nan % | nan |
| B Sektoren/Laender | 5 | 16 | 544 | -1.27 % | -1.24 | -64.6 % | -2.6 % | -62.0 % | -0.85 |
| B Sektoren/Laender | 20 | 1 | 34 | -2.13 % | nan | -20.2 % | +0.3 % | +nan % | nan |
| C Einzeltitel | 5 | 16 | 736 | -1.04 % | -2.08 | -99.0 % | +17.9 % | -116.9 % | -2.17 |
| C Einzeltitel | 20 | 1 | 46 | -1.39 % | nan | -20.4 % | +23.5 % | +nan % | nan |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.61 % | 2.13 | +0.059 |
| A | 5 | turn_of_month | +0.11 % | 1.42 | -0.005 |
| A | 5 | vix_level | +0.21 % | 1.12 | +0.034 |
| A | 5 | low_vol | +0.06 % | 0.75 | -0.005 |
| A | 5 | trend_200 | +0.22 % | 0.59 | -0.030 |
| A | 5 | dip_52w | +0.24 % | 0.58 | -0.030 |
| A | 5 | mom_1m | -0.19 % | -0.63 | +0.033 |
| A | 5 | rsi2_oversold | -0.23 % | -1.16 | +0.013 |
| A | 20 | vix_level | +1.03 % | -99.00 | +0.039 |
| A | 20 | turn_of_month | +0.60 % | -99.00 | -0.023 |
| A | 20 | trend_200 | +1.03 % | -99.00 | +0.009 |
| A | 20 | rsi2_oversold | +0.53 % | -99.00 | +0.002 |
| A | 20 | mom_1m | +2.53 % | -99.00 | +0.042 |
| A | 20 | mom_12_1 | +0.35 % | -99.00 | -0.027 |
| A | 20 | low_vol | +0.97 % | -99.00 | -0.043 |
| A | 20 | dip_52w | +1.58 % | -99.00 | -0.054 |
| B | 5 | dip_52w | -0.01 % | -0.76 | +0.022 |
| B | 5 | mom_12_1 | -0.49 % | -1.03 | +0.042 |
| B | 5 | rev_1w | -0.19 % | -1.18 | +0.033 |
| B | 5 | low_vol | -0.53 % | -1.46 | +0.016 |
| B | 5 | trend_200 | -0.27 % | -1.57 | -0.028 |
| B | 5 | rsi2_oversold | -0.08 % | -2.88 | -0.044 |
| B | 5 | mom_1m | -0.13 % | -5.50 | +0.006 |
| B | 20 | trend_200 | -0.01 % | -99.00 | -0.008 |
| B | 20 | rsi2_oversold | -1.01 % | -99.00 | -0.044 |
| B | 20 | rev_1w | -0.57 % | -99.00 | +0.016 |
| B | 20 | mom_1m | -0.01 % | -99.00 | -0.006 |
| B | 20 | mom_12_1 | -0.20 % | -99.00 | +0.036 |
| B | 20 | low_vol | -0.72 % | -99.00 | -0.036 |
| B | 20 | dip_52w | -0.08 % | -99.00 | +0.008 |
| C | 5 | rsi2_oversold | -0.08 % | -0.85 | -0.022 |
| C | 5 | rev_1w | -0.15 % | -0.97 | +0.026 |
| C | 5 | trend_200 | -0.17 % | -1.63 | +0.001 |
| C | 5 | dip_52w | -0.01 % | -1.66 | -0.002 |
| C | 5 | mom_12_1 | -0.45 % | -1.67 | +0.006 |
| C | 5 | low_vol | -0.22 % | -1.74 | +0.025 |
| C | 5 | mom_1m | -0.05 % | -2.29 | -0.016 |
| C | 20 | trend_200 | -0.07 % | -99.00 | -0.010 |
| C | 20 | rsi2_oversold | +0.03 % | -99.00 | -0.052 |
| C | 20 | rev_1w | -0.25 % | -99.00 | +0.015 |
| C | 20 | mom_1m | -0.01 % | -99.00 | -0.007 |
| C | 20 | mom_12_1 | -0.45 % | -99.00 | +0.036 |
| C | 20 | low_vol | -1.04 % | -99.00 | -0.035 |
| C | 20 | dip_52w | -0.06 % | -99.00 | +0.010 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 970 | 0.485 | 0.562 |
| 0.50–0.55 | 605 | 0.516 | 0.402 |
| 0.55–0.60 | 86 | 0.568 | 0.419 |
| 0.60–1.00 | 3 | 0.645 | 0.667 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-21): oben USO 56 % (+4.4), DBC 56 % (+3.5), UUP 52 % (+0.4), EWJ 54 % (-1.1), DIA 56 % (-1.7) · unten LQD 52 % (-4.4), GLD 49 % (-5.0), HYG 52 % (-6.0)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-21): oben USO 54 % (+1.0), DBC 56 % (+0.3), UUP 52 % (-0.2), DIA 65 % (-1.1), SPY 66 % (-1.3) · unten SLV 45 % (-5.9), EEM 52 % (-6.1), HYG 56 % (-6.8)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-21): oben EWY 53 % (+2.7), XLI 52 % (+1.8), EWI 52 % (+1.6), EWT 51 % (+1.1), SMH 51 % (+1.0) · unten ITB 47 % (-2.6), XLV 47 % (-3.3), XLP 47 % (-3.4)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-21): oben EWY 53 % (+3.3), EWT 53 % (+3.0), SMH 53 % (+2.8), EWN 52 % (+1.9), XLK 52 % (+1.9) · unten XLRE 46 % (-4.0), INDA 46 % (-4.1), XLP 46 % (-4.1)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-21): oben BAC 51 % (+0.7), JPM 51 % (+0.7), CAT 51 % (+0.6), BRK-B 51 % (+0.6), TSM 51 % (+0.5) · unten NKE 48 % (-2.3), CRM 48 % (-2.5), ADBE 47 % (-2.9)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-21): oben INTC 53 % (+3.1), AMD 53 % (+2.8), CAT 53 % (+2.7), TXN 52 % (+2.3), ASML 52 % (+2.2) · unten ABBV 47 % (-3.2), KO 47 % (-3.5), PG 46 % (-4.1)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 286): mom_12_1 +0.059, mom_1m +0.033, trend_200 -0.030, dip_52w -0.030, low_vol -0.005, rsi2_oversold +0.013, vix_level +0.034, turn_of_month -0.005
- A20 (Vorwaertsdaten: 18): mom_12_1 -0.027, mom_1m +0.042, trend_200 +0.009, dip_52w -0.054, low_vol -0.043, rsi2_oversold +0.002, vix_level +0.039, turn_of_month -0.023
- B5 (Vorwaertsdaten: 544): mom_12_1 +0.042, mom_1m +0.006, rev_1w +0.033, trend_200 -0.028, dip_52w +0.022, low_vol +0.016, rsi2_oversold -0.044
- B20 (Vorwaertsdaten: 34): mom_12_1 +0.036, mom_1m -0.006, rev_1w +0.016, trend_200 -0.008, dip_52w +0.008, low_vol -0.036, rsi2_oversold -0.044
- C5 (Vorwaertsdaten: 736): mom_12_1 +0.006, mom_1m -0.016, rev_1w +0.026, trend_200 +0.001, dip_52w -0.002, low_vol +0.025, rsi2_oversold -0.022
- C20 (Vorwaertsdaten: 46): mom_12_1 +0.036, mom_1m -0.007, rev_1w +0.015, trend_200 -0.010, dip_52w +0.010, low_vol -0.035, rsi2_oversold -0.052

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 16 | -0.36 | zu früh |
| A | 20 | 1 | None | zu früh |
| B | 5 | 16 | -1.24 | zu früh |
| B | 20 | 1 | None | zu früh |
| C | 5 | 16 | -2.08 | zu früh |
| C | 20 | 1 | None | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| mom_12_1 | A | 5 | 16 | 2.13 | zu früh |
| turn_of_month | A | 5 | 16 | 1.42 | zu früh |
| vix_level | A | 5 | 16 | 1.12 | zu früh |
| low_vol | A | 5 | 16 | 0.75 | zu früh |
| trend_200 | A | 5 | 16 | 0.59 | zu früh |
| dip_52w | A | 5 | 16 | 0.58 | zu früh |
| mom_1m | A | 5 | 16 | -0.63 | zu früh |
| dip_52w | B | 5 | 16 | -0.76 | zu früh |
| rsi2_oversold | C | 5 | 16 | -0.85 | zu früh |
| rev_1w | C | 5 | 16 | -0.97 | zu früh |
| mom_12_1 | B | 5 | 16 | -1.03 | zu früh |
| rsi2_oversold | A | 5 | 16 | -1.16 | zu früh |
| rev_1w | B | 5 | 16 | -1.18 | zu früh |
| low_vol | B | 5 | 16 | -1.46 | zu früh |
| trend_200 | B | 5 | 16 | -1.57 | zu früh |
| trend_200 | C | 5 | 16 | -1.63 | zu früh |
| dip_52w | C | 5 | 16 | -1.66 | zu früh |
| mom_12_1 | C | 5 | 16 | -1.67 | zu früh |
| low_vol | C | 5 | 16 | -1.74 | zu früh |
| mom_1m | C | 5 | 16 | -2.29 | zu früh |
| rsi2_oversold | B | 5 | 16 | -2.88 | zu früh |
| mom_1m | B | 5 | 16 | -5.5 | zu früh |
| mom_12_1 | A | 20 | 1 | None | zu früh |
| mom_1m | A | 20 | 1 | None | zu früh |
| trend_200 | A | 20 | 1 | None | zu früh |
| dip_52w | A | 20 | 1 | None | zu früh |
| low_vol | A | 20 | 1 | None | zu früh |
| rsi2_oversold | A | 20 | 1 | None | zu früh |
| vix_level | A | 20 | 1 | None | zu früh |
| turn_of_month | A | 20 | 1 | None | zu früh |
| mom_12_1 | B | 20 | 1 | None | zu früh |
| mom_1m | B | 20 | 1 | None | zu früh |
| rev_1w | B | 20 | 1 | None | zu früh |
| trend_200 | B | 20 | 1 | None | zu früh |
| dip_52w | B | 20 | 1 | None | zu früh |
| low_vol | B | 20 | 1 | None | zu früh |
| rsi2_oversold | B | 20 | 1 | None | zu früh |
| mom_12_1 | C | 20 | 1 | None | zu früh |
| mom_1m | C | 20 | 1 | None | zu früh |
| rev_1w | C | 20 | 1 | None | zu früh |
| trend_200 | C | 20 | 1 | None | zu früh |
| dip_52w | C | 20 | 1 | None | zu früh |
| low_vol | C | 20 | 1 | None | zu früh |
| rsi2_oversold | C | 20 | 1 | None | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (1/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

