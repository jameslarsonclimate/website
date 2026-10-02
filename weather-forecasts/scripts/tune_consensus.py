"""
Tune the consensus settings on stored data. Each variable's consensus (and its points) is
independent, so every variable is tuned on its own over a grid of:
  half-life   days for a verified day's weight to halve (0 = equal weights)
  shrink K    share of the bias removed = n_eff / (n_eff + K)  (0 = all of it)
  MAE offset  member weight = 1 / (MAE + offset): small = trust the best model more
  lookback    only use the last N days' track record (0 = everything since the period start)
For every combination the consensus is rebuilt for each stored day from the earlier days
only (as in backtest_consensus.py) and scored with WxChallenge points.

  python scripts/tune_consensus.py                                # every station with stored obs
  python scripts/tune_consensus.py --station KTPA --top 15
  python scripts/tune_consensus.py --half-lives 0 6 9 12 18 30 --shrink 1 3 6 --lookback 0 14

Output per variable: the best settings first, with the difference from the current settings
(wxc_verify.HALF_LIFE_DAYS, BIAS_SHRINK_DAYS, MAE_OFFSET) and its paired standard error over
days. Prefer the simplest setting whose difference is within about 1 standard error of the best:
with a few weeks of data, the "best" on paper is mostly noise. To adopt a setting, edit the
constants at the top of wxc_verify.py.
"""

import argparse
import itertools
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backtest_consensus import ROOT, SHORT, backtest, periods  # noqa: E402,F401
import wxc_verify as v  # noqa: E402


def current(var: str) -> tuple:
    off = v.MAE_OFFSET[var] if isinstance(v.MAE_OFFSET, dict) else v.MAE_OFFSET
    return (v.HALF_LIFE_DAYS.get(var) or 0, v.BIAS_SHRINK_DAYS, off, 0)


def run(segments: list, var: str, combo: tuple, min_prior: int) -> dict:
    """{(station, date): points of `var`} for one setting over all city periods."""
    hl, k, off, lb = combo
    out = {}
    for station, days in segments:
        for r in backtest(days, {var: hl or None}, lb or None, min_prior,
                          shrink_days=k, mae_offset=off):
            out[(station, r["date"])] = r["points"][var]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--station", nargs="*", help="ICAO ids (default: every station with stored obs)")
    ap.add_argument("--var", nargs="*", choices=v.VARS, default=v.VARS)
    ap.add_argument("--half-lives", nargs="*", type=float, default=[0, 4, 6, 9, 12, 18, 30])
    ap.add_argument("--shrink", nargs="*", type=float, default=[0, 1, 3, 6])
    ap.add_argument("--offsets", nargs="*", type=float, default=[0.25, 0.5, 1, 2],
                    help="MAE offsets for temperature (F) and wind (kt)")
    ap.add_argument("--precip-offsets", nargs="*", type=float, default=[0.02, 0.05, 0.1, 0.5],
                    help="MAE offsets for precip (in)")
    ap.add_argument("--lookback", nargs="*", type=int, default=[0], help="days of track record (0 = all)")
    ap.add_argument("--min-prior", type=int, default=1, help="earlier scored days needed to count a day")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()

    runs, obs = v.read_jsonl(v.RUNS), v.read_jsonl(v.OBS)
    stations = a.station or sorted({o["station"] for o in obs})
    segments = [(st, p) for st in stations for p in periods(v.scored_days(st, runs=runs, obs=obs))]
    print("Data: " + ", ".join(f"{st} {p[0]['date']}..{p[-1]['date']} ({len(p)} d)" for st, p in segments))

    for var in a.var:
        offs = a.precip_offsets if var == "precip_in" else a.offsets
        shrinks = [0.0] if var == "precip_in" else a.shrink       # precip is never bias-corrected
        grid = list(itertools.product(a.half_lives, shrinks, offs, a.lookback))
        cur = current(var)
        if var == "precip_in":
            cur = (cur[0], 0.0, cur[2], cur[3])
        if cur not in grid:
            grid.append(cur)
        base = run(segments, var, cur, a.min_prior)
        if not base:
            sys.exit("No day has an earlier scored day yet; hindcast more days first "
                     "(scripts/warm_hindcast.sh ICAO 21).")
        rows = []
        for combo in grid:
            res = run(segments, var, combo, a.min_prior)
            diff = [res[k] - base[k] for k in base if k in res]
            m = sum(diff) / len(diff)
            se = math.sqrt(sum((x - m) ** 2 for x in diff) / (len(diff) - 1) / len(diff)) if len(diff) > 1 else float("nan")
            rows.append((sum(res.values()), combo, sum(diff), se * len(diff)))
        rows.sort(key=lambda r: r[0])
        unit = "in" if var == "precip_in" else "kt" if var == "wind_max_kt" else "F"
        print(f"\n{SHORT[var].upper()} ({len(base)} days)   current: half-life {cur[0]:g} d, "
              f"K {cur[1]:g}, offset {cur[2]:g} {unit}, lookback {'all' if not cur[3] else cur[3]}")
        print(f"  {'points':>7s} {'vs now':>7s} {'±SE':>5s}   half-life  K    offset  lookback")
        for pts, (hl, k, off, lb), d, se in rows[:a.top]:
            mark = "  <- current" if (hl, k, off, lb) == cur else ""
            print(f"  {pts:7.1f} {d:+7.1f} {se:5.1f}   {'equal' if not hl else f'{hl:g} d':>9s} {k:<4g} "
                  f"{off:<7g} {'all' if not lb else lb:>8}{mark}")
        if all(r[1] != cur for r in rows[:a.top]):
            pts, _, d, se = next(r for r in rows if r[1] == cur)
            print(f"  {pts:7.1f} {d:+7.1f} {se:5.1f}   (current settings, rank "
                  f"{[r[1] for r in rows].index(cur) + 1} of {len(rows)})")


if __name__ == "__main__":
    main()
