"""
USL model point forecasts (NanoWeather, run by the WxChallenge managers).

Pages:
  index:  http://www.microclimates.org/forecast/KTPA/
  a run:  http://www.microclimates.org/forecast/KTPA/20260928_12.html   (YYYYMMDD_HH, 12Z and 22Z)

Each run page has an hourly table for the next WxChallenge day (06Z-06Z) and a
summary table (Max Temp, Min Temp, Max Wind, Total Precip). The summary values
are the model's own daily numbers (they can exceed the hourly extremes), so those
are what we use. A 12Z or 22Z run on day D-1 forecasts day D.

Only the standard library is used for parsing (no bs4/lxml needed).
"""

import re
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from typing import Optional

BASE = "http://www.microclimates.org/forecast/{icao}/"
_MONTHS = {m: i for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], start=1)}
_RE_RUN = re.compile(r'href="(\d{8})_(\d{2})\.html"')
_RE_GEN = re.compile(r"Generated\s+(\d{1,2})\s+([A-Z]{3})\s+(\d{4})\s+(\d{2})(\d{2})\s*UTC", re.I)
_RE_NUM = re.compile(r"-?\d+(?:\.\d+)?")


class _Tables(HTMLParser):
    """Collect rows of every <table id=...> as lists of cell strings."""

    def __init__(self):
        super().__init__()
        self.tables, self._id, self._row, self._cell = {}, None, None, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self._id = a.get("id", f"t{len(self.tables)}")
            self.tables[self._id] = []
        elif tag == "tr" and self._id:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.tables[self._id].append(self._row)
            self._row = None
        elif tag == "table":
            self._id = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _num(s: str) -> Optional[float]:
    m = _RE_NUM.search(s or "")
    return float(m.group()) if m else None


def list_runs(html: str) -> list:
    """Run times (UTC datetimes) linked from a station's index page, newest first."""
    runs = {datetime.strptime(d + h, "%Y%m%d%H").replace(tzinfo=timezone.utc) for d, h in _RE_RUN.findall(html)}
    return sorted(runs, reverse=True)


def parse_run(html: str) -> dict:
    """Parse one run page into hourly series + the daily summary."""
    p = _Tables()
    p.feed(html)
    gen = _RE_GEN.search(html)
    runtime = None
    if gen:
        d, mon, y, hh, mm = gen.groups()
        runtime = datetime(int(y), _MONTHS[mon.upper()], int(d), int(hh), int(mm), tzinfo=timezone.utc)

    rows = p.tables.get("main", [])
    header = [c.lower() for c in rows[0]] if rows else []

    def col(name):
        return next((i for i, h in enumerate(header) if h.startswith(name)), None)
    i_t, i_w, i_p = col("temp"), col("wspd"), col("precip")
    i_s = col("sky")          # "Sky Cover", e.g. "65%" (display only: not part of the summary)
    i_d = col("dewpt")        # display only (the page's dewpoint panel)

    # Times: the page's date labels can't be trusted at a month change (the 20260929_12
    # run labels 1 Oct 00Z as "01 SEP 0000"), so only the first label's date is used,
    # checked against the run time (a D-1 run forecasts 06Z on D), and every later row
    # is placed by its HHMM hour counted forward from there.
    times, temp, wind, precip, sky, dewpt = [], [], [], [], [], []
    for r in rows[1:]:
        label = r[0].upper().split()
        hh = int(label[-1][:2])
        if not times:
            start = None
            if runtime is not None:
                start = datetime(runtime.year, runtime.month, runtime.day, tzinfo=timezone.utc) + timedelta(days=1)
                start = start.replace(hour=hh)
            if len(label) == 3 and label[1] in _MONTHS:          # "29 SEP 0600"
                year = runtime.year if runtime else datetime.now(timezone.utc).year
                if runtime and _MONTHS[label[1]] < runtime.month:  # Dec run -> Jan forecast
                    year += 1
                try:
                    labelled = datetime(year, _MONTHS[label[1]], int(label[0]), hh, tzinfo=timezone.utc)
                except ValueError:
                    labelled = None
                if start is None or (labelled and abs(labelled - start) <= timedelta(days=2)):
                    start = labelled or start
            t = start
        else:
            step = (hh - times[-1].hour) % 24 or 24                # hours since the previous row
            t = times[-1] + timedelta(hours=step)
        times.append(t)
        temp.append(_num(r[i_t]) if i_t is not None and i_t < len(r) else None)
        wind.append(_num(r[i_w]) if i_w is not None and i_w < len(r) else None)
        precip.append((_num(r[i_p]) or 0.0) if i_p is not None and i_p < len(r) else 0.0)
        sky.append(_num(r[i_s]) if i_s is not None and i_s < len(r) else None)
        dewpt.append(_num(r[i_d]) if i_d is not None and i_d < len(r) else None)

    stats = {}
    srows = p.tables.get("stats", [])
    if len(srows) >= 2:
        stats = {h.lower(): _num(v) for h, v in zip(srows[0], srows[1])}
    return {"runtime": runtime, "times": times, "temp_f": temp, "wind_kt": wind,
            "precip_in": precip, "sky_pct": sky, "dewpt_f": dewpt, "stats": stats}


def summarize_run(run: dict, target_day: date) -> dict:
    empty = {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
             "init_time_utc": None, "valid_range_utc": None}
    rt = run.get("runtime")
    init = rt.strftime("%Y-%m-%dT%H") if rt else None
    start = datetime(target_day.year, target_day.month, target_day.day, 6, tzinfo=timezone.utc)
    if not run["times"] or run["times"][0] != start:
        got = run["times"][0].strftime("%Y-%m-%d %HZ") if run["times"] else "nothing"
        return {**empty, "init_time_utc": init, "error": f"USL run starts {got}, not {start:%Y-%m-%d %HZ}"}
    s = run["stats"]
    temps = [t for t in run["temp_f"] if t is not None]
    winds = [w for w in run["wind_kt"] if w is not None]
    tmax = s.get("max temp", max(temps) if temps else None)
    tmin = s.get("min temp", min(temps) if temps else None)
    wmax = s.get("max wind", max(winds) if winds else None)
    pcp = s.get("total precip", sum(run["precip_in"]))
    cum, tot = [], 0.0
    for v in run["precip_in"]:
        tot += v or 0.0
        cum.append(round(tot, 2))
    return {
        "tmax_f": tmax, "tmin_f": tmin, "wind_max_kt": wmax,
        "precip_in": None if pcp is None else round(pcp, 2),
        "init_time_utc": init,
        "valid_range_utc": [start.strftime("%Y-%m-%dT%H"), (start + timedelta(days=1)).strftime("%Y-%m-%dT%H")],
        "series": {"times": [t.strftime("%Y-%m-%dT%H:%M") for t in run["times"]],
                   "tmp_f": run["temp_f"], "wsp_kt": run["wind_kt"], "precip_cum_in": cum,
                   "dpt_f": run["dewpt_f"] if any(v is not None for v in run.get("dewpt_f") or []) else None},
    }


def _get(url: str) -> Optional[str]:
    import requests
    r = requests.get(url, timeout=30)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    r.encoding = r.encoding or "iso-8859-1"
    return r.text


def run_dewpoints(icao: str, init_iso: str, target_day: date) -> Optional[dict]:
    """{time: dewpoint degF} of the run made at `init_iso` ("YYYY-MM-DDTHH", as stored in the
    series), from its run page; None if the page is gone. Display only."""
    t = datetime.strptime(init_iso, "%Y-%m-%dT%H")
    html = _get(BASE.format(icao=icao.upper()) + t.strftime("%Y%m%d_%H") + ".html")
    if html is None:
        return None
    s = summarize_run(parse_run(html), target_day).get("series") or {}
    return dict(zip(s.get("times") or [], s.get("dpt_f") or []))


def get_usl_forecast(icao: str, target_day: date, as_of: Optional[datetime] = None) -> dict:
    """
    Newest USL run (available at `as_of`, default now) that forecasts `target_day`.
    The USL is run by hand for the current WxChallenge city only, so a missing
    index page or run is normal and returned as an error, not raised.
    """
    as_of = as_of or datetime.now(timezone.utc)
    base = BASE.format(icao=icao.upper())
    fail = {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
            "init_time_utc": None, "valid_range_utc": None}
    try:
        index = _get(base)
        if index is None:
            return {**fail, "error": f"no USL page for {icao}"}
        # runs made the day before the target and before the as-of time (+30 min to post)
        cands = [rt for rt in list_runs(index)
                 if rt.date() == target_day - timedelta(days=1) and rt + timedelta(minutes=30) <= as_of]
        if not cands:
            return {**fail, "error": f"no USL run for {target_day} available at {as_of:%Y-%m-%d %HZ}"}
        last_err = None
        import wxc_cache
        for rt in cands:                                        # newest first
            hit = wxc_cache.load(icao, "USL", rt, target_day)   # run pages never change
            if hit is not None:
                return hit
            html = _get(base + rt.strftime("%Y%m%d_%H") + ".html")
            if html is None:
                continue
            res = summarize_run(parse_run(html), target_day)
            if not res.get("error"):
                wxc_cache.save(icao, "USL", rt, target_day, res)
                return res
            last_err = res
        return last_err or {**fail, "error": "USL run pages missing"}
    except Exception as exc:
        return {**fail, "error": f"USL fetch failed: {exc}"}
