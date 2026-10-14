"""
"Forecast evolution" link panel on wxchallenge/index.html.

Pure functions, no network: build_config() collects the station's links (Pivotal Weather HRRR
loops, NBM 1D viewer, satellite, CSU) into a JSON-serialisable dict, and update_page()
writes it into the page's <script type="application/json" id="evo-config"> block. The page
builds the time-dependent Pivotal URLs (run hour, forecast hour) itself, so the links stay
current overnight when the scheduled job isn't running.

Values still marked FILL are left out (and logged), so a link is never published half-made.
"""

import json
import re
from pathlib import Path
from urllib.parse import urlencode

FILL = "<FILL>"

PIVOTAL_BASE = "https://www.pivotalweather.com/model.php"
PIVOTAL_MODEL = "hrrr"
DEFAULT_PIVOTAL_REGION = "conus"
# Pivotal product codes (p=); label shown in the table
PRODUCTS = [
    ("Radar + precip type", "ref1km_ptype"),
    ("MSLP + 10 m wind", "sfcwind_mslp"),
    ("Simulated IR", "sim_ir"),
    ("Total QPF", "qpf_acc"),
]
TREND_PRODUCT = "ref1km_ptype"   # dProg/dt links
POST_LAG_H = 2                   # a 00/06/12/18Z HRRR cycle counts as available this long after init
TREND_VALID_H = [12, 18, 24, 30]  # trend valid times, hours after the 00Z deadline

# NOAA GSL NBM 1D viewer (point meteogram of NBM percentiles), opened on the precipitation group;
# location is the station, everything else as James set it up (2026-10-06)
NBM_VIEWER_BASE = "https://apps.gsl.noaa.gov/nbmviewer/"
NBM_VIEWER_PARAMS = [
    ("col", "2"), ("hgt", "1"), ("obs", "false"), ("fontsize", "1"), ("location", "{icao}"),
    ("selectedgroup", "Precipitation"), ("darkmode", "on"), ("graph", "fa-chart-bar"),
    ("probfield", "Tmax"), ("proboperator", ">="), ("probvalue", "40"), ("colorfriendly", "false"),
    ("whiskers", "true"), ("boxes", "false"), ("median", "true"), ("det", "false"), ("tz", "local"),
]

SLIDER_DEFAULT = "https://rammb-slider.cira.colostate.edu/"
CSU_ZOOM_URL = FILL

CONFIG_RE = re.compile(r'(<script type="application/json" id="evo-config">)(.*?)(</script>)', re.S)


def is_fill(v):
    return v is None or (isinstance(v, str) and v.strip() == FILL)


def pivotal_region(station):
    region = getattr(station, "pivotal_region", None)
    if is_fill(region) or not region:
        print(f"Forecast evolution: no pivotal_region for {station.icao}; "
              f"using '{DEFAULT_PIVOTAL_REGION}'")
        return DEFAULT_PIVOTAL_REGION
    return region


def nbm_viewer_url(station):
    params = [(k, v.format(icao=station.icao.upper())) for k, v in NBM_VIEWER_PARAMS]
    return NBM_VIEWER_BASE + "?" + urlencode(params)


def build_config(station):
    """JSON-serialisable link config for the station. Entries still marked FILL are left out
    and listed under "skipped"."""
    skipped = []
    products = []
    for label, p in PRODUCTS:
        if is_fill(label) or is_fill(p):
            skipped.append(f"product {label}")
        else:
            products.append({"label": label, "p": p})
    trend = TREND_PRODUCT if not is_fill(TREND_PRODUCT) else None
    if trend is None:
        skipped.append("trend product")
    slider = getattr(station, "slider_url", None)
    if slider is not None and is_fill(slider):
        skipped.append("slider_url")
    satellite = slider if slider and not is_fill(slider) else SLIDER_DEFAULT
    csu = None if is_fill(CSU_ZOOM_URL) else CSU_ZOOM_URL
    if csu is None:
        skipped.append("CSU Zoom URL")
    if skipped:
        print(f"Forecast evolution: skipped (still {FILL}): {', '.join(skipped)}")
    return {
        "station": station.icao, "name": station.name,
        "lat": round(float(station.lat), 4), "lon": round(float(station.lon), 4),
        "pivotal": {"base": PIVOTAL_BASE, "model": PIVOTAL_MODEL, "region": pivotal_region(station),
                    "products": products, "trend_product": trend,
                    "post_lag_h": POST_LAG_H, "trend_valid_h": TREND_VALID_H},
        "nbm_viewer_url": nbm_viewer_url(station),
        "satellite_url": satellite,
        "csu_url": csu,
        "skipped": skipped,
    }


def config_json(cfg):
    """JSON safe inside a <script> element ('<' escaped, so no '</script>' or '<!--')."""
    return json.dumps(cfg, indent=1, ensure_ascii=False).replace("<", "\\u003c")


def embed_config(html, cfg):
    """Replace the contents of the page's evo-config block (ValueError if the page has none)."""
    if not CONFIG_RE.search(html):
        raise ValueError('page has no <script type="application/json" id="evo-config"> block')
    body = "\n" + config_json(cfg) + "\n  "
    return CONFIG_RE.sub(lambda m: m.group(1) + body + m.group(3), html, count=1)


def read_config(html):
    m = CONFIG_RE.search(html)
    return json.loads(m.group(2)) if m else None


def update_page(path, station):
    """Write the station's config into the page; True if the file changed."""
    path = Path(path)
    old = path.read_text(encoding="utf-8")
    new = embed_config(old, build_config(station))
    if new == old:
        return False
    path.write_text(new, encoding="utf-8")
    return True
