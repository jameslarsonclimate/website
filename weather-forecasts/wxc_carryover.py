"""
Keep the last good forecasts up when a run can't reach its data sources.

When the laptop sleeps or the wifi drops, most fetches fail and the run used to overwrite
forecast.json (and the page) with connection errors. Instead, a model that fails this run but
had values for the same station and target day in the previous forecast.json keeps those values,
marked "stale" (when they were pulled and why the refresh failed), and its plotting series is
restored from the saved "submitted" series so latest.png keeps its line. run_status() summarises
the run for the page banner.

Only forecast.json, the figures and the series files are affected: runs.jsonl keeps this run's
errors (verification already falls back to the previous run per model), so nothing is scored twice.
"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# connection-level failures (requests/urllib3, DNS, sockets): the source wasn't reached at all
NETWORK_ERROR = re.compile(
    r"max retries exceeded|connectionerror|connection (refused|reset|aborted)|newconnectionerror|"
    r"nameresolution|failed to resolve|nodename nor servname|name or service not known|"
    r"temporary failure in name resolution|network is unreachable|no route to host|"
    r"timed out|connecttimeout|readtimeout|remotedisconnected|urlopen error", re.I)


def is_network_error(msg) -> bool:
    return bool(msg) and bool(NETWORK_ERROR.search(str(msg)))


# a few of the hosts the run needs; reaching any one of them means the network is up
CHECK_HOSTS = ("noaa-hrrr-bdp-pds.s3.amazonaws.com", "mesonet.agron.iastate.edu", "github.com")


def network_up(hosts=CHECK_HOSTS, tries: int = 3, wait_s: float = 10.0, timeout_s: float = 5.0) -> bool:
    """True once any of `hosts` accepts a connection. A laptop just woken from sleep may need a
    few seconds to rejoin the wifi, so this tries `tries` times, `wait_s` apart."""
    import socket
    import time
    for attempt in range(tries):
        for host in hosts:
            try:
                socket.create_connection((host, 443), timeout=timeout_s).close()
                return True
            except OSError:
                continue
        if attempt < tries - 1:
            time.sleep(wait_s)
    return False


def has_values(m: Optional[dict]) -> bool:
    """A usable forecast (precip-only sources have no high/low)."""
    return bool(m) and not m.get("error") and (m.get("tmax_f") is not None or m.get("precip_in") is not None)


def load_previous(path: Path, station: str, day) -> dict:
    """Models of the previous forecast.json if it is for the same station and target day, else {}."""
    try:
        prev = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}
    meta = prev.get("meta") or {}
    if meta.get("station") != station or meta.get("target_date") != day.isoformat():
        return {}
    gen = prev.get("generated_at_utc")
    out = {}
    for k, m in (prev.get("models") or {}).items():
        if k != "CONSENSUS" and has_values(m):
            # when the values were pulled: kept from an earlier carry-over, else that run's time
            out[k] = {**m, "stale": {**(m.get("stale") or {}),
                                     "fetched_at_utc": (m.get("stale") or {}).get("fetched_at_utc") or gen}}
    return out


def _grib_series(s: dict) -> dict:
    return {"times": pd.to_datetime(s["times"]), "temp_f": np.asarray(s["temp_f"], float),
            "wind_kt": np.asarray(s["wind_kt"], float), "precip_in": np.asarray(s["precip_in"], float)}


def _text_series(s: dict) -> dict:
    return {"times": s["times"], "tmp_f": s.get("temp_f"), "wsp_kt": s.get("wind_kt"),
            "precip_cum_in": s.get("precip_in")}


def carry_over(results: dict, mos: dict, models: dict, previous: dict,
               prev_series: Optional[dict], grib: list) -> dict:
    """
    Replace each failed model in `models` (and its entry in `results` for the GRIB models in
    `grib`, or in `mos` for the rest) by its previous values. Returns {name: failed entry} of
    the models carried over; the failed entries are what runs.jsonl should record.
    prev_series: the saved "submitted" series for the day; a model's series is restored from
    it when it is of the same run.
    """
    saved = (prev_series or {}).get("models") or {}
    carried = {}
    for name, m in list(models.items()):
        if name == "CONSENSUS" or has_values(m) or name not in previous:
            continue
        old = dict(previous[name])
        old["stale"] = {**old["stale"], "error": (m or {}).get("error") or "no data this run"}
        s = saved.get(name)
        if not (s and s.get("times") and s.get("init_time_utc") == old.get("init_time_utc")):
            s = None
        if name in grib:
            results[name] = {"metrics": old, "series": _grib_series(s) if s else None}
        else:
            mos[name] = {**old, "series": _text_series(s) if s else None}
        carried[name] = m
        models[name] = old
    return carried


def run_status(errors: dict, carried: list, now_iso: str) -> dict:
    """
    errors: {model: error message} of every model that failed this run (before carry-over).
    The run counts as not ok when a source couldn't be reached, or a model that had a
    forecast for the day lost it (carried over); a precip product that simply isn't posted
    yet is normal.
    """
    network = sorted(k for k, e in errors.items() if is_network_error(e))
    ok = not network and not carried
    out = {"ok": ok, "checked_at_utc": now_iso, "connectivity": bool(network),
           "failed": sorted(errors), "carried_over": sorted(carried)}
    if not ok:
        when = f"{datetime.fromisoformat(now_iso):%H:%MZ}"
        out["message"] = ((f"Connectivity issues: the update at {when} couldn't reach some data sources"
                           if network else f"The update at {when} failed for some sources")
                          + f"; latest forecasts not pulled for {', '.join(sorted(errors))}."
                          + (f" Showing the last good forecasts for {', '.join(sorted(carried))}."
                             if carried else ""))
    return out
