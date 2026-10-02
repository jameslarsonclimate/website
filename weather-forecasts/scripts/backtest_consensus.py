"""
Backtest the consensus on stored data: for each observed day, rebuild it from the models'
stored pre-deadline forecasts for that day, corrected and weighted with the track record of
the earlier days only (no peeking), and score it with WxChallenge points.

  python scripts/backtest_consensus.py                    # KTPA, the three standard configs
  python scripts/backtest_consensus.py --station KDSM --by-day

Only days that have at least --min-prior earlier scored days are counted (the same days for
every config), since with no track record every config is the same plain average.
More history: scripts/warm_hindcast.sh ICAO DAYS (hindcasts DAYS days before the last full day).
"""

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import wxc_verify as v  # noqa: E402

EQUAL = {var: None for var in v.VARS}
CONFIGS = [
    ("prior 4 days, equal weight", "4d eq", dict(lookback=4, half_lives=EQUAL)),
    ("prior 14 days, equal weight", "14d eq", dict(lookback=14, half_lives=EQUAL)),
    ("prior 14 days, decay-weighted", "14d decay", dict(lookback=14, half_lives=v.HALF_LIFE_DAYS)),
]
SHORT = {"tmax_f": "high", "tmin_f": "low", "wind_max_kt": "wind", "precip_in": "precip"}


def backtest(days: list, half_lives: dict = v.HALF_LIFE_DAYS, lookback=None, min_prior: int = 1, **kw) -> list:
    """
    Rebuilt-consensus points per day: [{"date", "points": {var: pts}, "total"}].
    `days` from wxc_verify.scored_days (one station, one city period). Extra keywords
    (shrink_days, mae_offset) go to wxc_verify.consensus.
    """
    out = []
    for i, d in enumerate(days):
        if i < min_prior or any(d["obs"].get(var) is None for var in v.VARS):
            continue
        c = v.reconstruct_consensus(days, i, half_lives, lookback, **kw)
        if not c:
            continue
        pts = {var: v.var_points(var, c[var], d["obs"][var]) for var in v.VARS}
        out.append({"date": d["date"], "points": pts, "total": sum(pts.values())})
    return out


def model_points(days: list, dates: set) -> dict:
    """Each model's own points over the given days (for reference)."""
    tot = {}
    for d in days:
        if d["date"] in dates:
            for name, s in d["models"].items():
                if name != "CONSENSUS":
                    n, p = tot.get(name, (0, 0.0))
                    tot[name] = (n + 1, p + s["points"])
    return tot


def periods(days: list, gap: int = 7) -> list:
    """Split one station's days into city periods (a gap of more than `gap` days starts a new one)."""
    out = []
    for d in days:
        if out and (date.fromisoformat(d["date"]) - date.fromisoformat(out[-1][-1]["date"])).days <= gap:
            out[-1].append(d)
        else:
            out.append([d])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--station", default="KTPA")
    ap.add_argument("--start", help="first day YYYY-MM-DD (default: all stored days)")
    ap.add_argument("--end", help="last day YYYY-MM-DD")
    ap.add_argument("--min-prior", type=int, default=1, help="earlier scored days needed to count a day")
    ap.add_argument("--by-day", action="store_true", help="also print each day's points")
    a = ap.parse_args()

    runs, obs = v.read_jsonl(v.RUNS), v.read_jsonl(v.OBS)
    allp = periods(v.scored_days(a.station, a.start, a.end, runs=runs, obs=obs))
    if not allp:
        sys.exit(f"No scored days stored for {a.station}.")
    days = allp[-1]                                  # the latest city period
    print(f"{a.station}: {len(days)} observed days {days[0]['date']}..{days[-1]['date']}"
          + (f" (latest of {len(allp)} periods; use --start/--end for another)" if len(allp) > 1 else ""))

    results = [(name, backtest(days, min_prior=a.min_prior, **cfg)) for name, _, cfg in CONFIGS]
    n = len(results[0][1])
    if not n:
        sys.exit(f"No day has {a.min_prior} earlier scored day(s) yet. "
                 f"More history: scripts/warm_hindcast.sh {a.station} 21")
    print(f"Scored {n} days ({results[0][1][0]['date']}..{results[0][1][-1]['date']}), "
          f"each with only the earlier days' track record\n")
    print(f"{'config':32s} {'total':>6s} " + " ".join(f"{SHORT[var]:>6s}" for var in v.VARS) + f" {'/day':>5s}")
    for name, res in results:
        print(f"{name:32s} {sum(r['total'] for r in res):6.1f} "
              + " ".join(f"{sum(r['points'][var] for r in res):6.1f}" for var in v.VARS)
              + f" {sum(r['total'] for r in res) / n:5.1f}")

    ref = model_points(days, {r["date"] for r in results[0][1]})
    full = {k: p for k, (c, p) in ref.items() if c == n}
    if full:
        best = min(full, key=full.get)
        print(f"{'(best single model: ' + best + ')':32s} {full[best]:6.1f}")
    if n < 20:
        print(f"\nOnly {n} days: differences of a few points are within day-to-day noise.")

    if a.by_day:
        print(f"\n{'day':10s} " + " ".join(f"{short:>10s}" for _, short, _ in CONFIGS))
        for i in range(n):
            print(f"{results[0][1][i]['date']:10s} " + " ".join(f"{res[i]['total']:10.1f}" for _, res in results))


if __name__ == "__main__":
    main()
