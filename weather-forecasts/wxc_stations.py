"""
Station registry for WxChallenge cities.

To rotate cities, either:
  * change CURRENT_STATION below, or
  * pass it on the command line:  ./getForecast_wxChallenge.sh KTPA
  * or set the environment variable WXC_STATION=KTPA

Unknown ICAO ids are looked up automatically (lat/lon from the Iowa State
Mesonet), but adding them here is better so the name / CLI product are right.
"""

import io
import os
import sys
from dataclasses import dataclass
from typing import Optional

CURRENT_STATION = "KMSP"

AFD_URL = ("https://forecast.weather.gov/product.php?site={wfo}&issuedby={wfo}&product=afd"
           "&format=ci&version=1&glossary=1")


@dataclass
class Station:
    icao: str
    name: str
    lat: float
    lon: float
    # NWS daily climate report (CLI) product id used for the official max wind.
    # Default is "CLI" + last three letters of the ICAO id; override when it differs
    # (e.g., Juneau PAJN -> CLIJNU) or set "" when the site has no CLI (e.g., KFNL).
    cli_pil: Optional[str] = None
    # HRRR domain: "hrrr" (CONUS), "hrrrak" (Alaska) or None (Hawaii, PR, ...).
    # Leave as None-sentinel "auto" to infer from the ICAO prefix.
    hrrr_model: Optional[str] = "auto"
    # RRFS domain for Herbie: "conus", "ak", "hi", "pr" or None
    rrfs_domain: Optional[str] = "auto"
    # GOES satellite for the cloud-mask panel: "G19" (East) or "G18" (West), or None
    goes: Optional[str] = "auto"
    # ABI sector: "C" (CONUS/PACUS, every 5 min) or "F" (full disk, every 10 min)
    goes_sector: Optional[str] = "auto"
    # Pivotal Weather map region (r=) for the page's forecast-evolution links, e.g. "us_se";
    # None -> "conus" (wxc_links logs it). Only set codes checked on pivotalweather.com.
    pivotal_region: Optional[str] = None
    # RAMMB/CIRA SLIDER permalink centred on the station (None -> the SLIDER home page)
    slider_url: Optional[str] = None
    # IANA time zone; its STANDARD offset sets the CLI day (midnight to midnight local standard
    # time all year, e.g. EST 05Z-05Z). None -> guessed from the ICAO prefix / longitude (logged).
    tz: Optional[str] = None
    # NWS forecast office (WFO) that issues the Area Forecast Discussion, e.g. "TBW" for KTPA.
    # Not always the CLI PIL's letters; None -> no AFD link.
    wfo: Optional[str] = None

    def __post_init__(self):
        self.icao = self.icao.upper()
        if self.cli_pil is None:
            self.cli_pil = "CLI" + self.icao[-3:]
        if self.hrrr_model == "auto":
            self.hrrr_model = default_hrrr_model(self.icao)
        if self.rrfs_domain == "auto":
            self.rrfs_domain = default_rrfs_domain(self.icao)
        if self.goes == "auto":
            self.goes = default_goes(self.icao, self.lon)
        if self.goes_sector == "auto":
            self.goes_sector = "C" if self.icao.startswith("K") else "F"
        if self.tz is None:
            self.tz = default_tz(self.icao, self.lon)
            print(f"Note: {self.icao} has no tz in wxc_stations.STATIONS; guessed {self.tz} "
                  f"(LST = UTC{self.lst_offset_hours:+g}). Set it if that is wrong.")

    @property
    def lst_offset_hours(self) -> float:
        """UTC offset of local STANDARD time (no daylight saving), e.g. -5 for EST."""
        from datetime import datetime
        from zoneinfo import ZoneInfo
        d = datetime(2026, 1, 15, 12, tzinfo=ZoneInfo(self.tz))
        return (d.utcoffset() - d.dst()).total_seconds() / 3600

    @property
    def label(self) -> str:
        return f"{self.name} ({self.icao})"

    @property
    def afd_url(self) -> Optional[str]:
        """Latest NWS Area Forecast Discussion from the station's WFO (None when wfo is unset)."""
        return AFD_URL.format(wfo=self.wfo.lower()) if self.wfo else None


def default_rrfs_domain(icao: str) -> Optional[str]:
    icao = icao.upper()
    if icao.startswith("PA"):
        return "ak"
    if icao.startswith("PH"):
        return "hi"
    if icao.startswith(("TJ", "TI")):
        return "pr"
    if icao.startswith(("PG", "PW")):
        return None
    return "conus"


# GOES-R series operational satellites: AWS bucket and nominal sub-satellite longitude
GOES_SATELLITES = {"G19": ("noaa-goes19", -75.2), "G18": ("noaa-goes18", -137.2)}


def default_goes(icao: str, lon: float) -> Optional[str]:
    """Satellite with the nearest sub-satellite longitude; Alaska and Hawaii use GOES-18."""
    icao = icao.upper()
    if icao.startswith(("PA", "PH")):
        return "G18"
    if icao.startswith(("PG", "PW")):   # Guam, Wake: beyond the GOES-West view
        return None
    return min(GOES_SATELLITES, key=lambda s: abs(lon - GOES_SATELLITES[s][1]))


def default_tz(icao: str, lon: float) -> str:
    """Rough time zone guess for a station missing from the registry (US time-zone borders
    are not meridians, so check it): by ICAO prefix outside CONUS, else by longitude."""
    icao = icao.upper()
    prefixes = {"PA": "America/Anchorage", "PH": "Pacific/Honolulu", "TJ": "America/Puerto_Rico",
                "TI": "America/St_Thomas", "PG": "Pacific/Guam", "PW": "Pacific/Wake"}
    if icao[:2] in prefixes:
        return prefixes[icao[:2]]
    if lon >= -86.5:
        return "America/New_York"
    if lon >= -102.0:
        return "America/Chicago"
    if lon >= -115.5:
        return "America/Denver"
    return "America/Los_Angeles"


def default_hrrr_model(icao: str) -> Optional[str]:
    icao = icao.upper()
    if icao.startswith("PA"):          # Alaska
        return "hrrrak"
    if icao.startswith(("PH", "PG", "TJ", "TI", "PW")):  # Hawaii, Guam, PR, USVI, Wake
        return None
    return "hrrr"


SLIDER_KTPA = ("https://slider.cira.colostate.edu/?sat=goes-19&sec=full_disk&x=9432&y=5063&z=5"
               "&angle=0&im=12&ts=1&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white"
               "&mops%5Bborders%5D=0.6&p%5B0%5D=geocolor&opacity%5B0%5D=1&pause=0&slider=-1"
               "&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider"
               "&draw_color=FFD700&draw_width=6")

SLIDER_KOLM = ("https://slider.cira.colostate.edu/?sat=goes-18&sec=conus&x=6964&y=2663&z=4"
               "&angle=0&im=24&ts=1&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white"
               "&mops%5Bborders%5D=0.4&p%5B0%5D=geocolor&opacity%5B0%5D=1&pause=0&slider=-1"
               "&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider"
               "&draw_color=FFD700&draw_width=6")

SLIDER_KMSP = ("https://slider.cira.colostate.edu/?sat=goes-19&sec=conus&x=4508&y=2984&z=3"
               "&angle=0&im=24&ts=1&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white"
               "&mops%5Bborders%5D=0.4&p%5B0%5D=geocolor&opacity%5B0%5D=1&pause=0&slider=-1"
               "&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider"
               "&draw_color=FFD700&draw_width=6")

# Past and present WxChallenge sites (coordinates of the ASOS sensor).
STATIONS = {
    s.icao: s for s in [
        Station("KTPA", "Tampa, FL", 27.979400, -82.535258, pivotal_region="us_se",
                slider_url=SLIDER_KTPA, tz="America/New_York", wfo="TBW"),
        Station("KDSM", "Des Moines, IA", 41.533347, -93.658496, tz="America/Chicago", wfo="DMX"),
        Station("KFNL", "Loveland, CO", 40.451685, -105.004186, cli_pil="", tz="America/Denver",
                wfo="BOU"),
        Station("PAJN", "Juneau, AK", 58.356023, -134.576622, cli_pil="CLIJNU", tz="America/Juneau",
                wfo="AJK"),
        Station("KCON", "Concord, NH", 43.1953, -71.5011, tz="America/New_York", wfo="GYX"),
        Station("KSAV", "Savannah, GA", 32.1314, -81.2023, tz="America/New_York", wfo="CHS"),
        Station("KOLM", "Olympia, WA", 46.973445, -122.898031, pivotal_region="us_nw",
                slider_url=SLIDER_KOLM, tz="America/Los_Angeles", wfo="SEW"),
        Station("KMSP", "Minneapolis, MN", 44.883962, -93.220580, pivotal_region="us_mw",
                slider_url=SLIDER_KMSP, tz="America/Chicago", wfo="MPX"),
    ]
}


def _lookup_iem(icao: str) -> Optional[Station]:
    """Look up lat/lon for an unknown station from a 1-day IEM ASOS request."""
    try:
        import requests
        import pandas as pd
        from datetime import datetime, timedelta, timezone
        d = datetime.now(timezone.utc) - timedelta(days=1)
        r = requests.get(
            "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py",
            params={"station": icao, "data": "tmpf", "year1": d.year, "month1": d.month,
                    "day1": d.day, "year2": d.year, "month2": d.month, "day2": d.day,
                    "tz": "Etc/UTC", "format": "onlycomma", "latlon": "yes"},
            timeout=30)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text))
        if df.empty:
            return None
        return Station(icao, icao, float(df["lat"].iloc[0]), float(df["lon"].iloc[0]))
    except Exception as exc:
        print(f"Station lookup for {icao} failed: {exc}")
        return None


def get_station(icao: Optional[str] = None) -> Station:
    """Resolve the station: explicit arg > WXC_STATION env var > CURRENT_STATION."""
    icao = (icao or os.environ.get("WXC_STATION") or CURRENT_STATION).upper()
    if icao in STATIONS:
        return STATIONS[icao]
    st = _lookup_iem(icao)
    if st is None:
        sys.exit(f"Unknown station {icao}: add it to STATIONS in wxc_stations.py")
    print(f"Note: {icao} not in wxc_stations.STATIONS; using IEM location "
          f"({st.lat:.4f}, {st.lon:.4f}). Consider adding it to the registry.")
    return st
