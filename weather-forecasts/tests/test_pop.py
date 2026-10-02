"""Offline tests for PoP (wxc_pop), observed 6-h block precip, MOS P06 and NBM QMD reading."""
from datetime import date, datetime, timezone

import pandas as pd
import pytest

import wxc_mos
import wxc_nbm_qmd as qmd
import wxc_obs
import wxc_pop
from test_wxc import KSAV, STATIONS, FakeRemote, _mos_rows


def test_blocks_and_bounds():
    hr = lambda h: pd.Timestamp(f"2026-10-01 {h:02d}:00")  # noqa: E731
    assert [wxc_pop.block_of_hour_ending(hr(h)) for h in (7, 12, 13, 18, 19, 0, 1, 6)] == \
        ["06-12", "06-12", "12-18", "12-18", "18-00", "18-00", "00-06", "00-06"]
    w = wxc_pop.block_windows(date(2026, 10, 1))
    assert w[0] == ("06-12", datetime(2026, 10, 1, 6), datetime(2026, 10, 1, 12))
    assert w[-1] == ("00-06", datetime(2026, 10, 2, 0), datetime(2026, 10, 2, 6))
    # 24-h PoP is only bounded by four 6-h PoPs: max(p) <= P24 <= 1 - prod(1 - p)
    assert wxc_pop.p24_bounds({"06-12": 0.1, "12-18": 0.5, "18-00": 0.2, "00-06": 0.0}) == [0.5, 0.64]
    assert wxc_pop.p24_bounds({"06-12": 0.1}) is None
    assert wxc_pop.record(None, {}) is None


def test_member_fractions_count_trace_as_dry():
    rec = wxc_pop.from_members([0.0, 0.004, 0.01, 0.3], {"06-12": [0, 0, 0.01, 0.2], "00-06": [0, 0, 0, None]})
    assert rec["p24"] == 0.5 and rec["n_members"] == 4
    assert rec["blocks"] == {"06-12": 0.5, "12-18": None, "18-00": None, "00-06": 0.0}
    assert "p24_range" not in rec


def test_mos_pop_from_p06():
    res = wxc_mos.summarize_mos(_mos_rows("GFS"), date(2026, 9, 29), "GFS")
    pop = res["pop"]
    assert pop["p24"] is None and pop["blocks"] == {b: 0.3 for b in wxc_pop.BLOCK_LABELS}
    assert pop["p24_range"] == [0.3, pytest.approx(1 - 0.7 ** 4, abs=1e-3)] and pop["basis"] == "GFS MOS P06"


def test_observed_block_precip_ksav():
    d = wxc_obs.summarize_metars(pd.read_csv(KSAV)).set_index("date")
    for day in ("2025-09-18", "2025-09-26"):
        blocks = d.loc[day, "precip_6h_in"]
        assert set(blocks) == set(wxc_pop.BLOCK_LABELS)
        # complete day: the blocks add up to the daily (hourly P group) total
        assert sum(blocks.values()) == pytest.approx(d.loc[day, "precip_in"], abs=0.005)
    assert any(v > 0 for v in d.loc["2025-09-26", "precip_6h_in"].values())


def test_qmd_windows_per_cycle():
    day = date(2026, 10, 2)
    # (init, 24-h window text in the end-hour file, as read from the idx files on 2026-10-02)
    cases = [(datetime(2026, 10, 1, 12), "18-42 hour acc fcst", 42), (datetime(2026, 10, 1, 18), "12-36 hour acc fcst", 36),
             (datetime(2026, 10, 1, 0), "30-54 hour acc fcst", 54), (datetime(2026, 10, 1, 6), "1-2 day acc fcst", 48)]
    import re
    for init, text, e in cases:
        init = init.replace(tzinfo=timezone.utc)
        jobs = qmd.jobs_for(init, day, "co")
        key, url, pat = jobs[0]
        assert key == "p24" and url.endswith(f"/qmd/blend.t{init:%H}z.qmd.f{e:03d}.co.grib2")
        assert re.search(pat, f"1:0:d=x:APCP:surface:{text}:prob >0.254:prob fcst 255/255")
        assert not re.search(pat, f"1:0:d=x:APCP:surface:{text}:prob >2.54:prob fcst 255/255")
        blk = {k: (u, p) for k, u, p in jobs if k.startswith("b:")}
        assert list(blk) == [f"b:{b}" for b in wxc_pop.BLOCK_LABELS]
        u, p = blk["b:00-06"]
        assert u.endswith(f".f{e:03d}.co.grib2") and f"{e - 6}-{e} hour" in p
    # "10% level" must not match "100% level"
    p10 = qmd.pct_pattern(18, 42, 10)
    assert re.search(p10, "5:9:d=x:APCP:surface:18-42 hour acc fcst:10% level")
    assert not re.search(p10, "5:9:d=x:APCP:surface:18-42 hour acc fcst:100% level")


def test_qmd_summarize_units():
    rec = qmd.summarize({"p24": 70.6, "q10": 0.0, "q50": 5.25, "q90": 43.4, "b:06-12": 3.8, "b:12-18": float("nan")})
    assert rec["p24"] == 0.706 and rec["basis"] == "NBM QMD"
    assert rec["q24_in"] == {"10": 0.0, "50": pytest.approx(0.207, abs=1e-3), "90": pytest.approx(1.709, abs=1e-3)}
    assert rec["blocks"]["06-12"] == 0.038 and rec["blocks"]["12-18"] is None and rec["blocks"]["00-06"] is None


def test_qmd_get_with_fake_files(monkeypatch):
    import wxc_cam_ens as ce
    fake = FakeRemote()
    init = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)
    url = lambda fh: qmd.URL.format(init=init, fh=fh, dom="co")  # noqa: E731
    for i, fh in enumerate((24, 30, 36, 42)):
        recs = [(f"APCP:surface:{fh - 6}-{fh} hour acc fcst:prob >0.254:prob fcst 255/255", 10.0 * (i + 1))]
        if fh == 42:
            recs += [("APCP:surface:18-42 hour acc fcst:prob >0.254:prob fcst 255/255", 55.0)]
            recs += [(f"APCP:surface:18-42 hour acc fcst:{q}% level", q / 10) for q in (10, 25, 50, 75, 90, 100)]
        fake.add(url(fh), recs)
    monkeypatch.setattr(ce.PointReader, "get", lambda self, u, headers=None, timeout=60: fake.get(u, headers))
    st = STATIONS["KTPA"]
    now = datetime(2026, 10, 1, 21, tzinfo=timezone.utc)       # 18Z not posted -> 12Z used
    res = qmd.get_qmd(st, date(2026, 10, 2), now)
    assert "error" not in res, res.get("error")
    assert res["init_time_utc"] == "2026-10-01T12" and res["tmax_f"] is None and res["precip_only"]
    assert res["pop"]["p24"] == 0.55 and res["pop"]["blocks"] == {"06-12": 0.1, "12-18": 0.2, "18-00": 0.3, "00-06": 0.4}
    assert res["precip_in"] == round(5.0 / 25.4, 2)
    assert res["pop"]["q24_in"]["90"] == pytest.approx(9.0 / 25.4, abs=1e-3)
    assert qmd.get_qmd(st.__class__(**{**st.__dict__, "rrfs_domain": None}), date(2026, 10, 2), now)["error"]


def _run(gen, day, models, hindcast=False):
    r = {"generated_at_utc": gen, "station": "KTPA", "target_date": day, "models": models}
    if hindcast:
        r["hindcast"] = True
    return r


def test_verify_pop_brier_and_live_only():
    blocks = lambda *p: dict(zip(wxc_pop.BLOCK_LABELS, p))  # noqa: E731
    runs = [
        _run("2026-09-29T22:00:00+00:00", "2026-09-30", {
            "ENS": {"pop": wxc_pop.record(0.8, blocks(0.1, 0.6, 0.5, 0.0), n_members=51)},
            "NBM": {"pop": wxc_pop.record(None, blocks(0.2, 0.7, 0.4, 0.1), bounds=True)}}),
        # after the deadline: ignored
        _run("2026-09-30T01:00:00+00:00", "2026-09-30", {"ENS": {"pop": wxc_pop.record(0.0, blocks(0, 0, 0, 0))}}),
        # hindcast rows never count for PoP
        _run("2026-09-30T23:00:00+00:00", "2026-10-01", {"ENS": {"pop": wxc_pop.record(1.0, blocks(1, 1, 1, 1))}}, True),
        _run("2026-09-30T22:00:00+00:00", "2026-10-01", {"ENS": {"pop": wxc_pop.record(0.2, blocks(0.1, 0.1, 0.0, 0.0))}}),
    ]
    obs = [{"station": "KTPA", "date": "2026-09-30", "precip_in": 0.31, "complete": True,
            "precip_6h_in": blocks(0.0, 0.3, 0.01, 0.0)},
           # a trace counts as dry; no block values stored (older record) -> 24-h only
           {"station": "KTPA", "date": "2026-10-01", "precip_in": 0.0, "precip_trace": True, "complete": True}]
    res = wxc_pop.verify_pop(runs, obs, "KTPA")
    ens, nbm = res["summary"]["ENS"], res["summary"]["NBM"]
    assert ens["n_days"] == 2 and ens["brier_24h"] == pytest.approx(((0.8 - 1) ** 2 + 0.2 ** 2) / 2)
    assert ens["n_blocks"] == 4 and ens["brier_6h"] == pytest.approx((0.01 + 0.16 + 0.25 + 0) / 4)
    assert nbm["n_days"] == 0 and nbm["brier_24h"] is None and nbm["n_blocks"] == 4      # MOS: blocks only
    assert res["base_rate"]["freq_24h"] == 0.5 and res["base_rate"]["brier_24h"] == 0.25
    d0 = res["days"][0]
    assert d0["obs"] == {"24h": 1, "06-12": 0, "12-18": 1, "18-00": 1, "00-06": 0}
    assert res["days"][1]["obs"]["06-12"] is None
    rel = res["reliability"]["ENS"]
    assert rel["n"] == 6 and sum(b["n"] for b in rel["bins"]) == 6
    top = [b for b in rel["bins"] if b["bin"] == [0.8, 0.9]][0]
    assert top["n"] == 1 and top["obs_freq"] == 1.0
