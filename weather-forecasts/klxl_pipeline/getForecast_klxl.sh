#!/bin/bash
# Run one KLXL job in the wxchallenge conda env, then commit and push only KLXL files.
#   ./getForecast_klxl.sh pilot     pilot weather page data (data/klxl/pilot.json), ~20 s
#   ./getForecast_klxl.sh models    model comparison page (klxl_models.py), a few minutes
#   ./getForecast_klxl.sh models --no-push --skip-grib   (extra arguments go to the Python script)
#
# Side project next to the WxChallenge pipeline: its own lock, its own files, and it never
# starts or blocks a WxChallenge run. Before its git step it waits while a WxChallenge run is
# going (reading that job's lock file, never taking it), so the two never use git at once.

set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # .../weather-forecasts/klxl_pipeline
ROOT="$(dirname "$HERE")"                                # .../weather-forecasts
cd "$ROOT"

MODE="${1:-}"; shift || true
case "$MODE" in
  pilot)  SCRIPT="$HERE/klxl_pilot.py"
          PATHS=(data/klxl/pilot.json) ;;
  models) SCRIPT="$HERE/klxl_models.py"
          PATHS=(data/klxl images/klxl/latest.png images/klxl/today.png klxl/models/index.html) ;;
  *) echo "Usage: $0 pilot|models [args]"; exit 1 ;;
esac
PUSH=1
for a in "$@"; do [ "$a" = "--no-push" ] && PUSH=0; done
EXTRA=("$@")
[ "$MODE" = "models" ] && EXTRA+=(--no-push)              # git is done here, not in Python
[ "$MODE" = "pilot" ] && EXTRA=()

# One KLXL job at a time (a pilot run waits for a models run, up to 15 min). Fixed path, as for
# the WxChallenge lock: launchd jobs have no TMPDIR.
LOCK="/tmp/klxl-$(id -u).lock"
WXC_LOCK="/tmp/wxchallenge-$(id -u).lock"
busy() { [ -f "$1" ] && kill -0 "$(cat "$1" 2>/dev/null)" 2>/dev/null; }
for _ in $(seq 1 90); do busy "$LOCK" || break; sleep 10; done
if busy "$LOCK"; then echo "$(date): another KLXL job (pid $(cat "$LOCK")) is still going; skipping $MODE."; exit 0; fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

echo "=== KLXL $MODE: $(date) ==="
if ! command -v conda >/dev/null 2>&1; then
  for base in "$HOME/miniforge3" "$HOME/mambaforge" "$HOME/miniconda3" "$HOME/anaconda3" \
              "/opt/homebrew/Caskroom/miniforge/base" "/opt/miniconda3" "/opt/anaconda3"; do
    if [ -x "$base/bin/conda" ]; then export PATH="$base/bin:$PATH"; break; fi
  done
fi
eval "$(conda shell.bash hook)"
conda activate wxchallenge

if ! python "$SCRIPT" "${EXTRA[@]}"; then
  echo "KLXL $MODE: the Python step failed; nothing pushed."
  exit 1
fi
[ "$PUSH" = 1 ] || { echo "KLXL $MODE: done (not pushed)."; exit 0; }

# ---- git: wait out a WxChallenge run, then commit only this job's files ----
for _ in $(seq 1 90); do busy "$WXC_LOCK" || break; sleep 10; done
if busy "$WXC_LOCK"; then echo "A WxChallenge run is still going after 15 min; KLXL files left for the next run."; exit 0; fi
export GIT_TERMINAL_PROMPT=0
existing=(); for p in "${PATHS[@]}"; do [ -e "$p" ] && existing+=("$p"); done
git add -- "${existing[@]}"
staged=$(git diff --cached --name-only --relative -- "${existing[@]}")
if [ -n "$staged" ]; then
  # shellcheck disable=SC2086
  if ! git commit -q -m "update klxl $MODE: $(date -u +%Y-%m-%dT%H:%M:%SZ)" -- $staged; then
    git reset -q -- "${existing[@]}"          # never leave KLXL files staged for another commit
    echo "KLXL $MODE: git commit failed"; exit 1
  fi
  echo "Git: committed $(echo "$staged" | wc -l | tr -d ' ') KLXL file(s)"
else
  echo "Git: nothing new to commit"
fi
branch=$(git rev-parse --abbrev-ref HEAD)
if git push -q origin "$branch"; then
  echo "Git: pushed (website updates in a minute or two)"
else
  echo "GIT PUSH FAILED: the KLXL pages were not updated; the commit is kept and goes up with the next push."
fi
