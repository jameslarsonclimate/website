"""
Explore precip consensus variants on stored data (research only; the live consensus is
wxc_verify.consensus). Each variant rebuilds every stored day's precip consensus from the
earlier days only (as tune_consensus.py does) and scores it with WxChallenge points.

Variants
  wmean    1/(MAE+off) weighted mean of raw members (the current method; off=0.5 now)
  median   member median
  gate     wmean, but 0 when the weighted share of members forecasting >= 0.01" is < p
  regime   wet/dry split by the member median (>= 0.01" = wet day): each model's MAE comes from
           earlier days of the same regime; on wet days its forecast is also bias-corrected
           (additive shrunk, or multiplicative ratio sum(obs)/sum(fc)); dry days uncorrected
  own      like regime, but split by each model's own forecast (wet when it says >= 0.01")

  python scripts/tune_precip.py [--station KMSP ...] [--top 25]
"""

import argparse
import itertools
import math
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backtest_consensus import periods  # noqa: E402
import wxc_verify as v  # noqa: E402

P = "precip_in"
WET = 0.01


def members(d, prior):
    """The live consensus' precip members for day d (fresh, not excluded)."""
    fc = {n: f for n, f in d["forecasts"].items() if n != "CONSENSUS"}
    c = v.consensus(fc, v.model_stats(prior))
    names = (c.get("method", {}).get(P) or {}).get("members", [])
    return {n: fc[n][P] for n in names}


def track(prior, hl, select=lambda d, n, f: True):
    """{model: (sum w, sum w*|err|, sum w*err, sum w*fc, sum w*ob, n)} over prior days passing select."""
    if not prior:
        return {}
    ref = date.fromisoformat(prior[-1]["date"])
    out = {}
    for d in prior:
        age = (ref - date.fromisoformat(d["date"])).days
        w = 0.5 ** (age / hl) if hl else 1.0
        for n, s in d["models"].items():
            if n == "CONSENSUS" or s["error"].get(P) is None:
                continue
            f = s["forecast"][P]
            if not select(d, n, f):
                continue
            e = s["error"][P]
            t = out.setdefault(n, [0, 0, 0, 0, 0, 0])
            t[0] += w; t[1] += w * abs(e); t[2] += w * e; t[3] += w * f; t[4] += w * (f - e); t[5] += 1
    return out


def median(xs):
    s = sorted(xs)
    k = len(s)
    return s[k // 2] if k % 2 else (s[k // 2 - 1] + s[k // 2]) / 2


def wmean(vals, tr, off):
    ws = {n: 1 / (tr[n][1] / tr[n][0] + off) for n in vals if n in tr and tr[n][5] >= v.MIN_DAYS_FOR_CORRECTION}
    if not ws:
        return sum(vals.values()) / len(vals), {n: 1.0 for n in vals}
    wm = median(list(ws.values()))
    ws = {n: ws.get(n, wm) for n in vals}
    return sum(vals[n] * ws[n] for n in vals) / sum(ws.values()), ws


def forecast(variant, cfg, d, prior):
    vals = members(d, prior)
    if not vals:
        return None
    hl = cfg.get("hl", 12)
    if variant == "median":
        return median(list(vals.values()))
    if variant in ("wmean", "gate"):
        x, ws = wmean(vals, track(prior, hl), cfg["off"])
        if variant == "gate":
            share = sum(ws[n] for n in vals if vals[n] >= WET) / sum(ws.values())
            if share < cfg["p"]:
                return 0.0
        return x
    # regime / own: per-model stats from the matching regime of earlier days
    if variant == "regime":
        wet_day = lambda dd: median([f[P] for n, f in dd["forecasts"].items()
                                     if n != "CONSENSUS" and f.get(P) is not None] or [0]) >= WET
        wet = median(list(vals.values())) >= WET
        sel = lambda dd, n, f: wet_day(dd) == wet
        wet_of = {n: wet for n in vals}
    else:
        wet_of = {n: vals[n] >= WET for n in vals}
        sel = None
    corrected, ws = {}, {}
    for n, x in vals.items():
        w_ = wet_of[n]
        s = sel or (lambda dd, nn, f, w_=w_: (f >= WET) == w_)
        t = track(prior, hl, s).get(n)
        if t and t[5] >= v.MIN_DAYS_FOR_CORRECTION:
            ws[n] = 1 / (t[1] / t[0] + (cfg["off_wet"] if w_ else cfg["off_dry"]))
            if w_ and cfg["bc"] == "add":
                k = t[5] / (t[5] + cfg["K"])
                x = x - k * t[2] / t[0]
            elif w_ and cfg["bc"] == "mult" and t[3] > 0:
                k = t[5] / (t[5] + cfg["K"])
                ratio = min(max(t[4] / t[3], 0.25), 4.0)
                x = x * (1 + k * (ratio - 1))
        corrected[n] = max(x, 0.0)
    if ws:
        wm = median(list(ws.values()))
        ws = {n: ws.get(n, wm) for n in corrected}
    else:
        ws = {n: 1.0 for n in corrected}
    return sum(corrected[n] * ws[n] for n in corrected) / sum(ws.values())


def score(segments, variant, cfg, min_prior=1):
    out = {}
    for st, days in segments:
        for i, d in enumerate(days):
            if i < min_prior or d["obs"].get(P) is None:
                continue
            prior = [p for p in days[:i] if p["date"] < d["date"]]
            x = forecast(variant, cfg, d, prior)
            if x is not None:
                out[(st, d["date"])] = v.var_points(P, max(x, 0.0), d["obs"][P])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--station", nargs="*")
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    runs, obs = v.read_jsonl(v.RUNS), v.read_jsonl(v.OBS)
    stations = a.station or sorted({o["station"] for o in obs})
    segments = [(st, p) for st in stations for p in periods(v.scored_days(st, runs=runs, obs=obs))]

    configs = [("wmean", {"off": 0.5, "hl": 12})]
    configs += [("wmean", {"off": o, "hl": h}) for o in (0.005, 0.01, 0.02, 0.05, 0.1) for h in (6, 12)]
    configs += [("median", {})]
    configs += [("gate", {"off": o, "p": p, "hl": 12}) for o in (0.01, 0.05, 0.5) for p in (0.2, 0.33, 0.5, 0.67)]
    for variant in ("regime", "own"):
        for bc, K, ow, od in itertools.product(("none", "add", "mult"), (1, 3, 6),
                                               (0.01, 0.05, 0.2), (0.005, 0.02, 0.1)):
            if bc == "none" and K != 3:
                continue
            configs.append((variant, {"bc": bc, "K": K, "off_wet": ow, "off_dry": od, "hl": 12}))

    base = score(segments, *configs[0])
    wet_days = {k for st, days in segments for d in days if d["obs"].get(P, 0) >= WET
                for k in [(st, d["date"])]}
    print(f"{len(base)} days ({len(wet_days & set(base))} with >= 0.01\" observed)")
    rows = []
    for variant, cfg in configs:
        res = score(segments, variant, cfg)
        diff = [res[k] - base[k] for k in base if k in res]
        m = sum(diff) / len(diff)
        se = math.sqrt(sum((x - m) ** 2 for x in diff) / (len(diff) - 1) / len(diff)) * len(diff)
        wet = sum(res[k] for k in res if k in wet_days)
        rows.append((sum(res.values()), sum(diff), se, wet, sum(res.values()) - wet, variant, cfg))
    rows.sort(key=lambda r: r[0])
    print(f"{'points':>7s} {'vs now':>7s} {'±SE':>5s} {'wet':>6s} {'dry':>6s}  variant  settings")
    for i, (pts, d, se, wet, dry, var, cfg) in enumerate(rows):
        if i < a.top or (var == "wmean" and cfg == configs[0][1]) or var == "median":
            print(f"{pts:7.1f} {d:+7.1f} {se:5.1f} {wet:6.1f} {dry:6.1f}  {var:7s}  "
                  + " ".join(f"{k}={x}" for k, x in cfg.items()))


if __name__ == "__main__":
    main()
