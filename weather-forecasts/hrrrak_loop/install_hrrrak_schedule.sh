#!/bin/bash
# Installs / reloads the launchd job com.jglarson.hrrrak.
# HRRR-AK posts f045 of the 12Z run by ~13:25Z and f039 of the 18Z run by ~19:20Z (AWS), so
# the job fires at 13:40Z and 19:40Z, with a retry an hour later (runs already made are skipped).
# Times are converted to this Mac's local time when you run this; re-run after a DST change.
LABEL=com.jglarson.hrrrak
DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
UTC_TIMES="13:40 14:40 19:40 20:40"

entries=""
for t in $UTC_TIMES; do
  local_t=$(date -j -u -f "%H:%M" "$t" +%s | xargs -I{} date -r {} +%H:%M)
  h=$((10#${local_t%:*})); m=$((10#${local_t#*:}))
  entries+="    <dict><key>Hour</key><integer>$h</integer><key>Minute</key><integer>$m</integer></dict>"$'\n'
  echo "  ${t}Z -> $local_t local"
done

cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$DIR/run_hrrrak_loop.sh</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>/opt/homebrew/Caskroom/miniforge/base/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>HOME</key><string>$HOME</string>
  </dict>
  <key>StartCalendarInterval</key>
  <array>
$entries  </array>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/hrrrak_loop.log</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/hrrrak_loop.log</string>
  <key>ProcessType</key><string>Background</string>
</dict>
</plist>
PL

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null
launchctl enable "gui/$(id -u)/$LABEL"
launchctl bootstrap "gui/$(id -u)" "$PLIST" && echo "loaded $LABEL ($PLIST)"
