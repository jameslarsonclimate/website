"""
Convection-allowing (3 km) precipitation ensembles for the WxChallenge day (06Z-06Z):

HRRRCAST  NOAA GSL's HRRRCast, an AI emulator of the HRRR (experimental). 18 diffusion
          members; the 00/06/12/18Z cycles run to 48 h. Public on AWS:
            noaa-gsl-experimental-pds/HRRRCast/YYYYMMDD/HH/hrrrcast.mNN.tHHz.pgrb2.fFF
          APCP in each file is the precip of the hour ending at that step, so a member's day
          total is the sum of 24 fields (~2.5 MB each: ~1.1 GB per cycle). Only the APCP
          message is downloaded (byte ranges from the .idx files), the station's value is
          kept, and the values are stored locally so a cycle is only ever downloaded once.
          Timing: the 06Z cycle is complete ~12:40Z, the 12Z cycle ~20:00Z, the 18Z cycle
          only after the 00Z deadline.

REFS      NOAA's Rapid Refresh Ensemble Forecast System (operational 14 Oct 2026; replaces
          HREF). Its 14 members are rebuilt here from the member output, the same way REFS
          builds them: RRFS deterministic + RRFS ensemble m001-m005 + HRRR, each from the
          newest cycle and the one 6 h older. The 0-N h accumulated precip field at the start
          and end of the day is all that's needed (a few MB in total). REFS' own "prob" files
          hold neighbourhood (area) probabilities, not the point probabilities used here.
          RRFS on NOMADS: rrfs/prod (from 14 Oct) or rrfs/para (parallel); HRRR from AWS.

Both are precipitation only (the model's value is the member MEDIAN, which minimises the
expected WxChallenge precip error points), with no highs/lows/winds, so they are left out
of the consensus and of the scoring (which need all four values).
"""

import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import numpy as np

import wxc_cache
import wxc_pop
import wxc_site

MODELS = {"HRRRCAST": "HRRRCast", "REFS": "REFS"}     # our key -> display name
PRECIP_THRESHOLDS = [0.01, 0.10, 0.25, 0.50]
PCTS = [0, 10, 25, 50, 75, 90, 100]
MM_TO_IN = 1 / 25.4
MAX_DIST_KM = 5.0          # nearest grid point must be this close (else: outside the grid)

HRRRCAST_ENABLED = True    # set False to skip the ~1.1 GB-per-cycle download
HRRRCAST_URL = ("https://noaa-gsl-experimental-pds.s3.amazonaws.com/HRRRCast/"
                "{init:%Y%m%d}/{init:%H}/hrrrcast.{mem}.t{init:%H}z.pgrb2.f{fh:02d}")
HRRRCAST_MEMBERS = [f"m{i:02d}" for i in range(18)]
HRRRCAST_MAX_FH = 48
HRRRCAST_WORKERS = 12

NOMADS_RRFS = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/rrfs/{stage}"
RRFS_STAGES = ("prod", "para")      # prod from 14 Oct 2026; para until then
RRFS_DET = NOMADS_RRFS + "/rrfs.{init:%Y%m%d}/{init:%H}/rrfs.t{init:%H}z.2dfld.{res}.f{fh:03d}.{dom}.grib2"
RRFS_ENS = (NOMADS_RRFS + "/rrfsens.{init:%Y%m%d}/{init:%H}/{mem}/"
            "rrfs.t{init:%H}z.{mem}.2dfldnomads.{res}.f{fh:03d}.{dom}.grib2")
RRFS_ENS_MEMBERS = [f"m{i:03d}" for i in range(1, 6)]
HRRR_AWS = ("https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.{init:%Y%m%d}/{sub}/"
            "hrrr.t{init:%H}z.wrfsfcf{fh:02d}{suffix}.grib2")
MAX_FH = {"RRFS": 84, "RRFSENS": 60, "HRRR": 48}
REFS_WORKERS = 4           # NOMADS blocks clients that hit it too fast

_ECCODES_LOCK = threading.Lock()

# idx descriptors
ACC_FROM_INIT = re.compile(r":APCP:surface:0-(\d+) (hour|day) acc")
HOURLY_APCP = re.compile(r":APCP:surface:(\d+) hour fcst:|:APCP:surface:(\d+)-(\d+) hour acc")


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
def window(day: date):
    """The forecast day (06Z-06Z, or the WXC_SITE's local day) as aware UTC times."""
    return (wxc_site.day_start(day).replace(tzinfo=timezone.utc),
            wxc_site.day_end(day).replace(tzinfo=timezone.utc))


def leads(init: datetime, day: date):
    """Forecast hours of the start and end of the forecast day for a run."""
    start, end = window(day)
    s = int((start - init).total_seconds() // 3600)
    return s, s + int((end - start).total_seconds() // 3600)


def candidate_inits(day: date, now: datetime, max_fh: int, every: int = 6) -> list:
    """Cycles (newest first) that cover the whole day within max_fh and have started by now."""
    start, end = window(day)
    newest = now.replace(minute=0, second=0, microsecond=0)
    newest -= timedelta(hours=newest.hour % every)
    newest = min(newest, start)
    out, t = [], newest
    while t >= end - timedelta(hours=max_fh):
        out.append(t)
        t -= timedelta(hours=every)
    return out


def acc_hours(line: str) -> Optional[int]:
    """'...:APCP:surface:0-2 day acc fcst:' -> 48; None if not an accumulation from init."""
    m = ACC_FROM_INIT.search(line)
    if not m:
        return None
    return int(m.group(1)) * (24 if m.group(2) == "day" else 1)


def parse_idx(text: str) -> list:
    """wgrib2 inventory -> [(start byte, end byte or None, line)]."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    rows = []
    for i, ln in enumerate(lines):
        start = int(ln.split(":")[1])
        end = int(lines[i + 1].split(":")[1]) - 1 if i + 1 < len(lines) else None
        rows.append((start, end, ln))
    return rows


def ens_stats(values: list) -> dict:
    a = np.array(values, float)
    st = {"precip_in": {"mean": round(float(a.mean()), 3), "std": round(float(a.std()), 3),
                        **{f"p{q}": round(float(np.percentile(a, q)), 3) for q in PCTS}}}
    st["precip_prob"] = {f"{th:.2f}": round(float((a >= th - 1e-9).mean()), 3) for th in PRECIP_THRESHOLDS}
    return st


def _fail(msg, init=None):
    return {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
            "init_time_utc": init.strftime("%Y-%m-%dT%H") if init else None,
            "valid_range_utc": None, "precip_only": True, "error": msg}


def _result(label, init, day, names, values, note, blocks=None):
    """blocks: {member name: [precip in each 6-h block]} when the source has sub-daily values."""
    start, end = window(day)
    st = ens_stats(values)
    per_block = None
    if blocks:
        have = [n for n in names if n in blocks]
        per_block = {b: [blocks[n][i] for n in have] for i, b in enumerate(wxc_pop.BLOCK_LABELS)}
    return {
        "tmax_f": None, "tmin_f": None, "wind_max_kt": None,
        # median: the value that minimises the expected WxChallenge precip error points
        "precip_in": round(st["precip_in"]["p50"], 2),
        "precip_mean_in": round(st["precip_in"]["mean"], 2),
        "init_time_utc": init.strftime("%Y-%m-%dT%H"),
        "valid_range_utc": [start.strftime("%Y-%m-%dT%H"), end.strftime("%Y-%m-%dT%H")],
        "note": note, "precip_only": True,
        "pop": wxc_pop.from_members(list(values), per_block),
        "ensemble": {"n_members": len(values), "stats": st, "member_names": names,
                     "members": {"precip_in": [round(float(v), 3) for v in values]}},
    }


# ----------------------------------------------------------------------------
# point values from remote GRIB2 (byte ranges from the .idx inventory)
# ----------------------------------------------------------------------------
class PointReader:
    """Downloads single GRIB messages and keeps only the value at one point.
    Values are stored in `store_path`, so an interrupted or repeated run never downloads
    the same message twice."""

    def __init__(self, lat, lon, store_path: Optional[Path] = None):
        self.lat, self.lon = lat, lon
        self.store_path = store_path
        self.store = {}
        if store_path and store_path.exists():
            try:
                self.store = json.loads(store_path.read_text())
            except json.JSONDecodeError:
                self.store = {}
        self._idx, self._near = {}, {}
        self._lock = threading.Lock()
        self._local = threading.local()
        self.bytes = 0

    def _session(self):
        s = getattr(self._local, "s", None)
        if s is None:
            import requests
            s = self._local.s = requests.Session()
            s.headers["User-Agent"] = "wxchallenge-forecast (CSU)"
        return s

    def get(self, url, headers=None, timeout=60):
        import requests
        last = None
        for _ in range(3):
            try:
                r = self._session().get(url, headers=headers, timeout=timeout)
                if r.status_code == 404:
                    raise FileNotFoundError(url)
                r.raise_for_status()
                return r
            except FileNotFoundError:
                raise
            except requests.RequestException as exc:
                last = exc
        raise last

    def idx(self, url) -> list:
        if url not in self._idx:
            self._idx[url] = parse_idx(self.get(url + ".idx", timeout=30).text)
        return self._idx[url]

    def exists(self, url) -> bool:
        try:
            self.idx(url)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def line(self, url, pattern) -> str:
        for _, _, ln in self.idx(url):
            if re.search(pattern, ln):
                return ln
        raise KeyError(f"{pattern} not in {url}.idx")

    def value(self, url, pattern) -> float:
        """Value at the point of the first message matching `pattern` (regex on the idx line)."""
        key = f"{url}|{pattern}"
        if key in self.store:
            v = self.store[key]
            return np.nan if v is None else v
        for start, end, ln in self.idx(url):
            if re.search(pattern, ln):
                break
        else:
            raise KeyError(f"{pattern} not in {url}.idx")
        rng = f"bytes={start}-{'' if end is None else end}"
        data = self.get(url, headers={"Range": rng}).content
        v = self.decode(data)
        with self._lock:
            self.bytes += len(data)
            self.store[key] = None if not np.isfinite(v) else float(v)
        return v

    def decode(self, data: bytes) -> float:
        with _ECCODES_LOCK:          # downloads run in parallel, decoding one at a time
            return self._decode(data)

    def _decode(self, data: bytes) -> float:
        import eccodes
        gid = eccodes.codes_new_from_message(data)
        try:
            key = tuple(eccodes.codes_get(gid, k) for k in (
                "gridType", "numberOfDataPoints",
                "latitudeOfFirstGridPointInDegrees", "longitudeOfFirstGridPointInDegrees"))
            with self._lock:
                near = self._near.get(key)
            if near is None:
                n = eccodes.codes_grib_find_nearest(gid, self.lat, self.lon)[0]
                if n["distance"] > MAX_DIST_KM:
                    raise ValueError(f"station is {n['distance']:.0f} km from the nearest grid "
                                     "point (outside this model's domain)")
                near = int(n["index"])
                with self._lock:
                    self._near[key] = near
            v = float(eccodes.codes_get_values(gid)[near])
            if eccodes.codes_get(gid, "bitmapPresent") and v == eccodes.codes_get(gid, "missingValue"):
                v = np.nan
            return v
        finally:
            eccodes.codes_release(gid)

    def save(self):
        if not self.store_path:
            return
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.store_path.with_suffix(".tmp")
        with self._lock:
            tmp.write_text(json.dumps(self.store))
        tmp.replace(self.store_path)


def _store_path(station, label, init):
    return wxc_cache.CACHE_DIR / station.icao.upper() / f"_points_{label}_{init:%Y%m%d%H}.json"


# ----------------------------------------------------------------------------
# HRRRCast
# ----------------------------------------------------------------------------
def _hrrrcast_url(init, mem, fh):
    return HRRRCAST_URL.format(init=init, mem=mem, fh=fh)


def pick_hrrrcast_cycle(reader: PointReader, day: date, now: datetime):
    """Newest 6-hourly cycle whose members all reach the end of the day (a cycle that is
    older than 12 h is accepted with at least 12 members)."""
    for init in candidate_inits(day, now, HRRRCAST_MAX_FH):
        s, e = leads(init, day)
        if s < 0 or not reader.exists(_hrrrcast_url(init, "m00", e)):
            continue
        have = [m for m in HRRRCAST_MEMBERS if reader.exists(_hrrrcast_url(init, m, e))]
        if len(have) == len(HRRRCAST_MEMBERS) or (len(have) >= 12 and now - init > timedelta(hours=12)):
            return init, have
    return None, []


def hrrrcast_precip(reader: PointReader, init: datetime, day: date, members: list, blocks=None):
    """Per-member 06Z-06Z precip (inches). Handles hourly APCP (current HRRRCast output)
    and, should the output change, APCP accumulated from the start of the run. With hourly
    APCP, `blocks` (a dict, if given) is filled with each member's 6-h block totals (PoP)."""
    s, e = leads(init, day)
    lines = [ln for _, _, ln in reader.idx(_hrrrcast_url(init, members[0], e)) if ":APCP:" in ln]
    if not lines:
        raise KeyError("no APCP in HRRRCast output")
    acc_mode = any(acc_hours(ln) == e for ln in lines)
    if acc_mode:                                        # accumulated from the start of the run
        jobs = [(m, fh, ACC_FROM_INIT.pattern) for m in members for fh in ([s, e] if s > 0 else [e])]
    else:                                               # the hour ending at each step
        # PoP blocks are the UTC 6-h periods 06Z D - 06Z D+1 (wxc_pop), which a local day
        # (e.g. CDT 05Z-05Z) doesn't quite match: fetch the union of both
        b0 = int((wxc_pop.block_windows(day)[0][1].replace(tzinfo=timezone.utc) - init).total_seconds() // 3600)
        lo, hi = (min(s, b0), max(e, b0 + 24)) if blocks is not None else (s, e)
        jobs = [(m, fh, HOURLY_APCP.pattern) for m in members for fh in range(max(lo, 0) + 1, hi + 1)]
    vals, errors = {}, {}
    with ThreadPoolExecutor(HRRRCAST_WORKERS) as ex:
        futs = {ex.submit(reader.value, _hrrrcast_url(init, m, fh), pat): (m, fh) for m, fh, pat in jobs}
        for f in as_completed(futs):
            m, fh = futs[f]
            try:
                vals[(m, fh)] = f.result()
            except Exception as exc:
                errors[m] = f"f{fh:02d}: {type(exc).__name__}: {exc}"
    reader.save()
    out = {}
    for m in members:
        if m in errors:
            continue
        if acc_mode:
            total = vals[(m, e)] - (vals[(m, s)] if s > 0 else 0.0)
        else:
            total = sum(vals[(m, fh)] for fh in range(s + 1, e + 1))
            if blocks is not None:
                blocks[m] = [max(sum(vals[(m, fh)] for fh in range(a + 1, a + 7)), 0.0) * MM_TO_IN
                             for a in range(b0, b0 + 24, 6)]
        if np.isfinite(total):
            out[m] = max(total, 0.0) * MM_TO_IN
    return out, errors


def get_hrrrcast(station, day: date, now: datetime) -> dict:
    if not HRRRCAST_ENABLED:
        return _fail("disabled (wxc_cam_ens.HRRRCAST_ENABLED)")
    if station.hrrr_model != "hrrr":
        return _fail("HRRRCast covers the CONUS HRRR domain only")
    reader = PointReader(station.lat, station.lon)
    init, members = pick_hrrrcast_cycle(reader, day, now)
    if init is None:
        return _fail("no complete 00/06/12/18Z HRRRCast cycle covering the day yet")
    hit = wxc_cache.load(station.icao, "HRRRCAST", init, day)
    if hit is not None:
        print(f"  {'HRRRCAST':8s} {init:%Y-%m-%d %HZ}: using saved run")
        return hit
    reader.store_path = _store_path(station, "HRRRCAST", init)
    if reader.store_path.exists():
        reader.store = json.loads(reader.store_path.read_text())
    print(f"  HRRRCAST {init:%Y-%m-%d %HZ}: {len(members)} members, downloading precip "
          f"(~{2.5 * 24 * len(members) / 1000:.1f} GB the first time)...")
    blocks = {}
    vals, errors = hrrrcast_precip(reader, init, day, members, blocks)
    if reader.bytes:
        print(f"    downloaded {reader.bytes / 1e9:.2f} GB")
    if len(vals) < 5:
        return _fail(f"only {len(vals)} HRRRCast members: " + "; ".join(f"{k} {v}" for k, v in errors.items())[:300], init)
    names = sorted(vals)
    note = f"median of {len(vals)} members"
    if errors:
        note += f"; {len(errors)} member(s) failed"
    res = _result("HRRRCAST", init, day, names, [vals[m] for m in names], note, blocks)
    if len(vals) == len(HRRRCAST_MEMBERS):
        wxc_cache.save(station.icao, "HRRRCAST", init, day, res)
    return res


# ----------------------------------------------------------------------------
# REFS (rebuilt from RRFS deterministic + RRFS ensemble + HRRR, two cycles)
# ----------------------------------------------------------------------------
def _res_dom(station):
    dom = station.rrfs_domain
    return ("2p5km" if dom in ("hi", "pr") else "3km"), dom


def refs_members(station, init: datetime, stage: str, day: date) -> list:
    """(name, url at end hour, url at start hour or None) for one cycle's REFS members."""
    res, dom = _res_dom(station)
    s, e = leads(init, day)
    out = []
    kw = dict(stage=stage, init=init, res=res, dom=dom)
    tag = f"{init:%H}Z"
    if e <= MAX_FH["RRFS"]:
        out.append((f"RRFS {tag}", RRFS_DET.format(fh=e, **kw), RRFS_DET.format(fh=s, **kw) if s > 0 else None))
    if e <= MAX_FH["RRFSENS"]:
        for m in RRFS_ENS_MEMBERS:
            out.append((f"RRFS {m} {tag}", RRFS_ENS.format(mem=m, fh=e, **kw),
                        RRFS_ENS.format(mem=m, fh=s, **kw) if s > 0 else None))
    if station.hrrr_model in ("hrrr", "hrrrak") and e <= MAX_FH["HRRR"]:
        sub, suffix = ("conus", "") if station.hrrr_model == "hrrr" else ("alaska", ".ak")
        hk = dict(init=init, sub=sub, suffix=suffix)
        out.append((f"HRRR {tag}", HRRR_AWS.format(fh=e, **hk), HRRR_AWS.format(fh=s, **hk) if s > 0 else None))
    return out


def pick_refs_cycle(reader: PointReader, station, day: date, now: datetime):
    """Newest cycle whose RRFS ensemble has reached the end of the day (>= 3 members)."""
    res, dom = _res_dom(station)
    for init in candidate_inits(day, now, MAX_FH["RRFSENS"]):
        s, e = leads(init, day)
        if s < 0:
            continue
        for stage in RRFS_STAGES:
            urls = [RRFS_ENS.format(stage=stage, init=init, mem=m, fh=e, res=res, dom=dom)
                    for m in RRFS_ENS_MEMBERS]
            if sum(reader.exists(u) for u in urls) >= 3:
                return init, stage
    return None, None


def refs_precip(reader: PointReader, members: list):
    def one(name, url_e, url_s):
        ln = reader.line(url_e, ACC_FROM_INIT.pattern)
        v_e = reader.value(url_e, ACC_FROM_INIT.pattern)
        v_s = reader.value(url_s, ACC_FROM_INIT.pattern) if url_s else 0.0
        return max(v_e - v_s, 0.0) * MM_TO_IN, ln

    vals, errors = {}, {}
    with ThreadPoolExecutor(REFS_WORKERS) as ex:
        futs = {ex.submit(one, *m): m[0] for m in members}
        for f in as_completed(futs):
            name = futs[f]
            try:
                v, _ = f.result()
                if np.isfinite(v):
                    vals[name] = v
            except FileNotFoundError:
                errors[name] = "not posted"
            except Exception as exc:
                errors[name] = f"{type(exc).__name__}: {exc}"
    reader.save()
    return vals, errors


def get_refs(station, day: date, now: datetime) -> dict:
    if not station.rrfs_domain:
        return _fail("station outside the RRFS domains")
    reader = PointReader(station.lat, station.lon)
    init, stage = pick_refs_cycle(reader, station, day, now)
    if init is None:
        return _fail("no RRFS ensemble cycle covering the day found on NOMADS (prod or para)")
    hit = wxc_cache.load(station.icao, "REFS", init, day)
    if hit is not None:
        print(f"  {'REFS':8s} {init:%Y-%m-%d %HZ}: using saved run")
        return hit
    reader.store_path = _store_path(station, "REFS", init)
    if reader.store_path.exists():
        reader.store = json.loads(reader.store_path.read_text())
    lag = init - timedelta(hours=6)
    members = refs_members(station, init, stage, day) + refs_members(station, lag, stage, day)
    vals, errors = refs_precip(reader, members)
    if len(vals) < 6:
        return _fail(f"only {len(vals)} REFS members: " + "; ".join(f"{k} {v}" for k, v in errors.items())[:300], init)
    names = [n for n, _, _ in members if n in vals]
    note = f"median of {len(vals)} members"
    if errors:
        note += "; missing: " + ", ".join(sorted(errors))
    res = _result("REFS", init, day, names, [vals[n] for n in names], note)
    if not errors:
        wxc_cache.save(station.icao, "REFS", init, day, res)
    return res


# ----------------------------------------------------------------------------
def get_cam_ensembles(station, day: date, now: Optional[datetime] = None, only=None) -> dict:
    """HRRRCast and REFS precip for the target day (live runs only; no hindcasts)."""
    now = now or datetime.now(timezone.utc)
    out = {}
    for label, fn in (("REFS", get_refs), ("HRRRCAST", get_hrrrcast)):
        if only is not None and label not in only:
            continue
        try:
            out[label] = fn(station, day, now)
        except Exception as exc:
            out[label] = _fail(f"{type(exc).__name__}: {exc}")
        r = out[label]
        if r.get("error"):
            print(f"  {label:8s} {r.get('init_time_utc')}: {r['error']}")
        else:
            st = r["ensemble"]["stats"]
            print(f"  {label:8s} {r['init_time_utc']}: median {r['precip_in']:.2f}in "
                  f"(mean {r['precip_mean_in']:.2f}), P(>=0.01\")={st['precip_prob']['0.01']:.0%}, "
                  f"{r['ensemble']['n_members']} members")
    # label order as in MODELS
    return {k: out[k] for k in MODELS if k in out}
