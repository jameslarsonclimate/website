"""
Satellite cloud fraction near the station from the GOES ABI L2 Clear Sky Mask (ACM),
for the "today so far" figure. DISPLAY ONLY (see wxc_clouds.py).

  satellite  per station (wxc_stations: GOES-19 East or GOES-18 West)
  product    ABI-L2-ACMC (CONUS / PACUS sector, every 5 min) for lower-48 stations,
             ABI-L2-ACMF (full disk, every 10 min) for Alaska, Hawaii, ...
  value      % of pixels with BCM == 1 (cloudy or probably cloudy) among the good-quality
             pixels within RADIUS_KM of the station, from the scan nearest the top of the hour

Files come from the public NOAA buckets on AWS (anonymous HTTPS) and are read in memory
(~4 MB CONUS, ~24 MB full disk). netCDF's "#mode=bytes" range access was tried: it moved
nearly the whole file anyway (4.2 of 4.2 MB CONUS, 17 of 24 MB full disk) and was slower
than one plain download, so it is not used. Each hour's value is saved as cache/{ICAO}/_goes_acm_{YYYYMMDDHH}.json, so an hour is only
read once, and old files are pruned with the rest of the cache (wxc_cache.prune).

Caveat: at night the mask has no visible channels and relies on infrared tests, which
often miss low stratus and fog (cloud top about as warm as the ground), so night values
can read too clear exactly when ASOS reports a low overcast.
"""

import json
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import Optional

import numpy as np

import wxc_cache
from wxc_stations import GOES_SATELLITES

S3 = "https://{bucket}.s3.amazonaws.com"
PRODUCTS = {"C": "ABI-L2-ACMC", "F": "ABI-L2-ACMF"}
RADIUS_KM = 15.0
MIN_PIXELS = 5
# DQF: 0 good, 1 bad, 2 space, 6 degraded (e.g. high view angle, terminator). Bad and
# space pixels are skipped; degraded ones still carry a usable mask.
USABLE_DQF = (0, 6)
_RE_START = re.compile(r"_s(\d{4})(\d{3})(\d{2})(\d{2})(\d{2})\d_")


# ----------------------------------------------------------------------------
# fixed-grid navigation (GOES-R PUG vol. 3, section 4.2.8)
# ----------------------------------------------------------------------------
def _geometry(proj: dict):
    r_eq = float(proj["semi_major_axis"])
    r_pol = float(proj["semi_minor_axis"])
    h = float(proj["perspective_point_height"]) + r_eq
    lon0 = np.radians(float(proj["longitude_of_projection_origin"]))
    return r_eq, r_pol, h, lon0


def latlon_to_xy(lat, lon, proj: dict):
    """Geodetic lat/lon (deg) -> ABI fixed-grid scan angles x, y (rad). NaN where the
    point is not visible from the satellite."""
    r_eq, r_pol, h, lon0 = _geometry(proj)
    phi, lam = np.radians(lat), np.radians(lon)
    phi_c = np.arctan((r_pol ** 2 / r_eq ** 2) * np.tan(phi))
    e2 = (r_eq ** 2 - r_pol ** 2) / r_eq ** 2
    r_c = r_pol / np.sqrt(1 - e2 * np.cos(phi_c) ** 2)
    s_x = h - r_c * np.cos(phi_c) * np.cos(lam - lon0)
    s_y = -r_c * np.cos(phi_c) * np.sin(lam - lon0)
    s_z = r_c * np.sin(phi_c)
    visible = h * (h - s_x) >= s_y ** 2 + (r_eq ** 2 / r_pol ** 2) * s_z ** 2
    y = np.arctan(s_z / s_x)
    x = np.arcsin(-s_y / np.sqrt(s_x ** 2 + s_y ** 2 + s_z ** 2))
    return np.where(visible, x, np.nan), np.where(visible, y, np.nan)


def xy_to_latlon(x, y, proj: dict):
    """ABI fixed-grid scan angles (rad) -> geodetic lat/lon (deg); NaN off the Earth."""
    r_eq, r_pol, h, lon0 = _geometry(proj)
    x, y = np.asarray(x, float), np.asarray(y, float)
    a = np.sin(x) ** 2 + np.cos(x) ** 2 * (np.cos(y) ** 2 + (r_eq ** 2 / r_pol ** 2) * np.sin(y) ** 2)
    b = -2 * h * np.cos(x) * np.cos(y)
    c = h ** 2 - r_eq ** 2
    disc = b ** 2 - 4 * a * c
    with np.errstate(invalid="ignore"):
        r_s = (-b - np.sqrt(disc)) / (2 * a)
    s_x = r_s * np.cos(x) * np.cos(y)
    s_y = -r_s * np.sin(x)
    s_z = r_s * np.cos(x) * np.sin(y)
    lat = np.degrees(np.arctan((r_eq ** 2 / r_pol ** 2) * s_z / np.sqrt((h - s_x) ** 2 + s_y ** 2)))
    lon = np.degrees(lon0 - np.arctan(s_y / (h - s_x)))
    return lat, lon


def _km(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = p2 - p1, np.radians(np.asarray(lon2) - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(a))


def station_window(x, y, proj: dict, lat: float, lon: float, radius_km: float = RADIUS_KM):
    """(y, x) index slices of a box around the station that holds the radius_km circle.
    x, y: the file's 1-D scan-angle coordinates (rad)."""
    xs, ys = latlon_to_xy(lat, lon, proj)
    if not (np.isfinite(xs) and np.nanmin(x) <= xs <= np.nanmax(x) and np.nanmin(y) <= ys <= np.nanmax(y)):
        raise ValueError(f"station ({lat:.2f}, {lon:.2f}) is outside this ABI sector")
    ix, iy = int(np.argmin(np.abs(x - xs))), int(np.argmin(np.abs(y - ys)))
    nadir_km = abs(x[1] - x[0]) * float(proj["perspective_point_height"]) / 1000.0
    n = int(np.ceil(radius_km / nadir_km)) + 2              # pixels only grow away from nadir
    return slice(max(iy - n, 0), iy + n + 1), slice(max(ix - n, 0), ix + n + 1)


def fraction_near(x, y, bcm, dqf, proj: dict, lat: float, lon: float, radius_km: float = RADIUS_KM):
    """% cloudy (BCM == 1) among usable pixels within radius_km of lat/lon.
    bcm, dqf: 2-D (y, x) arrays. Returns (percent or None, number of pixels used)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    sy, sx = station_window(x, y, proj, lat, lon, radius_km)
    return _count(x[sx], y[sy], np.asarray(bcm)[sy, sx], np.asarray(dqf)[sy, sx], proj, lat, lon, radius_km)


def _count(xw, yw, bcm, dqf, proj, lat, lon, radius_km):
    xx, yy = np.meshgrid(xw, yw)
    plat, plon = xy_to_latlon(xx, yy, proj)
    with np.errstate(invalid="ignore"):
        near = _km(lat, lon, plat, plon) <= radius_km
    ok = near & np.isin(dqf, USABLE_DQF) & np.isin(bcm, (0, 1))
    n = int(ok.sum())
    if n < MIN_PIXELS:
        return None, n
    return round(100.0 * float((bcm[ok] == 1).mean()), 1), n


# ----------------------------------------------------------------------------
# AWS access
# ----------------------------------------------------------------------------
def list_keys(bucket: str, prefix: str) -> list:
    """Object keys under a prefix (anonymous S3 ListObjectsV2 over HTTPS)."""
    import requests
    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    keys, token = [], None
    while True:
        params = {"list-type": 2, "prefix": prefix}
        if token:
            params["continuation-token"] = token
        r = requests.get(S3.format(bucket=bucket), params=params, timeout=30)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        keys += [k.text for k in root.findall("s3:Contents/s3:Key", ns)]
        token = root.findtext("s3:NextContinuationToken", namespaces=ns)
        if not token:
            return keys


def scan_start(key: str) -> Optional[datetime]:
    m = _RE_START.search(key)
    if not m:
        return None
    y, j, hh, mm, ss = map(int, m.groups())
    return datetime(y, 1, 1, hh, mm, ss, tzinfo=timezone.utc) + timedelta(days=j - 1)


def nearest_scan(keys: list, t: datetime) -> Optional[str]:
    """The scan starting nearest the top of the hour `t` (CONUS scans start at xx:01,
    full disk at xx:00, so the hour's own folder holds it)."""
    timed = [(abs((scan_start(k) - t).total_seconds()), k) for k in keys if scan_start(k)]
    return min(timed)[1] if timed else None


def read_scan(url: str, lat: float, lon: float) -> dict:
    """Cloud fraction near lat/lon from one ACM file."""
    import netCDF4
    import requests
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    ds = netCDF4.Dataset("acm.nc", memory=r.content)
    try:
        pv = ds["goes_imager_projection"]
        proj = {k: pv.getncattr(k) for k in pv.ncattrs()}
        x, y = np.asarray(ds["x"][:], float), np.asarray(ds["y"][:], float)
        sy, sx = station_window(x, y, proj, lat, lon)
        bcm = np.ma.filled(ds["BCM"][sy, sx], 255)
        dqf = np.ma.filled(ds["DQF"][sy, sx], 255)
        pct, npix = _count(x[sx], y[sy], bcm, dqf, proj, lat, lon, RADIUS_KM)
    finally:
        ds.close()
    return {"cloud_pct": pct, "n_pixels": npix, "bytes": len(r.content)}


# ----------------------------------------------------------------------------
# hourly values for the today-so-far figure
# ----------------------------------------------------------------------------
def _cache_path(icao: str, t: datetime):
    return wxc_cache.CACHE_DIR / icao.upper() / f"_goes_acm_{t:%Y%m%d%H}.json"


def hour_value(station, t: datetime, stats: dict) -> Optional[dict]:
    """Cloud fraction for the hour starting at `t` (cached), or None if no scan is posted."""
    p = _cache_path(station.icao, t)
    if wxc_cache.ENABLED:
        try:
            return json.loads(p.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    bucket = GOES_SATELLITES[station.goes][0]
    product = PRODUCTS[station.goes_sector]
    keys = list_keys(bucket, f"{product}/{t:%Y}/{t:%j}/{t:%H}/")
    stats["listings"] += 1
    key = nearest_scan(keys, t)
    if key is None:
        return None
    res = read_scan(f"{S3.format(bucket=bucket)}/{key}", station.lat, station.lon)
    stats["scans"] += 1
    stats["bytes"] += res["bytes"]
    rec = {"hour": t.strftime("%Y-%m-%dT%H:%M"), "scan_start": scan_start(key).strftime("%Y-%m-%dT%H:%M:%S"),
           "satellite": station.goes, "product": product, "file": key.rsplit("/", 1)[-1], **res}
    if wxc_cache.ENABLED:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rec))
    return rec


def hourly_cloud(station, start: datetime, now: datetime) -> list:
    """GOES cloud fraction for each hour from `start` through `now` (oldest first)."""
    if not station.goes:
        print("  GOES: no geostationary coverage for this station; skipped")
        return []
    t0 = time.time()
    stats = {"listings": 0, "scans": 0, "bytes": 0}
    t = start.replace(minute=0, second=0, microsecond=0)
    out, failures = [], 0
    while t <= now:
        try:
            rec = hour_value(station, t, stats)
            if rec is not None and rec.get("cloud_pct") is not None:
                out.append(rec)
            failures = 0
        except ValueError:
            raise                               # outside the sector: every hour would fail
        except Exception as exc:
            failures += 1
            print(f"  warning: GOES {t:%H}Z failed ({type(exc).__name__}: {exc})")
            if failures >= 3:
                print("  warning: GOES giving up for this run")
                break
        t += timedelta(hours=1)
    print(f"  GOES-{station.goes[1:]} {PRODUCTS[station.goes_sector]}: {len(out)} hourly values, "
          f"{stats['scans']} new scan(s) ({stats['bytes'] / 1e6:.1f} MB downloaded), "
          f"{stats['listings']} listing(s), {time.time() - t0:.1f} s")
    return out
