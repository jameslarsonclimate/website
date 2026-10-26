"""
Offline tests for the WxChallenge scripts (no network needed).

    cd weather-forecasts && python -m pytest tests -q
"""
import importlib
import json
import shutil
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import functions  # noqa: E402
import wxc_mos  # noqa: E402
import wxc_obs  # noqa: E402
import wxc_usl  # noqa: E402
import wxc_verify  # noqa: E402
from wxc_stations import STATIONS, Station, default_hrrr_model  # noqa: E402

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


def test_report_series_running_precip():
    rs = wxc_obs.report_series(pd.read_csv(KSAV)[["valid", "metar"]])
    d = rs[(rs["valid"] >= "2025-09-26 18:00") & (rs["valid"] <= "2025-09-26 21:00")]
    # specials at 19:30-19:43 add their own P group on top of the routine total; 1953Z resets to routine sum
    assert list(d["precip_total_in"]) == [0.0, 0.01, 0.15, 0.28, 0.51, 0.59, 0.59]
    assert (~d["routine"]).sum() == 4


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


# ----------------------------------------------------------------- USL
USL_RUN = (HERE / "fixtures" / "usl_KTPA_20260928_12.html").read_text(encoding="iso-8859-1")
USL_INDEX = (HERE / "fixtures" / "usl_KTPA_index.html").read_text()


def _usl_page(gen, first_day, next_day, tmax):
    return (USL_RUN.replace("Generated 28 SEP 2026 1200", f"Generated {gen}")
            .replace("29 SEP 0600", f"{first_day} 0600").replace("30 SEP 0000", f"{next_day} 0000")
            .replace("87°F", f"{tmax}°F"))


def test_usl_parse():
    run = wxc_usl.parse_run(USL_RUN)
    assert run["runtime"] == datetime(2026, 9, 28, 12, tzinfo=timezone.utc)
    assert run["times"][0] == datetime(2026, 9, 29, 6, tzinfo=timezone.utc)
    assert run["times"][-1] == datetime(2026, 9, 30, 6, tzinfo=timezone.utc)
    res = wxc_usl.summarize_run(run, date(2026, 9, 29))
    # the summary table (not the hourly max of 86) is the model's daily value
    assert (res["tmax_f"], res["tmin_f"], res["wind_max_kt"], res["precip_in"]) == (87, 72, 10, 0.12)
    assert res["series"]["precip_cum_in"][-1] == pytest.approx(0.12)
    assert "error" in wxc_usl.summarize_run(run, date(2026, 9, 28))
    assert wxc_usl.list_runs(USL_INDEX)[0] == datetime(2026, 9, 28, 12, tzinfo=timezone.utc)


def test_usl_month_rollover_label_bug():
    """The 20260929_12 page labels 1 Oct 00Z as '01 SEP 0000'; times must still run 30 Sep 06Z -> 1 Oct 06Z."""
    page = (USL_RUN.replace("Generated 28 SEP 2026 1200", "Generated 29 SEP 2026 1200")
            .replace("29 SEP 0600", "30 SEP 0600").replace("30 SEP 0000", "01 SEP 0000"))
    run = wxc_usl.parse_run(page)
    assert run["times"][0] == datetime(2026, 9, 30, 6, tzinfo=timezone.utc)
    assert run["times"][-1] == datetime(2026, 10, 1, 6, tzinfo=timezone.utc)
    assert all(b > a for a, b in zip(run["times"], run["times"][1:]))
    assert "error" not in wxc_usl.summarize_run(run, date(2026, 9, 30))


def test_usl_run_selection(monkeypatch):
    pages = {
        "": USL_INDEX,
        "20260927_12.html": _usl_page("27 SEP 2026 1200", "28 SEP", "29 SEP", 88),
        "20260927_22.html": _usl_page("27 SEP 2026 2200", "28 SEP", "29 SEP", 89),
        "20260928_12.html": USL_RUN,
    }
    monkeypatch.setattr(wxc_usl, "_get", lambda url: pages.get(url.rsplit("/", 1)[-1]))
    at = lambda *a: datetime(*a, tzinfo=timezone.utc)  # noqa: E731
    assert wxc_usl.get_usl_forecast("KTPA", date(2026, 9, 28), at(2026, 9, 27, 23))["tmax_f"] == 89   # 22Z run
    assert wxc_usl.get_usl_forecast("KTPA", date(2026, 9, 28), at(2026, 9, 27, 21))["tmax_f"] == 88   # only 12Z out
    assert wxc_usl.get_usl_forecast("KTPA", date(2026, 9, 29), at(2026, 9, 28, 20))["init_time_utc"] == "2026-09-28T12"
    assert "error" in wxc_usl.get_usl_forecast("KTPA", date(2026, 9, 25), at(2026, 9, 28, 20))
    monkeypatch.setattr(wxc_usl, "_get", lambda url: None)
    assert "no USL page" in wxc_usl.get_usl_forecast("KDSM", date(2026, 9, 29))["error"]


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


def test_today_column_is_provisional_and_kept_out_of_the_record(tmp_path, monkeypatch):
    """Today's so-far column scores the submitted forecasts against the observations so far,
    rounds them like the verifiers, and never touches days or the summary."""
    run = lambda gen, models, **kw: {"generated_at_utc": gen, "station": "KXXX", "target_date": "2026-10-15",
                                     "models": models, **kw}
    fc = lambda t, n: {"tmax_f": t, "tmin_f": n, "wind_max_kt": 8, "precip_in": 0.0}
    runs = [run("2026-10-14T23:00:00+00:00", {"A": fc(70.4, 45), "B": fc(66, 41), "CONSENSUS": fc(68, 43)}),
            run("2026-10-15T01:00:00+00:00", {"A": fc(99, 99)})]          # after the deadline: not scored
    tj = {"date": "2026-10-15", "through_utc": "2026-10-15T20:54", "obs": {"high": 60.5, "low": 39.92, "wind": 7,
          "precip": 0.0, "n_obs": 15}}
    col = wxc_verify.today_column("KXXX", tj, [], runs=runs)
    assert col["provisional"] and col["obs"] == {"tmax_f": 61, "tmin_f": 40, "wind_max_kt": 7, "precip_in": 0.0}
    a = col["models"]["A"]
    assert a["forecast"]["tmax_f"] == 70 and a["points"] == 9 + 5 + 0.5
    assert "reconstructed" not in col["models"]["CONSENSUS"]

    # written next to the verified days, which (with the summary) stay as they were
    vf = tmp_path / "verification.json"
    before = {"station": "KXXX", "days": [{"date": "2026-10-14", "models": {"A": {"points": 3.0}}}],
              "summary": {"A": {"total_points": 3.0}}}
    vf.write_text(json.dumps(before))
    monkeypatch.setattr(wxc_verify, "VERIF", vf)
    monkeypatch.setattr(wxc_verify, "read_runs", lambda: runs)
    wxc_verify.write_today_column("KXXX", tj)
    after = json.loads(vf.read_text())
    assert after["days"] == before["days"] and after["summary"] == before["summary"]
    assert after["today"]["date"] == "2026-10-15"
    assert wxc_verify.write_today_column("KYYY", tj) is None        # verification is for another city


def test_consensus_mixed_verified_and_new():
    models = {"A": {"tmax_f": 90, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0},
              "NEW": {"tmax_f": 86, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0}}
    summary = {"A": {"n_days": 4, "bias": {"tmax_f": 2.0, "tmin_f": 0, "wind_max_kt": -4, "precip_in": 0},
                     "mae": {"tmax_f": 2.0, "tmin_f": 1, "wind_max_kt": 4, "precip_in": 0.0}}}
    c = wxc_verify.consensus(models, summary)
    # A has 4 days: 4/7 of its +2 bias is removed (90 -> 88.86); NEW (86) joins at the median weight
    assert c["tmax_f"] == pytest.approx((90 - 2 * 4 / 7 + 86) / 2, abs=0.05)
    assert c["wind_max_kt"] == pytest.approx((10 + 4 * 4 / 7 + 10) / 2, abs=0.05)
    assert c["method"]["tmax_f"]["not_yet_verified"] == ["NEW"]


def test_consensus_drops_outliers():
    models = {n: {"tmax_f": t, "tmin_f": 72, "wind_max_kt": 8, "precip_in": 0.0}
              for n, t in (("A", 88), ("B", 87), ("C", 89), ("GFS", 58))}
    c = wxc_verify.consensus(models, {})
    assert c["tmax_f"] == pytest.approx(88.0)
    assert c["method"]["tmax_f"]["excluded_outliers"] == ["GFS"]


def test_consensus_lows_remove_more_bias():
    models = {"A": {"tmax_f": 60, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0}}
    summary = {"A": {"n_days": 4, "n_eff": {v: 4 for v in wxc_verify.VARS},
                     "bias": {"tmax_f": 2.0, "tmin_f": 2.0, "wind_max_kt": 0, "precip_in": 0},
                     "mae": {"tmax_f": 2.0, "tmin_f": 2.0, "wind_max_kt": 1, "precip_in": 0.1}}}
    c = wxc_verify.consensus(models, summary)
    assert c["tmax_f"] == pytest.approx(60 - 2 * 4 / 7, abs=0.05)    # K=3
    assert c["tmin_f"] == pytest.approx(40 - 2 * 4 / 5, abs=0.05)    # K=1
    assert "n_eff+1)" in c["method"]["tmin_f"]["method"]


def test_consensus_drops_stale_runs():
    fc = lambda t, init: {"tmax_f": t, "tmin_f": 50, "wind_max_kt": 8, "precip_in": 0.0, "init_time_utc": init}
    models = {"A": fc(60, "2026-10-12T12"), "B": fc(62, "2026-10-12T06"),
              "ENS": fc(66, "2026-10-10T18"),                  # 42 h older than A: stale
              "GEFS": fc(80, "2026-10-12T12"),                 # never a member
              "OLD": fc(61, "2026-10-11T00")}                  # 36 h older: still kept
    c = wxc_verify.consensus(models, {})
    assert c["tmax_f"] == pytest.approx(61.0)
    assert c["method"]["tmax_f"]["excluded_stale"] == ["ENS"]
    assert "ENS" not in c["method"]["tmax_f"]["members"]
    # no init times (reconstructed days): nothing is stale
    c = wxc_verify.consensus({k: {**m, "init_time_utc": None} for k, m in models.items()}, {})
    assert "excluded_stale" not in c["method"]["tmax_f"] and "ENS" in c["method"]["tmax_f"]["members"]


def test_consensus_ensemble_borrows_parent_track_record():
    models = {"IFS": {"tmax_f": 60, "tmin_f": 44, "wind_max_kt": 10, "precip_in": 0.0},
              "ENS": {"tmax_f": 60, "tmin_f": 46, "wind_max_kt": 10, "precip_in": 0.0},
              "NEW": {"tmax_f": 60, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0}}
    st = lambda n, b: {"n_days": n, "n_eff": {v: n for v in wxc_verify.VARS},
                       "bias": {"tmax_f": 0, "tmin_f": b, "wind_max_kt": 0, "precip_in": 0},
                       "mae": {"tmax_f": 1, "tmin_f": 4, "wind_max_kt": 1, "precip_in": 0.1}}
    summary = {"IFS": st(12, 4.0), "ENS": st(1, 9.0)}       # ENS's own single day is too little
    c = wxc_verify.consensus(models, summary)
    corr = 4.0 * 12 / 13                                       # IFS's shrunk bias (K=1), used for both
    assert c["tmin_f"] == pytest.approx((44 - corr + 46 - corr + 40) / 3, abs=0.05)
    d = c["method"]["tmin_f"]
    assert d["proxy_track_record"] == {"ENS": "IFS"} and d["not_yet_verified"] == ["NEW"]
    # once ENS has its own record it uses it
    summary["ENS"] = st(3, 6.0)
    c = wxc_verify.consensus(models, summary)
    assert "proxy_track_record" not in c["method"]["tmin_f"]
    assert c["tmin_f"] == pytest.approx((44 - corr + 46 - 6.0 * 3 / 4 + 40) / 3, abs=0.05)


def test_decay_weight_and_n_eff():
    assert wxc_verify.decay_weight(0, 9) == 1.0
    assert wxc_verify.decay_weight(9, 9) == pytest.approx(0.5)
    assert wxc_verify.decay_weight(18, 9) == pytest.approx(0.25)
    assert wxc_verify.decay_weight(30, None) == 1.0                       # no half-life: equal weights
    assert wxc_verify.n_eff([1, 1, 1, 1]) == pytest.approx(4)
    assert wxc_verify.n_eff([1, 0.5]) == pytest.approx(1.5 ** 2 / 1.25)   # 1.8 effective days
    assert wxc_verify.n_eff([]) == 0
    w = wxc_verify.day_weights(["2026-09-20", "2026-09-29"], {"tmax_f": 9, "tmin_f": 9,
                                                              "wind_max_kt": 18, "precip_in": None})
    assert w["2026-09-29"]["tmax_f"] == 1.0
    assert w["2026-09-20"]["tmax_f"] == pytest.approx(0.5) and w["2026-09-20"]["wind_max_kt"] == pytest.approx(2 ** -0.5)
    assert w["2026-09-20"]["precip_in"] == 1.0


def _day(d, errs):
    """A scored day with tmax errors per model (other variables perfect)."""
    return {"date": d, "models": {n: {"points": abs(e), "error": {"tmax_f": e, "tmin_f": 0, "wind_max_kt": 0,
                                                                 "precip_in": 0}} for n, e in errs.items()}}


def test_model_stats_decay_weighted():
    hl = {"tmax_f": 9, "tmin_f": 9, "wind_max_kt": 18, "precip_in": 12}
    days = [_day("2026-09-20", {"A": 4.0, "B": 2.0}), _day("2026-09-29", {"A": -2.0})]
    st = wxc_verify.model_stats(days, hl)
    # A: weights 0.5 (9 days old) and 1 -> bias (0.5*4 - 2)/1.5 = 0, MAE (0.5*4 + 2)/1.5
    assert st["A"]["bias"]["tmax_f"] == pytest.approx(0.0)
    assert st["A"]["mae"]["tmax_f"] == pytest.approx(4 / 1.5, abs=1e-3)
    assert st["A"]["n_eff"]["tmax_f"] == pytest.approx(1.8)
    assert st["A"]["n_days"] == 2 and st["A"]["total_points"] == 6.0
    # B only has the old day: ages still count from the newest day overall, n_eff = 1
    assert st["B"]["n_days"] == 1 and st["B"]["n_eff"]["tmax_f"] == pytest.approx(1.0)
    # no half-life = the old equal-weight mean
    eq = wxc_verify.model_stats(days, {v: None for v in wxc_verify.VARS})
    assert eq["A"]["bias"]["tmax_f"] == pytest.approx(1.0) and eq["A"]["n_eff"]["tmax_f"] == 2


def test_consensus_shrink_uses_n_eff():
    models = {"A": {"tmax_f": 90, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0}}
    summary = {"A": {"n_days": 4, "n_eff": {"tmax_f": 1.8, "tmin_f": 4, "wind_max_kt": 4, "precip_in": 4},
                     "bias": {"tmax_f": 2.0, "tmin_f": 0, "wind_max_kt": 0, "precip_in": 0},
                     "mae": {"tmax_f": 2.0, "tmin_f": 1, "wind_max_kt": 1, "precip_in": 0.1}}}
    c = wxc_verify.consensus(models, summary)
    assert c["tmax_f"] == pytest.approx(90 - 2 * 1.8 / (1.8 + 3), abs=0.05)     # not 4/7 from n_days
    assert c["method"]["tmax_f"]["weights"] == {"A": 1.0}
    c = wxc_verify.consensus(models, summary, shrink_days=0)                    # tuning override
    assert c["tmax_f"] == pytest.approx(88.0)


def test_verify_reconstructs_hindcast_consensus(tmp_path, monkeypatch):
    monkeypatch.setattr(wxc_verify, "RUNS", tmp_path / "runs.jsonl")
    monkeypatch.setattr(wxc_verify, "OBS", tmp_path / "obs.jsonl")
    fc = lambda t: {"tmax_f": t, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0}
    for d, hind in (("2026-09-24", True), ("2026-09-25", True), ("2026-09-26", True), ("2026-09-27", False)):
        day = date.fromisoformat(d)
        # A always 2 F too warm, B 2 F too cold; the stored consensus is a deliberately bad 99
        wxc_verify.append_run(f"{day - timedelta(days=1)}T21:00:00+00:00", "KTPA", day,
                              {"A": fc(92), "B": fc(88), "CONSENSUS": fc(99 if hind else 90)}, hindcast=hind)
    wxc_verify.upsert_observations([{"station": "KTPA", "date": d, "tmax_f": 90, "tmin_f": 70, "wind_max_kt": 10,
                                     "precip_in": 0.0, "complete": True}
                                    for d in ("2026-09-24", "2026-09-25", "2026-09-26", "2026-09-27")])
    res = wxc_verify.verify("KTPA")
    assert res["city_start"] == "2026-09-27"
    days = {d["date"]: d for d in res["days"]}
    assert [days[d]["hindcast"] for d in sorted(days)] == [True, True, True, False]
    for d in ("2026-09-24", "2026-09-25", "2026-09-26"):
        c = days[d]["models"]["CONSENSUS"]
        assert c["reconstructed"] and c["forecast"]["tmax_f"] == 90               # from A and B, not the stored 99
    live = days["2026-09-27"]["models"]["CONSENSUS"]
    assert not live.get("reconstructed") and live["forecast"]["tmax_f"] == 90    # submitted value kept
    assert days["2026-09-27"]["decay_weight"]["tmax_f"] == 1.0
    assert days["2026-09-24"]["decay_weight"]["tmax_f"] == pytest.approx(0.5 ** (3 / 9), abs=1e-3)
    assert "forecasts" not in days["2026-09-24"]
    # leak-free: 9/26 rebuilt from 9/24-25 only, so changing 9/26's own obs can't change it
    sd = wxc_verify.scored_days("KTPA")
    a = wxc_verify.reconstruct_consensus(sd, 2)
    sd[2]["models"]["A"]["error"]["tmax_f"] = 50
    assert wxc_verify.reconstruct_consensus(sd, 2) == a
    assert wxc_verify.reconstruct_consensus(sd, 0)["method"]["tmax_f"]["method"].startswith("equal-weight")


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


def test_hindcast_never_overrides_live_forecast():
    fc = lambda t: {"tmax_f": t, "tmin_f": 70, "wind_max_kt": 10, "precip_in": 0.0}
    live = {"station": "KTPA", "target_date": "2026-09-29", "generated_at_utc": "2026-09-28T22:39:00+00:00",
            "models": {"GFS": fc(88), "CONSENSUS": fc(89)}}
    # gap-filling hindcast stamped 23Z, after the live run: adds USL, keeps the submitted values
    hind = {"station": "KTPA", "target_date": "2026-09-29", "generated_at_utc": "2026-09-28T23:00:00+00:00",
            "hindcast": True, "models": {"USL": fc(90), "GFS": fc(80), "CONSENSUS": fc(85)}}
    f = wxc_verify.forecasts_for_day([live, hind], "KTPA", "2026-09-29")
    assert f["CONSENSUS"][0]["tmax_f"] == 89 and not f["CONSENSUS"][2]
    assert f["GFS"][0]["tmax_f"] == 88
    assert f["USL"][0]["tmax_f"] == 90 and f["USL"][2]
    # a later live run still replaces an earlier one
    later = dict(live, generated_at_utc="2026-09-28T23:30:00+00:00", models={"GFS": fc(87)})
    assert wxc_verify.forecasts_for_day([live, hind, later], "KTPA", "2026-09-29")["GFS"][0]["tmax_f"] == 87


def test_hindcast_plan():
    ok = {"tmax_f": 88, "tmin_f": 72, "wind_max_kt": 8, "precip_in": 0.0}
    allm = ["HRRR", "IFS", "GFS", "NBM"]
    h1 = {"station": "KTPA", "target_date": "2026-09-27", "generated_at_utc": "2026-09-26T21:00:00+00:00",
          "hindcast": True, "models": {"HRRR": ok, "IFS": ok, "GFS": ok, "NBM": {"tmax_f": None, "error": "404"}}}
    assert wxc_verify.hindcast_plan([], "KTPA", "2026-09-27", allm) == allm
    assert wxc_verify.hindcast_plan([h1], "KTPA", "2026-09-27", allm) == ["NBM"]     # retry the gap
    assert wxc_verify.hindcast_plan([h1, dict(h1)], "KTPA", "2026-09-27", allm) == []  # gave up
    # a model added later is still hindcast for days that already have live forecasts
    live = {"station": "KTPA", "target_date": "2026-09-27", "generated_at_utc": "2026-09-26T20:00:00+00:00",
            "models": {m: ok for m in allm}}
    assert wxc_verify.hindcast_plan([live], "KTPA", "2026-09-27", allm + ["RRFS"]) == ["RRFS"]


def test_obs_is_final():
    now = datetime(2026, 9, 28, 20, tzinfo=timezone.utc)
    final = {"date": "2026-09-27", "complete": True, "final": True, "pending": [], "obs_method": wxc_obs.OBS_METHOD,
             "wind_source": "CLI", "source": {"wind_max_kt": "cli"}}
    assert wxc_verify.obs_is_final(final, True, now)
    # stored by the older method (no obs_method): fetched once more, even when old
    old = {"date": "2026-09-27", "complete": True, "wind_source": "CLI", "cli_preliminary": False,
           "precip_6h_in": {"06-12": 0.0, "12-18": 0.0, "18-00": 0.0, "00-06": 0.0}}
    assert not wxc_verify.obs_is_final(old, True, now)
    assert not wxc_verify.obs_is_final(dict(old, date="2026-09-24"), True, now)
    pend = dict(final, final=False, pending=["wind_max_kt"], source={"wind_max_kt": "pending"})
    assert not wxc_verify.obs_is_final(pend, True, now)
    assert wxc_verify.obs_is_final(dict(pend, date="2026-09-24"), True, now)        # gave up after 48 h
    assert not wxc_verify.obs_is_final(None, True, now)


def test_upsert_keeps_final_wind(tmp_path, monkeypatch):
    monkeypatch.setattr(wxc_verify, "OBS", tmp_path / "obs.jsonl")
    base = {"station": "KTPA", "date": "2026-10-01", "tmax_f": 88, "tmin_f": 74, "precip_in": 0.28,
            "complete": True, "obs_method": wxc_obs.OBS_METHOD}
    wxc_verify.upsert_observations([dict(base, wind_max_kt=14, wind_source="CLI", cli_wind_mph=16, final=True,
                                         pending=[], source={"tmax_f": "6h_group", "wind_max_kt": "cli"})])
    # a later fetch where the CLI failed: the wind stays the final CLI value
    wxc_verify.upsert_observations([dict(base, wind_max_kt=13, wind_source="pending (no final CLI)", final=False,
                                         pending=["wind_max_kt"], source={"tmax_f": "6h_group", "wind_max_kt": "pending"})])
    (r,) = wxc_verify.read_jsonl(wxc_verify.OBS)
    assert r["wind_max_kt"] == 14 and r["source"]["wind_max_kt"] == "cli" and r["final"] and r["pending"] == []
    # an old-method record with a final CLI wind is protected the same way
    assert wxc_verify.wind_is_final({"wind_source": "CLI", "cli_preliminary": False})
    assert not wxc_verify.wind_is_final({"wind_source": "CLI", "cli_preliminary": True})


def test_mos_candidate_runtimes():
    t = datetime(2026, 9, 27, 21, tzinfo=timezone.utc)
    assert [x.hour for x in wxc_mos.candidate_runtimes("GFS", t)] == [12, 6, 0]
    # NBS: every hourly cycle once its text is out (~1 h; 00/01/07/12/13/19Z ~1.7 h)
    assert [x.hour for x in wxc_mos.candidate_runtimes("NBS", t)] == [20, 19, 18]
    t = datetime(2026, 9, 27, 21, 50, tzinfo=timezone.utc)
    assert [x.hour for x in wxc_mos.candidate_runtimes("NBS", t, 2)] == [20, 19]
    t = datetime(2026, 9, 27, 21, 58, tzinfo=timezone.utc)
    assert [x.hour for x in wxc_mos.candidate_runtimes("NBS", t, 2)] == [21, 20]


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
    assert STATIONS["PAJN"].rrfs_domain == "ak" and STATIONS["KTPA"].rrfs_domain == "conus"
    assert STATIONS["KTPA"].wfo == "TBW" and STATIONS["KTPA"].afd_url == (
        "https://forecast.weather.gov/product.php?site=tbw&issuedby=tbw&product=afd"
        "&format=ci&version=1&glossary=1")
    assert STATIONS["KMSP"].afd_url == (
        "https://forecast.weather.gov/product.php?site=mpx&issuedby=mpx&product=afd"
        "&format=ci&version=1&glossary=1")
    assert Station("KXYZ", "Nowhere", 40.0, -100.0, tz="America/Chicago").afd_url is None


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
    MISSING = {}    # init (Timestamp) -> forecast hours "not posted yet"

    def __init__(self, dates, model, product, fxx, **kw):
        self.init, self.model, self.fxx, self.kw = pd.Timestamp(dates[0]), model, list(fxx), kw
        gone = self.MISSING.get(self.init, set())
        self.objects = [SimpleNamespace(fxx=f) for f in self.fxx]
        self.file_exists = [h for h in self.objects if h.fxx not in gone]
        self.searches = []                                  # what was read through this object

    def xarray(self, search, backend_kwargs=None, max_threads=None):
        self.searches.append(search)
        if search not in self.FIELDS:
            raise ValueError(f"no match for {search!r}")
        fields = self.FIELDS[search]
        import xarray as xr
        return xr.merge([_fake_grid_ds(var, self.fxx, self.init, [fn(f) for f in self.fxx], units)
                         for var, fn, units in (fields if isinstance(fields, list) else [fields])],
                        compat="override")


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
        ":APCP:surface:0-": ("tp", lambda h: 0.5 * h, "kg m**-2"),
        ":tp:": ("tp", lambda h: 0.0005 * h, "m"),
        ":10u:": ("u10", lambda h: 3.0, "m s**-1"), ":10v:": ("v10", lambda h: 4.0, "m s**-1"),
        "UGRD:10 m above ground": ("u10", lambda h: 3.0, "m s**-1"),
        "VGRD:10 m above ground": ("v10", lambda h: 4.0, "m s**-1"),
        # one search for both 10 m components (WIND_10M_NCEP / WIND_10M_ECMWF)
        ":[UV]GRD:10 m above ground:": [("u10", lambda h: 3.0, "m s**-1"), ("v10", lambda h: 4.0, "m s**-1")],
        ":10[uv]:": [("u10", lambda h: 3.0, "m s**-1"), ("v10", lambda h: 4.0, "m s**-1")],
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
    rrfs = m.fetch_rrfs(init, day, pts, st)["metrics"]
    assert rrfs["n_steps"] == 25 and rrfs["tmax_f"] == pytest.approx(86.0, abs=0.1)   # TMAX field used
    assert rrfs["precip_in"] == pytest.approx(0.5 * 24 * 0.0393701, abs=0.01)
    hrrr = m.fetch_hrrr(pd.Timestamp("2026-09-28 00:00"), day, pts, st)["metrics"]
    assert hrrr["partial_window"] and hrrr["valid_range_utc"][-1] == "2026-09-30T00"


def test_grib_fetch_reuses_one_herbie(fake_herbie, monkeypatch):
    """Max/min fields reuse the run's FastHerbie (no second round of file checks and .idx
    downloads), and 10 m U and V come in one search."""
    m = _main_module()
    made = []
    real_init = fake_herbie.__init__

    def counting_init(self, *a, **k):
        made.append(self)
        real_init(self, *a, **k)
    monkeypatch.setattr(fake_herbie, "__init__", counting_init)
    pts = pd.DataFrame({"longitude": [-82.5], "latitude": [28.0]})
    init = pd.Timestamp("2026-09-28 12:00")
    for fetch, wind, tmax in ((m.fetch_gfs, m.WIND_10M_NCEP, ":TMAX:2 m above"),
                              (m.fetch_ifs, m.WIND_10M_ECMWF, ":mx2t3:")):
        made.clear()
        res = fetch(init, date(2026, 9, 29), pts)
        assert len(made) == 1, fetch.__name__
        assert made[0].searches.count(wind) == 1 and tmax in made[0].searches
        assert res["metrics"]["wind_max_kt"] == pytest.approx(5 * 1.94384, abs=0.1)
        assert "note" not in res["metrics"] or "unavailable" not in res["metrics"]["note"]
    H = fake_herbie([init], "gfs", "x", [0, 3, 6])
    H2 = m.without_first_hour(H)
    assert H2.fxx == [3, 6] and [h.fxx for h in H2.file_exists] == [3, 6] and H.fxx == [0, 3, 6]
    assert H2.file_exists[0] is H.file_exists[1]          # same per-hour objects


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


def test_incomplete_cycle_falls_back_and_is_not_cached(fake_herbie, monkeypatch):
    """A cycle still being posted (late hours missing) must not be summarized from the hours
    that had arrived: use the previous complete cycle, and don't cache the partial one."""
    m = _main_module()
    import wxc_stations
    st = wxc_stations.get_station("KTPA")
    pts = pd.DataFrame({"longitude": [st.lon], "latitude": [st.lat]})
    new, old = pd.Timestamp("2026-10-01 00:00"), pd.Timestamp("2026-09-30 18:00")
    monkeypatch.setattr(m, "get_latest_forecast_cycle", lambda model, now=None: new)
    monkeypatch.setattr(FakeFastHerbie, "MISSING", {new: set(range(41, 49))})   # f41-f48 not posted
    with pytest.raises(m.IncompleteCycle, match="8 of 19"):
        m.fetch_hrrr(new, date(2026, 10, 2), pts, st)
    res = m.fetch_with_fallback("HRRR", "HRRR", m.fetch_hrrr, date(2026, 10, 2), pts, st)
    assert res["metrics"]["init_time_utc"].startswith("2026-09-30T18")
    assert "used previous" in res["metrics"]["note"]
    assert m.wxc_cache.load("KTPA", "HRRR", new, date(2026, 10, 2)) is None
    monkeypatch.setattr(FakeFastHerbie, "MISSING", {})
    res = m.fetch_with_fallback("HRRR", "HRRR", m.fetch_hrrr, date(2026, 10, 2), pts, st)
    assert res["metrics"]["init_time_utc"].startswith("2026-10-01T00")     # complete now: refetched
    assert res["metrics"]["valid_range_utc"][1].startswith("2026-10-03T00")


def test_fallback_to_previous_cycle(fake_herbie, monkeypatch):
    m = _main_module()
    calls = []

    def flaky(init, day, pts, st, partial=False):
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
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns("tests", "__pycache__", "*.ipynb", "images", "data", "cache"))
    monkeypatch.syspath_prepend(str(work))
    for name in ["functions", "wxc_obs", "wxc_mos", "wxc_verify", "wxc_stations", "wxc_timeline",
                 "getForecast_wxChallenge-pushGitHub"]:
        sys.modules.pop(name, None)
    import wxc_obs as o, wxc_mos as mo, wxc_verify as v  # noqa: E401
    m = importlib.import_module("getForecast_wxChallenge-pushGitHub")

    # observations: KSAV fixture relabelled as KTPA, "now" = 2025-09-29 20Z
    ks = pd.read_csv(KSAV)[["valid", "metar"]]
    ks_all = pd.read_csv(KSAV)[["valid", "metar"]]                 # the fixture includes specials
    monkeypatch.setattr(o, "fetch_metars", lambda st, a, b, specials=False: ks_all if specials else ks)
    monkeypatch.setattr(o, "get_cli", lambda st, first, last, now=None: o.parse_cli(
        CLI_TEXT.replace("SEPTEMBER 27 2026", "SEPTEMBER 27 2025"), st.lst_offset_hours))
    monkeypatch.setattr(o, "fetch_cf6", lambda icao, years: {})
    monkeypatch.setattr(o, "_get", lambda *a, **k: pytest.fail("network call in an offline test"))
    monkeypatch.setattr(mo, "fetch_mos", lambda st, model, runtime=None: _mos_rows(model).assign(
        runtime="2025-09-28 12:00",
        ftime=lambda d: (pd.to_datetime(d["ftime"]) - pd.Timedelta(days=365)).dt.strftime("%Y-%m-%d %H:%M")))
    monkeypatch.setattr(mo.wxc_nbm_text, "fetch", lambda icao, prod, init: pd.DataFrame())   # no NBM cloud here
    fixed = datetime(2025, 9, 28, 20, 0, tzinfo=timezone.utc)
    import wxc_usl as us
    monkeypatch.setattr(us, "_get", lambda url: None)     # no USL page for this fake period
    import wxc_ens as en
    monkeypatch.setattr(en, "latest_init", lambda model: datetime(2025, 9, 28, 0, tzinfo=timezone.utc))
    monkeypatch.setattr(en, "_get_json", lambda url, params=None: _openmeteo("2025-09-28"))
    from test_ifs_hres import single_run
    hr = m.wxc_ifs_hres                                  # IFS HRES 9 km (Open-Meteo single runs)
    monkeypatch.setattr(hr, "_get_json", lambda url, params=None: (
        {"last_run_initialisation_time": int(datetime(2025, 9, 28, 6, tzinfo=timezone.utc).timestamp())}
        if url == hr.META else single_run(params["run"])))
    import wxc_cam_ens as ce
    cam_init = datetime(2025, 9, 28, 12, tzinfo=timezone.utc)
    monkeypatch.setattr(ce, "get_refs", lambda st, day, now: ce._result(
        "REFS", cam_init, day, ["a", "b", "c"], [0.0, 0.12, 0.4], "test"))
    monkeypatch.setattr(ce, "get_hrrrcast", lambda st, day, now: ce._fail("not posted", cam_init))
    import wxc_nbm_qmd as nq
    monkeypatch.setattr(nq, "get_qmd", lambda st, day, now=None: {
        **nq._fail("", cam_init), "error": None, "precip_in": 0.05,
        "pop": nq.summarize({"p24": 62.0, "q10": 0.0, "q50": 1.27, "b:06-12": 5.0, "b:12-18": 40.0,
                             "b:18-00": 50.0, "b:00-06": 10.0})})

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
    monkeypatch.setattr(sys, "argv", ["x", "KTPA", "--no-push", "--obs-days", "3", "--hindcast-days", "4"])
    m.main()

    fc = json.loads((work / "data/wxchallenge/forecast.json").read_text())
    assert fc["meta"]["target_date"] == "2025-09-29" and fc["meta"]["station"] == "KTPA"
    for k in ["HRRR", "RRFS", "IFS", "GFS", "AIFS", "GFS_MOS", "NBM", "ENS", "AIFS_ENS", "CONSENSUS"]:
        assert "NAM_MOS" not in fc["models"]
        assert fc["models"][k].get("tmax_f") is not None, k
    ver = json.loads((work / "data/wxchallenge/verification.json").read_text())
    d27 = [d for d in ver["days"] if d["date"] == "2025-09-27"][0]
    assert d27["wind_source"] == "CLI" and d27["obs"]["wind_max_kt"] == 10
    assert d27["obs_source"]["wind_max_kt"] == "cli" and d27["obs_pending"] == []
    assert d27["models"]["GFS"]["points"] == pytest.approx(2 + 1 + 1 + wxc_verify.precip_points(0.1, 0.02))
    runs = wxc_verify.read_jsonl(work / "data/wxchallenge/runs.jsonl")
    assert runs[-1]["target_date"] == "2025-09-29" and "series" not in json.dumps(runs[-1])
    assert (work / "images/wxchallenge/latest.png").exists()
    assert (work / "images/wxchallenge/verification.png").exists()
    # "today so far": pre-deadline series rebuilt for 9/28, latest runs for the rest of the day
    assert (work / "images/wxchallenge/today.png").exists()
    tj = json.loads((work / "data/wxchallenge/today.json").read_text())
    assert tj["models"] and "temp_bias" in next(iter(tj["models"].values()))
    assert fc["models"]["ENS"]["ensemble"]["stats"]["precip_prob"]["0.01"] > 0
    assert fc["models"]["REFS"]["precip_in"] == 0.12 and fc["models"]["REFS"]["tmax_f"] is None
    assert fc["models"]["HRRRCAST"]["error"] == "not posted"
    assert not {"REFS", "HRRRCAST", "NBM_QMD", "GEFS"} & set(fc["models"]["CONSENSUS"]["method"]["precip_in"]["members"])
    assert fc["models"]["GEFS"]["tmax_f"] is not None                    # shown, just not blended
    assert fc["models"]["IFS_HRES"]["tmax_f"] == 60.0 and fc["models"]["IFS_HRES"]["init_time_utc"] == "2025-09-28T06"
    assert all("IFS_HRES" not in d.get("members", []) for d in fc["models"]["CONSENSUS"]["method"].values())
    # PoP: MOS bounds from P06, QMD from the (faked) file values; kept in runs.jsonl for live runs
    assert fc["models"]["NBM"]["pop"]["p24"] is None and fc["models"]["NBM"]["pop"]["p24_range"] == [0.3, pytest.approx(1 - 0.7 ** 4, abs=1e-3)]
    assert fc["models"]["NBM_QMD"]["pop"]["p24"] == 0.62 and fc["models"]["NBM_QMD"]["pop"]["q24_in"]["50"] == 0.05
    assert runs[-1]["models"]["NBM_QMD"]["pop"]["blocks"]["18-00"] == 0.5
    assert all("pop" not in mm for r in runs if r.get("hindcast") for mm in r["models"].values())
    sub = v.load_series("KTPA", date(2025, 9, 28), "submitted")
    lat = v.load_series("KTPA", date(2025, 9, 28), "latest")
    assert sub["hindcast"] and {"HRRR", "RRFS", "IFS", "GFS", "AIFS"} <= set(sub["models"])
    assert set(lat["models"]) <= set(m.TODAY_LATEST) and "HRRR" in lat["models"]
    assert v.load_series("KTPA", date(2025, 9, 29), "submitted")["models"]["IFS"]["times"][0] == "2025-09-29T06:00"

    # ---- second run: stored obs are reused where final, hindcasts are not repeated ----
    n_runs = len(runs)
    hind = [r for r in runs if r.get("hindcast")]
    assert {r["target_date"] for r in hind} == {"2025-09-24", "2025-09-25", "2025-09-26", "2025-09-27"}
    assert all(r["models"]["IFS_HRES"]["init_time_utc"] == f"{date.fromisoformat(r['target_date']) - timedelta(days=1)}T12"
               for r in hind)                       # hindcast from the archived 12Z run
    fetched = []
    monkeypatch.setattr(o, "fetch_metars",
                        lambda st, a, b, specials=False: (fetched.append((a, b)) or ks_all) if specials else ks)
    m.main()
    runs2 = wxc_verify.read_jsonl(work / "data/wxchallenge/runs.jsonl")
    # the live run + one retry per day for the MOS products the fake API couldn't supply
    retries = [r for r in runs2[n_runs:] if r.get("hindcast")]
    assert len(runs2) == n_runs + 1 + 4 and all(set(r["models"]) <= {"GFS_MOS", "NBM", "USL", "CONSENSUS"}
                                                 for r in retries)
    m.main()                                            # third run: nothing left to retry
    assert len(wxc_verify.read_jsonl(work / "data/wxchallenge/runs.jsonl")) == len(runs2) + 1
    # 9/24-25 are final (>48 h old) and 9/27 has a final CLI: only 9/26 is re-fetched
    assert len(fetched) >= 1 and fetched[0][0].date() == date(2025, 9, 26) and fetched[0][1].date() == date(2025, 9, 27)

    # ---- an hour later the text guidance and Open-Meteo can't be reached (laptop offline):
    # the page keeps their last forecasts, flagged; runs.jsonl records the failures ----
    fc1 = json.loads((work / "data/wxchallenge/forecast.json").read_text())

    def offline(*a, **k):
        raise ConnectionError("HTTPSConnectionPool(host='x', port=443): Max retries exceeded with url: /")
    monkeypatch.setattr(mo, "fetch_mos", offline)
    monkeypatch.setattr(en, "_get_json", offline)
    monkeypatch.setattr(en, "latest_init", offline)
    fixed += timedelta(hours=1)
    m.main()
    fc2 = json.loads((work / "data/wxchallenge/forecast.json").read_text())
    for k in ["GFS_MOS", "NBM", "ENS"]:
        assert fc2["models"][k]["tmax_f"] == fc1["models"][k]["tmax_f"], k
        assert fc2["models"][k]["stale"]["fetched_at_utc"] == fc1["generated_at_utc"]
    assert "stale" not in fc2["models"]["HRRR"] and fc2["models"]["CONSENSUS"]["tmax_f"] is not None
    st = fc2["run_status"]
    assert st["ok"] is False and st["connectivity"] and {"GFS_MOS", "NBM", "ENS"} <= set(st["carried_over"])
    last = wxc_verify.read_jsonl(work / "data/wxchallenge/runs.jsonl")[-1]
    assert "Max retries" in last["models"]["NBM"]["error"] and last["models"]["NBM"]["tmax_f"] is None


# ----------------------------------------------------------------- cache
def test_cache_roundtrip_and_reuse(fake_herbie, monkeypatch):
    import wxc_cache
    m = _main_module()
    monkeypatch.setattr(m, "wxc_cache", wxc_cache)
    monkeypatch.setattr(m, "get_latest_forecast_cycle", lambda model, now=None: pd.Timestamp("2026-09-28 12:00"))
    calls = []

    def counting(init, day, pts, st, partial=False):
        calls.append(init)
        return m.fetch_ifs(init, day, pts)
    pts = pd.DataFrame({"longitude": [STATIONS["KTPA"].lon], "latitude": [STATIONS["KTPA"].lat]})
    a = m.fetch_with_fallback("IFS", "IFS", counting, date(2026, 9, 29), pts, STATIONS["KTPA"])
    b = m.fetch_with_fallback("IFS", "IFS", counting, date(2026, 9, 29), pts, STATIONS["KTPA"])
    assert len(calls) == 1                                   # second run reused the saved result
    assert b["metrics"] == a["metrics"]
    assert list(b["series"]["temp_f"]) == pytest.approx(list(a["series"]["temp_f"]))
    assert b["series"]["times"][0] == a["series"]["times"][0]


# ----------------------------------------------------------------- ensembles
def _openmeteo(day0="2026-09-29", seed=1, humid=True):
    rng = np.random.default_rng(seed)
    times = pd.date_range(f"{day0} 00:00", periods=96, freq="h")
    hourly = {"time": [t.strftime("%Y-%m-%dT%H:%M") for t in times]}
    hrs = np.arange(96)
    # key suffixes as the real API names them in a combined request (GEFS has no "_ensemble")
    for model, suffix, n in (("ecmwf_ifs025", "_ecmwf_ifs025_ensemble", 51), ("ecmwf_aifs025", "_ecmwf_aifs025_ensemble", 51),
                             ("ncep_gefs025", "_ncep_gefs025", 31)):
        for mem in range(n):
            tag = "" if mem == 0 else f"_member{mem:02d}"
            off = rng.normal(0, 2)
            hourly[f"temperature_2m{tag}{suffix}"] = list(80 + off + 8 * np.sin(2 * np.pi * (hrs - 12) / 24))
            hourly[f"wind_speed_10m{tag}{suffix}"] = list(6 + rng.random(96) * 4)
            wet = mem % 4 == 0                           # 13 of 51 members bring 0.02"/h for 10 h
            p = np.zeros(96)
            if wet:
                p[40:50] = 0.02                          # 16-01Z of the day after day0
            hourly[f"precipitation{tag}{suffix}"] = list(p)
            if humid:                                    # display-only fields (dewpoint, RH, cloud)
                hourly[f"dew_point_2m{tag}{suffix}"] = [60.0 + mem % 2] * 96
                hourly[f"relative_humidity_2m{tag}{suffix}"] = [70.0 + 10 * (mem % 2)] * 96
                hourly[f"cloud_cover{tag}{suffix}"] = [None] * 3 + [float(mem % 2) * 100] * 93
    return {"hourly": hourly}


def test_ensemble_summary(monkeypatch):
    import wxc_ens
    data = _openmeteo()
    summ = wxc_ens.summarize_members(data["hourly"], "ecmwf_ifs025", date(2026, 9, 30))
    assert summ["n_members"] == 51
    st = summ["stats"]
    assert st["precip_prob"]["0.01"] == pytest.approx(13 / 51, abs=1e-3)
    assert st["precip_prob"]["0.25"] == 0 and st["precip_in"]["p100"] == pytest.approx(0.20)
    assert st["tmax_f"]["p10"] <= st["tmax_f"]["p50"] <= st["tmax_f"]["p90"]
    assert len(summ["series"]["tmp_f"]) == 25
    # PoP: member fractions; wet hours 16Z-01Z -> blocks 12-18 and 18-00 wet, 00-06 gets 01Z
    pop = summ["pop"]
    assert pop["p24"] == pytest.approx(13 / 51, abs=1e-3) and pop["n_members"] == 51
    assert pop["blocks"] == {"06-12": 0.0, "12-18": pytest.approx(13 / 51, abs=1e-3),
                             "18-00": pytest.approx(13 / 51, abs=1e-3), "00-06": pytest.approx(13 / 51, abs=1e-3)}
    # the AIFS keys must not leak into the IFS summary (ifs025 is a substring of aifs025)
    assert len(wxc_ens.members(data["hourly"], "temperature_2m", "ecmwf_ifs025")) == 51
    # a single-model request comes back without the model suffix ("temperature_2m_member01")
    single = {"time": data["hourly"]["time"]}
    single.update({k.replace("_ecmwf_ifs025_ensemble", ""): v for k, v in data["hourly"].items()
                   if k.endswith("_ecmwf_ifs025_ensemble")})
    s1 = wxc_ens.summarize_members(single, "ecmwf_ifs025", date(2026, 9, 30))
    assert s1["n_members"] == 51 and s1["stats"] == summ["stats"]
    # dewpoint / RH member means over the day, the cloud cover mean over the whole response
    # (members alternate 60/61 F, 70/80 %, 0/100 %: 26 odd of 51); an hour with no member is None
    s = summ["series"]
    assert s["dpt_f"] == [60.5] * 25 and s["rh_pct"] == [75.0] * 25
    assert len(summ["cloud"]["times"]) == 96 and summ["cloud"]["cloud_pct"][:3] == [None] * 3
    assert summ["cloud"]["cloud_pct"][3] == pytest.approx(100 * 25 / 51)
    # a response without them (or a member missing one) still gives the forecast, without them
    dry = wxc_ens.summarize_members(_openmeteo(humid=False)["hourly"], "ecmwf_ifs025", date(2026, 9, 30))
    assert dry["stats"] == summ["stats"] and dry["cloud"] is None
    assert "dpt_f" not in dry["series"] and "rh_pct" not in dry["series"]
    part = {k: v for k, v in data["hourly"].items() if k != "dew_point_2m_member03_ecmwf_ifs025_ensemble"}
    p1 = wxc_ens.summarize_members(part, "ecmwf_ifs025", date(2026, 9, 30))
    assert "dpt_f" not in p1["series"] and p1["series"]["rh_pct"] == [75.0] * 25
    with pytest.raises(ValueError, match="no ecmwf_aifs025 ensemble members"):
        wxc_ens.summarize_members({"time": data["hourly"]["time"]}, "ecmwf_aifs025", date(2026, 9, 30))

    calls = []
    monkeypatch.setattr(wxc_ens, "latest_init", lambda model: datetime(2026, 9, 29, 0, tzinfo=timezone.utc))
    monkeypatch.setattr(wxc_ens, "_get_json", lambda url, params=None: calls.append(params) or data)
    out = wxc_ens.get_ensembles(STATIONS["KTPA"], date(2026, 9, 30))
    assert out["ENS"]["init_time_utc"] == "2026-09-29T00" and "ensemble" in out["AIFS_ENS"]
    assert out["GEFS"]["ensemble"]["n_members"] == 31 and out["GEFS"]["pop"]["n_members"] == 31
    assert "GEPS" not in out
    assert "not in the consensus" in out["GEFS"]["note"] and "not in" not in out["ENS"]["note"]
    assert "dew_point_2m" in calls[0]["hourly"] and "cloud_cover" in calls[0]["hourly"]
    assert "cloud" not in out["ENS"] and out["ENS"]["series"]["rh_pct"][0] == 75.0
    import wxc_clouds
    c = wxc_clouds.load_cloud("KTPA", "GEFS", datetime(2026, 9, 29, 0))   # cloud cover: its own file
    assert c["model"] == "GEFS" and c["init_time_utc"] == "2026-09-29T00" and len(c["times"]) == 93
    wxc_ens.get_ensembles(STATIONS["KTPA"], date(2026, 9, 30))
    assert len(calls) == 1                                   # second call served from the cache

    # a rejected combined request falls back to one request per model
    import wxc_cache
    monkeypatch.setattr(wxc_cache, "ENABLED", False)
    def flaky(url, params=None):
        if "," in params["models"] or params["models"] == "ncep_gefs025":
            raise RuntimeError("400 bad model")
        return data
    monkeypatch.setattr(wxc_ens, "_get_json", flaky)
    out = wxc_ens.get_ensembles(STATIONS["KTPA"], date(2026, 9, 30))
    assert "ensemble" in out["ENS"] and "ensemble" in out["AIFS_ENS"] and "400 bad model" in out["GEFS"]["error"]
    assert "no hindcast" in wxc_ens.get_ensembles(STATIONS["KTPA"], date(2026, 9, 30),
                                                  as_of=datetime(2026, 9, 29, 21, tzinfo=timezone.utc))["ENS"]["error"]


# ----------------------------------------------------------------- today bias
def test_today_bias():
    import wxc_today
    obs = wxc_obs.report_series(pd.read_csv(KSAV)[["valid", "metar"]])
    day = date(2025, 9, 18)
    r_ = obs[obs["routine"] & (obs["valid"] >= "2025-09-18 06:00") & (obs["valid"] <= "2025-09-19 06:00")]
    t = list(r_["valid"])
    sub = {"models": {"WARM": {"init_time_utc": "2025-09-17T12", "times": [x.strftime("%Y-%m-%dT%H:%M") for x in t],
                               "temp_f": list(r_["temp_f"] + 2), "wind_kt": [5.0] * len(t), "precip_in": [0.0] * len(t)}}}
    b = wxc_today.today_bias(obs, sub, day, datetime(2025, 9, 18, 20, tzinfo=timezone.utc))
    r = b["models"]["WARM"]
    assert r["temp_bias"] == pytest.approx(2.0, abs=0.05) and r["temp_mae"] == pytest.approx(2.0, abs=0.05)
    assert r["high_err"] == pytest.approx(2.0, abs=1.0)     # obs high also uses 6-h max groups
    assert r["precip_err"] == 0.0 and b["through_utc"].startswith("2025-09-18T19:53")


def test_today_bias_uses_scored_daily_values_and_pending():
    """High/low use the model's daily (summary) values, greyed until the model's time for them."""
    import wxc_today
    obs = wxc_obs.report_series(pd.read_csv(KSAV)[["valid", "metar"]])
    day = date(2025, 9, 18)
    r_ = obs[obs["routine"] & (obs["valid"] >= "2025-09-18 06:00") & (obs["valid"] <= "2025-09-19 06:00")]
    t, temps = list(r_["valid"]), list(r_["temp_f"])
    i_hi = int(pd.Series(temps).idxmax())
    s = {"init_time_utc": "2025-09-17T22", "times": [x.strftime("%Y-%m-%dT%H:%M") for x in t],
         "temp_f": temps, "wind_kt": [5.0] * len(t), "precip_in": [0.0] * len(t)}
    obs_hi = wxc_today._so_far(obs[(obs["valid"] > "2025-09-18 06:00") & (obs["valid"] <= "2025-09-19 06:00")])
    # summary goes 2 beyond the hourly extremes (like the USL daily summary)
    s["tmax_f"], s["tmin_f"] = max(temps) + 2, min(temps) - 2
    early = datetime(2025, 9, 18, 9, tzinfo=timezone.utc)          # before the forecast high time
    b = wxc_today.today_bias(obs, {"models": {"USL": s}}, day, early)["models"]["USL"]
    assert b["high_fcst"] == pytest.approx(max(temps) + 2, abs=0.05) and b["high_source"] == "daily"
    assert b["high_pending"] is True and b["high_at"] == t[i_hi].strftime("%Y-%m-%dT%H:%M")
    late = datetime(2025, 9, 19, 6, tzinfo=timezone.utc)           # whole day observed
    b = wxc_today.today_bias(obs, {"models": {"USL": s}}, day, late)["models"]["USL"]
    assert b["high_pending"] is False and b["low_pending"] is False
    assert b["low_fcst"] == pytest.approx(min(temps) - 2, abs=0.05)
    assert b["high_err"] == pytest.approx(max(temps) + 2 - obs_hi["high"], abs=0.05)
    # the observed low already below the forecast low settles it even early in the day
    s2 = {**s, "tmin_f": min(temps) + 10}
    b = wxc_today.today_bias(obs, {"models": {"X": s2}}, day, early)["models"]["X"]
    assert b["low_pending"] is False and b["low_err"] > 0
    # series without daily values fall back to the hourly extreme
    s3 = {k: v for k, v in s.items() if k not in ("tmax_f", "tmin_f")}
    b = wxc_today.today_bias(obs, {"models": {"X": s3}}, day, late)["models"]["X"]
    assert b["high_source"] == "hourly" and b["high_fcst"] == pytest.approx(max(temps), abs=0.05)


# ----------------------------------------------------------------- 3 km precip ensembles
GRID_SAMPLE = HERE / "fixtures" / "hrrrcast_grid_sample.grib2"   # one real HRRRCast message (CFRZR)


@__import__("functools").lru_cache(maxsize=None)
def _grib(value):
    """A HRRRCast-grid GRIB2 message with the same value everywhere."""
    import eccodes
    g = eccodes.codes_new_from_message(GRID_SAMPLE.read_bytes())
    try:
        eccodes.codes_set_values(g, np.full(eccodes.codes_get(g, "numberOfDataPoints"), float(value)))
        return eccodes.codes_get_message(g)
    finally:
        eccodes.codes_release(g)


class FakeRemote:
    """url -> list of (idx descriptor, value); serves .idx text and byte ranges like S3/NOMADS."""
    def __init__(self):
        self.files, self.gets = {}, []

    def add(self, url, fields):
        blob, lines = b"", []
        for i, (desc, val) in enumerate(fields, 1):
            lines.append(f"{i}:{len(blob)}:d=2026093012:{desc}:")
            blob += _grib(val)
        self.files[url] = (blob, "\n".join(lines) + "\n")

    def get(self, url, headers=None, timeout=60):
        self.gets.append(url)
        class R:
            pass
        r = R()
        if url.endswith(".idx"):
            if url[:-4] not in self.files:
                raise FileNotFoundError(url)
            r.text = self.files[url[:-4]][1]
            return r
        blob = self.files[url][0]
        a, b = headers["Range"][6:].split("-")
        r.content = blob[int(a): int(b) + 1 if b else None]
        return r


def test_cam_ens_leads_and_cycles():
    import wxc_cam_ens as ce
    d = date(2026, 10, 1)
    assert ce.leads(datetime(2026, 9, 30, 12, tzinfo=timezone.utc), d) == (18, 42)
    now = datetime(2026, 9, 30, 21, 5, tzinfo=timezone.utc)
    got = ce.candidate_inits(d, now, 48)
    assert [t.hour for t in got] == [18, 12, 6] and got[-1].day == 30   # 00Z would need f54
    assert ce.acc_hours("26:1:d=x:APCP:surface:0-2 day acc fcst:ENS=+1") == 48
    assert ce.acc_hours("25:1:d=x:APCP:surface:29-30 hour acc fcst:") is None
    st = ce.ens_stats([0, 0, 0.004, 0.05, 0.3])
    assert st["precip_prob"]["0.01"] == pytest.approx(0.4) and st["precip_in"]["p50"] == pytest.approx(0.004)


def test_hrrrcast_precip_sum_and_cycle(monkeypatch):
    import wxc_cam_ens as ce
    fake = FakeRemote()
    init = datetime(2026, 9, 30, 12, tzinfo=timezone.utc)
    # member k rains k/10 mm every hour; 06Z cycle is incomplete (m17 missing) -> 12Z is used
    for k, m in enumerate(ce.HRRRCAST_MEMBERS):
        for fh in range(19, 43):
            fake.add(ce._hrrrcast_url(init, m, fh), [(f"APCP:surface:{fh} hour fcst", k / 10),
                                                     (f"TMP:2 m above ground:{fh} hour fcst", 290)])
    monkeypatch.setattr(ce.PointReader, "get", lambda self, url, headers=None, timeout=60: fake.get(url, headers))
    now = datetime(2026, 9, 30, 21, tzinfo=timezone.utc)
    st = STATIONS["KTPA"]
    res = ce.get_hrrrcast(st, date(2026, 10, 1), now)
    assert "error" not in res, res.get("error")
    assert res["init_time_utc"] == "2026-09-30T12" and res["ensemble"]["n_members"] == 18
    tot = [24 * k / 10 / 25.4 for k in range(18)]
    assert res["ensemble"]["members"]["precip_in"] == pytest.approx([round(t, 3) for t in tot], abs=1e-3)
    assert res["precip_in"] == round(float(np.median(tot)), 2) and res["tmax_f"] is None
    # PoP from the same hourly values: member 0 is dry, every other member wet in every block
    assert res["pop"]["p24"] == pytest.approx(17 / 18, abs=1e-3)
    assert list(res["pop"]["blocks"].values()) == [pytest.approx(17 / 18, abs=1e-3)] * 4
    # stored point values: a second call downloads nothing (result cache), and even without the
    # result cache the GRIB messages are not fetched again
    n = len([u for u in fake.gets if not u.endswith(".idx")])
    assert n == 18 * 24
    ce.get_hrrrcast(st, date(2026, 10, 1), now)
    import wxc_cache
    for f in (wxc_cache.CACHE_DIR / "KTPA").glob("HRRRCAST_*.json"):
        f.unlink()
    ce.get_hrrrcast(st, date(2026, 10, 1), now)
    assert len([u for u in fake.gets if not u.endswith(".idx")]) == n


def test_refs_members_and_precip(monkeypatch):
    import wxc_cam_ens as ce
    fake = FakeRemote()
    st = STATIONS["KTPA"]
    day = date(2026, 10, 1)
    init = datetime(2026, 9, 30, 12, tzinfo=timezone.utc)
    lag = init - pd.Timedelta(hours=6)
    mem = ce.refs_members(st, init, "para", day) + ce.refs_members(st, lag, "para", day)
    assert len(mem) == 14 and sum(n.startswith("HRRR") for n, _, _ in mem) == 2
    # 06Z cycle: its 00Z lagged HRRR would need f54 (> f48), so 13 members
    assert len(ce.refs_members(st, lag, "para", day) + ce.refs_members(st, lag - pd.Timedelta(hours=6), "para", day)) == 13
    for i, (name, ue, us) in enumerate(mem):
        e = ce.leads(init if "12Z" in name else lag, day)[1]
        s = e - 24
        # accumulated since init: 1 mm/h for member i*0.1 extra
        rate = 0.5 + 0.1 * i
        fake.add(ue, [(f"APCP:surface:{e - 1}-{e} hour acc fcst", rate), (f"APCP:surface:0-{e} hour acc fcst", rate * e)])
        fake.add(us, [(f"APCP:surface:{s - 1}-{s} hour acc fcst", rate), (f"APCP:surface:0-{s} hour acc fcst", rate * s)])
    # the pick step only looks at the RRFS ensemble files of the newest cycle
    monkeypatch.setattr(ce.PointReader, "get", lambda self, url, headers=None, timeout=60: fake.get(url, headers))
    monkeypatch.setattr(ce, "RRFS_STAGES", ("para",))
    res = ce.get_refs(st, day, datetime(2026, 9, 30, 16, tzinfo=timezone.utc))
    assert "error" not in res, res.get("error")
    assert res["ensemble"]["n_members"] == 14 and res["init_time_utc"] == "2026-09-30T12"
    want = sorted((0.5 + 0.1 * i) * 24 / 25.4 for i in range(14))
    assert sorted(res["ensemble"]["members"]["precip_in"]) == pytest.approx(want, abs=1e-3)
    assert "12Z + 06Z runs" in res["note"]


def test_cam_ens_outside_grid(monkeypatch):
    import wxc_cam_ens as ce
    r = ce.PointReader(21.3, -157.9)           # Honolulu is off the CONUS grid
    with pytest.raises(ValueError, match="outside"):
        r.decode(_grib(1.0))
    assert "CONUS" in ce.get_hrrrcast(STATIONS["PHNL"] if "PHNL" in STATIONS else
                                      type("S", (), {"hrrr_model": None})(), date(2026, 10, 1),
                                      datetime(2026, 9, 30, tzinfo=timezone.utc))["error"]
