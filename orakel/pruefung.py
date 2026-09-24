#!/usr/bin/env python3
"""Pruefung des Orakels (laeuft nach `orakel.py run`, aendert keine Prognose).

Bewusst NICHT Teil des Modell-Hashes (config.py, experts.py, orakel.py): reine Auswertung, keine Prognoselogik.

1. Mehrfachtest-Huerde: Jede Hypothese wird in mehreren Aufgaben und Horizonten gewertet. Je mehr Kombinationen
   jemals getestet wurden, desto hoeher die t-Schwelle fuer ein Urteil "bestaetigt". Gezaehlt werden alle je
   registrierten Experten (ausgemusterte bleiben im Register) und alle Kombinationen Experte x Aufgabe x Horizont.
   Schwelle wie im Perlen-Protokoll (research/harness.py): t >= max(3,0; 3,0 + 0,55 * ln(Versuche)).
2. Fruehwarnung Kern: Aufgabe B (Rangfolge Sektoren/Laender) misst vorwaerts denselben Mechanismus wie das
   Fuehrer-System (Branchen-Momentum). Ampel aus dem Papier-Vorsprung "oberstes Fuenftel minus Durchschnitt"
   bei B20 ueber die letzten 120 aufgeloesten Prognosetage.

Schreibt einen Abschnitt an orakel/state/bericht.md und ergaenzt orakel_data.json um den Schluessel "pruefung".
Aufruf: python3 orakel/pruefung.py
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import orakel as O  # noqa: E402

E, C = O.E, O.C
MIN_DAYS = 60          # ab so vielen aufgeloesten Prognosetagen wird geurteilt
WARN_WINDOW = 120      # Fenster der Fruehwarnung (aufgeloeste Prognosetage)
WARN_T = -1.5          # rot, wenn der Vorsprung im Fenster mit t <= -1,5 negativ ist
MARK = "<!-- pruefung -->"


def t_req(trials):
    return round(max(3.0, 3.0 + 0.55 * math.log(max(1, trials))), 2)


def trial_count(J):
    """Alle je registrierten Experten und alle Kombinationen Experte x Aufgabe x Horizont (Register + Journal)."""
    combos = set()
    for e in E.REGISTRY:
        for task, cfg in C.TASKS.items():
            if cfg["style"] in e["styles"]:
                for h in C.HORIZONS:
                    combos.add((e["name"], task, h))
    for F in J.forecasts():
        for n in F["experts"]:
            combos.add((n, F["task"], F["h"]))
    names = {e["name"] for e in E.REGISTRY} | {c[0] for c in combos}
    retired = sorted(e["name"] for e in E.REGISTRY if e.get("retired"))
    return len(names), len(combos), retired


def verdict(days, t, need):
    if days < MIN_DAYS:
        return "zu früh"
    if t is None or np.isnan(t):
        return "–"
    if t >= need:
        return "bestätigt"
    if t >= 2:
        return "Hinweis positiv"
    if t <= -2:
        return "Hinweis negativ"
    return "neutral"


def early_warning(res):
    key = ("B", 20)
    S = res.get(key)
    n = len(S["dates"]) if S else 0
    out = dict(task="B20", days=n, window=WARN_WINDOW, min_days=MIN_DAYS)
    if n < MIN_DAYS:
        out.update(status="grau", text=f"zu wenig Daten ({n}/{MIN_DAYS} aufgelöste Prognosetage)")
        return out
    port = np.array(S["port"])
    diff = (port[:, 0] - port[:, 1])[-WARN_WINDOW:]
    m, t = O.nw_t(diff, 20)
    ann = float(m * 252 / 20)
    out.update(diff_ann=ann, t=float(t))
    if t <= WARN_T:
        out.update(status="rot", text=f"Branchen-Momentum versagt vorwärts ({ann*100:+.1f} % p.a., t {t:.1f}). "
                                      "Führer-Kern prüfen, vierteljährliche Prüfung vorziehen.")
    elif m <= 0:
        out.update(status="gelb", text=f"Branchen-Momentum vorwärts ohne Vorsprung ({ann*100:+.1f} % p.a., t {t:.1f}). Beobachten.")
    else:
        out.update(status="grün", text=f"Branchen-Momentum trägt vorwärts ({ann*100:+.1f} % p.a., t {t:.1f}).")
    return out


def analyse(J):
    res = O.score(J)
    n_exp, n_tests, retired = trial_count(J)
    need_exp = t_req(n_tests)
    n_task = len(C.TASKS) * len(C.HORIZONS)
    need_task = t_req(n_task)
    tasks, experts = [], []
    for (task, h), S in sorted(res.items()):
        if not S["dates"]:
            continue
        m, t = O.nw_t(S["d_ens"], h)
        days = len(S["dates"])
        tasks.append(dict(task=task, h=h, days=days, t=None if np.isnan(t) else float(t),
                          verdict=verdict(days, t, need_task)))
        for name, dd in S["d_exp"].items():
            ser = [dd[d] for d in S["dates"] if d in dd]
            mm, tt = O.nw_t(ser, h)
            experts.append(dict(task=task, h=h, name=name, days=len(ser), t=None if np.isnan(tt) else float(tt),
                                verdict=verdict(len(ser), tt, need_exp)))
    return dict(n_experts=n_exp, n_tests=n_tests, retired=retired, t_req_expert=need_exp,
                n_task_tests=n_task, t_req_task=need_task, min_days=MIN_DAYS,
                tasks=tasks, experts=experts, early_warning=early_warning(res))


def markdown(P):
    L = [MARK, "", "## Prüfung: Mehrfachtest-Hürde", "",
         f"Bisher registrierte Hypothesen: **{P['n_experts']}** (ausgemustert: {', '.join(P['retired']) or 'keine'}), "
         f"gewertete Kombinationen Hypothese × Aufgabe × Horizont: **{P['n_tests']}**.",
         f"Hürde für „bestätigt\": Hypothese t ≥ **{P['t_req_expert']:.2f}**, Gesamtmodell je Aufgabe t ≥ **{P['t_req_task']:.2f}** "
         f"(Perlen-Protokoll: 3,0 + 0,55 · ln(Versuche)). Geurteilt wird erst ab {P['min_days']} aufgelösten Prognosetagen.", ""]
    if P["tasks"]:
        L += ["| Aufgabe | h | Tage | t | Urteil |", "|---|---|---|---|---|"]
        L += [f"| {x['task']} | {x['h']} | {x['days']} | {x['t'] if x['t'] is None else round(x['t'], 2)} | {x['verdict']} |" for x in P["tasks"]]
        L += ["", "| Hypothese | Aufgabe | h | Tage | t | Urteil |", "|---|---|---|---|---|---|"]
        for x in sorted(P["experts"], key=lambda x: -(x["t"] if x["t"] is not None else -99)):
            L.append(f"| {x['name']} | {x['task']} | {x['h']} | {x['days']} | {x['t'] if x['t'] is None else round(x['t'], 2)} | {x['verdict']} |")
    else:
        L += ["Noch nichts aufgelöst."]
    W = P["early_warning"]
    L += ["", "## Frühwarnung Kern (Branchen-Momentum, Aufgabe B20)", "",
          f"Ampel **{W['status']}**: {W['text']}",
          f"Messung: Papier-Vorsprung oberstes Fünftel minus Durchschnitt, letzte {W['window']} aufgelöste Prognosetage, "
          "t nach Newey-West. Rot bei t ≤ −1,5, gelb bei Vorsprung ≤ 0.", ""]
    return "\n".join(L) + "\n"


def main():
    J = O.Journal(O.JOURNAL)
    P = analyse(J)
    path_md = os.path.join(O.STATE, "bericht.md")
    base = open(path_md).read().split(MARK)[0].rstrip() + "\n\n" if os.path.exists(path_md) else ""
    with open(path_md, "w") as f:
        f.write(base + markdown(P))
    path_json = os.path.join(os.path.dirname(HERE), "orakel_data.json")
    if os.path.exists(path_json):
        with open(path_json) as f:
            data = json.load(f)
        data["pruefung"] = P
        with open(path_json, "w") as f:
            json.dump(data, f, indent=1, default=float)
    W = P["early_warning"]
    print(f"Pruefung: {P['n_experts']} Hypothesen, {P['n_tests']} Tests, Huerde t >= {P['t_req_expert']}, "
          f"Fruehwarnung Kern: {W['status']}")


if __name__ == "__main__":
    main()
