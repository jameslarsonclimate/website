"""
NBM text guidance (NBS, NBH) straight from the NBM bucket on AWS, every hourly cycle.

    noaa-nbm-grib2-pds/blend.YYYYMMDD/HH/text/blend_{nbs|nbh}tx.tHHz

NBM runs every hour and each cycle writes its bulletins (one file per product, every station,
~30 MB). IEM's MOS API only keeps NBS from 00/06/12/18Z, so it was up to ~3 h behind.
  NBS  3-hourly rows to ~72 h (TXN, TMP, DPT, SKY/SSD, WSP, P06/Q06, ...)
  NBH  hourly rows for 25 h (TMP, DPT, SKY/SSD, WSP, P01/Q01, CIG, ...)
SSD is the sky cover's standard deviation (%), the spread the NBM 1D viewer shades.

Posting (measured on AWS 2026-10-21): most cycles' text is out ~40-55 min after the hour;
00/01/07/12/13/19Z take ~65-100 min (01/07/13/19Z are the runs with hourly output to f264).

Reading: a station's block is ~3 KB. Stations are mostly, but not strictly, in alphabetical
order, and a station sits at the same place in every cycle, so the byte offset where it was
found last time is saved (cache/{ICAO}/_nbmtext_{prod}_offset.json) and the next cycle reads
only a window around it by HTTP Range. The first time (or if it moved) the file is streamed
until the block is complete. Blocks are kept in cache/{ICAO}/_nbmtext_{prod}_{init}.txt, so a
cycle is read once.

parse_block() returns rows shaped like IEM's MOS API (runtime, ftime and lower-case element
columns), so wxc_mos.summarize_mos and wxc_clouds read them unchanged.
"""

import functools
import json
import re
from datetime import datetime, timezone
from typing import Optional

import pandas as pd

import wxc_cache

URL = ("https://noaa-nbm-grib2-pds.s3.amazonaws.com/blend.{init:%Y%m%d}/{init:%H}/text/"
       "blend_{prod}tx.t{init:%H}z")
PRODUCTS = ("nbs", "nbh")
SLOW_CYCLES = {0, 1, 7, 12, 13, 19}       # cycles whose text posts late (see above)
DELAY_H = {True: 1.7, False: 0.95}        # hours after the cycle until its text is safely out
HINT_PAD = 512 * 1024                     # bytes read either side of the remembered offset
BLOCK_MAX = 16 * 1024                     # ... plus room for the block itself (~3 KB)
STREAM_CHUNK = 1 << 20
TIMEOUT = 60

_HEADER = re.compile(r"^ ?(\S+)\s+NBM V\S+ (NB[A-Z]) GUIDANCE\s+(\d\d)/(\d\d)/(\d{4})\s+(\d\d)00 UTC", re.M)


class NotPosted(RuntimeError):
    """The cycle's file isn't on AWS (yet)."""


def url_for(prod: str, init) -> str:
    return URL.format(prod=prod, init=pd.Timestamp(init))


def posted_delay(hour: int) -> float:
    return DELAY_H[hour in SLOW_CYCLES]


def candidate_runtimes(as_of: datetime, n: int = 4) -> list:
    """The n newest cycles whose text should be out at `as_of` (newest first)."""
    t = pd.Timestamp(as_of)
    t = t.tz_convert("UTC") if t.tzinfo else t.tz_localize("UTC")
    c, out = t.floor("h"), []
    while len(out) < n:
        if c + pd.Timedelta(hours=posted_delay(c.hour)) <= t:
            out.append(c.to_pydatetime())
        c -= pd.Timedelta(hours=1)
    return out


# ----------------------------------------------------------------------------
# finding a station's block
# ----------------------------------------------------------------------------
def find_block(text: str, icao: str, complete: bool = True) -> tuple:
    """(block, start index) of station `icao` in `text`, or (None, None). With complete=False
    a block running to the end of `text` counts (the end of the file)."""
    icao = icao.upper()
    for m in _HEADER.finditer(text):
        if m.group(1) != icao:
            continue
        nxt = _HEADER.search(text, m.end())
        if nxt is None and complete:
            return None, None         # the block may go on past what was read
        return text[m.start():nxt.start() if nxt else len(text)].rstrip("\n") + "\n", m.start()
    return None, None


def _session():
    import requests
    return requests


def _read_window(url: str, offset: int, icao: str) -> Optional[tuple]:
    lo = max(0, offset - HINT_PAD)
    r = _session().get(url, headers={"Range": f"bytes={lo}-{offset + HINT_PAD + BLOCK_MAX}"}, timeout=TIMEOUT)
    if r.status_code in (403, 404):
        raise NotPosted(url)
    r.raise_for_status()
    text = r.content.decode("latin-1")          # one character per byte: indexes are offsets
    total = r.headers.get("Content-Range", "").rpartition("/")[2]
    eof = r.status_code == 200 or (total.isdigit() and lo + len(text) >= int(total))
    block, i = find_block(text, icao, complete=not eof)
    return None if block is None else (block, lo + i)


def _stream(url: str, icao: str) -> tuple:
    r = _session().get(url, stream=True, timeout=TIMEOUT)
    try:
        if r.status_code in (403, 404):
            raise NotPosted(url)
        r.raise_for_status()
        mine = re.compile(rf"^ ?{re.escape(icao.upper())}\s+NBM V", re.M)
        buf, base = "", 0
        for chunk in r.iter_content(STREAM_CHUNK):
            buf += chunk.decode("latin-1")
            block, i = find_block(buf, icao)
            if block is not None:
                return block, base + i
            # drop what's been searched, keeping the station's header if it has started
            # (its block isn't complete yet) and the last line (a header may be cut in two)
            m = mine.search(buf)
            cut = m.start() if m else buf.rfind("\n") + 1
            base += cut
            buf = buf[cut:]
        block, i = find_block(buf, icao, complete=False)
        if block is None:
            raise LookupError(f"{icao} not in {url}")
        return block, base + i
    finally:
        r.close()


def _hint_path(icao: str, prod: str):
    return wxc_cache.CACHE_DIR / icao.upper() / f"_nbmtext_{prod}_offset.json"


def _block_path(icao: str, prod: str, init):
    return wxc_cache.CACHE_DIR / icao.upper() / f"_nbmtext_{prod}_{pd.Timestamp(init):%Y%m%d%H}.txt"


@functools.lru_cache(maxsize=64)
def station_block(icao: str, prod: str, init) -> str:
    """Raw text block of one station from one cycle's bulletin. Raises NotPosted when the file
    isn't on AWS, LookupError when the station isn't in it."""
    init = pd.Timestamp(init)
    bp = _block_path(icao, prod, init)
    if wxc_cache.ENABLED and bp.exists():
        return bp.read_text()
    url = url_for(prod, init)
    hp = _hint_path(icao, prod)
    found = None
    try:
        found = _read_window(url, int(json.loads(hp.read_text())["offset"]), icao)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
        pass
    if found is None:
        found = _stream(url, icao)
    block, offset = found
    if wxc_cache.ENABLED:
        bp.parent.mkdir(parents=True, exist_ok=True)
        bp.write_text(block)
        hp.write_text(json.dumps({"offset": offset, "init": f"{init:%Y%m%d%H}"}))
    return block


# ----------------------------------------------------------------------------
# parsing
# ----------------------------------------------------------------------------
def _cells(line: str, n: int) -> list:
    """The n 3-character value fields after the 5-character row label."""
    return [line[5 + 3 * i:8 + 3 * i].strip() for i in range(n)]


def parse_block(block: str) -> pd.DataFrame:
    """One station block -> a row per forecast time: runtime and ftime (UTC, tz-aware) plus each
    element row in lower case (numeric; blank cells NaN)."""
    m = _HEADER.search(block)
    if m is None:
        raise ValueError("not an NBM text block")
    _, _, mo, dd, yyyy, hh = m.groups()
    init = pd.Timestamp(datetime(int(yyyy), int(mo), int(dd), int(hh), tzinfo=timezone.utc))
    rows = {}
    for line in block[m.end():].splitlines():
        label = line[:5].strip()
        if label and label != "DT" and re.fullmatch(r"[A-Z][A-Z0-9]{1,3}", label):
            rows[label] = line
    if "UTC" not in rows:
        raise ValueError("no UTC row")
    utc = [int(x) for x in rows["UTC"][5:].split()]
    n = len(utc)
    if "FHR" in rows:
        times = [init + pd.Timedelta(hours=int(f)) for f in _cells(rows["FHR"], n)]
    else:                           # NBH: consecutive hours from the cycle on
        times, t = [], init
        for h in utc:
            t += pd.Timedelta(hours=1)
            while t.hour != h:
                t += pd.Timedelta(hours=1)
            times.append(t)
    df = pd.DataFrame({"runtime": [init] * n, "ftime": times})
    for label, line in rows.items():
        if label in ("UTC", "FHR"):
            continue
        df[label.lower()] = pd.to_numeric(pd.Series(_cells(line, n)), errors="coerce")
    return df


def fetch(icao: str, prod: str, init) -> pd.DataFrame:
    """Rows of one cycle (see parse_block); empty when the file isn't posted or lacks the station."""
    try:
        return parse_block(station_block(icao.upper(), prod, pd.Timestamp(init)))
    except (NotPosted, LookupError):
        return pd.DataFrame()


def newest(icao: str, prod: str, as_of: Optional[datetime] = None, n: int = 4) -> pd.DataFrame:
    """Rows of the newest posted cycle at `as_of` (default now)."""
    for init in candidate_runtimes(as_of or datetime.now(timezone.utc), n):
        df = fetch(icao, prod, init)
        if not df.empty:
            return df
    return pd.DataFrame()


# ----------------------------------------------------------------------------
# cloud cover: NBH hourly SKY/SSD, then NBS 3-hourly past NBH's last hour
# ----------------------------------------------------------------------------
def cloud(icao: str, init) -> Optional[dict]:
    """Cloud series of one cycle: times, cloud_pct (SKY) and cloud_sd (SSD)."""
    init = pd.Timestamp(init)
    init = init.tz_localize("UTC") if init.tzinfo is None else init
    rows = {}
    for prod in ("nbs", "nbh"):          # NBH last, so it wins where both have the hour
        df = fetch(icao, prod, init)
        if df.empty or "sky" not in df:
            continue
        ft = pd.to_datetime(df["ftime"], utc=True)
        for t, v, s in zip(ft, df["sky"], df["ssd"] if "ssd" in df else [None] * len(df)):
            if not pd.isna(v):
                rows[t] = (float(v), None if s is None or pd.isna(s) else float(s))
    if not rows:
        return None
    ts = sorted(rows)
    return {"init_time_utc": init.strftime("%Y-%m-%dT%H"),
            "times": [t.strftime("%Y-%m-%dT%H:%M") for t in ts],
            "cloud_pct": [rows[t][0] for t in ts], "cloud_sd": [rows[t][1] for t in ts],
            "step": False, "source": "NBH SKY (hourly) + NBS SKY, SSD spread"}
