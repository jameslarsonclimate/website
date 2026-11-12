"""
Data for the page's scrollable timeline (wxchallenge/timeline.js): every 06Z-06Z day of the
current city side by side, each with the runs that were out before its 00Z deadline
(series/<ICAO>_<date>_submitted.json), today's newest runs, the observations and cloud
cover, bundled into data/wxchallenge/timeline.json.

DISPLAY ONLY, like the cloud files: nothing here feeds the scores or the consensus.

Per-day files in data/wxchallenge/timeline/ (kept for good: the model cache is pruned and
IEM / GOES are slow to ask again):
  <ICAO>_<date>_obs.json     every METAR of the day (temp, dewpoint, wind, gust, precip running total
                             since 06Z), METAR sky cover and the hourly GOES cloud fraction;
                             "complete" once the day has ended
  <ICAO>_<date>_clouds.json  model cloud cover of the day's submitted runs ("submitted") and,
                             for today, of the newest runs ("latest")

Every function takes the data directory explicitly (no module-level paths), so tests that
run the pipeline in a scratch copy never touch the real files.
"""

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

MAX_DAYS = 35              # cap: a two-week city plus its 14 hindcast days, with a margin
FINAL_AFTER = timedelta(hours=1)   # a day's reports are complete this long after its 06Z end
VERIF_VARS = ("tmax_f", "tmin_f", "wind_max_kt", "precip_in")


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
def day_start(day: date) -> pd.Timestamp:
    return pd.Timestamp(datetime(day.year, day.month, day.day, 6))


def _iso(t) -> str:
    t = pd.Timestamp(t)
    if t.tzinfo is not None:
        t = t.tz_convert("UTC").tz_localize(None)
    return t.strftime("%Y-%m-%dT%H:%M")


def _num(v, nd):
    """Rounded float, or None for missing / non-finite values."""
    if v is None:
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return round(f, nd) if np.isfinite(f) else None


def _nums(vals, nd):
    return None if vals is None else [_num(v, nd) for v in vals]


def day_path(data_dir: Path, icao: str, day: date, kind: str) -> Path:
    return Path(data_dir) / "timeline" / f"{icao.upper()}_{day.isoformat()}_{kind}.json"


def load_day(data_dir: Path, icao: str, day: date, kind: str) -> Optional[dict]:
    try:
        return json.loads(day_path(data_dir, icao, day, kind).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_day(data_dir: Path, icao: str, day: date, kind: str, rec: dict) -> Path:
    p = day_path(data_dir, icao, day, kind)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, separators=(",", ":"), allow_nan=False))
    tmp.replace(p)
    return p


def load_series(data_dir: Path, icao: str, day: date, kind: str) -> Optional[dict]:
    try:
        return json.loads((Path(data_dir) / "series" / f"{icao.upper()}_{day.isoformat()}_{kind}.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def is_final(day: date, now: datetime) -> bool:
    """The 06Z-06Z day has ended (with a margin for late reports)."""
    end = datetime(day.year, day.month, day.day, 6, tzinfo=timezone.utc) + timedelta(days=1)
    return now >= end + FINAL_AFTER


# ----------------------------------------------------------------------------
# per-day records
# ----------------------------------------------------------------------------
def day_reports(raw: pd.DataFrame, day: date) -> pd.DataFrame:
    """The IEM reports inside the day (06Z exclusive, so the running precip total starts at 0)."""
    if raw is None or raw.empty:
        return raw
    t = pd.to_datetime(raw["valid"], utc=True)
    s = pd.Timestamp(day_start(day)).tz_localize("UTC")
    return raw[(t > s) & (t <= s + pd.Timedelta(hours=24))]


def obs_record(icao: str, day: date, reports: Optional[pd.DataFrame], sky: Optional[pd.DataFrame],
               goes: Optional[list], now: datetime, complete: bool) -> dict:
    """reports: wxc_obs.report_series() of the day's METARs; sky: wxc_clouds.sky_series();
    goes: wxc_goes.hourly_cloud() records. Missing parts are left out."""
    rec = {"station": icao.upper(), "date": day.isoformat(), "generated_at_utc": now.isoformat(),
           "complete": bool(complete)}
    if reports is not None and not reports.empty:
        r = reports.sort_values("valid")
        rec["reports"] = {"times": [_iso(t) for t in r["valid"]],
                          "temp_f": _nums(r["temp_f"], 1),
                          "dewpt_f": _nums(r["dewpt_f"], 1) if "dewpt_f" in r else None,
                          "wind_kt": _nums(r["wind_kt"], 0),
                          "gust_kt": _nums(r["gust_kt"], 0), "precip_in": _nums(r["precip_total_in"], 2),
                          "routine": [bool(x) for x in r["routine"]]}
    if sky is not None and not sky.empty:
        s = sky.sort_values("valid")
        rec["sky"] = {"times": [_iso(t) for t in s["valid"]], "pct": _nums(s["sky_pct"], 0),
                      "clear": [bool(x) for x in s["clear"]]}
    if goes:
        g = [x for x in goes if x.get("cloud_pct") is not None]
        rec["goes"] = {"times": [x["hour"] for x in g], "pct": [_num(x["cloud_pct"], 0) for x in g]}
    return rec


def clouds_record(icao: str, day: date, submitted: Optional[dict], latest: Optional[dict],
                  now: datetime) -> dict:
    """{model: wxc_clouds.for_day() record} of the submitted runs (and today's latest runs)."""
    def slim(group):
        out = {}
        for name, r in (group or {}).items():
            if r and r.get("times"):
                out[name] = {"init_time_utc": r.get("init_time_utc"), "times": list(r["times"]),
                             "cloud_pct": _nums(r.get("cloud_pct"), 0), "step": bool(r.get("step"))}
                if r.get("cloud_sd") and len(r["cloud_sd"]) == len(r["times"]):
                    out[name]["cloud_sd"] = _nums(r["cloud_sd"], 0)       # NBM's SSD
        return out
    rec = {"station": icao.upper(), "date": day.isoformat(), "generated_at_utc": now.isoformat(),
           "submitted": slim(submitted)}
    if latest:
        rec["latest"] = slim(latest)
    return rec


# ----------------------------------------------------------------------------
# the bundle
# ----------------------------------------------------------------------------
def timeline_days(data_dir: Path, icao: str, since: Optional[str] = None) -> list:
    """Every day from the city's first submitted series (not before `since`, the scoreboard's
    period start, so an earlier visit to the same station is left out) to the newest one (the
    day being forecast), at most MAX_DAYS, with no gaps (a day missed offline is still a day)."""
    days = []
    for p in (Path(data_dir) / "series").glob(f"{icao.upper()}_*_submitted.json"):
        try:
            days.append(date.fromisoformat(p.name.split("_")[1]))
        except ValueError:
            continue
    if not days:
        return []
    last = max(days)
    lo = last - timedelta(days=MAX_DAYS)
    if since:
        lo = max(lo, date.fromisoformat(since) - timedelta(days=1))
    first = min((d for d in days if d > lo), default=last)
    return [first + timedelta(days=i) for i in range((last - first).days + 1)]


def _hours(times, day: date) -> list:
    """Valid times -> hours since the day's 06Z."""
    t0 = day_start(day)
    out = []
    for t in times:
        t = pd.Timestamp(t)
        if t.tzinfo is not None:
            t = t.tz_convert("UTC").tz_localize(None)
        out.append(round((t - t0).total_seconds() / 3600, 2))
    return out


def _model(rec: dict, day: date) -> Optional[dict]:
    """A series model -> {init, tmax, tmin, h, temp, [td], [rh], wind, precip, [p10, p90]} inside
    the day. rh only for the ensembles (their members' mean RH); the page computes the others'."""
    times = rec.get("times") or []
    if not times:
        return None
    h = _hours(times, day)
    keep = [i for i, x in enumerate(h) if -0.01 <= x <= 24.01]
    if not keep:
        return None
    order = sorted(keep, key=lambda i: h[i])

    def pick(key, nd):
        v = rec.get(key)
        if not isinstance(v, list) or len(v) != len(times):
            return None
        out = [_num(v[i], nd) for i in order]
        return out if any(x is not None for x in out) else None
    out = {"init": rec.get("init_time_utc"), "tmax": _num(rec.get("tmax_f"), 1), "tmin": _num(rec.get("tmin_f"), 1),
           "h": [h[i] for i in order], "temp": pick("temp_f", 1), "wind": pick("wind_kt", 1),
           "precip": pick("precip_in", 3)}
    td = pick("dewpt_f", 1)
    if td:
        out["td"] = td
    rh = pick("rh_pct", 0)
    if rh:
        out["rh"] = rh
    tt, tk = rec.get("wind_tail_times"), rec.get("wind_tail_kt")
    if isinstance(tt, list) and isinstance(tk, list) and len(tt) == len(tk) and tt:
        th = _hours(tt, day)          # wind past 06Z, to the end of the LST (CLI) day
        out["wind_tail"] = {"h": th, "kt": [_num(v, 1) for v in tk]}
    p10, p90 = pick("temp_p10", 1), pick("temp_p90", 1)
    if p10 and p90:
        out["p10"], out["p90"] = p10, p90
    return out


def _cloud(rec: dict, day: date) -> Optional[dict]:
    if not rec or not rec.get("times") or len(rec.get("cloud_pct") or []) != len(rec["times"]):
        return None
    h = _hours(rec["times"], day)
    keep = [i for i, x in enumerate(h) if -0.01 <= x <= 24.01 and rec["cloud_pct"][i] is not None]
    if not keep:
        return None
    out = {"init": rec.get("init_time_utc"), "h": [h[i] for i in keep],
           "pct": [rec["cloud_pct"][i] for i in keep], "step": bool(rec.get("step"))}
    sd = rec.get("cloud_sd")
    if sd and len(sd) == len(rec["times"]) and any(sd[i] is not None for i in keep):
        out["sd"] = [sd[i] for i in keep]
    return out


def _obs(rec: Optional[dict], day: date) -> Optional[dict]:
    if not rec:
        return None
    out = {"complete": bool(rec.get("complete"))}
    r = rec.get("reports")
    if r and r.get("times"):
        out["reports"] = {"h": _hours(r["times"], day), "temp": r.get("temp_f"), "td": r.get("dewpt_f"),
                          "wind": r.get("wind_kt"),
                          "gust": r.get("gust_kt"), "precip": r.get("precip_in"), "routine": r.get("routine")}
    for key in ("sky", "goes"):
        s = rec.get(key)
        if s and s.get("times"):
            out[key] = {"h": _hours(s["times"], day), "pct": s["pct"]}
            if key == "sky":
                out[key]["clear"] = s.get("clear")
    return out


def _verif_day(row: Optional[dict]) -> Optional[dict]:
    """A verification.json day -> the official obs and each model's scored forecast and error
    (the same numbers as the scoreboard)."""
    if not row or not row.get("obs"):
        return None
    models = {}
    for name, m in (row.get("models") or {}).items():
        fc, err = m.get("forecast") or {}, m.get("error") or {}
        models[name] = {"fc": [fc.get(v) for v in VERIF_VARS], "err": [err.get(v) for v in VERIF_VARS],
                        "points": m.get("points")}
    return {"obs": [row["obs"].get(v) for v in VERIF_VARS], "pending": row.get("obs_pending") or [],
            "hindcast": bool(row.get("hindcast")), "models": models}


def cloud_windows(day: date, lat: float, lon: float) -> dict:
    """The day's cloud windows as hours since 06Z: night = 06Z to sunrise (drives the low),
    day = sunrise to sunset (drives the high), as on the scoreboard's cloud tabs."""
    import wxc_clouds
    day_h, night_h = wxc_clouds.day_night_hours(day, lat, lon)
    span = lambda hs: [_hours(hs, day)[0], _hours(hs, day)[-1]] if hs else None   # noqa: E731
    return {"night": span(night_h), "day": span(day_h)}


def _cloud_scores(ctx: Optional[dict]) -> Optional[dict]:
    """A cloud_context.json day -> observed (ASOS, GOES) and each scored run's night / day
    cloud cover and error: [night, day] and [night, day, night error, day error]."""
    if not ctx:
        return None
    o = ctx.get("obs") or {}
    return {"obs": [o.get("night_pct"), o.get("day_pct")], "goes": [o.get("goes_night_pct"), o.get("goes_day_pct")],
            "models": {n: [m.get("night_pct"), m.get("day_pct"), m.get("night_err"), m.get("day_err")]
                       for n, m in (ctx.get("models") or {}).items()}}


def build(data_dir: Path, icao: str, now: datetime, verification: Optional[dict] = None,
          today_json: Optional[dict] = None, station_label: Optional[str] = None,
          since: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None,
          latest_models: Optional[list] = None, lst_offset: Optional[float] = None) -> Optional[dict]:
    """The whole timeline for the page, or None without any submitted series. lat/lon add
    each day's cloud windows; the scoreboard's cloud numbers come from cloud_context.json.
    latest_models: the newest runs to draw for today (None: every one stored)."""
    icao = icao.upper()
    days = timeline_days(data_dir, icao, since)
    if not days:
        return None
    today = (now - timedelta(hours=6)).date()
    vrows = {}
    if verification and verification.get("station") == icao:
        vrows = {d["date"]: d for d in verification.get("days", [])}
    try:
        cctx = json.loads((Path(data_dir) / "cloud_context.json").read_text())["stations"].get(icao) or {}
    except (FileNotFoundError, json.JSONDecodeError, KeyError, AttributeError):
        cctx = {}
    out_days = []
    for d in days:
        sub = load_series(data_dir, icao, d, "submitted") or {}
        rec = {"date": d.isoformat(), "hindcast": bool(sub.get("hindcast")), "models": {}}
        for name, m in (sub.get("models") or {}).items():
            mm = _model(m, d)
            if mm:
                rec["models"][name] = mm
        clouds = load_day(data_dir, icao, d, "clouds") or {}
        for name, c in (clouds.get("submitted") or {}).items():
            cc = _cloud(c, d)
            if cc and name in rec["models"]:
                rec["models"][name]["cloud"] = cc
            elif cc:          # cloud cover without a stored series (shouldn't happen): still drawn
                rec["models"][name] = {"init": cc["init"], "tmax": None, "tmin": None, "h": [], "cloud": cc}
        if d == today:
            newest = load_series(data_dir, icao, d, "latest") or {}
            latest = {}
            for name, m in (newest.get("models") or {}).items():
                if latest_models is not None and name not in latest_models:
                    continue
                mm = _model(m, d)
                if mm:
                    latest[name] = mm
            for name, c in (clouds.get("latest") or {}).items():
                cc = _cloud(c, d)
                if cc and name in latest:
                    latest[name]["cloud"] = cc
            if latest:
                rec["latest"] = latest
            tj = today_json or {}
            if tj.get("date") == d.isoformat() and tj.get("obs"):
                o = tj["obs"]
                rec["so_far"] = {"high": _num(o.get("high"), 1), "low": _num(o.get("low"), 1),
                                 "wind": _num(o.get("wind"), 0), "precip": _num(o.get("precip"), 2),
                                 "through": tj.get("through_utc")}
        ob = _obs(load_day(data_dir, icao, d, "obs"), d)
        if ob:
            rec["obs"] = ob
        v = _verif_day(vrows.get(d.isoformat()))
        if v:
            rec["verif"] = v
        if lat is not None and lon is not None:
            rec["cloud_win"] = cloud_windows(d, lat, lon)
        cs = _cloud_scores(cctx.get(d.isoformat()))
        if cs:
            rec["cloud_scores"] = cs
        out_days.append(rec)
    extra = {}
    if lst_offset is not None:    # the CLI day (wind is verified over it): hours after 06Z it starts
        extra["wind_day_h"] = -lst_offset - 6
    return {**extra, "station": icao, "label": station_label, "generated_at_utc": now.isoformat(),
            "now_utc": _iso(now), "today": today.isoformat(), "forecast_day": days[-1].isoformat(),
            "note": "Display only. Hours (h) count from 06Z of each day. Temperatures in °F, wind in kt, "
                    "precip in inches (running total since 06Z), cloud cover in %, dewpoint (td) in °F. Each day's models are "
                    "the runs available before its 00Z deadline; 'latest' are today's newest runs; "
                    "'verif' holds the official observations and the scored forecasts; 'cloud_win' the "
                    "night (06Z to sunrise) and day (sunrise to sunset) hours; 'cloud_scores' the "
                    "scoreboard's night/day cloud cover (not scored).",
            "days": out_days}


def write(data_dir: Path, bundle: dict) -> Path:
    p = Path(data_dir) / "timeline.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(bundle, separators=(",", ":"), allow_nan=False))
    tmp.replace(p)
    return p
