#!/bin/bash
# Schedule the WxChallenge forecast on this Mac with launchd (macOS's built-in scheduler).
#
#   ./install_schedule.sh                 install: every 30 min from 8:00 am, then every 12 min
#                                         from 3:00 pm to the 00Z forecast cutoff
#   ./install_schedule.sh --start 7 --end 17 --every 20 --minute 5 --late-start 14 --late-every 10
#   ./install_schedule.sh --status        is it loaded, when did it last run
#   ./install_schedule.sh --run-now       start one run right away (to test)
#   ./install_schedule.sh --uninstall     remove the schedule
#
# Log: ~/Library/Logs/wxchallenge.log
#
# Notes
#  * Times are the Mac's local time, so the schedule follows daylight saving on its own.
#  * If the laptop is asleep at a scheduled time, launchd runs the job once when it wakes
#    (missed runs are merged into one, not replayed one by one).
#  * Model runs already downloaded are reused (weather-forecasts/cache), so frequent runs
#    only download what is new.
#  * Cutoff: WxChallenge forecasts are due at 00Z (6 pm MDT, 5 pm MST). Slots run through
#    --end local time (default 17:48), and each run first checks the UTC clock and skips
#    itself once 00Z has passed, so the schedule stays correct across the DST change
#    without reinstalling.

set -euo pipefail

LABEL="com.jglarson.wxchallenge"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"          # .../weather-forecasts
RUNNER="$DIR/getForecast_wxChallenge.sh"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/wxchallenge.log"
DOMAIN="gui/$(id -u)"
START=8; END=17; MINUTE=0; EVERY=30   # 8:00, 8:30, ... 14:30
LATE_START=15; LATE_EVERY=12           # then 15:00, 15:12, ... 17:48; runs after 00Z skip themselves

case "${1:-}" in
  --uninstall)
    launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
    rm -f "$PLIST"
    echo "Schedule removed."
    exit 0 ;;
  --status)
    if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
      launchctl print "$DOMAIN/$LABEL" | grep -E "state|last exit code|runs" || true
      echo "Log: $LOG"; [ -f "$LOG" ] && { echo "--- last lines ---"; tail -n 15 "$LOG"; }
    else
      echo "Not installed."
    fi
    exit 0 ;;
  --run-now)
    launchctl kickstart "$DOMAIN/$LABEL"
    echo "Started. Follow it with:  tail -f $LOG"
    exit 0 ;;
esac

while [ $# -gt 0 ]; do
  case "$1" in
    --start)  START="$2"; shift 2 ;;
    --end)    END="$2"; shift 2 ;;
    --minute) MINUTE="$2"; shift 2 ;;
    --every)  EVERY="$2"; shift 2 ;;
    --late-start) LATE_START="$2"; shift 2 ;;
    --late-every) LATE_EVERY="$2"; shift 2 ;;
    *) echo "Unknown option $1"; exit 1 ;;
  esac
done

[ -x "$RUNNER" ] || chmod +x "$RUNNER"

# launchd starts jobs with a bare PATH: record where conda and gh (git's GitHub login)
# live now, while this terminal has them.
EXTRA_PATH=""
for tool in conda gh git; do
  p="$(command -v "$tool" 2>/dev/null || true)"
  [ -n "$p" ] && EXTRA_PATH="$EXTRA_PATH:$(dirname "$p")"
done
if [ -z "$(command -v conda 2>/dev/null || true)" ] && [ -n "${CONDA_EXE:-}" ]; then
  EXTRA_PATH="$EXTRA_PATH:$(dirname "$CONDA_EXE")"
fi
PATH_FOR_JOB="${EXTRA_PATH#:}:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Slots in minutes after midnight: every EVERY min until LATE_START, then every LATE_EVERY
# min through the END hour.
intervals=""
nslots=0
last=0
t=$((START * 60 + MINUTE))
while [ "$t" -le $((END * 60 + 59)) ]; do
  intervals+="    <dict><key>Hour</key><integer>$((t / 60))</integer><key>Minute</key><integer>$((t % 60))</integer></dict>
"
  nslots=$((nslots + 1)); last=$t
  if [ $((t + EVERY)) -lt $((LATE_START * 60 + MINUTE)) ]; then
    t=$((t + EVERY))
  elif [ "$t" -lt $((LATE_START * 60 + MINUTE)) ]; then
    t=$((LATE_START * 60 + MINUTE))
  else
    t=$((t + LATE_EVERY))
  fi
done

# Skip the run once the 00Z deadline has passed (UTC hour 00-11 = evening/night in the US).
GUARD='h=$(date -u +%H); if [ "$h" -ge 12 ]; then exec /bin/bash "$0"; else echo "$(date): past the 00Z forecast cutoff, skipping"; fi'

mkdir -p "$(dirname "$PLIST")" "$(dirname "$LOG")"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>$GUARD</string>
    <string>$RUNNER</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>$PATH_FOR_JOB</string>
    <key>HOME</key><string>$HOME</string>
  </dict>
  <key>StartCalendarInterval</key>
  <array>
$intervals  </array>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
  <key>ProcessType</key><string>Background</string>
</dict>
</plist>
EOF

plutil -lint "$PLIST" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"

printf "Installed: %d runs, every %d min from %d:%02d, every %d min from %d:%02d until the 00Z cutoff (last slot %d:%02d local).\n" \
  "$nslots" "$EVERY" "$START" "$MINUTE" "$LATE_EVERY" "$LATE_START" "$MINUTE" "$((last / 60))" "$((last % 60))"
echo "PATH for the job: $PATH_FOR_JOB"
echo "Log:              $LOG"
echo
echo "Test it now with:   $0 --run-now   then   tail -f $LOG"
echo "If the log says 'Operation not permitted', macOS is blocking background access to"
echo "Documents: System Settings > Privacy & Security > Full Disk Access > add /bin/bash."
