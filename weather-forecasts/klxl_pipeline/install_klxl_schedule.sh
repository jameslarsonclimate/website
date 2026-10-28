#!/bin/bash
# Schedule the two KLXL jobs with launchd (separate from the WxChallenge job, which is untouched).
#
#   ./install_klxl_schedule.sh              install both
#   ./install_klxl_schedule.sh --status     loaded? last lines of the log
#   ./install_klxl_schedule.sh --run-now    start one run of each now
#   ./install_klxl_schedule.sh --uninstall  remove both
#
#   pilot   every 30 min, all day (:05 and :35)
#   models  every 30 min (:15 and :45) from 7:15 to 17:45 Mac local time; like WxChallenge, a run
#           after the 00Z forecast cutoff skips itself
# Log: ~/Library/Logs/klxl.log. If the laptop is asleep at a slot, launchd runs it once on wake.

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"          # .../klxl_pipeline
RUNNER="$DIR/getForecast_klxl.sh"
LOG="$HOME/Library/Logs/klxl.log"
DOMAIN="gui/$(id -u)"
LABELS=(com.jglarson.klxl-pilot com.jglarson.klxl-models)
plist() { echo "$HOME/Library/LaunchAgents/$1.plist"; }

case "${1:-}" in
  --uninstall)
    for l in "${LABELS[@]}"; do launchctl bootout "$DOMAIN/$l" 2>/dev/null || true; rm -f "$(plist "$l")"; done
    echo "KLXL schedule removed."; exit 0 ;;
  --status)
    for l in "${LABELS[@]}"; do
      if launchctl print "$DOMAIN/$l" >/dev/null 2>&1; then echo "$l: loaded"; launchctl print "$DOMAIN/$l" | grep -E "last exit code|runs" || true
      else echo "$l: not installed"; fi
    done
    [ -f "$LOG" ] && { echo "--- last lines of $LOG ---"; tail -n 15 "$LOG"; }
    exit 0 ;;
  --run-now)
    for l in "${LABELS[@]}"; do launchctl kickstart "$DOMAIN/$l"; done
    echo "Started. Follow with:  tail -f $LOG"; exit 0 ;;
esac

chmod +x "$RUNNER"
EXTRA_PATH=""
for tool in conda gh git; do
  p="$(command -v "$tool" 2>/dev/null || true)"
  [ -n "$p" ] && EXTRA_PATH="$EXTRA_PATH:$(dirname "$p")"
done
PATH_FOR_JOB="${EXTRA_PATH#:}:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

slots_pilot=""
for m in 5 35; do slots_pilot+="    <dict><key>Minute</key><integer>$m</integer></dict>
"; done
slots_models=""
for h in $(seq 7 17); do for m in 15 45; do
  slots_models+="    <dict><key>Hour</key><integer>$h</integer><key>Minute</key><integer>$m</integer></dict>
"; done; done

# models: skip once the 00Z deadline has passed (UTC hour 00-11 = evening/night in the US)
GUARD='h=$(date -u +%H); if [ "$h" -ge 12 ]; then exec /bin/bash "$0" models; else echo "$(date): KLXL models: past the 00Z cutoff, skipping"; fi'

write_plist() {   # label, slots, program arguments (as <string> lines)
  cat > "$(plist "$1")" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$1</string>
  <key>ProgramArguments</key>
  <array>
$3  </array>
  <key>WorkingDirectory</key><string>$(dirname "$DIR")</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>$PATH_FOR_JOB</string>
    <key>HOME</key><string>$HOME</string>
  </dict>
  <key>StartCalendarInterval</key>
  <array>
$2  </array>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
  <key>ProcessType</key><string>Background</string>
</dict>
</plist>
EOF
  plutil -lint "$(plist "$1")" >/dev/null
  launchctl bootout "$DOMAIN/$1" 2>/dev/null || true
  launchctl bootstrap "$DOMAIN" "$(plist "$1")"
}

mkdir -p "$HOME/Library/LaunchAgents" "$(dirname "$LOG")"
write_plist com.jglarson.klxl-pilot "$slots_pilot" "    <string>/bin/bash</string>
    <string>$RUNNER</string>
    <string>pilot</string>
"
write_plist com.jglarson.klxl-models "$slots_models" "    <string>/bin/bash</string>
    <string>-c</string>
    <string>$GUARD</string>
    <string>$RUNNER</string>
"
echo "Installed: KLXL pilot every 30 min (:05, :35), KLXL models :15/:45 from 7:15 to 17:45 until the 00Z cutoff."
echo "Log: $LOG    Status: $0 --status"
