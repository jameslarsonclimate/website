"""Per-cycle scores for the scoreboard's 12Z/18Z toggle (wxc_verify.CYCLES; display only):
each model's 12Z and 18Z runs from the day before scored on their own, from runs.jsonl or the
backfilled cycle_runs.jsonl, without touching the submitted scores or the summary."""
import copy
from datetime import datetime

import wxc_verify

DAY = "2026-10-28"
OBS = {"tmax_f": 60, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0}


def fc(init, tmax=60, **kw):
    return {"tmax_f": tmax, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0, "init_time_utc": init, **kw}


def run(t, models, hindcast=False, day=DAY):
    r = {"station": "KMSP", "target_date": day, "generated_at_utc": t, "models": models}
    if hindcast:
        r["hindcast"] = True
    return r


RUNS = [
    run("2026-10-27T15:00:00+00:00", {"GFS": fc("2026-10-27T12", 62), "NBM": fc("2026-10-27T13", 61),
                                      "USL": fc("2026-10-27T12", 59)}),
    run("2026-10-27T23:30:00+00:00", {"GFS": fc("2026-10-27T18", 57), "NBM": fc("2026-10-27T22", 60),
                                      "USL": fc("2026-10-27T22", 60), "IFS": fc("2026-10-27T12", 63)}),
    run("2026-10-28T01:00:00+00:00", {"GFS": fc("2026-10-28T00", 70)}),        # after the deadline
]


def test_cycle_forecasts_pick_each_cycles_run():
    c = wxc_verify.cycle_forecasts(RUNS, [], "KMSP", DAY)
    assert c["GFS"][12]["tmax_f"] == 62 and c["GFS"][18]["tmax_f"] == 57
    assert c["USL"] == {12: RUNS[0]["models"]["USL"], 22: RUNS[1]["models"]["USL"]}
    assert set(c["IFS"]) == {12}
    assert "NBM" not in c          # 13Z and 22Z are neither 12Z nor 18Z (12Z/18Z come from the backfill)


def test_backfilled_rows_fill_gaps_but_never_replace_stored_runs():
    rows = [{"station": "KMSP", "target_date": DAY, "model": "NBM", "init_time_utc": "2026-10-27T12",
             "tmax_f": 58, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0},
            {"station": "KMSP", "target_date": DAY, "model": "GFS", "init_time_utc": "2026-10-27T12",
             "tmax_f": 99, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0},
            {"station": "KMSP", "target_date": DAY, "model": "NBM", "init_time_utc": "2026-10-27T18",
             "error": "not found"}]
    c = wxc_verify.cycle_forecasts(RUNS, rows, "KMSP", DAY)
    assert c["NBM"][12]["tmax_f"] == 58 and 18 not in c["NBM"]
    assert c["GFS"][12]["tmax_f"] == 62


def test_live_run_preferred_over_hindcast_of_the_same_cycle():
    runs = [run("2026-10-27T20:00:00+00:00", {"GFS": fc("2026-10-27T12", 62)}),
            run("2026-10-27T23:00:00+00:00", {"GFS": fc("2026-10-27T12", 66)}, hindcast=True)]
    assert wxc_verify.cycle_forecasts(runs, [], "KMSP", DAY)["GFS"][12]["tmax_f"] == 62


def test_attach_cycles_leaves_the_submitted_scores_alone():
    days = wxc_verify.scored_days("KMSP", runs=RUNS, obs=[{"station": "KMSP", "date": DAY, **OBS}])
    res = {"station": "KMSP", "days": days, "summary": wxc_verify.model_stats(days)}
    for d in res["days"]:
        d.pop("forecasts")
    before = copy.deepcopy(res)
    wxc_verify.attach_cycles(res, runs=RUNS, cycle_rows=[])
    assert res["days"][0]["models"] == before["days"][0]["models"]
    assert res["summary"] == before["summary"]
    cyc = res["days"][0]["cycles"]
    assert cyc["GFS"]["12"]["points"] == 2.0 and cyc["GFS"]["18"]["points"] == 3.0
    assert cyc["GFS"]["12"]["run"] == "2026-10-27T12" and "error" not in cyc["GFS"]["12"]
    assert res["cycle_summary"]["GFS|18"]["total_points"] == 3.0
    assert res["cycles_def"]["NBM"] == ["12", "18", "sub"] and res["cycles_def"]["USL"] == ["12", "22"]


def test_cycle_plan_skips_present_and_given_up_cycles():
    rows = [{"station": "KMSP", "target_date": DAY, "model": "NBM", "init_time_utc": "2026-10-27T18",
             "error": "not found"}] * wxc_verify.CYCLE_MAX_ATTEMPTS
    plan = wxc_verify.cycle_plan(RUNS, rows, "KMSP", [DAY], ["GFS", "NBM", "USL", "IFS"])
    assert plan == [(DAY, "NBM", datetime(2026, 10, 27, 12))]
