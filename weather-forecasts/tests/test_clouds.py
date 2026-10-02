"""
Offline tests for the display-only cloud cover (wxc_clouds, wxc_goes, the cloud panels),
including the check that cloud data never changes a scored output.

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

import wxc_clouds  # noqa: E402
import wxc_goes  # noqa: E402
import wxc_usl  # noqa: E402
from wxc_stations import STATIONS, default_goes  # noqa: E402
from test_wxc import (CLI_TEXT, KSAV, FakeFastHerbie, _main_module, _mos_rows,  # noqa: E402,F401
                      _openmeteo, fake_herbie)

USL_REAL = (HERE / "fixtures" / "usl_KTPA_20260930_12.html").read_text(encoding="iso-8859-1")
PROJ_EAST = dict(semi_major_axis=6378137.0, semi_minor_axis=6356752.31414,
                 perspective_point_height=35786023.0, longitude_of_projection_origin=-75.0)


# ----------------------------------------------------------------- METAR sky cover
@pytest.mark.parametrize("codes,pct,clear", [
    (["FEW", "SCT", "BKN", "M"], 75, False),       # highest-coverage layer wins
    (["SCT", "OVC"], 100, False),
    (["VV"], 100, False),                           # sky obscured
    (["CLR", "M", "M", "M"], 0, True),
    (["SKC"], 0, True),
    (["NCD"], 0, False),
    (["FEW"], 19, False),
    (["M", "M"], None, False),
])
def test_metar_sky_pct(codes, pct, clear):
    assert wxc_clouds.sky_pct(codes) == (pct, clear)


def test_metar_sky_codes_and_series():
    assert wxc_clouds.metar_sky_codes("KTPA 010053Z 00000KT 1/4SM FG VV002 22/22 A3000 RMK AO2 FEW100") == ["VV"]
    assert wxc_clouds.metar_sky_codes("KTPA 301653Z 13006KT 10SM FEW037 SCT150 BKN250CB 30/22 A3004") == \
        ["FEW", "SCT", "BKN"]
    raw = pd.DataFrame({
        "valid": ["2026-09-30 06:53", "2026-09-30 07:53", "2026-09-30 08:53", "2026-09-30 09:53"],
        "skyc1": ["SCT", "CLR", "M", "VV "], "skyc2": ["BKN", "M", "M", "M"],
        "metar": ["x", "x", "KTPA 300853Z 00000KT 10SM OVC008 25/22 A2997", "x"]})
    s = wxc_clouds.sky_series(raw)
    assert list(s["sky_pct"]) == [75, 0, 100, 100]      # 08:53: no skyc columns -> from the METAR text
    assert list(s["clear"]) == [False, True, False, False]


# ----------------------------------------------------------------- MOS / NBM
def test_mos_cld_categories():
    assert [wxc_clouds.mos_cld_pct(c) for c in ["CL", "FW", "SC", "BK", "OV", None, "XX"]] == \
        [0, 19, 44, 75, 100, None, None]
    df = pd.DataFrame({"runtime": "2026-09-30 12:00",
                       "ftime": ["2026-10-01 06:00", "2026-10-01 09:00", "2026-10-01 12:00"],
                       "cld": ["BK", "OV", "CL"], "sky": [None, None, None]})
    rec = wxc_clouds.mos_cloud(df, "GFS")
    assert rec["cloud_pct"] == [75, 100, 0] and rec["step"] and rec["init_time_utc"] == "2026-09-30T12"
    assert rec["times"][0] == "2026-10-01T06:00"
    nbs = wxc_clouds.mos_cloud(df.assign(cld=None, sky=[80, 54, 60]), "NBS")
    assert nbs["cloud_pct"] == [80, 54, 60] and not nbs["step"]
    assert wxc_clouds.mos_cloud(df.assign(cld=None), "GFS") is None


# ----------------------------------------------------------------- USL
def test_usl_sky_cover_real_page():
    """Real 20260930_12 page: 'Sky Cover' is a whole percent ('65%'); the page labels
    1 Oct as '01 SEP', so the times must still come from the month-rollover fix."""
    run = wxc_usl.parse_run(USL_REAL)
    assert len(run["sky_pct"]) == len(run["times"]) == 25
    assert run["times"][0] == datetime(2026, 10, 1, 6, tzinfo=timezone.utc)
    assert run["times"][-1] == datetime(2026, 10, 2, 6, tzinfo=timezone.utc)
    assert run["sky_pct"][:3] == [65, 70, 75] and run["sky_pct"][-1] == 90
    assert all(0 <= v <= 100 for v in run["sky_pct"])
    # the scored summary is unchanged by the extra column
    res = wxc_usl.summarize_run(run, date(2026, 10, 1))
    assert (res["tmax_f"], res["tmin_f"], res["wind_max_kt"], res["precip_in"]) == (89, 74, 11, 0.79)
    assert "sky" not in json.dumps(res).lower()


def test_usl_text_cloud(monkeypatch):
    monkeypatch.setattr(wxc_usl, "_get", lambda url: USL_REAL if url.endswith("20260930_12.html") else None)
    rec = wxc_clouds.fetch_text_cloud("KTPA", "USL", "2026-09-30T12")
    assert rec["times"][0] == "2026-10-01T06:00" and rec["cloud_pct"][0] == 65
    assert wxc_clouds.fetch_text_cloud("KTPA", "USL", "2026-09-29T22") is None


# ----------------------------------------------------------------- cloud cache
def test_cloud_cache_merge_and_day():
    a = {"model": "GFS", "times": ["2026-10-01T06:00", "2026-10-01T09:00"], "cloud_pct": [10.0, None]}
    b = {"model": "GFS", "times": ["2026-10-01T09:00", "2026-10-02T09:00"], "cloud_pct": [50.0, 120.0],
         "averaged": [True, False]}
    m = wxc_clouds.merge(a, b)
    assert m["times"] == ["2026-10-01T06:00", "2026-10-01T09:00", "2026-10-02T09:00"]
    assert m["cloud_pct"] == [10.0, 50.0, 100.0] and m["averaged"] == [False, True, False]
    wxc_clouds.save_cloud("KTPA", "GFS", "2026-09-30T12", m)
    assert wxc_clouds.cloud_path("KTPA", "GFS", "2026-09-30T12").name == "_cloud_GFS_2026093012.json"
    d = wxc_clouds.for_day(wxc_clouds.load_cloud("KTPA", "GFS", "2026-09-30 12:00"), date(2026, 10, 1))
    assert d["times"] == ["2026-10-01T06:00", "2026-10-01T09:00"] and d["averaged"] == [False, True]


# ----------------------------------------------------------------- GOES
def test_goes_pug_example():
    """GOES-R PUG vol. 3 worked example (lon0 = -75)."""
    x, y = wxc_goes.latlon_to_xy(33.846162, -84.690932, PROJ_EAST)
    assert float(x) == pytest.approx(-0.024052, abs=1e-6) and float(y) == pytest.approx(0.095340, abs=1e-6)
    lat, lon = wxc_goes.xy_to_latlon(-0.024052, 0.095340, PROJ_EAST)
    assert float(lat) == pytest.approx(33.846162, abs=1e-4) and float(lon) == pytest.approx(-84.690932, abs=1e-4)
    # the far side of the Earth is not visible
    assert np.isnan(wxc_goes.latlon_to_xy(0.0, 105.0, PROJ_EAST)[0])


def _synthetic_grid(lat, lon, n=60):
    """A CONUS-like 2 km fixed grid (56 microrad) centred near the station."""
    xs, ys = wxc_goes.latlon_to_xy(lat, lon, PROJ_EAST)
    d = 5.6e-5
    x = float(xs) + d * (np.arange(n) - n // 2 + 0.3)
    y = float(ys) - d * (np.arange(n) - n // 2 + 0.3)       # y decreases with row, as in the files
    return x, y


def test_goes_fraction_on_synthetic_grid():
    st = STATIONS["KTPA"]
    x, y = _synthetic_grid(st.lat, st.lon)
    xs, _ = wxc_goes.latlon_to_xy(st.lat, st.lon, PROJ_EAST)
    xx, _ = np.meshgrid(x, y)
    bcm = (xx > xs).astype(np.uint8)                       # cloudy east of the station
    dqf = np.zeros_like(bcm)
    pct, n = wxc_goes.fraction_near(x, y, bcm, dqf, PROJ_EAST, st.lat, st.lon)
    assert 100 < n < 250 and pct == pytest.approx(50, abs=6)
    # the station's own pixel is the nearest one
    sy, sx = wxc_goes.station_window(x, y, PROJ_EAST, st.lat, st.lon)
    assert sx.start < 30 < sx.stop and sy.start < 30 < sy.stop
    # bad-quality pixels are skipped: mark the whole cloudy half bad -> all clear
    pct, n2 = wxc_goes.fraction_near(x, y, bcm, np.where(bcm == 1, 1, 0), PROJ_EAST, st.lat, st.lon)
    assert pct == 0 and n2 < n
    # fill values (255) are not pixels
    pct, _ = wxc_goes.fraction_near(x, y, np.where(bcm == 1, 255, 0).astype(np.uint8), dqf,
                                    PROJ_EAST, st.lat, st.lon)
    assert pct == 0
    with pytest.raises(ValueError, match="outside"):
        wxc_goes.fraction_near(x, y, bcm, dqf, PROJ_EAST, 40.0, -105.0)


def test_goes_scan_choice_and_station_satellite():
    keys = [f"ABI-L2-ACMC/2026/273/15/OR_ABI-L2-ACMC-M6_G19_s202627315{m:02d}172_e1_c2.nc" for m in (1, 6, 56)]
    t = datetime(2026, 9, 30, 15, tzinfo=timezone.utc)
    assert wxc_goes.scan_start(keys[0]) == datetime(2026, 9, 30, 15, 1, 17, tzinfo=timezone.utc)
    assert wxc_goes.nearest_scan(keys, t) == keys[0]
    assert (STATIONS["KTPA"].goes, STATIONS["KTPA"].goes_sector) == ("G19", "C")
    assert (STATIONS["PAJN"].goes, STATIONS["PAJN"].goes_sector) == ("G18", "F")
    assert default_goes("KSEA", -122.3) == "G18" and default_goes("KFNL", -105.0) == "G19"
    assert default_goes("PHNL", -157.9) == "G18" and default_goes("PGUM", 144.8) is None


def test_goes_hourly_cache(monkeypatch):
    st = STATIONS["KTPA"]
    calls = []
    monkeypatch.setattr(wxc_goes, "list_keys", lambda b, p: [
        f"{p}OR_ABI-L2-ACMC-M6_G19_s2026273{p[-3:-1]}01172_e1_c2.nc"] if p[-3:-1] != "09" else [])
    monkeypatch.setattr(wxc_goes, "read_scan", lambda url, la, lo: calls.append(url) or
                        {"cloud_pct": 40.0, "n_pixels": 140, "bytes": 4_000_000})
    now = datetime(2026, 9, 30, 10, 20, tzinfo=timezone.utc)
    out = wxc_goes.hourly_cloud(st, datetime(2026, 9, 30, 6, tzinfo=timezone.utc), now)
    assert [o["hour"][11:13] for o in out] == ["06", "07", "08", "10"]     # 09Z: no scan posted
    assert len(calls) == 4 and "noaa-goes19" in calls[0] and "/ABI-L2-ACMC/2026/273/06/" in calls[0]
    assert (wxc_goes.wxc_cache.CACHE_DIR / "KTPA" / "_goes_acm_2026093006.json").exists()
    wxc_goes.hourly_cloud(st, datetime(2026, 9, 30, 6, tzinfo=timezone.utc), now)
    assert len(calls) == 4                                               # cached hours not read again


# ----------------------------------------------------------------- GRIB cloud cover
def _cloud_fields(gfs_instant=True):
    f = {":tcc:": ("tcc", lambda h: 0.25 + 0.01 * (h % 10), "(0 - 1)"),
         "TCDC_AVE": ("tcc", lambda h: 60.0, "%")}
    if gfs_instant:
        f["TCDC_NOW"] = ("tcc", lambda h: 30.0 + h % 5, "%")
    return f


def test_grib_cloud_fetch(fake_herbie):
    m = _main_module()
    st = STATIONS["KTPA"]
    pts = pd.DataFrame({"longitude": [st.lon], "latitude": [st.lat]})
    fields = {k if k.startswith(":") else getattr(m, k): v for k, v in _cloud_fields().items()}
    FakeFastHerbie.FIELDS.update(fields)
    init = pd.Timestamp("2026-09-30 12:00")
    ifs = m.fetch_cloud_grib("IFS", init, [18, 21, 24], pts, st)
    assert ifs["cloud_pct"] == pytest.approx([33.0, 26.0, 29.0]) and ifs["times"][0] == "2026-10-01T06:00"
    hrrr = m.fetch_cloud_grib("HRRR", init, [18, 19], pts, st)
    assert hrrr["cloud_pct"] == [33.0, 34.0] and not any(hrrr["averaged"])
    # GFS with only the interval average posted: used, and flagged
    del FakeFastHerbie.FIELDS[m.TCDC_NOW]
    gfs = m.fetch_cloud_grib("GFS", init, [18, 21], pts, st)
    assert gfs["cloud_pct"] == [60.0, 60.0] and gfs["averaged"] == [True, True]


def test_model_cloud_caches_and_fills_gaps(fake_herbie, monkeypatch):
    m = _main_module()
    st = STATIONS["KTPA"]
    pts = pd.DataFrame({"longitude": [st.lon], "latitude": [st.lat]})
    FakeFastHerbie.FIELDS.update({getattr(m, k) if not k.startswith(":") else k: v
                                  for k, v in _cloud_fields().items()})
    asked = []
    real = m.fetch_cloud_grib
    monkeypatch.setattr(m, "fetch_cloud_grib", lambda *a: asked.append(list(a[2])) or real(*a))
    day = date(2026, 10, 1)
    r1 = m.model_cloud(st, "HRRR", "2026-09-30T12", day, pts)
    assert len(r1["times"]) == 25 and asked == [list(range(18, 43))]
    r2 = m.model_cloud(st, "HRRR", "2026-09-30T12", day, pts)
    assert r2 == r1 and len(asked) == 1                         # second call: cloud file only
    # a failing model is left out with a warning, the others still come back
    FakeFastHerbie.FIELDS.pop(":tcc:")
    out = m.collect_clouds(st, day, {"HRRR": "2026-09-30T12", "AIFS": "2026-09-30T06",
                                     "ENS": "2026-09-30T00"}, pts)
    assert set(out) == {"HRRR"}


# ----------------------------------------------------------------- isolation from scoring
FIXED_NOW = datetime(2025, 9, 28, 20, 0, tzinfo=timezone.utc)
MODULES = ["functions", "wxc_obs", "wxc_mos", "wxc_verify", "wxc_stations", "wxc_usl", "wxc_ens",
           "wxc_cam_ens", "wxc_cache", "wxc_clouds", "wxc_goes", "wxc_today",
           "getForecast_wxChallenge-pushGitHub"]


def _offline_main(tmp_path, monkeypatch, name, clouds_on):
    """One full main() run in a scratch copy (no data/ or cache/ carried over), every
    network call faked. Returns the work directory."""
    work = tmp_path / name
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(
        "tests", "__pycache__", "*.ipynb", "images", "data", "cache"))
    monkeypatch.syspath_prepend(str(work))
    for mod in MODULES:
        monkeypatch.delitem(sys.modules, mod, raising=False)
    import wxc_cache as ca, wxc_clouds as cl, wxc_goes as go, wxc_obs as o, wxc_mos as mo  # noqa: E401
    import wxc_usl as us, wxc_ens as en, wxc_cam_ens as ce, wxc_verify as v  # noqa: E401
    m = importlib.import_module("getForecast_wxChallenge-pushGitHub")
    assert Path(m.__file__).parent == work
    ca.CACHE_DIR = work / "cache"
    cl.CLOUDS_ENABLED = cl.GOES_ENABLED = clouds_on

    ks = pd.read_csv(KSAV)[["valid", "metar"]]
    monkeypatch.setattr(o, "fetch_metars", lambda st, a, b, specials=False, sky=False, retries=3: ks)
    monkeypatch.setattr(o, "get_cli", lambda st, first, last, now=None: o.parse_cli(
        CLI_TEXT.replace("SEPTEMBER 27 2026", "SEPTEMBER 27 2025"), st.lst_offset_hours))
    monkeypatch.setattr(o, "fetch_cf6", lambda icao, years: {})
    monkeypatch.setattr(o, "_get", lambda *a, **k: pytest.fail("network call in an offline test"))

    def fake_mos(st, model, runtime=None):
        df = _mos_rows(model).assign(
            runtime="2025-09-28 12:00",
            ftime=lambda d: (pd.to_datetime(d["ftime"]) - pd.Timedelta(days=365)).dt.strftime("%Y-%m-%d %H:%M"))
        return df.assign(cld=["SC", "BK", "OV"] * (len(df) // 3) + ["CL"] * (len(df) % 3),
                         sky=np.linspace(10, 90, len(df)))
    monkeypatch.setattr(mo, "fetch_mos", fake_mos)
    monkeypatch.setattr(us, "_get", lambda url: None)
    monkeypatch.setattr(en, "latest_init", lambda model: datetime(2025, 9, 28, 0, tzinfo=timezone.utc))
    monkeypatch.setattr(en, "_get_json", lambda url, params=None: _openmeteo("2025-09-28"))
    cam_init = datetime(2025, 9, 28, 12, tzinfo=timezone.utc)
    monkeypatch.setattr(ce, "get_refs", lambda st, day, now: ce._result(
        "REFS", cam_init, day, ["a", "b", "c"], [0.0, 0.12, 0.4], "test"))
    monkeypatch.setattr(ce, "get_hrrrcast", lambda st, day, now: ce._fail("not posted", cam_init))
    monkeypatch.setattr(go, "list_keys", lambda b, p: [f"{p}OR_ABI-L2-ACMC-M6_G19_s2025271{p[-3:-1]}01172_e_c.nc"])
    monkeypatch.setattr(go, "read_scan", lambda url, la, lo: {"cloud_pct": 55.0, "n_pixels": 140, "bytes": 1})

    class FixedDT(datetime):
        @classmethod
        def now(cls, tz=None):
            return FIXED_NOW
    monkeypatch.setattr(m, "datetime", FixedDT)
    monkeypatch.setattr(m, "get_latest_forecast_cycle", lambda model, now=None: (
        pd.Timestamp(now or FIXED_NOW).tz_convert(None) - pd.Timedelta(hours=8)).floor("6h"))
    v.DATA.mkdir(parents=True, exist_ok=True)
    v.append_run("2025-09-26T22:00:00+00:00", "KTPA", date(2025, 9, 27),
                 {"GFS": {"tmax_f": 84, "tmin_f": 71, "wind_max_kt": 8, "precip_in": 0.1}})
    monkeypatch.setattr(sys, "argv", ["x", "KTPA", "--no-push", "--obs-days", "3"])
    m.main()
    return work


def _scored_outputs(work):
    """Every scored / published data file, with the wall-clock stamps removed."""
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k != "generated_at_utc"}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    d = work / "data" / "wxchallenge"
    out = {}
    for p in sorted(d.rglob("*.json*")):
        text = p.read_text()
        rows = [json.loads(ln) for ln in text.splitlines() if ln.strip()] if p.suffix == ".jsonl" else json.loads(text)
        out[str(p.relative_to(d))] = strip(rows)
    return out


def test_clouds_never_change_scoring(tmp_path, monkeypatch, fake_herbie):
    FakeFastHerbie.FIELDS.update({":tcc:": ("tcc", lambda h: 0.4, "(0 - 1)"),
                                  r":TCDC:entire atmosphere[^:]*:\d+ hour fcst:": ("tcc", lambda h: 35.0, "%")})
    off = _offline_main(tmp_path, monkeypatch, "off", clouds_on=False)
    on = _offline_main(tmp_path, monkeypatch, "on", clouds_on=True)

    a, b = _scored_outputs(off), _scored_outputs(on)
    assert {"forecast.json", "runs.jsonl", "observations.jsonl", "verification.json", "today.json"} <= set(a)
    assert any(k.startswith("series/") for k in a)
    assert set(a) == set(b)
    for k in a:
        assert a[k] == b[k], f"{k} differs with CLOUDS_ENABLED on"
    assert "cloud" not in json.dumps(b).lower()

    # the "on" run really produced cloud data (in its own cache files) and both figures
    cached = sorted(p.name for p in (on / "cache" / "KTPA").glob("_cloud_*"))
    assert {n.split("_")[2] for n in cached} >= {"HRRR", "RRFS", "IFS", "GFS", "AIFS", "NBM"}
    assert any(n.startswith("_cloud_GFS_MOS_") for n in cached)
    assert list((on / "cache" / "KTPA").glob("_goes_acm_*.json"))
    assert not (off / "cache" / "KTPA").exists() or not list((off / "cache" / "KTPA").glob("_cloud_*"))
    for w in (off, on):
        assert (w / "images/wxchallenge/latest.png").exists() and (w / "images/wxchallenge/today.png").exists()
