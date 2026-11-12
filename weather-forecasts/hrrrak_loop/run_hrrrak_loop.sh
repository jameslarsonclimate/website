#!/bin/bash
# launchd entry point for the HRRR-AK 4-panel loop (com.jglarson.hrrrak).
# Makes today's 12Z/18Z runs (hrrrak_loop.py skips non-forecast days and runs already done),
# and removes its own launchd job once the Alaska (PAYA) city is over.
LAST_RUN_DATE=20261119          # last UTC date a forecast is made (for Fri 20 Nov)
LABEL=com.jglarson.hrrrak
PY=/opt/homebrew/Caskroom/miniforge/base/envs/wxchallenge/bin/python
DIR="$(cd "$(dirname "$0")" && pwd)"

today=$(date -u +%Y%m%d)
if [ "$today" -gt "$LAST_RUN_DATE" ]; then
  echo "$(date -u '+%F %H:%MZ') Alaska forecasting is over ($LAST_RUN_DATE); removing $LABEL"
  launchctl disable "gui/$(id -u)/$LABEL"
  launchctl bootout "gui/$(id -u)/$LABEL"
  exit 0
fi

LOCK="/tmp/hrrrak-$(id -u).lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "$(date -u '+%F %H:%MZ') another HRRR-AK run is in progress, skipping"
  exit 0
fi
trap 'rmdir "$LOCK"' EXIT

FILTER="Warning|create_collection|logic = df"
cd "$DIR" || exit 1
"$PY" -W ignore hrrrak_loop.py "$@" 2>&1 | grep -v -E "$FILTER"
rc=${PIPESTATUS[0]}

# Scheduled runs (no arguments) also compare GOES-18 clouds with HRRR-AK for the hours that
# have verified since the last firing, for every run made in the last 48 h (goes_vs_hrrr.py
# skips frames it already made and rebuilds each run's MP4). Manual calls with arguments don't.
if [ $# -eq 0 ]; then
  "$PY" -W ignore goes_vs_hrrr.py 2>&1 | grep -v -E "$FILTER"
  [ "${PIPESTATUS[0]}" -ne 0 ] && rc=1
fi
exit "$rc"
