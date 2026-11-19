"""
Fill the brief archive (wxc_brief_archive.py, briefs/<ICAO>/<day>/<generated>.md.gz) with every
version of data/wxchallenge/brief.md that is still in git history.

Walks `git rev-list HEAD` (which stops quietly at a missing commit instead of failing, as
`git log -- <path>` does), reads each commit's brief blob with one `git cat-file --batch`, and
archives each distinct version. Read-only for git; safe to re-run (existing copies are kept).

    python scripts/recover_briefs.py [--root briefs]
"""

import argparse
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import wxc_brief_archive  # noqa: E402

PATH = "weather-forecasts/data/wxchallenge/brief.md"


def git(*args, input=None):
    return subprocess.run(["git", *args], cwd=wxc_brief_archive.ROOT, input=input,
                          capture_output=True, check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=None, help="archive folder (default: briefs/)")
    args = ap.parse_args()

    revs = git("rev-list", "HEAD")
    commits = revs.stdout.decode().split()
    if revs.returncode:
        print(f"note: rev-list stopped early ({revs.stderr.decode().strip().splitlines()[-1]})")
    # blob id of brief.md in each commit (missing in commits before it existed)
    check = git("cat-file", "--batch-check", input="".join(f"{c}:{PATH}\n" for c in commits).encode())
    blobs = []
    for line in check.stdout.decode().splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[1] == "blob" and parts[0] not in blobs:
            blobs.append(parts[0])
    print(f"{len(commits)} commits walked, {len(blobs)} distinct brief versions")

    out = git("cat-file", "--batch", input="".join(f"{b}\n" for b in blobs).encode()).stdout
    keyed, bad, i = [], 0, 0
    while i < len(out):                       # "<sha> blob <size>\n<content>\n" per blob
        nl = out.index(b"\n", i)
        size = int(out[i:nl].split()[2])
        body, i = out[nl + 1: nl + 1 + size], nl + 1 + size + 1
        try:
            text = body.decode("utf-8")
            keyed.append((wxc_brief_archive.parse_header(text), text))
        except (UnicodeDecodeError, ValueError):
            bad += 1
    # oldest first, so a version that only repeats its predecessor is skipped
    added, days, skipped = Counter(), {}, 0
    for (station, target, gen), text in sorted(keyed, key=lambda k: k[0][2]):
        days.setdefault(station, []).append(gen)
        if wxc_brief_archive.archive_text(text, args.root):
            added[station] += 1
        else:
            skipped += 1
    for st, gens in sorted(days.items()):
        print(f"{st}: {added[st]} archived of {len(gens)}, generated {min(gens):%Y-%m-%d %HZ} "
              f"to {max(gens):%Y-%m-%d %HZ}")
    print(f"skipped (already archived or unchanged): {skipped}; unparseable: {bad}")


if __name__ == "__main__":
    main()
