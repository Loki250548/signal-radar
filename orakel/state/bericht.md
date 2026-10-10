# Orakel – Stand 2026-10-09

Journal: 102 Eintraege, Hash-Kette OK, Kopf `064dffccdab06042`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 8 | 144 | +0.51 % | 2.49 | -11.4 % | -15.0 % | +3.6 % | 0.81 |
| B Sektoren/Laender | 5 | 8 | 272 | +0.41 % | 1.01 | +43.4 % | -13.9 % | +57.3 % | 1.86 |
| C Einzeltitel | 5 | 8 | 368 | -0.25 % | -0.78 | -22.3 % | +11.9 % | -34.2 % | -0.99 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | trend_200 | +0.79 % | 3.11 | -0.013 |
| A | 5 | dip_52w | +0.92 % | 2.83 | -0.044 |
| A | 5 | mom_12_1 | +0.64 % | 2.63 | +0.032 |
| A | 5 | turn_of_month | +0.19 % | 2.41 | -0.002 |
| A | 5 | mom_1m | +0.36 % | 2.20 | +0.054 |
| A | 5 | low_vol | +0.14 % | 1.92 | -0.003 |
| A | 5 | vix_level | +0.39 % | 1.74 | +0.043 |
| A | 5 | rsi2_oversold | -0.42 % | -1.53 | +0.033 |
| B | 5 | mom_12_1 | +0.25 % | 0.82 | +0.067 |
| B | 5 | low_vol | +0.07 % | 0.57 | -0.031 |
| B | 5 | rev_1w | -0.04 % | -0.22 | +0.053 |
| B | 5 | trend_200 | -0.04 % | -0.34 | -0.014 |
| B | 5 | rsi2_oversold | -0.05 % | -1.29 | -0.022 |
| B | 5 | dip_52w | -0.02 % | -3.87 | +0.018 |
| B | 5 | mom_1m | -0.13 % | -5.06 | +0.032 |
| C | 5 | rsi2_oversold | +0.06 % | 1.45 | +0.003 |
| C | 5 | mom_12_1 | -0.05 % | -0.24 | +0.045 |
| C | 5 | low_vol | -0.03 % | -0.39 | -0.012 |
| C | 5 | trend_200 | -0.04 % | -0.41 | -0.005 |
| C | 5 | dip_52w | -0.01 % | -1.19 | +0.004 |
| C | 5 | rev_1w | -0.10 % | -1.41 | +0.032 |
| C | 5 | mom_1m | -0.07 % | -3.32 | +0.018 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 452 | 0.487 | 0.500 |
| 0.50–0.55 | 274 | 0.514 | 0.464 |
| 0.55–0.60 | 58 | 0.568 | 0.483 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-09): oben UUP 52 % (+1.0), DBC 52 % (-0.6), EWJ 55 % (-0.7), QQQ 57 % (-0.9), USO 50 % (-1.1) · unten LQD 49 % (-6.6), GLD 47 % (-7.1), HYG 50 % (-8.1)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-09): oben UUP 53 % (+0.5), QQQ 65 % (+0.4), SPY 67 % (-0.3), EWJ 58 % (-1.3), DBC 53 % (-1.8) · unten IEF 52 % (-5.1), SLV 46 % (-5.3), HYG 58 % (-5.8)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-09): oben SMH 55 % (+5.4), EWY 55 % (+4.7), EWT 54 % (+3.9), XBI 53 % (+3.0), EWN 52 % (+2.2) · unten XLU 46 % (-3.5), XLRE 46 % (-3.8), XLF 45 % (-4.8)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-09): oben XBI 52 % (+2.3), EWZ 52 % (+2.1), EWY 52 % (+1.7), XLE 51 % (+0.9), SMH 51 % (+0.8) · unten XLC 48 % (-2.4), EWG 47 % (-2.7), INDA 47 % (-2.8)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-09): oben INTC 53 % (+3.3), AMD 53 % (+3.3), ASML 53 % (+3.0), TXN 52 % (+2.4), CAT 52 % (+2.4) · unten MA 47 % (-3.0), NVO 47 % (-3.1), NFLX 47 % (-3.4)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-09): oben MRK 52 % (+1.8), INTC 51 % (+1.1), GOOGL 51 % (+1.0), CAT 51 % (+0.9), WMT 51 % (+0.8) · unten PEP 48 % (-2.2), LIN 47 % (-2.6), HD 47 % (-2.6)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 144): mom_12_1 +0.032, mom_1m +0.054, trend_200 -0.013, dip_52w -0.044, low_vol -0.003, rsi2_oversold +0.033, vix_level +0.043, turn_of_month -0.002
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 272): mom_12_1 +0.067, mom_1m +0.032, rev_1w +0.053, trend_200 -0.014, dip_52w +0.018, low_vol -0.031, rsi2_oversold -0.022
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 368): mom_12_1 +0.045, mom_1m +0.018, rev_1w +0.032, trend_200 -0.005, dip_52w +0.004, low_vol -0.012, rsi2_oversold +0.003
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 8 | 2.49 | zu früh |
| B | 5 | 8 | 1.01 | zu früh |
| C | 5 | 8 | -0.78 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| trend_200 | A | 5 | 8 | 3.11 | zu früh |
| dip_52w | A | 5 | 8 | 2.83 | zu früh |
| mom_12_1 | A | 5 | 8 | 2.63 | zu früh |
| turn_of_month | A | 5 | 8 | 2.41 | zu früh |
| mom_1m | A | 5 | 8 | 2.2 | zu früh |
| low_vol | A | 5 | 8 | 1.92 | zu früh |
| vix_level | A | 5 | 8 | 1.74 | zu früh |
| rsi2_oversold | C | 5 | 8 | 1.45 | zu früh |
| mom_12_1 | B | 5 | 8 | 0.82 | zu früh |
| low_vol | B | 5 | 8 | 0.57 | zu früh |
| rev_1w | B | 5 | 8 | -0.22 | zu früh |
| mom_12_1 | C | 5 | 8 | -0.24 | zu früh |
| trend_200 | B | 5 | 8 | -0.34 | zu früh |
| low_vol | C | 5 | 8 | -0.39 | zu früh |
| trend_200 | C | 5 | 8 | -0.41 | zu früh |
| dip_52w | C | 5 | 8 | -1.19 | zu früh |
| rsi2_oversold | B | 5 | 8 | -1.29 | zu früh |
| rev_1w | C | 5 | 8 | -1.41 | zu früh |
| rsi2_oversold | A | 5 | 8 | -1.53 | zu früh |
| mom_1m | C | 5 | 8 | -3.32 | zu früh |
| dip_52w | B | 5 | 8 | -3.87 | zu früh |
| mom_1m | B | 5 | 8 | -5.06 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

