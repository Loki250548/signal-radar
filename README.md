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
