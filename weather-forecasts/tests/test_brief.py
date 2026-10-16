"""Offline tests for the plain-text AI brief (wxc_brief)."""
import json
from datetime import datetime, timezone

import wxc_brief

NOW = datetime(2026, 10, 6, 22, 30, tzinfo=timezone.utc)


def _forecast():
    stats = {"mean": 0.8, "p10": 0.1, "p25": 0.4, "p50": 0.85, "p75": 1.0, "p90": 1.5}
    return {
        "generated_at_utc": "2026-10-06T22:12:10+00:00",
        "meta": {"site": "Tampa, FL (KTPA)", "station": "KTPA", "wfo": "TBW",
                 "afd_url": "https://forecast.weather.gov/product.php?site=TBW&issuedby=TBW&product=AFD"
                            "&format=txt&version=1&glossary=0",
                 "target_date": "2026-10-07",
                 "valid_range_utc": ["2026-10-07T06", "2026-10-08T06"],
                 "models": ["HRRR", "ENS", "NBM_QMD", "CONSENSUS"]},
        "models": {
            "HRRR": {"tmax_f": 81.1, "tmin_f": 71.9, "wind_max_kt": 10.1, "precip_in": 1.39,
                     "init_time_utc": "2026-10-06T18"},
            "ENS": {"tmax_f": 81.2, "tmin_f": 73.9, "wind_max_kt": 7.8, "precip_in": 0.82,
                    "init_time_utc": "2026-10-06T06", "note": "ensemble mean of 51 members",
                    "pop": {"p24": 1.0, "blocks": {"06-12": 0.9}, "basis": "member fraction"},
                    "ensemble": {"n_members": 51, "stats": {"precip_in": {**stats, "std": 0.5},
                                                            "precip_prob": {"0.01": 1.0, "0.10": 0.94}}}},
            "NBM_QMD": {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": 2.37,
                        "precip_only": True, "init_time_utc": "2026-10-06T12",
                        "pop": {"p24": 0.985, "blocks": {}, "basis": "NBM QMD", "q24_in": {"50": 2.369}}},
            "CONSENSUS": {"tmax_f": 81.5, "tmin_f": 75.0, "wind_max_kt": 11.7, "precip_in": 1.4,
                          "method": {"tmax_f": {"method": "bias-corrected", "weights": {"HRRR": 0.6, "ENS": 0.4},
                                                "excluded_outliers": ["GFS"]}}},
        },
    }


def _verif():
    day = {"date": "2026-10-05", "obs": {"tmax_f": 88, "tmin_f": 78, "wind_max_kt": 11, "precip_in": 0.0},
           "obs_pending": ["wind_max_kt"], "hindcast": False,
           "models": {"HRRR": {"error": {"tmax_f": 0, "tmin_f": -3, "wind_max_kt": 1, "precip_in": 0.11},
                               "points": 7.8}}}
    early = {"date": "2026-10-04", "hindcast": True, "obs": {"tmax_f": 89, "tmin_f": 79, "wind_max_kt": 9,
                                                              "precip_in": 0.01},
             "models": {"HRRR": {"error": {"tmax_f": -2, "tmin_f": -4, "wind_max_kt": -1, "precip_in": 0.0},
                                 "points": 9.0}}}
    return {"station": "KTPA", "period_start": "2026-09-16", "city_start": "2026-09-29",
            "half_life_days": {"tmax_f": 9.0}, "days": [early, day],
            "summary": {"HRRR": {"n_days": 20, "mean_points": 11.11,
                                 "bias": {"tmax_f": -1.93, "tmin_f": -0.01, "wind_max_kt": -2.3, "precip_in": 0.06},
                                 "mae": {"tmax_f": 2.1, "tmin_f": 3.1, "wind_max_kt": 3.4, "precip_in": 0.18}}},
            "pop": {"summary": {"ENS": {"brier_6h": 0.322, "n_blocks": 12}}, "event_in": 0.01,
                    "days": [{"date": "2026-10-05", "precip_in": 0.01, "obs": {"24h": 1, "00-06": 1},
                              "models": {"ENS": {"p24": 1.0, "blocks": {"06-12": 0.9}}}}],
                    "base_rate": {"freq_6h": 0.083, "brier_6h": 0.0761}}}


def _today(station="KTPA"):
    return {"date": "2026-10-06", "through_utc": "2026-10-06T21:53", "station": station,
            "obs": {"high": 78.98, "low": 75.92, "wind": 5, "precip": 0.92, "n_obs": 16},
            "models": {"AIFS": {"init_time_utc": "2026-10-05T12", "temp_bias": -0.02, "temp_mae": 1.3,
                                "high_fcst": 82.0, "high_err": 2.0, "low_fcst": 75.9, "low_err": -0.2,
                                "low_pending": True, "wind_bias": -0.6}}}


def test_brief_has_every_section_and_key_numbers():
    txt = wxc_brief.build_brief(_forecast(), _verif(), _today(), now=NOW)
    for heading in ("# WxChallenge forecast brief: Tampa, FL (KTPA)", "## How to use this brief",
                    "## Scoring", "## Guidance for the target day", "## Consensus method",
                    "## Ensemble spread", "## Chance of measurable precip", "## Track record this period",
                    "## Daily verification (all 2 days", "## Daily verification of precip chances",
                    "## Today so far", "## Raw data"):
        assert heading in txt, heading
    assert "Submission deadline: 2026-10-07T00Z" in txt
    assert "| **CONSENSUS** |  | **81.5** | **75.0** | **11.7** | **1.40** |" in txt
    assert "| HRRR | 06/18Z | 81.1 | 71.9 | 10.1 | 1.39 |" in txt
    assert "NBM_QMD (precip only)" in txt and 'p50 2.37"' in txt
    assert "outliers excluded: GFS" in txt
    assert "| ENS | 51 | Precip in | 0.10 | 0.40 | 0.85 | 1.00 | 1.50 | 0.80 |" in txt
    assert "| HRRR | 20 | 11.1 | -1.9 | +0.0 |" in txt          # -0.01 shown as +0.0, never -0.0
    assert "| 10-04 h | 9.0 | HRRR |" in txt and "| 10-05 | 7.8 | HRRR |" in txt   # every day, hindcasts marked
    assert "| 10-05 | 78 | -3 |" in txt and "| 10-05 | 0.00 | +0.11 |" in txt   # obs + error per variable
    assert "| 10-05 | ~11 | +1 |" in txt                          # preliminary wind marked
    assert "- NWS Area Forecast Discussion (TBW): https://forecast.weather.gov/product.php?site=TBW" in txt
    assert "Read the latest AFD" in txt
    assert '| 10-05 | 0.01" (wet: 00-06) | 90/—/—/— |' in txt     # daily precip chances
    assert "76 (+0) pending" in txt                               # rounded -0.2 isn't "-0"
    assert "-0 " not in txt and "-0.0 " not in txt and "Warning" not in txt


def test_brief_without_today_and_stale_warning():
    late = datetime(2026, 10, 7, 4, 0, tzinfo=timezone.utc)
    txt = wxc_brief.build_brief(_forecast(), {}, None, now=late)
    assert "## Today so far" not in txt and "## Track record" not in txt
    assert "Warning: this brief is 6 h old" in txt


def test_write_brief_ignores_other_stations_today(tmp_path):
    (tmp_path / "forecast.json").write_text(json.dumps(_forecast()))
    (tmp_path / "verification.json").write_text(json.dumps(_verif()))
    (tmp_path / "today.json").write_text(json.dumps(_today("KDSM")))
    out = wxc_brief.write_brief(tmp_path)
    assert out == tmp_path / "brief.md"
    txt = out.read_text()
    assert "## Guidance for the target day" in txt and "## Today so far" not in txt


def _clouds():
    obs = {"night_pct": 89.0, "day_pct": 90.0, "goes_night_pct": 60.0, "goes_day_pct": 95.0}
    return {"2026-10-04": {"obs": {"night_pct": None, "day_pct": 22.0},      # station outage overnight
                           "models": {"HRRR": {"night_err": None, "day_err": 39}}},
            "2026-10-05": {"obs": obs, "models": {"HRRR": {"night_err": -40, "day_err": 10}}}}


def test_brief_cloud_section():
    txt = wxc_brief.build_brief(_forecast(), _verif(), _today(), now=NOW, clouds=_clouds())
    assert "## Clouds (context only, not scored)" in txt
    assert txt.index("## Daily verification (all") < txt.index("## Clouds") < txt.index("## Today so far")
    assert "| HRRR | 2 | -40 | 40 | +24 | 24 |" in txt      # night: 10-05 only; day: mean of +39, +10
    assert "| 10-04 h | — | — | — |" in txt and "| 10-05 | 89% | 60% | -40 |" in txt     # night table (+ GOES)
    assert "| 10-04 h | 22% | — | +39 |" in txt and "| 10-05 | 90% | 95% | +10 |" in txt  # day table
    assert "cloud_context.json" in txt and "too clear at night -> low too cold" in txt
    # no clouds: no section (but the how-to step and the link stay)
    assert "## Clouds" not in wxc_brief.build_brief(_forecast(), _verif(), _today(), now=NOW)


def test_write_brief_reads_cloud_context(tmp_path):
    (tmp_path / "forecast.json").write_text(json.dumps(_forecast()))
    (tmp_path / "verification.json").write_text(json.dumps(_verif()))
    (tmp_path / "cloud_context.json").write_text(json.dumps({"stations": {"KTPA": _clouds(), "KOLM": {}}}))
    assert "## Clouds (context only" in wxc_brief.write_brief(tmp_path).read_text()
    (tmp_path / "cloud_context.json").write_text(json.dumps({"stations": {"KDSM": _clouds()}}))
    assert "## Clouds" not in wxc_brief.write_brief(tmp_path).read_text()   # another station's clouds


def _series(precip):
    t = ["2026-10-07T06:00", "2026-10-07T09:00", "2026-10-07T12:00"]
    return {"station": "KTPA", "target_date": "2026-10-07", "kind": "submitted",
            "generated_at_utc": "2026-10-06T22:12:10+00:00",
            "models": {"HRRR": {"times": t, "temp_f": [75.0, 73.2, 72.0], "wind_kt": [5.0, 4.0, 3.5],
                                "precip_in": precip},
                       "GFS_MOS": {"times": t[::2], "temp_f": [76.0, 71.0], "wind_kt": [3.0, 2.0],
                                   "precip_in": None}}}


def test_hourly_guidance_tables():
    txt = wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW, series=_series([0.0, 0.12, 0.5]))
    assert "## Hourly guidance through the target day\n" in txt
    assert "| UTC | Local (EDT) | HRRR | GFS_MOS |" in txt                 # tz from the station registry
    assert "| 10-07 06Z | Wed 02:00 | 75.0 | 76.0 |" in txt
    assert "| 10-07 09Z | Wed 05:00 | 73.2 |  |" in txt                    # MOS has no 09Z value
    assert "| UTC | Local (EDT) | HRRR |\n" in txt                          # no MOS precip column
    assert "| 10-07 12Z | Wed 08:00 | 0.50 |" in txt
    dry = wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW, series=_series([0.0, 0.0, 0.0]))
    assert "0.00 in every model (HRRR) all day." in dry
    assert "## Hourly guidance" not in wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW)


def test_write_brief_reads_target_day_series(tmp_path):
    (tmp_path / "forecast.json").write_text(json.dumps(_forecast()))
    (tmp_path / "series").mkdir()
    (tmp_path / "series" / "KTPA_2026-10-07_submitted.json").write_text(json.dumps(_series([0, 0.1, 0.2])))
    assert "## Hourly guidance through the target day\n" in wxc_brief.write_brief(tmp_path).read_text()


def _cloud_series():
    return {"station": "KTPA", "target_date": "2026-10-07",
            "generated_at_utc": "2026-10-06T22:12:10+00:00",
            "models": {"GFS": {"times": ["2026-10-07T06:00", "2026-10-07T09:00"], "cloud_pct": [40.0, 87.6],
                               "averaged": [False, True]},
                       "GFS_MOS": {"times": ["2026-10-07T06:00"], "cloud_pct": [19.0], "step": True}}}


def test_hourly_cloud_table():
    txt = wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW, series=_series([0.0, 0.0, 0.0]),
                                cloud_series=_cloud_series())
    i = txt.index("Total cloud cover (%):")
    assert txt.index("0.00 in every model (HRRR) all day.") < i            # dry line stays in its place
    assert "| UTC | Local (EDT) | GFS | GFS_MOS |" in txt[i:]
    assert "| 10-07 06Z | Wed 02:00 | 40 | 19 |" in txt[i:]
    assert "| 10-07 09Z | Wed 05:00 | 88* |  |" in txt[i:]                 # * = time-averaged step
    only_clouds = wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW, cloud_series=_cloud_series())
    assert "## Hourly guidance" in only_clouds and "Total cloud cover (%):" in only_clouds


def test_write_brief_reads_target_day_clouds(tmp_path):
    (tmp_path / "forecast.json").write_text(json.dumps(_forecast()))
    (tmp_path / "cloud_forecast.json").write_text(json.dumps(_cloud_series()))
    assert "Total cloud cover (%):" in wxc_brief.write_brief(tmp_path).read_text()
    (tmp_path / "cloud_forecast.json").write_text(json.dumps({**_cloud_series(), "target_date": "2026-10-06"}))
    assert "Total cloud cover" not in wxc_brief.write_brief(tmp_path).read_text()   # stale day ignored


def _cloud_today():
    return {"station": "KTPA", "date": "2026-10-06", "generated_at_utc": "2026-10-06T22:12:10+00:00",
            "goes": [{"hour": "2026-10-06T06:00", "cloud_pct": 12.3, "satellite": "G19"},
                     {"hour": "2026-10-06T07:00", "cloud_pct": 88.0, "satellite": "G19"}],
            "metar": [{"hour": "2026-10-06T06:00", "sky_pct": 100.0}, {"hour": "2026-10-06T08:00", "sky_pct": 44.0}],
            "models": {"HRRR": {"times": ["2026-10-06T06:00", "2026-10-06T07:00"], "cloud_pct": [90.0, 75.4]}}}


def test_today_clouds_goes_and_metar():
    txt = wxc_brief.build_brief(_forecast(), _verif(), _today(), now=NOW, cloud_today=_cloud_today())
    i = txt.index("## Clouds so far today (2026-10-06, observed vs forecast)")
    assert txt.index("## Today so far") < i < txt.index("## Raw data")
    sec = txt[i:]
    assert "GOES-19 Clear Sky Mask" in sec and "misses low stratus and fog" in sec
    assert "| UTC | Local (EDT) | GOES | METAR | HRRR |" in sec
    assert "| 10-06 06Z | Tue 02:00 | 12 | 100 | 90 |" in sec      # GOES too clear under a low overcast
    assert "| 10-06 07Z | Tue 03:00 | 88 |  | 75 |" in sec
    assert "| 10-06 08Z | Tue 04:00 |  | 44 |  |" in sec


def test_write_brief_today_clouds_must_match(tmp_path):
    (tmp_path / "forecast.json").write_text(json.dumps(_forecast()))
    (tmp_path / "today.json").write_text(json.dumps(_today()))
    (tmp_path / "cloud_today.json").write_text(json.dumps(_cloud_today()))
    assert "## Clouds so far today" in wxc_brief.write_brief(tmp_path).read_text()
    (tmp_path / "cloud_today.json").write_text(json.dumps({**_cloud_today(), "date": "2026-10-05"}))
    assert "## Clouds so far today" not in wxc_brief.write_brief(tmp_path).read_text()   # yesterday's file


def test_hourly_dewpoint_and_rh_tables():
    ser = _series([0.0, 0.12, 0.5])
    ser["models"]["HRRR"]["dewpt_f"] = [70.0, 73.2, None]
    ser["models"]["GFS_MOS"]["dewpt_f"] = [60.0, 65.0]
    txt = wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW, series=ser)
    t, d, r, w = (txt.index(x) for x in ("Temperature (°F):", "Dewpoint (°F):", "Relative humidity (%)",
                                         "Wind speed (kt)"))
    assert t < d < r < w                                                    # right after temperature
    assert "| 10-07 06Z | Wed 02:00 | 70.0 | 60.0 |" in txt[d:r]
    assert "| 10-07 09Z | Wed 05:00 | 73.2 |  |" in txt[d:r]
    assert "| 10-07 06Z | Wed 02:00 | 84 | 58 |" in txt[r:w]                # 75/70 F, 76/60 F
    assert "| 10-07 09Z | Wed 05:00 | 100 |  |" in txt[r:w]                 # dewpoint = temperature
    assert "Dewpoint and relative humidity (context, not scored)" in txt
    assert "Dewpoint (°F):" not in wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW,
                                                         series=_series([0.0, 0.1, 0.2]))


def test_rh():
    assert wxc_brief._rh(75.0, 75.0) == 100.0 and wxc_brief._rh(70.0, 72.0) == 100.0
    assert round(wxc_brief._rh(68.0, 50.0)) == 53 and wxc_brief._rh(None, 50.0) is None


def _obs_today():
    return {"station": "KTPA", "date": "2026-10-06",
            "reports": {"times": ["2026-10-06T05:53", "2026-10-06T06:10", "2026-10-06T06:53", "2026-10-06T08:20"],
                        "temp_f": [80.0, 79.0, 78.1, 77.0], "dewpt_f": [70.0, 71.1, 72.0, None]}}


def _series_today():
    t = ["2026-10-06T06:00", "2026-10-06T07:00", "2026-10-06T09:00"]
    return {"models": {"HRRR": {"times": t, "temp_f": [80, 79, 78], "dewpt_f": [71.0, 73.0, 74.0]},
                       "GFS_MOS": {"times": t[::2], "temp_f": [80, 78], "dewpt_f": [68.0, 70.0]},
                       "ENS": {"times": t, "temp_f": [80, 79, 78]}}}


def test_today_dewpoint_so_far():
    txt = wxc_brief.build_brief(_forecast(), _verif(), _today(), now=NOW,
                                obs_today=_obs_today(), series_today=_series_today())
    i = txt.index("## Dewpoint so far today (2026-10-06, observed vs forecast)")
    assert txt.index("## Today so far") < i < txt.index("## Raw data")
    sec = txt[i:txt.index("## Raw data")]
    assert "| UTC | Local (EDT) | Obs Td | Obs RH | HRRR | GFS_MOS |" in sec     # ENS: no dewpoint
    assert "| 10-06 06Z | Tue 02:00 | 70.0 | 72 | 71.0 | 68.0 |" in sec       # 05:53 is nearer than 06:10
    assert "| 10-06 07Z | Tue 03:00 | 72.0 | 82 | 73.0 |  |" in sec
    assert "08Z" not in sec                                                 # 08:20 has no dewpoint
    assert "| Bias so far |  |  |  | +1.0 | -2.0 |" in sec
    assert "## Dewpoint so far" not in wxc_brief.build_brief(_forecast(), _verif(), _today(), now=NOW)


def test_write_brief_reads_today_dewpoint(tmp_path):
    (tmp_path / "forecast.json").write_text(json.dumps(_forecast()))
    (tmp_path / "today.json").write_text(json.dumps(_today()))
    (tmp_path / "timeline").mkdir()
    (tmp_path / "timeline" / "KTPA_2026-10-06_obs.json").write_text(json.dumps(_obs_today()))
    (tmp_path / "series").mkdir()
    (tmp_path / "series" / "KTPA_2026-10-06_submitted.json").write_text(json.dumps(_series_today()))
    assert "## Dewpoint so far today" in wxc_brief.write_brief(tmp_path).read_text()


def _timeline():
    # night = hours 0-2, day = hours 3-5 (since 06Z); HRRR hourly, GFS 3-hourly
    return {"station": "KTPA", "days": [
        {"date": "2026-10-05", "cloud_win": {"night": [0, 2], "day": [3, 5]},
         "models": {"HRRR": {"h": [0, 1, 2, 3, 4, 5], "td": [61, 61, 61, 60, 60, 60]},
                    "GFS": {"h": [0, 3, 6], "td": [56, 59, 62]},
                    "ENS": {"h": [0, 3], "temp": [70, 71]}},
         "obs": {"reports": {"h": [0.88, 1.9, 2.6, 2.95, 3.9, 4.88, 5.2],
                             "td": [60, 59, None, 58, 62, 62, 99]}}},
        {"date": "2026-10-04", "cloud_win": {"night": [0, 2], "day": [3, 5]},
         "models": {"HRRR": {"h": [0, 1, 2, 3, 4, 5], "td": [50, 50, 50, 50, 50, 50]}},
         "obs": {"reports": {"h": [1.0], "td": [48.0]}}}]}       # one hour of 3: too few


def test_dewpoint_window_means():
    m = {"h": [0, 3, 6], "td": [56, 59, 62]}
    assert wxc_brief._model_window(m, [0, 2]) == 57.0                       # 56, 57, 58 interpolated
    assert wxc_brief._model_window(m, [5, 9]) is None                       # covers 5-6 only: too few
    r = {"h": [0.88, 1.9, 2.6], "td": [60, 59, None]}
    assert wxc_brief._obs_window(r, [0, 2]) == 59.5                         # 0Z: none within 35 min
    assert wxc_brief._obs_window(r, [0, 5]) is None


def test_past_days_dewpoint_section():
    txt = wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW, timeline=_timeline())
    i = txt.index("## Dewpoint (context only, not scored)")
    assert txt.index("## Daily verification (all") < i < txt.index("## Daily verification of precip")
    sec = txt[i:txt.index("## Daily verification of precip")]
    # observed, nearest report each hour: night 0Z none, 1Z 60, 2Z 59 -> 59.5; day 3Z 58, 4Z 62, 5Z 62 -> 60.7
    assert "| HRRR | 1 | +1.5 | 1.5 | -0.7 | 0.7 |" in sec
    assert "| 10-05 | 59.5 | +1.5 |" in sec and "| 10-05 | 60.7 | -0.7 |" in sec
    assert "| 10-04 h | — | — |" in sec                                      # too few obs hours
    assert "ENS" not in sec                                                 # no dewpoint
    assert "## Dewpoint (context" not in wxc_brief.build_brief(_forecast(), _verif(), None, now=NOW)


def test_write_brief_reads_timeline(tmp_path):
    (tmp_path / "forecast.json").write_text(json.dumps(_forecast()))
    (tmp_path / "verification.json").write_text(json.dumps(_verif()))
    (tmp_path / "timeline.json").write_text(json.dumps(_timeline()))
    assert "## Dewpoint (context only" in wxc_brief.write_brief(tmp_path).read_text()
    (tmp_path / "timeline.json").write_text(json.dumps({**_timeline(), "station": "KOLM"}))
    assert "## Dewpoint (context only" not in wxc_brief.write_brief(tmp_path).read_text()
