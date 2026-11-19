"""The Claude forecaster (wxc_claude): as-of inputs never include what came later, records,
deadline handling, and its row in team.json (display only)."""
import json
from datetime import date, datetime, timedelta, timezone

import pytest

import wxc_claude
import wxc_stations
import wxc_team
import wxc_verify

STATION = wxc_stations.Station("PAYA", "Yakutat, AK", 59.5, -139.7, tz="America/Juneau", wfo="AJK")
D = date(2026, 11, 15)
OBS = {"tmax_f": 46, "tmin_f": 38, "wind_max_kt": 10, "precip_in": 0.05}


def _fc(t, **kw):
    return {"tmax_f": t, "tmin_f": t - 8, "wind_max_kt": 10, "precip_in": 0.1,
            "init_time_utc": "2026-11-14T12", **kw}


def _day(d, obs, hind=False):
    return {"date": d, "obs": obs, "hindcast": hind,
            "models": {"GFS": {"forecast": {**obs, "tmax_f": obs["tmax_f"] + 2},
                               "error": {"tmax_f": 2, "tmin_f": 0, "wind_max_kt": 0, "precip_in": 0},
                               "points": 2.0},
                       "CONSENSUS": {"forecast": obs, "error": {v: 0 for v in wxc_verify.VARS}, "points": 0.0}}}


@pytest.fixture
def data(tmp_path, monkeypatch):
    """A small verification.json / runs.jsonl in a temp data dir."""
    dd = tmp_path / "data"
    dd.mkdir()
    days = [_day(f"2026-11-{n:02d}", {**OBS, "tmax_f": 40 + n}) for n in range(8, 16)]
    (dd / "verification.json").write_text(json.dumps(
        {"station": "PAYA", "city_start": "2026-11-10", "period_start": "2026-11-08",
         "half_life_days": wxc_verify.HALF_LIFE_DAYS, "days": days, "summary": {}}))
    runs = [  # before the cutoff, at it, and after it (must be ignored)
        {"generated_at_utc": "2026-11-14T22:48:00+00:00", "station": "PAYA", "target_date": "2026-11-15",
         "models": {"GFS": _fc(47), "CONSENSUS": _fc(46)}},
        {"generated_at_utc": "2026-11-14T23:00:00+00:00", "station": "PAYA", "target_date": "2026-11-15",
         "models": {"HRRR": _fc(45, init_time_utc="2026-11-14T18")}},
        {"generated_at_utc": "2026-11-14T23:48:00+00:00", "station": "PAYA", "target_date": "2026-11-15",
         "models": {"GFS": _fc(99), "LATE": _fc(98)}},
    ]
    (dd / "runs.jsonl").write_text("\n".join(json.dumps(r) for r in runs) + "\n")
    monkeypatch.setattr(wxc_claude, "DATA", dd)
    monkeypatch.setattr(wxc_verify, "RUNS", dd / "runs.jsonl")
    monkeypatch.setattr(wxc_verify, "SERIES_DIR", dd / "series", raising=False)
    monkeypatch.setattr(wxc_verify, "load_series", lambda *a, **k: None)
    return dd


def test_as_of_is_23z_the_day_before():
    assert wxc_claude._as_of(D) == datetime(2026, 11, 14, 23, tzinfo=timezone.utc)


def test_asof_brief_uses_nothing_after_the_cutoff(data):
    text, info = wxc_claude.asof_brief(D, STATION)
    assert info["verified_through"] == "2026-11-13"
    assert "| 11-13 |" in text
    for later in ("11-14", "11-15"):                  # day-1 still running at 23Z; the day itself
        assert f"| {later} " not in text and f"| {later} h" not in text
    assert "99.0" not in text and "LATE" not in text  # the 23:48Z run came after the cutoff
    assert "| HRRR " in text and "| GFS " in text and "**46.0**" in text  # 23:00Z run counts


def test_models_as_of_prefers_live_over_hindcast():
    runs = [{"generated_at_utc": "2026-11-14T20:00:00+00:00", "station": "PAYA", "target_date": "2026-11-15",
             "models": {"GFS": _fc(40)}},
            {"generated_at_utc": "2026-11-14T23:00:00+00:00", "station": "PAYA", "target_date": "2026-11-15",
             "hindcast": True, "models": {"GFS": _fc(50), "IFS": _fc(51)}}]
    m = wxc_claude.models_as_of(runs, "PAYA", "2026-11-15", wxc_claude._as_of(D))
    assert m["GFS"]["tmax_f"] == 40 and m["IFS"]["tmax_f"] == 51


def test_validate_rounds_and_rejects():
    assert wxc_claude.validate({"tmax_f": 45.4, "tmin_f": 37, "wind_max_kt": 12.6, "precip_in": 0.234}) == \
        {"tmax_f": 45, "tmin_f": 37, "wind_max_kt": 13, "precip_in": 0.23}
    with pytest.raises(ValueError):
        wxc_claude.validate({"tmax_f": 30, "tmin_f": 40, "wind_max_kt": 5, "precip_in": 0})


def _fake(fc):
    return lambda prompt, schema, system=None: (
        {"notes": "Yakutat: wet, mild."} if "notes" in schema["properties"]
        else {"reasoning": "r", "summary": "near consensus", **fc, "_meta": {}})


def test_hindcast_record_and_notes_version(data, monkeypatch):
    monkeypatch.setattr(wxc_claude, "fetch_afd", lambda wfo, t: f"AFD at {t:%HZ}")
    wxc_claude.save_notes("PAYA", datetime(2026, 11, 10, 23, tzinfo=timezone.utc), "old notes")
    wxc_claude.save_notes("PAYA", datetime(2026, 11, 20, 23, tzinfo=timezone.utc), "future notes")
    brief, info = wxc_claude.asof_brief(D, STATION)
    rec = wxc_claude.make_forecast(STATION, D, wxc_claude._as_of(D), brief, "hindcast",
                                   call=_fake({"tmax_f": 47, "tmin_f": 38, "wind_max_kt": 11, "precip_in": 0.04}))
    assert rec["hindcast"] and rec["forecast"]["tmax_f"] == 47
    assert rec["notes_version"] == "20261110T2300Z"   # never notes written later
    prompt = (wxc_claude.INPUTS_DIR / "PAYA_2026-11-15_hindcast.md").read_text()
    assert "old notes" in prompt and "future notes" not in prompt and "AFD at 23Z" in prompt
    assert wxc_claude.best_records("PAYA")["2026-11-15"]["kind"] == "hindcast"


def test_live_forecast_after_deadline_is_discarded(data, monkeypatch):
    monkeypatch.setattr(wxc_claude, "fetch_afd", lambda wfo, t: "AFD")
    monkeypatch.setattr(wxc_claude, "_now", lambda: datetime(2026, 11, 15, 0, 5, tzinfo=timezone.utc))
    rec = wxc_claude.make_forecast(STATION, D, wxc_claude._as_of(D), "brief", "live",
                                   call=_fake({"tmax_f": 47, "tmin_f": 38, "wind_max_kt": 11, "precip_in": 0.04}))
    assert rec is None and not wxc_claude.RUNS.exists()


def test_live_beats_hindcast_in_records():
    for kind, t, at in (("hindcast", 40, "2026-11-16T01:00:00+00:00"), ("live", 45, "2026-11-14T23:10:00+00:00"),
                        ("hindcast", 41, "2026-11-17T01:00:00+00:00")):
        wxc_claude._append(wxc_claude.RUNS, {"station": "PAYA", "target_date": "2026-11-15", "kind": kind,
                                             "hindcast": kind != "live", "issued_at_utc": at,
                                             "forecast": {**OBS, "tmax_f": t}})
    assert wxc_claude.best_records("PAYA")["2026-11-15"]["forecast"]["tmax_f"] == 45


def test_team_json_row_live_ranked_hindcast_marked():
    for d, kind, t in (("2026-11-14", "hindcast", 44), ("2026-11-15", "live", 47)):
        wxc_claude._append(wxc_claude.RUNS, {"station": "PAYA", "target_date": d, "kind": kind,
                                             "hindcast": kind != "live", "issued_at_utc": d + "T23:00:00+00:00",
                                             "model": wxc_claude.MODEL, "summary": "s",
                                             "forecast": {**OBS, "tmax_f": t}})
    # a forecast for a day without observations yet must not appear
    wxc_claude._append(wxc_claude.RUNS, {"station": "PAYA", "target_date": "2026-11-16", "kind": "live",
                                         "hindcast": False, "issued_at_utc": "2026-11-15T23:00:00+00:00",
                                         "forecast": OBS})
    verif = {"station": "PAYA", "days": [_day("2026-11-14", OBS), _day("2026-11-15", OBS)]}
    out = wxc_team.scores({"stations": {}}, verif)
    c = out["forecasters"]["Claude"]
    assert c["ai"] and set(c["days"]) == {"2026-11-14", "2026-11-15"}
    assert c["days"]["2026-11-14"]["hindcast"] and not c["days"]["2026-11-15"].get("hindcast")
    assert c["summary"]["n_days"] == 1 and c["summary"]["total_points"] == 1.0      # live only
    assert c["summary_hindcast"]["n_days"] == 1 and c["summary_hindcast"]["total_points"] == 2.0
    assert "2026-11-16" not in json.dumps(out)


def test_late_forecast_counts_as_live(data, monkeypatch):
    monkeypatch.setattr(wxc_claude, "fetch_afd", lambda wfo, t: "AFD")
    monkeypatch.setattr(wxc_claude, "_now", lambda: datetime(2026, 11, 15, 0, 5, tzinfo=timezone.utc))
    rec = wxc_claude.make_forecast(STATION, D, wxc_claude._now(), "brief", "late",
                                   call=_fake({"tmax_f": 47, "tmin_f": 38, "wind_max_kt": 11, "precip_in": 0.04}))
    assert rec["kind"] == "late" and rec["hindcast"] is False


def test_no_claude_row_without_records():
    verif = {"station": "PAYA", "days": [_day("2026-11-14", OBS)]}
    assert "Claude" not in wxc_team.scores({"stations": {}}, verif)["forecasters"]
