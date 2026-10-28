#!/bin/bash
# Schedule the WxChallenge deadline reminder (wxc_push.py send) with launchd.
#
#   ./install_wxc_reminder.sh              install
#   ./install_wxc_reminder.sh --status     loaded? last lines of the log
#   ./install_wxc_reminder.sh --uninstall  remove
#
# 22Z is 4 pm CST / 5 pm CDT, so the job starts at both 16:00 and 17:00 Mac local time on
# Sunday-Wednesday (the evenings before the Mon-Thu forecast days); wxc_push.py sends only
# between 21:50Z and 23:30Z and once per UTC day, so exactly one of the two sends.
# If the laptop is asleep at a slot, launchd runs it once on wake (still sent if inside the window).
# Log: ~/Library/Logs/wxc-reminder.log.

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY=/opt/homebrew/Caskroom/miniforge/base/envs/wxchallenge/bin/python
LOG="$HOME/Library/Logs/wxc-reminder.log"
DOMAIN="gui/$(id -u)"
LABEL=com.jglarson.wxc-reminder
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

case "${1:-}" in
  --uninstall)
    launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true; rm -f "$PLIST"
    echo "Reminder schedule removed."; exit 0 ;;
  --status)
    if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then echo "$LABEL: loaded"; launchctl print "$DOMAIN/$LABEL" | grep -E "last exit code|runs" || true
    else echo "$LABEL: not installed"; fi
    [ -f "$LOG" ] && { echo "--- last lines of $LOG ---"; tail -n 10 "$LOG"; }
    exit 0 ;;
esac

slots=""
for wd in 0 1 2 3; do for h in 16 17; do        # launchd weekdays: 0 = Sunday
  slots+="    <dict><key>Weekday</key><integer>$wd</integer><key>Hour</key><integer>$h</integer><key>Minute</key><integer>0</integer></dict>
"; done; done

mkdir -p "$(dirname "$PLIST")" "$(dirname "$LOG")"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PY</string>
    <string>$DIR/wxc_push.py</string>
    <string>send</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>StartCalendarInterval</key>
  <array>
$slots  </array>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
EOF
plutil -lint "$PLIST" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"
echo "Installed $LABEL: Sun-Wed at 16:00 and 17:00 local (sends at 22Z). Log: $LOG"
