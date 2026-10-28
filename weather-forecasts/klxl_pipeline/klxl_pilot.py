"""
Data for the KLXL pilot weather page (weather-forecasts/klxl/, pilot.js): data/klxl/pilot.json.

The past 24 h observed and the next 7 days forecast, hour by hour, plus a flight outlook per
local day, the current METAR and the nearest TAFs (KLXL has none). A planning aid only.

Sources
  observations   KLXL METARs, last 26 h (aviationweather.gov data API)
  TAFs           KBRD (Brainerd) and KSTC (St. Cloud), same API
  ceiling, vis   NBM text guidance from AWS (wxc_nbm_text, unchanged WxChallenge module): NBH hourly
                 to 25 h, then NBS 3-hourly to ~72 h. Past that NBM has no ceiling or visibility, so
                 the hours have no flight category ("none") and the day outlook uses cloud cover
  surface        NBM via Open-Meteo (ncep_nbm_conus), hourly 8 days: wind, gusts, temp, dewpoint,
                 sky cover, precip chance and type (weather code); NBS 3-h thunder chance on top
  aloft          GFS via Open-Meteo (gfs_seamless): low / mid / high cloud, freezing level, winds at
                 925 / 850 / 700 mb (~2.5k / 5k / 10k ft MSL), 700 mb temp, surface pressure
                 (density altitude)
  sun            NOAA sunrise / sunset / civil twilight algorithm

Writes data/klxl/pilot.json only (pushed by getForecast_klxl.sh pilot). Never touches the
WxChallenge files.

  python klxl_pipeline/klxl_pilot.py [--out PATH]
"""

import argparse
import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(1, str(Path(__file__).resolve().parent.parent))   # unchanged WxChallenge modules

import pandas as pd
import requests

import wxc_nbm_text

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "klxl" / "pilot.json"

ICAO, LAT, LON, ELEV_FT = "KLXL", 45.9491, -94.347, 1122
TZ = ZoneInfo("America/Chicago")
TAF_SITES = "KBRD,KSTC"
RWYS = [("13", 131), ("31", 311), ("18", 181), ("36", 1)]   # true headings
XW_LIMIT, GUST_LIMIT = 10, 20      # outlook limits (kt): typical training / student limits
SKY_OK = 70                        # past NBM's ceiling guidance: sky cover (%) below this counts as VFR-likely
PAST_H, AHEAD_H = 24, 168
UA = {"User-Agent": "klxl-pilot-page (personal weather page)"}
AWC = "https://aviationweather.gov/api/data"
OM = "https://api.open-meteo.com/v1/forecast"
M_TO_FT = 3.28084


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def cat_of(ceil, vis):
    """Flight category from ceiling (ft AGL, None = no ceiling) and visibility (SM)."""
    c = 99999 if ceil is None else ceil
    v = 99 if vis is None else vis
    if c < 500 or v < 1:
        return "LIFR"
    if c < 1000 or v < 3:
        return "IFR"
    if c <= 3000 or v <= 5:
        return "MVFR"
    return "VFR"


def local(t):
    return t.astimezone(TZ)


def hfmt(t):
    lt = local(t)
    return f"{lt.hour % 12 or 12}{'a' if lt.hour < 12 else 'p'}"


def tfmt(t):
    lt = local(t)
    return f"{lt.hour % 12 or 12}:{lt.minute:02d}{'a' if lt.hour < 12 else 'p'}"


def crosswind(wdir, spd, gst):
    """(runway, crosswind, gust crosswind, headwind) for the runway with the least gust
    crosswind and no tailwind; ('—', 0, 0, 0) when calm or variable."""
    if wdir is None or not spd:
        return ("—", 0, 0, 0)
    best = None
    for rid, hdg in RWYS:
        ang = math.radians(wdir - hdg)
        head = spd * math.cos(ang)
        if head < -0.5:
            continue
        xw, xg = abs(spd * math.sin(ang)), abs((gst or spd) * math.sin(ang))
        if best is None or xg < best[2]:
            best = (rid, round(xw), round(xg), round(head))
    return best or ("—", 0, 0, 0)


def press_alt(p_hpa):
    return (1 - (p_hpa / 1013.25) ** 0.190284) * 145366.45


def dens_alt(pa_ft, tc):
    return pa_ft + 118.8 * (tc - (15 - 1.98 * pa_ft / 1000))


def dist_nm(lat, lon):
    p1, p2 = math.radians(LAT), math.radians(lat)
    dl = math.radians(lon - LON)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    km = 6371 * 2 * math.asin(math.sqrt(a))
    brg = (math.degrees(math.atan2(math.sin(dl) * math.cos(p2),
                                   math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl))) + 360) % 360
    return round(km / 1.852), "N NE E SE S SW W NW".split()[round(brg / 45) % 8]


# ----------------------------------------------------------------------------
# sun (NOAA sunrise/sunset algorithm)
# ----------------------------------------------------------------------------
def sun_event(day, zenith, rising):
    n = day.timetuple().tm_yday
    lng_h = LON / 15
    t = n + ((6 if rising else 18) - lng_h) / 24
    M = 0.9856 * t - 3.289
    L = (M + 1.916 * math.sin(math.radians(M)) + 0.020 * math.sin(math.radians(2 * M)) + 282.634) % 360
    RA = math.degrees(math.atan(0.91764 * math.tan(math.radians(L)))) % 360
    RA = (RA + (L // 90) * 90 - (RA // 90) * 90) / 15
    sd = 0.39782 * math.sin(math.radians(L))
    cd = math.cos(math.asin(sd))
    ch = (math.cos(math.radians(zenith)) - sd * math.sin(math.radians(LAT))) / (cd * math.cos(math.radians(LAT)))
    H = (360 - math.degrees(math.acos(ch))) if rising else math.degrees(math.acos(ch))
    T = H / 15 + RA - 0.06571 * t - 6.622
    UT = (T - lng_h) % 24
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc) + timedelta(hours=UT)


def sun_for_local_day(ld):
    """Sunrise (sr), sunset (ss), civil dawn (cd) and dusk (ck) of local date `ld`, in UTC."""
    out = {}
    for key, zen, rising in (("sr", 90.833, True), ("ss", 90.833, False), ("cd", 96, True), ("ck", 96, False)):
        ev = sun_event(ld, zen, rising)
        while local(ev).date() > ld:
            ev -= timedelta(days=1)
        while local(ev).date() < ld:
            ev += timedelta(days=1)
        out[key] = ev
    return out


# ----------------------------------------------------------------------------
# fetching
# ----------------------------------------------------------------------------
def get_json(url, params):
    r = requests.get(url, params=params, headers=UA, timeout=60)
    r.raise_for_status()
    return r.json()


def open_meteo(model, hourly):
    d = get_json(OM, dict(latitude=LAT, longitude=LON, models=model, hourly=hourly, timezone="UTC",
                          wind_speed_unit="kn", forecast_days=8, past_days=1))
    if "error" in d or "hourly" not in d:
        raise RuntimeError(f"Open-Meteo {model}: {d.get('reason', d)}")
    units = d.get("hourly_units", {})
    h = d["hourly"]
    idx = {datetime.fromisoformat(t).replace(tzinfo=timezone.utc): i for i, t in enumerate(h["time"])}
    return h, idx, units


def nbm_text(prod):
    """{valid time (UTC): row} of the newest posted NBM text cycle, and its init time."""
    df = wxc_nbm_text.newest(ICAO, prod)
    if df.empty:
        return {}, None
    rows = {pd.Timestamp(t).to_pydatetime(): r for t, r in zip(df["ftime"], df.to_dict("records"))}
    return rows, pd.Timestamp(df["runtime"].iloc[0]).to_pydatetime()


def num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) else f


# ----------------------------------------------------------------------------
# building the page data
# ----------------------------------------------------------------------------
def build(now):
    hour0 = now.replace(minute=0, second=0, microsecond=0)
    start = hour0 - timedelta(hours=PAST_H)
    N = PAST_H + AHEAD_H
    hours = [start + timedelta(hours=i) for i in range(N)]
    hidx = lambda t: (t - start).total_seconds() / 3600   # noqa: E731
    notes = []

    # ---- observations ----
    obs, metars = {}, []
    try:
        metars = get_json(f"{AWC}/metar", {"ids": ICAO, "hours": PAST_H + 2, "format": "json"}) or []
    except Exception as exc:
        notes.append(f"METARs unavailable ({type(exc).__name__})")
    for m in sorted(metars, key=lambda m: m["obsTime"]):
        t = datetime.fromtimestamp(m["obsTime"], timezone.utc)
        ceil = None
        for c in m.get("clouds") or []:
            if c.get("cover") in ("BKN", "OVC", "OVX") and c.get("base") is not None:
                ceil = c["base"]
                break
        if m.get("vertVis"):
            ceil = m["vertVis"]
        v = m.get("visib")
        vis = 10.0 if v in ("10+", "6+", None) else float(str(v).rstrip("+"))
        wdir = m.get("wdir") if isinstance(m.get("wdir"), (int, float)) else None
        obs[t.replace(minute=0, second=0, microsecond=0)] = dict(   # the hour's last report
            ceil=ceil, vis=min(vis, 10), wdir=wdir, wspd=m.get("wspd"), wgst=m.get("wgst"),
            tc=m.get("temp"), dc=m.get("dewp"), cat=m.get("fltCat") or cat_of(ceil, vis),
            raw=m["rawOb"], altim=m.get("altim"), t=t)

    # ---- NBM text: ceiling and visibility (hundreds of ft, -88 = none; tenths of a mile) ----
    nbh, nbh_init = nbm_text("nbh")
    nbs, nbs_init = nbm_text("nbs")
    if not nbh:
        notes.append("NBM hourly text unavailable")
    ceilvis = {}

    def cv(r):
        c, v = num(r.get("cig")), num(r.get("vis"))
        return (None if c is None or c < 0 else c * 100, None if v is None else min(v / 10, 10))
    for t, r in nbs.items():                  # 3-hourly rows stand for the hour either side
        for dh in (-1, 0, 1):
            ceilvis[t + timedelta(hours=dh)] = (*cv(r), "nbs")
    for t, r in nbh.items():                  # hourly wins where both have the hour
        ceilvis[t] = (*cv(r), "nbh")
    tstorm = {}
    for t, r in nbs.items():                  # T03: thunder chance in the 3 h ending at t
        for dh in (-2, -1, 0):
            if num(r.get("t03")) is not None:
                tstorm[t + timedelta(hours=dh)] = num(r.get("t03"))

    # ---- Open-Meteo: NBM surface, GFS aloft ----
    sfc, si, _ = open_meteo("ncep_nbm_conus", "temperature_2m,dew_point_2m,wind_speed_10m,wind_direction_10m,"
                            "wind_gusts_10m,cloud_cover,precipitation_probability,weather_code")
    up, ui, uu = open_meteo("gfs_seamless", "cloud_cover_low,cloud_cover_mid,cloud_cover_high,freezing_level_height,"
                            "surface_pressure,wind_speed_925hPa,wind_direction_925hPa,wind_speed_850hPa,"
                            "wind_direction_850hPa,wind_speed_700hPa,wind_direction_700hPa,temperature_700hPa,"
                            "geopotential_height_925hPa,geopotential_height_850hPa,geopotential_height_700hPa")
    ft = (lambda v: v * M_TO_FT) if uu.get("freezing_level_height", "m") == "m" else (lambda v: v)

    def S(var, t):
        i = si.get(t)
        return None if i is None else num(sfc[var][i])

    def U(var, t):
        i = ui.get(t)
        return None if i is None else num(up[var][i])

    def ptype(code, ts):
        if ts is not None and ts >= 20:
            return "TS"
        if code is None:
            return ""
        code = int(code)
        if code in (95, 96, 99):
            return "TS"
        if code in (56, 57, 66, 67):
            return "FZ"
        if code in (71, 73, 75, 77, 85, 86):
            return "SN"
        return "RA" if code in (51, 53, 55, 61, 63, 65, 80, 81, 82) else ""

    h = {k: [] for k in ("t lbl dayStart cat src ceil vis wdir wspd wgst xw xwg rwy tc dc da sky cl cm ch "
                         "pop pt fzl a1d a1s a2d a2s a3d a3s a3t").split()}
    r0 = lambda v, n=0: None if v is None else (round(v) if n == 0 else round(v, n))   # noqa: E731
    for t in hours:
        o = obs.get(t) if t <= hour0 else None
        lt = local(t)
        h["t"].append(lt.strftime("%a %b %-d, ") + tfmt(t))
        h["lbl"].append(hfmt(t))
        h["dayStart"].append(1 if lt.hour == 0 else 0)
        if o:
            ceil, vis, src, cat = o["ceil"], o["vis"], "obs", o["cat"]
            wdir, wspd, wgst, tc, dc = o["wdir"], o["wspd"], o["wgst"], o["tc"], o["dc"]
        else:
            if t > hour0 and t in ceilvis:
                ceil, vis, src = ceilvis[t]
                cat = cat_of(ceil, vis)
            else:
                ceil, vis, src, cat = None, None, ("none" if t > hour0 else "gap"), None
            wdir, wspd, wgst = S("wind_direction_10m", t), S("wind_speed_10m", t), S("wind_gusts_10m", t)
            tc, dc = S("temperature_2m", t), S("dew_point_2m", t)
            if wgst is not None and wspd is not None and (wgst < wspd + 5 or wgst < 12):
                wgst = None                      # NBM gust barely above the wind: not a gust
        wdir = None if wdir is None else int(round(wdir / 10) * 10) % 360
        wspd, wgst = r0(wspd), r0(wgst)
        rwy, xw, xwg, _ = crosswind(wdir, wspd, wgst)
        p = U("surface_pressure", t)
        if o and o.get("altim"):
            pa = ELEV_FT + (29.92 - o["altim"] * 0.02953) * 1000
        else:
            pa = press_alt(p) if p else ELEV_FT
        h["cat"].append(cat)
        h["src"].append(src)
        h["ceil"].append(r0(ceil))
        h["vis"].append(r0(vis, 1))
        h["wdir"].append(wdir)
        h["wspd"].append(wspd)
        h["wgst"].append(wgst)
        h["xw"].append(xw)
        h["xwg"].append(xwg)
        h["rwy"].append(rwy)
        h["tc"].append(r0(tc, 1))
        h["dc"].append(r0(dc, 1))
        h["da"].append(None if tc is None else int(round(dens_alt(pa, tc) / 10) * 10))
        h["sky"].append(r0(S("cloud_cover", t)))
        for k, v in (("cl", "low"), ("cm", "mid"), ("ch", "high")):
            h[k].append(r0(U(f"cloud_cover_{v}", t)))
        pop = S("precipitation_probability", t)
        h["pop"].append(int(pop or 0))
        h["pt"].append(ptype(S("weather_code", t), tstorm.get(t)))
        fz = U("freezing_level_height", t)
        h["fzl"].append(None if fz is None else int(round(ft(fz) / 100) * 100))
        for n, lev in (("1", "925"), ("2", "850"), ("3", "700")):
            d_, s_ = U(f"wind_direction_{lev}hPa", t), U(f"wind_speed_{lev}hPa", t)
            h[f"a{n}d"].append(None if d_ is None else int(round(d_ / 10) * 10) % 360)
            h[f"a{n}s"].append(r0(s_))
        h["a3t"].append(r0(U("temperature_700hPa", t)))

    lev_ft = []
    for lev in ("925", "850", "700"):
        z = [U(f"geopotential_height_{lev}hPa", t) for t in hours]
        z = [v for v in z if v is not None]
        lev_ft.append(int(round(ft(sum(z) / len(z)) / 500) * 500) if z else None)

    # ---- night / twilight shading ----
    shade = []
    d0 = local(start).date() - timedelta(days=1)
    for k in range(10):
        ld = d0 + timedelta(days=k)
        s, s2 = sun_for_local_day(ld), sun_for_local_day(ld + timedelta(days=1))
        shade += [{"a": hidx(s["ss"]), "b": hidx(s["ck"]), "k": "civil"},
                  {"a": hidx(s["ck"]), "b": hidx(s2["cd"]), "k": "night"},
                  {"a": hidx(s2["cd"]), "b": hidx(s2["sr"]), "k": "civil"}]
    shade = [{"a": round(max(p["a"], 0), 2), "b": round(min(p["b"], N), 2), "k": p["k"]}
             for p in shade if p["b"] > 0 and p["a"] < N]

    # ---- daily flight outlook ----
    days = []
    today = local(now).date()
    if now > sun_for_local_day(today)["ss"]:      # after sunset: the outlook starts tomorrow
        today += timedelta(days=1)
    for k in range(7):
        ld = today + timedelta(days=k)
        s = sun_for_local_day(ld)
        idx = [i for i, t in enumerate(hours) if local(t).date() == ld]
        if not idx:
            continue
        dl = [i for i in idx if s["sr"] <= hours[i] + timedelta(minutes=30) <= s["ss"]] or idx
        nocat = [i for i in dl if h["cat"][i] is None]

        def vfr(i):
            if h["cat"][i] is not None:
                return h["cat"][i] == "VFR"
            return h["src"][i] == "none" and (h["sky"][i] or 0) < SKY_OK

        def good(i):
            return (vfr(i) and h["xw"][i] <= XW_LIMIT and (h["wgst"][i] or 0) <= GUST_LIMIT
                    and h["pop"][i] < 50 and h["pt"][i] != "TS")
        run, best, cur = 0, (0, None, None), None
        for i in dl:
            if good(i):
                cur = cur if run else i
                run += 1
                if run > best[0]:
                    best = (run, cur, i)
            else:
                run = 0
        outlook = "Good" if best[0] >= 6 else "Fair" if best[0] >= 3 else "Poor"
        reasons = []
        bad = [i for i in dl if not vfr(i)]
        if nocat and len(nocat) > len(dl) / 2:
            sky = sum(h["sky"][i] or 0 for i in dl) / len(dl)
            reasons.append("Mostly cloudy" if sky >= SKY_OK else "Partly cloudy" if sky > 30 else "Mostly clear")
        elif len(bad) > len(dl) / 3:
            cats = [h["cat"][i] for i in bad if h["cat"][i]]
            worst = min(cats, key=["LIFR", "IFR", "MVFR", "VFR"].index) if cats else None
            reasons.append("Below VFR all daylight hrs" if len(bad) == len(dl)
                           else f"Below VFR {len(bad)} of {len(dl)} daylight hrs")
            if worst in ("IFR", "LIFR"):
                reasons.append(f"{worst} at times")
        mxg = max((h["wgst"][i] or h["wspd"][i] or 0) for i in dl)
        if mxg > GUST_LIMIT:
            reasons.append(f"gusts to {mxg} kt")
        mxw = max(h["xw"][i] for i in dl)
        if mxw > XW_LIMIT:
            reasons.append(f"crosswind {mxw} kt")
        pmax = max(h["pop"][i] for i in idx)
        types = {h["pt"][i] for i in idx if h["pop"][i] >= 30} - {""}
        if pmax >= 50:
            reasons.append(("T-storms" if "TS" in types else "snow" if "SN" in types else "rain") + f" {pmax}%")
        if not reasons:
            reasons.append("VFR, light winds")
        srcs = {h["src"][i] for i in dl}
        ceils = [h["ceil"][i] for i in dl if h["ceil"][i] is not None]
        viss = [h["vis"][i] for i in dl if h["vis"][i] is not None]
        xw_i = max(dl, key=lambda i: (h["xwg"][i], h["xw"][i]))
        mid = [i for i in dl if 11 <= local(hours[i]).hour <= 15] or dl
        a1 = mid[len(mid) // 2]
        fz = [h["fzl"][i] for i in idx if h["fzl"][i] is not None]
        das = [h["da"][i] for i in dl if h["da"][i] is not None]
        aloft = lambda d_, s_: "—" if d_ is None or s_ is None else f"{d_ or 360:03d}@{s_}"   # noqa: E731
        days.append(dict(
            name=local(hours[idx[0]]).strftime("%a"), date=local(hours[idx[0]]).strftime("%b %-d"),
            long=local(hours[idx[0]]).strftime("%A, %B %-d"),
            first=idx[0], last=idx[-1], dlFirst=dl[0], dlLast=dl[-1],
            outlook=outlook, why=reasons[0], why2=", ".join(reasons[1:3]),
            win="—" if not best[1] else f"{hfmt(hours[best[1]])}–{hfmt(hours[best[2]] + timedelta(hours=1))}",
            winH=best[0], dlH=len(dl),
            strip=[h["cat"][i] for i in dl], stripSrc=[h["src"][i] for i in dl],
            conf=("low" if "none" in srcs else "med" if "nbs" in srcs else "high"),
            minCeil=min(ceils) if ceils else None, ceilKnown=not nocat,
            minVis=min(viss) if viss else None,
            maxWind=max(h["wspd"][i] or 0 for i in dl), maxGust=max((h["wgst"][i] or 0) for i in dl) or None,
            maxXw=h["xw"][xw_i], maxXwg=h["xwg"][xw_i], xwRwy=h["rwy"][xw_i],
            pop=pmax, ptype=("TS" if "TS" in types else "SN" if "SN" in types else "FZ" if "FZ" in types
                             else "RA" if types else ""),
            fzlMin=min(fz) if fz else None,
            aloft=aloft(h["a1d"][a1], h["a1s"][a1]), aloft2=aloft(h["a2d"][a1], h["a2s"][a1]),
            daMax=max(das) if das else None,
            sr=tfmt(s["sr"]), ss=tfmt(s["ss"]), civDawn=tfmt(s["cd"]), civDusk=tfmt(s["ck"]),
            curStart=tfmt(s["ss"] + timedelta(hours=1)),
            curEnd=tfmt(sun_for_local_day(ld + timedelta(days=1))["sr"] - timedelta(hours=1)),
        ))

    # ---- TAFs ----
    tafs = []
    try:
        raw_tafs = get_json(f"{AWC}/taf", {"ids": TAF_SITES, "format": "json"}) or []
    except Exception as exc:
        raw_tafs = []
        notes.append(f"TAFs unavailable ({type(exc).__name__})")
    for tf in sorted(raw_tafs, key=lambda x: TAF_SITES.split(",").index(x["icaoId"])
                     if x["icaoId"] in TAF_SITES else 9):
        nm, dr = dist_nm(tf["lat"], tf["lon"])
        groups = []
        for g in tf.get("fcsts") or []:
            ceil = next((c["base"] for c in g.get("clouds") or [] if c.get("cover") in ("BKN", "OVC", "OVX")), None)
            if g.get("vertVis"):
                ceil = g["vertVis"]
            v = g.get("visib")
            vis = 10 if v in ("6+", None) else float(str(v).rstrip("+"))
            a = datetime.fromtimestamp(g["timeFrom"], timezone.utc)
            b = datetime.fromtimestamp(g["timeTo"], timezone.utc)
            groups.append(dict(kind=g.get("fcstChange") or "BASE", a=round(hidx(a), 2), b=round(hidx(b), 2),
                               from_=tfmt(a), to=tfmt(b), cat=cat_of(ceil, vis)))
        raw = re.sub(r" (FM\d{6}|TEMPO|BECMG|PROB\d\d)", r"\n  \1", tf["rawTAF"])
        tafs.append(dict(id=tf["icaoId"], name=tf.get("name") or "", nm=nm, dir=dr, raw=raw, groups=groups,
                         issued=tfmt(datetime.fromisoformat(tf["issueTime"].replace("Z", "+00:00")))))

    # ---- now ----
    nowd = None
    if metars:
        lm = max(metars, key=lambda m: m["obsTime"])
        mt = datetime.fromtimestamp(lm["obsTime"], timezone.utc)
        lo = obs[mt.replace(minute=0, second=0, microsecond=0)]
        rwy, xw, xwg, head = crosswind(lo["wdir"], lo["wspd"], lo["wgst"])
        altin = round(lo["altim"] * 0.02953, 2) if lo.get("altim") else None
        da = None
        if altin is not None and lo["tc"] is not None:
            da = int(round(dens_alt(ELEV_FT + (29.92 - altin) * 1000, lo["tc"]) / 10) * 10)
        cover = next((c["cover"] for c in lm.get("clouds") or [] if c.get("base") == lo["ceil"]), "")
        nowd = dict(
            raw=lm["rawOb"], cat=lo["cat"], time=tfmt(mt), obsUtc=mt.strftime("%Y-%m-%dT%H:%MZ"),
            wind=("Calm" if not lo["wspd"] else ("VRB" if lo["wdir"] is None else f"{lo['wdir'] or 360:03d}°")
                  + f" at {lo['wspd']} kt" + (f" G{lo['wgst']}" if lo["wgst"] else "")),
            vis=("10+" if lo["vis"] >= 10 else f"{lo['vis']:g}") + " SM",
            ceil="None" if lo["ceil"] is None else f"{cover or 'VV'} {lo['ceil']:,} ft",
            temp="—" if lo["tc"] is None else f"{lo['tc']:g}°C / {lo['dc']:g}°C",
            spread=None if lo["tc"] is None or lo["dc"] is None else round(lo["tc"] - lo["dc"], 1),
            altim="—" if altin is None else f"{altin:.2f}", da="—" if da is None else f"{da:,} ft",
            rwy=rwy, xw=xw, head=head)

    return dict(
        station=dict(id=ICAO, name="Little Falls/Morrison County – Lindbergh Field", elev=ELEV_FT,
                     rwys="13/31 4,010×75 · 18/36 2,858×60", wfo="MPX"),
        generated_at_utc=now.replace(microsecond=0).isoformat(),
        updated=local(now).strftime("%a %b %-d, ") + tfmt(now) + " " + local(now).strftime("%Z"),
        nbmInit=None if nbh_init is None else f"{nbh_init:%H}Z",
        nbsInit=None if nbs_init is None else f"{nbs_init:%H}Z",
        startUtc=start.strftime("%Y-%m-%dT%H:%MZ"), N=N, nowIdx=round(hidx(now), 2),
        xwLimit=XW_LIMIT, gustLimit=GUST_LIMIT, skyOk=SKY_OK,
        levFt=lev_ft, shade=shade, h=h, days=days, tafs=tafs, now=nowd, notes=notes,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    data = build(now)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, separators=(",", ":"), allow_nan=False))
    tmp.replace(out)
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB): NBH {data['nbmInit']}, NBS {data['nbsInit']}, "
          f"{len(data['tafs'])} TAFs, now {data['now'] and data['now']['cat']}"
          + (f"; notes: {'; '.join(data['notes'])}" if data["notes"] else ""))
    for d in data["days"]:
        print(f"  {d['name']} {d['date']}: {d['outlook']:4s} {d['why']}{' | ' + d['why2'] if d['why2'] else ''}"
              f"  (window {d['win']}, conf {d['conf']})")


if __name__ == "__main__":
    main()
