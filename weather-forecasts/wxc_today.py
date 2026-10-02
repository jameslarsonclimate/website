"""
"Today so far" figure: observations for the current WxChallenge day (06Z-06Z)
against the forecasts for that day.

  solid lines   the forecasts made before the 00Z deadline (what you submitted with)
  dashed lines  the newest runs, to show how the guidance has trended since
  black         every METAR so far (routine + specials): temperature, sustained wind
                with gusts, running precipitation total
  cloud panel   (display only) model cloud cover, METAR sky cover (open = CLR/SKC) and
                the GOES clear-sky-mask cloud fraction near the station
"""

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

import wxc_clouds
from wxc_verify import STYLE


def _so_far(obs: pd.DataFrame) -> dict:
    if obs.empty:
        return {}
    temps = pd.concat([obs["temp_f"], obs["max6_f"], obs["min6_f"]]).dropna()
    hi_idx = obs["temp_f"].idxmax() if obs["temp_f"].notna().any() else None
    lo_idx = obs["temp_f"].idxmin() if obs["temp_f"].notna().any() else None
    return {
        "high": None if temps.empty else temps.max(),
        "high_at": None if hi_idx is None else obs.loc[hi_idx, "valid"],
        "low": None if temps.empty else temps.min(),
        "low_at": None if lo_idx is None else obs.loc[lo_idx, "valid"],
        "wind": obs["wind_kt"].max(),
        "gust": obs["gust_kt"].max(),
        "precip": obs["precip_total_in"].iloc[-1],
        "last": obs["valid"].iloc[-1],
    }


def line_style(name: str, latest_run: bool) -> dict:
    """How a model's lines look in every panel of this figure (the cloud panel included)."""
    family = STYLE.get(name, ("C7", "-"))[1]
    ls, lw, alpha = ("--", 1.3, 0.75) if latest_run else ("-", 1.6, 0.9)
    # text guidance (MOS/NBM/USL) gets square markers so e.g. GFS and GFS MOS differ
    return dict(ls=ls, lw=lw, alpha=alpha, marker="s" if family == "--" else None, ms=3.5)


def _draw_clouds(ax, clouds: dict, start, end, now):
    wxc_clouds.draw_models(ax, clouds.get("submitted"), lambda n: line_style(n, False), utc=True)
    wxc_clouds.draw_models(ax, clouds.get("latest"), lambda n: line_style(n, True), utc=True)
    sky = clouds.get("metar")
    if sky is not None and not sky.empty:
        sky = sky[(sky["valid"] > start) & (sky["valid"] <= min(end, now))]
        cov, clr = sky[~sky["clear"]], sky[sky["clear"]]
        ax.plot(cov["valid"], cov["sky_pct"], "o", color="k", ms=5, label="METAR sky cover", zorder=6)
        if not clr.empty:
            ax.plot(clr["valid"], clr["sky_pct"], "o", mfc="white", mec="k", ms=5, label="METAR CLR/SKC", zorder=6)
    goes = clouds.get("goes") or []
    if goes:
        t = pd.to_datetime([g["hour"] for g in goes], utc=True)
        ax.plot(t, [g["cloud_pct"] for g in goes], "-", color="0.3", lw=1.6, marker="D", ms=3.5,
                label="GOES", zorder=5)
    # beside the panel, under its legend (inside it would sit on the 100 % lines)
    ax.text(1.012, 0.02, "ASOS sees clouds only up to 12k ft", transform=ax.transAxes,
            fontsize=7.5, va="bottom", ha="left", color="0.35")


def plot_today(station, day, now, obs: pd.DataFrame, submitted: dict, latest: dict, path: Path,
               clouds: dict = None) -> bool:
    """clouds (optional, display only) adds a cloud-cover panel at the bottom."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    start = pd.Timestamp(datetime(day.year, day.month, day.day, 6), tz="UTC")
    end = start + pd.Timedelta(hours=24)
    now = pd.Timestamp(now)
    n = 3 if clouds is None else 4
    fig, axes = plt.subplots(n, 1, figsize=(13.5, 10.5 if n == 3 else 14.0), sharex=True,
                             gridspec_kw={"height_ratios": [1, 1, 1, wxc_clouds.PANEL_RATIO][:n]})
    ax_t, ax_w, ax_p = axes[:3]

    if not obs.empty:
        obs = obs[(obs["valid"] > start) & (obs["valid"] <= min(end, now))]
    obs_total = pd.Series(dtype=float)
    if not obs.empty:
        obs_total = obs.set_index("valid")["precip_total_in"]

    def draw(group: dict, latest_run: bool):
        for name, s in (group or {}).get("models", {}).items():
            if not s or not s.get("times"):
                continue
            color = STYLE.get(name, ("C7", "-"))[0]
            t = pd.to_datetime(s["times"], utc=True)
            ok = (t >= start) & (t <= end)            # drop points outside the day (bad timestamps)
            if not ok.all():
                idx = [i for i in range(len(t)) if ok[i]]
                t = t[idx]
                s = {k: ([v[i] for i in idx] if isinstance(v, list) and len(v) == len(ok) else v) for k, v in s.items()}
            st = line_style(name, latest_run)
            run = s.get("init_time_utc")
            label = f"{name} {run[-2:]}Z" if run else name
            label += " (latest)" if latest_run else ""
            if s.get("temp_f"):
                ax_t.plot(t, s["temp_f"], color=color, label=label, **st)
            if s.get("wind_kt"):
                ax_w.plot(t, s["wind_kt"], color=color, **st)
            if s.get("precip_in"):
                p = pd.Series(s["precip_in"], index=t, dtype=float)
                # a run that starts during the day accumulates from its start time:
                # add what had already been observed so the lines are comparable
                if latest_run and not obs_total.empty and t[0] > start:
                    before = obs_total[obs_total.index <= t[0]]
                    p = p + (before.iloc[-1] if not before.empty else 0.0)
                ax_p.plot(t, p.values, color=color, **st)

    draw(submitted, latest_run=False)
    draw(latest, latest_run=True)

    if not obs.empty:
        routine = obs[obs["routine"]]
        ax_t.plot(obs["valid"], obs["temp_f"], "-", color="k", lw=3.6, label="Observed", zorder=5)
        ax_t.plot(routine["valid"], routine["temp_f"], "o", color="k", ms=5, zorder=6)
        ax_w.plot(obs["valid"], obs["wind_kt"], "-o", color="k", lw=3.6, ms=4.5, label="Observed wind", zorder=5)
        g = obs.dropna(subset=["gust_kt"])
        ax_w.plot(g["valid"], g["gust_kt"], "x", color="k", ms=7, label="Gusts", zorder=6)
        ax_p.step(obs["valid"], obs["precip_total_in"], where="post", color="k", lw=3.6,
                  label="Observed (running total)", zorder=5)

    for ax in axes:
        ax.axvspan(max(now, start), end, color="0.5", alpha=0.08, lw=0)
        if start <= now <= end:
            ax.axvline(now, color="0.35", lw=1, ls=":")
        ax.grid(True, ls="--", alpha=0.35)
        ax.set_xlim(start, end)
    ax_t.set_ylabel("Temperature (°F)")
    ax_w.set_ylabel("Wind speed (kt)")
    ax_p.set_ylabel("Precip since 06Z (in)")
    ax_p.set_ylim(bottom=0)
    if clouds is not None:
        try:
            _draw_clouds(axes[3], clouds, start, end, now)
        except Exception as exc:          # never lose the figure over the cloud panel
            print(f"  warning: cloud panel left empty ({type(exc).__name__}: {exc})")
        wxc_clouds.style_axis(axes[3])
    axes[-1].set_xlabel("Time (UTC)")
    axes[-1].xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%HZ\n%b %d"))
    for ax in axes:   # legends outside the plot so they never hide data
        if ax.get_legend_handles_labels()[0]:
            ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8, frameon=False)

    sf = _so_far(obs)
    if sf:
        def f(v, d=0):
            return "—" if v is None or pd.isna(v) else f"{v:.{d}f}"
        hi_at = f" ({sf['high_at']:%H%MZ})" if sf.get("high_at") is not None else ""
        lo_at = f" ({sf['low_at']:%H%MZ})" if sf.get("low_at") is not None else ""
        txt = (f"So far (through {sf['last']:%H%MZ}):  high {f(sf['high'])}°F{hi_at}   "
               f"low {f(sf['low'])}°F{lo_at}   max wind {f(sf['wind'])} kt (gust {f(sf['gust'])})   "
               f"precip {f(sf['precip'], 2)}\"")
        fig.text(0.5, 0.935, txt, ha="center", fontsize=10,
                 bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="0.7"))
    fig.suptitle(f"{station.label}: {day:%a %b %d} so far (06Z-06Z). Solid = runs before the 00Z "
                 f"deadline, dashed = latest runs", y=0.985, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return True


def _secs(times) -> "np.ndarray":
    """UTC times -> seconds since 1970 (independent of pandas' datetime resolution)."""
    import numpy as np
    idx = pd.DatetimeIndex(pd.to_datetime(times, utc=True))
    return np.asarray((idx - pd.Timestamp(0, tz="UTC")) / pd.Timedelta(seconds=1), dtype=float)


PENDING_GRACE_H = 1.0   # an extreme counts as settled this long after the forecast's time for it


def today_bias(obs: pd.DataFrame, submitted: dict, day, now) -> dict:
    """
    How each pre-deadline forecast is doing so far today: model values are
    interpolated to the routine METAR times (06Z..now) and compared with them.
    Errors are forecast minus observed (negative = running cold / light / dry).

    High / low: the model's scored daily value (its table number, e.g. the USL or MOS
    daily summary, which can go beyond its hourly values) minus the observed high / low
    so far. Until the time the model has its high (low) plus PENDING_GRACE_H, the
    comparison is marked pending, because the observed extreme can still change.
    Older series files without daily values fall back to the hourly extremes.
    """
    import numpy as np
    start = pd.Timestamp(datetime(day.year, day.month, day.day, 6), tz="UTC")
    now = pd.Timestamp(now)
    out = {"date": day.isoformat(), "through_utc": None, "obs": {}, "models": {}}
    if obs is None or obs.empty:
        return out
    obs = obs[(obs["valid"] > start) & (obs["valid"] <= now)]
    rout = obs[obs["routine"]].dropna(subset=["temp_f"])
    if rout.empty:
        return out
    sf = _so_far(obs)
    last = obs["valid"].iloc[-1]
    out["through_utc"] = last.strftime("%Y-%m-%dT%H:%M")
    out["obs"] = {"high": sf["high"], "low": sf["low"], "wind": sf["wind"], "precip": sf["precip"],
                  "n_obs": int(len(rout))}
    ot = _secs(rout["valid"])
    t_last = float(_secs([last])[0])
    t_start = float(_secs([start])[0])
    for name, s in (submitted or {}).get("models", {}).items():
        if not s or not s.get("times") or not s.get("temp_f"):
            continue
        t = _secs(s["times"])
        inside = (ot >= t[0]) & (ot <= t[-1])
        if inside.sum() < 2:
            continue
        def interp(vals, at):
            v = np.array([np.nan if x is None else x for x in vals], float)
            ok = np.isfinite(v)
            return np.interp(at, t[ok], v[ok]) if ok.sum() >= 2 else np.full(np.shape(at), np.nan)
        ft = interp(s["temp_f"], ot[inside])
        err_t = ft - rout["temp_f"].to_numpy()[inside]
        row = {"init_time_utc": s.get("init_time_utc"), "n": int(inside.sum()),
               "temp_bias": round(float(np.nanmean(err_t)), 1),
               "temp_mae": round(float(np.nanmean(np.abs(err_t))), 1)}

        # daily high / low: the scored value, timed by the model's own hourly curve
        tv = np.array([np.nan if x is None else x for x in s["temp_f"]], float)
        day_pts = (t >= t_start) & (t <= t_start + 86400) & np.isfinite(tv)
        if day_pts.any():
            idx = np.flatnonzero(day_pts)
            i_hi, i_lo = idx[np.argmax(tv[idx])], idx[np.argmin(tv[idx])]
            for key, fc_key, i, o, sign in (("high", "tmax_f", i_hi, sf.get("high"), 1),
                                            ("low", "tmin_f", i_lo, sf.get("low"), -1)):
                fc = s.get(fc_key)
                src = "daily"
                if fc is None or (isinstance(fc, float) and not np.isfinite(fc)):
                    fc, src = float(tv[i]), "hourly"
                at = pd.Timestamp(t[i], unit="s", tz="UTC")
                row[f"{key}_fcst"] = round(float(fc), 1)
                row[f"{key}_at"] = at.strftime("%Y-%m-%dT%H:%M")
                row[f"{key}_source"] = src
                if o is None or pd.isna(o):
                    row[f"{key}_err"], row[f"{key}_pending"] = None, True
                    continue
                row[f"{key}_err"] = round(float(fc) - float(o), 1)
                # settled once the forecast's time for it has passed, or the observation
                # has already gone past the forecast (the miss can only grow from there)
                passed = t_last >= t[i] + PENDING_GRACE_H * 3600
                beyond = sign * (float(o) - float(fc)) > 0
                row[f"{key}_pending"] = not (passed or beyond)

        if s.get("wind_kt"):
            ow = rout["wind_kt"].to_numpy(dtype=float)[inside]
            fw = interp(s["wind_kt"], ot[inside])
            row["wind_bias"] = round(float(np.nanmean(fw - ow)), 1)
        if s.get("precip_in"):
            tnow = min(t_last, t[-1])
            fp = float(interp(s["precip_in"], np.array([tnow]))[0])
            row["precip_so_far"] = round(fp, 2)
            row["precip_err"] = round(fp - float(sf["precip"] or 0.0), 2)
        out["models"][name] = row
    return out
