"""Dewpoint for the timeline's dewpoint / RH panels (display only): METARs, MOS, GRIB series,
the backfill of series saved before dewpoints were kept, and the timeline bundle."""
import importlib
import json
import types
from datetime import date, datetime, timezone

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import wxc_mos
import wxc_obs
import wxc_usl
import wxc_timeline as tl

NOW = datetime(2026, 10, 15, 18, 0, tzinfo=timezone.utc)
DAY = date(2026, 10, 14)


@pytest.fixture(scope="module")
def m():
    return importlib.import_module("getForecast_wxChallenge-pushGitHub")


# ----------------------------------------------------------------- METARs
@pytest.mark.parametrize("metar,td_c10", [
    ("KSAV 180453Z AUTO 00000KT 10SM CLR 22/19 A3002 RMK AO2 SLP165 T02220194", 194),   # T group: tenths
    ("KDSM 011153Z 32018G27KT 10SM CLR M05/M12 A3030 RMK AO2 T10501117", -117),         # negative
    ("KXXX 012353Z 00000KT 10SM CLR 20/M01 A3000 RMK AO2", -10),                       # body only
    ("KXXX 012353Z 00000KT 10SM CLR 20/09 A3000 RMK AO2 T0200////", 90),               # T group without dewpoint
    ("KXXX 012353Z 00000KT 10SM CLR 20/ A3000 RMK AO2", None),                          # missing
])
def test_parse_metar_dewpoint(metar, td_c10):
    p = wxc_obs.parse_metar(metar)
    assert p["dewpt_c10"] == td_c10
    assert p["dewpt_f"] == (None if td_c10 is None else pytest.approx(td_c10 / 10 * 1.8 + 32))


def test_parse_metar_temperature_unchanged():
    p = wxc_obs.parse_metar("KSAV 180453Z AUTO 00000KT 10SM CLR 22/19 A3002 RMK AO2 T02220194")
    assert p["temp_c10"] == 222 and p["temp_tgroup"] is True
    p = wxc_obs.parse_metar("KXXX 012353Z 00000KT 10SM CLR M02/M05 A3000 RMK AO2")
    assert p["temp_c10"] == -20 and p["temp_tgroup"] is False


def test_report_series_and_obs_record_keep_dewpoint():
    raw = pd.DataFrame({"valid": ["2026-10-14 06:53", "2026-10-14 07:53"],
                        "metar": ["METAR KOLM 140653Z 00000KT 10SM CLR 07/05 A3000 RMK AO2 T00670050",
                                  "METAR KOLM 140753Z 00000KT 10SM CLR 06/M01 A3000 RMK AO2"],
                        "report_type": [3, 3]})
    rep = wxc_obs.report_series(raw)
    assert rep["dewpt_f"].round(1).tolist() == [41.0, 30.2]
    rec = tl.obs_record("KOLM", DAY, rep, None, None, NOW, complete=True)
    assert rec["reports"]["dewpt_f"] == [41.0, 30.2]
    ob = tl._obs(rec, DAY)
    assert ob["reports"]["td"] == [41.0, 30.2]
    # a record saved before dewpoints were kept
    del rec["reports"]["dewpt_f"]
    assert tl._obs(rec, DAY)["reports"]["td"] is None


# ----------------------------------------------------------------- models
def _mos_rows(dpt=True):
    rows = []
    for i, ft in enumerate(pd.date_range("2026-10-13 18:00", "2026-10-16 00:00", freq="3h")):
        r = {"runtime": "2026-10-13 12:00", "ftime": ft.strftime("%Y-%m-%d %H:%M"), "tmp": 60 + i % 8,
             "wsp": 5, "n_x": None, "q06": 0, "p06": 10}
        if dpt:
            r["dpt"] = 45 + i % 3
        rows.append(r)
    return pd.DataFrame(rows)


def test_summarize_mos_dewpoint():
    s = wxc_mos.summarize_mos(_mos_rows(), DAY, "GFS")["series"]
    assert len(s["dpt_f"]) == len(s["times"]) == 9 and s["dpt_f"][0] == 46.0
    assert wxc_mos.summarize_mos(_mos_rows(dpt=False), DAY, "GFS")["series"]["dpt_f"] is None


def test_usl_dewpoint():
    html = (__import__("pathlib").Path(__file__).parent / "fixtures" / "usl_KTPA_20260928_12.html").read_text(
        encoding="iso-8859-1")
    run = wxc_usl.parse_run(html)
    assert run["dewpt_f"][:2] == [69.0, 69.0]                       # the "Dewpt" column
    s = wxc_usl.summarize_run(run, date(2026, 9, 29))["series"]
    assert len(s["dpt_f"]) == len(s["times"]) and s["dpt_f"][0] == 69.0


def test_collect_series_dewpoint(m):
    times = pd.date_range("2026-10-14 06:00", periods=3, freq="h")
    grib = lambda td: {"metrics": {"init_time_utc": "2026-10-13T18", "tmax_f": 50, "tmin_f": 40},
                       "series": {"times": times, "temp_f": np.array([40.0, 45, 50]), "wind_kt": np.ones(3),
                                  "precip_in": np.zeros(3), "dewpt_f": td}}
    mos = {"init_time_utc": "2026-10-13T12", "tmax_f": 50, "tmin_f": 40,
           "series": {"times": ["2026-10-14T06:00"], "tmp_f": [40.0], "wsp_kt": [3.0], "dpt_f": [38.0]}}
    out = m.collect_series({"HRRR": grib(np.array([38.04, np.nan, 41.0])), "GFS": grib(None)}, {"NBM": mos})
    assert out["HRRR"]["dewpt_f"] == [38.0, None, 41.0]
    assert "dewpt_f" not in out["GFS"]
    assert out["NBM"]["dewpt_f"] == [38.0]


def test_summarize_keeps_failed_dewpoint_as_none(m):
    times = pd.date_range("2026-10-14 06:00", periods=2, freq="h")
    r = m.summarize("HRRR", pd.Timestamp("2026-10-13 18:00"), times, [40, 41], [1, 2], [0, 0])
    assert "dewpt_f" in r["series"] and r["series"]["dewpt_f"] is None     # not asked for again


def _station():
    return types.SimpleNamespace(icao="KOLM", hrrr_model="hrrr", rrfs_domain="conus")


def _fake_herbie(monkeypatch, m, calls, fail=False):
    import herbie

    class FH:
        def __init__(self, inits, fxx, **kw):
            calls.append((inits[0], list(fxx), kw.get("model")))
            self.n = len(fxx)

    def pick(H, search, points, prefer=None):
        if fail:
            raise ValueError("no such field")
        return xr.DataArray(np.full(H.n, 283.15))                       # 50 F
    monkeypatch.setattr(herbie, "FastHerbie", FH)
    monkeypatch.setattr(m, "pick", pick)


def test_add_dewpoint(monkeypatch, m):
    calls = []
    _fake_herbie(monkeypatch, m, calls)
    res = {"metrics": {"init_time_utc": "2026-10-13T18"},
           "series": {"times": pd.date_range("2026-10-14 06:00", periods=3, freq="3h")}}
    assert m.add_dewpoint("GFS", res, None, _station()) is True
    assert calls == [(pd.Timestamp("2026-10-13 18:00"), [12, 15, 18], "gfs")]
    assert res["series"]["dewpt_f"] == pytest.approx([50.0] * 3)
    assert m.add_dewpoint("GFS", res, None, _station()) is False         # already there
    assert m.add_dewpoint("USL", {"series": {"times": []}, "metrics": {}}, None, _station()) is False
    calls.clear()
    _fake_herbie(monkeypatch, m, calls, fail=True)
    res["series"].pop("dewpt_f")
    assert m.add_dewpoint("IFS", res, None, _station()) is True
    assert res["series"]["dewpt_f"] is None                              # tried; never fails the model


def test_series_dewpoints_backfill(tmp_path, monkeypatch, m):
    monkeypatch.setattr(m.wxc_verify, "SERIES_DIR", tmp_path)
    times = [f"2026-10-14T{h:02d}:00" for h in (6, 9, 12)]
    model = lambda init: {"init_time_utc": init, "times": times, "temp_f": [40, 45, 50]}
    models = {"HRRR": model("2026-10-13T18"), "GFS": model("2026-10-13T18"), "GFS_MOS": model("2026-10-13T12"),
              "USL": model("2026-10-13T12"), "ENS": model("2026-10-13T00"),
              "IFS": {**model("2026-10-13T12"), "dewpt_f": [1, 2, 3]}}            # already done
    path = tmp_path / f"KOLM_{DAY}_submitted.json"
    path.write_text(json.dumps({"station": "KOLM", "models": models}))
    # HRRR from the model cache; GFS downloaded (fake); GFS_MOS from IEM (fake)
    cached = {"series": {"times": pd.to_datetime(times), "dewpt_f": np.array([39.0, np.nan, 41.0])}}
    monkeypatch.setattr(m.wxc_cache, "load", lambda st, lab, init, day, partial=False: cached if lab == "HRRR" else None)
    calls = []
    _fake_herbie(monkeypatch, m, calls)
    monkeypatch.setattr(m.wxc_mos, "fetch_mos", lambda st, model, rt: _mos_rows())
    monkeypatch.setattr(m.wxc_usl, "run_dewpoints", lambda icao, init, day: {times[0]: 44.0, times[2]: 47.0})
    assert m.series_dewpoints(_station(), DAY, None) == 4
    got = json.loads(path.read_text())["models"]
    assert got["HRRR"]["dewpt_f"] == [39.0, None, 41.0]
    assert got["GFS"]["dewpt_f"] == [50.0] * 3 and [c[2] for c in calls] == ["gfs"]
    assert got["GFS_MOS"]["dewpt_f"] == [46.0, 47.0, 45.0]
    assert got["USL"]["dewpt_f"] == [44.0, None, 47.0]
    assert "dewpt_f" not in got["ENS"]
    assert got["IFS"]["dewpt_f"] == [1, 2, 3]
    assert m.series_dewpoints(_station(), DAY, None) == 0                    # nothing left to do
    # a MOS run IEM can't give back is marked, not retried
    models["GFS_MOS"].pop("dewpt_f", None)
    path.write_text(json.dumps({"station": "KOLM", "models": {"GFS_MOS": models["GFS_MOS"]}}))
    monkeypatch.setattr(m.wxc_mos, "fetch_mos", lambda *a: (_ for _ in ()).throw(OSError("down")))
    assert m.series_dewpoints(_station(), DAY, None) == 1
    assert json.loads(path.read_text())["models"]["GFS_MOS"]["dewpt_f"] is None


def test_timeline_model_dewpoint():
    times = [f"2026-10-14T{h:02d}:00" for h in (6, 7)]
    rec = {"init_time_utc": "2026-10-13T18", "times": times, "temp_f": [40, 41], "wind_kt": [1, 1],
           "precip_in": [0, 0], "dewpt_f": [38.04, None]}
    assert tl._model(rec, DAY)["td"] == [38.0, None]
    assert "td" not in tl._model({**rec, "dewpt_f": None}, DAY)
    assert "td" not in tl._model({**rec, "dewpt_f": [None, None]}, DAY)
