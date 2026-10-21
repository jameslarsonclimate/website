"""
Give a model added during a city period (e.g. IFS_HRES) a track record over the whole period.

The main script hindcasts a newly added model itself, but only over its last HINDCAST_DAYS (14)
days. This hindcasts it for every observed day of the current city period that has no forecast
from it: the run out at 23Z the day before (as the main script's hindcasts), appended to
runs.jsonl as a hindcast row with only that model (a live forecast is never replaced), and its
hourly series added to the timeline of days that are hindcasts themselves. Then it rewrites
verification.json and compares the model's errors with a reference model's on the same days.
Nothing is committed or pushed: the next scheduled run does that.

    python scripts/hindcast_model.py [ICAO] [--model IFS_HRES] [--compare IFS] [--dry-run]

Only for models whose old runs can still be had (IFS_HRES: Open-Meteo's single-run archive; the
GRIB models: while their files are on the archives). Run it with the wxchallenge conda env.
Takes the same lock as the scheduled job.
"""

import argparse
import importlib
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

VARS = ["tmax_f", "tmin_f", "wind_max_kt", "precip_in"]


def compare(verif: dict, model: str, ref: str) -> list:
    """Rows of the side-by-side comparison on the days both were scored."""
    days = [d for d in verif["days"] if model in d["models"] and ref in d["models"]]
    rows = []
    for name in (model, ref):
        sc = [d["models"][name] for d in days]
        if not sc:
            continue
        n = len(sc)
        row = {"model": name, "n": n, "pts": sum(s["points"] for s in sc) / n}
        for v in VARS:
            e = [s["error"][v] for s in sc]
            row[f"{v}_mae"], row[f"{v}_bias"] = sum(map(abs, e)) / n, sum(e) / n
        rows.append(row)
    return rows


def print_compare(rows, title):
    if not rows:
        print(f"{title}: no days with both")
        return
    print(f"\n{title} ({rows[0]['n']} days)")
    print(f"  {'model':9s} {'pts/day':>7s}   {'high MAE':>8s} {'bias':>5s}   {'low MAE':>7s} {'bias':>5s}   "
          f"{'wind MAE':>8s} {'bias':>5s}   {'pcp MAE':>7s} {'bias':>6s}")
    for r in rows:
        print(f"  {r['model']:9s} {r['pts']:7.2f}   {r['tmax_f_mae']:8.2f} {r['tmax_f_bias']:+5.1f}   "
              f"{r['tmin_f_mae']:7.2f} {r['tmin_f_bias']:+5.1f}   {r['wind_max_kt_mae']:8.2f} "
              f"{r['wind_max_kt_bias']:+5.1f}   {r['precip_in_mae']:7.3f} {r['precip_in_bias']:+6.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("station", nargs="?", help="ICAO id (default: wxc_stations.CURRENT_STATION)")
    ap.add_argument("--model", default="IFS_HRES", help="model to hindcast (default IFS_HRES)")
    ap.add_argument("--compare", default="IFS", help="reference model for the error comparison (default IFS)")
    ap.add_argument("--dry-run", action="store_true", help="list the days that would be hindcast, then stop")
    args = ap.parse_args()

    import pandas as pd
    import wxc_verify
    from backfill_timeline import LOCK, take_lock
    from wxc_stations import get_station
    m = importlib.import_module("getForecast_wxChallenge-pushGitHub")

    station = get_station(args.station)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    start = wxc_verify.current_period_start(station.icao, now.date())
    runs = wxc_verify.read_runs()
    obs_days = sorted(o["date"] for o in wxc_verify.read_jsonl(wxc_verify.OBS)
                      if o["station"] == station.icao and o["date"] >= start and o["date"] < now.date().isoformat())
    todo = [d for d in obs_days
            if wxc_verify.hindcast_plan(runs, station.icao, d, [args.model])]
    print(f"{station.icao}: period from {start}; {args.model} to hindcast for {len(todo)} day(s): "
          f"{', '.join(todo) or 'none'}")
    if args.dry_run:
        return

    if todo:
        take_lock()
        try:
            points = pd.DataFrame({"longitude": [station.lon], "latitude": [station.lat]})
            for ds in todo:
                d = date.fromisoformat(ds)
                as_of = datetime(d.year, d.month, d.day, tzinfo=timezone.utc) - timedelta(hours=24 - m.HINDCAST_HOUR)
                res, mos, models = m.run_models(station, d, points, as_of, skip_grib=args.model not in m.GRIB_MODELS,
                                                only=[args.model])
                fc = models.get(args.model) or {}
                if fc.get("error") and m.wxc_carryover.is_network_error(fc["error"]):
                    print(f"  {ds}: not reached, left for a later run ({fc['error'][:80]})")
                    continue
                wxc_verify.append_run(as_of.isoformat(), station.icao, d, {args.model: fc}, hindcast=True)
                try:          # timeline series, on days that are hindcasts themselves
                    m.save_hindcast_series(station, d, as_of, res, mos)
                except Exception as exc:
                    print(f"  warning: series for {ds} not saved ({type(exc).__name__}: {exc})")
                print(f"  {ds}: {fc.get('init_time_utc')} run " + (f"failed: {fc['error']}" if fc.get("error") else
                      f"{fc['tmax_f']}/{fc['tmin_f']}F {fc['wind_max_kt']}kt {fc['precip_in']}in"))
        finally:
            LOCK.unlink(missing_ok=True)

    verif = wxc_verify.write_verification(station.icao, now.date())
    print_compare(compare(verif, args.model, args.compare), f"{args.model} vs {args.compare}, all scored days")
    live = {"days": [d for d in verif["days"] if not d.get("hindcast")]}
    print_compare(compare(live, args.model, args.compare), "  ... days after the city's first forecast day")


if __name__ == "__main__":
    main()
