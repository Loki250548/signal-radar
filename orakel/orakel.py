#!/usr/bin/env python3
"""Orakel – ein Prognose-Agent, der nur vorwaerts lernt.

Jeden Handelstag nach US-Schluss:
  1. offene Prognosen aufloesen, deren Horizont abgelaufen ist
  2. Modelle neu schaetzen: eingefrorener Prior aus der Historie (bis START) + aufgeloeste Vorwaertsprognosen
  3. neue Wahrscheinlichkeiten ausgeben und fälschungssicher ins Journal schreiben (Hash-Kette)
  4. Bericht: Wer sagt die Zukunft besser voraus als die Klimatologie? Mit t-Werten.

Befehle:
  python3 orakel.py run            taeglicher Lauf
  python3 orakel.py verify         Hash-Kette pruefen
  python3 orakel.py report         nur Bericht neu schreiben
  python3 orakel.py simulate 2025-01-02   Probelauf auf der Vergangenheit (zaehlt NICHT, nur Technikpruefung)
"""
import hashlib
import json
import os
import pickle
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import config as C  # noqa: E402
import experts as E  # noqa: E402

STATE = os.path.join(HERE, "state")
JOURNAL = os.path.join(STATE, "journal.jsonl")
os.makedirs(STATE, exist_ok=True)


# ---------------------------------------------------------------- Daten
def all_tickers():
    s = []
    for t in C.TASKS.values():
        s += t["tickers"]
    return sorted(set(s)) + C.MARKET_FEATURE_TICKERS


def load_data(offline=False):
    cache = os.path.join(STATE, "data.pkl")
    raw = None
    if not offline:
        try:
            import yfinance as yf
            raw = yf.download(all_tickers(), start=C.DATA_START, auto_adjust=True,
                              progress=False, threads=True)
            if raw is None or raw.empty:
                raw = None
            else:
                with open(cache, "wb") as f:
                    pickle.dump(raw, f)
        except Exception as ex:  # Netzfehler -> Cache
            print("WARNUNG Download:", ex)
    if raw is None:
        with open(cache, "rb") as f:
            raw = pickle.load(f)
    close = raw["Close"].copy()
    opn = raw["Open"].copy()
    spy = close["SPY"].dropna()
    idx = spy.index
    # unvollstaendigen Tagesbalken verwerfen (Lauf waehrend der Handelszeit)
    ny = pd.Timestamp.now(tz="America/New_York")
    if idx[-1].date() == ny.date() and (ny.hour, ny.minute) < (16, 20):
        idx = idx[:-1]
    close = close.reindex(idx)
    opn = opn.reindex(idx)
    vix = close["^VIX"].ffill()
    fut = pd.bdate_range(idx[-1] + pd.Timedelta(days=1), periods=40)
    cal = idx.append(fut)
    return dict(close=close, open=opn, vix=vix, cal=cal)


# ---------------------------------------------------------------- Merkmale und Ziele
def normalize(raw, style, name):
    if style == "ts":
        if name == "vix_level":
            z = raw
        elif name == "turn_of_month":
            z = (raw - 0.2) / 0.2
        else:
            m = raw.rolling(756, min_periods=252).mean()
            s = raw.rolling(756, min_periods=252).std()
            z = (raw - m) / s
    else:
        pct = raw.rank(axis=1, pct=True)
        n = raw.notna().sum(axis=1)
        pct = pct.sub(0.5 / n, axis=0)  # zentrieren
        z = (pct - 0.5) * np.sqrt(12)
        z[n < 6] = np.nan
    return z.clip(-C.CLIP, C.CLIP)


class Panel:
    """Merkmale, Ziele, Klimatologie fuer eine Aufgabe und einen Horizont."""

    def __init__(self, D, task, h):
        self.task, self.h = task, h
        cfg = C.TASKS[task]
        self.style = cfg["style"]
        tk = [t for t in cfg["tickers"] if t in D["close"].columns]
        self.tickers = tk
        sub = dict(close=D["close"][tk], open=D["open"][tk], vix=D["vix"], cal=D["cal"])
        self.dates = D["close"].index
        self.experts = [e["name"] for e in E.REGISTRY if self.style in e["styles"]]
        self.F = {}
        for e in E.REGISTRY:
            if self.style in e["styles"]:
                self.F[e["name"]] = normalize(e["fn"](sub, h), self.style, e["name"])
        c, o = sub["close"], sub["open"]
        self.r = c.shift(-h) / o.shift(-1) - 1
        if self.style == "ts":
            y = (self.r > 0).astype(float).where(self.r.notna())
            clim = y.shift(h).expanding(min_periods=250).mean().fillna(0.53).clip(0.3, 0.7)
        else:
            med = self.r.median(axis=1)
            y = self.r.gt(med, axis=0).astype(float).where(self.r.notna())
            clim = pd.DataFrame(0.5, index=y.index, columns=y.columns)
        self.y, self.clim = y, clim
        self.valid_close = c.notna().values
        self.pos = {d: i for i, d in enumerate(self.dates)}
        self.Fa = {n: f.reindex(index=self.dates, columns=tk).values for n, f in self.F.items()}
        self.clim_a = clim.values
        self.y_a = y.values

    def rows_at(self, date, names):
        """Merkmalsvektoren fuer alle Ticker an einem Tag (NaN -> 0 = neutral)."""
        i = self.pos[date] if not isinstance(date, (int, np.integer)) else int(date)
        X = np.column_stack([self.Fa[n][i] for n in names])
        out = {}
        for j, t in enumerate(self.tickers):
            if not self.valid_close[i, j]:
                continue
            x = X[j]
            if np.isnan(x).mean() > 0.5:
                continue
            out[t] = (np.nan_to_num(x), float(self.clim_a[i, j]))
        return out


def logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# ---------------------------------------------------------------- Modell
def fit_logit(X, y, off, w, lam, b0=None, L=None):
    """Gewichtete logistische Regression mit Offset. Strafe: 0.5*(b-b0)'L(b-b0), sonst Ridge lam."""
    n, k = X.shape
    Z = np.hstack([np.ones((n, 1)), X])
    if L is None:
        L = np.diag(np.r_[lam * 0.01, np.full(k, lam)])
        b0 = np.zeros(k + 1)
    beta = b0.copy()
    for _ in range(60):
        p = sigmoid(off + Z @ beta) if n else np.zeros(0)
        g = Z.T @ (w * (p - y)) + L @ (beta - b0)
        Hm = (Z * (w * p * (1 - p))[:, None]).T @ Z + L + np.eye(k + 1) * 1e-9
        step = np.linalg.solve(Hm, g)
        beta -= step
        if np.max(np.abs(step)) < 1e-9:
            break
    return beta


def laplace(X, y, off, w, lam):
    """Posterior-Naeherung: Mittel und Praezision (Hesse-Matrix inkl. Ridge)."""
    b = fit_logit(X, y, off, w, lam)
    Z = np.hstack([np.ones((len(y), 1)), X])
    p = sigmoid(off + Z @ b)
    H = (Z * (w * p * (1 - p))[:, None]).T @ Z + np.diag(np.r_[lam * 0.01, np.full(X.shape[1], lam)])
    return b, H


def build_prior(P, cutoff, names, n_tickers):
    """Eingefrorener Prior: Historie jede h-te Sitzung von PRIOR_START bis Ausgang < cutoff,
    gewichtet wie PRIOR_DAYS Vorwaerts-Handelstage, als Laplace-Naeherung gespeichert."""
    ci = np.searchsorted(P.dates.values, np.datetime64(pd.Timestamp(cutoff)))
    last = ci - P.h - 2
    first = np.searchsorted(P.dates.values, np.datetime64(pd.Timestamp(C.PRIOR_START)))
    col = {t: j for j, t in enumerate(P.tickers)}
    X, Y, O = [], [], []
    for i in range(first, max(first, last), P.h):
        for t, (x, pc) in P.rows_at(i, names).items():
            yy = P.y_a[i, col[t]]
            if np.isnan(yy):
                continue
            X.append(x); Y.append(yy); O.append(logit(pc))
    X, Y, O = np.array(X), np.array(Y), np.array(O)
    W = np.full(len(Y), n_tickers * C.PRIOR_DAYS / max(len(Y), 1))
    b, H = laplace(X, Y, O, W, C.RIDGE)
    single = {}
    for j, n in enumerate(names):
        bj, Hj = laplace(X[:, [j]], Y, O, W, C.RIDGE)
        single[n] = dict(b=bj.tolist(), H=Hj.tolist())
    return dict(names=list(names), b=b.tolist(), H=H.tolist(), single=single, n_hist=int(len(Y)),
                cutoff=str(cutoff), source=P.task)


def prior_for(pr, names):
    """Prior auf die aktuelle Expertenliste abbilden; spaet geborene Experten: Mittel 0, nur Ridge."""
    k = len(names)
    b0 = np.zeros(k + 1)
    L = np.diag(np.r_[C.RIDGE * 0.01, np.full(k, C.RIDGE)])
    if pr is None:
        return b0, L
    idx = [0] + [1 + pr["names"].index(n) if n in pr["names"] and not _late(n) else -1 for n in names]
    Hp, bp = np.array(pr["H"]), np.array(pr["b"])
    for a, ia in enumerate(idx):
        if ia < 0:
            continue
        b0[a] = bp[ia]
        for c, ic in enumerate(idx):
            if ic >= 0:
                L[a, c] = Hp[ia, ic]
    return b0, L


def _late(n):
    return next(e for e in E.REGISTRY if e["name"] == n)["born"] > E.START


class Brain:
    """Haelt Prior und Vorwaertsdaten je (Aufgabe, Horizont) und schaetzt die Modelle."""

    def __init__(self):
        self.prior = {}
        self.fwd = {}      # (task,h) -> list of (date, names, x, y, off)
        self.models = {}   # (task,h) -> dict(names, beta_ens, beta_single{name: beta})

    def train(self, key, asof, names):
        pr = self.prior.get(key)
        k = len(names)
        rows = self.fwd.get(key, [])
        X = np.zeros((len(rows), k)); Y = np.zeros(len(rows)); O = np.zeros(len(rows)); W = np.zeros(len(rows))
        for i, (d, nm, x, yy, o) in enumerate(rows):
            for j, n in enumerate(names):
                if n in nm:
                    X[i, j] = x[nm.index(n)]
            Y[i], O[i] = yy, o
            W[i] = 0.5 ** ((pd.Timestamp(asof) - pd.Timestamp(d)).days / C.FORWARD_HALFLIFE_DAYS)
        b0, L = prior_for(pr, names)
        ens = fit_logit(X, Y, O, W, C.RIDGE, b0, L)
        single = {}
        for j, n in enumerate(names):
            if pr is not None and n in pr["single"] and not _late(n):
                sb0, sL = np.array(pr["single"][n]["b"]), np.array(pr["single"][n]["H"])
            else:
                sb0, sL = np.zeros(2), np.diag([C.RIDGE * 0.01, C.RIDGE])
            single[n] = fit_logit(X[:, [j]], Y, O, W, C.RIDGE, sb0, sL)
        self.models[key] = dict(names=names, ens=ens, single=single, n_fwd=len(rows))

    def predict(self, key, x, pc):
        m = self.models[key]
        o = logit(pc)
        p = float(sigmoid(o + m["ens"][0] + x @ m["ens"][1:]))
        pe = [float(sigmoid(o + m["single"][n][0] + x[j] * m["single"][n][1])) for j, n in enumerate(m["names"])]
        return p, pe


# ---------------------------------------------------------------- Journal
def model_hash():
    hs = hashlib.sha256()
    for fn in ("config.py", "experts.py", "orakel.py"):
        with open(os.path.join(HERE, fn), "rb") as f:
            hs.update(f.read())
    return hs.hexdigest()[:12]


class Journal:
    def __init__(self, path=None):
        self.path = path
        self.recs = []
        if path and os.path.exists(path):
            with open(path) as f:
                self.recs = [json.loads(l) for l in f if l.strip()]

    def head(self):
        return self.recs[-1]["hash"] if self.recs else "GENESIS"

    def append(self, rec):
        rec = dict(rec)
        rec["prev"] = self.head()
        body = json.dumps(rec, sort_keys=True, separators=(",", ":"))
        rec["hash"] = hashlib.sha256(body.encode()).hexdigest()
        self.recs.append(rec)
        if self.path:
            with open(self.path, "a") as f:
                f.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

    def verify(self):
        prev = "GENESIS"
        for i, r in enumerate(self.recs):
            r2 = {k: v for k, v in r.items() if k != "hash"}
            if r2.get("prev") != prev:
                return False, i
            body = json.dumps(r2, sort_keys=True, separators=(",", ":"))
            if hashlib.sha256(body.encode()).hexdigest() != r["hash"]:
                return False, i
            prev = r["hash"]
        return True, len(self.recs)

    def forecasts(self):
        return [r for r in self.recs if r["type"] == "F"]

    def resolved_keys(self):
        return {(r["asof"], r["task"], r["h"]) for r in self.recs if r["type"] == "R"}


# ---------------------------------------------------------------- Kernschritte
def resolve(J, panels, today_pos_of):
    done = J.resolved_keys()
    n = 0
    for F in J.forecasts():
        key = (F["asof"], F["task"], F["h"])
        if key in done:
            continue
        P = panels[(F["task"], F["h"])]
        d = pd.Timestamp(F["asof"])
        if d not in P.pos:
            continue
        i = P.pos[d]
        if i + F["h"] > today_pos_of:
            continue
        rr = {t: P.r.at[d, t] for t in F["rows"]}
        rr = {t: float(v) for t, v in rr.items() if not np.isnan(v)}
        if not rr:
            continue
        if P.style == "xs":
            med = float(np.median(list(rr.values())))
            yy = {t: int(v > med) for t, v in rr.items()}
        else:
            yy = {t: int(v > 0) for t, v in rr.items()}
        J.append(dict(type="R", asof=F["asof"], task=F["task"], h=F["h"],
                      resolved_on=str(P.dates[i + F["h"]].date()), y=yy, r=rr))
        n += 1
    return n


def load_forward(J, brain):
    ys = {(r["asof"], r["task"], r["h"]): r for r in J.recs if r["type"] == "R"}
    brain.fwd = {}
    for F in J.forecasts():
        R = ys.get((F["asof"], F["task"], F["h"]))
        if R is None:
            continue
        for t, row in F["rows"].items():
            if t not in R["y"]:
                continue
            brain.fwd.setdefault((F["task"], F["h"]), []).append(
                (F["asof"], F["experts"], np.array(row["x"]), float(R["y"][t]), logit(row["pc"])))


def issue(J, brain, panels, date, mh):
    out = 0
    have = {(r["asof"], r["task"], r["h"]) for r in J.forecasts()}
    for (task, h), P in panels.items():
        ds = str(date.date())
        if (ds, task, h) in have:
            continue
        names = [e["name"] for e in E.active(P.style, ds)]
        brain.train((task, h), date, names)
        rows = {}
        for t, (x_all, pc) in P.rows_at(date, names).items():
            p, pe = brain.predict((task, h), x_all, pc)
            rows[t] = dict(p=round(p, 5), pc=round(pc, 5), pe=[round(v, 5) for v in pe],
                           x=[round(float(v), 4) for v in x_all])
        if rows:
            J.append(dict(type="F", asof=ds, task=task, h=h, model=mh, experts=names, rows=rows,
                          issued_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
            out += 1
    return out


def make_panels(D):
    return {(t, h): Panel(D, t, h) for t in C.TASKS for h in C.HORIZONS}


def load_priors(brain, panels, cutoff, cache_name):
    path = os.path.join(STATE, cache_name)
    if os.path.exists(path):
        with open(path) as f:
            raw = json.load(f)
        brain.prior = {(k[0], int(k[1:])): v for k, v in raw.items()}
        return
    for (task, h), P in panels.items():
        cfg = C.TASKS[task]
        src = task if cfg["prior"] else cfg.get("prior_from")
        if src is None:
            continue
        Psrc = panels[(src, h)]
        names = [e["name"] for e in E.REGISTRY if Psrc.style in e["styles"] and not _late(e["name"])]
        brain.prior[(task, h)] = build_prior(Psrc, cutoff, names, len(cfg["tickers"]))
    with open(path, "w") as f:
        json.dump({f"{t}{h}": v for (t, h), v in brain.prior.items()}, f)


# ---------------------------------------------------------------- Auswertung
def nw_t(x, lag):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    T = len(x)
    if T < 3:
        return np.nan, np.nan
    m = x.mean()
    e = x - m
    v = e @ e / T
    for l in range(1, min(lag, T - 1) + 1):
        v += 2 * (1 - l / (lag + 1)) * (e[l:] @ e[:-l]) / T
    se = np.sqrt(max(v, 1e-18) / T)
    return m, m / se


def ll(p, y):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def score(J):
    ys = {(r["asof"], r["task"], r["h"]): r for r in J.recs if r["type"] == "R"}
    res = {}
    for F in J.forecasts():
        R = ys.get((F["asof"], F["task"], F["h"]))
        if R is None:
            continue
        key = (F["task"], F["h"])
        S = res.setdefault(key, dict(dates=[], d_ens=[], d_exp={}, all_p=[], all_y=[], port=[],
                                     llm=0.0, llc=0.0, n=0, lle={}))
        pl, yl, dl, pcl, rl = [], [], [], [], []
        dex = {}
        for t, row in F["rows"].items():
            if t not in R["y"]:
                continue
            y = R["y"][t]
            pl.append(row["p"]); yl.append(y); pcl.append(row["pc"]); rl.append(R["r"][t])
            for n, pe in zip(F["experts"], row["pe"]):
                dex.setdefault(n, []).append(ll(row["pc"], y) - ll(pe, y))
                S["lle"][n] = S["lle"].get(n, 0.0) + ll(pe, y)
        if not pl:
            continue
        pl, yl, pcl, rl = map(np.array, (pl, yl, pcl, rl))
        S["dates"].append(F["asof"])
        S["d_ens"].append(float(np.mean(ll(pcl, yl) - ll(pl, yl))))
        for n, v in dex.items():
            S["d_exp"].setdefault(n, {})[F["asof"]] = float(np.mean(v))
        S["llm"] += float(ll(pl, yl).sum()); S["llc"] += float(ll(pcl, yl).sum()); S["n"] += len(yl)
        S["all_p"] += list(pl); S["all_y"] += list(yl)
        if C.TASKS[F["task"]]["style"] == "ts":
            sel = pl >= pcl + C.CONVICTION
            strat = float(rl[sel].mean()) if sel.any() else 0.0
            S["port"].append((strat, float(rl.mean()), float(sel.mean())))
        else:
            q = max(1, len(pl) // 5)
            order = np.argsort(-pl)
            S["port"].append((float(rl[order[:q]].mean()), float(rl.mean()), float(rl[order[-q:]].mean())))
    return res


def report(J, brain, panels, title="Orakel", path_md=None, path_json=None, sim=False):
    res = score(J)
    lines = [f"# {title} – Stand {max((F['asof'] for F in J.forecasts()), default='-')}", ""]
    if sim:
        lines += ["**Probelauf auf der Vergangenheit. Zaehlt nicht als Beweis:** Die Hypothesen wurden mit "
                  "Kenntnis der Literatur gewaehlt. Er prueft nur, ob die Mechanik funktioniert.", ""]
    ok, n = J.verify()
    lines += [f"Journal: {len(J.recs)} Eintraege, Hash-Kette {'OK' if ok else 'GEBROCHEN bei ' + str(n)}, "
              f"Kopf `{J.head()[:16]}`, Modell `{model_hash()}`", ""]
    out = dict(asof=None, tasks={}, head=J.head(), chain_ok=ok, sim=sim)
    lines += ["## Vorwaerts-Bilanz (nur aufgeloeste Prognosen)", "",
              "Skill = Log-Loss-Verbesserung gegen die Klimatologie. t nach Newey-West (Tage ueberlappen).", "",
              "| Aufgabe | h | Tage | Prognosen | Skill | t | Papier: Top/long | Durchschnitt | Differenz p.a. | t |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for (task, h), S in sorted(res.items()):
        if not S["dates"]:
            continue
        m, t = nw_t(S["d_ens"], h)
        skill = (S["llc"] - S["llm"]) / S["llc"] * 100
        port = np.array(S["port"])
        diff = port[:, 0] - port[:, 1]
        pm, pt = nw_t(diff, h)
        ann = 252 / h
        lines.append(f"| {task} {C.TASKS[task]['name']} | {h} | {len(S['dates'])} | {S['n']} | {skill:+.2f} % | "
                     f"{t:.2f} | {port[:,0].mean()*ann*100:+.1f} % | {port[:,1].mean()*ann*100:+.1f} % | "
                     f"{pm*ann*100:+.1f} % | {pt:.2f} |")
        out["tasks"][f"{task}{h}"] = dict(days=len(S["dates"]), n=S["n"], skill=skill, t=t,
                                          port_ann=port[:, 0].mean() * ann, bench_ann=port[:, 1].mean() * ann,
                                          diff_ann=pm * ann, diff_t=pt)
    lines += ["", "## Welche Theorie traegt? (Experten einzeln, vorwaerts)", "",
              "| Aufgabe | h | Experte | Skill | t | Gewicht im Modell |", "|---|---|---|---|---|---|"]
    for (task, h), S in sorted(res.items()):
        m_ = brain.models.get((task, h))
        rows = []
        for n, dd in S["d_exp"].items():
            ser = [dd[d] for d in S["dates"] if d in dd]
            mm, tt = nw_t(ser, h)
            sk = (S["llc"] - S["lle"][n]) / S["llc"] * 100
            wgt = ""
            if m_ and n in m_["names"]:
                wgt = f"{m_['ens'][1 + m_['names'].index(n)]:+.3f}"
            rows.append((tt if not np.isnan(tt) else -99, n, sk, wgt))
        for tt, n, sk, wgt in sorted(rows, reverse=True):
            lines.append(f"| {task} | {h} | {n} | {sk:+.2f} % | {tt:.2f} | {wgt} |")
            out.setdefault("experts", []).append(dict(task=task, h=h, name=n, skill=sk,
                                                      t=None if tt == -99 else tt))
    lines += ["", "## Kalibrierung (alle Aufgaben)", "", "| p-Bereich | n | Ø p | Trefferquote |", "|---|---|---|---|"]
    allp = np.concatenate([np.array(S["all_p"]) for S in res.values()]) if res else np.array([])
    ally = np.concatenate([np.array(S["all_y"]) for S in res.values()]) if res else np.array([])
    for lo, hi in [(0, .45), (.45, .5), (.5, .55), (.55, .6), (.6, 1)]:
        s = (allp >= lo) & (allp < hi)
        if s.sum():
            lines.append(f"| {lo:.2f}–{hi:.2f} | {s.sum()} | {allp[s].mean():.3f} | {ally[s].mean():.3f} |")
    # aktuelle Prognosen
    lines += ["", "## Aktuelle Prognosen", "", "In Klammern: Abstand zur Klimatologie in Prozentpunkten (das eigentliche Signal).", ""]
    latest = {}
    for F in J.forecasts():
        latest[(F["task"], F["h"])] = F
    for (task, h), F in sorted(latest.items()):
        out["asof"] = F["asof"]
        items = sorted(F["rows"].items(), key=lambda kv: -(kv[1]["p"] - kv[1]["pc"]))
        fmt = lambda t, r: (f"{t} {r['p']*100:.0f} % ({(r['p']-r['pc'])*100:+.1f})")
        top = ", ".join(fmt(t, r) for t, r in items[:5])
        bot = ", ".join(fmt(t, r) for t, r in items[-3:])
        lab = "steigt" if C.TASKS[task]["style"] == "ts" else "schlaegt Median"
        lines.append(f"- **{task} {C.TASKS[task]['name']}, {h} Tage** (P {lab}, ab {F['asof']}): "
                     f"oben {top} · unten {bot}")
        out["tasks"].setdefault(f"{task}{h}", {})["latest"] = {t: [r["p"], r["pc"]] for t, r in F["rows"].items()}
        out["tasks"][f"{task}{h}"]["latest_asof"] = F["asof"]
    lines += ["", "## Aktuelle Theorie (Gewichte des Gesamtmodells)", ""]
    out["weights"] = {f"{t}{h}": dict(n_fwd=m_["n_fwd"], w={n: float(m_["ens"][1 + j]) for j, n in enumerate(m_["names"])})
                      for (t, h), m_ in brain.models.items()}
    out["mechanism"] = {e["name"]: e["mechanism"] for e in E.REGISTRY}
    out["task_names"] = {t: v["name"] for t, v in C.TASKS.items()}
    out["styles"] = {t: v["style"] for t, v in C.TASKS.items()}
    out["model"] = model_hash()
    out["n_records"] = len(J.recs)
    out["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for (task, h), m_ in sorted(brain.models.items()):
        ws = ", ".join(f"{n} {m_['ens'][1+j]:+.3f}" for j, n in enumerate(m_["names"]))
        lines.append(f"- {task}{h} (Vorwaertsdaten: {m_['n_fwd']}): {ws}")
    txt = "\n".join(lines) + "\n"
    if path_md:
        with open(path_md, "w") as f:
            f.write(txt)
    if path_json:
        with open(path_json, "w") as f:
            json.dump(out, f, indent=1, default=float)
    return txt


# ---------------------------------------------------------------- Befehle
def cmd_run(offline=False):
    D = load_data(offline)
    panels = make_panels(D)
    asof = D["close"].index[-1]
    if str(asof.date()) < E.START:
        print("Vor START – nichts zu tun."); return
    J = Journal(JOURNAL)
    ok, n = J.verify()
    if not ok:
        raise SystemExit(f"Hash-Kette gebrochen bei Eintrag {n}. Abbruch.")
    brain = Brain()
    load_priors(brain, panels, E.START, "prior.json")
    today = len(D["close"].index) - 1
    nr = resolve(J, panels, today)
    load_forward(J, brain)
    ni = issue(J, brain, panels, asof, model_hash())
    for key in panels:
        if key not in brain.models:
            names = [e["name"] for e in E.active(panels[key].style, str(asof.date()))]
            brain.train(key, asof, names)
    report(J, brain, panels, path_md=os.path.join(STATE, "bericht.md"),
           path_json=os.path.join(os.path.dirname(HERE), "orakel_data.json"))
    print(f"asof {asof.date()}: {nr} aufgeloest, {ni} Prognosesaetze, Kopf {J.head()[:16]}")


def cmd_simulate(start, offline=True, refit_every=5):
    D = load_data(offline)
    panels = make_panels(D)
    J = Journal(None)
    brain = Brain()
    load_priors(brain, panels, start, f"prior_sim_{start}.json")
    dates = D["close"].index
    i0 = np.searchsorted(dates.values, np.datetime64(pd.Timestamp(start)))
    mh = "SIM"
    for i in range(i0, len(dates)):
        resolve(J, panels, i)
        if (i - i0) % refit_every == 0:
            load_forward(J, brain)
            frozen = dict(brain.models)
        else:
            frozen = None
        d = dates[i]
        if frozen is None:
            # zwischen den Neuschaetzungen: Modelle nicht neu trainieren
            have = {(r["asof"], r["task"], r["h"]) for r in J.forecasts()}
            for (task, h), P in panels.items():
                names = brain.models[(task, h)]["names"]
                rows = {}
                for t, (x, pc) in P.rows_at(d, names).items():
                    p, pe = brain.predict((task, h), x, pc)
                    rows[t] = dict(p=round(p, 5), pc=round(pc, 5), pe=[round(v, 5) for v in pe],
                                   x=[round(float(v), 4) for v in x])
                if rows:
                    J.append(dict(type="F", asof=str(d.date()), task=task, h=h, model=mh, experts=names,
                                  rows=rows, issued_utc="SIM"))
        else:
            issue(J, brain, panels, d, mh)
    resolve(J, panels, len(dates) - 1)
    txt = report(J, brain, panels, title=f"Orakel-Probelauf ab {start}",
                 path_md=os.path.join(STATE, f"probelauf_{start}.md"), sim=True)
    print(txt)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "run":
        cmd_run(offline="--offline" in sys.argv)
    elif cmd == "verify":
        ok, n = Journal(JOURNAL).verify()
        print("OK" if ok else f"GEBROCHEN bei {n}", n)
    elif cmd == "simulate":
        cmd_simulate(sys.argv[2], offline="--online" not in sys.argv)
    elif cmd == "report":
        D = load_data(True); panels = make_panels(D); J = Journal(JOURNAL); brain = Brain()
        load_priors(brain, panels, E.START, "prior.json"); load_forward(J, brain)
        for key, P in panels.items():
            brain.train(key, D["close"].index[-1], [e["name"] for e in E.active(P.style)])
        print(report(J, brain, panels, path_md=os.path.join(STATE, "bericht.md"),
                     path_json=os.path.join(STATE, "orakel.json")))
