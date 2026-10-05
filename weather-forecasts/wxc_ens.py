"""
Global ensembles from the Open-Meteo ensemble API: one small point request instead of
gigabytes of global GRIB.

  ENS       ECMWF IFS ENS 0.25 deg, 51 members      (in the consensus)
  AIFS_ENS  ECMWF AIFS ENS, 51 members              (in the consensus)
  GEFS      NCEP GEFS 0.25 deg, 31 members          (shown and scored, NOT in the consensus)

  https://ensemble-api.open-meteo.com/v1/ensemble?models=ecmwf_ifs025,ecmwf_aifs025,ncep_gefs025&...

Open-Meteo serves only the latest run (the run time comes from each model's
meta.json), so ensembles are not hindcast; results are cached per run like the
other models, so repeated script runs reuse them.

Per member the WxChallenge day (06Z-06Z) is summarised: high, low, max wind and
precip total. The summary gives the ensemble mean (used as the model's forecast),
percentiles for box plots and precipitation probabilities.
Note: Open-Meteo interpolates the 3-hourly (IFS, GEFS) / 6-hourly (AIFS) output to
hourly values, so highs and lows are only as good as those output times (muted extremes).
Each model also gets a PoP record (wxc_pop): the share of members with >= 0.01" in the day
and in each 6-h block (block edges fall on output times, so the block sums are exact).
"""

from datetime import date, datetime, timedelta, timezone
from typing import Optional

import numpy as np

import wxc_cache
import wxc_pop

API = "https://ensemble-api.open-meteo.com/v1/ensemble"
META = "https://ensemble-api.open-meteo.com/data/{path}/static/meta.json"
# our label -> Open-Meteo model id (checked against the API on 2026-10-02)
MODELS = {"ENS": "ecmwf_ifs025", "AIFS_ENS": "ecmwf_aifs025", "GEFS": "ncep_gefs025"}
# meta.json folder per model id (GEFS doesn't follow the "<id>_ensemble" pattern)
META_PATH = {"ecmwf_ifs025": "ecmwf_ifs025_ensemble", "ecmwf_aifs025": "ecmwf_aifs025_ensemble",
             "ncep_gefs025": "ncep_gefs025"}
from wxc_verify import NOT_IN_CONSENSUS   # GEFS
EXTRA_ENABLED = True       # False skips GEFS (ECMWF ensembles unaffected)
PRECIP_THRESHOLDS = [0.01, 0.10, 0.25, 0.50]
PCTS = [0, 10, 25, 50, 75, 90, 100]


def _get_json(url, params=None):
    import requests
    r = requests.get(url, params=params, timeout=45)
    r.raise_for_status()
    return r.json()


def latest_init(model: str) -> Optional[datetime]:
    meta = _get_json(META.format(path=META_PATH.get(model, f"{model}_ensemble")))
    t = meta.get("last_run_initialisation_time")
    return datetime.fromtimestamp(t, tz=timezone.utc) if t else None


def members(hourly: dict, var: str, model: str) -> dict:
    """
    {member number: values}. Open-Meteo names keys "<var>_member07_<model>_ensemble" when
    several models are requested (but "<var>_member07_ncep_gefs025" for GEFS), and just
    "<var>_member07" when only one model is, so all layouts are accepted (control = member 0,
    no member tag).
    """
    out = {}
    for suffix in (f"_{model}_ensemble", f"_{model}", ""):
        if f"{var}{suffix}" in hourly:
            out[0] = hourly[f"{var}{suffix}"]
        for m in range(1, 100):
            k = f"{var}_member{m:02d}{suffix}"
            if k in hourly:
                out[m] = hourly[k]
        if out:
            return out
    return out


def summarize_members(hourly: dict, model: str, target_day: date) -> dict:
    times = np.array(hourly["time"], dtype="datetime64[m]")
    start = np.datetime64(datetime(target_day.year, target_day.month, target_day.day, 6), "m")
    end = start + np.timedelta64(24, "h")
    inst = (times >= start) & (times <= end)            # temps / winds: 06Z..06Z inclusive
    accum = (times > start) & (times <= end)            # hourly precip ending at each hour
    if inst.sum() < 20:
        raise ValueError(f"ensemble data does not cover {target_day} 06Z-06Z")
    T = members(hourly, "temperature_2m", model)
    W = members(hourly, "wind_speed_10m", model)
    P = members(hourly, "precipitation", model)
    ids = sorted(set(T) & set(W) & set(P))
    if not ids:
        raise ValueError(f"no {model} ensemble members in the Open-Meteo response "
                         f"(keys like {list(hourly)[1:3]})")
    arr = lambda d, m, mask: np.array([np.nan if v is None else v for v in np.asarray(d[m], dtype=object)[mask]], float)  # noqa: E731
    per = {"tmax_f": [], "tmin_f": [], "wind_max_kt": [], "precip_in": []}
    for m in ids:
        t, w, p = arr(T, m, inst), arr(W, m, inst), arr(P, m, accum)
        per["tmax_f"].append(np.nanmax(t))
        per["tmin_f"].append(np.nanmin(t))
        per["wind_max_kt"].append(np.nanmax(w))
        per["precip_in"].append(np.nansum(p))
    stats = {}
    for v, vals in per.items():
        a = np.array(vals, float)
        stats[v] = {"mean": round(float(a.mean()), 2), "std": round(float(a.std()), 2),
                    **{f"p{q}": round(float(np.percentile(a, q)), 2) for q in PCTS}}
    pr = np.array(per["precip_in"])
    stats["precip_prob"] = {f"{th:.2f}": round(float((pr >= th - 1e-9).mean()), 3) for th in PRECIP_THRESHOLDS}
    # PoP: member fractions for the day and each 6-h block (hourly precip = hour ending at t)
    blocks = {}
    for lab, b0, b1 in wxc_pop.block_windows(target_day):
        sel = (times > np.datetime64(b0, "m")) & (times <= np.datetime64(b1, "m"))
        if sel.sum() == 6:
            blocks[lab] = [float(np.nansum(arr(P, m, sel))) for m in ids]
    pop = wxc_pop.from_members(per["precip_in"], blocks)

    # hourly ensemble mean / 10th / 90th percentile series (for figures)
    sel = inst
    tt = np.array([arr(T, m, sel) for m in ids])
    ww = np.array([arr(W, m, sel) for m in ids])
    pp = np.array([np.concatenate([[0.0], np.cumsum(np.nan_to_num(arr(P, m, sel)[1:]))]) for m in ids])
    series = {
        "times": [str(t)[:16] for t in times[sel]],
        "tmp_f": [round(float(x), 1) for x in np.nanmean(tt, 0)],
        "tmp_p10": [round(float(x), 1) for x in np.nanpercentile(tt, 10, 0)],
        "tmp_p90": [round(float(x), 1) for x in np.nanpercentile(tt, 90, 0)],
        "wsp_kt": [round(float(x), 1) for x in np.nanmean(ww, 0)],
        "precip_cum_in": [round(float(x), 3) for x in np.nanmean(pp, 0)],
    }
    return {"n_members": len(ids), "stats": stats, "series": series, "pop": pop,
            "members": {v: [round(float(x), 2) for x in vals] for v, vals in per.items()}}


def _result(label, init, summ, target_day):
    s = summ["stats"]
    start = datetime(target_day.year, target_day.month, target_day.day, 6)
    return {
        # the ensemble mean is this model's forecast in the tables, scoring and consensus
        "tmax_f": round(s["tmax_f"]["mean"], 1), "tmin_f": round(s["tmin_f"]["mean"], 1),
        "wind_max_kt": round(s["wind_max_kt"]["mean"], 1), "precip_in": round(s["precip_in"]["mean"], 2),
        "init_time_utc": init.strftime("%Y-%m-%dT%H"),
        "valid_range_utc": [start.strftime("%Y-%m-%dT%H"), (start + timedelta(days=1)).strftime("%Y-%m-%dT%H")],
        "note": f"ensemble mean of {summ['n_members']} members (Open-Meteo)"
                + ("; not in the consensus" if label in NOT_IN_CONSENSUS else ""),
        "ensemble": {"n_members": summ["n_members"], "stats": s, "members": summ["members"]},
        "series": summ["series"],
        "pop": summ.get("pop"),
    }


def get_ensembles(station, target_day: date, as_of: Optional[datetime] = None, only=None) -> dict:
    """ENS, AIFS_ENS and GEFS for the target day. Live only (Open-Meteo keeps only the
    latest run), so a hindcast (as_of) gets an error entry."""
    labels = [k for k in MODELS if (only is None or k in only)
              and (EXTRA_ENABLED or k not in NOT_IN_CONSENSUS)]
    out, need = {}, []
    fail = {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
            "init_time_utc": None, "valid_range_utc": None}
    for label in labels:
        model = MODELS[label]
        try:
            if as_of is not None:
                out[label] = {**fail, "error": "Open-Meteo serves only the latest run (no hindcast)"}
                continue
            init = latest_init(model)
            hit = wxc_cache.load(station.icao, label, init, target_day)
            if hit is not None:
                print(f"  {label:8s} {init:%Y-%m-%d %HZ}: using saved run")
                out[label] = hit
            else:
                need.append((label, init))
        except Exception as exc:
            out[label] = {**fail, "error": f"Open-Meteo meta failed: {exc}"}
    def request(group):
        return _get_json(API, {
            "latitude": station.lat, "longitude": station.lon,
            "hourly": "temperature_2m,wind_speed_10m,precipitation",
            "models": ",".join(MODELS[l] for l, _ in group),
            "temperature_unit": "fahrenheit", "wind_speed_unit": "kn", "precipitation_unit": "inch",
            "timezone": "GMT", "past_days": 1, "forecast_days": 4,
        })

    def summarize(group, data):
        for label, init in group:
            try:
                res = _result(label, init, summarize_members(data["hourly"], MODELS[label], target_day), target_day)
                wxc_cache.save(station.icao, label, init, target_day, res)
                out[label] = res
            except Exception as exc:
                out[label] = {**fail, "init_time_utc": init.strftime("%Y-%m-%dT%H"), "error": str(exc)}

    if need:
        try:
            summarize(need, request(need))
        except Exception as exc:
            # one combined request; if it fails (e.g. one model id rejected), ask per model so a
            # problem with one ensemble never costs the others
            for one in need:
                try:
                    summarize([one], request([one]))
                except Exception as exc1:
                    out[one[0]] = {**fail, "error": f"Open-Meteo request failed: {exc1 if len(need) > 1 else exc}"}
    for label in labels:
        r = out[label]
        print(f"  {label:8s} {r.get('init_time_utc')}: " + (r.get("error") or
              f"mean {r['tmax_f']}/{r['tmin_f']}F {r['wind_max_kt']}kt {r['precip_in']}in, "
              f"P(>=0.01\")={r['ensemble']['stats']['precip_prob']['0.01']:.0%}"))
    return out
