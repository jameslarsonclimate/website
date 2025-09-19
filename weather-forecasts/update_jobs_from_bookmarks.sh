#!/usr/bin/env bash
set -euo pipefail

# update_jobs_from_bookmarks.sh
# Parse Chrome/Firefox bookmarks HTML and generate jobs.html
# Location: weather-forecasts/data/jobs/JamesJobsBookmarks.html

BOOKMARKS="$(dirname "$0")/data/jobs/JamesJobsBookmarks.html"
# place output in ClimateJobs folder
OUTDIR="$(dirname "$0")/ClimateJobs"
mkdir -p "$OUTDIR"
OUTHTML="$OUTDIR/jobs.html"
TMP="$(mktemp)"

if [[ ! -f "$BOOKMARKS" ]]; then
  echo "Bookmarks file not found: $BOOKMARKS" >&2
  exit 1
fi

# Extract the Jobs folder section: find the H3 that contains "Jobs" and grab its following DL block.
# We use awk to record between the <H3 ...>Jobs</H3> line and the matching </DL>
awk 'BEGIN{ignore=1;depth=0}
     /<H3[^>]*>[[:space:]]*Jobs[[:space:]]*<\/H3>/ {ignore=0; next}
     ignore==0 {
       print
       if (/<DL>/) depth++
       if (/<\/DL>/) { depth--; if (depth<0) exit }
     }' "$BOOKMARKS" > "$TMP" || true

# If the Jobs folder wasn't found, fallback to extracting items under "Jobs" anywhere
if [[ ! -s "$TMP" ]]; then
  grep -A200 "<H3 [^>]*>Jobs<\/H3>" "$BOOKMARKS" | sed -n '1,200p' > "$TMP" || true
fi

# Build minimal HTML page
cat > "$OUTHTML" <<'HTML'
<!doctype html>
<meta charset="utf-8">
<title>Jobs</title>
<style>body{font-family:system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial;max-width:900px;margin:2rem auto;padding:0 1rem}a{color:#0366d6}</style>
<h1>Jobs — Bookmarks</h1>
<ul>
HTML

# From the extracted block, pull <A HREF="...">text</A> lines and create list items
# From the extracted block, pull <A HREF="...">text</A> lines and create list items
# Use perl for robust extraction (portable on macOS)
perl -ne '
  while (/<A [^>]*HREF="([^"]+)"[^>]*>([^<]*)/gi) {
    $h = $1; $t = $2; $t = $h if $t eq "";
    # escape HTML in text minimally
    $t =~ s/&/&amp;/g; $t =~ s/</&lt;/g; $t =~ s/>/&gt;/g;
    print "  <li><a href=\"$h\" target=\"_blank\">$t</a></li>\n";
  }
' "$TMP" >> "$OUTHTML"

cat >> "$OUTHTML" <<'HTML'
</ul>
<footer><p>Generated from bookmarks on: <!-- DATE -->
</p></footer>
HTML

# Insert date
sed -i.bak "s/<!-- DATE -->/$(date -u +'%Y-%m-%d %H:%M UTC')/" "$OUTHTML" && rm -f "$OUTHTML.bak"

echo "Generated $OUTHTML"

# Try to commit and push (fast, simple). Only commit the generated file.
cd "$(dirname "$0")"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # add by relative path from repo root (we are in weather-forecasts)
  RELPATH="$(realpath --relative-to="$(pwd)" "$OUTHTML" 2>/dev/null || printf '%s' "$OUTHTML")"
  git add "$RELPATH" || true
  if ! git diff --staged --quiet -- "$RELPATH"; then
    git commit -m "Update ClimateJobs/jobs.html from bookmarks: $(date -u +%Y-%m-%d)" || true
    git push origin HEAD || true
  else
    echo "No changes to commit for $RELPATH"
  fi
else
  echo "Not a git repo — skipping commit/push"
fi

rm -f "$TMP"
