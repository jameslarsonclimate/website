"""Offline tests for wxc_carryover (last good forecasts kept when a run can't reach its sources)."""
import json
from datetime import date

import wxc_carryover as co

DAY = date(2026, 10, 14)
NET = ("HTTPSConnectionPool(host='mesonet.agron.iastate.edu', port=443): Max retries exceeded "
       "with url: /api/1/mos.json?station=")


def fc(t, init="2026-10-13T18", **kw):
    return {"tmax_f": t, "tmin_f": 50.0, "wind_max_kt": 8.0, "precip_in": 0.0, "init_time_utc": init, **kw}


def write_prev(tmp_path, models, station="KOLM", day=DAY, gen="2026-10-13T22:28:50+00:00"):
    p = tmp_path / "forecast.json"
    p.write_text(json.dumps({"generated_at_utc": gen, "meta": {"station": station, "target_date": day.isoformat()},
                             "models": models}))
    return p


def test_network_errors_recognised():
    assert co.is_network_error(NET)
    assert co.is_network_error("Open-Meteo meta failed: HTTPSConnectionPool(host='ensemble-api.open-meteo.com', "
                               "port=443): Max retries exceeded with url")
    assert co.is_network_error("USL fetch failed: HTTPConnectionPool(host='www.microclimates.org', port=80): "
                               "Read timed out.")
    assert not co.is_network_error("no NBM QMD cycle covering the day is posted yet")
    assert not co.is_network_error(None)


def test_previous_only_for_same_station_and_day(tmp_path):
    p = write_prev(tmp_path, {"GFS": fc(64.5), "NBM": {"tmax_f": None, "precip_in": None, "error": NET},
                              "CONSENSUS": fc(65.0)})
    prev = co.load_previous(p, "KOLM", DAY)
    assert list(prev) == ["GFS"]                                  # failed and consensus left out
    assert prev["GFS"]["stale"]["fetched_at_utc"] == "2026-10-13T22:28:50+00:00"
    assert co.load_previous(p, "KTPA", DAY) == {}
    assert co.load_previous(p, "KOLM", date(2026, 10, 15)) == {}
    assert co.load_previous(tmp_path / "missing.json", "KOLM", DAY) == {}


def test_failed_models_keep_previous_forecast(tmp_path):
    p = write_prev(tmp_path, {"GFS": fc(64.5, "2026-10-13T12"), "NBM": fc(66.0),
                              "REFS": {"tmax_f": None, "precip_in": 0.0, "precip_only": True,
                                       "init_time_utc": "2026-10-13T18"}})
    failed = {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None, "error": NET}
    results = {"GFS": {"metrics": dict(failed), "series": None}}
    mos = {"NBM": dict(failed), "REFS": {**failed, "error": "no RRFS ensemble cycle covering the day found"},
           "USL": dict(failed)}
    models = {"GFS": results["GFS"]["metrics"], "NBM": dict(failed), "REFS": dict(mos["REFS"]),
              "USL": dict(failed), "HRRR": fc(65.9)}
    series = {"models": {"GFS": {"init_time_utc": "2026-10-13T12", "times": ["2026-10-14T06:00", "2026-10-14T09:00"],
                                 "temp_f": [52.0, 55.0], "wind_kt": [3.0, 4.0], "precip_in": [0.0, 0.0]},
                         "NBM": {"init_time_utc": "2026-10-13T12",          # older run than the kept one
                                 "times": ["2026-10-14T06:00"], "temp_f": [51.0]}}}
    errors = {k: m.get("error") for k, m in models.items() if not co.has_values(m)}
    carried = co.carry_over(results, mos, models, co.load_previous(p, "KOLM", DAY), series, ["GFS", "HRRR"])

    assert sorted(carried) == ["GFS", "NBM", "REFS"]               # USL had nothing to keep
    assert carried["GFS"]["error"] == NET                          # what runs.jsonl records
    assert models["GFS"]["tmax_f"] == 64.5 and models["GFS"]["stale"]["error"] == NET
    assert models["NBM"]["tmax_f"] == 66.0 and models["REFS"]["precip_in"] == 0.0
    assert models["USL"]["error"] == NET and models["HRRR"]["tmax_f"] == 65.9 and "stale" not in models["HRRR"]
    # plotting series restored when it is the same run
    assert list(results["GFS"]["series"]["temp_f"]) == [52.0, 55.0]
    assert mos["NBM"]["series"] is None and mos["NBM"]["tmax_f"] == 66.0

    st = co.run_status(errors, list(carried), "2026-10-14T00:15:00+00:00")
    assert st["ok"] is False and st["connectivity"] is True
    assert st["carried_over"] == ["GFS", "NBM", "REFS"] and "USL" in st["failed"]
    assert "Connectivity issues" in st["message"] and "00:15Z" in st["message"]


def test_carried_value_keeps_original_pull_time(tmp_path):
    first = {"GFS": {**fc(64.5), "stale": {"fetched_at_utc": "2026-10-13T20:00:00+00:00", "error": NET}}}
    p = write_prev(tmp_path, first, gen="2026-10-13T23:00:00+00:00")
    models = {"GFS": {"tmax_f": None, "precip_in": None, "error": "boom"}}
    co.carry_over({}, {}, models, co.load_previous(p, "KOLM", DAY), None, ["GFS"])
    assert models["GFS"]["stale"] == {"fetched_at_utc": "2026-10-13T20:00:00+00:00", "error": "boom"}


def test_status_ok_when_only_unposted_products_missing():
    st = co.run_status({"NBM_QMD": "no NBM QMD cycle covering the day is posted yet"}, [], "2026-10-13T22:00:00+00:00")
    assert st["ok"] is True and "message" not in st
    assert co.run_status({}, [], "2026-10-13T22:00:00+00:00")["ok"] is True
