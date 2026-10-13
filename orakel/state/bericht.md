# Orakel – Stand 2026-10-12

Journal: 111 Eintraege, Hash-Kette OK, Kopf `34ce55218e29dcf9`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|
| A Markt | 5 | 9 | 161 | +0.29 % | 0.87 | -10.1 % | -12.8 % | +2.7 % | 0.61 |
| B Sektoren/Laender | 5 | 9 | 306 | +0.17 % | 0.31 | +18.6 % | -16.6 % | +35.2 % | 0.80 |
| C Einzeltitel | 5 | 9 | 414 | -0.26 % | -0.91 | -35.6 % | +14.3 % | -49.9 % | -1.19 |

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|
| A | 5 | turn_of_month | +0.14 % | 1.66 | -0.003 |
| A | 5 | mom_12_1 | +0.51 % | 1.62 | +0.035 |
| A | 5 | trend_200 | +0.56 % | 1.39 | -0.014 |
| A | 5 | dip_52w | +0.62 % | 1.24 | -0.037 |
| A | 5 | vix_level | +0.30 % | 1.20 | +0.040 |
| A | 5 | low_vol | +0.09 % | 0.97 | -0.001 |
| A | 5 | mom_1m | +0.21 % | 0.90 | +0.056 |
| A | 5 | rsi2_oversold | -0.38 % | -1.38 | +0.040 |
| B | 5 | mom_12_1 | +0.11 % | 0.31 | +0.065 |
| B | 5 | low_vol | -0.02 % | -0.14 | -0.026 |
| B | 5 | rev_1w | -0.02 % | -0.14 | +0.055 |
| B | 5 | trend_200 | -0.10 % | -0.66 | -0.017 |
| B | 5 | rsi2_oversold | -0.05 % | -1.56 | -0.026 |
| B | 5 | dip_52w | -0.01 % | -2.37 | +0.017 |
| B | 5 | mom_1m | -0.13 % | -5.99 | +0.029 |
| C | 5 | rsi2_oversold | +0.08 % | 1.65 | -0.000 |
| C | 5 | rev_1w | +0.02 % | 0.11 | +0.040 |
| C | 5 | mom_12_1 | -0.11 % | -0.48 | +0.040 |
| C | 5 | trend_200 | -0.06 % | -0.57 | -0.004 |
| C | 5 | low_vol | -0.08 % | -0.74 | -0.010 |
| C | 5 | dip_52w | -0.01 % | -1.62 | -0.002 |
| C | 5 | mom_1m | -0.06 % | -2.98 | +0.014 |

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|
| 0.45–0.50 | 508 | 0.487 | 0.514 |
| 0.50–0.55 | 314 | 0.514 | 0.452 |
| 0.55–0.60 | 59 | 0.568 | 0.475 |

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-10-12): oben UUP 52 % (+0.5), DBC 52 % (-0.0), EWJ 55 % (-0.5), USO 51 % (-0.6), SPY 57 % (-1.7) · unten GLD 48 % (-5.9), LQD 50 % (-6.4), HYG 50 % (-7.6)
- **A Markt, 20 Tage** (P steigt, ab 2026-10-12): oben UUP 53 % (+1.0), SPY 66 % (-0.6), DBC 54 % (-0.9), USO 51 % (-1.8), EWJ 57 % (-2.3) · unten IWM 56 % (-5.2), SLV 46 % (-5.3), HYG 58 % (-5.6)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-10-12): oben SMH 55 % (+4.9), EWT 54 % (+4.0), EWY 54 % (+3.7), XBI 53 % (+3.1), XLK 52 % (+2.1) · unten EWG 47 % (-3.1), XLRE 46 % (-4.2), XLF 45 % (-4.7)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-10-12): oben EWZ 52 % (+2.0), XLE 52 % (+1.9), EWY 52 % (+1.8), XBI 51 % (+1.5), EWW 51 % (+1.3) · unten EWL 47 % (-2.8), EWG 47 % (-2.8), EWQ 47 % (-3.0)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-10-12): oben AMD 53 % (+3.4), INTC 53 % (+2.8), ASML 53 % (+2.7), TSM 52 % (+2.2), TXN 52 % (+2.1) · unten HD 47 % (-2.7), NKE 47 % (-3.2), NFLX 46 % (-3.5)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-10-12): oben INTC 51 % (+1.2), GOOGL 51 % (+1.1), CRM 51 % (+1.0), CAT 51 % (+1.0), WMT 51 % (+0.9) · unten MCD 48 % (-2.1), PEP 48 % (-2.3), HD 47 % (-2.6)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 161): mom_12_1 +0.035, mom_1m +0.056, trend_200 -0.014, dip_52w -0.037, low_vol -0.001, rsi2_oversold +0.040, vix_level +0.040, turn_of_month -0.003
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 306): mom_12_1 +0.065, mom_1m +0.029, rev_1w +0.055, trend_200 -0.017, dip_52w +0.017, low_vol -0.026, rsi2_oversold -0.026
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 414): mom_12_1 +0.040, mom_1m +0.014, rev_1w +0.040, trend_200 -0.004, dip_52w -0.002, low_vol -0.010, rsi2_oversold -0.000
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049

<!-- pruefung -->

## Prüfung: Mehrfachtest-Hürde

Bisher registrierte Hypothesen: **9** (ausgemustert: keine), gewertete Kombinationen Hypothese × Aufgabe × Horizont: **44**.
Hürde für „bestätigt": Hypothese t ≥ **5.08**, Gesamtmodell je Aufgabe t ≥ **3.99** (Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab 60 aufgelösten Prognosetagen.

| Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|
| A | 5 | 9 | 0.87 | zu früh |
| B | 5 | 9 | 0.31 | zu früh |
| C | 5 | 9 | -0.91 | zu früh |

| Hypothese | Aufgabe | h | Tage | t | Urteil |
|---|---|---|---|---|---|
| turn_of_month | A | 5 | 9 | 1.66 | zu früh |
| rsi2_oversold | C | 5 | 9 | 1.65 | zu früh |
| mom_12_1 | A | 5 | 9 | 1.62 | zu früh |
| trend_200 | A | 5 | 9 | 1.39 | zu früh |
| dip_52w | A | 5 | 9 | 1.24 | zu früh |
| vix_level | A | 5 | 9 | 1.2 | zu früh |
| low_vol | A | 5 | 9 | 0.97 | zu früh |
| mom_1m | A | 5 | 9 | 0.9 | zu früh |
| mom_12_1 | B | 5 | 9 | 0.31 | zu früh |
| rev_1w | C | 5 | 9 | 0.11 | zu früh |
| low_vol | B | 5 | 9 | -0.14 | zu früh |
| rev_1w | B | 5 | 9 | -0.14 | zu früh |
| mom_12_1 | C | 5 | 9 | -0.48 | zu früh |
| trend_200 | C | 5 | 9 | -0.57 | zu früh |
| trend_200 | B | 5 | 9 | -0.66 | zu früh |
| low_vol | C | 5 | 9 | -0.74 | zu früh |
| rsi2_oversold | A | 5 | 9 | -1.38 | zu früh |
| rsi2_oversold | B | 5 | 9 | -1.56 | zu früh |
| dip_52w | C | 5 | 9 | -1.62 | zu früh |
| dip_52w | B | 5 | 9 | -2.37 | zu früh |
| mom_1m | C | 5 | 9 | -2.98 | zu früh |
| mom_1m | B | 5 | 9 | -5.99 | zu früh |

## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)

Ampel **grau**: zu wenig Daten (0/60 aufgelöste Prognosetage)
Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte 120 aufgelöste Prognosetage, t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.

