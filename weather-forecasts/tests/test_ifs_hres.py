"""IFS HRES 9 km from Open-Meteo's Single Runs API (wxc_ifs_hres.py): faked responses, no network."""
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd
import pytest

import wxc_cache
import wxc_clouds
import wxc_ifs_hres as hr
import wxc_verify
from wxc_stations import STATIONS

ST = STATIONS["KOLM"]
DAY = date(2026, 10, 20)


def single_run(run: str, hours: int = 168, done=None):
    """A fake single-run response for init `run` ("YYYY-MM-DDTHH:00"): temperature 60 at 22Z,
    40 at 10Z, 0.01"/h of rain in the hours ending 12-17Z every day, wind 5 kt but 14 kt at 21Z.
    `done`: only the first `done` hours written (a run still in progress answers with nulls
    after them)."""
    init = pd.Timestamp(run)
    times = pd.date_range(init, periods=hours, freq="h")
    hod = times.hour.values
    temp = 50 + 10 * np.sin(2 * np.pi * (hod - 16) / 24)                # max 60 at 22Z, min 40 at 10Z
    wind = np.where(hod == 21, 14.0, 5.0)
    pcp = np.where((hod >= 12) & (hod <= 17), 0.01, 0.0)
    hourly = {"time": [t.strftime("%Y-%m-%dT%H:%M") for t in times],
              "temperature_2m": [round(float(x), 1) for x in temp],
              "wind_speed_10m": list(map(float, wind)),
              "precipitation": [None] + list(map(float, pcp[1:])),          # hour 0 has no precip
              "dew_point_2m": [45.0] * hours, "relative_humidity_2m": [80.0] * hours,
              "cloud_cover": [float(h * 4 % 100) for h in hod]}
    if done is not None:
        for k in hourly:
            if k != "time":
                hourly[k] = hourly[k][:done] + [None] * (hours - done)
    return {"latitude": ST.lat, "longitude": ST.lon, "hourly": hourly}


class FakeAPI:
    """Stands in for wxc_ifs_hres._get_json; records the runs asked for."""

    def __init__(self, latest="2026-10-19T12:00", runs=None):
        self.latest, self.runs, self.calls = latest, runs or {}, []

    def __call__(self, url, params=None):
        if url == hr.META:
            self.calls.append("meta")
            return {"last_run_initialisation_time": int(pd.Timestamp(self.latest, tz="UTC").timestamp())}
        assert url == hr.API and params["models"] == "ecmwf_ifs"
        assert params["temperature_unit"] == "fahrenheit" and params["wind_speed_unit"] == "kn"
        assert params["precipitation_unit"] == "inch" and params["timezone"] == "GMT"
        assert set(params["hourly"].split(",")) >= {"temperature_2m", "wind_speed_10m", "precipitation",
                                                    "dew_point_2m", "relative_humidity_2m", "cloud_cover"}
        run = params["run"]
        self.calls.append(run)
        r = self.runs.get(run, {})
        if r == "missing":
            raise ValueError(f"Open-Meteo: The requested model run is not available. Run: {run}Z")
        return single_run(run, **r)


@pytest.fixture
def api(monkeypatch):
    fake = FakeAPI()
    monkeypatch.setattr(hr, "_get_json", fake)
    return fake


def test_summary_of_the_06z_06z_day():
    init = datetime(2026, 10, 19, 12)
    res = hr.summarize_run(single_run("2026-10-19T12:00")["hourly"], init, DAY)
    m, s = res["metrics"], res["series"]
    assert m["tmax_f"] == 60.0 and m["tmin_f"] == 40.0 and m["wind_max_kt"] == 14.0
    assert m["precip_in"] == 0.06                       # 12-17Z: six hours of 0.01"
    assert m["init_time_utc"] == "2026-10-19T12" and m["valid_range_utc"] == ["2026-10-20T06", "2026-10-21T06"]
    assert m["n_steps"] == 25
    assert len(s["times"]) == 25 and s["times"][0] == pd.Timestamp("2026-10-20 06:00")
    assert s["precip_in"][0] == 0.0 and s["precip_in"][-1] == pytest.approx(0.06)
    assert np.all(np.diff(s["precip_in"]) >= 0)        # running total since 06Z
    assert list(s["dewpt_f"]) == [45.0] * 25


def test_precip_is_the_24_hours_after_06z():
    """The hour ending 06Z belongs to the day before; the hour ending 06Z the next day counts."""
    raw = single_run("2026-10-19T12:00")["hourly"]
    t = raw["time"]
    p = [0.0] * len(t)
    p[t.index("2026-10-20T06:00")] = 0.50
    p[t.index("2026-10-21T06:00")] = 0.07
    raw["precipitation"] = p
    assert hr.summarize_run(raw, datetime(2026, 10, 19, 12), DAY)["metrics"]["precip_in"] == 0.07


def test_run_still_being_written_is_incomplete():
    raw = single_run("2026-10-19T12:00", done=30)["hourly"]       # through 10/20 17Z only
    with pytest.raises(hr.IncompleteRun):
        hr.summarize_run(raw, datetime(2026, 10, 19, 12), DAY)
    with pytest.raises(ValueError):                                # starts inside the day
        hr.summarize_run(single_run("2026-10-20T12:00")["hourly"], datetime(2026, 10, 20, 12), DAY)


def test_run_choice_live_and_hindcast(api):
    assert hr.init_for(None) == datetime(2026, 10, 19, 12) and api.calls == ["meta"]
    # hindcasts: the newest run out PUBLISH_DELAY_HOURS (8) before as_of; meta.json not asked
    utc = timezone.utc
    assert hr.init_for(datetime(2026, 10, 19, 23, tzinfo=utc)) == datetime(2026, 10, 19, 12)
    assert hr.init_for(datetime(2026, 10, 19, 19, 59, tzinfo=utc)) == datetime(2026, 10, 19, 6)
    assert hr.init_for(datetime(2026, 10, 19, 20, 0, tzinfo=utc)) == datetime(2026, 10, 19, 12)
    assert hr.init_for(datetime(2026, 10, 20, 3, tzinfo=utc)) == datetime(2026, 10, 19, 18)
    assert api.calls == ["meta"]


def test_get_forecast_caches_the_run_and_saves_cloud(api):
    now = datetime(2026, 10, 19, 21, tzinfo=timezone.utc)
    res = hr.get_forecast(ST, DAY, now=now)
    assert res["metrics"]["tmax_f"] == 60.0 and res["metrics"]["init_time_utc"] == "2026-10-19T12"
    assert "not in the consensus" in res["metrics"]["note"]
    assert api.calls == ["meta", "2026-10-19T12:00"]
    assert wxc_cache.load(ST.icao, "IFS_HRES", datetime(2026, 10, 19, 12), DAY) is not None
    cloud = wxc_clouds.load_cloud(ST.icao, "IFS_HRES", datetime(2026, 10, 19, 12))
    assert cloud["model"] == "IFS_HRES" and len(cloud["times"]) == 168 and cloud["step"] is False
    assert cloud["cloud_pct"][cloud["times"].index("2026-10-20T06:00")] == 24.0
    # a later run of the script: from the cache, only meta.json asked
    again = hr.get_forecast(ST, DAY, now=now)
    assert api.calls == ["meta", "2026-10-19T12:00", "meta"]
    assert again["metrics"]["tmax_f"] == 60.0 and list(again["series"]["temp_f"]) == list(res["series"]["temp_f"])
    assert again["metrics"]["note"].count("not in the consensus") == 1


def test_falls_back_to_the_previous_run(api):
    api.latest = "2026-10-19T18:00"
    api.runs = {"2026-10-19T18:00": {"done": 20}}                   # meta ahead of the data: nulls
    res = hr.get_forecast(ST, DAY, now=datetime(2026, 10, 20, 2, tzinfo=timezone.utc))
    assert api.calls == ["meta", "2026-10-19T18:00", "2026-10-19T12:00"]
    assert res["metrics"]["init_time_utc"] == "2026-10-19T12"
    assert "used previous" in res["metrics"]["note"]
    # nothing partial was cached
    assert wxc_cache.load(ST.icao, "IFS_HRES", datetime(2026, 10, 19, 18), DAY) is None


def test_error_entry_when_no_run_can_be_had(api):
    api.runs = {"2026-10-19T12:00": "missing", "2026-10-19T06:00": "missing"}
    res = hr.get_forecast(ST, DAY, as_of=datetime(2026, 10, 19, 23, tzinfo=timezone.utc))
    assert res["series"] is None and res["metrics"]["tmax_f"] is None
    assert "not available" in res["metrics"]["error"]
    assert "meta" not in api.calls                                 # hindcast: no meta.json


def test_meta_failure_is_an_error_entry(monkeypatch):
    def down(url, params=None):
        raise ConnectionError("Max retries exceeded with url: /data/ecmwf_ifs/static/meta.json")
    monkeypatch.setattr(hr, "_get_json", down)
    res = hr.get_forecast(ST, DAY)
    import wxc_carryover
    assert wxc_carryover.is_network_error(res["metrics"]["error"])   # counted as offline, not a failure


def test_hindcast_uses_the_archived_run(api):
    res = hr.get_forecast(ST, DAY, as_of=datetime(2026, 10, 19, 23, tzinfo=timezone.utc))
    assert api.calls == ["2026-10-19T12:00"]
    assert res["metrics"]["init_time_utc"] == "2026-10-19T12"
    assert "STALE" not in (res["metrics"].get("note") or "")


def test_stale_live_run_is_flagged(api):
    api.latest = "2026-10-18T00:00"
    res = hr.get_forecast(ST, DAY, now=datetime(2026, 10, 19, 23, tzinfo=timezone.utc))
    assert "STALE RUN" in res["metrics"]["note"]


def test_fetch_cloud_asks_again_for_an_archived_run(api):
    init = datetime(2026, 10, 1, 0)
    rec = hr.fetch_cloud(ST, "2026-10-01T00")
    assert rec["init_time_utc"] == "2026-10-01T00" and api.calls == ["2026-10-01T00:00"]
    assert hr.fetch_cloud(ST, init) == rec and api.calls == ["2026-10-01T00:00"]     # now from its file


def test_not_in_the_consensus():
    models = {"IFS": {"tmax_f": 60, "tmin_f": 40, "wind_max_kt": 5, "precip_in": 0.1},
              "GFS": {"tmax_f": 62, "tmin_f": 42, "wind_max_kt": 7, "precip_in": 0.2},
              "IFS_HRES": {"tmax_f": 90, "tmin_f": 70, "wind_max_kt": 30, "precip_in": 2.0}}
    c = wxc_verify.consensus(models, {})
    assert c["tmax_f"] == 61 and c["precip_in"] == pytest.approx(0.15)
    assert "IFS_HRES" in wxc_verify.STYLE


def test_main_script_wiring(api, monkeypatch):
    """run_models gives IFS_HRES a GRIB-style result (also with skip_grib, also as a hindcast),
    its series goes into the series files, and hindcasts plan for it."""
    import importlib
    m = importlib.import_module("getForecast_wxChallenge-pushGitHub")
    assert "IFS_HRES" in m.GRIB_ORDER
    pts = pd.DataFrame({"longitude": [ST.lon], "latitude": [ST.lat]})
    as_of = datetime(2026, 10, 19, 23, tzinfo=timezone.utc)
    results, mos, models = m.run_models(ST, DAY, pts, as_of, skip_grib=True, only=["IFS_HRES"])
    assert set(results) == {"IFS_HRES"} and not mos
    assert models["IFS_HRES"]["tmax_f"] == 60.0 and models["IFS_HRES"]["init_time_utc"] == "2026-10-19T12"
    ser = m.collect_series(results, mos)["IFS_HRES"]
    assert len(ser["times"]) == 25 and ser["dewpt_f"] == [45.0] * 25 and ser["precip_in"][-1] == 0.06
    # the rest-of-today runs (partial) leave it out
    assert m.run_models(ST, DAY, pts, None, skip_grib=True, only=["IFS_HRES"], partial=True)[0] == {}
    # hindcast planning: a city's days that never had it get it
    runs = [{"generated_at_utc": "2026-10-19T22:00:00+00:00", "station": "KOLM", "target_date": "2026-10-20",
             "models": {"IFS": {"tmax_f": 60, "tmin_f": 40, "wind_max_kt": 5, "precip_in": 0.0}}}]
    assert wxc_verify.hindcast_plan(runs, "KOLM", "2026-10-20", m.GRIB_ORDER) == \
        [k for k in m.GRIB_ORDER if k != "IFS"]
    # cloud cover: from its file, asked for again when missing
    rec = m.model_cloud(ST, "IFS_HRES", "2026-10-19T12", DAY, pts)
    assert rec["times"][0] == "2026-10-20T06:00" and rec["times"][-1] == "2026-10-21T06:00"
    out = m.collect_clouds(ST, DAY, {"IFS_HRES": "2026-10-19T06"}, pts)
    assert out["IFS_HRES"]["init_time_utc"] == "2026-10-19T06"
    assert m.collect_clouds(ST, DAY, {"IFS_HRES": "2026-10-18T06"}, pts, fetch_grib=False) == {}
