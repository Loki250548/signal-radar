# Orakel – Stand 2026-09-23

Journal: 6 Eintraege, Hash-Kette OK, Kopf `a945a06e19d87d80`, Modell `885755fa119e`

## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)

Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).

| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |
|---|---|---|---|---|---|---|---|---|---|

## Welche Theorie traegt? (Experten einzeln, vorwaerts)

| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |
|---|---|---|---|---|---|

## Kalibrierung (alle Aufgaben)

| p-Bereich | n | Ø p | Trefferquote |
|---|---|---|---|

## Aktuelle Prognosen

In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).

- **A Markt, 5 Tage** (P steigt, ab 2026-09-23): oben DBC 54 % (+2.1), IWM 56 % (+1.1), USO 52 % (+0.8), TLT 53 % (+0.2), SLV 52 % (-0.0) · unten HYG 55 % (-2.1), LQD 54 % (-2.3), FXI 50 % (-2.5)
- **A Markt, 20 Tage** (P steigt, ab 2026-09-23): oben QQQ 66 % (+0.6), USO 53 % (-0.2), UUP 51 % (-0.8), EWJ 58 % (-0.9), DBC 54 % (-1.0) · unten IWM 56 % (-5.3), SLV 46 % (-5.5), GLD 50 % (-5.7)
- **B Sektoren/Laender, 5 Tage** (P schlaegt Median, ab 2026-09-23): oben XLE 52 % (+1.7), EWP 51 % (+0.9), EWI 51 % (+0.9), EWZ 51 % (+0.8), XBI 51 % (+0.8) · unten INDA 48 % (-2.2), FXI 48 % (-2.3), ITB 47 % (-2.8)
- **B Sektoren/Laender, 20 Tage** (P schlaegt Median, ab 2026-09-23): oben EWT 53 % (+3.2), XLK 53 % (+2.7), XBI 53 % (+2.7), SMH 53 % (+2.6), EWN 52 % (+2.4) · unten EWQ 47 % (-3.0), XLU 46 % (-3.5), XLF 46 % (-4.3)
- **C Einzeltitel, 5 Tage** (P schlaegt Median, ab 2026-09-23): oben CSCO 51 % (+1.5), CAT 51 % (+1.0), LLY 51 % (+1.0), GOOGL 51 % (+0.8), MRK 51 % (+0.6) · unten TSLA 48 % (-2.2), NKE 48 % (-2.2), META 47 % (-3.4)
- **C Einzeltitel, 20 Tage** (P schlaegt Median, ab 2026-09-23): oben ASML 53 % (+3.2), CAT 53 % (+2.9), INTC 53 % (+2.9), LLY 53 % (+2.5), MRK 53 % (+2.5) · unten PG 47 % (-3.3), HD 46 % (-3.7), BRK-B 46 % (-4.2)

## Aktuelle Theorie (Gewichte des Gesamtmodells)

- A5 (Vorwaertsdaten: 0): mom_12_1 +0.027, mom_1m +0.013, trend_200 +0.016, dip_52w +0.006, low_vol +0.017, rsi2_oversold +0.044, vix_level +0.019, turn_of_month +0.007
- A20 (Vorwaertsdaten: 0): mom_12_1 -0.035, mom_1m +0.030, trend_200 +0.025, dip_52w -0.042, low_vol -0.037, rsi2_oversold -0.002, vix_level +0.036, turn_of_month -0.021
- B5 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m +0.007, rev_1w +0.043, trend_200 +0.011, dip_52w +0.017, low_vol -0.002, rsi2_oversold -0.014
- B20 (Vorwaertsdaten: 0): mom_12_1 +0.042, mom_1m -0.001, rev_1w +0.011, trend_200 -0.012, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.047
- C5 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m +0.007, rev_1w +0.044, trend_200 +0.012, dip_52w +0.018, low_vol -0.002, rsi2_oversold -0.015
- C20 (Vorwaertsdaten: 0): mom_12_1 +0.043, mom_1m -0.000, rev_1w +0.011, trend_200 -0.013, dip_52w +0.014, low_vol -0.038, rsi2_oversold -0.049
