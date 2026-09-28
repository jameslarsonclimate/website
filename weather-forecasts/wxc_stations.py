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

CURRENT_STATION = "KTPA"


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

    def __post_init__(self):
        self.icao = self.icao.upper()
        if self.cli_pil is None:
            self.cli_pil = "CLI" + self.icao[-3:]
        if self.hrrr_model == "auto":
            self.hrrr_model = default_hrrr_model(self.icao)

    @property
    def label(self) -> str:
        return f"{self.name} ({self.icao})"


def default_hrrr_model(icao: str) -> Optional[str]:
    icao = icao.upper()
    if icao.startswith("PA"):          # Alaska
        return "hrrrak"
    if icao.startswith(("PH", "PG", "TJ", "TI", "PW")):  # Hawaii, Guam, PR, USVI, Wake
        return None
    return "hrrr"


# Past and present WxChallenge sites (coordinates of the ASOS sensor).
STATIONS = {
    s.icao: s for s in [
        Station("KTPA", "Tampa, FL", 27.979400, -82.535258),
        Station("KDSM", "Des Moines, IA", 41.533347, -93.658496),
        Station("KFNL", "Loveland, CO", 40.451685, -105.004186, cli_pil=""),
        Station("PAJN", "Juneau, AK", 58.356023, -134.576622, cli_pil="CLIJNU"),
        Station("KCON", "Concord, NH", 43.1953, -71.5011),
        Station("KSAV", "Savannah, GA", 32.1314, -81.2023),
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
