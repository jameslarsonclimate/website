"""
Offline tests for the WxChallenge scripts (no network needed).

    cd weather-forecasts && python -m pytest tests -q
"""
import importlib
import json
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import functions  # noqa: E402
import wxc_mos  # noqa: E402
import wxc_obs  # noqa: E402
import wxc_verify  # noqa: E402
from wxc_stations import STATIONS, default_hrrr_model  # noqa: E402

KSAV = HERE / "fixtures" / "KSAV_routine_20250917_20251001.csv"


# ----------------------------------------------------------------- METARs
def test_parse_metar_groups():
    m = ("KPDX 272353Z 20009KT 8SM RA FEW020 BKN055 OVC080 11/08 A2978 RMK AO2 RAB29 "
         "SLP085 P0001 60002 T01060078 10117 20106 50001")
    p = wxc_obs.parse_metar(m)
    assert p["wind_kt"] == 9
    assert p["temp_f"] == pytest.approx(10.6 * 1.8 + 32)
    assert p["precip_1h"] == 0.01 and p["precip_6grp"] == 0.02
    assert p["max6_f"] == pytest.approx(11.7 * 1.8 + 32)
    assert p["min6_f"] == pytest.approx(10.6 * 1.8 + 32)


def test_parse_metar_negative_and_gust():
    p = wxc_obs.parse_metar("KDSM 011153Z 32018G27KT 10SM CLR M05/M12 A3030 RMK AO2 T10501117 11044 21061")
    assert p["wind_kt"] == 18 and p["gust_kt"] == 27
    assert p["temp_f"] == pytest.approx(-5.0 * 1.8 + 32)
    assert p["max6_f"] == pytest.approx(-4.4 * 1.8 + 32)
    assert p["min6_f"] == pytest.approx(-6.1 * 1.8 + 32)
    # 24-h max/min group (4snTTTsnTTT) must not be mistaken for 6-h groups
    p = wxc_obs.parse_metar("KSAV 180453Z AUTO 00000KT 10SM CLR 22/19 A3002 RMK AO2 SLP165 T02220194 403060172")
    assert p["max6_f"] is None and p["min6_f"] is None


def test_day_label_boundaries():
    t = pd.Timestamp
    assert str(wxc_obs.day_label(t("2025-09-18 05:53", tz="UTC"))) == "2025-09-17"  # 06Z end of 9/17
    assert str(wxc_obs.day_label(t("2025-09-18 06:53", tz="UTC"))) == "2025-09-18"
    assert str(wxc_obs.day_label(t("2025-09-19 05:53", tz="UTC"))) == "2025-09-18"


def test_ksav_daily_summary():
    d = wxc_obs.summarize_metars(pd.read_csv(KSAV)).set_index("date")
    # 9/18: hourly max was 89 F but the 2353Z 6-h max group (10322) shows 90 F
    assert d.loc["2025-09-18", "tmax_f"] == 90
    assert d.loc["2025-09-18", "tmin_f"] == 67        # 1153Z 6-h min group 20194
    # 9/26: specials in the file must not be double counted
    assert d.loc["2025-09-26", "precip_in"] == pytest.approx(0.63)
    assert d.loc["2025-09-26", "precip_6hr_groups_in"] == pytest.approx(0.63)
    assert d.loc["2025-09-26", "wind_max_kt_all_reports"] == 16
    assert bool(d.loc["2025-09-18", "complete"]) and not bool(d.loc["2025-09-17", "complete"])


# ----------------------------------------------------------------- CLI
CLI_TEXT = """
000
CDUS42 KTBW 280634
CLITPA

CLIMATE REPORT
NATIONAL WEATHER SERVICE TAMPA BAY AREA - RUSKIN FL
234 AM EDT MON SEP 28 2026

...THE TAMPA BAY AREA CLIMATE SUMMARY FOR SEPTEMBER 27 2026...
CLIMATE NORMAL PERIOD 1991 TO 2020

TEMPERATURE (F)
 YESTERDAY
  MAXIMUM         83    312 PM  97    1998  89     -6       88
  MINIMUM         65    405 AM  63    1947  74     -9       73

WIND (MPH)
  HIGHEST WIND SPEED    12   HIGHEST WIND DIRECTION     W (270)
  HIGHEST GUST SPEED    22   HIGHEST GUST DIRECTION     W (270)
  AVERAGE WIND SPEED     4.1
\x03
000
CDUS42 KTBW 272034
CLITPA

...THE TAMPA BAY AREA CLIMATE SUMMARY FOR SEPTEMBER 27 2026...
VALID TODAY AS OF 0400 PM LOCAL TIME.

WIND (MPH)
  HIGHEST WIND SPEED    10   HIGHEST WIND DIRECTION     W (270)
"""


def test_parse_cli_prefers_final():
    c = wxc_obs.parse_cli(CLI_TEXT)["2026-09-27"]
    assert c["cli_wind_mph"] == 12 and not c["cli_preliminary"]
    assert c["cli_wind_kt"] == 10              # 12 mph = 10.4 kt
    assert c["cli_tmax_f"] == 83 and c["cli_tmin_f"] == 65


# ----------------------------------------------------------------- MOS
def _mos_rows(model):
    rows = []
    rt = "2026-09-28 12:00"
    for i, ft in enumerate(pd.date_range("2026-09-28 18:00", "2026-10-01 00:00", freq="3h")):
        r = {"runtime": rt, "ftime": ft.strftime("%Y-%m-%d %H:%M"), "tmp": 75 + (i % 8),
             "wsp": 5 + (i % 5), "n_x": None, "txn": None, "q06": None, "p06": None}
        if ft.hour in (0, 6, 12, 18):
            r["q06"] = 3 if model == "NBS" else 1
            r["p06"] = 30
        key = "txn" if model == "NBS" else "n_x"
        if ft == pd.Timestamp("2026-09-29 12:00"):
            r[key] = 70
        if ft == pd.Timestamp("2026-09-30 00:00"):
            r[key] = 90
        rows.append(r)
    return pd.DataFrame(rows)


@pytest.mark.parametrize("model,precip", [("NBS", 0.12), ("GFS", 0.20)])
def test_summarize_mos(model, precip):
    res = wxc_mos.summarize_mos(_mos_rows(model), date(2026, 9, 29), model)
    assert res["tmax_f"] == 90 and res["tmin_f"] == 70
    assert res["wind_max_kt"] == 9
    assert res["precip_in"] == pytest.approx(precip)
    assert res["valid_range_utc"] == ["2026-09-29T06", "2026-09-30T06"]


def test_summarize_mos_short_run():
    df = _mos_rows("NBS")
    df = df[pd.to_datetime(df["ftime"]) < "2026-09-30 00:00"]
    assert "error" in wxc_mos.summarize_mos(df, date(2026, 9, 29), "NBS")


# ----------------------------------------------------------------- scoring
def test_precip_points():
    assert wxc_verify.precip_points(0.0, 0.0) == 0
    assert wxc_verify.precip_points(0.0, 0.12) == pytest.approx(4.6)       # 10*0.4 + 2*0.3
    assert wxc_verify.precip_points(0.60, 0.0) == pytest.approx(4 + 4.5 + 5 + 1)


def test_score_day_and_deadline():
    ob = {"tmax_f": 88, "tmin_f": 72, "wind_max_kt": 10, "precip_in": 0.0}
    fc = {"tmax_f": 86.4, "tmin_f": 73.5, "wind_max_kt": 12.2, "precip_in": 0.02}
    s = wxc_verify.score_day(fc, ob)
    assert s["forecast"] == {"tmax_f": 86, "tmin_f": 74, "wind_max_kt": 12, "precip_in": 0.02}
    assert s["points"] == pytest.approx(2 + 2 + 1 + 0.8)
    runs = [{"station": "KTPA", "target_date": "2026-09-29", "generated_at_utc": t, "models": {}}
            for t in ("2026-09-28T18:55:00+00:00", "2026-09-28T23:10:00+00:00", "2026-09-29T01:00:00+00:00")]
    assert wxc_verify.run_for_day(runs, "KTPA", "2026-09-29")["generated_at_utc"].startswith("2026-09-28T23")


def test_consensus_bias_correction():
    models = {"A": {"tmax_f": 90, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.1},
              "B": {"tmax_f": 86, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0}}
    summary = {n: {"n_days": 3, "bias": {"tmax_f": b, "tmin_f": 0, "wind_max_kt": 0, "precip_in": 0},
                   "mae": {"tmax_f": 1.5, "tmin_f": 1, "wind_max_kt": 1, "precip_in": 0.1}}
               for n, b in (("A", 2.0), ("B", -2.0))}
    c = wxc_verify.consensus(models, summary)
    assert c["tmax_f"] == pytest.approx(88.0)
    assert "bias-corrected" in c["method"]["tmax_f"]["method"]
    c = wxc_verify.consensus(models, {})
    assert c["tmax_f"] == pytest.approx(88.0) and "equal-weight" in c["method"]["tmax_f"]["method"]


def test_consensus_mixed_verified_and_new():
    models = {"A": {"tmax_f": 90, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0},
              "NEW": {"tmax_f": 86, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0}}
    summary = {"A": {"n_days": 4, "bias": {"tmax_f": 2.0, "tmin_f": 0, "wind_max_kt": -4, "precip_in": 0},
                     "mae": {"tmax_f": 2.0, "tmin_f": 1, "wind_max_kt": 4, "precip_in": 0.0}}}
    c = wxc_verify.consensus(models, summary)
    assert c["tmax_f"] == pytest.approx(87.0)                # (88 + 86) / 2 at equal (median) weight
    assert c["wind_max_kt"] == pytest.approx(12.0)           # A corrected up to 14, NEW 10
    assert c["method"]["tmax_f"]["not_yet_verified"] == ["NEW"]


def test_consensus_drops_outliers():
    models = {n: {"tmax_f": t, "tmin_f": 72, "wind_max_kt": 8, "precip_in": 0.0}
              for n, t in (("A", 88), ("B", 87), ("C", 89), ("GFS", 58))}
    c = wxc_verify.consensus(models, {})
    assert c["tmax_f"] == pytest.approx(88.0)
    assert c["method"]["tmax_f"]["excluded_outliers"] == ["GFS"]


def test_forecasts_for_day_per_model_and_hindcast_need():
    ok = {"tmax_f": 88, "tmin_f": 72, "wind_max_kt": 8, "precip_in": 0.0}
    runs = [
        {"station": "KTPA", "target_date": "2026-09-29", "generated_at_utc": "2026-09-28T18:55:00+00:00",
         "models": {"GFS": dict(ok, tmax_f=86), "IFS": ok}},
        {"station": "KTPA", "target_date": "2026-09-29", "generated_at_utc": "2026-09-28T20:55:00+00:00",
         "models": {"GFS": {"tmax_f": None, "error": "x"}, "IFS": dict(ok, tmax_f=90)}},
    ]
    f = wxc_verify.forecasts_for_day(runs, "KTPA", "2026-09-29")
    assert f["GFS"][0]["tmax_f"] == 86 and f["IFS"][0]["tmax_f"] == 90   # GFS from the earlier run
    assert wxc_verify.needs_hindcast(runs, "KTPA", "2026-09-29")          # only 2 models
    assert not wxc_verify.needs_hindcast(runs + [{"station": "KTPA", "target_date": "2026-09-29",
                                                  "generated_at_utc": "2026-09-28T21:00:00+00:00",
                                                  "hindcast": True, "models": {}}], "KTPA", "2026-09-29")
    assert wxc_verify.needs_hindcast(runs, "KTPA", "2026-09-27")


def test_hindcast_plan():
    ok = {"tmax_f": 88, "tmin_f": 72, "wind_max_kt": 8, "precip_in": 0.0}
    allm = ["HRRR", "IFS", "GFS", "NBM"]
    h1 = {"station": "KTPA", "target_date": "2026-09-27", "generated_at_utc": "2026-09-26T21:00:00+00:00",
          "hindcast": True, "models": {"HRRR": ok, "IFS": ok, "GFS": ok, "NBM": {"tmax_f": None, "error": "404"}}}
    assert wxc_verify.hindcast_plan([], "KTPA", "2026-09-27", allm) == allm
    assert wxc_verify.hindcast_plan([h1], "KTPA", "2026-09-27", allm) == ["NBM"]     # retry the gap
    assert wxc_verify.hindcast_plan([h1, dict(h1)], "KTPA", "2026-09-27", allm) == []  # gave up


def test_obs_is_final():
    now = datetime(2026, 9, 28, 20, tzinfo=timezone.utc)
    cli_final = {"date": "2026-09-27", "complete": True, "wind_source": "CLI", "cli_preliminary": False}
    assert wxc_verify.obs_is_final(cli_final, True, now)
    assert not wxc_verify.obs_is_final(dict(cli_final, cli_preliminary=True), True, now)
    assert not wxc_verify.obs_is_final(dict(cli_final, wind_source="METAR (no CLI)"), True, now)
    assert wxc_verify.obs_is_final(dict(cli_final, wind_source="METAR (no CLI)"), False, now)   # e.g. KFNL
    assert wxc_verify.obs_is_final(dict(cli_final, date="2026-09-24", wind_source="METAR"), True, now)  # gave up
    assert not wxc_verify.obs_is_final(None, True, now)


def test_mos_candidate_runtimes():
    t = datetime(2026, 9, 27, 21, tzinfo=timezone.utc)
    assert [x.hour for x in wxc_mos.candidate_runtimes("GFS", t)] == [12, 6, 0]
    assert [x.hour for x in wxc_mos.candidate_runtimes("NAM", t)] == [12, 0, 12]
    assert [x.hour for x in wxc_mos.candidate_runtimes("NBS", t)] == [18, 12, 6]


# ----------------------------------------------------------------- timing
def test_forecast_hours_for_day():
    d = date(2026, 9, 29)
    assert functions.forecast_hours_for_day(pd.Timestamp("2026-09-28 18:00"), d, 1, 48) == (list(range(12, 37)), False)
    fxx, tr = functions.forecast_hours_for_day(pd.Timestamp("2026-09-28 00:00"), d, 1, 48)
    assert fxx[0] == 30 and fxx[-1] == 48 and tr
    assert functions.forecast_hours_for_day(pd.Timestamp("2026-09-28 06:00"), d, 6, 360)[0] == [24, 30, 36, 42, 48]
    assert functions.previous_forecast_cycle(pd.Timestamp("2026-09-28 06:00"), "IFS") == pd.Timestamp("2026-09-28 00:00")


def test_station_registry():
    assert STATIONS["PAJN"].hrrr_model == "hrrrak" and STATIONS["PAJN"].cli_pil == "CLIJNU"
    assert STATIONS["KTPA"].cli_pil == "CLITPA" and STATIONS["KTPA"].hrrr_model == "hrrr"
    assert STATIONS["KFNL"].cli_pil == "" and default_hrrr_model("PHNL") is None


# ----------------------------------------------------------------- GRIB code paths
def _fake_grid_ds(var, fxx, init, values, units):
    """Tiny cfgrib-like dataset (decode_times=False) that real herbie pick_points accepts."""
    lat = np.array([[27.9, 27.9], [28.0, 28.0]])
    lon = np.array([[-82.6, -82.5], [-82.6, -82.5]])
    t0 = pd.Timestamp(init).value // 10**9
    import xarray as xr
    data = np.broadcast_to(np.asarray(values, float)[:, None, None], (len(fxx), 2, 2)).copy()
    ds = xr.Dataset(
        {var: (("step", "y", "x"), data, {"units": units})},
        coords={"latitude": (("y", "x"), lat), "longitude": (("y", "x"), lon),
                "time": t0, "step": np.array(fxx, float) * 3600,
                "valid_time": ("step", t0 + np.array(fxx) * 3600)})
    return ds


class FakeFastHerbie:
    """Maps search strings to fake fields; fails like Herbie on unknown searches."""
    FIELDS = {}

    def __init__(self, dates, model, product, fxx):
        self.init, self.model, self.fxx = pd.Timestamp(dates[0]), model, list(fxx)

    def xarray(self, search, backend_kwargs=None):
        if search not in self.FIELDS:
            raise ValueError(f"no match for {search!r}")
        var, fn, units = self.FIELDS[search]
        return _fake_grid_ds(var, self.fxx, self.init, [fn(f) for f in self.fxx], units)


@pytest.fixture
def fake_herbie(monkeypatch):
    import herbie
    monkeypatch.setattr(herbie, "FastHerbie", FakeFastHerbie)
    K = lambda f: 273.15 + (f - 32) / 1.8  # noqa: E731
    temp = lambda h: K(75 + 10 * np.sin(np.pi * ((h + 18) % 24 - 6) / 12))  # noqa: E731
    FakeFastHerbie.FIELDS = {
        "TMP:2 m above": ("t2m", temp, "K"),
        ":2t:": ("t2m", temp, "K"),
        ":WIND": ("max_10si", lambda h: 5.0, "m s**-1"),
        "APCP": ("tp", lambda h: 0.5 * h, "kg m**-2"),
        ":APCP:surface:0-*": ("tp", lambda h: 0.5 * h, "kg m**-2"),
        ":tp:": ("tp", lambda h: 0.0005 * h, "m"),
        ":10u:": ("u10", lambda h: 3.0, "m s**-1"), ":10v:": ("v10", lambda h: 4.0, "m s**-1"),
        "UGRD:10 m above ground": ("u10", lambda h: 3.0, "m s**-1"),
        "VGRD:10 m above ground": ("v10", lambda h: 4.0, "m s**-1"),
        ":mx2t3:": ("mx2t3", lambda h: K(87.0), "K"), ":mn2t3:": ("mn2t3", lambda h: K(64.0), "K"),
        ":TMAX:2 m above": ("tmax", lambda h: K(86.0), "K"), ":TMIN:2 m above": ("tmin", lambda h: K(66.0), "K"),
    }
    return FakeFastHerbie


def _main_module():
    return importlib.import_module("getForecast_wxChallenge-pushGitHub")


def test_grib_fetchers(fake_herbie):
    m = _main_module()
    st, day = STATIONS["KTPA"], date(2026, 9, 29)
    pts = pd.DataFrame({"longitude": [st.lon], "latitude": [st.lat]})
    init = pd.Timestamp("2026-09-28 12:00")
    ifs = m.fetch_ifs(init, day, pts)["metrics"]
    assert ifs["tmax_f"] == pytest.approx(87.0) and ifs["tmin_f"] == pytest.approx(64.0)
    assert ifs["wind_max_kt"] == pytest.approx(5 * 1.94384, abs=0.1)
    assert ifs["precip_in"] == pytest.approx(0.0005 * 24 * 39.3701, abs=0.01)
    assert ifs["valid_range_utc"] == ["2026-09-29T06", "2026-09-30T06"]
    gfs = m.fetch_gfs(init, day, pts)["metrics"]
    assert gfs["tmax_f"] == pytest.approx(86.0, abs=0.1) or gfs["tmax_f"] > 86
    aifs = m.fetch_aifs(pd.Timestamp("2026-09-28 06:00"), day, pts)["metrics"]
    assert aifs["n_steps"] == 5 and aifs["precip_in"] == pytest.approx(0.5 * 24 * 0.0393701, abs=0.01)
    hrrr = m.fetch_hrrr(pd.Timestamp("2026-09-28 00:00"), day, pts, st)["metrics"]
    assert hrrr["partial_window"] and hrrr["valid_range_utc"][-1] == "2026-09-30T00"


def test_grid_id_and_distance_guard(fake_herbie):
    import xarray as xr
    m = _main_module()
    lat = np.linspace(90, -90, 721)
    g_gfs = xr.Dataset(coords={"latitude": lat, "longitude": np.arange(0, 360, 0.25)})
    g_ifs = xr.Dataset(coords={"latitude": lat, "longitude": np.arange(-180, 180, 0.25)})
    assert m._grid_id(g_gfs) != m._grid_id(g_ifs)       # same shape, different longitudes
    far = pd.DataFrame({"longitude": [-82.55], "latitude": [28.9]})   # ~100 km from the fake grid
    H = FakeFastHerbie([pd.Timestamp("2026-09-28 12:00")], "gfs", "x", [18, 21])
    with pytest.raises(ValueError, match="km away"):
        m.pick(H, ":2t:", far, "t2m")


def test_fallback_to_previous_cycle(fake_herbie, monkeypatch):
    m = _main_module()
    calls = []

    def flaky(init, day, pts, st):
        calls.append(pd.Timestamp(init).hour)
        if len(calls) == 1:
            raise FileNotFoundError("not posted yet")
        return m.fetch_ifs(init, day, pts)
    monkeypatch.setattr(m, "get_latest_forecast_cycle", lambda model, now=None: pd.Timestamp("2026-09-28 18:00"))
    res = m.fetch_with_fallback("IFS", "IFS", flaky, date(2026, 9, 29),
                                pd.DataFrame({"longitude": [-82.5], "latitude": [28.0]}), STATIONS["KTPA"])
    assert calls == [18, 12] and "used previous" in res["metrics"]["note"]


# ----------------------------------------------------------------- end to end
def test_main_end_to_end(tmp_path, monkeypatch, fake_herbie):
    """Full run in a scratch copy with every network call faked."""
    work = tmp_path / "wf"
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns("tests", "__pycache__", "*.ipynb", "images"))
    monkeypatch.syspath_prepend(str(work))
    for name in ["functions", "wxc_obs", "wxc_mos", "wxc_verify", "wxc_stations",
                 "getForecast_wxChallenge-pushGitHub"]:
        sys.modules.pop(name, None)
    import wxc_obs as o, wxc_mos as mo, wxc_verify as v  # noqa: E401
    m = importlib.import_module("getForecast_wxChallenge-pushGitHub")

    # observations: KSAV fixture relabelled as KTPA, "now" = 2025-09-29 20Z
    ks = pd.read_csv(KSAV)[["valid", "metar"]]
    monkeypatch.setattr(o, "fetch_metars", lambda st, a, b: ks)
    monkeypatch.setattr(o, "fetch_cli", lambda pil, limit=30: wxc_obs.parse_cli(
        CLI_TEXT.replace("SEPTEMBER 27 2026", "SEPTEMBER 27 2025")))
    monkeypatch.setattr(mo, "fetch_mos", lambda st, model, runtime=None: _mos_rows(model).assign(
        runtime="2025-09-28 12:00",
        ftime=lambda d: (pd.to_datetime(d["ftime"]) - pd.Timedelta(days=365)).dt.strftime("%Y-%m-%d %H:%M")))
    fixed = datetime(2025, 9, 28, 20, 0, tzinfo=timezone.utc)

    class FixedDT(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed
    monkeypatch.setattr(m, "datetime", FixedDT)
    monkeypatch.setattr(m, "get_latest_forecast_cycle", lambda model, now=None: (
        pd.Timestamp(now or fixed).tz_convert(None) - pd.Timedelta(hours=8)).floor("6h"))
    # an earlier run for 9/27, submitted before the deadline, so verification has something to score
    v.DATA.mkdir(parents=True, exist_ok=True)
    (v.LEGACY_HISTORY).unlink(missing_ok=True)
    v.append_run("2025-09-26T22:00:00+00:00", "KTPA", date(2025, 9, 27),
                 {"GFS": {"tmax_f": 84, "tmin_f": 71, "wind_max_kt": 8, "precip_in": 0.1}})
    monkeypatch.setattr(sys, "argv", ["x", "KTPA", "--no-push", "--obs-days", "3"])
    m.main()

    fc = json.loads((work / "data/wxchallenge/forecast.json").read_text())
    assert fc["meta"]["target_date"] == "2025-09-29" and fc["meta"]["station"] == "KTPA"
    for k in ["HRRR", "IFS", "GFS", "AIFS", "GFS_MOS", "NAM_MOS", "NBM", "CONSENSUS"]:
        assert fc["models"][k].get("tmax_f") is not None, k
    ver = json.loads((work / "data/wxchallenge/verification.json").read_text())
    d27 = [d for d in ver["days"] if d["date"] == "2025-09-27"][0]
    assert d27["wind_source"] == "CLI" and d27["obs"]["wind_max_kt"] == 10
    assert d27["models"]["GFS"]["points"] == pytest.approx(2 + 1 + 1 + wxc_verify.precip_points(0.1, 0.02))
    runs = wxc_verify.read_jsonl(work / "data/wxchallenge/runs.jsonl")
    assert runs[-1]["target_date"] == "2025-09-29" and "series" not in json.dumps(runs[-1])
    assert (work / "images/wxchallenge/latest.png").exists()
    assert (work / "images/wxchallenge/verification.png").exists()

    # ---- second run: stored obs are reused where final, hindcasts are not repeated ----
    n_runs = len(runs)
    hind = [r for r in runs if r.get("hindcast")]
    assert {r["target_date"] for r in hind} == {"2025-09-24", "2025-09-25", "2025-09-26", "2025-09-27"}
    fetched = []
    monkeypatch.setattr(o, "fetch_metars", lambda st, a, b: fetched.append((a, b)) or ks)
    m.main()
    runs2 = wxc_verify.read_jsonl(work / "data/wxchallenge/runs.jsonl")
    # the live run + one retry per day for the MOS products the fake API couldn't supply
    retries = [r for r in runs2[n_runs:] if r.get("hindcast")]
    assert len(runs2) == n_runs + 1 + 4 and all(set(r["models"]) <= {"GFS_MOS", "NAM_MOS", "NBM", "CONSENSUS"}
                                                 for r in retries)
    m.main()                                            # third run: nothing left to retry
    assert len(wxc_verify.read_jsonl(work / "data/wxchallenge/runs.jsonl")) == len(runs2) + 1
    # 9/24-25 are final (>48 h old) and 9/27 has a final CLI: only 9/26 is re-fetched
    assert len(fetched) >= 1 and fetched[0][0].date() == date(2025, 9, 26) and fetched[0][1].date() == date(2025, 9, 27)
