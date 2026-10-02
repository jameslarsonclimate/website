#!/bin/bash
# Build a new WxChallenge city's track record before its first forecast day: hindcasts the
# last DAYS days (model runs available at 23Z the day before each), fetches their observations
# and scores them, so the consensus is bias-corrected and skill-weighted from day one.
#
#   scripts/warm_hindcast.sh ICAO [DAYS]     (default 14; nothing is committed or pushed)
#
# Saved model results are reused (weather-forecasts/cache), so re-running only fetches what is
# missing. Keeps the Mac awake (caffeinate) while it runs. The next scheduled run pushes the result.

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"          # .../weather-forecasts
ICAO="${1:?usage: $0 ICAO [DAYS]}"
DAYS="${2:-14}"
[[ "$DAYS" =~ ^[0-9]+$ ]] || { echo "DAYS must be a whole number, got '$DAYS'"; exit 1; }

# same lock as getForecast_wxChallenge.sh: give up rather than wait if a run is going
LOCK="/tmp/wxchallenge-$(id -u).lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "Another forecast run (pid $(cat "$LOCK")) is going; not starting. Try again once it finishes"
  echo "(follow it with: tail -f ~/Library/Logs/wxchallenge.log)."
  exit 1
fi

# Scheduled runs fire between 12Z and the 00Z cutoff; while this holds the lock they skip themselves.
h=$((10#$(date -u +%H)))
if [ "$h" -ge 12 ]; then
  echo "WARNING: it is ${h}Z, before today's 00Z forecast cutoff. Scheduled runs are skipped while"
  echo "this one holds the lock, so the forecast page won't update until it finishes."
fi

cd "$DIR"
exec caffeinate -i ./getForecast_wxChallenge.sh "$ICAO" --hindcast-days "$DAYS" --no-push
