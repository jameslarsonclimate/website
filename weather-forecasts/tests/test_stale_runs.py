"""Stale model runs (Open-Meteo's ECMWF ensemble feed stalled on 10/11-10/12 2026 and the
pipeline kept submitting the 10/10 18Z ENS / AIFS ENS runs): not scored, not in the consensus,
flagged on fetch."""
from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace

import wxc_ens
import wxc_verify

OK = {"tmax_f": 80, "tmin_f": 60, "wind_max_kt": 10, "precip_in": 0.0}


def fc(init, **kw):
    return dict(OK, init_time_utc=init, **kw)


def run(t, models, day="2026-10-13", station="KOLM"):
    return {"station": station, "target_date": day, "generated_at_utc": t, "models": models}


def test_stale_run_not_scored_even_from_an_earlier_run():
    # KOLM 2026-10-13 as recorded: ENS stuck on 10/10 18Z (54 h old at the deadline)
    runs = [run("2026-10-12T17:00:00+00:00", {"ENS": fc("2026-10-10T18"), "IFS": fc("2026-10-12T06")}),
            run("2026-10-12T23:54:29+00:00", {"ENS": fc("2026-10-10T18", tmax_f=70),
                                              "AIFS_ENS": fc("2026-10-12T12"), "IFS": fc("2026-10-12T12"),
                                              "CONSENSUS": dict(OK)})]
    f = wxc_verify.forecasts_for_day(runs, "KOLM", "2026-10-13")
    assert "ENS" not in f                                   # neither the last run nor the 17Z copy
    assert f["IFS"][0]["init_time_utc"] == "2026-10-12T12"
    assert "AIFS_ENS" in f and "CONSENSUS" in f             # no init time: never too old


def test_run_age_limit_is_taken_at_the_deadline():
    day = "2026-10-06"
    runs = [run("2026-10-05T23:39:46+00:00", {"ENS": fc("2026-10-04T18"),        # 30 h: stale
                                              "AIFS_ENS": fc("2026-10-05T00"),   # 24 h: allowed
                                              "GFS": fc("2026-10-05T18")}, day=day, station="KTPA")]
    f = wxc_verify.forecasts_for_day(runs, "KTPA", day)
    assert set(f) == {"AIFS_ENS", "GFS"}


def test_consensus_drops_runs_too_old_at_run_time():
    # KTPA 2026-10-12 at the deadline: ENS/AIFS_ENS on 10/10 18Z are only 24 h behind the newest
    # member (inside STALE_HOURS) but 30 h old
    models = {"GFS": fc("2026-10-11T18", tmax_f=85), "IFS": fc("2026-10-11T12", tmax_f=85),
              "ENS": fc("2026-10-10T18", tmax_f=79), "AIFS_ENS": fc("2026-10-10T18", tmax_f=79)}
    assert wxc_verify.consensus(models, {})["tmax_f"] == 82.0                      # old behaviour
    now = datetime(2026, 10, 11, 23, 54, tzinfo=timezone.utc)
    c = wxc_verify.consensus(models, {}, now=now)
    assert c["tmax_f"] == 85.0
    assert sorted(c["method"]["tmax_f"]["excluded_stale"]) == ["AIFS_ENS", "ENS"]


def _fake_hourly(day: date, model: str, n_members=3):
    t0 = datetime(day.year, day.month, day.day) - timedelta(days=1)
    times = [(t0 + timedelta(hours=h)).strftime("%Y-%m-%dT%H:%M") for h in range(72)]
    h = {"time": times}
    for m in range(n_members):
        tag = "" if m == 0 else f"_member{m:02d}"
        h[f"temperature_2m{tag}_{model}_ensemble"] = [70.0 + m + (i % 24) / 4 for i in range(72)]
        h[f"wind_speed_10m{tag}_{model}_ensemble"] = [8.0] * 72
        h[f"precipitation{tag}_{model}_ensemble"] = [0.0] * 72
    return {"hourly": h}


def test_get_ensembles_flags_a_stale_run(monkeypatch, capsys):
    day = date(2026, 10, 13)
    init = datetime(2026, 10, 10, 18, tzinfo=timezone.utc)
    monkeypatch.setattr(wxc_ens, "latest_init", lambda model: init)
    monkeypatch.setattr(wxc_ens, "_get_json", lambda url, params=None: _fake_hourly(day, "ecmwf_ifs025"))
    st = SimpleNamespace(icao="KOLM", lat=46.97, lon=-122.9)

    fresh = wxc_ens.get_ensembles(st, day, only=["ENS"], now=init + timedelta(hours=20))["ENS"]
    assert fresh["tmax_f"] is not None and "STALE" not in fresh["note"]

    # same run, now from the cache, 54 h later: values kept (shown), but flagged loudly
    stale = wxc_ens.get_ensembles(st, day, only=["ENS"], now=init + timedelta(hours=54))["ENS"]
    assert stale["tmax_f"] == fresh["tmax_f"] and not stale.get("error")
    assert "STALE RUN" in stale["note"] and "54 h old" in stale["note"]
    assert "STALE RUN" in capsys.readouterr().out
