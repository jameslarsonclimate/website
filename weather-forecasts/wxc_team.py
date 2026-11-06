"""
Team forecasters on the WxChallenge page's scoreboard (DISPLAY ONLY: never in the summary,
the totals of the models or the consensus).

WxChallenge has no API, but its results page (results.php) is a plain form: POSTing
year / school / city / day returns that day's table for the school, with each forecaster's
forecast, official daily error, penalty and city rank. A forecast day's table is up from that
day's morning (06Z on), with provisional verification "As of" the latest hour.

Files (under data/wxchallenge/):
  team_raw.json  what was read off results.php, per city and date (kept across cities)
  team.json      the current city's forecasters scored like the models: their forecast against
                 the scoreboard's own observed values (verification.json), so a forecaster's row
                 compares with the model rows on the same footing; the official points are kept
                 alongside for the tooltip. The page shows only the names a reader types in.

Requests stay few (results.php's robots.txt asks crawlers to stay away): at most a handful of
checks per UTC day, each one GET plus a POST per day not read yet (or not final yet).

  python wxc_team.py            check now (ignores the per-day limit) and rescore
  python wxc_team.py --score    rescore from the saved results only (no requests)
"""

import argparse
import html as _html
import json
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import wxc_verify
from wxc_verify import VARS, DATA, dumps, score_day, model_stats

URL = "https://www.wxchallenge.com/results.php"
SCHOOL = "csu"
SCHOOL_LABEL = "Colorado State Univ."
RAW = DATA / "team_raw.json"
OUT = DATA / "team.json"
UA = "Mozilla/5.0 (compatible; weather-forecasts page; team results once a day)"
PAUSE_S = 2.0              # between requests
CHECKS_PER_DAY = 3         # while today's table isn't up yet (or it's not a forecast day)
CHECK_GAP = timedelta(minutes=60)
MAX_POSTS = 10             # per check: a new city's first check reads every day so far


# ----------------------------------------------------------------------------
# results.php parsing
# ----------------------------------------------------------------------------
def _text(cell: str) -> str:
    return _html.unescape(re.sub(r"<[^>]+>", "", cell)).replace("\xa0", " ").strip()


def _num(s: str):
    s = s.strip().rstrip("*")
    if s in ("", "---", "--", "-"):
        return None
    try:
        return float(s) if "." in s else int(s)
    except ValueError:
        return None


def _rows(page: str) -> list:
    return [[_text(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S | re.I)]
            for r in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S | re.I)]


def parse_form(page: str) -> dict:
    """The form's current choices: season ("26-27"), city ("kmsp") and day number."""
    out = {"cities": []}
    for name in ("year", "city", "day"):
        m = re.search(rf'<select name="{name}".*?</select>', page, re.S | re.I)
        if not m:
            continue
        opts = re.findall(r'<option\s+(selected\s+)?value="([^"]*)"', m.group(0), re.I)
        sel = next((v for s, v in opts if s), None)
        out[name] = int(sel) if name == "day" and sel and sel.isdigit() else sel
        if name == "city":
            out["cities"] = [v for _, v in opts]
    return out


def parse_results(page: str, school: str = SCHOOL) -> dict:
    """
    One day's results table: {"day", "status", "dates": {n: {"date", "status", "final"}},
    "forecasters": {name: {...}}} (only the school's forecasters; the model rows and the
    consensus separators are skipped).
    """
    head = re.search(r"<h5>\s*Day\s+(\d+)\s*\(([^)]*)\)", page, re.I)
    out = {"day": int(head.group(1)) if head else None, "status": head.group(2).strip() if head else None,
           "dates": {}, "forecasters": {}}
    for c in _rows(page):
        if len(c) == 6 and re.fullmatch(r"\d{8}", c[0]):        # the verification list: date ... status
            m = re.search(r"Day\s+(\d+)", c[5])
            n = int(m.group(1)) if m else out["day"]
            if n is not None:
                d = f"{c[0][:4]}-{c[0][4:6]}-{c[0][6:]}"
                out["dates"][n] = {"date": d, "status": c[5], "final": c[5].lower().startswith("final")}
        elif len(c) >= 27 and c[4].lower() == school.lower() and c[3]:
            fc = dict(zip(VARS, (_num(x) for x in c[7:11])))
            if any(v is None for v in fc.values()):
                continue
            out["forecasters"][c[3]] = {
                "forecast": fc,
                "flag": c[11] or None,                     # e.g. "G" (as shown by WxChallenge)
                "cat": _num(c[5]), "absences": _num(c[6]) or 0,
                "official": {"error": dict(zip(VARS, (_num(x) for x in c[12:16]))),
                             "penalty": _num(c[16]) or 0, "points": _num(c[17]),
                             "cum_points": _num(c[23]), "rank": _num(c[0])},
            }
    return out


# ----------------------------------------------------------------------------
# fetching (few requests: see the module docstring)
# ----------------------------------------------------------------------------
def _get(session):
    r = session.get(URL, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.text


def _post(session, year, city, day, school=SCHOOL):
    r = session.post(URL, headers={"User-Agent": UA}, timeout=30,
                     data={"year": year, "school": school, "city": city, "day": str(day),
                           "submitted": "", "change": "Display"})
    r.raise_for_status()
    return r.text


def load_raw() -> dict:
    try:
        return json.loads(RAW.read_text())
    except (OSError, ValueError):
        return {}


def due(raw: dict, station: str, now: datetime) -> bool:
    """Check at most CHECKS_PER_DAY times a UTC day, an hour apart, until today's table is in."""
    today = now.date().isoformat()
    st = raw.get("stations", {}).get(station, {})
    if today in st.get("days", {}):
        return False
    checks = [datetime.fromisoformat(t) for t in raw.get("checks", []) if t[:10] == today]
    return len(checks) < CHECKS_PER_DAY and (not checks or now - max(checks) >= CHECK_GAP)


def update(station: str, now: Optional[datetime] = None, force: bool = False) -> int:
    """Read the days not saved yet (and saved days not final yet). Returns the days read."""
    import requests
    now = now or datetime.now(timezone.utc).replace(microsecond=0)
    raw = load_raw()
    if not force and not due(raw, station, now):
        return 0
    raw["checks"] = [t for t in raw.get("checks", []) if t[:10] == now.date().isoformat()] + [now.isoformat()]
    RAW.write_text(dumps(raw, indent=1))       # count the check even if it fails below
    city = station.lower()
    s = requests.Session()
    form = parse_form(_get(s))
    if city not in form.get("cities", []) or form.get("city") != city or not form.get("day"):
        print(f"  team: results.php is on {form.get('city')} day {form.get('day')}, not {city}; nothing read")
        return 0
    year, cur = form["year"], form["day"]
    st = raw.setdefault("stations", {}).setdefault(station, {"days": {}})
    st.update({"year": year, "school": SCHOOL})
    time.sleep(PAUSE_S)
    first = parse_results(_post(s, year, city, cur))
    pages = {cur: first}
    have = {v["day"]: v for v in st["days"].values() if v.get("year") == year}
    todo = [n for n, d in sorted(first["dates"].items()) if n != cur and
            (n not in have or (not have[n].get("final") and d["final"]))][:MAX_POSTS - 1]
    for n in todo:
        time.sleep(PAUSE_S)
        pages[n] = parse_results(_post(s, year, city, n))
    read = 0
    for n, p in pages.items():
        d = first["dates"].get(n) or p["dates"].get(n)
        if not d or not p["forecasters"]:
            continue
        st["days"][d["date"]] = {"day": n, "year": year, "status": d["status"], "final": d["final"],
                                 "fetched_at_utc": now.isoformat(), "forecasters": p["forecasters"]}
        read += 1
    raw["generated_at_utc"] = now.isoformat()
    RAW.write_text(dumps(raw, indent=1))
    print(f"  team: read {read} day(s) of {SCHOOL} results for {city} (day {cur} is {first['status']})")
    return read


# ----------------------------------------------------------------------------
# scoring for the page (no requests)
# ----------------------------------------------------------------------------
def _score(fc: dict, ob: dict, rec: dict) -> Optional[dict]:
    s = score_day(fc, ob)
    if not s:
        return None
    pen = (rec.get("official") or {}).get("penalty") or 0
    if pen:
        s["points"] = round(s["points"] + pen, 1)
        s["penalty"] = pen
    if rec.get("flag"):
        s["flag"] = rec["flag"]
    return s


def scores(raw: dict, verif: dict) -> dict:
    """team.json: each forecaster's days scored against the scoreboard's observed values."""
    station = verif.get("station")
    st = (raw.get("stations") or {}).get(station) or {}
    team = st.get("days") or {}
    days = [d for d in verif.get("days") or [] if d.get("models")]
    people = {}
    pseudo = []
    for d in days:
        t = team.get(d["date"])
        row = {}
        for name, rec in ((t or {}).get("forecasters") or {}).items():
            s = _score(rec["forecast"], d["obs"], rec)
            if not s:
                continue
            off = rec.get("official") or {}
            if t.get("final") and off.get("points") is not None:
                s["official_points"] = off["points"]
            if off.get("rank") is not None:
                s["rank"] = off["rank"]
            s["day"] = t.get("day")
            row[name] = s
            people.setdefault(name, {"days": {}})["days"][d["date"]] = s
        pseudo.append({"date": d["date"], "models": row})
    for name, st_ in model_stats(pseudo).items():     # same decay weights as the model rows
        people[name]["summary"] = st_
    today = None
    T = verif.get("today")
    if T and T.get("obs") and T["obs"].get("wind_max_kt") is not None:
        t = team.get(T["date"])
        if t:
            today = {"date": T["date"], "status": t.get("status"), "forecasters": {}}
            for name, rec in t["forecasters"].items():
                s = _score(rec["forecast"], T["obs"], rec)
                if s:
                    s["day"] = t.get("day")
                    today["forecasters"][name] = s
                    people.setdefault(name, {"days": {}})
    return {"station": station, "school": st.get("school", SCHOOL), "school_label": SCHOOL_LABEL,
            "season": st.get("year"), "fetched_at_utc": raw.get("generated_at_utc"),
            "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "note": "display only; scored against this page's observed values like the models "
                    "(official WxChallenge points in official_points once final)",
            "forecasters": people, "today": today}


def write_scores() -> Optional[dict]:
    if not wxc_verify.VERIF.exists():
        return None
    out = scores(load_raw(), json.loads(wxc_verify.VERIF.read_text()))
    OUT.write_text(dumps(out, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--score", action="store_true", help="rescore only, no requests")
    args = ap.parse_args()
    if not args.score:
        station = json.loads(wxc_verify.VERIF.read_text())["station"]
        update(station, force=True)
    out = write_scores()
    if out:
        print(f"Wrote {OUT}: {len(out['forecasters'])} forecaster(s)")


if __name__ == "__main__":
    main()
