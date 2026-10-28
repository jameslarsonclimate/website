"""
The KLXL model-comparison page (klxl/models/) and how it defines a forecast day.

Day D runs midnight to midnight local CLOCK time at Little Falls (CDT 05Z-05Z, CST 06Z-06Z;
the fall-back day is 25 h and the spring-forward day 23 h). Forecasts are still the last runs
before 00Z D, as on the WxChallenge page. Data in data/klxl, images in images/klxl.

Only the KLXL copies of the pipeline modules in this folder use this; the WxChallenge
originals one folder up keep their 06Z-06Z days. All times are naive UTC unless a name says
otherwise.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent      # weather-forecasts/


@dataclass(frozen=True)
class Site:
    key: str
    page: str                  # page folder under weather-forecasts/
    tz: str                    # days run local midnight to midnight in this zone
    station: str
    title: str

    @property
    def data(self) -> Path:
        return ROOT / "data" / self.key

    @property
    def images(self) -> Path:
        return ROOT / "images" / self.key

    @property
    def page_dir(self) -> Path:
        return ROOT / self.page


SITE = Site("klxl", "klxl/models", "America/Chicago", "KLXL", "Little Falls (KLXL) model forecasts")
DATA = SITE.data
IMAGES = SITE.images
TZ = ZoneInfo(SITE.tz)


def _naive(t: datetime) -> datetime:
    return t.astimezone(timezone.utc).replace(tzinfo=None) if t.tzinfo else t


def day_start(day: date) -> datetime:
    """Start of forecast day `day` (naive UTC): local midnight."""
    return _naive(datetime(day.year, day.month, day.day, tzinfo=TZ))


def day_end(day: date) -> datetime:
    """End of forecast day `day` (naive UTC) = start of the next day."""
    return day_start(day + timedelta(days=1))


def day_hours(day: date) -> int:
    """Length of day `day` in hours: 24, or 23 / 25 on a day with a clock change."""
    return int((day_end(day) - day_start(day)).total_seconds() // 3600)


def day_of(t: datetime) -> date:
    """The forecast day whose window [start, end) holds time `t` (aware, or naive UTC)."""
    return _naive(t).replace(tzinfo=timezone.utc).astimezone(TZ).date()


def window_label(day: Optional[date] = None) -> str:
    """'midnight-midnight CDT' (the zone's abbreviation on `day`)."""
    d = day or date.today()
    return f"midnight-midnight {datetime(d.year, d.month, d.day, 12, tzinfo=TZ).tzname()}"


def start_label() -> str:
    """How the day's start is named in text."""
    return "midnight"


def clip_to_day(times, cols: dict, day: date, accumulated=(), stepwise=False):
    """A model series cut to day `day`, ending exactly at both midnights.

    3- and 6-hourly output (GFS, IFS, AIFS, MOS, NBM) falls on 00/03/06...Z, which a CDT day
    (05Z-05Z) doesn't start or end on. Fetch the output times just outside the day, then call
    this: a midnight between two of them gets a value interpolated in time (or, stepwise, the
    earlier one's), and everything outside the day is dropped. Keys in `accumulated` are
    running totals and start from 0 at midnight. A midnight with no output on one side is
    left out (no extrapolation).

    times: naive UTC (anything pandas reads); cols: {key: per-time values or None}.
    Returns (times as a DatetimeIndex, {key: float array, or None where it was None}).
    """
    import numpy as np
    import pandas as pd

    t = pd.DatetimeIndex(pd.to_datetime(times))
    if t.tz is not None:
        t = t.tz_convert("UTC").tz_localize(None)
    vals = {k: (None if v is None else np.array([np.nan if x is None else x for x in v], float))
            for k, v in cols.items()}
    start, end = pd.Timestamp(day_start(day)), pd.Timestamp(day_end(day))

    def at(edge):
        """Values at `edge` from the output times on either side, or None."""
        after = np.searchsorted(t.values, edge.to_datetime64())
        if after == 0 or after >= len(t):
            return None
        a, b = after - 1, after
        w = 0.0 if stepwise else (edge - t[a]) / (t[b] - t[a])
        return {k: None if v is None else v[a] + w * (v[b] - v[a]) for k, v in vals.items()}

    inside = (t >= start) & (t <= end)
    new_t = list(t[inside])
    new_v = {k: (None if v is None else list(v[inside])) for k, v in vals.items()}
    for edge, front in ((start, True), (end, False)):
        if edge in t:
            continue
        got = at(edge)
        if got is None:
            continue
        if front:
            new_t.insert(0, edge)
        else:
            new_t.append(edge)
        for k, x in got.items():
            if new_v[k] is not None:
                new_v[k].insert(0, x) if front else new_v[k].append(x)
    out = {k: (None if v is None else np.array(v, float)) for k, v in new_v.items()}
    if new_t and new_t[0] == start:
        for k in accumulated:
            if out.get(k) is not None and len(out[k]) and np.isfinite(out[k][0]):
                out[k] = out[k] - out[k][0]
    return pd.DatetimeIndex(new_t), out


def bucket_inside(valid, step_h: int, day: date) -> bool:
    """Whether the `step_h`-hour interval ending at `valid` (naive UTC) is mostly inside day
    `day`: for interval max/min fields (GFS TMAX, IFS mx2t3, ...), so the bucket that ends
    just after midnight but mostly covers the evening before is left out, and the one that
    ends just after the next midnight is kept."""
    import pandas as pd
    v = pd.Timestamp(valid)
    s, e = pd.Timestamp(day_start(day)), pd.Timestamp(day_end(day))
    overlap = (min(v, e) - max(v - pd.Timedelta(hours=step_h), s)) / pd.Timedelta(hours=1)
    return overlap * 2 > step_h
