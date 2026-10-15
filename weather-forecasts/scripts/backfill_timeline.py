"""
Extend the page's timeline back over the current city's earlier days (display only:
nothing is scored, appended to runs.jsonl, committed or pushed).

Days hindcast before hindcasts saved their hourly series have scores on the scoreboard but
no series, so the timeline starts later than the scoreboard. For each such day this rebuilds
the series from the runs that were out at 23Z the day before (the same runs the hindcast
scored: from the saved model results in cache/ while they are there, pruned after 35 days,
else downloaded again). The ensembles can't be rebuilt (Open-Meteo only serves the latest
run). Then it fills in those days' METARs, sky cover and model cloud cover and rewrites
data/wxchallenge/timeline.json. The next scheduled run commits and pushes the files.

New cities don't need this: their hindcast (scripts/warm_hindcast.sh) saves the series.

    python scripts/backfill_timeline.py [ICAO] [--goes] [--dry-run]

  --goes      also download the GOES cloud fraction for those days (~120 MB a day; without
              it the cloud panel shows the ASOS sky cover for them)
  --dry-run   list the days that would be rebuilt and what the cache holds, then stop

Run it with the wxchallenge conda env. Takes the same lock as the scheduled job.
"""

import argparse
import importlib
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LOCK = Path(f"/tmp/wxchallenge-{os.getuid()}.lock")     # same as getForecast_wxChallenge.sh


def take_lock():
    try:
        pid = int(LOCK.read_text().strip())
        os.kill(pid, 0)
        sys.exit(f"Another forecast run (pid {pid}) is going; try again once it finishes.")
    except (FileNotFoundError, ValueError, ProcessLookupError):
        pass
    except PermissionError:
        sys.exit("A forecast run holds the lock; try again once it finishes.")
    LOCK.write_text(str(os.getpid()))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("station", nargs="?", help="ICAO id (default: wxc_stations.CURRENT_STATION)")
    ap.add_argument("--goes", action="store_true", help="also download GOES for the rebuilt days")
    ap.add_argument("--dry-run", action="store_true", help="list what would be rebuilt, then stop")
    args = ap.parse_args()

    import pandas as pd
    import wxc_cache
    import wxc_timeline
    import wxc_verify
    from wxc_stations import get_station
    m = importlib.import_module("getForecast_wxChallenge-pushGitHub")

    station = get_station(args.station)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    today = (now - timedelta(hours=6)).date()
    verif = json.loads((m.DATA / "verification.json").read_text())
    if verif.get("station") != station.icao:
        sys.exit(f"verification.json is for {verif.get('station')}, not {station.icao}; run the forecast first")
    start = date.fromisoformat(verif["period_start"])
    days = [start + timedelta(days=i) for i in range((today - start).days)]
    todo = [d for d in days if wxc_verify.load_series(station.icao, d, "submitted") is None]
    models = [k for k in m.GRIB_ORDER if (k != "HRRR" or station.hrrr_model)
              and (k != "RRFS" or station.rrfs_domain)] + m.MOS_ORDER
    print(f"{station.icao}: scoreboard from {start}; {len(todo)} day(s) without hourly series: "
          f"{', '.join(map(str, todo)) or 'none'}")
    for d in todo:
        cached = sorted({p.name.rsplit("_", 2)[0].split("-v")[0] for p in (wxc_cache.CACHE_DIR / station.icao).glob(f"*_{d:%Y%m%d}.json")
                         if not p.name.startswith("_")})
        print(f"  {d}: saved model results for {', '.join(cached) or 'nothing (would download)'}")
    if args.dry_run:
        return

    take_lock()
    try:
        points = pd.DataFrame({"longitude": [station.lon], "latitude": [station.lat]})
        for d in todo:
            as_of = datetime(d.year, d.month, d.day, tzinfo=timezone.utc) - timedelta(hours=24 - m.HINDCAST_HOUR)
            print(f"\nSeries for {d} from the runs out at {as_of:%Y-%m-%d %HZ}")
            res, mos, _ = m.run_models(station, d, points, as_of, only=models)
            path = m.save_hindcast_series(station, d, as_of, res, mos)
            print(f"  {'saved ' + path.name if path else 'nothing saved'}")
        print("\nTimeline:")
        m.timeline_update(station, now, points, verif, budget_s=3600,
                          goes_days=None if args.goes else m.TIMELINE_GOES_DAYS)
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
