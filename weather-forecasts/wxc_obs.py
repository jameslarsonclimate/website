"""
Observed WxChallenge verification values for forecast day D (06Z D to 06Z D+1).

Follows the WxChallenge rules, checked against their final results (tests/test_obs_official.py).
Temperatures are rounded to whole degF, wind to whole kt, precip to 0.01"; a trace counts as 0.

  high / low  max / min, in tenths of degC, of the T groups of every report in the day (routine
              and SPECI; whole-degree body temperatures only if no T groups) and of the 6-h max /
              min groups (1snTTT / 2snTTT) of the four standard synoptic reports ending the 6-h periods (~1153Z, 1753Z, 2353Z on D and ~0553Z
              on D+1; the ~0553Z report on D covers the day before). Then degF, rounded.
  precip      sum of the 6RRRR groups of those four reports (absent = 0, 60000 = trace = 0; the
              03/09/15/21Z groups are 3-h amounts and are ignored). If one is 6//// (indeterminate)
              the P groups of the day's ROUTINE reports (0653Z D .. 0553Z D+1) are summed instead.
              A SPECI's P group counts from the last routine report, so SPECI P groups are never
              summed. Precip after the ~0553Z D+1 report counts for D+1.
  max wind    the NWS daily climate report (CLI) highest (2-min) wind speed for D, mph -> kt. The
              CLI day is midnight to midnight local STANDARD time all year (EST 05Z-05Z, CST
              06Z-06Z, ...) and only a CLI issued after that day ended is final; until then the wind
              is "pending". A METAR sustained wind (routine or SPECI, never a gust) replaces the CLI
              value only if it is higher and inside that LST window.
  backups     the CLI high / low / precip, only when the METARs fail (a standard report or its
              group missing, or 6//// without a full set of routine reports).

Each record's "source" says what set each value: "6h_group", "hourly" (report T or P groups),
"cli", "metar_override", "metar" (no CLI wind), "cli_backup", "pending". Nothing automated
knows about precip measured by an NWS observer or Advisory Board rulings, so those are never
forced here; "notes" flags CLI / METAR disagreements that may point at one.
"""

import io
import re
import time
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import pandas as pd

import wxc_pop

IEM_ASOS = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
IEM_AFOS = "https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py"
IEM_CLI_JSON = "https://mesonet.agron.iastate.edu/json/cli.py"
IEM_CF6_JSON = "https://mesonet.agron.iastate.edu/json/cf6.py"
NWS_API = "https://api.weather.gov"
NWS_HEADERS = {"User-Agent": "wxchallenge-verification (personal forecasting script)",
               "Accept": "application/ld+json"}
MPH_PER_KT = 1.150779
MPH_TO_KT = 1 / MPH_PER_KT
OBS_METHOD = 2            # stored records from an older method are fetched once more
STD_WINDOW = timedelta(minutes=15)       # standard report: routine, 45-59 min before 00/06/12/18Z
PERIOD_ENDS_H = (12, 18, 24, 30)         # hours after 00Z D ending the day's 6-h periods
SCORED = ("tmax_f", "tmin_f", "wind_max_kt", "precip_in")

_RE_WIND = re.compile(r"\b(\d{3}|VRB)(\d{2,3})(?:G(\d{2,3}))?KT\b")
_RE_TEMP_BODY = re.compile(r"(?<![\w/])(M?\d{2})/(M?\d{2})?(?![\w/])")
_RE_COR = re.compile(r"\bCOR\b")
# remark groups, matched against whole tokens (a search would also hit e.g. PK WND 21031/2312)
_RE_TGROUP = re.compile(r"T([01])(\d{3})(?:[01]\d{3}|////)?")
_RE_P = re.compile(r"P(\d{4}|////)")
_RE_6 = re.compile(r"6(\d{4}|////)")
_RE_MAX6 = re.compile(r"1([01])(\d{3})")
_RE_MIN6 = re.compile(r"2([01])(\d{3})")


def c_to_f(c):
    return None if c is None else c * 9.0 / 5.0 + 32.0


def c10_to_f(c10):
    """Tenths of degC -> degF."""
    return None if c10 is None or pd.isna(c10) else c10 / 10.0 * 9.0 / 5.0 + 32.0


def round_half_up(x):
    """Round like the verifiers do (0.5 -> away from zero), not banker's rounding."""
    if x is None or pd.isna(x):
        return None
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def mph_to_kt(mph):
    return None if mph is None else round_half_up(mph / MPH_PER_KT)


def _signed_tenths(sign, digits) -> int:
    v = int(digits)
    return -v if sign == "1" else v


# ----------------------------------------------------------------------------
# METAR parsing
# ----------------------------------------------------------------------------
def parse_metar(metar: str) -> dict:
    """Pull out the fields WxChallenge needs from one METAR / SPECI string."""
    out = {"temp_f": None, "temp_c10": None, "temp_tgroup": False, "wind_kt": None, "gust_kt": None,
           "precip_1h": None, "precip_1h_missing": False,
           "precip_6grp": None, "precip_6grp_missing": False,
           "max6_f": None, "min6_f": None, "max6_c10": None, "min6_c10": None,
           "has_rmk": False, "cor": False, "speci": None}
    if not isinstance(metar, str):
        return out
    metar = metar.strip()
    head = metar.split(None, 1)[0] if metar else ""
    out["speci"] = True if head == "SPECI" else False if head == "METAR" else None
    body, _, rmk = metar.partition(" RMK ")
    out["has_rmk"] = bool(rmk)
    out["cor"] = bool(_RE_COR.search(body))
    tokens = rmk.split()

    def group(rx):
        return next((m for m in map(rx.fullmatch, tokens) if m), None)

    m = _RE_WIND.search(body)
    if m:
        out["wind_kt"] = int(m.group(2))
        out["gust_kt"] = int(m.group(3)) if m.group(3) else None

    m = group(_RE_TGROUP)
    if m:
        out["temp_c10"] = _signed_tenths(m.group(1), m.group(2))
        out["temp_tgroup"] = True
    else:                                    # whole degC from the body (display; see day_values)
        m = _RE_TEMP_BODY.search(body)
        if m:
            t = m.group(1)
            out["temp_c10"] = 10 * (-int(t[1:]) if t.startswith("M") else int(t))
    out["temp_f"] = c10_to_f(out["temp_c10"])

    # Hourly precip (hundredths). P0000 = trace. No P group in a routine ob = no precip.
    m = group(_RE_P)
    if m:
        if m.group(1) == "////":
            out["precip_1h_missing"] = True
        else:
            out["precip_1h"] = int(m.group(1)) / 100.0
            out["trace"] = out["precip_1h"] == 0.0
    # 6RRRR: 6-h amount in the 00/06/12/18Z reports (3-h at 03/09/15/21Z); 60000 = trace
    m = group(_RE_6)
    if m:
        if m.group(1) == "////":
            out["precip_6grp_missing"] = True
        else:
            out["precip_6grp"] = int(m.group(1)) / 100.0

    m = group(_RE_MAX6)
    if m:
        out["max6_c10"] = _signed_tenths(m.group(1), m.group(2))
        out["max6_f"] = c10_to_f(out["max6_c10"])
    m = group(_RE_MIN6)
    if m:
        out["min6_c10"] = _signed_tenths(m.group(1), m.group(2))
        out["min6_f"] = c10_to_f(out["min6_c10"])
    return out


def day_label(ts: pd.Timestamp) -> date:
    """WxChallenge day of a routine report: the xx53Z report belongs to the next top of the
    hour, so day D holds the reports rounded to (D 06Z, D+1 06Z], i.e. 0653Z ... 0553Z(+1)."""
    rounded = ts.round("h")
    return (rounded - timedelta(hours=6, minutes=1)).date()


def routine_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Heuristic routine reports, for data without report types: the routine minute is the site's
    most common minute (e.g. :53); per hour keep the report closest to it (within 10 minutes).
    """
    if df.empty:
        return df
    minutes = df["valid"].dt.minute
    routine_min = int(minutes.mode().iloc[0])
    target = df["valid"].dt.floor("h") + pd.to_timedelta(routine_min, unit="m")
    dist = (df["valid"] - target).abs()
    df = df.assign(_dist=dist, _slot=target)
    df = df[df["_dist"] <= pd.Timedelta(minutes=10)]
    df = df.sort_values("_dist").drop_duplicates("_slot").sort_values("valid")
    return df.drop(columns=["_dist", "_slot"])


def prepare_reports(df: pd.DataFrame) -> pd.DataFrame:
    """
    Raw reports (columns 'valid' UTC, 'metar', optional 'report_type' 3 = routine / 4 = SPECI as
    IEM tags them) -> one report per time, sorted, with a 'routine' flag and the parsed fields.
    An ob sent twice (original and COR) keeps the correction (else the later copy). Without
    report types, a leading METAR / SPECI decides, else the routine_only heuristic.
    """
    cols = ["valid", "metar", "routine"] + list(parse_metar("").keys())
    if df is None or df.empty:
        return pd.DataFrame(columns=cols)
    df = df.copy()
    df["valid"] = pd.to_datetime(df["valid"], utc=True)
    df = df[df["metar"].notna()]
    df = df.assign(_cor=df["metar"].str.contains(_RE_COR), _ord=range(len(df)))
    df = (df.sort_values(["valid", "_cor", "_ord"]).drop_duplicates("valid", keep="last")
          .drop(columns=["_cor", "_ord"]))
    parsed = pd.DataFrame([parse_metar(m) for m in df["metar"]], index=df.index)
    heur = set(routine_only(df[["valid"]]).index)
    rt = df["report_type"] if "report_type" in df else pd.Series(None, index=df.index, dtype=object)
    routine = []
    for i, typ, speci in zip(df.index, rt, parsed["speci"]):
        if pd.notna(typ):
            routine.append(int(typ) == 3)
        elif speci is not None:
            routine.append(not speci)
        else:
            routine.append(i in heur)
    out = pd.concat([df[["valid", "metar"]], parsed], axis=1)
    out["routine"] = routine
    return out[cols].reset_index(drop=True)


def report_series(df: pd.DataFrame) -> pd.DataFrame:
    """
    Every report (routine + specials) as a time series for plotting the day so far:
    temp_f, wind_kt, gust_kt, 6-h max/min marks and a running precip total. Specials'
    P groups count precip since the last routine ob, so the running total is
    (sum of routine P groups so far) + (the special's own P group).
    """
    if df.empty:
        return pd.DataFrame(columns=["valid", "temp_f", "wind_kt", "gust_kt", "max6_f", "min6_f",
                                     "precip_total_in", "routine"])
    out = prepare_reports(df)[["valid", "temp_f", "wind_kt", "gust_kt", "max6_f", "min6_f",
                               "precip_1h", "routine"]]
    total, running = 0.0, []
    for is_routine, p in zip(out["routine"], out["precip_1h"]):
        p = 0.0 if p is None or pd.isna(p) else float(p)
        if is_routine:
            total += p
            running.append(round(total, 2))
        else:
            running.append(round(total + p, 2))
    out = out.assign(precip_total_in=running)
    return out.drop(columns=["precip_1h"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Daily values from the METARs
# ----------------------------------------------------------------------------
def _utc(d: date, hours: float = 0) -> pd.Timestamp:
    return pd.Timestamp(datetime(d.year, d.month, d.day, tzinfo=timezone.utc)) + pd.Timedelta(hours=hours)


def lst_window(d: date, utc_offset: float):
    """The CLI day D in UTC: midnight to midnight local standard time (e.g. EST: 05Z-05Z)."""
    start = _utc(d, -utc_offset)
    return start, start + pd.Timedelta(hours=24)


def standard_reports(rep: pd.DataFrame, d: date) -> list:
    """The four standard synoptic reports ending day D's 6-h periods (12Z, 18Z, 00Z, 06Z+1):
    routine reports 45-59 min before the hour. None where missing."""
    out = []
    for h in PERIOD_ENDS_H:
        end = _utc(d, h)
        sel = rep[rep["routine"] & (rep["valid"] >= end - STD_WINDOW) & (rep["valid"] < end)]
        out.append(None if sel.empty else sel.iloc[-1])
    return out


def _num(x):
    """None for missing values (pandas gives NaN, which is truthy)."""
    return None if x is None or pd.isna(x) else x


def _max(vals):
    vals = [v for v in vals if v is not None and not pd.isna(v)]
    return max(vals) if vals else None


def _min(vals):
    vals = [v for v in vals if v is not None and not pd.isna(v)]
    return min(vals) if vals else None


def _six_valid(s) -> bool:
    """A standard report whose 6RRRR can be used (absent group = no precip)."""
    return s is not None and bool(s["has_rmk"]) and not s["precip_6grp_missing"]


def day_values(rep: pd.DataFrame, d: date, utc_offset: Optional[float] = None) -> dict:
    """
    METAR-based values for day D from prepared reports (prepare_reports). The CLI is applied
    later (finalize). utc_offset (local standard time) adds the max wind inside the CLI's LST day.
    """
    start, end = _utc(d, 6), _utc(d, 30)
    inday = rep[(rep["valid"] > start) & (rep["valid"] <= end)]
    rounded = rep["valid"].dt.round("h")
    routine = rep[rep["routine"] & (rounded > start) & (rounded <= end)]     # day_label() == d
    n_hours = int(routine["valid"].dt.round("h").nunique())
    std = standard_reports(rep, d)
    src, ok, notes = {}, {}, []

    # ---- temperature: T groups of every report + the 6-h groups, in tenths of degC ----
    # A body temperature (e.g. 24/23 in a SPECI without remarks) is rounded to whole degC, so it
    # can't set a tenths extreme (24 could be 24.4 C = 76 F); used only if no report has a T group.
    tg = inday[inday["temp_tgroup"].astype(bool)] if inday["temp_tgroup"].astype(bool).any() else inday
    t_hi, t_lo = _max(tg["temp_c10"]), _min(tg["temp_c10"])
    s_hi = _max([s["max6_c10"] for s in std if s is not None])
    s_lo = _min([s["min6_c10"] for s in std if s is not None])
    hi, lo = _max([t_hi, s_hi]), _min([t_lo, s_lo])
    src["tmax_f"] = "6h_group" if s_hi is not None and (t_hi is None or s_hi > t_hi) else "hourly"
    src["tmin_f"] = "6h_group" if s_lo is not None and (t_lo is None or s_lo < t_lo) else "hourly"
    ok["tmax_f"] = all(s is not None and _num(s["max6_c10"]) is not None for s in std)
    ok["tmin_f"] = all(s is not None and _num(s["min6_c10"]) is not None for s in std)

    # ---- precip: 6RRRR of the standard reports; routine P groups if one is 6//// ----
    p_routine = routine["precip_1h"].fillna(0.0)
    hourly_sum = round(float(p_routine.sum()), 2)
    hourly_ok = (n_hours == 24 and routine["has_rmk"].all()
                 and not routine["precip_1h_missing"].any())
    blocks = {}
    lab = routine["valid"].dt.round("h").map(wxc_pop.block_of_hour_ending)
    for b, s in zip(wxc_pop.BLOCK_LABELS, std):
        sel = routine[lab == b]
        if _six_valid(s):
            blocks[b] = round(float(_num(s["precip_6grp"]) or 0.0), 2)
        elif sel["valid"].dt.round("h").nunique() >= 4:          # PoP only: partial sum is fine
            blocks[b] = round(float(sel["precip_1h"].fillna(0.0).sum()), 2)
        else:
            blocks[b] = None
    six_ok = all(_six_valid(s) for s in std)
    six_sum = round(sum(float(_num(s["precip_6grp"]) or 0.0) for s in std if _six_valid(s)), 2)
    if six_ok:
        precip, src["precip_in"], ok["precip_in"] = six_sum, "6h_group", True
    elif hourly_ok:
        precip, src["precip_in"], ok["precip_in"] = hourly_sum, "hourly", True
        notes.append("6-h precip group indeterminate or missing: routine hourly P groups summed")
    else:
        # best METAR estimate: each period's 6RRRR where usable, else its hourly P groups
        precip = round(sum(v or 0.0 for v in blocks.values()), 2)
        src["precip_in"], ok["precip_in"] = "hourly", False
    trace = precip == 0.0 and (bool((routine["precip_1h"] == 0.0).any())
                               or any(_six_valid(s) and s["precip_6grp"] == 0.0 for s in std))

    # ---- wind (METAR side; the CLI decides in finalize) ----
    rec_lst = {}
    if utc_offset is not None:
        ls, le = lst_window(d, utc_offset)
        lw = rep[(rep["valid"] > ls) & (rep["valid"] <= le) & rep["wind_kt"].notna()]
        top = lw.loc[lw["wind_kt"].idxmax()] if not lw.empty else None
        rec_lst = {
            "lst_window_utc": [ls.strftime("%Y-%m-%dT%H:%MZ"), le.strftime("%Y-%m-%dT%H:%MZ")],
            "wind_max_kt_lst": None if top is None else int(top["wind_kt"]),
            "wind_max_lst_at": None if top is None else top["valid"].strftime("%Y-%m-%dT%H:%MZ"),
            "lst_covered": bool(not rep.empty and rep["valid"].min() <= ls + pd.Timedelta(hours=1)
                                and rep["valid"].max() >= le - pd.Timedelta(hours=1)),
        }

    def wmax(s):
        return None if s.isna().all() else int(s.max())

    def f1(c10):
        return None if c10 is None else round(c10_to_f(c10), 1)

    return {
        "date": d.isoformat(),
        "tmax_f_raw": f1(hi), "tmin_f_raw": f1(lo),
        "tmax_f": round_half_up(c10_to_f(hi)), "tmin_f": round_half_up(c10_to_f(lo)),
        # report T groups only (routine + SPECI), without the 6-h groups
        "tmax_f_hourly": round_half_up(c10_to_f(t_hi)), "tmin_f_hourly": round_half_up(c10_to_f(t_lo)),
        "wind_max_kt_metar": wmax(routine["wind_kt"]),             # routine reports, 06Z-06Z
        "gust_max_kt_metar": wmax(routine["gust_kt"]),
        "wind_max_kt_all_reports": wmax(inday["wind_kt"]),          # routine + SPECI, 06Z-06Z
        **rec_lst,
        "precip_in": precip,
        "precip_trace": bool(trace),
        "precip_source": src["precip_in"],
        "precip_6hr_groups_in": six_sum if six_ok else None,
        "precip_hourly_in": hourly_sum,
        "precip_6h_in": blocks,
        "n_routine_obs": n_hours,
        "n_standard_obs": sum(s is not None for s in std),
        "complete": bool(n_hours >= 20 or all(ok.values())),
        "source": src,
        "metar_ok": ok,
        "notes": notes,
    }


def daily_records(df: pd.DataFrame, utc_offset: Optional[float] = None) -> list:
    """df has columns 'valid' (UTC) and 'metar' (optionally 'report_type'). One dict per
    WxChallenge day with routine reports, METAR values only (finalize() adds the CLI)."""
    rep = prepare_reports(df)
    if rep.empty:
        return []
    days = sorted({day_label(t) for t in rep.loc[rep["routine"], "valid"]})
    return [day_values(rep, d, utc_offset) for d in days]


def summarize_metars(df: pd.DataFrame, utc_offset: Optional[float] = None) -> pd.DataFrame:
    """daily_records as a DataFrame (one row per day)."""
    return pd.DataFrame(daily_records(df, utc_offset))


SKY_FIELDS = ["skyc1", "skyc2", "skyc3", "skyc4", "skyl1", "skyl2", "skyl3", "skyl4"]


def _get(url, params=None, headers=None, retries=3, timeout=60):
    """GET with retries; IEM answers 'Too many requests' when hit too fast, so back off."""
    import requests
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=timeout)
            if r.status_code == 429 or r.text.startswith("Too many requests"):
                raise RuntimeError("rate limited")
            r.raise_for_status()
            if r.text.startswith("ERROR"):
                raise RuntimeError(r.text[:200])
            return r
        except Exception as exc:
            last = exc
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"request failed ({url}): {last}")


def fetch_metars(station: str, start: datetime, end: datetime, retries: int = 3,
                 specials: bool = False, sky: bool = False) -> pd.DataFrame:
    """Routine METARs (plus specials if asked) from IEM in [start, end] (UTC), with IEM's
    report_type (3 routine, 4 SPECI) kept in a column. sky=True also returns the sky condition
    columns (skyc1-4, skyl1-4; display only)."""
    params = {
        "network": "ASOS", "station": station, "data": "metar",
        "year1": start.year, "month1": start.month, "day1": start.day,
        "hour1": start.hour, "minute1": 0,
        "year2": end.year, "month2": end.month, "day2": end.day,
        "hour2": end.hour, "minute2": 59,
        "tz": "Etc/UTC", "format": "onlycomma", "latlon": "no", "elev": "no",
        "missing": "M", "trace": "T", "direct": "no",
    }
    extra = [("data", f) for f in SKY_FIELDS] if sky else []
    frames = []
    # one request per report type: IEM's output has no type column, and the routine/SPECI split
    # decides which reports carry the day's 6-h groups and which P groups may be summed
    for rt in ([3, 4] if specials else [3]):
        r = _get(IEM_ASOS, params=list(params.items()) + [("report_type", rt)] + extra, retries=retries)
        df = pd.read_csv(io.StringIO(r.text))
        if not df.empty:
            if "metar" not in df:
                raise RuntimeError(f"IEM METAR request for {station}: unexpected reply {r.text[:120]!r}")
            frames.append(df[["valid", "metar"] + ([f for f in SKY_FIELDS if f in df] if sky else [])]
                          .assign(report_type=rt))
    if not frames:
        return pd.DataFrame(columns=["valid", "metar", "report_type"])
    return pd.concat(frames).sort_values("valid").reset_index(drop=True)


# ----------------------------------------------------------------------------
# NWS daily climate report (CLI)
# ----------------------------------------------------------------------------
_MONTHS = {m: i for i, m in enumerate(
    ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST",
     "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"], start=1)}
_RE_WMO = re.compile(r"^[A-Z]{4}\d{2} [A-Z]{4} (\d{2})(\d{2})(\d{2})", re.M)
_RE_CLI_DATE = re.compile(r"CLIMATE SUMMARY FOR\s+([A-Z]+)\s+(\d{1,2})\s+(\d{4})")
_RE_CLI_WIND = re.compile(r"HIGHEST WIND SPEED\s+(\d+|MM)")
_RE_CLI_GUST = re.compile(r"HIGHEST GUST SPEED\s+(\d+|MM)")
_RE_CLI_MAX = re.compile(r"^\s*MAXIMUM\s+(-?\d+|MM)", re.M)
_RE_CLI_MIN = re.compile(r"^\s*MINIMUM\s+(-?\d+|MM)", re.M)
_RE_CLI_PCP = re.compile(r"PRECIPITATION \(IN\)\s*\n\s*(?:YESTERDAY|TODAY)\s+(\d+\.\d+|T|MM)")
_RE_PIL = re.compile(r"^(CLI[A-Z0-9]{3})\s*$", re.M)


def _cli_precip(v):
    """CLI precip value -> (inches, trace flag); trace counts as 0."""
    if v is None or v in ("M", "MM", ""):
        return None, False
    if v == "T":
        return 0.0, True
    v = float(v)
    return (0.0, True) if 0 < v < 0.005 else (round(v, 2), False)     # IEM JSON: 0.0001 = trace


def _cli_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def parse_cli_products(text: str) -> list:
    """Every CLI product in `text` (IEM AFOS / NWS API text): one dict per product with its
    climate date, issue time (from the WMO header, UTC) and values."""
    heads = [m for m in _RE_WMO.finditer(text)]
    if heads:
        segs = [text[m.start(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
                for i, m in enumerate(heads)]
    else:
        starts = [m.start() for m in _RE_CLI_DATE.finditer(text)]
        segs = [text[s: starts[i + 1] if i + 1 < len(starts) else len(text)] for i, s in enumerate(starts)]
    out = []
    for seg in segs:
        m = _RE_CLI_DATE.search(seg)
        if not m or not _MONTHS.get(m.group(1)):
            continue
        d = date(int(m.group(3)), _MONTHS[m.group(1)], int(m.group(2)))
        issued = None
        h = _RE_WMO.match(seg)
        if h:   # DDHHMM: the first day on or after the climate date with that day of month
            dd, hh, mi = (int(x) for x in h.groups())
            for k in range(8):
                c = d + timedelta(days=k)
                if c.day == dd:
                    issued = datetime(c.year, c.month, c.day, hh, mi, tzinfo=timezone.utc)
                    break

        def num(rx):
            mm = rx.search(seg)
            return None if not mm or mm.group(1) == "MM" else int(mm.group(1))
        pm = _RE_CLI_PCP.search(seg)
        pcp, trace = _cli_precip(pm.group(1) if pm else None)
        pil = _RE_PIL.search(seg)
        out.append({"date": d.isoformat(), "issued": issued, "pil": pil.group(1) if pil else None,
                    "product": None, "prelim_text": "VALID TODAY AS OF" in seg,
                    "wind_mph": num(_RE_CLI_WIND), "gust_mph": num(_RE_CLI_GUST),
                    "tmax_f": num(_RE_CLI_MAX), "tmin_f": num(_RE_CLI_MIN),
                    "precip_in": pcp, "precip_trace": trace})
    return out


def parse_cli_json(results: list) -> list:
    """IEM json/cli.py rows -> product dicts as parse_cli_products (IEM keeps the newest
    product per day; its id holds the issue time, e.g. 202610020831-KTBW-CDUS42-CLITPA)."""
    out = []
    for r in results:
        prod = r.get("product") or ""
        parts = prod.split("-")
        try:
            issued = datetime.strptime(parts[0], "%Y%m%d%H%M").replace(tzinfo=timezone.utc)
        except ValueError:
            issued = None
        pcp, trace = _cli_precip(r.get("precip"))
        out.append({"date": r["valid"], "issued": issued, "pil": parts[-1] if len(parts) > 1 else None,
                    "product": prod or None, "prelim_text": False,
                    "wind_mph": _cli_int(r.get("highest_wind_speed")),
                    "gust_mph": _cli_int(r.get("highest_gust_speed")),
                    "tmax_f": _cli_int(r.get("high")), "tmin_f": _cli_int(r.get("low")),
                    "precip_in": pcp, "precip_trace": trace})
    return out


def select_cli(products: list, utc_offset: Optional[float] = None, source: str = "") -> dict:
    """
    One CLI per climate date: the latest-issued final one, else the latest preliminary one.
    Final = issued after the LST day ended (needs utc_offset; else only the 'VALID TODAY AS OF'
    wording marks a preliminary report).
    """
    best = {}
    for p in products:
        d = date.fromisoformat(p["date"])
        prelim = p["prelim_text"]
        if utc_offset is not None:
            end = lst_window(d, utc_offset)[1]
            prelim = prelim or p["issued"] is None or p["issued"] < end.to_pydatetime()
        key = (not prelim, p["issued"] or datetime.min.replace(tzinfo=timezone.utc))
        if p["date"] not in best or key > best[p["date"]][0]:
            best[p["date"]] = (key, p, prelim)
    out = {}
    for d, (_, p, prelim) in best.items():
        out[d] = {"cli_wind_mph": p["wind_mph"], "cli_gust_mph": p["gust_mph"],
                  "cli_wind_kt": mph_to_kt(p["wind_mph"]),
                  "cli_tmax_f": p["tmax_f"], "cli_tmin_f": p["tmin_f"],
                  "cli_precip_in": p["precip_in"], "cli_precip_trace": p["precip_trace"],
                  "cli_preliminary": bool(prelim),
                  "cli_issued_utc": p["issued"].strftime("%Y-%m-%dT%H:%MZ") if p["issued"] else None,
                  "cli_product": p.get("product") or p.get("pil"),
                  "cli_via": p.get("via", source) or None}
        if out[d]["cli_wind_kt"] is None:
            out[d].pop("cli_wind_kt")
    return out


def parse_cli(text: str, utc_offset: Optional[float] = None) -> dict:
    """Parse one or more CLI text products -> {date_iso: {...}} preferring final reports."""
    return select_cli(parse_cli_products(text), utc_offset, "text")


def fetch_cli_json(icao: str, years) -> list:
    out = []
    for y in sorted(set(years)):
        r = _get(IEM_CLI_JSON, params={"station": icao, "year": y})
        out += [dict(p, via="iem_json") for p in parse_cli_json(r.json().get("results", []))]
    return out


def fetch_cli_text(pil: str, limit: int = 30, sdate: Optional[date] = None,
                   edate: Optional[date] = None) -> list:
    """IEM's raw CLI products (newest first), optionally only those issued sdate..edate."""
    params = {"pil": pil, "fmt": "text", "limit": limit}
    if sdate and edate:
        params.update(sdate=sdate.isoformat(), edate=edate.isoformat())
    r = _get(IEM_AFOS, params=params)
    return [dict(p, via="iem_text") for p in parse_cli_products(r.text)]


def fetch_cli_nws(pil: str, max_products: int = 6) -> list:
    """Backup: the NWS API's newest CLI products for the location (e.g. CLITPA -> TPA)."""
    r = _get(f"{NWS_API}/products/types/CLI/locations/{pil[3:]}", headers=NWS_HEADERS)
    out = []
    for item in r.json().get("@graph", [])[:max_products]:
        p = _get(f"{NWS_API}/products/{item['id']}", headers=NWS_HEADERS).json()
        out += [dict(q, via="nws_api") for q in parse_cli_products(p.get("productText", ""))]
    return out


def get_cli(station, first: date, last: date, now: Optional[datetime] = None) -> dict:
    """
    The CLI for each day first..last: IEM's parsed JSON, then IEM's raw text (all versions,
    preliminary included) for days still without a final report, then the NWS API if IEM failed.
    Respects the station's CLI PIL (wxc_stations: '' = no CLI).
    """
    if not station.cli_pil:
        return {}
    now = now or datetime.now(timezone.utc)
    off = station.lst_offset_hours
    days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
    want = {d.isoformat() for d in days}
    prods, failed = [], []

    def missing(sel):
        return [d for d in days if d.isoformat() not in sel or sel[d.isoformat()]["cli_preliminary"]]

    try:
        prods += [p for p in fetch_cli_json(station.icao, {d.year for d in days})
                  if p["date"] in want and p["pil"] == station.cli_pil]
    except Exception as exc:
        failed.append(f"IEM json: {exc}")
    sel = select_cli(prods, off)
    if missing(sel):
        try:   # ~2-3 products per day (preliminary, final, corrections), issued from D to D+2
            miss = missing(sel)
            n = (max(miss) - min(miss)).days + 1
            prods += [p for p in fetch_cli_text(station.cli_pil, limit=min(100, 3 * n + 6), sdate=min(miss),
                                                edate=max(miss) + timedelta(days=2))
                      if p["date"] in want]
        except Exception as exc:
            failed.append(f"IEM text: {exc}")
        sel = select_cli(prods, off)
    due = [d for d in missing(sel) if pd.Timestamp(now) > lst_window(d, off)[1] + pd.Timedelta(hours=2)]
    if due and failed:
        try:
            prods += [p for p in fetch_cli_nws(station.cli_pil) if p["date"] in want]
            sel = select_cli(prods, off)
        except Exception as exc:
            failed.append(f"NWS API: {exc}")
    if failed:
        print(f"CLI fetch problems ({station.cli_pil}): " + "; ".join(failed))
    return sel


def fetch_cf6(icao: str, years) -> dict:
    """CF6 daily max 2-min wind (mph) per date, for a sanity check of the CLI wind."""
    out = {}
    for y in sorted(set(years)):
        r = _get(IEM_CF6_JSON, params={"station": icao, "year": y})
        for row in r.json().get("results", []):
            v = row.get("max_smph")
            if isinstance(v, (int, float)):
                out[row["valid"]] = int(round(v))
    return out


# ----------------------------------------------------------------------------
# METAR + CLI -> verification values
# ----------------------------------------------------------------------------
def finalize(rec: dict, cli: Optional[dict], has_cli: bool, now: datetime,
             cf6_wind_mph: Optional[int] = None) -> dict:
    """
    Combine one day's METAR values (day_values) with its CLI: the official wind, CLI backups for
    METAR failures, the per-variable source, and whether the record is final (no pending parts).
    """
    rec = dict(rec)
    src, notes = dict(rec["source"]), list(rec.get("notes", []))
    ok = rec.get("metar_ok", {})
    cli = cli or {}
    rec.update(cli)
    final_cli = bool(cli) and not cli.get("cli_preliminary", True)
    pending = []

    # ---- wind: the final CLI, unless a METAR in the CLI's LST day is higher ----
    m = rec.get("wind_max_kt_lst")
    if "wind_max_kt_lst" not in rec:              # no LST window known: the 06Z-06Z reports
        m = rec.get("wind_max_kt_all_reports")
    cw = cli.get("cli_wind_kt")
    if final_cli and cw is not None:
        if m is not None and m > cw:
            wind, src["wind_max_kt"] = m, "metar_override"
            notes.append(f"METAR {m} kt at {rec.get('wind_max_lst_at')} is above the CLI "
                         f"{cli['cli_wind_mph']} mph ({cw} kt)")
        else:
            wind, src["wind_max_kt"] = cw, "cli"
    elif has_cli and not final_cli:
        # no final CLI yet: best guess from the preliminary CLI and the METARs so far
        wind, src["wind_max_kt"] = _max([cw, m]), "pending"
        pending.append("wind_max_kt")
    else:
        wind, src["wind_max_kt"] = m, "metar"
        if has_cli:
            notes.append("final CLI has no highest wind speed: METAR max used")
        window_over = "lst_window_utc" not in rec or pd.Timestamp(now) >= pd.Timestamp(rec["lst_window_utc"][1])
        if not window_over or not rec.get("lst_covered", True):
            src["wind_max_kt"] = "pending"
            pending.append("wind_max_kt")
    rec["wind_max_kt"] = wind
    rec["wind_source"] = {"cli": "CLI", "metar_override": "METAR (above CLI)", "metar": "METAR (no CLI)",
                          "pending": "pending (no final CLI)"}[src["wind_max_kt"]]

    # ---- CLI backups when the METARs failed ----
    for v, ck in (("tmax_f", "cli_tmax_f"), ("tmin_f", "cli_tmin_f"), ("precip_in", "cli_precip_in")):
        if ok.get(v, True):
            continue
        if final_cli and cli.get(ck) is not None:
            rec[v], src[v] = cli[ck], "cli_backup"
            if v == "precip_in":
                rec["precip_trace"] = bool(cli.get("cli_precip_trace"))
                rec["precip_source"] = "cli_backup"
        elif has_cli and not final_cli:
            pending.append(v)

    # ---- checks (informational): disagreements that may point at an observer / Board value ----
    if final_cli and src["precip_in"] != "cli_backup" and cli.get("cli_precip_in") is not None \
            and abs(cli["cli_precip_in"] - rec["precip_in"]) >= 0.005:
        notes.append(f"CLI precip {cli['cli_precip_in']:.2f} vs METAR {rec['precip_in']:.2f} (the CLI "
                     f"day is midnight-midnight LST; an NWS observer measurement would also show here)")
    if cf6_wind_mph is not None:
        rec["cf6_wind_mph"] = cf6_wind_mph
        if final_cli and cli.get("cli_wind_mph") is not None and cf6_wind_mph != cli["cli_wind_mph"]:
            notes.append(f"CF6 max wind {cf6_wind_mph} mph differs from the CLI {cli['cli_wind_mph']} mph")

    rec["source"], rec["notes"] = src, notes
    rec["pending"] = sorted(set(pending))
    rec["complete"] = bool(rec.get("complete")) or all(ok.get(v, True) or src.get(v) == "cli_backup"
                                                       for v in ("tmax_f", "tmin_f", "precip_in"))
    rec["complete"] = rec["complete"] and all(rec.get(v) is not None for v in SCORED)
    rec["final"] = rec["complete"] and not rec["pending"]
    rec["obs_method"] = OBS_METHOD
    return rec


# ----------------------------------------------------------------------------
# Public entry point
# ----------------------------------------------------------------------------
def last_complete_day(now: datetime) -> date:
    """Most recent WxChallenge day whose 06Z end (+10 min for the 0553Z ob) has passed."""
    return (now - timedelta(hours=6, minutes=10)).date() - timedelta(days=1)


def get_observations(station, days_back: int = 3, now: Optional[datetime] = None,
                     first: Optional[date] = None, last: Optional[date] = None) -> list:
    """
    Observed values for completed WxChallenge days, either the last `days_back`
    days or the explicit range [first, last]. `station` is a wxc_stations.Station.
    Returns a list of dicts (one per day).
    """
    now = now or datetime.now(timezone.utc)
    last_complete = min(last or last_complete_day(now), last_complete_day(now))
    first = first or last_complete - timedelta(days=days_back - 1)
    if first > last_complete:
        return []
    off = station.lst_offset_hours
    # the 06Z-06Z days and the CLI's LST days, plus the reports around their edges
    start = min(_utc(first, 6), lst_window(first, off)[0]) - pd.Timedelta(hours=1)
    end = max(_utc(last_complete, 30), lst_window(last_complete, off)[1]) + pd.Timedelta(minutes=30)
    end = min(pd.Timestamp(now), end)
    daily = daily_records(fetch_metars(station.icao, start.to_pydatetime(), end.to_pydatetime(),
                                       specials=True), utc_offset=off)
    daily = [r for r in daily if first.isoformat() <= r["date"] <= last_complete.isoformat()]
    if not daily:
        return []

    cli, cf6 = {}, {}
    try:
        cli = get_cli(station, first, last_complete, now)
    except Exception as exc:
        print(f"CLI fetch failed ({station.cli_pil}): {exc}")
    if station.cli_pil:
        try:
            cf6 = fetch_cf6(station.icao, {first.year, last_complete.year})
        except Exception as exc:
            print(f"CF6 fetch failed ({station.icao}): {exc}")

    fetched = now.replace(microsecond=0).isoformat()
    records = []
    for rec in daily:
        rec.update({"station": station.icao, "fetched_at_utc": fetched})
        records.append(finalize(rec, cli.get(rec["date"]), bool(station.cli_pil), now,
                                cf6.get(rec["date"])))
    return records
