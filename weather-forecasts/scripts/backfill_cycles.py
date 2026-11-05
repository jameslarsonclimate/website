"""
Fetch every 12Z/18Z run the scoreboard's "12Z / 18Z runs" toggle is still missing for the
current city period (display only: nothing is scored as submitted, appended to runs.jsonl,
committed or pushed). The scheduled run does the same within a time budget
(cycle_backfill, CYCLE_BUDGET_S); this does it all at once, e.g. at a new city.

    python scripts/backfill_cycles.py [ICAO] [--dry-run]

Writes data/wxchallenge/cycle_runs.jsonl and the per-cycle scores in verification.json; the
next scheduled run commits and pushes them. Run it with the wxchallenge conda env. Takes the
same lock as the scheduled job.
"""

import argparse
import importlib.util
import os
import sys
from collections import Counter
from datetime import datetime, timezone
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
    ap.add_argument("--dry-run", action="store_true", help="list what would be fetched, then stop")
    args = ap.parse_args()

    import json
    import pandas as pd
    import wxc_verify
    from wxc_stations import get_station

    spec = importlib.util.spec_from_file_location("wxc_pipeline", ROOT / "getForecast_wxChallenge-pushGitHub.py")
    pipe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pipe)

    station = get_station(args.station)
    verif = json.loads(wxc_verify.VERIF.read_text())
    if verif.get("station") != station.icao:
        sys.exit(f"verification.json is for {verif.get('station')}, not {station.icao}")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    if args.dry_run:
        days = sorted({d["date"] for d in verif.get("days") or []})
        plan = wxc_verify.cycle_plan(wxc_verify.read_runs(), wxc_verify.read_jsonl(wxc_verify.CYCLE_RUNS),
                                     station.icao, days, pipe.CYCLE_SOURCES)
        print(f"{len(plan)} runs to fetch: {dict(Counter(m for _, m, _ in plan))}")
        return
    take_lock()
    try:
        points = pd.DataFrame({"longitude": [station.lon], "latitude": [station.lat]})
        n = pipe.cycle_backfill(station, verif, points, now, budget_s=None)
        wxc_verify.refresh_cycles(station.icao)
        print(f"{n} run(s) added; verification.json updated")
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
