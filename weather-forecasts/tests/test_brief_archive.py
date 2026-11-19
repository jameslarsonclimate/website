"""Offline tests for the brief archive (wxc_brief_archive)."""
import gzip
from datetime import datetime, timezone

import pytest

import wxc_brief
import wxc_brief_archive as arc


def _brief(gen, extra="", station="PAYA", day="2026-11-20"):
    return (f"# WxChallenge forecast brief: Yakutat, AK ({station})\n\n"
            f"- Station: **{station}**\n"
            f"- Target day: **{day}**, scored over {day}T06Z to ...\n"
            f"- Generated: {gen} (refreshed several times an hour while the forecast job runs)\n\n"
            f"## Body\n\nconsensus 41/33{extra}\n")


def test_parse_header():
    st, day, gen = arc.parse_header(_brief("2026-11-19T00:15:23+00:00"))
    assert (st, day, gen) == ("PAYA", "2026-11-20", datetime(2026, 11, 19, 0, 15, 23, tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        arc.parse_header("# not a brief\n")


def test_archive_keeps_each_version_and_skips_repeats(tmp_path):
    p1 = arc.archive_text(_brief("2026-11-19T18:05:00+00:00"), tmp_path)
    assert p1 == tmp_path / "PAYA" / "2026-11-20" / "20261119T180500Z.md.gz"
    assert gzip.decompress(p1.read_bytes()).decode() == _brief("2026-11-19T18:05:00+00:00")
    # same content, only the Generated line moved on: skipped
    assert arc.archive_text(_brief("2026-11-19T18:20:00+00:00"), tmp_path) is None
    # new content: kept; the same file again: skipped, nothing overwritten
    p2 = arc.archive_text(_brief("2026-11-19T18:35:00+00:00", " new HRRR"), tmp_path)
    assert p2 is not None and p2 != p1
    assert arc.archive_text(_brief("2026-11-19T18:35:00+00:00", " new HRRR"), tmp_path) is None
    assert [g.minute for g, _ in arc.list_briefs("PAYA", "2026-11-20", tmp_path)] == [5, 35]


def test_brief_as_of(tmp_path):
    for t, x in (("18:05", " a"), ("21:10", " b"), ("23:45", " c")):
        arc.archive_text(_brief(f"2026-11-19T{t}:00+00:00", x), tmp_path)
    at = lambda h, m: datetime(2026, 11, 19, h, m, tzinfo=timezone.utc)
    gen, text = arc.brief_as_of("PAYA", "2026-11-20", at(21, 10), tmp_path)
    assert gen == at(21, 10) and text.endswith(" b\n")
    assert arc.brief_as_of("PAYA", "2026-11-20", at(23, 0), tmp_path)[1].endswith(" b\n")
    assert arc.brief_as_of("PAYA", "2026-11-20", None, tmp_path)[1].endswith(" c\n")
    assert arc.brief_as_of("PAYA", "2026-11-20", at(18, 0), tmp_path) is None
    assert arc.brief_as_of("KMSP", "2026-11-20", None, tmp_path) is None


def test_archive_brief_reads_a_real_brief(tmp_path):
    """A brief from wxc_brief.build_brief parses and archives under its own header."""
    from tests.test_brief import NOW, _forecast
    text = wxc_brief.build_brief(_forecast(), {}, None, now=NOW)
    f = tmp_path / "brief.md"
    f.write_text(text)
    p = arc.archive_brief(f, tmp_path / "briefs")
    st, day, gen = arc.parse_header(text)
    assert p == arc.brief_path(st, day, gen, tmp_path / "briefs") and p.exists()
    assert st == "KTPA" and day == "2026-10-07"

