"""Team forecasters from WxChallenge's results.php (wxc_team; display only)."""
from datetime import datetime, timezone
from pathlib import Path

import pytest

import wxc_team
from wxc_verify import score_day

FIX = Path(__file__).parent / "fixtures"
DAY7 = (FIX / "wxc_results_csu_kmsp_day7.html").read_text()
DAY8 = (FIX / "wxc_results_csu_kmsp_day8.html").read_text()
FORM = (FIX / "wxc_results_form.html").read_text()
OBS7 = {"tmax_f": 51, "tmin_f": 37, "wind_max_kt": 21, "precip_in": 0.03}   # official, final day 7


def test_form_defaults():
    f = wxc_team.parse_form(FORM)
    assert (f["year"], f["city"], f["day"]) == ("26-27", "kmsp", 8)
    assert "kmsp" in f["cities"]


def test_results_rows_and_dates():
    r = wxc_team.parse_results(DAY8)
    assert (r["day"], r["status"]) == (8, "As of 15Z")
    assert r["dates"][5] == {"date": "2026-11-03", "status": "Final Day 5", "final": True}
    assert r["dates"][8]["date"] == "2026-11-06" and not r["dates"][8]["final"]
    assert len(r["forecasters"]) == 8                  # model rows (USL12Z, GFS18Z...) skipped
    k = r["forecasters"]["Kraken"]
    assert k["forecast"] == {"tmax_f": 49, "tmin_f": 33, "wind_max_kt": 6, "precip_in": 0.0}
    assert (k["flag"], k["official"]["penalty"], k["official"]["points"]) == ("G", 5, 19.0)


def test_scoring_matches_official_points():
    r = wxc_team.parse_results(DAY7)
    assert r["status"] == "Final Day 7" and len(r["forecasters"]) == 8
    for name, rec in r["forecasters"].items():
        s = wxc_team._score(rec["forecast"], OBS7, rec)
        assert s["points"] == pytest.approx(rec["official"]["points"]), name


def _verif(days, today=None):
    return {"station": "KMSP", "days": days, "today": today}


def test_scores_for_the_page():
    rec = wxc_team.parse_results(DAY7)["forecasters"]
    raw = {"stations": {"KMSP": {"year": "26-27", "school": "csu", "days": {
        "2026-11-05": {"day": 7, "final": True, "status": "Final Day 7", "forecasters": rec},
        "2026-11-06": {"day": 8, "final": False, "status": "As of 15Z",
                       "forecasters": wxc_team.parse_results(DAY8)["forecasters"]}}}}}
    gfs = score_day({"tmax_f": 50, "tmin_f": 38, "wind_max_kt": 11, "precip_in": 0.01}, OBS7)
    days = [{"date": "2026-11-04", "obs": OBS7, "models": {"GFS": gfs}},       # before the team data
            {"date": "2026-11-05", "obs": OBS7, "models": {"GFS": gfs}}]
    today = {"date": "2026-11-06", "obs": {"tmax_f": 38, "tmin_f": 31, "wind_max_kt": 4, "precip_in": 0.0}}
    out = wxc_team.scores(raw, _verif(days, today))
    w = out["forecasters"]["Wndigo"]
    assert list(w["days"]) == ["2026-11-05"]
    assert w["days"]["2026-11-05"]["points"] == 2.0 == w["days"]["2026-11-05"]["official_points"]
    assert w["summary"]["n_days"] == 1 and w["summary"]["total_points"] == 2.0
    k = out["today"]["forecasters"]["Kraken"]
    assert k["penalty"] == 5 and k["flag"] == "G" and "official_points" not in k
    assert "official_points" not in out["today"]["forecasters"]["Wndigo"]


def test_check_limit():
    now = datetime(2026, 11, 6, 13, tzinfo=timezone.utc)
    assert wxc_team.due({}, "KMSP", now)
    raw = {"checks": ["2026-11-06T12:30:00+00:00"]}
    assert not wxc_team.due(raw, "KMSP", now)                       # under an hour since
    assert wxc_team.due(raw, "KMSP", now.replace(hour=14))
    raw["checks"] += ["2026-11-06T14:00:00+00:00", "2026-11-06T15:00:00+00:00"]
    assert not wxc_team.due(raw, "KMSP", now.replace(hour=20))      # three checks today
    assert wxc_team.due(raw, "KMSP", datetime(2026, 11, 7, 12, tzinfo=timezone.utc))
    raw = {"stations": {"KMSP": {"days": {"2026-11-06": {}}}}}
    assert not wxc_team.due(raw, "KMSP", now)                       # today's table is in
