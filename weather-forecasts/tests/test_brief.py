"""Offline tests for the plain-text AI brief (wxc_brief)."""
import json
from datetime import datetime, timezone

import wxc_brief

NOW = datetime(2026, 10, 6, 22, 30, tzinfo=timezone.utc)


def _forecast():
    stats = {"mean": 0.8, "p10": 0.1, "p25": 0.4, "p50": 0.85, "p75": 1.0, "p90": 1.5}
    return {
        "generated_at_utc": "2026-10-06T22:12:10+00:00",
        "meta": {"site": "Tampa, FL (KTPA)", "station": "KTPA", "target_date": "2026-10-07",
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
    return {"station": "KTPA", "period_start": "2026-09-16", "city_start": "2026-09-29",
            "half_life_days": {"tmax_f": 9.0}, "days": [day],
            "summary": {"HRRR": {"n_days": 20, "mean_points": 11.11,
                                 "bias": {"tmax_f": -1.93, "tmin_f": -0.01, "wind_max_kt": -2.3, "precip_in": 0.06},
                                 "mae": {"tmax_f": 2.1, "tmin_f": 3.1, "wind_max_kt": 3.4, "precip_in": 0.18}}},
            "pop": {"summary": {"ENS": {"brier_6h": 0.322, "n_blocks": 12}},
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
                    "## Recent days", "## Today so far", "## Raw data"):
        assert heading in txt, heading
    assert "Submission deadline: 2026-10-07T00Z" in txt
    assert "| **CONSENSUS** |  | **81.5** | **75.0** | **11.7** | **1.40** |" in txt
    assert "| HRRR | 06/18Z | 81.1 | 71.9 | 10.1 | 1.39 |" in txt
    assert "NBM_QMD (precip only)" in txt and 'p50 2.37"' in txt
    assert "outliers excluded: GFS" in txt
    assert "| ENS | 51 | Precip in | 0.10 | 0.40 | 0.85 | 1.00 | 1.50 | 0.80 |" in txt
    assert "| HRRR | 20 | 11.1 | -1.9 | +0.0 |" in txt          # -0.01 shown as +0.0, never -0.0
    assert "+0/-3/+1/+0.11" in txt                                # recent errors, high/low/wind/precip
    assert "| 2026-10-05 | 88 | 78 | ~11 | 0.00 |" in txt          # preliminary wind marked
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
