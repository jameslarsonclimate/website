"""
Forecast-vs-observation bookkeeping for the WxChallenge page.

Files (under data/wxchallenge/):
  runs.jsonl          every forecast run: station, target day, per-model values
  observations.jsonl  observed values per station/day (upserted; final values replace pending ones;
                      see wxc_obs for the method and the per-variable "source")
  verification.json   per-day errors + period summary for the current station

Which run is verified for day D?  The last run generated before the 00Z D
submission deadline (what you could have used). Runs after the deadline are kept
in runs.jsonl for lead-time studies but are not scored.

Scoring ("error points") follows the WxChallenge rules as I understand them:
  temperature 1 pt per degF (high and low), wind 0.5 pt per kt,
  precipitation 0.4 pt per 0.01" in 0-0.10", 0.3 in 0.11-0.25", 0.2 in 0.26-0.50",
  0.1 above 0.50" (applied across the range between forecast and observed).
Forecasts are rounded to whole degF / kt and 0.01" before scoring, as submitted.

Run standalone to backfill/verify a past city period, e.g.
  python wxc_verify.py --station KDSM --start 2026-02-23 --end 2026-03-13
"""

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "wxchallenge"
RUNS = DATA / "runs.jsonl"
OBS = DATA / "observations.jsonl"
VERIF = DATA / "verification.json"
LEGACY_HISTORY = DATA / "forecast_history.jsonl"

VARS = ["tmax_f", "tmin_f", "wind_max_kt", "precip_in"]
MIN_DAYS_FOR_CORRECTION = 2
# A model's bias and MAE are decaying averages (like NBM's): a verified day's weight halves
# every HALF_LIFE_DAYS days back from the newest verified day. Half-lives are long so a couple
# of bad recent forecasts don't undo weeks of track record; scripts/tune_consensus.py tries others.
HALF_LIFE_DAYS = {"tmax_f": 9.0, "tmin_f": 9.0, "wind_max_kt": 18.0, "precip_in": 12.0}
# Bias corrections from only a few days are noisy, so only n_eff/(n_eff + BIAS_SHRINK_DAYS) of a
# model's average error is removed, with n_eff = (sum w)^2 / sum(w^2) the effective number of days
# (K=3, equal weights: 2 days -> 40%, 5 -> 62%, 8 -> 73%, 14 -> 82%; decay lowers n_eff a little).
# Lows use K=1 (2 days -> 67%, 14 -> 93%): their model biases tend to be persistent (e.g. warm
# lows on clear nights at KOLM), so more of the bias is removed sooner. Chosen by judgment: on
# the 38 stored days (KOLM, KTPA) the backtest can't tell K=1 from K=3 for lows.
BIAS_SHRINK_DAYS = {"tmax_f": 3, "tmin_f": 1, "wind_max_kt": 3, "precip_in": 3}
MAE_OFFSET = 0.5   # consensus weight = 1/(MAE + MAE_OFFSET)
OUTLIER_TOLERANCE = {"tmax_f": 8.0, "tmin_f": 8.0, "wind_max_kt": 10.0}   # from the member median
# shown and scored, but never consensus members (live or reconstructed): the GEFS ensemble, and
# IFS HRES at 9 km (wxc_ifs_hres; added 2026-10-21) until it has a track record of its own
NOT_IN_CONSENSUS = {"GEFS", "IFS_HRES"}
# A member whose run is more than STALE_HOURS older than the newest member's is left out of the
# consensus (e.g. Open-Meteo's ECMWF ensemble feed stalling while every other model updates).
STALE_HOURS = 36
# A forecast from a run more than MAX_RUN_AGE_HOURS old (at the 00Z deadline when scoring, at
# run time in the consensus) is not scored and left out of the consensus. Normally every model's
# run is <= 18 h old at the deadline; Open-Meteo's ECMWF ensemble feed stalled on 10/11-10/12 and
# the pipeline kept submitting the 10/10 18Z ENS and AIFS ENS runs (30-54 h old).
MAX_RUN_AGE_HOURS = 24
# Ensembles can't be hindcast (Open-Meteo serves only the latest run), so at a new city they
# have no track record; until they do, they borrow their deterministic parent's bias and MAE.
PROXY_TRACK_RECORD = {"ENS": "IFS", "AIFS_ENS": "AIFS"}
PERIOD_DAYS = 14   # a city period is two weeks (Mon-Thu x2, ~8 forecast days)
HINDCAST_DAYS = 14   # days hindcast before a city's first forecast day, for its track record


# ----------------------------------------------------------------------------
# jsonl helpers
# ----------------------------------------------------------------------------
def clean(obj):
    """Replace NaN/inf (invalid JSON, breaks the web page) with None, numpy -> python."""
    import math
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [clean(v) for v in obj]
    if hasattr(obj, "item") and not isinstance(obj, (str, bytes)):
        try:
            obj = obj.item()
        except (ValueError, AttributeError):
            pass
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def dumps(obj, **kw) -> str:
    return json.dumps(clean(obj), allow_nan=False, default=str, **kw)


def read_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    out = []
    for ln in path.read_text(encoding="utf8").splitlines():
        ln = ln.strip()
        if ln:
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                pass
    return out


def read_runs() -> list:
    """runs.jsonl without RETIRED models (the file itself keeps them)."""
    rows = read_jsonl(RUNS)
    for r in rows:
        for k in RETIRED & set(r.get("models", {})):
            del r["models"][k]
    return rows


def write_jsonl(path: Path, rows: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf8") as fh:
        for r in rows:
            fh.write(dumps(r, separators=(",", ":"), ensure_ascii=False) + "\n")
    tmp.replace(path)


def _strip(models: dict, pop: bool = True) -> dict:
    """Keep only the scalar forecast values (drop plotting series etc.), plus the PoP record
    (wxc_pop; display/verification only) unless pop=False."""
    keep = VARS + ["init_time_utc", "valid_range_utc", "error"] + (["pop"] if pop else [])
    return {k: {kk: v.get(kk) for kk in keep if kk in v and (kk != "pop" or v[kk])}
            for k, v in models.items()}


# ----------------------------------------------------------------------------
# runs
# ----------------------------------------------------------------------------
def append_run(generated_at: str, station: str, target_day: date, models: dict, hindcast: bool = False):
    rows = read_jsonl(RUNS)
    # PoP is verified from live runs only (no PoP hindcasts), so hindcast rows don't keep it
    row = {"generated_at_utc": generated_at, "station": station,
           "target_date": target_day.isoformat(), "models": _strip(models, pop=not hindcast)}
    if hindcast:
        row["hindcast"] = True
    rows.append(row)
    write_jsonl(RUNS, rows)


def migrate_legacy_history():
    """One-time import of forecast_history.jsonl (one entry per UTC day) into runs.jsonl."""
    if RUNS.exists() or not LEGACY_HISTORY.exists():
        return 0
    rows = []
    for h in read_jsonl(LEGACY_HISTORY):
        site = h.get("meta", {}).get("site", "")
        icao = site[site.rfind("(") + 1: site.rfind(")")] if "(" in site else None
        tgt = None
        for m in h.get("models", {}).values():
            vr = m.get("valid_range_utc")
            if vr:
                tgt = vr[0][:10]
                break
        if icao and tgt:
            rows.append({"generated_at_utc": h.get("generated_at_utc"), "station": icao,
                         "target_date": tgt, "models": _strip(h.get("models", {})),
                         "migrated": True})
    write_jsonl(RUNS, rows)
    print(f"Migrated {len(rows)} legacy history entries into {RUNS.name}")
    return len(rows)


# ----------------------------------------------------------------------------
# hourly series (for the "today so far" figure)
# ----------------------------------------------------------------------------
SERIES_DIR = DATA / "series"


def save_series(station: str, day: date, kind: str, generated_at: str, models: dict, hindcast=False):
    """kind: 'submitted' (last runs before the 00Z deadline) or 'latest'."""
    SERIES_DIR.mkdir(parents=True, exist_ok=True)
    path = SERIES_DIR / f"{station}_{day.isoformat()}_{kind}.json"
    path.write_text(dumps({"station": station, "target_date": day.isoformat(), "kind": kind,
                           "generated_at_utc": generated_at, "hindcast": hindcast, "models": models}))
    return path


def load_series(station: str, day: date, kind: str) -> Optional[dict]:
    path = SERIES_DIR / f"{station}_{day.isoformat()}_{kind}.json"
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


# ----------------------------------------------------------------------------
# observations
# ----------------------------------------------------------------------------
def wind_is_final(rec: dict) -> bool:
    """The stored wind is official: from a final CLI (or METAR above it, or no CLI at the site).
    Records from before wxc_obs.OBS_METHOD 2 only had wind_source / cli_preliminary."""
    s = (rec.get("source") or {}).get("wind_max_kt")
    if s is not None:
        return s != "pending"
    return rec.get("wind_source") == "CLI" and not rec.get("cli_preliminary")


def upsert_observations(records: list):
    rows = {(r["station"], r["date"]): r for r in read_jsonl(OBS)}
    for r in records:
        key = (r["station"], r["date"])
        old = rows.get(key)
        # never replace a final wind with a pending one (e.g. the CLI fetch failed this time)
        if old and wind_is_final(old) and not wind_is_final(r):
            r = {**r, **{k: old[k] for k in old if k.startswith("cli_") or k in ("wind_max_kt", "wind_source")}}
            r["source"] = {**r.get("source", {}),
                           "wind_max_kt": (old.get("source") or {}).get("wind_max_kt", "cli")}
            r["pending"] = [v for v in r.get("pending", []) if v != "wind_max_kt"]
            r["final"] = bool(r.get("complete")) and not r["pending"]
        rows[key] = r
    write_jsonl(OBS, sorted(rows.values(), key=lambda r: (r["station"], r["date"])))


GIVE_UP_WAITING_HOURS = 48    # stop re-fetching a day after this long (CLI never came)


def obs_is_final(rec: Optional[dict], has_cli: bool, now: datetime) -> bool:
    """True when a stored observation won't change, so it needn't be fetched again.
    (has_cli is kept for callers; the record itself says what is still pending.)"""
    from wxc_obs import OBS_METHOD
    if not rec:
        return False
    if rec.get("obs_method", 1) < OBS_METHOD:   # stored by an older method: fetch once more
        return False
    day_end = datetime.fromisoformat(rec["date"]).replace(tzinfo=timezone.utc) + timedelta(days=1, hours=6)
    if now - day_end > timedelta(hours=GIVE_UP_WAITING_HOURS):
        return True
    return bool(rec.get("final"))


def obs_days_to_fetch(station: str, days: list, has_cli: bool, now: datetime) -> list:
    stored = {o["date"]: o for o in read_jsonl(OBS) if o["station"] == station}
    return [d for d in days if not obs_is_final(stored.get(d.isoformat()), has_cli, now)]


# ----------------------------------------------------------------------------
# scoring
# ----------------------------------------------------------------------------
def precip_points(fc: float, ob: float) -> float:
    lo, hi = sorted([round(fc * 100), round(ob * 100)])
    pts = 0.0
    for h in range(lo, hi):          # each 0.01" step between the two values
        v = h + 1                    # upper edge of this hundredth, in hundredths
        pts += 0.4 if v <= 10 else 0.3 if v <= 25 else 0.2 if v <= 50 else 0.1
    return round(pts, 1)


def _r(x):
    from wxc_obs import round_half_up
    return round_half_up(x)


def submitted(v: str, x: float) -> float:
    """A forecast value as entered on the WxChallenge form."""
    return round(x, 2) if v == "precip_in" else _r(x)


def var_points(v: str, fc: float, ob: float) -> float:
    """Error points for one variable (fc as forecast, rounded here as submitted)."""
    f = submitted(v, fc)
    if v == "precip_in":
        return precip_points(f, ob)
    return (0.5 if v == "wind_max_kt" else 1.0) * abs(f - ob)


def score_day(fc: dict, ob: dict) -> Optional[dict]:
    if any(fc.get(v) is None for v in VARS) or any(ob.get(v) is None for v in VARS):
        return None
    f = {v: submitted(v, fc[v]) for v in VARS}
    err = {v: round(f[v] - ob[v], 2) for v in VARS}
    pts = sum(var_points(v, f[v], ob[v]) for v in VARS)
    return {"forecast": f, "error": err, "points": round(pts, 1)}


def _before_deadline(runs: list, station: str, day: str) -> list:
    deadline = datetime.fromisoformat(day).replace(tzinfo=timezone.utc)   # 00Z on day D
    return sorted((r for r in runs if r["station"] == station and r["target_date"] == day
                   and datetime.fromisoformat(r["generated_at_utc"]) < deadline),
                  key=lambda r: r["generated_at_utc"])


def run_for_day(runs: list, station: str, day: str) -> Optional[dict]:
    cands = _before_deadline(runs, station, day)
    return cands[-1] if cands else None


# models no longer used: kept in runs.jsonl but left out of scoring, the page and the consensus
RETIRED = {"NAM_MOS", "GEPS"}


def run_too_old(fc: dict, ref: datetime) -> bool:
    """True when fc's run (init_time_utc) is more than MAX_RUN_AGE_HOURS before ref.
    Forecasts without an init time (e.g. the consensus) are never too old."""
    t = _init_time(fc)
    return t is not None and (ref.replace(tzinfo=None) - t).total_seconds() > MAX_RUN_AGE_HOURS * 3600


def forecasts_for_day(runs: list, station: str, day: str) -> dict:
    """Per model, the latest pre-deadline forecast that has values (so a model that
    failed in the last run is still scored from the run before). A live forecast is never
    replaced by a hindcast: a hindcast filling a gap (stamped at HINDCAST_HOUR, often after
    the last live run) must not override what was actually submitted, e.g. the consensus.
    Forecasts from a run more than MAX_RUN_AGE_HOURS old at the deadline are skipped (an
    earlier run's copy of the same stale run is skipped too, since the age is taken at the
    deadline)."""
    deadline = datetime.fromisoformat(day)
    out = {}
    for r in _before_deadline(runs, station, day):
        hind = bool(r.get("hindcast"))
        for name, fc in r["models"].items():
            if name in RETIRED or (hind and name in out and not out[name][2]):
                continue
            if all(fc.get(v) is not None for v in VARS) and not run_too_old(fc, deadline):
                out[name] = (fc, r["generated_at_utc"], hind)
    return out


def needs_hindcast(runs: list, station: str, day: str, min_models: int = 3) -> bool:
    """A day needs a hindcast if nothing (or almost nothing) was forecast for it before
    the deadline, and no hindcast was attempted yet (so failures aren't retried forever)."""
    if any(r.get("hindcast") and r["station"] == station and r["target_date"] == day for r in runs):
        return False
    return len(forecasts_for_day(runs, station, day)) < min_models


def hindcast_plan(runs: list, station: str, day: str, all_models: list, max_attempts: int = 2):
    """
    Which models to hindcast for `day`: all of them when the day was never forecast,
    only the missing ones when an earlier hindcast left gaps (e.g. a source was down),
    nothing once `max_attempts` hindcasts were made or everything is present.
    """
    # attempts are counted per model, so a model added later (e.g. RRFS) is still
    # hindcast for recent days, and a source that keeps failing is given up on
    tries = {}
    for r in runs:
        if r.get("hindcast") and r["station"] == station and r["target_date"] == day:
            for m in r["models"]:
                tries[m] = tries.get(m, 0) + 1
    have = forecasts_for_day(runs, station, day)
    return [m for m in all_models if m not in have and tries.get(m, 0) < max_attempts]


def scored_days(station: str, start: Optional[str] = None, end: Optional[str] = None,
                runs: Optional[list] = None, obs: Optional[list] = None) -> list:
    """
    One entry per observed day: obs, and per model the score of its last pre-deadline
    forecast ("models") plus the unrounded forecast itself ("forecasts", used to rebuild the
    consensus). Pass runs/obs to reuse already-loaded files (backtests).
    """
    runs = read_runs() if runs is None else runs
    obs = read_jsonl(OBS) if obs is None else obs
    obs = [o for o in obs if o["station"] == station and o.get("complete", True)
           and (not start or o["date"] >= start) and (not end or o["date"] <= end)]
    days = []
    for o in sorted(obs, key=lambda o: o["date"]):
        fcs = forecasts_for_day(runs, station, o["date"])
        entry = {"date": o["date"], "obs": {v: o.get(v) for v in VARS},
                 "wind_source": o.get("wind_source"),
                 "obs_source": o.get("source"), "obs_pending": o.get("pending") or [],
                 "run": max((t for _, t, _ in fcs.values()), default=None),
                 "hindcast": any(h for _, _, h in fcs.values()), "models": {}, "forecasts": {}}
        for name, (fc, t, hind) in fcs.items():
            s = score_day(fc, o)
            if s:
                s["run"] = t
                if hind:
                    s["hindcast"] = True
                entry["models"][name] = s
                entry["forecasts"][name] = {v: fc[v] for v in VARS}
        days.append(entry)
    return days


def decay_weight(age_days: float, half_life: Optional[float]) -> float:
    """NBM-style decaying-average weight; half_life None (or 0) means equal weights."""
    return 0.5 ** (age_days / half_life) if half_life else 1.0


def n_eff(weights: list) -> float:
    """Effective number of days behind a weighted mean: (sum w)^2 / sum(w^2)."""
    s2 = sum(w * w for w in weights)
    return sum(weights) ** 2 / s2 if s2 else 0.0


def day_weights(dates: list, half_lives: dict = HALF_LIFE_DAYS) -> dict:
    """{date: {var: weight}}, 1 for the newest date and decaying back from it."""
    if not dates:
        return {}
    ref = date.fromisoformat(max(dates))
    return {d: {v: decay_weight((ref - date.fromisoformat(d)).days, half_lives.get(v)) for v in VARS}
            for d in dates}


def model_stats(days: list, half_lives: dict = HALF_LIFE_DAYS) -> dict:
    """
    Per-model track record from scored days: totals plus decay-weighted bias and MAE.
    Ages count from the newest of `days`, so a model that missed recent days (e.g. USL) has
    fewer, older terms, a lower n_eff and so a smaller bias correction.
    """
    w = day_weights([d["date"] for d in days], half_lives)
    per = {}
    for d in days:
        for name, s in d["models"].items():
            per.setdefault(name, []).append((w[d["date"]], s))
    out = {}
    for name, lst in per.items():
        n = len(lst)
        pts = sum(s["points"] for _, s in lst)
        st = {"n_days": n, "total_points": round(pts, 1), "mean_points": round(pts / n, 2),
              "bias": {}, "mae": {}, "n_eff": {}}
        for v in VARS:
            ws = [wd[v] for wd, _ in lst]
            st["bias"][v] = round(sum(x * s["error"][v] for x, (_, s) in zip(ws, lst)) / sum(ws), 3)
            st["mae"][v] = round(sum(x * abs(s["error"][v]) for x, (_, s) in zip(ws, lst)) / sum(ws), 3)
            st["n_eff"][v] = round(n_eff(ws), 2)
        out[name] = st
    return out


def reconstruct_consensus(days: list, i: int, half_lives: dict = HALF_LIFE_DAYS,
                          lookback: Optional[int] = None, **kw) -> Optional[dict]:
    """
    The consensus for days[i] built only from what was known before it: the models'
    forecasts for that day, corrected and weighted with the track record of the earlier
    days (only those within `lookback` calendar days, if given). Extra keywords go to consensus().
    """
    d = days[i]
    day = date.fromisoformat(d["date"])
    prior = [p for p in days[:i] if p["date"] < d["date"]
             and (lookback is None or (day - date.fromisoformat(p["date"])).days <= lookback)]
    members = {n: fc for n, fc in d["forecasts"].items() if n != "CONSENSUS"}
    if not members:
        return None
    c = consensus(members, model_stats(prior, half_lives), **kw)
    return c if all(c.get(v) is not None for v in VARS) else None


def city_start_date(runs: list, station: str, since: str = "") -> Optional[str]:
    """A city's first forecast day: the first target day with a live (not hindcast) run."""
    live = [r["target_date"] for r in runs if r["station"] == station and not r.get("hindcast")
            and r["target_date"] >= since]
    return min(live) if live else None


def verify(station: str, start: Optional[str] = None, end: Optional[str] = None) -> dict:
    """
    Scores per day and model since `start`, plus each model's (decay-weighted) summary.
    Days before the city's first forecast day, and days whose consensus only exists from a
    hindcast, get a reconstructed consensus: what the current method would have submitted
    with only the earlier days' track record (never the day itself).
    """
    runs = read_runs()
    days = scored_days(station, start, end, runs=runs)
    city_start = city_start_date(runs, station, start or "")
    for i, d in enumerate(days):
        d["hindcast"] = city_start is None or d["date"] < city_start
        stored = d["models"].get("CONSENSUS")
        if d["hindcast"] or not stored or stored.get("hindcast"):
            c = reconstruct_consensus(days, i)
            s = score_day(c, d["obs"]) if c else None
            if s:
                s["reconstructed"] = True
                d["models"]["CONSENSUS"] = s
            else:
                d["models"].pop("CONSENSUS", None)
    weights = day_weights([d["date"] for d in days if d["models"]])
    for d in days:
        d.pop("forecasts")
        if d["date"] in weights:
            d["decay_weight"] = {v: round(w, 3) for v, w in weights[d["date"]].items()}
    return {"station": station, "city_start": city_start, "half_life_days": HALF_LIFE_DAYS,
            "days": days, "summary": model_stats(days)}


def current_period_start(station: str, today: date) -> str:
    """Start of the current city period (hindcast days included): first obs/run date for
    this station within the last PERIOD_DAYS + HINDCAST_DAYS + a week."""
    dates = [r["target_date"] for r in read_jsonl(RUNS) if r["station"] == station]
    dates += [o["date"] for o in read_jsonl(OBS) if o["station"] == station]
    cutoff = (today - timedelta(days=PERIOD_DAYS + HINDCAST_DAYS + 7)).isoformat()
    recent = sorted(d for d in dates if d >= cutoff)
    return recent[0] if recent else today.isoformat()


# ----------------------------------------------------------------------------
# consensus
# ----------------------------------------------------------------------------
def _init_time(m: dict) -> Optional[datetime]:
    t = m.get("init_time_utc")
    try:
        return datetime.strptime(t[:13], "%Y-%m-%dT%H") if t else None
    except (TypeError, ValueError):
        return None


def _stale_members(models: dict, now: Optional[datetime] = None) -> list:
    """Members whose run is more than STALE_HOURS older than the newest member's run, or
    (given now) more than MAX_RUN_AGE_HOURS old. Members without an init time (e.g.
    reconstructed days) are never called stale."""
    inits = {n: _init_time(m) for n, m in models.items()
             if n != "CONSENSUS" and n not in NOT_IN_CONSENSUS}
    known = [t for t in inits.values() if t]
    if not known:
        return []
    newest = max(known)
    return [n for n, t in inits.items() if t and ((newest - t).total_seconds() > STALE_HOURS * 3600
                                                  or (now is not None and run_too_old(models[n], now)))]


def consensus(models: dict, summary: dict, shrink_days=None, mae_offset=None,
              now: Optional[datetime] = None) -> dict:
    """
    Bias-corrected, skill-weighted blend of today's model values.
    Models with >= MIN_DAYS_FOR_CORRECTION verified days are bias-corrected (by the shrunk
    decay-weighted bias n_eff/(n_eff + BIAS_SHRINK_DAYS[var]) x mean error) and weighted by
    1/(MAE + MAE_OFFSET); a model without that track record uses its PROXY_TRACK_RECORD
    parent's if that has one, otherwise it joins uncorrected at the median weight.
    With no verified models at all, an equal-weight mean is used. Members whose run is more
    than STALE_HOURS older than the newest member's, or (given now) more than
    MAX_RUN_AGE_HOURS old, are left out.
    Precip is not bias-corrected (errors are too skewed), only weighted.
    shrink_days / mae_offset override the defaults (a number, or a dict per variable).
    """
    out, detail = {}, {}
    stale = _stale_members(models, now)
    for v in VARS:
        K = shrink_days if shrink_days is not None else BIAS_SHRINK_DAYS
        K = K[v] if isinstance(K, dict) else K
        off = mae_offset if mae_offset is not None else MAE_OFFSET
        off = off[v] if isinstance(off, dict) else off
        vals, wts, used, proxied = [], [], [], {}
        for name, m in models.items():
            if name == "CONSENSUS" or name in NOT_IN_CONSENSUS or name in stale or m.get(v) is None:
                continue
            s = summary.get(name)
            if not (s and s["n_days"] >= MIN_DAYS_FOR_CORRECTION):
                p = summary.get(PROXY_TRACK_RECORD.get(name))
                if p and p["n_days"] >= MIN_DAYS_FOR_CORRECTION:
                    s = p
                    proxied[name] = PROXY_TRACK_RECORD[name]
            if s and s["n_days"] >= MIN_DAYS_FOR_CORRECTION:
                n = s.get("n_eff", {}).get(v, s["n_days"])
                shrink = n / (n + K)
                x = m[v] - (shrink * s["bias"][v] if v != "precip_in" else 0.0)
                w = 1.0 / (s["mae"][v] + off)
            else:
                x, w = m[v], None
            vals.append(x); wts.append(w); used.append(name)
        unverified = [n for n, w in zip(used, wts) if w is None]
        # Drop members far from the median (a broken download shouldn't drag the blend)
        excluded = []
        tol = OUTLIER_TOLERANCE.get(v)
        if tol and len(vals) >= 3:
            med = sorted(vals)[len(vals) // 2] if len(vals) % 2 else \
                sum(sorted(vals)[len(vals) // 2 - 1: len(vals) // 2 + 1]) / 2
            keep = [abs(x - med) <= tol for x in vals]
            excluded = [n for n, k in zip(used, keep) if not k]
            vals = [x for x, k in zip(vals, keep) if k]
            wts = [w for w, k in zip(wts, keep) if k]
            used = [n for n, k in zip(used, keep) if k]
        if not vals:
            out[v] = None
            continue
        known = sorted(w for w in wts if w is not None)
        if known:
            # models without a track record yet (e.g. a new product) get the median
            # weight of the verified ones and no bias correction
            w_med = known[len(known) // 2]
            wts = [w_med if w is None else w for w in wts]
            method = (f"bias-corrected (n_eff/(n_eff+{K:g}) of each model's decay-weighted mean error), "
                      f"1/(MAE+{off:g}) weighted")
        else:
            wts = [1.0] * len(vals)
            method = "equal-weight mean (not enough verified days)"
        val = sum(x * w for x, w in zip(vals, wts)) / sum(wts)
        out[v] = round(max(val, 0.0) if v in ("precip_in", "wind_max_kt") else val,
                       2 if v == "precip_in" else 1)
        detail[v] = {"method": method, "members": used,
                     "weights": {n: round(w / sum(wts), 3) for n, w in zip(used, wts)}}
        if excluded:
            detail[v]["excluded_outliers"] = excluded
        if stale:
            detail[v]["excluded_stale"] = [n for n in stale if models[n].get(v) is not None]
        if any(n in used for n in proxied):
            detail[v]["proxy_track_record"] = {n: p for n, p in proxied.items() if n in used}
        if known and unverified:
            detail[v]["not_yet_verified"] = [n for n in unverified if n in used]
    out["method"] = detail
    return out


# ----------------------------------------------------------------------------
# page outputs
# ----------------------------------------------------------------------------
def write_verification(station: str, today: date) -> dict:
    start = current_period_start(station, today)
    res = verify(station, start=start)
    res["period_start"] = start
    res["generated_at_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    all_obs = read_jsonl(OBS)
    obs = [o for o in all_obs if o["station"] == station and o["date"] >= start]
    res["observations"] = obs
    try:                       # PoP verification (display only); never block the scoreboard
        import wxc_pop
        res["pop"] = wxc_pop.verify_pop(read_runs(), all_obs, station, start)
    except Exception as exc:
        print(f"Warning: PoP verification skipped ({type(exc).__name__}: {exc})")
    VERIF.write_text(dumps(res, indent=2))
    return res


def today_column(station: str, today_json: dict, days: list, runs: Optional[list] = None) -> Optional[dict]:
    """
    Today's scores so far (verification.json "today"; DISPLAY ONLY): each model's
    pre-deadline forecast scored against the observed extremes so far (today.json).
    Kept out of "days", so it never enters the summary, the totals or the consensus
    weights.
    """
    o = (today_json or {}).get("obs") or {}
    day = (today_json or {}).get("date")
    if not day or o.get("high") is None or o.get("low") is None:
        return None
    from wxc_obs import round_half_up
    ob = {"tmax_f": round_half_up(o["high"]), "tmin_f": round_half_up(o["low"]),
          "wind_max_kt": None if o.get("wind") is None else round_half_up(o["wind"]),
          "precip_in": round(float(o.get("precip") or 0.0), 2)}
    if ob["wind_max_kt"] is None:
        return None
    runs = read_runs() if runs is None else runs
    fcs = forecasts_for_day(runs, station, day)
    stored = fcs.get("CONSENSUS")
    if not stored or stored[2]:
        # no submitted consensus: rebuild it from the members and the verified days' record
        members = {n: fc for n, (fc, _, _) in fcs.items() if n != "CONSENSUS"}
        c = consensus(members, model_stats(days)) if members else None
        fcs.pop("CONSENSUS", None)
        if c and all(c.get(v) is not None for v in VARS):
            fcs["CONSENSUS"] = (c, None, True)
    models = {}
    for name, (fc, t, hind) in fcs.items():
        s = score_day(fc, ob)
        if not s:
            continue
        if name == "CONSENSUS" and (not stored or stored[2]):
            s["reconstructed"] = True
        elif t:
            s["run"] = t
        models[name] = s
    return {"date": day, "through_utc": today_json.get("through_utc"), "n_obs": o.get("n_obs"),
            "provisional": True, "obs": ob, "models": models}


def write_today_column(station: str, today_json: dict) -> Optional[dict]:
    """Add today's provisional column to the verification.json written earlier this run."""
    res = json.loads(VERIF.read_text())
    if res.get("station") != station:
        return None
    col = today_column(station, today_json, res.get("days") or [])
    done = {d["date"] for d in res.get("days") or [] if d.get("models")}
    if col and col["date"] in done:    # already verified (shouldn't happen): no second column
        col = None
    res["today"] = col
    VERIF.write_text(dumps(res, indent=2))
    return col


def print_summary(res: dict):
    s = res["summary"]
    if not s:
        print("Verification: no scored days yet for", res["station"])
        return
    print(f"\nVerification for {res['station']} since {res.get('period_start', '?')}")
    print(f"{'model':10s} {'n':>2s} {'pts/day':>7s} {'total':>6s}  "
          f"{'bias Tx':>7s} {'Tn':>5s} {'wind':>5s} {'pcp':>5s}")
    for name, v in sorted(s.items(), key=lambda kv: kv[1]["mean_points"]):
        b = v["bias"]
        print(f"{name:10s} {v['n_days']:2d} {v['mean_points']:7.1f} {v['total_points']:6.1f}  "
              f"{b['tmax_f']:7.1f} {b['tmin_f']:5.1f} {b['wind_max_kt']:5.1f} {b['precip_in']:5.2f}")


# same colours as the forecast figure (latest.png); MOS dashed, consensus black
STYLE = {"HRRR": ("C0", "-"), "RRFS": ("C8", "-"), "IFS": ("C1", "-"), "GFS": ("C2", "-"), "AIFS": ("C3", "-"),
         "IFS_HRES": ("#a63603", "-"),       # IFS at 9 km: a darker orange than IFS
         "GFS_MOS": ("C2", "--"), "NBM": ("C5", "--"), "USL": ("C6", "--"),
         "ENS": ("C9", "--"), "AIFS_ENS": ("C3", "--"), "GEFS": ("C4", "--"),
         "CONSENSUS": ("k", "-")}


def save_png(fig, path: Path, dpi: int):
    """Save a figure as a 256-colour PNG: these plots look the same and the file is ~3x smaller,
    which is what gets pushed to GitHub every run. Falls back to a plain save without Pillow."""
    import io
    try:
        from PIL import Image
    except ImportError:
        fig.savefig(path, dpi=dpi)
        return
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, format="png")
    buf.seek(0)
    with Image.open(buf) as im:
        im.convert("RGB").quantize(256, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)


def plot_verification(res: dict, path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    days = [d for d in res["days"] if d["models"]]
    if not days:
        return False
    names = sorted({m for d in days for m in d["models"]})
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    x = [d["date"][5:] for d in days]
    for i, name in enumerate(names):
        pts = [d["models"].get(name, {}).get("points") for d in days]
        cum, tot = [], 0.0
        for p in pts:
            tot += p if p is not None else 0.0
            cum.append(tot if p is not None else None)
        color, ls = STYLE.get(name, (f"C{(i + 6) % 10}", "-"))
        axes[0].plot(x, pts, marker="o", ls=ls, label=name, color=color)
        axes[1].plot(x, cum, marker="o", ls=ls, label=name, color=color)
    axes[0].set_ylabel("Error points (day)")
    axes[1].set_ylabel("Cumulative points")
    axes[1].set_xlabel("Forecast day (06Z-06Z)")
    for ax in axes:
        ax.grid(True, linestyle="--", alpha=0.4)
    axes[0].legend(ncol=4, fontsize=8)
    fig.suptitle(f"{res['station']}: model verification since {res.get('period_start')}")
    fig.tight_layout()
    save_png(fig, path, dpi=120)
    plt.close(fig)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--station", required=True)
    ap.add_argument("--start", help="first day YYYY-MM-DD")
    ap.add_argument("--end", help="last day YYYY-MM-DD")
    ap.add_argument("--no-fetch", action="store_true", help="use stored observations only")
    a = ap.parse_args()

    from wxc_stations import get_station
    from wxc_obs import get_observations
    st = get_station(a.station)
    migrate_legacy_history()
    if not a.no_fetch:
        end = date.fromisoformat(a.end) if a.end else datetime.now(timezone.utc).date()
        start = date.fromisoformat(a.start) if a.start else end - timedelta(days=PERIOD_DAYS)
        now = datetime(end.year, end.month, end.day, 12, tzinfo=timezone.utc) + timedelta(days=1)
        now = min(now, datetime.now(timezone.utc))
        upsert_observations(get_observations(st, days_back=(end - start).days + 1, now=now))
    res = verify(st.icao, a.start, a.end)
    res["period_start"] = a.start
    print_summary(res)


if __name__ == "__main__":
    main()
