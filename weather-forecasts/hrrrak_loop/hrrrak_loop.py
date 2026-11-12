#!/usr/bin/env python
"""
HRRR-Alaska 4-panel loop for the WxChallenge Alaska city (PAYA, Yakutat).

For each 12Z / 18Z HRRR-AK run that feeds a WxChallenge forecast, downloads only the needed
GRIB fields (byte-range subsets via Herbie, ~6 MB per hour), draws one 300 dpi 4-panel frame
per forecast hour and stitches the frames into an MP4:

    2 m temperature (+ MSLP)  |  10 m wind speed + barbs
    total cloud cover          |  1-h precip, snow hatched  (or --panel4 dewpt / rh)

The header also shows PAYA's precip since 06Z (the start of the WxC window), from the run-total
APCP: blank before 06Z, frozen at the window total after 06Z the next day.

A run on UTC date D forecasts WxChallenge day D+1. Its window is 06Z-06Z, but the max wind is
verified over the NWS CLI day, midnight-to-midnight AKST = 09Z-09Z, so the loop runs from the
run's first output (f000) to 09Z on D+2 (12Z run: f000-f045, 18Z run: f000-f039). HRRR-AK
12Z/18Z reach f048. The time bar under the maps shows both windows.

Usage (the wxchallenge conda env has Herbie / cartopy):
    python hrrrak_loop.py                    # today's posted 12Z/18Z runs not yet made
    python hrrrak_loop.py --init 2026-11-12T18 [--force]
    python hrrrak_loop.py --init 2026-11-12T12 --fxx 0 6 21   # just some frames, no video

Output: ~/Documents/HRRR-AK/PAYA/<YYYYMMDD_HHz>/  (frames/*.png + <run>.mp4)
"""

import argparse
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
import time
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning, module="shapely")
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ------------------------------------------------------------------ configuration
STATION = "PAYA"
STATION_NAME = "Yakutat, AK"
STATION_LAT, STATION_LON = 59.507124, -139.659842
LOCAL_TZ = ZoneInfo("America/Yakutat")
WXC_START_H = 6                  # WxChallenge window: 06Z-06Z
LST_OFFSET_H = 9                 # AKST: the CLI day (max wind) is 09Z-09Z all year

# WxChallenge forecast days for PAYA (two Tue-Fri weeks from city_start 2026-11-10). A run is
# made only when the day it forecasts (UTC run date + 1) is one of these.
FORECAST_DAYS = [date(2026, 11, d) for d in (10, 11, 12, 13, 17, 18, 19, 20)]
CYCLES = (12, 18)

# Map view: a polar-stereographic frame whose central meridian runs through PAYA, spanning
# MAP_LAT_S-MAP_LAT_N along that meridian, MAP_ASPECT (width/height) wide. HRRR-AK's southern
# boundary is ~51.8N at 140W and 53.2N at 128W, so the bottom corners can be off the grid
# (drawn hatched).
MAP_CENTER_LON = -139.588
MAP_LAT_S, MAP_LAT_N = 51.5, 61.6
MAP_ASPECT = 1.26

OUT_ROOT = Path.home() / "Documents" / "HRRR-AK" / STATION
DPI = 300
FIGSIZE = (10.0, 8.7)            # inches -> 3000 x 2610 px at 300 dpi (H.264 level 5.1)
FPS = 3                          # frames (forecast hours) per second in the MP4
WORKERS = 4                      # parallel download + render processes
WAIT_MAX_MIN = 120               # how long to wait for the last needed hour to be posted
SOURCES = ["aws", "nomads"]

SEARCH = (r":(?:TMP|DPT|RH):2 m above ground:|:[UV]GRD:10 m above ground:"
          r"|:TCDC:entire atmosphere:|:MSLMA:mean sea level:|:C(?:SNOW|RAIN):surface:")
MM_TO_IN = 1 / 25.4
AWS_IDX = ("https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.{d:%Y%m%d}/alaska/"
           "hrrr.t{d:%H}z.wrfsfcf{f:02d}.ak.grib2.idx")

MS_TO_KT = 1.943844
LOV = -135.0                     # HRRR-AK grid orientation (225 E)


def k_to_f(k):
    return (k - 273.15) * 9 / 5 + 32


def map_crs():
    """Display projection: polar stereographic centred on PAYA's meridian (north is up there)."""
    import cartopy.crs as ccrs
    globe = ccrs.Globe(ellipse=None, semimajor_axis=6371229.0, semiminor_axis=6371229.0)
    return ccrs.NorthPolarStereo(central_longitude=MAP_CENTER_LON, true_scale_latitude=60.0,
                                 globe=globe)


def map_bounds(crs):
    """(x0, x1, y0, y1) of the view in map_crs coordinates."""
    import cartopy.crs as ccrs
    pc = ccrs.PlateCarree()
    y0 = crs.transform_point(MAP_CENTER_LON, MAP_LAT_S, pc)[1]
    y1 = crs.transform_point(MAP_CENTER_LON, MAP_LAT_N, pc)[1]
    half_w = (y1 - y0) * MAP_ASPECT / 2
    return -half_w, half_w, y0, y1


def native_crs():
    """HRRR-AK grid: north polar stereographic, LoV 225E, true at 60N, sphere R=6371229 m.
    (metpy/Herbie's .herbie.crs gives lat_0=0 for this grid, which is wrong.)"""
    import cartopy.crs as ccrs
    globe = ccrs.Globe(ellipse=None, semimajor_axis=6371229.0, semiminor_axis=6371229.0)
    return ccrs.NorthPolarStereo(central_longitude=LOV, true_scale_latitude=60.0, globe=globe)


# ------------------------------------------------------------------ run timing
def window_for(init: datetime):
    """(target day, (WxC start, end), (wind / CLI-day start, end)) in naive UTC for a run
    initialised at `init`: WxC 06Z-06Z, wind 09Z-09Z."""
    day = init.date() + timedelta(days=1)
    d0 = datetime(day.year, day.month, day.day)
    wxc = (d0 + timedelta(hours=WXC_START_H), d0 + timedelta(hours=WXC_START_H + 24))
    wind = (d0 + timedelta(hours=LST_OFFSET_H), d0 + timedelta(hours=LST_OFFSET_H + 24))
    return day, wxc, wind


def fxx_for(init: datetime):
    _, _, (_, end) = window_for(init)          # out to the end of the wind (CLI) day
    last = int((end - init).total_seconds() // 3600)
    return list(range(0, min(last, 48) + 1))


def run_dir(init: datetime) -> Path:
    return OUT_ROOT / f"{init:%Y%m%d_%H}z"


def posted(init: datetime, fxx: int) -> bool:
    import requests
    try:
        return requests.head(AWS_IDX.format(d=init, f=fxx), timeout=20).status_code == 200
    except Exception:
        return False


def wait_for(init: datetime, fxx: int, max_min: int) -> bool:
    t0 = time.time()
    while not posted(init, fxx):
        if time.time() - t0 > max_min * 60:
            return False
        log(f"  {init:%HZ} f{fxx:03d} not posted yet, waiting 3 min")
        time.sleep(180)
    return True


def log(msg):
    print(f"{datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} {msg}", flush=True)


# ------------------------------------------------------------------ data
def fetch(init: datetime, fxx: int, search: str, grib_dir: Path):
    """Datasets (list) for the GRIB messages matching `search`, with retries."""
    from herbie import Herbie
    last_exc = None
    for attempt in range(3):
        try:
            H = Herbie(init, model="hrrrak", product="sfc", fxx=fxx, priority=SOURCES,
                       save_dir=grib_dir, verbose=False)
            dss = H.xarray(search, remove_grib=True)
            return dss if isinstance(dss, list) else [dss]
        except Exception as exc:          # transient S3 / network errors
            last_exc = exc
            time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"f{fxx:03d} download failed ({search}): {last_exc}")


def apcp_search(fxx: int, hours: int) -> str:
    """APCP accumulated over the `hours` ending at fxx (1 = hourly bucket, fxx = run total).
    wgrib2 writes whole-day spans in days: f024's run total is "0-1 day acc", f048's "0-2 day"."""
    a = fxx - hours
    if a % 24 == 0 and fxx % 24 == 0:
        return f":APCP:surface:{a // 24}-{fxx // 24} day acc"
    return f":APCP:surface:{a}-{fxx} hour acc"


def station_total(init: datetime, fxx: int, grib_dir: Path) -> float:
    """Run-total precip (in) at PAYA from f000 to fxx."""
    if fxx <= 0:
        return 0.0
    ds = fetch(init, fxx, apcp_search(fxx, fxx), grib_dir)[0]
    lat = np.asarray(ds.latitude.values)
    lon = ((np.asarray(ds.longitude.values) + 180) % 360) - 180
    j, i = station_index(lat, lon)
    return float(np.asarray(ds["tp"].values)[j, i]) * MM_TO_IN


def load_hour(init: datetime, fxx: int, grib_dir: Path):
    """Cropped fields for one forecast hour (dict of 2-D arrays + lat/lon)."""
    dss = fetch(init, fxx, SEARCH, grib_dir)
    f = {}
    for ds in dss:
        for v in ds.data_vars:
            f[v] = np.asarray(ds[v].values, dtype=float)
    # precip (in): hourly bucket and run total (f000 has neither; f001's are the same message)
    if fxx >= 1:
        tot = np.asarray(fetch(init, fxx, apcp_search(fxx, fxx), grib_dir)[0]["tp"].values, float)
        one = tot if fxx == 1 else np.asarray(
            fetch(init, fxx, apcp_search(fxx, 1), grib_dir)[0]["tp"].values, float)
        f["apcp1"], f["apcp_tot"] = one * MM_TO_IN, tot * MM_TO_IN
    else:
        f["apcp1"] = f["apcp_tot"] = np.zeros_like(f["t2m"])
    for k in ("csnow", "crain"):
        f.setdefault(k, np.zeros_like(f["t2m"]))
    lat = np.asarray(dss[0].latitude.values)
    lon = ((np.asarray(dss[0].longitude.values) + 180) % 360) - 180
    valid = dss[0].valid_time.values

    # crop to the map view (+ margin) to keep plotting fast
    import cartopy.crs as ccrs
    crs = map_crs()
    x0, x1, y0, y1 = map_bounds(crs)
    pad = 0.05 * (x1 - x0)
    xyz = crs.transform_points(ccrs.PlateCarree(), lon, lat)
    m = ((xyz[..., 0] > x0 - pad) & (xyz[..., 0] < x1 + pad)
         & (xyz[..., 1] > y0 - pad) & (xyz[..., 1] < y1 + pad))
    jj, ii = np.where(m)
    sl = (slice(jj.min(), jj.max() + 1), slice(ii.min(), ii.max() + 1))
    out = {k: v[sl] for k, v in f.items()}
    out["lat"], out["lon"] = lat[sl], lon[sl]
    out["valid"] = datetime.utcfromtimestamp(valid.astype("datetime64[s]").astype(int))

    # grid-relative (HRRR-AK grid, LoV 225E) -> earth-relative wind
    a = np.deg2rad(out["lon"] - LOV)
    out["ue"] = out["u10"] * np.cos(a) + out["v10"] * np.sin(a)
    out["ve"] = -out["u10"] * np.sin(a) + out["v10"] * np.cos(a)
    return out


def station_index(lat, lon):
    d = (lat - STATION_LAT) ** 2 + ((lon - STATION_LON) * np.cos(np.deg2rad(STATION_LAT))) ** 2
    return np.unravel_index(np.argmin(d), d.shape)


def compass(u, v):
    deg = (270 - np.degrees(np.arctan2(v, u))) % 360
    pts = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
           "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return pts[int((deg + 11.25) // 22.5) % 16], deg


# ------------------------------------------------------------------ plotting
def render(init: datetime, fxx: int, panel4: str, frame_path: Path, grib_dir: Path,
           acc_bounds=None):
    """acc_bounds: PAYA run-total precip (in) at the WxC window's start and end hours, for the
    header's "since 06Z" total (None -> shown as n/a)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    d = load_hour(init, fxx, grib_dir)
    crs = map_crs()
    bounds = map_bounds(crs)
    pc = ccrs.PlateCarree()
    xyz = crs.transform_points(pc, d["lon"], d["lat"])
    X, Y = xyz[..., 0], xyz[..., 1]
    sj, si = station_index(d["lat"], d["lon"])

    t2m = k_to_f(d["t2m"])
    td = k_to_f(d["d2m"])
    spd = np.hypot(d["u10"], d["v10"]) * MS_TO_KT
    tcc = d["tcc"]
    mslp = d["mslma"] / 100.0
    st_dir, _ = compass(d["ue"][sj, si], d["ve"][sj, si])

    day, (x0, x1), (w0t, w1t) = window_for(init)
    valid = d["valid"]
    vloc = valid.replace(tzinfo=timezone.utc).astimezone(LOCAL_TZ)

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.1], left=0.012, right=0.968,
                          top=0.905, bottom=0.035, hspace=0.12, wspace=0.11)
    axes = [fig.add_subplot(gs[r, c], projection=crs) for r in (0, 1) for c in (0, 1)]

    coast = cfeature.NaturalEarthFeature("physical", "coastline", "10m")
    border = cfeature.NaturalEarthFeature("cultural", "admin_0_boundary_lines_land", "10m")
    lakes = cfeature.NaturalEarthFeature("physical", "lakes", "10m")

    def base(ax, line="k"):
        ax.set_extent(bounds, crs=crs)
        ax.patch.set_facecolor("white")
        ax.patch.set_hatch("////")          # shows only where HRRR-AK has no data
        ax.patch.set_edgecolor("0.75")
        ax.add_feature(coast, facecolor="none", edgecolor=line, linewidth=0.5, zorder=5)
        ax.add_feature(lakes, facecolor="none", edgecolor=line, linewidth=0.25, zorder=5)
        ax.add_feature(border, facecolor="none", edgecolor=line, linewidth=0.5,
                       linestyle=(0, (4, 2)), zorder=5)
        ax.gridlines(crs=pc, linewidth=0.25, color="0.35", alpha=0.6,
                          xlocs=range(-160, -115, 5), ylocs=range(48, 68, 2))
        ax.plot(STATION_LON, STATION_LAT, marker="*", ms=9, mfc="white", mec="k",
                mew=0.8, transform=pc, zorder=8)

    def cbar(ax, cf_, label, ticks=None):
        cb = fig.colorbar(cf_, ax=ax, orientation="vertical", fraction=0.04, pad=0.012,
                          shrink=0.92, ticks=ticks)
        cb.ax.tick_params(labelsize=6.5, length=2, width=0.5)
        cb.outline.set_linewidth(0.5)

    def station_box(ax, text):
        ax.text(0.015, 0.985, text, transform=ax.transAxes, ha="left", va="top", fontsize=8,
                fontweight="bold", zorder=10,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.3", lw=0.5, alpha=0.9))

    def title(ax, text):
        ax.set_title(text, fontsize=9, loc="left", pad=3, fontweight="bold")

    # 1) 2 m temperature + MSLP
    ax = axes[0]
    base(ax)
    lev = np.arange(-20, 62, 2)
    # purples/blues below freezing, greens->yellows->reds above; 32 F sits on the blue/green edge
    stops = [(-20, "#3f007d"), (0, "#6a51a3"), (10, "#2b5fbf"), (24, "#6baed6"),
             (31.99, "#c6e7f5"), (32, "#c7e9c0"), (40, "#41ab5d"), (46, "#d9ef8b"),
             (52, "#fdae61"), (60, "#a50026")]
    tcmap = mcolors.LinearSegmentedColormap.from_list(
        "temp", [((v + 20) / 80, c) for v, c in stops])
    cf1 = ax.contourf(X, Y, t2m, levels=lev, cmap=tcmap, extend="both", zorder=1)
    ax.contour(X, Y, t2m, levels=[32], colors="k", linewidths=0.6, linestyles="--", zorder=3)
    cs = ax.contour(X, Y, mslp, levels=np.arange(940, 1060, 4), colors="0.15",
                    linewidths=0.5, zorder=4)
    ax.clabel(cs, fontsize=5.5, fmt="%d", inline=True, inline_spacing=1)
    cbar(ax, cf1, "°F", ticks=np.arange(-20, 62, 10))
    title(ax, "2 m temperature (°F), MSLP (hPa), 32 °F dashed")
    station_box(ax, f"{STATION} {t2m[sj, si]:.0f}°F  |  {mslp[sj, si]:.0f} hPa")

    # 2) 10 m wind
    ax = axes[1]
    base(ax)
    wlev = np.arange(0, 65, 5)
    wcmap = mcolors.LinearSegmentedColormap.from_list(
        "wind", ["#ffffff", "#c6e2f5", "#6baed6", "#2171b5", "#41ab5d", "#fed976",
                 "#fd8d3c", "#e31a1c", "#99000d", "#54278f"])
    cf2 = ax.contourf(X, Y, spd, levels=wlev, cmap=wcmap, extend="max", zorder=1)
    n = max(1, X.shape[1] // 22)
    o = n // 2
    # earth-relative winds on lon/lat: cartopy rotates them into the PAYA-centred projection
    ax.barbs(d["lon"][o::n, o::n], d["lat"][o::n, o::n], d["ue"][o::n, o::n] * MS_TO_KT,
             d["ve"][o::n, o::n] * MS_TO_KT, length=4.2, linewidth=0.45, zorder=6,
             sizes=dict(emptybarb=0.12), transform=pc)
    cbar(ax, cf2, "kt", ticks=np.arange(0, 65, 10))
    title(ax, "10 m wind speed + barbs (kt)")
    station_box(ax, f"{STATION} {st_dir} {spd[sj, si]:.0f} kt")

    # 3) total cloud cover
    ax = axes[2]
    base(ax, line="#e9a23b")
    ccmap = mcolors.LinearSegmentedColormap.from_list(
        "cloud", ["#1d3557", "#3d5a80", "#7d8fa3", "#b9c2cc", "#e3e7eb", "#ffffff"])
    cf3 = ax.contourf(X, Y, tcc, levels=np.arange(0, 101, 10), cmap=ccmap, zorder=1)
    cbar(ax, cf3, "%", ticks=np.arange(0, 101, 20))
    title(ax, "Total cloud cover (%)")
    station_box(ax, f"{STATION} {tcc[sj, si]:.0f}%")

    # 4) 1-h precip (default), dewpoint or RH
    ax = axes[3]
    base(ax)
    p1 = d["apcp1"]
    ptype = ("snow" if d["csnow"][sj, si] >= 0.5 else
             "rain" if d["crain"][sj, si] >= 0.5 else "none")
    if panel4 == "precip":
        plev = [0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0]
        pcols = ["#c7e9c0", "#a1d99b", "#74c476", "#31a354", "#006d2c", "#fed976",
                 "#feb24c", "#fd8d3c", "#e31a1c", "#b10026"]
        pcmap = mcolors.ListedColormap(pcols).with_extremes(over="#7a0177")
        # white under the grid, so "no precip" isn't left showing the off-grid hatching
        ax.contourf(X, Y, np.zeros_like(p1), levels=[-1, 1], colors="white", zorder=0.5)
        cf4 = ax.contourf(X, Y, p1, levels=plev, cmap=pcmap,
                          norm=mcolors.BoundaryNorm(plev, len(pcols)), extend="max", zorder=1)
        # HRRR flags snow wherever the type would be snow, even with a trace: hatch only
        # where at least 0.01 in fell this hour
        snow = np.where((d["csnow"] >= 0.5) & (p1 >= 0.01), 1.0, 0.0)
        if snow.any():
            plt.rcParams["hatch.linewidth"] = 0.4
            sn = ax.contourf(X, Y, snow, levels=[0.5, 1.5], colors="none", hatches=["xxx"],
                             zorder=2)
            sn.set_edgecolor("#1f4e9a")
            sn.set_linewidth(0)
            ax.contour(X, Y, snow, levels=[0.5], colors="#1f4e9a", linewidths=0.4, zorder=3)
        cbar(ax, cf4, "in", ticks=plev)
        title(ax, "1-h precip (in), snow hatched")
        station_box(ax, f"{STATION} {p1[sj, si]:.2f} in/h  |  {ptype}" if fxx else
                    f"{STATION} (no precip at f000)")
    elif panel4 == "rh":
        cf4 = ax.contourf(X, Y, d["r2"], levels=np.arange(0, 101, 5), cmap="BrBG", zorder=1)
        cbar(ax, cf4, "%", ticks=np.arange(0, 101, 20))
        title(ax, "2 m relative humidity (%)")
        station_box(ax, f"{STATION} {d['r2'][sj, si]:.0f}%  (Td {td[sj, si]:.0f}°F)")
    else:
        cf4 = ax.contourf(X, Y, td, levels=np.arange(-30, 62, 2), cmap="BrBG",
                          extend="both", zorder=1)
        ax.contour(X, Y, td, levels=[32], colors="k", linewidths=0.6, linestyles="--", zorder=3)
        cbar(ax, cf4, "°F", ticks=np.arange(-30, 62, 10))
        title(ax, "2 m dewpoint (°F), 32 °F dashed")
        station_box(ax, f"{STATION} Td {td[sj, si]:.0f}°F  |  RH {d['r2'][sj, si]:.0f}%")

    # header
    in_wxc = x0 < valid <= x1
    in_wind = w0t < valid <= w1t
    fig.text(0.015, 0.975, f"HRRR-AK  {init:%HZ %a %d %b %Y}   f{fxx:03d}",
             fontsize=13, fontweight="bold", ha="left", va="top")
    fig.text(0.015, 0.944,
             f"Valid {valid:%HZ %a %d %b}  ({vloc:%-I %p %Z %a})     "
             f"{STATION} {STATION_NAME}  ★", fontsize=9.5, ha="left", va="top")
    if in_wxc:
        tag = "IN WxC WINDOW" + ("" if in_wind else "  (wind day starts 09Z)")
    elif in_wind:
        tag = "WIND DAY ONLY (WxC window over)"
    else:
        tag = "BEFORE WINDOW" if valid <= x0 else "AFTER WINDOW"
    hot = in_wxc or in_wind
    # PAYA precip since the 06Z start of the WxC window (frozen at the window total after it)
    tot = float(d["apcp_tot"][sj, si])
    if acc_bounds is None or acc_bounds[0] is None:
        acc_txt, since06 = "n/a", np.nan
    elif valid < x0:
        acc_txt, since06 = "—  (before 06Z)", np.nan
    elif valid <= x1:
        since06 = max(tot - acc_bounds[0], 0.0)
        acc_txt = f"{since06:.2f} in"
    elif acc_bounds[1] is not None:
        since06 = max(acc_bounds[1] - acc_bounds[0], 0.0)
        acc_txt = f"{since06:.2f} in  (final)"
    else:
        acc_txt, since06 = "n/a", np.nan
    fig.text(0.985, 0.975, f"WxChallenge day {day:%a %d %b}   ·   {STATION} precip since 06Z: "
             f"{acc_txt}", fontsize=10, ha="right", va="top", fontweight="bold")
    fig.text(0.985, 0.944, f"{x0:%HZ %d %b} – {x1:%HZ %d %b}  ·  {tag}", fontsize=9,
             ha="right", va="top", color=("#1a7f37" if in_wxc else "#1f5fa8") if hot else "0.35",
             fontweight="bold" if hot else "normal")

    # time bar: run start -> end of the wind day. Top row: WxC window 06Z-06Z; bottom row:
    # max-wind (CLI) day 09Z-09Z. Elapsed forecast shaded grey, current hour marked.
    tax = fig.add_subplot(gs[2, :])
    hr = lambda t: (t - init).total_seconds() / 3600
    t_end = hr(w1t)
    tax.set_xlim(0, t_end)
    tax.set_ylim(0, 1)
    tax.axhline(0.5, color="0.6", lw=0.4)
    rows = [((x0, x1), (0.5, 1.0), "#1a7f37", "#e3f1e6",
             f"WxChallenge window  {x0:%HZ %a} – {x1:%HZ %a}  (T, precip)"),
            ((w0t, w1t), (0.0, 0.5), "#1f5fa8", "#e1ebf7",
             f"Max wind: CLI day  {w0t:%HZ %a} – {w1t:%HZ %a}  (00–24 AKST)")]
    for (a, b), (y0, y1), col, light, label in rows:
        tax.axvspan(hr(a), hr(b), ymin=y0, ymax=y1, color=col, alpha=0.2, lw=0)
        tax.text((hr(a) + hr(b)) / 2, (y0 + y1) / 2, label, ha="center", va="center",
                 fontsize=6, color=col, zorder=5,
                 bbox=dict(boxstyle="round,pad=0.12", fc=light, ec="none"))
    tax.axvspan(0, fxx, color="0.55", alpha=0.35, lw=0)
    tax.axvline(fxx, color="k", lw=1.4, zorder=6)
    ticks = [h for h in range(0, int(t_end) + 1) if (init + timedelta(hours=h)).hour % 6 == 0]
    tax.set_xticks(ticks)
    tax.set_xticklabels([f"{(init + timedelta(hours=h)):%HZ\n%a}" for h in ticks], fontsize=5.5)
    tax.set_yticks([])
    tax.tick_params(length=2, width=0.5, pad=1)
    for s in tax.spines.values():
        s.set_linewidth(0.5)

    fig.savefig(frame_path, dpi=DPI)
    plt.close(fig)
    return fxx, {"t2m": round(float(t2m[sj, si]), 1), "td": round(float(td[sj, si]), 1),
                 "p1": round(float(p1[sj, si]), 3), "ptype": ptype,
                 "since06": "" if np.isnan(since06) else round(since06, 3),
                 "wind_kt": round(float(spd[sj, si]), 1), "dir": st_dir,
                 "tcc": round(float(tcc[sj, si])), "valid": f"{valid:%Y-%m-%dT%H}"}


def make_video(frames, out_mp4: Path, fps: int):
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    lst = out_mp4.with_suffix(".txt")
    dur = 1.0 / fps
    with open(lst, "w") as fh:
        for p in frames:
            fh.write(f"file '{p}'\nduration {dur:.4f}\n")
        fh.write(f"file '{frames[-1]}'\nduration 1.5\n")   # hold the last frame
        fh.write(f"file '{frames[-1]}'\n")
    cmd = [ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
           "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2:color=white,format=yuv420p",
           "-fps_mode", "vfr", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-movflags", "+faststart", str(out_mp4)]
    subprocess.run(cmd, check=True)
    lst.unlink()


def notify(msg):
    try:
        subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "HRRR-AK loop"'],
                       timeout=10, check=False)
    except Exception:
        pass


# ------------------------------------------------------------------ main
def process_run(init: datetime, panel4: str, only_fxx=None, force=False, wait=True):
    rd = run_dir(init)
    done = rd / ".complete"
    if done.exists() and not force and only_fxx is None:
        log(f"{init:%Y-%m-%d %HZ} already done ({rd})")
        return True
    fxx = only_fxx if only_fxx is not None else fxx_for(init)
    if wait and not wait_for(init, max(fxx), WAIT_MAX_MIN):
        log(f"{init:%Y-%m-%d %HZ} f{max(fxx):03d} still not posted after {WAIT_MAX_MIN} min, giving up")
        return False
    frames_dir = rd / "frames"
    grib_dir = rd / "_grib"
    frames_dir.mkdir(parents=True, exist_ok=True)
    tag = f"HRRRAK_{STATION}_{init:%Y%m%d_%H}z"
    log(f"{init:%Y-%m-%d %HZ}: f{fxx[0]:03d}-f{fxx[-1]:03d} ({len(fxx)} frames) -> {rd}")
    t0 = time.time()
    # PAYA run-total precip at the WxC window's start (06Z) and end hours, for "since 06Z"
    _, (x0, x1), _ = window_for(init)
    acc_bounds = []
    for t in (x0, x1):
        try:
            acc_bounds.append(station_total(init, int((t - init).total_seconds() // 3600), grib_dir))
        except Exception as exc:
            log(f"  warning: precip total at {t:%HZ %d %b} unavailable ({str(exc)[:120]})")
            acc_bounds.append(None)
    results, failed = {}, []
    with cf.ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(render, init, f, panel4, frames_dir / f"{tag}_f{f:03d}.png", grib_dir,
                          tuple(acc_bounds)): f
                for f in fxx}
        for fut in cf.as_completed(futs):
            f = futs[fut]
            try:
                _, vals = fut.result()
                results[f] = vals
            except Exception as exc:
                failed.append(f)
                log(f"  f{f:03d} FAILED: {type(exc).__name__}: {str(exc)[:200]}")
    shutil.rmtree(grib_dir, ignore_errors=True)
    log(f"  rendered {len(results)}/{len(fxx)} frames in {time.time() - t0:.0f} s")
    if failed:
        log(f"  missing frames: {sorted(failed)}; not making the video (re-run to retry)")
        return False
    if only_fxx is not None:
        return True
    frames = [frames_dir / f"{tag}_f{f:03d}.png" for f in fxx]
    mp4 = rd / f"{tag}.mp4"
    make_video(frames, mp4, FPS)
    with open(rd / f"{tag}_point.csv", "w") as fh:
        fh.write("fxx,valid_utc,t2m_f,dewpt_f,wind_kt,wind_dir,cloud_pct,precip_1h_in,ptype,"
                 "precip_since06z_in\n")
        for f in fxx:
            v = results[f]
            fh.write(f"{f},{v['valid']},{v['t2m']},{v['td']},{v['wind_kt']},{v['dir']},{v['tcc']},"
                     f"{v['p1']},{v['ptype']},{v['since06']}\n")
    done.write_text(datetime.now(timezone.utc).isoformat())
    log(f"  video: {mp4} ({mp4.stat().st_size / 1e6:.1f} MB)")
    notify(f"{init:%HZ %d %b} loop ready: {mp4.name}")
    return True


def due_runs(now: datetime):
    """Today's (UTC) 12Z/18Z runs that forecast a WxChallenge day and have started posting."""
    out = []
    for c in CYCLES:
        init = datetime(now.year, now.month, now.day, c)
        if init + timedelta(minutes=50) > now:      # f000 posts ~45 min after init
            continue
        if window_for(init)[0] not in FORECAST_DAYS:
            continue
        out.append(init)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--init", help="run to make, e.g. 2026-11-12T18 (default: today's due runs)")
    ap.add_argument("--fxx", type=int, nargs="+", help="only these forecast hours (no video)")
    ap.add_argument("--panel4", choices=["precip", "dewpt", "rh"], default="precip")
    ap.add_argument("--force", action="store_true", help="remake a run that is already done")
    ap.add_argument("--no-wait", action="store_true", help="don't wait for unposted hours")
    a = ap.parse_args()

    if a.init:
        runs = [datetime.strptime(a.init.replace("Z", ""), "%Y-%m-%dT%H")]
    else:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        runs = due_runs(now)
        if not runs:
            log("no HRRR-AK run due (not a WxChallenge forecast day, or before 12:50Z)")
            return 0
    ok = True
    for init in runs:
        ok &= process_run(init, a.panel4, only_fxx=a.fxx, force=a.force, wait=not a.no_wait)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
