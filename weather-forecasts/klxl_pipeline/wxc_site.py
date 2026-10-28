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
