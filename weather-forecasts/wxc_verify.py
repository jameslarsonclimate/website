"""
Forecast-vs-observation bookkeeping for the WxChallenge page.

Files (under data/wxchallenge/):
  runs.jsonl          every forecast run: station, target day, per-model values
  observations.jsonl  observed values per station/day (upserted; CLI finals replace prelims)
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
OUTLIER_TOLERANCE = {"tmax_f": 8.0, "tmin_f": 8.0, "wind_max_kt": 10.0}   # from the member median
PERIOD_DAYS = 14   # a city period is two weeks (Mon-Thu x2, ~8 forecast days)


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


def write_jsonl(path: Path, rows: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf8") as fh:
        for r in rows:
            fh.write(dumps(r, separators=(",", ":"), ensure_ascii=False) + "\n")
    tmp.replace(path)


def _strip(models: dict) -> dict:
    """Keep only the scalar forecast values (drop plotting series etc.)."""
    keep = VARS + ["init_time_utc", "valid_range_utc", "error"]
    return {k: {kk: v.get(kk) for kk in keep if kk in v} for k, v in models.items()}


# ----------------------------------------------------------------------------
# runs
# ----------------------------------------------------------------------------
def append_run(generated_at: str, station: str, target_day: date, models: dict, hindcast: bool = False):
    rows = read_jsonl(RUNS)
    row = {"generated_at_utc": generated_at, "station": station,
           "target_date": target_day.isoformat(), "models": _strip(models)}
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
# observations
# ----------------------------------------------------------------------------
def upsert_observations(records: list):
    rows = {(r["station"], r["date"]): r for r in read_jsonl(OBS)}
    for r in records:
        key = (r["station"], r["date"])
        old = rows.get(key)
        # never replace a final CLI-based record with a preliminary one
        if old and old.get("wind_source") == "CLI" and not old.get("cli_preliminary") \
                and (r.get("wind_source") != "CLI" or r.get("cli_preliminary")):
            r = {**r, **{k: old[k] for k in old if k.startswith("cli_") or k in ("wind_max_kt", "wind_source")}}
        rows[key] = r
    write_jsonl(OBS, sorted(rows.values(), key=lambda r: (r["station"], r["date"])))


GIVE_UP_WAITING_HOURS = 48    # stop re-fetching a day after this long (CLI never came)


def obs_is_final(rec: Optional[dict], has_cli: bool, now: datetime) -> bool:
    """True when a stored observation won't change, so it needn't be fetched again."""
    if not rec:
        return False
    day_end = datetime.fromisoformat(rec["date"]).replace(tzinfo=timezone.utc) + timedelta(days=1, hours=6)
    if now - day_end > timedelta(hours=GIVE_UP_WAITING_HOURS):
        return True
    if not rec.get("complete", False):
        return False
    return (not has_cli) or (rec.get("wind_source") == "CLI" and not rec.get("cli_preliminary"))


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


def score_day(fc: dict, ob: dict) -> Optional[dict]:
    if any(fc.get(v) is None for v in VARS) or any(ob.get(v) is None for v in VARS):
        return None
    f = {"tmax_f": _r(fc["tmax_f"]), "tmin_f": _r(fc["tmin_f"]),
         "wind_max_kt": _r(fc["wind_max_kt"]), "precip_in": round(fc["precip_in"], 2)}
    err = {v: round(f[v] - ob[v], 2) for v in VARS}
    pts = abs(err["tmax_f"]) + abs(err["tmin_f"]) + 0.5 * abs(err["wind_max_kt"]) \
        + precip_points(f["precip_in"], ob["precip_in"])
    return {"forecast": f, "error": err, "points": round(pts, 1)}


def _before_deadline(runs: list, station: str, day: str) -> list:
    deadline = datetime.fromisoformat(day).replace(tzinfo=timezone.utc)   # 00Z on day D
    return sorted((r for r in runs if r["station"] == station and r["target_date"] == day
                   and datetime.fromisoformat(r["generated_at_utc"]) < deadline),
                  key=lambda r: r["generated_at_utc"])


def run_for_day(runs: list, station: str, day: str) -> Optional[dict]:
    cands = _before_deadline(runs, station, day)
    return cands[-1] if cands else None


def forecasts_for_day(runs: list, station: str, day: str) -> dict:
    """Per model, the latest pre-deadline forecast that has values (so a model that
    failed in the last run is still scored from the run before)."""
    out = {}
    for r in _before_deadline(runs, station, day):
        for name, fc in r["models"].items():
            if all(fc.get(v) is not None for v in VARS):
                out[name] = (fc, r["generated_at_utc"], bool(r.get("hindcast")))
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
    tries = sum(1 for r in runs if r.get("hindcast") and r["station"] == station and r["target_date"] == day)
    have = forecasts_for_day(runs, station, day)
    if tries == 0:
        return list(all_models) if len(have) < 3 else []
    if tries >= max_attempts:
        return []
    return [m for m in all_models if m not in have]


def verify(station: str, start: Optional[str] = None, end: Optional[str] = None) -> dict:
    runs = read_jsonl(RUNS)
    obs = [o for o in read_jsonl(OBS) if o["station"] == station and o.get("complete", True)]
    if start:
        obs = [o for o in obs if o["date"] >= start]
    if end:
        obs = [o for o in obs if o["date"] <= end]
    days, per_model = [], {}
    for o in sorted(obs, key=lambda o: o["date"]):
        fcs = forecasts_for_day(runs, station, o["date"])
        entry = {"date": o["date"], "obs": {v: o.get(v) for v in VARS},
                 "wind_source": o.get("wind_source"),
                 "run": max((t for _, t, _ in fcs.values()), default=None),
                 "hindcast": any(h for _, _, h in fcs.values()), "models": {}}
        for name, (fc, t, hind) in fcs.items():
            s = score_day(fc, o)
            if s:
                s["run"] = t
                entry["models"][name] = s
                per_model.setdefault(name, []).append(s)
        days.append(entry)

    summary = {}
    for name, lst in per_model.items():
        n = len(lst)
        summary[name] = {
            "n_days": n,
            "total_points": round(sum(s["points"] for s in lst), 1),
            "mean_points": round(sum(s["points"] for s in lst) / n, 2),
            "bias": {v: round(sum(s["error"][v] for s in lst) / n, 2) for v in VARS},
            "mae": {v: round(sum(abs(s["error"][v]) for s in lst) / n, 2) for v in VARS},
        }
    return {"station": station, "days": days, "summary": summary}


def current_period_start(station: str, today: date) -> str:
    """Start of the current city period: first obs/run date for this station within ~3 weeks."""
    dates = [r["target_date"] for r in read_jsonl(RUNS) if r["station"] == station]
    dates += [o["date"] for o in read_jsonl(OBS) if o["station"] == station]
    cutoff = (today - timedelta(days=PERIOD_DAYS + 7)).isoformat()
    recent = sorted(d for d in dates if d >= cutoff)
    return recent[0] if recent else today.isoformat()


# ----------------------------------------------------------------------------
# consensus
# ----------------------------------------------------------------------------
def consensus(models: dict, summary: dict) -> dict:
    """
    Bias-corrected, skill-weighted blend of today's model values.
    Models with >= MIN_DAYS_FOR_CORRECTION verified days are bias-corrected and
    weighted by 1/(MAE + 0.5); models without that track record join uncorrected at
    the median weight. With no verified models at all, an equal-weight mean is used.
    Precip is not bias-corrected (errors are too skewed), only weighted.
    """
    out, detail = {}, {}
    for v in VARS:
        vals, wts, used = [], [], []
        for name, m in models.items():
            if name == "CONSENSUS" or m.get(v) is None:
                continue
            s = summary.get(name)
            if s and s["n_days"] >= MIN_DAYS_FOR_CORRECTION:
                x = m[v] - (s["bias"][v] if v != "precip_in" else 0.0)
                w = 1.0 / (s["mae"][v] + 0.5)
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
            val = sum(x * w for x, w in zip(vals, wts)) / sum(wts)
            method = "bias-corrected, 1/MAE weighted"
        else:
            val = sum(vals) / len(vals)
            method = "equal-weight mean (not enough verified days)"
        out[v] = round(max(val, 0.0) if v in ("precip_in", "wind_max_kt") else val,
                       2 if v == "precip_in" else 1)
        detail[v] = {"method": method, "members": used}
        if excluded:
            detail[v]["excluded_outliers"] = excluded
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
    obs = [o for o in read_jsonl(OBS) if o["station"] == station and o["date"] >= start]
    res["observations"] = obs
    VERIF.write_text(dumps(res, indent=2))
    return res


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
STYLE = {"HRRR": ("C0", "-"), "IFS": ("C1", "-"), "GFS": ("C2", "-"), "AIFS": ("C3", "-"),
         "GFS_MOS": ("C2", "--"), "NAM_MOS": ("C4", "--"), "NBM": ("C5", "--"), "CONSENSUS": ("k", "-")}


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
    fig.savefig(path, dpi=120)
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
