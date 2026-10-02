"""
NBM QMD (quantile mapping) probabilistic precipitation: calibrated PoP and precip percentiles
for the WxChallenge day (06Z-06Z). DISPLAY / PoP VERIFICATION ONLY: precip only, so it is left
out of the consensus and the scoring (both need all four values). Live runs only (no hindcasts).

Files (AWS, 00/06/12/18Z; the CONUS file of one hour is ~450 MB, so only single messages are
read, by byte range from the .idx, keeping the value at the station):
  noaa-nbm-grib2-pds/blend.YYYYMMDD/HH/qmd/blend.tHHz.qmd.fFFF.{co|ak|hi|pr}.grib2

Every cycle has APCP windows ending every 6 h (checked 2026-10-02 in the idx files), including a
24-h window that ends at 06Z: e.g. the 12Z run's f042 holds "APCP:surface:18-42 hour acc fcst"
(06Z-06Z), the 06Z run's f048 "1-2 day acc". Per window:
  "prob >0.254"       chance of > 0.254 mm (0.01")   -> PoP
  "<q>% level"        unconditional percentiles (mm; dry members included, so the 50% level is
                      the value minimising expected WxChallenge precip points)
Read per cycle (lean set, ~29 MB): the 24-h PoP, the four 6-h PoPs (one in each block's end-hour
file) and the 24-h 10/25/50/75/90% levels. Values are stored per cycle in
cache/{ICAO}/_points_NBM_QMD_{init}.json, so a cycle is downloaded once.
Posting: the 12Z cycle's qmd files arrive ~19:15Z, the 06Z ~13:15Z (18Z: after the deadline).
"""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from typing import Optional

import numpy as np

import wxc_cache
import wxc_cam_ens as cam
import wxc_pop

ENABLED = True             # False skips NBM QMD entirely
LABEL = "NBM_QMD"
URL = ("https://noaa-nbm-grib2-pds.s3.amazonaws.com/blend.{init:%Y%m%d}/{init:%H}/qmd/"
       "blend.t{init:%H}z.qmd.f{fh:03d}.{dom}.grib2")
DOMAINS = {"conus": "co", "ak": "ak", "hi": "hi", "pr": "pr"}   # Station.rrfs_domain -> NBM domain
PCTS = [10, 25, 50, 75, 90]
MAX_CYCLES = 4             # newest cycles tried (6-hourly)
WORKERS = 4
MM_TO_IN = 1 / 25.4


def window_desc(a: int, b: int) -> str:
    """Regex for the APCP window a-b hours (NBM writes whole days as "1-2 day")."""
    alts = [f"{a}-{b} hour"]
    if a % 24 == 0 and b % 24 == 0:
        alts.append(f"{a // 24}-{b // 24} day")
    return f"(?:{'|'.join(alts)}) acc fcst"


def pop_pattern(a: int, b: int) -> str:
    return rf":APCP:surface:{window_desc(a, b)}:prob >0\.254:"


def pct_pattern(a: int, b: int, q: int) -> str:
    # the real idx line ends at "level" (no trailing colon); "10% level" must not match "100% level"
    return rf":APCP:surface:{window_desc(a, b)}:{q}% level(?::|$)"


def jobs_for(init: datetime, day: date, dom: str) -> list:
    """(key, url, pattern) for every value read from one cycle."""
    s, e = cam.leads(init, day)
    url = lambda fh: URL.format(init=init, fh=fh, dom=dom)  # noqa: E731
    out = [("p24", url(e), pop_pattern(s, e))]
    out += [(f"q{q}", url(e), pct_pattern(s, e, q)) for q in PCTS]
    out += [(f"b:{lab}", url(s + 6 * (i + 1)), pop_pattern(s + 6 * i, s + 6 * (i + 1)))
            for i, lab in enumerate(wxc_pop.BLOCK_LABELS)]
    return out


def pick_cycle(reader, day: date, now: datetime, dom: str):
    """Newest 00/06/12/18Z cycle whose qmd files for the day's four block ends are posted and
    hold the 24-h window ending at 06Z."""
    for init in cam.candidate_inits(day, now, max_fh=264)[:MAX_CYCLES]:
        s, e = cam.leads(init, day)
        if s < 0:
            continue
        urls = [URL.format(init=init, fh=s + 6 * i, dom=dom) for i in (1, 2, 3, 4)]
        if all(reader.exists(u) for u in urls):
            try:
                reader.line(urls[-1], pop_pattern(s, e))
                return init
            except KeyError:
                continue
    return None


def summarize(vals: dict) -> dict:
    """Values read ({key: value}; probs in %, percentiles in mm) -> PoP record."""
    pct = lambda v: None if v is None or not np.isfinite(v) else min(max(v / 100.0, 0.0), 1.0)  # noqa: E731
    q = {str(p): round(max(vals[f"q{p}"], 0.0) * MM_TO_IN, 3) for p in PCTS
         if vals.get(f"q{p}") is not None and np.isfinite(vals[f"q{p}"])}
    blocks = {lab: pct(vals.get(f"b:{lab}")) for lab in wxc_pop.BLOCK_LABELS}
    return wxc_pop.record(pct(vals.get("p24")), blocks, basis="NBM QMD", q24_in=q or None)


def _fail(msg, init=None):
    return {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
            "init_time_utc": init.strftime("%Y-%m-%dT%H") if init else None,
            "valid_range_utc": None, "precip_only": True, "error": msg}


def get_qmd(station, day: date, now: Optional[datetime] = None) -> dict:
    """NBM QMD PoP + percentiles for the day from the newest posted cycle (live only)."""
    if not ENABLED:
        return _fail("disabled (wxc_nbm_qmd.ENABLED)")
    dom = DOMAINS.get(station.rrfs_domain or "")
    if not dom:
        return _fail("station outside the NBM domains")
    now = now or datetime.now(timezone.utc)
    reader = cam.PointReader(station.lat, station.lon)
    init = pick_cycle(reader, day, now, dom)
    if init is None:
        return _fail("no NBM QMD cycle covering the day is posted yet")
    hit = wxc_cache.load(station.icao, LABEL, init, day)
    if hit is not None:
        print(f"  {LABEL:8s} {init:%Y-%m-%d %HZ}: using saved run")
        return hit
    reader.store_path = cam._store_path(station, LABEL, init)
    if reader.store_path.exists():
        reader.store = json.loads(reader.store_path.read_text())
    vals, errors = {}, {}
    jobs = jobs_for(init, day, dom)
    with ThreadPoolExecutor(WORKERS) as ex:
        futs = {key: ex.submit(reader.value, url, pat) for key, url, pat in jobs}
        for key, f in futs.items():
            try:
                vals[key] = f.result()
            except Exception as exc:
                errors[key] = f"{type(exc).__name__}: {exc}"
    reader.save()
    if reader.bytes:
        print(f"    NBM QMD: downloaded {reader.bytes / 1e6:.0f} MB")
    pop = summarize(vals)
    if pop is None or pop["p24"] is None:
        return _fail("NBM QMD 24-h PoP unavailable: " + "; ".join(f"{k} {v}" for k, v in errors.items())[:300], init)
    start, end = cam.window(day)
    med = (pop.get("q24_in") or {}).get("50")
    note = "calibrated PoP and percentiles (NBM QMD); precip = 50% level"
    if errors:
        note += f"; {len(errors)} value(s) missing"
    res = {"tmax_f": None, "tmin_f": None, "wind_max_kt": None,
           "precip_in": None if med is None else round(med, 2),
           "init_time_utc": init.strftime("%Y-%m-%dT%H"),
           "valid_range_utc": [start.strftime("%Y-%m-%dT%H"), end.strftime("%Y-%m-%dT%H")],
           "note": note, "precip_only": True, "pop": pop}
    if not errors:
        wxc_cache.save(station.icao, LABEL, init, day, res)
    p, b = pop["p24"], pop["blocks"]
    print(f"  {LABEL:8s} {res['init_time_utc']}: PoP24 {p:.0%}, blocks "
          + " ".join("--" if b[k] is None else f"{b[k]:.0%}" for k in wxc_pop.BLOCK_LABELS)
          + (f", median {med:.2f}in" if med is not None else ""))
    return res
