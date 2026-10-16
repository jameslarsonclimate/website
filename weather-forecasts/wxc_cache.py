"""
Point-forecast cache: once a model run has been downloaded and the station's values
extracted, the result is kept here so a later run of the script (e.g. morning, then
afternoon) reuses it instead of downloading the same model run again.

Key: station + model + run (init) time + WxChallenge day (+ 'partial' for the
rest-of-today windows). Model runs never change once published, so entries don't go
stale; old ones are pruned after PRUNE_DAYS (35: 14 hindcast days + a 14-day city + margin,
so nothing is pruned mid-city). The folder is local only (git-ignored).
"""

import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "cache"
PRUNE_DAYS = 35
ENABLED = True


def _stamp(t) -> str:
    return pd.Timestamp(t).strftime("%Y%m%d%H")


# Bump a model's version when the way its values are extracted changes, so results saved
# by the old code are ignored (and re-downloaded once) instead of being reused.
#   USL v2: fixed hourly times at month changes (page mislabels "01 SEP" for 1 Oct)
#   ENS, AIFS_ENS, HRRRCAST, REFS v2: PoP record added (HRRRCast/REFS rebuild it from the
#   point values already stored, so nothing is downloaded again)
#   USL v3: dewpoint column kept (display only)
MODEL_VERSIONS = {"USL": 3, "ENS": 2, "AIFS_ENS": 2, "HRRRCAST": 2, "REFS": 2}


def path_for(station: str, model: str, init, day, partial: bool = False) -> Path:
    tag = "_partial" if partial else ""
    ver = MODEL_VERSIONS.get(model, 1)
    name = model if ver == 1 else f"{model}-v{ver}"
    return CACHE_DIR / station.upper() / f"{name}_{_stamp(init)}_{pd.Timestamp(day):%Y%m%d}{tag}.json"


def _encode(obj):
    if isinstance(obj, dict):
        return {k: _encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_encode(v) for v in obj]
    if isinstance(obj, (pd.DatetimeIndex, pd.Series)) and np.issubdtype(obj.dtype, np.datetime64):
        return {"__times__": [pd.Timestamp(t).strftime("%Y-%m-%dT%H:%M") for t in obj]}
    if isinstance(obj, np.ndarray):
        if np.issubdtype(obj.dtype, np.datetime64):
            return {"__times__": [pd.Timestamp(t).strftime("%Y-%m-%dT%H:%M") for t in obj]}
        return {"__array__": [None if not np.isfinite(v) else float(v) for v in obj.astype(float)]}
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, (pd.Timestamp, datetime)):
        return pd.Timestamp(obj).isoformat()
    return obj


def _decode(obj):
    if isinstance(obj, dict):
        if "__times__" in obj:
            return pd.to_datetime(obj["__times__"])
        if "__array__" in obj:
            return np.array([np.nan if v is None else v for v in obj["__array__"]], dtype=float)
        return {k: _decode(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_decode(v) for v in obj]
    return obj


def load(station, model, init, day, partial=False):
    if not ENABLED:
        return None
    p = path_for(station, model, init, day, partial)
    try:
        return _decode(json.loads(p.read_text()))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save(station, model, init, day, result, partial=False):
    if not ENABLED:
        return
    p = path_for(station, model, init, day, partial)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(_encode(result)))
    tmp.replace(p)


def prune(max_age_days: int = PRUNE_DAYS) -> int:
    if not CACHE_DIR.exists():
        return 0
    cutoff, n = time.time() - max_age_days * 86400, 0
    for f in CACHE_DIR.rglob("*.json"):
        try:
            if f.stat().st_mtime < cutoff:
                f.unlink()
                n += 1
        except OSError:
            pass
    return n
