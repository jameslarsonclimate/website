"""The page's scrollable timeline (wxc_timeline.py): per-day files and the bundle."""
import importlib
import json
import types
from datetime import date, datetime, timezone

import numpy as np
import pandas as pd

import wxc_timeline as tl

NOW = datetime(2026, 10, 15, 18, 0, tzinfo=timezone.utc)      # today = Oct 15, forecasting Oct 16


def _series(data, day, kind, models, hindcast=False):
    p = data / "series" / f"KOLM_{day}_{kind}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"station": "KOLM", "target_date": day, "kind": kind, "hindcast": hindcast,
                             "generated_at_utc": "x", "models": models}))


def _hrrr(day, init, base=50.0):
    t0 = pd.Timestamp(f"{day} 06:00")
    times = [(t0 + pd.Timedelta(hours=h)).strftime("%Y-%m-%dT%H:%M") for h in range(25)]
    return {"init_time_utc": init, "tmax_f": base + 12, "tmin_f": base, "times": times,
            "temp_f": [base + h / 2 for h in range(25)], "wind_kt": [3.0] * 25, "precip_in": [0.0] * 25}


def test_timeline_days_fill_gaps_and_cap(tmp_path, monkeypatch):
    for d in ["2026-10-12", "2026-10-13", "2026-10-15", "2026-10-16"]:      # Oct 14 missed (offline)
        _series(tmp_path, d, "submitted", {})
    _series(tmp_path, "2026-10-16", "latest", {})                          # other kinds don't count
    (tmp_path / "series" / "KTPA_2026-10-11_submitted.json").write_text("{}")   # another city
    days = tl.timeline_days(tmp_path, "KOLM")
    assert days == [date(2026, 10, d) for d in range(12, 17)]
    monkeypatch.setattr(tl, "MAX_DAYS", 3)
    assert tl.timeline_days(tmp_path, "kolm") == [date(2026, 10, 15), date(2026, 10, 16)]   # 14th: no series
    assert tl.timeline_days(tmp_path, "KXXX") == []
    monkeypatch.setattr(tl, "MAX_DAYS", 35)
    # the scoreboard's period start cuts off an earlier visit to the same station
    _series(tmp_path, "2026-09-20", "submitted", {})
    assert tl.timeline_days(tmp_path, "KOLM")[0] == date(2026, 9, 20)
    assert tl.timeline_days(tmp_path, "KOLM", since="2026-10-13")[0] == date(2026, 10, 13)
    assert tl.timeline_days(tmp_path, "KOLM", since="2026-10-01")[0] == date(2026, 10, 12)


def test_save_hindcast_series(tmp_path, monkeypatch):
    """A hindcast's hourly series becomes the day's 'submitted' series (with the ensembles'
    10-90% range when there is one), merged with an earlier hindcast, never over a live one."""
    m = importlib.import_module("getForecast_wxChallenge-pushGitHub")
    monkeypatch.setattr(m.wxc_verify, "SERIES_DIR", tmp_path / "series")
    st, d = types.SimpleNamespace(icao="KOLM"), date(2026, 10, 1)
    as_of = datetime(2026, 9, 30, 23, tzinfo=timezone.utc)
    times = pd.date_range("2026-10-01 06:00", periods=3, freq="12h")

    def grib(init):
        return {"metrics": {"init_time_utc": init, "tmax_f": 60.0, "tmin_f": 40.0},
                "series": {"times": times, "temp_f": np.array([40.0, 60.0, 45.0]),
                           "wind_kt": np.array([1.0, 2.0, 3.0]), "precip_in": np.zeros(3)}}
    ens = {"init_time_utc": "2026-09-30T12", "tmax_f": 61, "tmin_f": 41,
           "series": {"times": ["2026-10-01T06:00", "2026-10-01T18:00"], "tmp_f": [41, 61], "wsp_kt": [2, 3],
                      "precip_cum_in": [0, 0.1], "tmp_p10": [39, 58], "tmp_p90": [43, 64]}}
    rec = json.loads(m.save_hindcast_series(st, d, as_of, {"HRRR": grib("2026-09-30T18")}, {"ENS": ens}).read_text())
    assert rec["hindcast"] is True and rec["kind"] == "submitted" and rec["generated_at_utc"] == as_of.isoformat()
    assert rec["models"]["HRRR"]["temp_f"] == [40.0, 60.0, 45.0] and rec["models"]["HRRR"]["init_time_utc"] == "2026-09-30T18"
    assert rec["models"]["ENS"]["temp_p10"] == [39, 58] and rec["models"]["ENS"]["temp_p90"] == [43, 64]
    # a second hindcast of the day (a model that failed the first time) keeps the others
    rec = json.loads(m.save_hindcast_series(st, d, as_of, {"IFS": grib("2026-09-30T12")}, {}).read_text())
    assert set(rec["models"]) == {"HRRR", "IFS", "ENS"}
    assert m.save_hindcast_series(st, d, as_of, {}, {}) is None              # nothing fetched
    m.wxc_verify.save_series("KOLM", d, "submitted", "2026-09-30T23:50:00+00:00", {"GFS": {}})
    assert m.save_hindcast_series(st, d, as_of, {"HRRR": grib("2026-09-30T18")}, {}) is None   # live series stays
    assert set(m.wxc_verify.load_series("KOLM", d, "submitted")["models"]) == {"GFS"}


def test_day_reports_and_obs_record():
    raw = pd.DataFrame({"valid": ["2026-10-14 06:00", "2026-10-14 06:53", "2026-10-15 05:53",
                                  "2026-10-15 06:00", "2026-10-15 06:53"]})
    part = tl.day_reports(raw, date(2026, 10, 14))
    assert list(part["valid"]) == ["2026-10-14 06:53", "2026-10-15 05:53", "2026-10-15 06:00"]

    reports = pd.DataFrame({"valid": pd.to_datetime(["2026-10-14 06:53", "2026-10-14 07:10"], utc=True),
                            "temp_f": [44.06, float("nan")], "wind_kt": [3.0, 5.0], "gust_kt": [None, 12.0],
                            "max6_f": [None, None], "min6_f": [None, None],
                            "precip_total_in": [0.0, 0.02], "routine": [True, False]})
    sky = pd.DataFrame({"valid": pd.to_datetime(["2026-10-14 06:53"], utc=True), "sky_pct": [100.0], "clear": [False]})
    goes = [{"hour": "2026-10-14T06:00", "cloud_pct": 87.4}, {"hour": "2026-10-14T07:00", "cloud_pct": None}]
    rec = tl.obs_record("kolm", date(2026, 10, 14), reports, sky, goes, NOW, complete=True)
    assert rec["station"] == "KOLM" and rec["complete"] is True
    r = rec["reports"]
    assert r["times"] == ["2026-10-14T06:53", "2026-10-14T07:10"]
    assert r["temp_f"] == [44.1, None] and r["gust_kt"] == [None, 12] and r["precip_in"] == [0.0, 0.02]
    assert r["routine"] == [True, False]
    assert rec["sky"] == {"times": ["2026-10-14T06:53"], "pct": [100], "clear": [False]}
    assert rec["goes"] == {"times": ["2026-10-14T06:00"], "pct": [87]}
    json.dumps(rec, allow_nan=False)                     # no NaN reaches the file
    bare = tl.obs_record("KOLM", date(2026, 10, 14), None, None, None, NOW, complete=False)
    assert set(bare) == {"station", "date", "generated_at_utc", "complete"}


def test_is_final():
    d = date(2026, 10, 14)
    assert not tl.is_final(d, datetime(2026, 10, 15, 6, 30, tzinfo=timezone.utc))
    assert tl.is_final(d, datetime(2026, 10, 15, 7, 0, tzinfo=timezone.utc))


def test_build_bundle(tmp_path):
    ens = {"init_time_utc": "2026-10-14T06", "tmax_f": 70, "tmin_f": 48,
           "times": ["2026-10-15T00:00", "2026-10-15T06:00", "2026-10-15T18:00", "2026-10-16T06:00"],
           "temp_f": [60, 50, 66, 52], "wind_kt": [2, 3, 4, 5], "precip_in": [0, 0, 0.01, 0.02],
           "temp_p10": [58, 48, 63, 50], "temp_p90": [62, 52, 69, 54]}
    mos = {"init_time_utc": "2026-10-14T18", "tmax_f": 71, "tmin_f": 47,
           "times": ["2026-10-15T06:00", "2026-10-15T18:00"], "temp_f": [49, 65], "wind_kt": [0, 4], "precip_in": None}
    _series(tmp_path, "2026-10-14", "submitted", {"HRRR": _hrrr("2026-10-14", "2026-10-13T18")}, hindcast=True)
    _series(tmp_path, "2026-10-15", "submitted", {"HRRR": _hrrr("2026-10-15", "2026-10-14T18"), "ENS": ens,
                                                  "GFS_MOS": mos})
    _series(tmp_path, "2026-10-15", "latest", {"HRRR": _hrrr("2026-10-15", "2026-10-15T12", 52),
                                               "RRFS": _hrrr("2026-10-15", "2026-10-15T12", 53)})
    _series(tmp_path, "2026-10-14", "latest", {"HRRR": _hrrr("2026-10-14", "2026-10-14T12")})
    _series(tmp_path, "2026-10-16", "submitted", {"HRRR": _hrrr("2026-10-16", "2026-10-15T12")})
    cl = {"model": "HRRR", "init_time_utc": "2026-10-14T18", "times": ["2026-10-15T06:00", "2026-10-15T07:00"],
          "cloud_pct": [10.0, None], "step": False}
    tl.save_day(tmp_path, "KOLM", date(2026, 10, 15), "clouds",
                tl.clouds_record("KOLM", date(2026, 10, 15), {"HRRR": cl, "NBM": None},
                                 {"HRRR": {**cl, "init_time_utc": "2026-10-15T12"}}, NOW))
    tl.save_day(tmp_path, "KOLM", date(2026, 10, 15), "obs", {
        "complete": False, "reports": {"times": ["2026-10-15T06:53", "2026-10-15T17:53"], "temp_f": [42.1, 52.0],
                                       "wind_kt": [0, 5], "gust_kt": [None, None], "precip_in": [0, 0],
                                       "routine": [True, True]},
        "goes": {"times": ["2026-10-15T07:00"], "pct": [0]}})
    verif = {"station": "KOLM", "days": [{"date": "2026-10-14", "hindcast": True, "obs_pending": [],
                                          "obs": {"tmax_f": 66, "tmin_f": 44, "wind_max_kt": 9, "precip_in": 0.0},
                                          "models": {"HRRR": {"forecast": {"tmax_f": 66, "tmin_f": 50, "wind_max_kt": 7,
                                                                           "precip_in": 0.0},
                                                              "error": {"tmax_f": 0, "tmin_f": 6, "wind_max_kt": -2,
                                                                        "precip_in": 0.0}, "points": 7.0}}}]}
    today = {"date": "2026-10-15", "through_utc": "2026-10-15T17:53", "obs": {"high": 52.04, "low": 41.0,
                                                                             "wind": 5, "precip": 0.0}}
    (tmp_path / "cloud_context.json").write_text(json.dumps({"stations": {"KOLM": {"2026-10-14": {
        "obs": {"day_pct": 90.4, "night_pct": 88.9, "goes_day_pct": 94.3, "goes_night_pct": None},
        "models": {"HRRR": {"init_time_utc": "2026-10-13T18", "day_pct": 100.0, "night_pct": 48.6,
                            "day_err": 10, "night_err": -40}}}}}}))
    b = tl.build(tmp_path, "KOLM", NOW, verif, today, "Olympia, WA (KOLM)", lat=46.97, lon=-122.90)
    json.dumps(b, allow_nan=False)
    assert b["today"] == "2026-10-15" and b["forecast_day"] == "2026-10-16" and b["now_utc"] == "2026-10-15T18:00"
    days = {d["date"]: d for d in b["days"]}
    assert list(days) == ["2026-10-14", "2026-10-15", "2026-10-16"]

    past = days["2026-10-14"]
    assert past["hindcast"] is True and "latest" not in past and "so_far" not in past   # latest: today only
    assert past["verif"]["obs"] == [66, 44, 9, 0.0]
    assert past["verif"]["models"]["HRRR"] == {"fc": [66, 50, 7, 0.0], "err": [0, 6, -2, 0.0], "points": 7.0}
    # the scoreboard's cloud numbers, and every day's night (06Z to sunrise) and day windows
    assert past["cloud_scores"] == {"obs": [88.9, 90.4], "goes": [None, 94.3],
                                    "models": {"HRRR": [48.6, 100.0, -40, 10]}}
    assert past["cloud_win"] == {"night": [0, 8], "day": [9, 19]}
    assert all("cloud_win" in d for d in b["days"]) and "cloud_scores" not in days["2026-10-15"]

    td = days["2026-10-15"]
    h = td["models"]["HRRR"]
    assert h["init"] == "2026-10-14T18" and h["h"][0] == 0 and h["h"][-1] == 24 and len(h["temp"]) == 25
    e = td["models"]["ENS"]                       # the point before 06Z is dropped
    assert e["h"] == [0, 12, 24] and e["temp"] == [50, 66, 52] and e["p10"] == [48, 63, 54 - 4]
    assert td["models"]["GFS_MOS"]["precip"] is None
    assert h["cloud"] == {"init": "2026-10-14T18", "h": [0], "pct": [10], "step": False}
    assert td["latest"]["HRRR"]["init"] == "2026-10-15T12" and td["latest"]["HRRR"]["cloud"]["h"] == [0]
    assert "RRFS" in td["latest"]                 # every newest run stored, unless the list says otherwise
    only = tl.build(tmp_path, "KOLM", NOW, verif, today, "Olympia, WA (KOLM)", latest_models=["HRRR"])
    assert list({x["date"]: x for x in only["days"]}["2026-10-15"]["latest"]) == ["HRRR"]
    assert td["so_far"] == {"high": 52.0, "low": 41.0, "wind": 5, "precip": 0.0, "through": "2026-10-15T17:53"}
    assert td["obs"]["reports"]["h"] == [0.88, 11.88] and td["obs"]["goes"] == {"h": [1], "pct": [0]}
    assert "verif" not in td and "obs" not in days["2026-10-16"]

    # verification of another city is ignored
    other = tl.build(tmp_path, "KOLM", NOW, {**verif, "station": "KTPA"}, None)
    assert all("verif" not in d and "cloud_win" not in d for d in other["days"])     # no lat/lon: no windows
    assert tl.build(tmp_path, "KXXX", NOW) is None
    p = tl.write(tmp_path, b)
    assert json.loads(p.read_text())["station"] == "KOLM"
