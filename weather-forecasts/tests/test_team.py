"""WxChallenge's results.php: official observed values and the team's forecasts (wxc_team)."""
from datetime import datetime, timezone
from pathlib import Path

import pytest

import wxc_team
import wxc_verify
from wxc_verify import score_day

FIX = Path(__file__).parent / "fixtures"
DAY7 = (FIX / "wxc_results_csu_kmsp_day7.html").read_text()
DAY8 = (FIX / "wxc_results_csu_kmsp_day8.html").read_text()
OBS7 = {"tmax_f": 51, "tmin_f": 37, "wind_max_kt": 21, "precip_in": 0.03}   # official, final day 7
NOW = datetime(2026, 11, 6, 15, 30, tzinfo=timezone.utc)


def test_season():
    assert wxc_team.season(NOW.date()) == "26-27"
    assert wxc_team.season(datetime(2027, 3, 1).date()) == "26-27"


def test_results_rows_and_dates():
    r = wxc_team.parse_results(DAY8)
    assert (r["day"], r["status"]) == (8, "As of 15Z")
    d5 = r["dates"][5]
    assert (d5["date"], d5["status"], d5["final"]) == ("2026-11-03", "Final Day 5", True)
    assert d5["obs"] == {"tmax_f": 66, "tmin_f": 53, "wind_max_kt": 15, "precip_in": 0.74}
    assert r["dates"][8]["date"] == "2026-11-06" and not r["dates"][8]["final"]
    assert len(r["forecasters"]) == 8                  # model rows (USL12Z, GFS18Z...) skipped
    k = r["forecasters"]["Kraken"]
    assert k["forecast"] == {"tmax_f": 49, "tmin_f": 33, "wind_max_kt": 6, "precip_in": 0.0}
    assert (k["flag"], k["official"]["penalty"], k["official"]["points"]) == ("G", 5, 19.0)
    assert k["official"]["prev_rank"] == 233


def test_scoring_matches_official_points():
    r = wxc_team.parse_results(DAY7)
    assert r["status"] == "Final Day 7" and len(r["forecasters"]) == 8
    for name, rec in r["forecasters"].items():
        s = wxc_team._score(rec["forecast"], OBS7, rec)
        assert s["points"] == pytest.approx(rec["official"]["points"]), name


# ---- official values replace ours ----
def _ours(day, tmax, src="cli_backup"):
    return {"station": "KMSP", "date": day, "tmax_f": tmax, "tmin_f": 44, "wind_max_kt": 17, "precip_in": 0.14,
            "source": {"tmax_f": src, "tmin_f": "hourly", "wind_max_kt": "cli", "precip_in": "6h_group"},
            "pending": ["wind_max_kt"], "complete": True, "final": False, "obs_method": 2}


OFF = {"obs": {"tmax_f": 56, "tmin_f": 43, "wind_max_kt": 17, "precip_in": 0.14}, "status": "Final Day 1"}


def test_official_override(tmp_path, monkeypatch):
    monkeypatch.setattr(wxc_verify, "OBS", tmp_path / "obs.jsonl")
    wxc_verify.upsert_observations([_ours("2026-10-27", 61)])
    ch = wxc_verify.set_official("KMSP", {"2026-10-27": OFF})
    assert ch == [("2026-10-27", "tmax_f", 61, 56), ("2026-10-27", "tmin_f", 44, 43)]
    r = wxc_verify.read_jsonl(wxc_verify.OBS)[0]
    assert (r["tmax_f"], r["tmin_f"], r["wind_max_kt"]) == (56, 43, 17)
    assert r["source"]["tmax_f"] == "wxc_official" and r["source"]["wind_max_kt"] == "cli"   # same: ours kept
    assert r["own"] == {"tmax_f": 61, "tmin_f": 44} and r["own_source"]["tmax_f"] == "cli_backup"
    assert r["final"] and r["pending"] == []
    assert wxc_verify.set_official("KMSP", {"2026-10-27": OFF}) == []         # applied once only
    # a later fetch of our own values doesn't undo it
    wxc_verify.upsert_observations([_ours("2026-10-27", 60, src="6h_group")])
    r = wxc_verify.read_jsonl(wxc_verify.OBS)[0]
    assert r["tmax_f"] == 56 and r["own"]["tmax_f"] == 60 and r["own_source"]["tmax_f"] == "6h_group"
    assert wxc_verify.obs_is_final(r, True, NOW)
    # and scoring uses the official values, with ours alongside for the page
    d = wxc_verify.scored_days("KMSP", runs=[], obs=wxc_verify.read_jsonl(wxc_verify.OBS))[0]
    assert d["obs"]["tmax_f"] == 56 and d["obs_own"]["tmax_f"] == 60


def test_official_day_we_never_stored(tmp_path, monkeypatch):
    monkeypatch.setattr(wxc_verify, "OBS", tmp_path / "obs.jsonl")
    wxc_verify.set_official("KMSP", {"2026-10-27": OFF})
    r = wxc_verify.read_jsonl(wxc_verify.OBS)[0]
    assert r["tmax_f"] == 56 and set(r["source"].values()) == {"wxc_official"} and "own" not in r


class FakeSession:
    def __init__(self, pages):
        self.pages, self.posts = pages, []

    def post(self, url, headers=None, timeout=None, data=None):
        self.posts.append(data)
        page = self.pages[int(data["day"])]
        return type("R", (), {"text": page, "raise_for_status": lambda self: None})()


def _fake(monkeypatch, tmp_path, pages):
    import requests
    s = FakeSession(pages)
    monkeypatch.setattr(requests, "Session", lambda: s)
    monkeypatch.setattr(wxc_team, "_post", lambda session, year, city, day, school="csu": session.post(
        wxc_team.URL, data={"year": year, "school": school, "city": city, "day": str(day)}).text)
    monkeypatch.setattr(wxc_team.time, "sleep", lambda s: None)
    monkeypatch.setattr(wxc_verify, "OBS", tmp_path / "obs.jsonl")
    return s


def test_update_is_one_request(tmp_path, monkeypatch):
    s = _fake(monkeypatch, tmp_path, {16: DAY8, 7: DAY7})
    raw = {"stations": {"KMSP": {"days": {f"2026-{d}": {"forecasters": {}} for d in
                                          ["10-27", "10-28", "10-29", "10-30", "11-03", "11-04", "11-05"]}}}}
    raw["stations"]["KMSP"]["days"]["2026-11-05"] = {"day": 7, "forecasters": wxc_team.parse_results(DAY7)["forecasters"]}
    wxc_team.RAW.write_text(wxc_verify.dumps(raw))
    wxc_verify.upsert_observations([_ours("2026-10-27", 61)])
    out = wxc_team.update("KMSP", NOW)
    assert [p["day"] for p in s.posts] == ["16"]                 # one POST, no GET
    assert s.posts[0]["year"] == "26-27" and s.posts[0]["city"] == "kmsp"
    assert out["read"] == 1 and ("2026-10-27", "tmax_f", 61, 56) in [c for c in out["changes"]]
    raw = wxc_team.load_raw()
    assert raw["stations"]["KMSP"]["done_for"] == "2026-11-06"   # days 1-7 final: done for today
    assert "2026-11-06" in raw["stations"]["KMSP"]["days"]
    assert raw["stations"]["KMSP"]["days"]["2026-11-05"]["forecasters"]["Kraken"]["official"]["rank"] == 233
    assert wxc_team.update("KMSP", NOW.replace(hour=20)) is None and len(s.posts) == 1


def test_update_catches_up_missed_days(tmp_path, monkeypatch):
    s = _fake(monkeypatch, tmp_path, {16: DAY8, 7: DAY7, **{n: "<h5>Day 1 (x)</h5>" for n in range(1, 7)}})
    wxc_team.update("KMSP", NOW)
    assert [p["day"] for p in s.posts] == ["16", "1", "2", "3", "4", "5", "6", "7"]
    assert "2026-11-05" in wxc_team.load_raw()["stations"]["KMSP"]["days"]


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
    assert w["days"]["2026-11-05"]["points"] == 2.0
    assert w["summary"]["n_days"] == 1 and w["summary"]["total_points"] == 2.0
    k = out["today"]["forecasters"]["Kraken"]
    assert k["penalty"] == 5 and k["flag"] == "G"


def test_check_limit():
    now = datetime(2026, 11, 6, 13, tzinfo=timezone.utc)
    assert wxc_team.due({}, "KMSP", now)
    raw = {"checks": ["2026-11-06T12:30:00+00:00"]}
    assert not wxc_team.due(raw, "KMSP", now)                       # under two hours since
    assert wxc_team.due(raw, "KMSP", now.replace(hour=15))
    raw["checks"] += ["2026-11-06T14:30:00+00:00", "2026-11-06T16:30:00+00:00"]
    assert not wxc_team.due(raw, "KMSP", now.replace(hour=20))      # three checks today
    assert wxc_team.due(raw, "KMSP", datetime(2026, 11, 7, 12, tzinfo=timezone.utc))
    raw = {"stations": {"KMSP": {"done_for": "2026-11-06"}}}
    assert not wxc_team.due(raw, "KMSP", now)                       # yesterday was final: done
