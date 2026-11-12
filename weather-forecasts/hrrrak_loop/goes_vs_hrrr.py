#!/usr/bin/env python
"""
GOES-18 clear-sky mask vs HRRR-AK total cloud cover around PAYA (Yakutat), for the hours of a
HRRR-AK run that have already verified. One 300 dpi 4-panel frame per hour + an MP4 (2.4 fps):

    (a) GOES-18 ABI Clear Sky Mask (ACM: clear / prob. clear / prob. cloudy / cloudy)
    (b) HRRR-AK total cloud cover (%)
    (c) HRRR-AK total cloud cover + GOES cloudy/clear edge (BCM, lightly smoothed)
    (d) agreement: HRRR cloudy (TCDC >= 50 %) vs GOES cloudy (BCM == 1)

Matching: each HRRR valid time (top of the hour) is paired with the GOES-18 full-disk scan
(ABI-L2-ACMF, every 10 min) starting nearest it; the full disk is scanned north to south, so
Alaska is imaged within ~1-2 min of the scan start. PACUS does not reach Alaska. GOES pixels are
put on the HRRR-AK grid by nearest neighbour (GOES pixels are ~4-6 km here, HRRR 3 km).

Caveat: at night the mask has no visible channels; IR-only tests often miss low stratus / fog
(cloud top as warm as the surface), so night frames can show GOES "clear" under real overcast.

The GOES navigation / S3 listing comes from ../wxc_goes.py (imported, not modified); the map,
HRRR fetch and run folders from hrrrak_loop.py.

Usage (wxchallenge conda env):
    python goes_vs_hrrr.py                         # verified hours of runs made in the last 48 h
    python goes_vs_hrrr.py --init 2026-11-12T12 [--force] [--fxx 0 3 6]

Output: ~/Documents/HRRR-AK/PAYA/<YYYYMMDD_HHz>/goes_vs_hrrr/  (frames/*.png, .mp4, .csv)
"""

import argparse
import concurrent.futures as cf
import shutil
import sys
import time
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]

import hrrrak_loop as hl          # noqa: E402
import wxc_goes as wg             # noqa: E402  (read-only reuse: navigation + S3 listing)

BUCKET = "noaa-goes18"
PRODUCT = "ABI-L2-ACMF"           # full disk, every 10 min (PACUS doesn't cover Alaska)
GOES_LATENCY_MIN = 25             # a scan's L2 file is usually on S3 ~10-15 min after it starts
MAX_SCAN_OFFSET_MIN = 20          # skip an hour if the nearest scan is further away than this
LOOKBACK_H = 48                   # default mode: runs initialised in the last 48 h
CLOUDY_TCDC = 50.0                # HRRR "cloudy" threshold for the agreement panel
NN_MAX_KM = 10.0                  # no GOES pixel within this distance -> no data
WORKERS = 3


# ------------------------------------------------------------------ data
def hrrr_tcdc(init, fxx, grib_dir):
    """HRRR-AK total cloud cover cropped to the map view (+ lat/lon, map x/y, valid time)."""
    import cartopy.crs as ccrs
    ds = hl.fetch(init, fxx, ":TCDC:entire atmosphere:", grib_dir)[0]
    lat = np.asarray(ds.latitude.values)
    lon = ((np.asarray(ds.longitude.values) + 180) % 360) - 180
    crs = hl.map_crs()
    x0, x1, y0, y1 = hl.map_bounds(crs)
    pad = 0.05 * (x1 - x0)
    xyz = crs.transform_points(ccrs.PlateCarree(), lon, lat)
    m = ((xyz[..., 0] > x0 - pad) & (xyz[..., 0] < x1 + pad)
         & (xyz[..., 1] > y0 - pad) & (xyz[..., 1] < y1 + pad))
    jj, ii = np.where(m)
    sl = (slice(jj.min(), jj.max() + 1), slice(ii.min(), ii.max() + 1))
    valid = ds.valid_time.values.astype("datetime64[s]").astype(int)
    return {"tcc": np.asarray(ds["tcc"].values, float)[sl], "lat": lat[sl], "lon": lon[sl],
            "X": xyz[..., 0][sl], "Y": xyz[..., 1][sl],
            "valid": datetime.fromtimestamp(valid, tz=timezone.utc).replace(tzinfo=None)}


def goes_key(t: datetime):
    """(S3 key, scan start) of the full-disk ACM scan starting nearest valid time t (naive UTC)."""
    tz = t.replace(tzinfo=timezone.utc)
    keys = []
    for h in (tz - timedelta(hours=1), tz):          # a :55 scan may be nearest a top of hour
        keys += wg.list_keys(BUCKET, f"{PRODUCT}/{h:%Y/%j/%H}/")
    key = wg.nearest_scan(keys, tz)
    if key is None:
        return None, None
    return key, wg.scan_start(key).replace(tzinfo=None)


def goes_on_grid(key, h):
    """GOES ACM / BCM / DQF for the map area, nearest-neighbour onto the HRRR grid `h`, plus the
    station's GOES cloud % within wxc_goes.RADIUS_KM."""
    import netCDF4
    import requests
    from scipy.spatial import cKDTree
    import cartopy.crs as ccrs
    r = None
    for attempt in range(3):
        try:
            r = requests.get(f"{wg.S3.format(bucket=BUCKET)}/{key}", timeout=180)
            r.raise_for_status()
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(15 * (attempt + 1))
    ds = netCDF4.Dataset("acm.nc", memory=r.content)
    try:
        pv = ds["goes_imager_projection"]
        proj = {k: pv.getncattr(k) for k in pv.ncattrs()}
        x, y = np.asarray(ds["x"][:], float), np.asarray(ds["y"][:], float)
        gx, gy = wg.latlon_to_xy(h["lat"], h["lon"], proj)
        ix = np.where((x >= np.nanmin(gx)) & (x <= np.nanmax(gx)))[0]
        iy = np.where((y >= np.nanmin(gy)) & (y <= np.nanmax(gy)))[0]
        sx = slice(max(ix.min() - 3, 0), ix.max() + 4)
        sy = slice(max(iy.min() - 3, 0), iy.max() + 4)
        bcm = np.ma.filled(ds["BCM"][sy, sx], 255).astype(float)
        acm = np.ma.filled(ds["ACM"][sy, sx], 255).astype(float)
        dqf = np.ma.filled(ds["DQF"][sy, sx], 255)
        xs, ys = x[sx], y[sy]
    finally:
        ds.close()
    st_pct, st_n = wg.fraction_near(xs, ys, bcm.astype(int), dqf, proj, hl.STATION_LAT,
                                    hl.STATION_LON)
    bad = ~np.isin(dqf, wg.USABLE_DQF) | ~np.isin(bcm, (0, 1))
    bcm[bad], acm[bad] = np.nan, np.nan
    xx, yy = np.meshgrid(xs, ys)
    plat, plon = wg.xy_to_latlon(xx, yy, proj)
    ok = np.isfinite(plat) & np.isfinite(plon)
    pxy = hl.map_crs().transform_points(ccrs.PlateCarree(), plon[ok], plat[ok])[:, :2]
    tree = cKDTree(pxy)
    dist, idx = tree.query(np.column_stack([h["X"].ravel(), h["Y"].ravel()]))
    far = dist > NN_MAX_KM * 1000
    out = {}
    for name, arr in (("bcm", bcm), ("acm", acm)):
        v = arr[ok][idx]
        v[far] = np.nan
        out[name] = v.reshape(h["X"].shape)
    out["station_pct"], out["station_n"] = st_pct, st_n
    return out


def sun_elevation(t: datetime, lat: float, lon: float) -> float:
    """Approximate solar elevation (deg) at naive-UTC time t (NOAA low-accuracy formulas)."""
    doy = t.timetuple().tm_yday
    g = 2 * np.pi / 365 * (doy - 1 + (t.hour - 12) / 24)
    decl = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
            + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    eqt = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g)
                    - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    tst = t.hour * 60 + t.minute + eqt + 4 * lon
    ha = np.radians(tst / 4 - 180)
    la = np.radians(lat)
    cz = np.sin(la) * np.sin(decl) + np.cos(la) * np.cos(decl) * np.cos(ha)
    return float(90 - np.degrees(np.arccos(np.clip(cz, -1, 1))))


# ------------------------------------------------------------------ plotting
def render(init, fxx, frame_path: Path, grib_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from matplotlib.patches import Patch
    from scipy.ndimage import uniform_filter
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    h = hrrr_tcdc(init, fxx, grib_dir)
    valid = h["valid"]
    key, scan = goes_key(valid)
    if key is None or abs((scan - valid).total_seconds()) > MAX_SCAN_OFFSET_MIN * 60:
        raise RuntimeError(f"no GOES scan within {MAX_SCAN_OFFSET_MIN} min of {valid:%H:%MZ}")
    g = goes_on_grid(key, h)

    crs = hl.map_crs()
    bounds = hl.map_bounds(crs)
    X, Y, tcc = h["X"], h["Y"], h["tcc"]
    sj, si = hl.station_index(h["lat"], h["lon"])
    # HRRR mean TCDC within the same radius GOES uses at the station
    dkm = wg._km(hl.STATION_LAT, hl.STATION_LON, h["lat"], h["lon"])
    hrrr_near = float(np.nanmean(tcc[dkm <= wg.RADIUS_KM]))

    hc = tcc >= CLOUDY_TCDC
    gc = g["bcm"] == 1
    have = np.isfinite(g["bcm"])
    # agreement over the visible map only
    inview = (X >= bounds[0]) & (X <= bounds[1]) & (Y >= bounds[2]) & (Y <= bounds[3]) & have
    agree = float(np.mean((hc == gc)[inview]) * 100) if inview.any() else np.nan
    hrrr_frac = float(np.mean(hc[inview]) * 100) if inview.any() else np.nan
    goes_frac = float(np.mean(gc[inview]) * 100) if inview.any() else np.nan
    cat = np.full(tcc.shape, np.nan)
    cat[have & ~hc & ~gc] = 0           # both clear
    cat[have & hc & gc] = 1             # both cloudy
    cat[have & hc & ~gc] = 2            # HRRR cloudy, GOES clear
    cat[have & ~hc & gc] = 3            # GOES cloudy, HRRR clear

    sun = sun_elevation(valid, hl.STATION_LAT, hl.STATION_LON)
    night = sun < -6

    fig = plt.figure(figsize=hl.FIGSIZE, dpi=hl.DPI)
    gs = fig.add_gridspec(2, 2, left=0.012, right=0.968, top=0.862, bottom=0.05,
                          hspace=0.14, wspace=0.11)
    axes = [fig.add_subplot(gs[r, c], projection=crs) for r in (0, 1) for c in (0, 1)]
    pc = ccrs.PlateCarree()
    coast = cfeature.NaturalEarthFeature("physical", "coastline", "10m")
    border = cfeature.NaturalEarthFeature("cultural", "admin_0_boundary_lines_land", "10m")
    lakes = cfeature.NaturalEarthFeature("physical", "lakes", "10m")

    def base(ax, line="#e9a23b"):
        ax.set_extent(bounds, crs=crs)
        ax.patch.set_facecolor("white")
        ax.patch.set_hatch("////")
        ax.patch.set_edgecolor("0.75")
        ax.add_feature(coast, facecolor="none", edgecolor=line, linewidth=0.5, zorder=5)
        ax.add_feature(lakes, facecolor="none", edgecolor=line, linewidth=0.25, zorder=5)
        ax.add_feature(border, facecolor="none", edgecolor=line, linewidth=0.5,
                       linestyle=(0, (4, 2)), zorder=5)
        ax.gridlines(crs=pc, linewidth=0.25, color="0.35", alpha=0.6,
                     xlocs=range(-160, -115, 5), ylocs=range(48, 68, 2))
        ax.plot(hl.STATION_LON, hl.STATION_LAT, marker="*", ms=9, mfc="white", mec="k",
                mew=0.8, transform=pc, zorder=8)

    def cbar(ax, m, ticks=None, labels=None):
        cb = fig.colorbar(m, ax=ax, orientation="vertical", fraction=0.04, pad=0.012,
                          shrink=0.92, ticks=ticks)
        if labels:
            cb.ax.set_yticklabels(labels)
        cb.ax.tick_params(labelsize=6.5, length=2, width=0.5)
        cb.outline.set_linewidth(0.5)

    def title(ax, text):
        ax.set_title(text, fontsize=9, loc="left", pad=3, fontweight="bold")

    def station_box(ax, text):
        ax.text(0.015, 0.985, text, transform=ax.transAxes, ha="left", va="top", fontsize=8,
                fontweight="bold", zorder=10,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.3", lw=0.5, alpha=0.9))

    ccmap = mcolors.LinearSegmentedColormap.from_list(
        "cloud", ["#1d3557", "#3d5a80", "#7d8fa3", "#b9c2cc", "#e3e7eb", "#ffffff"])
    st_g = "n/a" if g["station_pct"] is None else f"{g['station_pct']:.0f}%"

    # (a) GOES ACM, 4 categories on the cloud colour scale
    ax = axes[0]
    base(ax)
    acmap = mcolors.ListedColormap(["#1d3557", "#5b7394", "#c9d0d8", "#ffffff"])
    m = ax.pcolormesh(X, Y, g["acm"], cmap=acmap, norm=mcolors.BoundaryNorm([-.5, .5, 1.5, 2.5, 3.5], 4),
                      shading="nearest", zorder=1, rasterized=True)
    cbar(ax, m, ticks=[0, 1, 2, 3], labels=["clear", "prob.\nclear", "prob.\ncloudy", "cloudy"])
    title(ax, f"GOES-18 clear sky mask  (scan {scan:%H:%M}Z)")
    station_box(ax, f"{hl.STATION} {st_g} cloudy within {wg.RADIUS_KM:.0f} km")

    # (b) HRRR-AK TCDC
    ax = axes[1]
    base(ax)
    m = ax.contourf(X, Y, tcc, levels=np.arange(0, 101, 10), cmap=ccmap, zorder=1)
    cbar(ax, m, ticks=np.arange(0, 101, 20))
    title(ax, f"HRRR-AK total cloud cover (%)  (valid {valid:%H:%M}Z)")
    station_box(ax, f"{hl.STATION} {tcc[sj, si]:.0f}%  ({hrrr_near:.0f}% mean within {wg.RADIUS_KM:.0f} km)")

    # (c) overlay: HRRR TCDC + GOES cloudy/clear edge
    ax = axes[2]
    base(ax, line="0.45")
    m = ax.contourf(X, Y, tcc, levels=np.arange(0, 101, 10), cmap=ccmap, zorder=1)
    gsm = uniform_filter(np.nan_to_num(g["bcm"], nan=0.0), size=3)
    ax.contour(X, Y, gsm, levels=[0.5], colors="#e03131", linewidths=0.75, zorder=4)
    cbar(ax, m, ticks=np.arange(0, 101, 20))
    title(ax, "HRRR-AK cloud (%) + GOES cloudy/clear edge (red)")
    station_box(ax, f"{hl.STATION} HRRR {tcc[sj, si]:.0f}%  |  GOES {st_g}")

    # (d) agreement
    ax = axes[3]
    base(ax, line="k")
    acols = ["#1d3557", "#e3e7eb", "#f08c00", "#7b2cbf"]
    ax.pcolormesh(X, Y, cat, cmap=mcolors.ListedColormap(acols),
                  norm=mcolors.BoundaryNorm([-.5, .5, 1.5, 2.5, 3.5], 4),
                  shading="nearest", zorder=1, rasterized=True)
    ax.legend(handles=[Patch(fc=c, ec="0.4", lw=0.4, label=l) for c, l in zip(acols, [
        "both clear", "both cloudy", "HRRR cloudy, GOES clear", "GOES cloudy, HRRR clear"])],
        loc="lower left", fontsize=6, framealpha=0.92, borderpad=0.4, handlelength=1.2)
    title(ax, f"Agreement (HRRR cloudy = TCDC ≥ {CLOUDY_TCDC:.0f}%)")
    station_box(ax, f"{agree:.0f}% of map agrees  |  cloudy: HRRR {hrrr_frac:.0f}%, GOES {goes_frac:.0f}%")

    # header
    vloc = valid.replace(tzinfo=timezone.utc).astimezone(hl.LOCAL_TZ)
    fig.text(0.015, 0.975, f"GOES-18 vs HRRR-AK clouds   ·   HRRR {init:%HZ %a %d %b}  f{fxx:03d}",
             fontsize=13, fontweight="bold", ha="left", va="top")
    dt = (scan - valid).total_seconds() / 60
    fig.text(0.015, 0.940,
             f"HRRR valid {valid:%H:%MZ %a %d %b} ({vloc:%-I %p %Z})   ·   GOES-18 full-disk scan "
             f"{scan:%H:%M}Z ({dt:+.0f} min)   ·   {hl.STATION} {hl.STATION_NAME} ★",
             fontsize=8.5, ha="left", va="top")
    fig.text(0.015, 0.915,
             f"Sun at {hl.STATION}: {sun:+.0f}°  " + (
                 "· NIGHT: the mask is IR-only and often misses low stratus / fog"
                 if night else "· daytime: visible + IR tests"),
             fontsize=8, ha="left", va="top", color="#b02a37" if night else "0.3",
             fontweight="bold" if night else "normal")
    fig.text(0.985, 0.012, "GOES-18 ABI L2 ACMF (NOAA, AWS) nearest-neighbour on the HRRR-AK 3 km "
             "grid; hatched = no data", fontsize=6, ha="right", va="bottom", color="0.4")

    fig.savefig(frame_path, dpi=hl.DPI)
    plt.close(fig)
    return fxx, {"valid": f"{valid:%Y-%m-%dT%H:%M}", "scan": f"{scan:%Y-%m-%dT%H:%M:%S}",
                 "hrrr_pt": round(float(tcc[sj, si])), "hrrr_15km": round(hrrr_near),
                 "goes_15km": "" if g["station_pct"] is None else g["station_pct"],
                 "agree": round(agree, 1), "hrrr_cloudy": round(hrrr_frac, 1),
                 "goes_cloudy": round(goes_frac, 1), "sun": round(sun, 1)}


# ------------------------------------------------------------------ driver
def verified_fxx(init, now):
    """Forecast hours of the run (same span as the loop) whose valid time has a GOES scan by now."""
    return [f for f in hl.fxx_for(init)
            if init + timedelta(hours=f) <= now - timedelta(minutes=GOES_LATENCY_MIN)]


def process(init, now, only_fxx=None, force=False):
    rd = hl.run_dir(init) / "goes_vs_hrrr"
    frames_dir, grib_dir = rd / "frames", rd / "_grib"
    frames_dir.mkdir(parents=True, exist_ok=True)
    tag = f"GOESvsHRRRAK_{hl.STATION}_{init:%Y%m%d_%H}z"
    fxx = only_fxx if only_fxx is not None else verified_fxx(init, now)
    path = lambda f: frames_dir / f"{tag}_f{f:03d}.png"
    todo = [f for f in fxx if force or only_fxx is not None or not path(f).exists()]
    if not todo:
        hl.log(f"GOES vs HRRR {init:%Y-%m-%d %HZ}: nothing new ({len(fxx)} verified hours done)")
        return True
    hl.log(f"GOES vs HRRR {init:%Y-%m-%d %HZ}: {len(todo)} new frame(s) of {len(fxx)} verified hours")
    t0 = time.time()
    ok = True
    rows = {}
    csv = rd / f"{tag}.csv"
    if csv.exists():                                  # keep rows of frames made earlier
        lines = csv.read_text().splitlines()
        for ln in lines[1:]:
            rows[int(ln.split(",")[0])] = ln
    with cf.ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(render, init, f, path(f), grib_dir): f for f in todo}
        for fut in cf.as_completed(futs):
            f = futs[fut]
            try:
                _, v = fut.result()
                rows[f] = ",".join(str(x) for x in [f, v["valid"], v["scan"], v["hrrr_pt"],
                                   v["hrrr_15km"], v["goes_15km"], v["agree"], v["hrrr_cloudy"],
                                   v["goes_cloudy"], v["sun"]])
            except Exception as exc:
                ok = False
                hl.log(f"  f{f:03d} FAILED: {type(exc).__name__}: {str(exc)[:200]}")
    shutil.rmtree(grib_dir, ignore_errors=True)
    csv.write_text("fxx,valid_utc,goes_scan_utc,hrrr_tcdc_pt,hrrr_tcdc_15km,goes_cloudy_15km,"
                   "map_agree_pct,map_hrrr_cloudy_pct,map_goes_cloudy_pct,sun_elev_deg\n"
                   + "\n".join(rows[k] for k in sorted(rows)) + "\n")
    frames = sorted(frames_dir.glob(f"{tag}_f*.png"))
    hl.log(f"  rendered in {time.time() - t0:.0f} s; {len(frames)} frames on disk")
    if only_fxx is None and frames:
        mp4 = rd / f"{tag}.mp4"
        hl.make_video(frames, mp4, hl.FPS)
        hl.log(f"  video: {mp4} ({mp4.stat().st_size / 1e6:.1f} MB, f000-f{int(frames[-1].stem[-3:]):03d})")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--init", help="run to compare, e.g. 2026-11-12T12 (default: runs from the "
                    f"last {LOOKBACK_H} h that have a loop folder)")
    ap.add_argument("--fxx", type=int, nargs="+", help="only these hours (no video)")
    ap.add_argument("--force", action="store_true", help="remake frames already made")
    a = ap.parse_args()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if a.init:
        runs = [datetime.strptime(a.init.replace("Z", ""), "%Y-%m-%dT%H")]
    else:
        runs = []
        for d in sorted(hl.OUT_ROOT.glob("*_[0-9][0-9]z")):
            try:
                init = datetime.strptime(d.name, "%Y%m%d_%Hz")
            except ValueError:
                continue
            if now - timedelta(hours=LOOKBACK_H) <= init <= now:
                runs.append(init)
    ok = True
    for init in runs:
        ok &= process(init, now, only_fxx=a.fxx, force=a.force)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
