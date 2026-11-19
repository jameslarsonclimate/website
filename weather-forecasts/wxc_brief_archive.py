"""
Keep every AI brief (wxc_brief.py) that the pipeline writes, not only the newest.

data/wxchallenge/brief.md is overwritten on every pipeline run. After each run the pipeline
calls archive_brief(), which stores a gzip copy at

    briefs/<ICAO>/<target_date>/<generated, e.g. 20261119T001523Z>.md.gz

The station, target day and generated time come from the brief's own header.

Local only (gitignored, outside data/ so git_push never adds it): every brief.md is already in
git history (each pipeline commit pushes it), so a committed copy would add nothing but size
(~0.5 MB/day gzipped, ~2 MB/day raw, on a site and repo that are already large). A copy is
skipped when it differs from the newest one already archived for that day only in its
Generated line (nothing new came in between runs).

Readers: list_briefs() and brief_as_of(station, target_date, as_of), the newest brief for a
station/target day issued at or before a time (e.g. for a hindcast that uses the real brief
instead of a rebuilt one). scripts/recover_briefs.py filled the archive from git history.
"""

import gzip
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional, Union

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "briefs"

_STATION = re.compile(r"^- Station: \*\*([A-Z0-9]{3,5})\*\*", re.M)
_TARGET = re.compile(r"^- Target day: \*\*(\d{4}-\d{2}-\d{2})\*\*", re.M)
_GENERATED = re.compile(r"^- Generated: (\S+)", re.M)
_STAMP = "%Y%m%dT%H%M%SZ"


def parse_header(text: str) -> tuple:
    """(station, target_date 'YYYY-MM-DD', generated datetime UTC) from a brief's header."""
    head = text[:3000]
    ms, mt, mg = _STATION.search(head), _TARGET.search(head), _GENERATED.search(head)
    if not (ms and mt and mg):
        raise ValueError("brief header lacks Station / Target day / Generated")
    gen = datetime.fromisoformat(mg.group(1).replace("Z", "+00:00"))
    if gen.tzinfo is None:
        gen = gen.replace(tzinfo=timezone.utc)
    return ms.group(1), mt.group(1), gen.astimezone(timezone.utc)


def brief_path(station: str, target_date: str, generated: datetime, root: Optional[Path] = None) -> Path:
    return Path(root or ARCHIVE) / station / target_date / f"{generated.astimezone(timezone.utc):{_STAMP}}.md.gz"


def _body(text: str) -> str:
    """The brief without its Generated line (the only line that changes on every run)."""
    return _GENERATED.sub("", text, count=1)


def _read(path: Path) -> str:
    return gzip.decompress(Path(path).read_bytes()).decode("utf-8")


def list_briefs(station: str, target_date: Union[str, date], root: Optional[Path] = None) -> list:
    """[(generated datetime UTC, path)] for one station/target day, oldest first."""
    d = Path(root or ARCHIVE) / station / str(target_date)
    out = []
    for p in d.glob("*.md.gz") if d.is_dir() else ():
        try:
            out.append((datetime.strptime(p.name[:-6], _STAMP).replace(tzinfo=timezone.utc), p))
        except ValueError:
            continue
    return sorted(out)


def brief_as_of(station: str, target_date: Union[str, date], as_of: Optional[datetime] = None,
                root: Optional[Path] = None) -> Optional[tuple]:
    """(generated datetime, brief text) of the newest archived brief for station/target day
    generated at or before as_of (None: the newest of all), or None if there is none."""
    briefs = list_briefs(station, target_date, root)
    if as_of is not None:
        if as_of.tzinfo is None:
            as_of = as_of.replace(tzinfo=timezone.utc)
        briefs = [b for b in briefs if b[0] <= as_of]
    if not briefs:
        return None
    gen, path = briefs[-1]
    return gen, _read(path)


def archive_text(text: str, root: Optional[Path] = None) -> Optional[Path]:
    """Store one brief; returns its path, or None when skipped (same as the newest earlier copy
    for that day apart from the Generated line, or already archived under that time)."""
    station, target, gen = parse_header(text)
    path = brief_path(station, target, gen, root)
    if path.exists():
        return None
    prev = list_briefs(station, target, root)
    prev = [b for b in prev if b[0] < gen]
    if prev and _body(_read(prev[-1][1])) == _body(text):
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(gzip.compress(text.encode("utf-8"), compresslevel=9, mtime=0))
    tmp.replace(path)
    return path


def archive_brief(brief: Path, root: Optional[Path] = None) -> Optional[Path]:
    """Archive the brief file the pipeline just wrote (data/wxchallenge/brief.md)."""
    return archive_text(Path(brief).read_text(encoding="utf-8"), root)
