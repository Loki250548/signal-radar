# Orakel – Stand 2026-10-15

Journal: 138 Eintraege, Hash-Kette OK, Kopf `7b6bb6758cd84ca5`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 12 | 215 | -0.45 % | -0.63 | -7.6 % | -7.5 % | -0.1 % | -0.01 |
| B Sektoren/Laender | 5 | 12 | 408 | -0.85 % | -0.80 | -40.0 % | -8.2 % | -31.7 % | -0.41 |
| C Einzeltitel | 5 | 12 | 552 | -0.76 % | -1.55 | -75.1 % | +21.1 % | -96.3 % | -1.66 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | mom_12_1 | +0.37 % | 1.15 | +0.042 |
| A | 5 | turn_of_month | +0.07 % | 0.68 | -0.006 |
| A | 5 | vix_level | +0.15 % | 0.55 | +0.034 |
| A | 5 | dip_52w | +0.23 % | 0.38 | -0.031 |
| A | 5 | trend_200 | +0.18 % | 0.32 | -0.023 |
| A | 5 | low_vol | +0.02 % | 0.18 | +0.001 |
| A | 5 | mom_1m | -0.15 % | -0.40 | +0.042 |
| A | 5 | rsi2_oversold | -0.36 % | -1.77 | +0.020 |
| B | 5 | dip_52w | -0.00 % | -0.15 | +0.028 |
| B | 5 | rev_1w | -0.09 % | -0.64 | +0.050 |
| B | 5 | mom_12_1 | -0.37 % | -0.68 | +0.054 |
| B | 5 | low_vol | -0.44 % | -1.09 | +0.002 |
| B | 5 | trend_200 | -0.28 % | -1.26 | -0.024 |
| B | 5 | rsi2_oversold | -0.07 % | -2.32 | -0.040 |
| B | 5 | mom_1m | -0.15 % | -7.14 | +0.022 |
| C | 5 | rev_1w | +0.01 % | 0.11 | +0.046 |
| C | 5 | rsi2_oversold | -0.01 % | -0.18 | -0.018 |
| C | 5 | mom_12_1 | -0.40 % | -1.20 | +0.019 |
| C | 5 | trend_200 | -0.16 % | -1.20 | -0.002 |
| C | 5 | low_vol | -0.21 % | -1.33 | +0.004 |
| C | 5 | dip_52w | -0.01 % | -1.79 | -0.008 |
| C | 5 | mom_1m | -0.08 % | -5.88 | -0.002 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 682 | 0.486 | 0.554 |
| 0.50–0.55 | 427 | 0.515 | 0.410 |
| 0.55–0.60 | 66 | 0.567 | 0.439 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-15): oben DBC 55 % (+2.2), USO 53 % (+1.6), UUP 52 % (+1.0), EWJ 55 % (+0.1), QQQ 57 % (-0.7) · unten LQD 52 % (-4.3), GLD 50 % (-4.6), HYG 52 % (-5.3)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-15): oben UUP 52 % (+0.1), USO 52 % (-0.4), SPY 66 % (-0.5), DBC 54 % (-0.8), QQQ 64 % (-0.9) · unten IWM 56 % (-4.7), SLV 46 % (-5.1), HYG 58 % (-5.3)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-15): oben EWY 53 % (+3.0), SMH 52 % (+2.5), XBI 51 % (+1.1), KRE 51 % (+1.1), EWT 51 % (+0.8) · unten XLRE 48 % (-2.2), XLP 48 % (-2.3), XLF 48 % (-2.4)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-15): oben EWY 52 % (+2.2), XBI 52 % (+1.8), EWW 51 % (+1.0), SMH 51 % (+1.0), ITB 51 % (+0.8) · unten XLRE 48 % (-2.4), XLF 47 % (-2.8), XLU 47 % (-3.2)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-15): oben AMD 51 % (+1.2), INTC 51 % (+1.2), ASML 51 % (+1.1), TSM 51 % (+1.0), JNJ 51 % (+0.9) · unten CRM 48 % (-2.3), ADBE 48 % (-2.3), NKE 47 % (-2.5)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-15): oben INTC 52 % (+1.9), QCOM 51 % (+1.2), AMD 51 % (+1.2), ASML 51 % (+1.2), MRK 50 % (+0.5) · unten BRK-B 48 % (-2.4), V 47 % (-2.5), COST 47 % (-2.9)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 215): mom_12_1 +0.042, mom_1m +0.042, trend_200 -0.023, dip_52w -0.031, low_vol +0.001, rsi2_oversold +0.020, vix_level +0.034, turn_of_month -0.006
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 408): mom_12_1 +0.054, mom_1m +0.022, rev_1w +0.050, trend_200 -0.024, dip_52w +0.028, low_vol +0.002, rsi2_oversold -0.040
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 552): mom_12_1 +0.019, mom_1m -0.002, rev_1w +0.046, trend_200 -0.002, dip_52w -0.008, low_vol +0.004, rsi2_oversold -0.018
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 12 | -0.63 | zu früh |
| B | 5 | 12 | -0.8 | zu früh |
| C | 5 | 12 | -1.55 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| mom_12_1 | A | 5 | 12 | 1.15 | zu früh |
| turn_of_month | A | 5 | 12 | 0.68 | zu früh |
| vix_level | A | 5 | 12 | 0.55 | zu früh |
| dip_52w | A | 5 | 12 | 0.38 | zu früh |
| trend_200 | A | 5 | 12 | 0.32 | zu früh |
| low_vol | A | 5 | 12 | 0.18 | zu früh |
| rev_1w | C | 5 | 12 | 0.11 | zu früh |
| dip_52w | B | 5 | 12 | -0.15 | zu früh |
| rsi2_oversold | C | 5 | 12 | -0.18 | zu früh |
| mom_1m | A | 5 | 12 | -0.4 | zu früh |
| rev_1w | B | 5 | 12 | -0.64 | zu früh |
| mom_12_1 | B | 5 | 12 | -0.68 | zu früh |
| low_vol | B | 5 | 12 | -1.09 | zu früh |
| mom_12_1 | C | 5 | 12 | -1.2 | zu früh |
| trend_200 | C | 5 | 12 | -1.2 | zu früh |
| trend_200 | B | 5 | 12 | -1.26 | zu früh |
| low_vol | C | 5 | 12 | -1.33 | zu früh |
| rsi2_oversold | A | 5 | 12 | -1.77 | zu früh |
| dip_52w | C | 5 | 12 | -1.79 | zu früh |
| rsi2_oversold | B | 5 | 12 | -2.32 | zu früh |
| mom_1m | C | 5 | 12 | -5.88 | zu früh |
| mom_1m | B | 5 | 12 | -7.14 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

