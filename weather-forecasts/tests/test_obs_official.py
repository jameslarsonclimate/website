"""
Observed values against the official WxChallenge final results, plus the edge cases of the
verification rules (see wxc_obs). Offline: raw METARs / CLI / CF6 saved under tests/fixtures/.

    cd weather-forecasts && python -m pytest tests/test_obs_official.py -q
"""
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

import wxc_obs
from wxc_stations import STATIONS, Station

FIX = Path(__file__).resolve().parent / "fixtures"
METARS = FIX / "KTPA_metar_20260929_20261002.csv"     # IEM asos.py data=metar, report_type 3 and 4
CLI_JSON = FIX / "KTPA_cli_2026.json"                 # IEM json/cli.py
CLI_TEXT = FIX / "CLITPA_20260928_20261002.txt"       # IEM AFOS text, preliminary + final products
CF6_JSON = FIX / "KTPA_cf6_2026.json"
KTPA = STATIONS["KTPA"]
NOW = datetime(2026, 10, 2, 16, tzinfo=timezone.utc)

# Official WxChallenge final results, KTPA (day = 06Z on the date to 06Z the next day)
OFFICIAL = {
    "2026-09-29": {"tmax_f": 87, "tmin_f": 74, "wind_max_kt": 10, "precip_in": 0.00},
    "2026-09-30": {"tmax_f": 88, "tmin_f": 75, "wind_max_kt": 14, "precip_in": 0.42},
    "2026-10-01": {"tmax_f": 88, "tmin_f": 74, "wind_max_kt": 14, "precip_in": 0.28},
}


def _metars():
    return pd.read_csv(METARS)[["valid", "metar", "report_type"]]


def _records(cli: dict, now=NOW) -> dict:
    daily = {r["date"]: r for r in wxc_obs.daily_records(_metars(), KTPA.lst_offset_hours)}
    return {d: wxc_obs.finalize(daily[d], cli.get(d), True, now) for d in OFFICIAL}


def _cli_json():
    return wxc_obs.select_cli(wxc_obs.parse_cli_json(json.loads(CLI_JSON.read_text())["results"]),
                              KTPA.lst_offset_hours)


# ----------------------------------------------------------------- official results
@pytest.mark.parametrize("cli_source", ["json", "text"])
def test_official_results_ktpa(cli_source):
    cli = _cli_json() if cli_source == "json" else wxc_obs.parse_cli(CLI_TEXT.read_text(), KTPA.lst_offset_hours)
    recs = _records(cli)
    for d, off in OFFICIAL.items():
        assert {v: recs[d][v] for v in off} == off, d
        assert recs[d]["final"] and recs[d]["pending"] == [] and recs[d]["complete"]
        assert recs[d]["source"]["wind_max_kt"] == "cli" and recs[d]["source"]["precip_in"] == "6h_group"


def test_official_results_via_get_observations(monkeypatch):
    """The whole fetch path (METAR window, CLI JSON -> text, CF6) on the saved responses."""
    raw = _metars()
    windows = []

    def fake_metars(st, a, b, specials=False, sky=False, retries=3):
        windows.append((a, b))
        t = pd.to_datetime(raw["valid"], utc=True)
        sel = raw[(t >= pd.Timestamp(a)) & (t <= pd.Timestamp(b))]
        return sel if specials else sel[sel["report_type"] == 3]
    monkeypatch.setattr(wxc_obs, "fetch_metars", fake_metars)
    monkeypatch.setattr(wxc_obs, "fetch_cli_json", lambda icao, years: [
        dict(p, via="iem_json") for p in wxc_obs.parse_cli_json(json.loads(CLI_JSON.read_text())["results"])])
    monkeypatch.setattr(wxc_obs, "fetch_cli_text", lambda pil, limit=30: pytest.fail("JSON had every final CLI"))
    monkeypatch.setattr(wxc_obs, "fetch_cf6", lambda icao, years: {
        r["valid"]: int(r["max_smph"]) for r in json.loads(CF6_JSON.read_text())["results"]})
    monkeypatch.setattr(wxc_obs, "_get", lambda *a, **k: pytest.fail("network call in an offline test"))
    recs = {r["date"]: r for r in wxc_obs.get_observations(KTPA, now=NOW, first=date(2026, 9, 29),
                                                           last=date(2026, 10, 1))}
    assert sorted(recs) == sorted(OFFICIAL)
    for d, off in OFFICIAL.items():
        assert {v: recs[d][v] for v in off} == off, d
        assert recs[d]["final"] and recs[d]["cli_via"] == "iem_json"
        assert recs[d]["cf6_wind_mph"] == recs[d]["cli_wind_mph"]          # CF6 agrees with the CLI
        assert not recs[d]["notes"]
    # fetched from the start of the first LST day (05Z) to past the last 06Z end
    (a, b), = windows
    assert pd.Timestamp(a) == pd.Timestamp("2026-09-29 04:00", tz="UTC")
    assert pd.Timestamp(b) == pd.Timestamp("2026-10-02 06:30", tz="UTC")


def test_known_check_ktpa_20261001():
    """The hand-verified case: hourly T groups alone, P groups across SPECIs and routine winds
    all give the wrong answer."""
    r = _records(_cli_json())["2026-10-01"]
    assert (r["tmax_f_hourly"], r["tmin_f_hourly"]) == (87, 75)               # T groups alone
    assert (r["tmax_f_raw"], r["tmin_f_raw"]) == (88.0, 73.9)                 # 31.1 C / 23.3 C
    assert (r["tmax_f"], r["tmin_f"]) == (88, 74)
    assert r["source"]["tmax_f"] == r["source"]["tmin_f"] == "6h_group"
    # precip: only the 012353Z standard report has a 6-h group (60028)
    rep = wxc_obs.prepare_reports(_metars())
    std = wxc_obs.standard_reports(rep, date(2026, 10, 1))
    assert [s["valid"].strftime("%d%H%M") for s in std] == ["011153", "011753", "012353", "020553"]
    assert [s["precip_6grp"] for s in std][2] == 0.28 and all(pd.isna(s["precip_6grp"]) for s in std[:2] + std[3:])
    assert r["precip_in"] == 0.28 and r["precip_6h_in"] == {"06-12": 0.0, "12-18": 0.0, "18-00": 0.28, "00-06": 0.0}
    t = rep["valid"]
    day = rep[(t > pd.Timestamp("2026-10-01 06:00", tz="UTC")) & (t <= pd.Timestamp("2026-10-02 06:00", tz="UTC"))]
    assert round(day["precip_1h"].fillna(0).sum(), 2) == 0.61                 # the double count avoided
    # wind: CLI 16 mph = 13.9 kt -> 14; METAR max in the EST day is the 1913Z SPECI's 13 kt
    assert r["cli_wind_mph"] == 16 and r["wind_max_kt"] == 14
    assert r["wind_max_kt_lst"] == 13 and r["wind_max_lst_at"] == "2026-10-01T19:13Z"
    assert r["wind_max_kt_metar"] == 8                                        # routine reports only
    assert r["lst_window_utc"] == ["2026-10-01T05:00Z", "2026-10-02T05:00Z"]


def test_preliminary_cli_from_real_products():
    """9/30: the 5 PM preliminary CLI said 13 mph (11 kt), the final 16 mph (14 kt)."""
    prods = wxc_obs.parse_cli_products(CLI_TEXT.read_text())
    p930 = sorted((p for p in prods if p["date"] == "2026-09-30"), key=lambda p: p["issued"])
    assert [(p["issued"].strftime("%d%H%M"), p["wind_mph"], p["prelim_text"]) for p in p930] == \
        [("302113", 13, True), ("010828", 16, False)]
    only_prelim = wxc_obs.select_cli(p930[:1], KTPA.lst_offset_hours)
    rec = _records(only_prelim, now=datetime(2026, 9, 30, 22, tzinfo=timezone.utc))["2026-09-30"]
    assert rec["source"]["wind_max_kt"] == "pending" and rec["pending"] == ["wind_max_kt"] and not rec["final"]
    assert rec["wind_max_kt"] == 11                                            # best guess so far
    assert rec["wind_source"].startswith("pending")


# ----------------------------------------------------------------- synthetic edge cases
D = date(2026, 3, 10)        # after the DST change: the LST windows must not move


def _metar(ts, t10=250, wind="09005KT", rmk="", kind=None, cor=False):
    tg = f"T{'1' if t10 < 0 else '0'}{abs(t10):03d}0200"
    head = f"{kind} " if kind else ""
    body = f"{head}KXXX {ts:%d%H%M}Z {'COR ' if cor else ''}{wind} 10SM CLR {round(t10 / 10):02d}/20 A3000"
    return f"{body} RMK AO2 {rmk + ' ' if rmk else ''}{tg}"


def _day(std=None, hourly=None, specials=(), drop=(), d=D):
    """Routine :53 reports from 0553Z D (the day before's standard report) to 0653Z D+1.
    std: {period end hour 12/18/24/30: remark groups} for the standard reports (default
    max 26.0 / min 24.0 C, no precip); hourly: {"HH" or "HH+1": remark}; specials: (valid, metar)."""
    std = {12: "10260 20240", 18: "10260 20240", 24: "10260 20240", 30: "10260 20240", **(std or {})}
    rows = []
    t0 = pd.Timestamp(d, tz="UTC") + pd.Timedelta(hours=5, minutes=53)
    for k in range(26):
        ts = t0 + pd.Timedelta(hours=k)
        h = k + 6                                       # hour after 00Z D that this report ends
        key = f"{ts:%H}" + ("+1" if ts.date() > d else "")
        if key in drop:
            continue
        rmk = std.get(h, "") if h in (12, 18, 24, 30) else ""
        if k == 0:
            rmk = "10400 20000 60150"                   # previous day's 00-06Z: must be ignored
        rmk = " ".join(x for x in (rmk, (hourly or {}).get(key, "")) if x)
        rows.append((ts, _metar(ts, rmk=rmk), 3))
    rows += [(pd.Timestamp(v, tz="UTC"), m, 4) for v, m in specials]
    return pd.DataFrame(rows, columns=["valid", "metar", "report_type"])


def _one(df, utc_offset=-5, d=D):
    return {r["date"]: r for r in wxc_obs.daily_records(df, utc_offset)}[d.isoformat()]


def test_six_hour_groups_cover_the_day_exactly():
    r = _one(_day())
    assert (r["tmax_f_raw"], r["tmin_f_raw"]) == (78.8, 75.2)        # not the 0553Z D groups (40.0 / 0.0 C)
    assert r["precip_in"] == 0.0 and not r["precip_trace"] and r["n_standard_obs"] == 4
    assert r["metar_ok"] == {"tmax_f": True, "tmin_f": True, "precip_in": True}


def test_trace_60000_counts_as_zero():
    r = _one(_day(std={24: "10260 20240 60000"}, hourly={"21": "P0000", "23": "P0000"}))
    assert r["precip_in"] == 0.0 and r["precip_trace"] and r["source"]["precip_in"] == "6h_group"
    assert wxc_obs.parse_metar("KXXX 012353Z 00000KT 10SM CLR 20/10 A3000 RMK AO2 60000")["precip_6grp"] == 0.0


def test_three_hour_groups_ignored_and_after_0553z_is_next_day():
    df = _day(std={18: "10260 20240 60012", 24: "10260 20240 60020", 30: "10260 20240 60005"},
              hourly={"21": "60030", "06+1": "P0040 60040"})     # 21Z 3-h group; 0653Z rain is D+1
    assert _one(df)["precip_in"] == 0.37


def test_indeterminate_6_group_falls_back_to_routine_p_groups():
    # 6//// at 0553Z; hourly P groups 0.10 + 0.05 + 0.02 in routine reports; a SPECI's
    # cumulative P0012 (since the 0253Z report) must not be added on top
    hourly = {"20": "P0010", "02+1": "P0005", "03+1": "P0002"}
    df = _day(std={24: "10260 20240 60010", 30: "10260 20240 6////"}, hourly=hourly,
              specials=[("2026-03-11 03:20", _metar(pd.Timestamp("2026-03-11 03:20"), rmk="P0012", kind="SPECI"))])
    r = _one(df)
    assert r["precip_in"] == 0.17 and r["source"]["precip_in"] == "hourly" and r["metar_ok"]["precip_in"]
    assert r["precip_6hr_groups_in"] is None and r["precip_hourly_in"] == 0.17
    assert any("indeterminate" in n for n in r["notes"])


def test_speci_p_groups_never_summed():
    # rain in SPECIs between routine reports: their P groups are cumulative since 1953Z
    sp = [(f"2026-03-10 20:{m}", _metar(pd.Timestamp(f"2026-03-10 20:{m}"), rmk=f"P00{p}", kind="SPECI"))
          for m, p in (("10", "05"), ("25", "20"), ("40", "28"))]
    df = _day(std={24: "10260 20240 60030"}, hourly={"21": "P0030", "22": "P0000"}, specials=sp)
    r = _one(df)
    assert r["precip_in"] == 0.30 and r["precip_hourly_in"] == 0.30
    # the same with the 6-h group indeterminate: still the routine sum, not 0.30 + 0.53
    df = _day(std={24: "10260 20240 6////"}, hourly={"21": "P0030", "22": "P0000"}, specials=sp)
    assert _one(df)["precip_in"] == 0.30
    # SPECI T groups do count for the temperature
    hot = [("2026-03-10 19:40", _metar(pd.Timestamp("2026-03-10 19:40"), t10=281, kind="SPECI"))]
    r = _one(_day(specials=hot))
    assert r["tmax_f"] == 83 and r["source"]["tmax_f"] == "hourly"            # 28.1 C, above the 26.0 C groups


def test_body_temperature_without_t_group_not_used_for_extremes():
    """KTPA 9/22/2026: the 1150Z SPECI had no remarks T group, only 24/23 (whole degC). The T
    groups and 6-h groups say 24.4 C (75.9 F) and the CLI low was 76; 24 C would give 75."""
    sp = [("2026-03-10 11:50", "SPECI KXXX 101150Z 09003KT 8SM FEW006 SCT250 24/23 A2992 RMK AO2")]
    df = _day(std={12: "10256 20244", 18: "10317 20244", 24: "10322 20267", 30: "10267 20244"}, specials=sp)
    df["metar"] = df["metar"].str.replace("T02500200", "T02670233")
    r = _one(df)
    assert r["tmin_f_raw"] == pytest.approx(75.9) and r["tmin_f"] == 76
    assert wxc_obs.parse_metar(sp[0][1])["temp_c10"] == 240                  # still shown in the figures


def test_cor_duplicate_keeps_the_correction():
    df = _day()
    i = df.index[df["valid"] == pd.Timestamp("2026-03-10 23:53", tz="UTC")][0]
    wrong = df.loc[i, "metar"].replace("10260 20240", "10300 20100 60050")
    cor = df.loc[i, "metar"].replace("Z 09005KT", "Z COR 09005KT").replace("10260 20240", "10270 20235 60012")
    for rows in ([wrong, cor], [cor, wrong]):                  # whichever order IEM returns them in
        dup = pd.concat([df.drop(i), pd.DataFrame({"valid": df.loc[i, "valid"], "metar": rows, "report_type": 3})])
        r = _one(dup)
        assert r["precip_in"] == 0.12 and r["tmax_f_raw"] == pytest.approx(27.0 * 1.8 + 32)
        assert r["tmin_f_raw"] == pytest.approx(23.5 * 1.8 + 32, abs=0.05)
    # without a COR flag the later copy wins
    dup = pd.concat([df.drop(i), pd.DataFrame({"valid": df.loc[i, "valid"], "metar": [cor.replace(" COR", ""), wrong],
                                               "report_type": 3})])
    assert _one(dup)["precip_in"] == 0.50


def test_peak_wind_remark_not_read_as_6h_groups():
    m = ("KTPA 012353Z 21025G35KT 10SM SCT030 28/23 A3002 RMK AO2 PK WND 21036/2312 SLP164 60028 "
         "T02780233 10311 20261 53009")
    p = wxc_obs.parse_metar(m)
    assert p["min6_c10"] == 261 and p["max6_c10"] == 311 and p["precip_6grp"] == 0.28
    p = wxc_obs.parse_metar("KTPA 011753Z 10030G40KT 10SM 30/23 A3002 RMK AO2 PK WND 10041/1712 T03000228")
    assert p["max6_c10"] is None and p["min6_c10"] is None


def _cli(wind_mph, issued, prelim_text=False, d=D, **kw):
    p = {"date": d.isoformat(), "issued": issued, "pil": "CLIXXX", "product": None, "prelim_text": prelim_text,
         "wind_mph": wind_mph, "gust_mph": None, "tmax_f": kw.get("tmax_f"), "tmin_f": kw.get("tmin_f"),
         "precip_in": kw.get("precip_in"), "precip_trace": False}
    return p


def test_lst_window_mountain_station():
    """MST: the CLI day is 07Z-07Z (also during daylight saving). A SPECI at 0620Z D is in the
    06Z-06Z forecast day but not the CLI day; one at 0640Z D+1 is the other way round."""
    st = Station("KFNL", "Loveland, CO", 40.45, -105.0, cli_pil="CLIFNL", tz="America/Denver")
    assert st.lst_offset_hours == -7
    assert [t.strftime("%d%H") for t in wxc_obs.lst_window(date(2026, 7, 1), -7)] == ["0107", "0207"]
    sp = [("2026-03-10 06:20", _metar(pd.Timestamp("2026-03-10 06:20"), wind="27025KT", kind="SPECI")),
          ("2026-03-11 06:40", _metar(pd.Timestamp("2026-03-11 06:40"), wind="27018G30KT", kind="SPECI"))]
    r = _one(_day(specials=sp), utc_offset=-7)
    assert r["wind_max_kt_all_reports"] == 25 and r["wind_max_kt_lst"] == 18
    issued = datetime(2026, 3, 11, 9, tzinfo=timezone.utc)
    cli = wxc_obs.select_cli([_cli(15, issued)], -7)                          # 15 mph = 13 kt
    f = wxc_obs.finalize(r, cli[D.isoformat()], True, NOW)
    assert f["wind_max_kt"] == 18 and f["source"]["wind_max_kt"] == "metar_override" and f["final"]
    # no CLI at the site: the METAR max of the LST day, gusts never count
    f = wxc_obs.finalize(r, None, False, NOW)
    assert f["wind_max_kt"] == 18 and f["source"]["wind_max_kt"] == "metar"
    # ... and pending until that LST day has ended
    f = wxc_obs.finalize(r, None, False, datetime(2026, 3, 11, 6, 30, tzinfo=timezone.utc))
    assert f["source"]["wind_max_kt"] == "pending" and not f["final"]


def test_lst_window_eastern_station():
    """EST 05Z-05Z: a SPECI at 0530Z D+1 is in the forecast day but not the CLI day."""
    sp = [("2026-03-11 05:30", _metar(pd.Timestamp("2026-03-11 05:30"), wind="18030KT", kind="SPECI"))]
    r = _one(_day(specials=sp), utc_offset=-5)
    assert r["wind_max_kt_all_reports"] == 30 and r["wind_max_kt_lst"] == 5
    cli = wxc_obs.select_cli([_cli(16, datetime(2026, 3, 11, 8, 30, tzinfo=timezone.utc))], -5)
    f = wxc_obs.finalize(r, cli[D.isoformat()], True, NOW)
    assert f["wind_max_kt"] == 14 and f["source"]["wind_max_kt"] == "cli"


def test_preliminary_only_cli_is_pending():
    r = _one(_day(), utc_offset=-5)
    # issued at 0300Z D+1 = 10 PM EST: before the LST day ended, so preliminary even without the wording
    early = _cli(20, datetime(2026, 3, 11, 3, tzinfo=timezone.utc))
    for p in (early, _cli(20, datetime(2026, 3, 10, 22, tzinfo=timezone.utc), prelim_text=True)):
        cli = wxc_obs.select_cli([p], -5)[D.isoformat()]
        assert cli["cli_preliminary"]
        f = wxc_obs.finalize(r, cli, True, NOW)
        assert f["source"]["wind_max_kt"] == "pending" and f["pending"] == ["wind_max_kt"] and not f["final"]
        assert f["wind_max_kt"] == 17                                         # the preliminary 20 mph
    # no CLI at all yet: the METARs so far, still pending
    f = wxc_obs.finalize(r, None, True, NOW)
    assert f["wind_max_kt"] == 5 and f["source"]["wind_max_kt"] == "pending"
    # the final one replaces the preliminary one whatever order they come in
    late = _cli(12, datetime(2026, 3, 11, 8, 30, tzinfo=timezone.utc))
    for prods in ([early, late], [late, early]):
        cli = wxc_obs.select_cli(prods, -5)[D.isoformat()]
        assert not cli["cli_preliminary"] and cli["cli_wind_kt"] == 10


def test_cli_backup_only_when_metars_fail():
    final = _cli(12, datetime(2026, 3, 11, 8, 30, tzinfo=timezone.utc), tmax_f=81, tmin_f=70, precip_in=0.55)
    cli = wxc_obs.select_cli([final], -5)[D.isoformat()]
    ok = wxc_obs.finalize(_one(_day()), cli, True, NOW)
    assert (ok["tmax_f"], ok["tmin_f"], ok["precip_in"]) == (79, 75, 0.0)     # METARs fine: CLI not used
    assert any("CLI precip 0.55" in n for n in ok["notes"])                   # but the disagreement is flagged
    # 1753Z standard report (and 1653Z) missing: no 12-18Z 6-h groups -> the CLI is the backup
    r = _one(_day(drop=("16", "17")))
    assert r["n_standard_obs"] == 3 and not r["metar_ok"]["tmax_f"] and not r["metar_ok"]["precip_in"]
    f = wxc_obs.finalize(r, cli, True, NOW)
    assert (f["tmax_f"], f["tmin_f"], f["precip_in"]) == (81, 70, 0.55)
    assert f["source"]["tmax_f"] == f["source"]["tmin_f"] == f["source"]["precip_in"] == "cli_backup"
    assert f["final"]
    # before the final CLI exists the METAR value stands, marked pending
    pre = wxc_obs.select_cli([dict(final, issued=datetime(2026, 3, 10, 22, tzinfo=timezone.utc))], -5)[D.isoformat()]
    f = wxc_obs.finalize(r, pre, True, NOW)
    assert f["tmax_f"] == 79 and set(f["pending"]) == {"tmax_f", "tmin_f", "precip_in", "wind_max_kt"}


def test_cli_text_issue_time_and_precip():
    text = CLI_TEXT.read_text()
    p = [q for q in wxc_obs.parse_cli_products(text) if q["date"] == "2026-10-01" and not q["prelim_text"]][0]
    assert p["issued"] == datetime(2026, 10, 2, 8, 31, tzinfo=timezone.utc) and p["pil"] == "CLITPA"
    assert (p["precip_in"], p["tmax_f"], p["tmin_f"], p["wind_mph"]) == (0.28, 88, 74, 16)
    assert wxc_obs._cli_precip("T") == (0.0, True) and wxc_obs._cli_precip(0.0001) == (0.0, True)
    assert wxc_obs.mph_to_kt(16) == 14 and wxc_obs.mph_to_kt(12) == 10 and wxc_obs.mph_to_kt(13) == 11
