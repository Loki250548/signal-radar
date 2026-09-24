"""Orakel – Konfiguration. Aenderungen hier werden im Journal ueber den Modell-Hash sichtbar."""

# Aufgaben: A = Markt-Timing (steigt das Instrument?), B = Quer (schlaegt der Titel den Median seines Universums?)
TASKS = {
    "A": {
        "name": "Markt",
        "style": "ts",  # Zeitreihe: Signal je Instrument gegen die eigene Historie normiert
        "tickers": ["SPY", "QQQ", "IWM", "DIA", "EFA", "EEM", "EWG", "EWJ", "FXI",
                    "GLD", "SLV", "TLT", "IEF", "LQD", "HYG", "USO", "DBC", "UUP"],
        "prior": True,
    },
    "B": {
        "name": "Sektoren/Laender",
        "style": "xs",  # Querschnitt: Signal je Tag ueber das Universum rang-normiert
        "tickers": ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC",
                    "SMH", "XBI", "KRE", "ITB",
                    "EWJ", "EWU", "EWG", "EWQ", "EWI", "EWP", "EWL", "EWN", "EWD", "EWA",
                    "EWC", "EWZ", "EWW", "EWY", "EWT", "EWH", "INDA", "FXI", "EWS"],
        "prior": True,
    },
    "C": {
        "name": "Einzeltitel",
        "style": "xs",
        "tickers": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "BRK-B", "JPM",
                    "V", "MA", "LLY", "UNH", "XOM", "JNJ", "PG", "HD", "COST", "ABBV",
                    "MRK", "KO", "PEP", "WMT", "BAC", "ORCL", "CRM", "AMD", "NFLX", "ADBE",
                    "QCOM", "TXN", "INTC", "CSCO", "CAT", "GE", "LIN", "TMO", "DIS", "MCD",
                    "NKE", "PLTR", "ASML", "SAP", "NVO", "TSM"],
        # Kein Prior aus der Einzeltitel-Historie (heutige Grosswerte = Survivorship).
        # C lernt vom Prior der Aufgabe B plus eigenen Vorwaertsdaten.
        "prior": False,
        "prior_from": "B",
    },
}
MARKET_FEATURE_TICKERS = ["^VIX"]

HORIZONS = [5, 20]              # Handelstage; Einstieg naechste Eroeffnung, Ausstieg Schluss Tag t+h
DATA_START = "2003-01-01"
PRIOR_START = "2006-01-01"      # Historie fuer den Prior
PRIOR_DAYS = 126                # Gewicht des Priors = so viele Vorwaerts-Handelstage (halbes Jahr)
FORWARD_HALFLIFE_DAYS = 365     # aeltere Vorwaertsdaten verlieren langsam Gewicht
RIDGE = 50.0                    # Schrumpfung Richtung "kein Effekt"
CLIP = 3.0
CONVICTION = 0.02               # Papierportfolio A: long, wenn p >= Klimatologie + 2 Punkte
