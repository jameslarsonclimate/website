#!/bin/bash
# Schedule the KLXL pages with launchd (separate from the WxChallenge job, which is untouched).
#
#   ./install_klxl_schedule.sh              install (replaces the old separate pilot/models jobs)
#   ./install_klxl_schedule.sh --status     loaded? last lines of the log
#   ./install_klxl_schedule.sh --run-now    start one run now
#   ./install_klxl_schedule.sh --uninstall  remove it
#
# One job, com.jglarson.klxl, once an hour: the pilot page, then the model page (7:00-17:59 local,
# before the 00Z cutoff; getForecast_klxl.sh all), then ONE push for both. Every push to GitHub
# starts a Pages deploy and a new push cancels the one in progress, so KLXL pushes sit as far as
# possible from the WxChallenge runs (:00/:30 from 6:00 to 14:30, every 12 min from 15:00 to 17:48):
#   :15 each hour (15 min from :00 and :30), but :18 at 15:xx and 16:xx (6 min from :12 and :24).
# The schedule is in Mac local time, like the WxChallenge job's, so the spacing holds year-round.
# Log: ~/Library/Logs/klxl.log. If the laptop is asleep at a slot, launchd runs it once on wake.

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"          # .../klxl_pipeline
RUNNER="$DIR/getForecast_klxl.sh"
LOG="$HOME/Library/Logs/klxl.log"
DOMAIN="gui/$(id -u)"
LABEL=com.jglarson.klxl
OLD_LABELS=(com.jglarson.klxl-pilot com.jglarson.klxl-models)    # before 2026-11-10
BUSY_HOURS=(15 16)                                               # WxChallenge every 12 min
plist() { echo "$HOME/Library/LaunchAgents/$1.plist"; }
remove() { launchctl bootout "$DOMAIN/$1" 2>/dev/null || true; launchctl enable "$DOMAIN/$1" 2>/dev/null || true; rm -f "$(plist "$1")"; }

case "${1:-}" in
  --uninstall)
    for l in "$LABEL" "${OLD_LABELS[@]}"; do remove "$l"; done
    echo "KLXL schedule removed."; exit 0 ;;
  --status)
    if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then echo "$LABEL: loaded"; launchctl print "$DOMAIN/$LABEL" | grep -E "last exit code|runs" || true
    else echo "$LABEL: not installed"; fi
    [ -f "$LOG" ] && { echo "--- last lines of $LOG ---"; tail -n 15 "$LOG"; }
    exit 0 ;;
  --run-now)
    launchctl kickstart "$DOMAIN/$LABEL"
    echo "Started. Follow with:  tail -f $LOG"; exit 0 ;;
esac

chmod +x "$RUNNER"
EXTRA_PATH=""
for tool in conda gh git; do
  p="$(command -v "$tool" 2>/dev/null || true)"
  [ -n "$p" ] && EXTRA_PATH="$EXTRA_PATH:$(dirname "$p")"
done
PATH_FOR_JOB="${EXTRA_PATH#:}:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

slots=""
for h in $(seq 0 23); do
  m=15; for b in "${BUSY_HOURS[@]}"; do [ "$h" = "$b" ] && m=18; done
  slots+="    <dict><key>Hour</key><integer>$h</integer><key>Minute</key><integer>$m</integer></dict>
"
done

mkdir -p "$HOME/Library/LaunchAgents" "$(dirname "$LOG")"
for l in "${OLD_LABELS[@]}"; do remove "$l"; done
cat > "$(plist "$LABEL")" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$RUNNER</string>
    <string>all</string>
  </array>
  <key>WorkingDirectory</key><string>$(dirname "$DIR")</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>$PATH_FOR_JOB</string>
    <key>HOME</key><string>$HOME</string>
  </dict>
  <key>StartCalendarInterval</key>
  <array>
$slots  </array>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
  <key>ProcessType</key><string>Background</string>
</dict>
</plist>
EOF
plutil -lint "$(plist "$LABEL")" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl enable "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$(plist "$LABEL")"
echo "Installed: $LABEL hourly at :15 (:18 at ${BUSY_HOURS[*]}h): pilot, then models 7:00-17:59 before 00Z, one push."
echo "Log: $LOG    Status: $0 --status"
