"""The forecast table's "earlier runs" toggle (wxc_verify.earlier_runs; display only): each
model's 12Z and 18Z runs (USL 12Z/22Z) for the day being forecast, read back from the runs
already pulled today. Nothing is fetched for it."""
import wxc_verify

DAY = "2026-11-06"


def fc(init, tmax=60, **kw):
    return {"tmax_f": tmax, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0, "init_time_utc": init, **kw}


def run(t, models, hindcast=False, day=DAY):
    r = {"station": "KMSP", "target_date": day, "generated_at_utc": t, "models": models}
    if hindcast:
        r["hindcast"] = True
    return r


RUNS = [
    run("2026-11-05T14:00:00+00:00", {"GFS": fc("2026-11-05T06", 50), "NBM": fc("2026-11-05T13", 51)}),
    run("2026-11-05T16:30:00+00:00", {"GFS": fc("2026-11-05T12", 52), "NBM": fc("2026-11-05T12", 53),
                                      "USL": fc("2026-11-05T12", 54),
                                      "REFS": {"precip_in": 0.1, "tmax_f": None, "init_time_utc": "2026-11-05T12"}}),
    run("2026-11-05T17:00:00+00:00", {"GFS": fc("2026-11-05T12", 55)}),            # a later pull wins
    run("2026-11-05T22:30:00+00:00", {"GFS": fc("2026-11-05T18", 56), "NBM": fc("2026-11-05T18", 57),
                                      "USL": fc("2026-11-05T22", 58), "HRRR": fc("2026-11-05T18", 1, stale={"x": 1})}),
    run("2026-11-05T22:40:00+00:00", {"GFS": fc("2026-11-05T12", 99)}, hindcast=True),
    run("2026-11-05T23:00:00+00:00", {"GFS": fc("2026-11-04T12", 99)}, day="2026-11-05"),  # another day
]


def test_picks_each_models_12z_and_18z_runs():
    e = wxc_verify.earlier_runs(RUNS, "KMSP", DAY)
    assert e["GFS"]["12"]["tmax_f"] == 55 and e["GFS"]["18"]["tmax_f"] == 56
    assert set(e["NBM"]) == {"12", "18"}                    # the hourly 13Z run is left out
    assert set(e["USL"]) == {"12", "22"} and e["USL"]["22"]["tmax_f"] == 58
    assert e["REFS"]["12"]["precip_in"] == 0.1              # precip-only models count too
    assert "HRRR" not in e                                  # a carried-over (stale) copy isn't a pull


def test_current_run_is_included():
    e = wxc_verify.earlier_runs(RUNS[:2], "KMSP", DAY, {"GFS": fc("2026-11-05T18", 61),
                                                        "CONSENSUS": {"tmax_f": 60, "init_time_utc": None}})
    assert e["GFS"]["18"]["tmax_f"] == 61 and "CONSENSUS" not in e


def test_backfilled_runs_fill_gaps_but_never_replace_pulled_ones():
    rows = [{"station": "KMSP", "target_date": DAY, "model": "NBM", "init_time_utc": "2026-11-05T12",
             "tmax_f": 70, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0},
            {"station": "KMSP", "target_date": DAY, "model": "GFS", "init_time_utc": "2026-11-05T12",
             "tmax_f": 99, "tmin_f": 40, "wind_max_kt": 10, "precip_in": 0.0},
            {"station": "KMSP", "target_date": DAY, "model": "HRRR", "init_time_utc": "2026-11-05T12",
             "error": "not found"}]
    runs = [r for r in RUNS if "NBM" not in r["models"] or r["models"]["NBM"]["init_time_utc"][11:13] != "12"]
    e = wxc_verify.earlier_runs(runs, "KMSP", DAY, cycle_rows=rows)
    assert e["NBM"]["12"]["tmax_f"] == 70 and e["GFS"]["12"]["tmax_f"] == 55 and "HRRR" not in e
