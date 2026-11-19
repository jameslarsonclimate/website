#!/bin/bash
# Schedule the "Claude" WxChallenge forecaster (wxc_claude.py; display only, never submitted).
#
#   ./install_claude_schedule.sh              install
#   ./install_claude_schedule.sh --status     is it loaded, last log lines
#   ./install_claude_schedule.sh --run-now    one `wxc_claude.py auto` now
#   ./install_claude_schedule.sh --uninstall  remove it
#
# Runs for day D at fixed UTC times on D-1: 18Z, 21Z and 23:50Z (11:00, 14:00, 16:50 MST).
# launchd only knows local time, so both the MST and the MDT local times are listed (11:00 12:00
# 14:00 15:00 16:50 17:50); wxc_claude.py checks the UTC clock and runs the newest slot that is
# due and not done yet, so the extra triggers do nothing. A run that starts late (laptop asleep)
# still counts until 00Z; one that finishes after 00Z is thrown away. Each run also hindcasts
# any missed days (a new city: its station study first).
#
# Needs the claude CLI signed in once (see the docstring of wxc_claude.py):
#   "<claude>" auth login          or   "<claude>" setup-token  (then save the token in
#                                        weather-forecasts/claude_forecaster/.oauth_token)
#
# Log: ~/Library/Logs/wxc-claude.log

set -euo pipefail

LABEL="com.jglarson.wxc-claude"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"          # .../weather-forecasts
PY="/opt/homebrew/Caskroom/miniforge/base/envs/wxchallenge/bin/python"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/wxc-claude.log"
DOMAIN="gui/$(id -u)"

case "${1:-}" in
  --uninstall)
    launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
    rm -f "$PLIST"; echo "Schedule removed."; exit 0 ;;
  --status)
    if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
      launchctl print "$DOMAIN/$LABEL" | grep -E "state|last exit code|runs" || true
      echo "Log: $LOG"; [ -f "$LOG" ] && { echo "--- last lines ---"; tail -n 15 "$LOG"; }
    else echo "Not installed."; fi
    exit 0 ;;
  --run-now)
    launchctl kickstart "$DOMAIN/$LABEL"; echo "Started. Follow it with:  tail -f $LOG"; exit 0 ;;
esac

[ -x "$PY" ] || { echo "Python not found: $PY"; exit 1; }

# one run at a time (a hindcast can take most of an hour)
CMD='LOCK=/tmp/wxc-claude-$(id -u).lock; if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK")" 2>/dev/null; then echo "$(date): still running, skip"; exit 0; fi; echo $$ > "$LOCK"; trap "rm -f $LOCK" EXIT; echo "=== $(date -u +%FT%TZ)"; "$0" -u wxc_claude.py auto'

CMD_XML="$(printf '%s' "$CMD" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g')"   # plist is XML

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
    <string>$CMD_XML</string>
    <string>$PY</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>HOME</key><string>$HOME</string>
  </dict>
  <key>StartCalendarInterval</key>
  <array>
    <dict><key>Hour</key><integer>11</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>12</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>14</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>15</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>16</integer><key>Minute</key><integer>50</integer></dict>
    <dict><key>Hour</key><integer>17</integer><key>Minute</key><integer>50</integer></dict>
  </array>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
  <key>ProcessType</key><string>Background</string>
</dict>
</plist>
EOF

plutil -lint "$PLIST" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"
echo "Installed: runs at 18Z, 21Z, 23:50Z (local 11:00/12:00, 14:00/15:00, 16:50/17:50). Log: $LOG"
