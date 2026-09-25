# Signal Radar — Insider-Cluster

Läuft komplett automatisch in der Cloud. **Kein Terminal.** Einrichtung nur per Klick im Browser (~5 Minuten).

## Einrichtung (einmalig)

1. **Repo anlegen** — auf github.com oben rechts „+" → *New repository*. Name z. B. `signal-radar`, **Public** (nötig für kostenloses Pages), *Create repository*.
2. **Dateien hochladen** — im neuen Repo *Add file* → *Upload files*. Diesen ganzen Ordner reinziehen (inkl. des versteckten Ordners `.github`). Unten *Commit changes*.
   - Falls der Browser `.github` nicht mitnimmt: *Add file* → *Create new file*, als Dateiname `.github/workflows/signal-radar.yml` eintippen und den Inhalt aus dieser Datei hineinkopieren.
3. **Kontakt für EDGAR hinterlegen** — *Settings* → *Secrets and variables* → *Actions* → Reiter **Variables** → *New repository variable*.
   Name: `EDGAR_UA` — Wert: `Signal Radar <deine-echte-email>`. (Die SEC verlangt das; ohne Kontakt blockt sie.)
4. **Pages einschalten** — *Settings* → *Pages* → Source: **Deploy from a branch** → Branch **main**, Ordner **/ (root)** → *Save*.
   Nach ~1 Minute steht oben die URL deiner Seite (z. B. `https://<dein-name>.github.io/signal-radar/`).
5. **Ersten Lauf starten** — Reiter *Actions* → links „Signal Radar" → rechts *Run workflow* → *Run workflow*.
   Nach ein paar Minuten liegt eine frische `radar_data.json` im Repo und die Seite zeigt sie an.

Ab dann läuft der Screener **jede Nacht automatisch** (04:30 UTC, Di–Sa = nach jedem US-Handelstag) und aktualisiert die Seite von selbst.

## Dateien

- `index.html` — das Dashboard (deine Seite). Lädt `radar_data.json` automatisch; „JSON laden…" nur als Fallback.
- `insider_screener.py` — holt Form-4-Filings von SEC EDGAR, filtert offene Insiderkäufe, schreibt `radar_data.json`.
- `.github/workflows/signal-radar.yml` — der nächtliche Zeitplan.
- `radar_data.json` — das aktuelle Ergebnis (wird vom Bot überschrieben).

## Ehrlich zur Einordnung

„Stärke" ist eine **Sortierhilfe**, kein validiertes Signal. Ein Treffer ist ein **Kandidat**, keine Kaufentscheidung.
Nächster sinnvoller Schritt: Backtest — Cluster-Käufe eines Zeitraums gegen die Kursentwicklung danach messen.
Keine Anlageberatung.

## Kern · „Surfen mit Risiko" (Papierbetrieb ab 01.10.2026)
`core.py` schreibt nachts `core_data.json` (Reiter **Kern**): je Index (S&P 500, Nasdaq 100) drei Linien – Halten 1×, Trendfilter (gehebelt über der 200-Tage-Linie am Monatsende), Konjunkturfilter (Ausstieg nur bei Trendbruch *und* US-Arbeitslosenquote über 12-Monats-Schnitt). Ausweich Gold/Cash. Signal nur am Monatsende, Ausführung am ersten Handelstag danach. Hebel (Konstante `LEV`) ist ein Platzhalter. Belege: Backtest-Log Tests 9, 11, v3. Kein Kapital.

## Depot · Struktur 40/10/40/10 (Papierbetrieb ab 01.10.2026)
`depot.py` schreibt nachts `depot_data.json` (Reiter **Depot**) und ergänzt `depot_log.jsonl`. Linien: **Kern 40 %** Führer-System (am Monatsende die 5 stärksten von 41 US-Branchen-ETFs nach 12-1-Momentum, max. 1 je Cluster = Korrelation der Tagesrenditen < 0,90, Konjunkturfilter mit Gold-Ausweich, Rücksetzer-Zusatz SPY +5 %/−5 %), **Gold 10 %** (GLD), **Intraday 40 %** (bis zum bestandenen 5-Jahres-Test Cash), **Lucky Punch 10 %** (TQQQ über der 10-Monats-Linie des Nasdaq 100, sonst Cash), dazu die Vergleichslinien Kern ohne Cluster-Deckel und SPY halten. Signal zum Monatsschluss, Ausführung zum Schluss des ersten Handelstags danach.
- **Festgeschrieben:** Jede Monatsentscheidung ab Papierstart steht in `depot_log.jsonl`, bevor sie ausgeführt wird, und wird nie neu berechnet. Das Protokoll wächst nur.
- **Kontrolle:** `python depot.py --rueckrechnung` rechnet ab 2002 mit genau diesem Code zurück. Gerechnet wie im Research trifft er Test 28 (2008–2026 16,4 % gegen 16,3 % p.a., max. DD −45 %).
- Kein Kapital. Belege: Tests 26, 28, 34, 36 im Projekt.

## Screen · 22 Börsen, drei Papier-Körbe (Papier ab Monatsende 30.09.2026)
`screen.py` rechnet nach jedem Monatsende den Checklisten-Screen aus Test 19 (Regel v2) über 22 Börsen (Aktien ab 2 Mrd. USD) und schreibt drei Körbe mit je 10 Titeln in `screen_log.jsonl` fest: **v2** (Top-Dezil je Land, Gates FCF/ROE/Nettoschulden, Cluster-, Branchen- und Sektor-Deckel, Mid Caps), **v1** (alte Regel mit Sektor-Deckel) und **pur** (Momentum-Dezil ohne Gates). Täglich prüft er die Exit-Regel (unter 200-Tage-Linie und ≥ 25 % unter dem 52-Wochen-Hoch) und bewertet die Körbe in USD gegen MSCI World und SPY → `screen_data.json`, Reiter **Screen**. `python screen.py --vorschau` rechnet den Screen zum letzten Handelstag, ohne etwas festzuschreiben. Kein Kapital.

## Carry · Cash-and-Carry-Ampel BTC/ETH (Papier ab 01.10.2026)
`funding.py` liest die Funding Rates der Perpetuals bei Deribit und schaltet je Instrument über die 200-Tage-Linie (Test 15): Ampel, Funding der letzten 7/30/365 Tage, Papier-Ergebnis auf Nominal und Kapital (30 % Puffer), Kapitalrechner → `funding_data.json`, Reiter **Carry**; Ampelwechsel in `funding_log.jsonl`. Liquidations- und Börsenrisiko sind nicht eingerechnet. Kein Kapital.

## Orakel · Prognose-Agent, der nur vorwärts lernt (seit 24.09.2026)
`orakel/orakel.py` läuft im Nachtlauf nach `core.py` und schreibt `orakel_data.json` (Reiter **Orakel**). Jede Nacht gibt er Wahrscheinlichkeiten ab: **A Markt** (18 ETFs: steigt das Instrument über 5/20 Handelstage?), **B Sektoren/Länder** (34 ETFs) und **C Einzeltitel** (46 Großwerte): schlägt der Titel den Median seiner Gruppe? Einstieg jeweils nächste Eröffnung.
- **Fälschungssicher:** `orakel/state/journal.jsonl` ist eine Hash-Kette (jede Zeile enthält den Hash der vorigen). Der Git-Commit um 04:30 UTC belegt, dass die Prognose vor der US-Eröffnung stand. `python orakel/orakel.py verify` prüft die Kette.
- **Lernen:** Nach jeder Auflösung werden die Gewichte neu geschätzt. Vorwissen aus 2006–2026 ist in `orakel/state/prior.json` eingefroren und zählt wie ein halbes Jahr Vorwärtsdaten (Laplace-Näherung). Danach entscheidet nur noch die Zukunft; ältere Vorwärtsdaten verlieren mit Halbwertszeit 1 Jahr an Gewicht.
- **Theorie:** Hypothesen stehen mit Mechanismus in `orakel/experts.py`. Neue Hypothesen bekommen **kein** Vorwissen aus der Historie, weil sie mit Kenntnis der Vergangenheit entstanden sind. Bestehende werden nie geändert, nur ausgemustert.
- **Maßstab:** Log-Loss gegen die Klimatologie (Basisrate), t-Werte nach Newey-West. Frühestens nach ~3 Monaten aussagekräftig. Kein Kapital.
