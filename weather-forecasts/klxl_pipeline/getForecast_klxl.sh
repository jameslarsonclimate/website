#!/bin/bash
# Run the KLXL jobs in the wxchallenge conda env, then commit and push only KLXL files.
#   ./getForecast_klxl.sh all       the scheduled run: pilot, then models (when due, see below),
#                                   then ONE commit and ONE push for both (fewer GitHub Pages deploys)
#   ./getForecast_klxl.sh pilot     pilot weather page data (data/klxl/pilot.json), ~5 s
#   ./getForecast_klxl.sh models    model comparison page (klxl_models.py), ~30 s, more with new GRIBs
#   ./getForecast_klxl.sh models --no-push --skip-grib   (extra arguments go to the models script)
#
# "all" runs the models step only from 7:00 to 17:59 Mac local time and before the 00Z forecast
# cutoff (UTC hour >= 12), as the old separate models job did; outside that it's the pilot only.
#
# Side project next to the WxChallenge pipeline: its own lock, its own files, and it never
# starts or blocks a WxChallenge run. Before its git step it waits while a WxChallenge run is
# going (reading that job's lock file, never taking it), so the two never use git at once.

set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # .../weather-forecasts/klxl_pipeline
ROOT="$(dirname "$HERE")"                                # .../weather-forecasts
cd "$ROOT"

PILOT_PATHS=(data/klxl/pilot.json)
MODELS_PATHS=(data/klxl images/klxl/latest.png images/klxl/today.png klxl/models/index.html)
MODELS_LOCAL_HOURS=(7 17)                                # first and last local hour for "all"

MODE="${1:-}"; shift || true
case "$MODE" in
  pilot|models|all) ;;
  *) echo "Usage: $0 all|pilot|models [args]"; exit 1 ;;
esac
PUSH=1
for a in "$@"; do [ "$a" = "--no-push" ] && PUSH=0; done
EXTRA=("$@")

models_due() {
  local h u
  h=$((10#$(date +%H))); u=$((10#$(date -u +%H)))
  [ "$h" -ge "${MODELS_LOCAL_HOURS[0]}" ] && [ "$h" -le "${MODELS_LOCAL_HOURS[1]}" ] && [ "$u" -ge 12 ]
}
STEPS=()
case "$MODE" in
  pilot)  STEPS=(pilot) ;;
  models) STEPS=(models) ;;
  all)    STEPS=(pilot); models_due && STEPS+=(models) ;;
esac

# One KLXL job at a time (waits for another KLXL run, up to 15 min). Fixed path, as for
# the WxChallenge lock: launchd jobs have no TMPDIR.
LOCK="/tmp/klxl-$(id -u).lock"
WXC_LOCK="/tmp/wxchallenge-$(id -u).lock"
busy() { [ -f "$1" ] && kill -0 "$(cat "$1" 2>/dev/null)" 2>/dev/null; }
for _ in $(seq 1 90); do busy "$LOCK" || break; sleep 10; done
if busy "$LOCK"; then echo "$(date): another KLXL job (pid $(cat "$LOCK")) is still going; skipping $MODE."; exit 0; fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

echo "=== KLXL $MODE (${STEPS[*]}): $(date) ==="
if ! command -v conda >/dev/null 2>&1; then
  for base in "$HOME/miniforge3" "$HOME/mambaforge" "$HOME/miniconda3" "$HOME/anaconda3" \
              "/opt/homebrew/Caskroom/miniforge/base" "/opt/miniconda3" "/opt/anaconda3"; do
    if [ -x "$base/bin/conda" ]; then export PATH="$base/bin:$PATH"; break; fi
  done
fi
eval "$(conda shell.bash hook)"
conda activate wxchallenge

# each step on its own: a failed one leaves its files alone, the other still goes up
PATHS=(); DONE=()
for step in "${STEPS[@]}"; do
  if [ "$step" = pilot ]; then
    ok=0; python "$HERE/klxl_pilot.py" && ok=1
    [ "$ok" = 1 ] && PATHS+=("${PILOT_PATHS[@]}")
  else
    ok=0; python "$HERE/klxl_models.py" "${EXTRA[@]}" --no-push && ok=1   # git is done here, not in Python
    [ "$ok" = 1 ] && PATHS+=("${MODELS_PATHS[@]}")
  fi
  if [ "$ok" = 1 ]; then DONE+=("$step"); else echo "KLXL $step: the Python step failed; its files are not pushed."; fi
done
[ "${#DONE[@]}" -gt 0 ] || exit 1
[ "$PUSH" = 1 ] || { echo "KLXL ${DONE[*]}: done (not pushed)."; exit 0; }

# ---- git: wait out a WxChallenge run, then commit only this run's files, push once ----
for _ in $(seq 1 90); do busy "$WXC_LOCK" || break; sleep 10; done
if busy "$WXC_LOCK"; then echo "A WxChallenge run is still going after 15 min; KLXL files left for the next run."; exit 0; fi
export GIT_TERMINAL_PROMPT=0
existing=(); for p in "${PATHS[@]}"; do [ -e "$p" ] && existing+=("$p"); done
git add -- "${existing[@]}"
staged=$(git diff --cached --name-only --relative -- "${existing[@]}")
if [ -n "$staged" ]; then
  label=$(IFS=+; echo "${DONE[*]}")
  # shellcheck disable=SC2086
  if ! git commit -q -m "update klxl $label: $(date -u +%Y-%m-%dT%H:%M:%SZ)" -- $staged; then
    git reset -q -- "${existing[@]}"          # never leave KLXL files staged for another commit
    echo "KLXL $MODE: git commit failed"; exit 1
  fi
  echo "Git: committed $(echo "$staged" | wc -l | tr -d ' ') KLXL file(s)"
else
  echo "Git: nothing new to commit"
  # an earlier failed push may have left commits behind: send them only if there are any
  [ -z "$(git log --oneline '@{u}..HEAD' 2>/dev/null)" ] && exit 0
fi
branch=$(git rev-parse --abbrev-ref HEAD)
if git push -q origin "$branch"; then
  echo "Git: pushed (website updates in a minute or two)"
else
  echo "GIT PUSH FAILED: the KLXL pages were not updated; the commit is kept and goes up with the next push."
fi
