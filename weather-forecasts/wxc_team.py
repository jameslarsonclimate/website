"""
WxChallenge's own results (results.php): the official observed values, and the team's forecasts
for the page's scoreboard.

WxChallenge has no API, but its results page is a plain form. POSTing year / school / city / day
returns that day's table for the school: each forecaster's forecast, daily error, penalty and
rank, plus the list of days 1..N with WxChallenge's observed values ("Final Day N" once final,
"As of 15Z" for today). POST only: a GET with the same query returns no table.

Asking for a day past the latest is NOT a shortcut while a city is in progress: the page comes
back with no "Day N (...)" heading and no table. Only once the city is over does it clamp to the
city's last day. So the day to ask for is counted from the city's first day (verification.json's
city_start; WxChallenge days are Tue-Fri, CITY_DAYS per city), and the check steps down a day at
a time when that page is empty: before 06Z today's table isn't up yet, and after a break week the
count overshoots. Normally that is one POST for today's table and every earlier day's values.

One request a day, in the morning: today's team forecasts (submitted by 00Z, public once the day
starts) and the official values for yesterday and before. A second (third) check, two hours
later, only while yesterday isn't final on WxChallenge yet. results.php's robots.txt asks crawlers
to stay away, so this stays this small. (Days missed while the laptop was off are read one POST
each on the next check.)

What it does with them:
  * official values -> observations.jsonl (wxc_verify.set_official): where WxChallenge's final
    value differs from ours, theirs is used for all scoring; ours is kept as "own".
  * team forecasts -> team_raw.json (kept across cities) and team.json, the current city's
    forecasters scored like the models (DISPLAY ONLY: never in the summary, the models' totals or
    the consensus). The page shows only the names a reader types in.

  python wxc_team.py            check now (ignores the once-a-day limit) and rescore
  python wxc_team.py --score    rescore from the saved results only (no requests)
"""

import argparse
import html as _html
import json
import re
import time
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import wxc_verify
from wxc_verify import VARS, DATA, dumps, score_day, model_stats

URL = "https://www.wxchallenge.com/results.php"
SCHOOL = "csu"
SCHOOL_LABEL = "Colorado State Univ."
RAW = DATA / "team_raw.json"
OUT = DATA / "team.json"
UA = "Mozilla/5.0 (compatible; weather-forecasts page; team results once a day)"
LAST_DAY = 16              # the form's last day number (an in-progress city answers days past
                           # the latest with an empty page; only a finished city clamps)
CITY_DAYS = 8              # forecast days per city (two Tue-Fri weeks)
STEP_DOWN = 4              # extra POSTs, one day back each, when the expected day is empty
PAUSE_S = 2.0              # between requests (catch-up only)
CHECKS_PER_DAY = 3         # only while yesterday isn't final on WxChallenge yet
CHECK_GAP = timedelta(hours=2)
MAX_POSTS = 10             # per check, catching up on missed days


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


def parse_results(page: str, school: str = SCHOOL) -> dict:
    """
    One day's results table: {"day", "status", "dates": {n: {"date", "status", "final", "obs",
    "review"}}, "forecasters": {name: {...}}} (only the school's forecasters; the model rows and
    the consensus separators are skipped).
    """
    head = re.search(r"<h5>\s*Day\s+(\d+)\s*\(([^)]*)\)", page, re.I)
    out = {"day": int(head.group(1)) if head else None, "status": head.group(2).strip() if head else None,
           "dates": {}, "forecasters": {}}
    for c in _rows(page):
        if len(c) == 6 and re.fullmatch(r"\d{8}", c[0]):        # the day list: date, values, status
            m = re.search(r"Day\s+(\d+)", c[5])
            n = int(m.group(1)) if m else out["day"]
            if n is not None:
                out["dates"][n] = {"date": f"{c[0][:4]}-{c[0][4:6]}-{c[0][6:]}", "status": c[5],
                                   "final": c[5].lower().startswith("final"),
                                   "obs": dict(zip(VARS, (_num(x) for x in c[1:5]))),
                                   "review": any("*" in x for x in c[1:5])}    # "under review"
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
                             "cum_points": _num(c[23]), "rank": _num(c[0]), "prev_rank": _num(c[1])},
            }
    return out


# ----------------------------------------------------------------------------
# fetching (one request a day: see the module docstring)
# ----------------------------------------------------------------------------
def season(d: date) -> str:
    """The form's season, e.g. "26-27" for fall 2026 through spring 2027."""
    y = d.year if d.month >= 7 else d.year - 1
    return f"{y % 100:02d}-{(y + 1) % 100:02d}"


def _post(session, year, city, day, school=SCHOOL):
    r = session.post(URL, headers={"User-Agent": UA}, timeout=30,
                     data={"year": year, "school": school, "city": city, "day": str(day),
                           "submitted": "", "change": "Display"})
    r.raise_for_status()
    return r.text


def _city_start(station: str) -> Optional[date]:
    """The current city's first forecast day (verification.json), or None if unknown."""
    try:
        v = json.loads(wxc_verify.VERIF.read_text())
        if v.get("station") != station or not v.get("city_start"):
            return None
        return date.fromisoformat(v["city_start"])
    except (OSError, ValueError, TypeError, AttributeError):
        return None


def expected_day(city_start: Optional[date], today: date) -> Optional[int]:
    """WxChallenge day number for today: Tue-Fri dates from city_start through today (0 before the
    city starts, None when the start is unknown). Overshoots after a break week; see fetch_latest."""
    if city_start is None:
        return None
    if today < city_start:
        return 0
    return sum(1 for i in range((today - city_start).days + 1)
               if (city_start + timedelta(days=i)).weekday() in (1, 2, 3, 4))


def fetch_latest(session, year: str, city: str, guess: Optional[int]) -> dict:
    """
    The latest day's parsed page. Asks for the expected day (CITY_DAYS when unknown, capped at
    CITY_DAYS) and steps down a day while the page has no table: at most STEP_DOWN extra POSTs
    when the day is known, down to day 1 when it isn't. guess == 0 (city not started): no POST.
    """
    if guess == 0:
        return parse_results("")
    start = min(guess or CITY_DAYS, CITY_DAYS)
    lowest = max(1, start - STEP_DOWN) if guess else 1
    page = parse_results("")
    for i, day in enumerate(range(start, lowest - 1, -1)):
        if i:
            time.sleep(PAUSE_S)
        page = parse_results(_post(session, year, city, day))
        if page["day"] and page["dates"]:
            return page
    return page


def load_raw() -> dict:
    try:
        return json.loads(RAW.read_text())
    except (OSError, ValueError):
        return {}


def due(raw: dict, station: str, now: datetime) -> bool:
    """Once a UTC day; again (2 h apart, 3 checks at most) only while yesterday isn't final."""
    today = now.date().isoformat()
    if (raw.get("stations") or {}).get(station, {}).get("done_for") == today:
        return False
    checks = [datetime.fromisoformat(t) for t in raw.get("checks", []) if t[:10] == today]
    return len(checks) < CHECKS_PER_DAY and (not checks or now - max(checks) >= CHECK_GAP)


def _save_day(st: dict, n: int, d: dict, page: dict, year: str, now: datetime):
    st["days"][d["date"]] = {"day": n, "year": year, "status": d["status"], "final": d["final"],
                             "fetched_at_utc": now.isoformat(), "forecasters": page["forecasters"]}


def update(station: str, now: Optional[datetime] = None, force: bool = False) -> Optional[dict]:
    """
    Read results.php (one POST normally; a few more before 06Z or after a break week, see
    fetch_latest, and one each to catch up on missed days), save the team's forecasts
    and put WxChallenge's final values into observations.jsonl. Returns {"read": days read,
    "changes": [(date, var, ours, official)]}, or None when not due.
    """
    import requests
    now = now or datetime.now(timezone.utc).replace(microsecond=0)
    today = now.date().isoformat()
    raw = load_raw()
    if not force and not due(raw, station, now):
        return None
    raw["checks"] = [t for t in raw.get("checks", []) if t[:10] == today] + [now.isoformat()]
    RAW.write_text(dumps(raw, indent=1))       # count the check even if it fails below
    year, city = season(now.date()), station.lower()
    s = requests.Session()
    latest = fetch_latest(s, year, city, expected_day(_city_start(station), now.date()))
    cur = latest["day"]
    if not cur or not latest["dates"]:
        print(f"  WxChallenge: no {year} results for {city} yet")
        return {"read": 0, "changes": []}
    st = raw.setdefault("stations", {}).setdefault(station, {"days": {}})
    st.update({"year": year, "school": SCHOOL})
    read = 0
    if latest["forecasters"] and cur in latest["dates"]:
        _save_day(st, cur, latest["dates"][cur], latest, year, now)
        read += 1
    # the rank after the day before is final on today's page ("Prev")
    prev = latest["dates"].get(cur - 1)
    if prev and prev["date"] in st["days"]:
        for name, rec in st["days"][prev["date"]]["forecasters"].items():
            pr = (latest["forecasters"].get(name) or {}).get("official", {}).get("prev_rank")
            if pr is not None:
                rec["official"]["rank"] = pr
    # catch-up: days missed while nothing ran (one POST each)
    missing = [n for n, d in sorted(latest["dates"].items()) if n != cur and d["date"] not in st["days"]]
    for n in missing[:MAX_POSTS - 1]:
        time.sleep(PAUSE_S)
        p = parse_results(_post(s, year, city, n))
        if p["forecasters"]:
            _save_day(st, n, latest["dates"][n], p, year, now)
            read += 1
    # WxChallenge's final values replace ours where they differ
    official = {d["date"]: {"obs": d["obs"], "status": d["status"], "review": d["review"],
                            "fetched_at_utc": now.isoformat()}
                for d in latest["dates"].values()
                if d["final"] and all(d["obs"].get(v) is not None for v in VARS)}
    changes = wxc_verify.set_official(station, official) if official else []
    if all(d["final"] for d in latest["dates"].values() if d["date"] < today):
        st["done_for"] = today                 # yesterday is final: nothing more to read today
    raw["generated_at_utc"] = now.isoformat()
    RAW.write_text(dumps(raw, indent=1))
    print(f"  WxChallenge: {city} day {cur} ({latest['status']}); {len(official)} final day(s); "
          f"team forecasts for {read} day(s)")
    for day, v, ours, off in changes:
        print(f"    {day} {v}: ours {ours} -> official {off}")
    return {"read": read, "changes": changes}


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
    """team.json: each forecaster's days scored against the scoreboard's observed values
    (WxChallenge's own once final, see set_official), so the points match the official ones."""
    station = verif.get("station")
    st = (raw.get("stations") or {}).get(station) or {}
    team = st.get("days") or {}
    days = [d for d in verif.get("days") or [] if d.get("models")]
    people, pseudo = {}, []
    for d in days:
        t = team.get(d["date"]) or {}
        row = {}
        for name, rec in (t.get("forecasters") or {}).items():
            s = _score(rec["forecast"], d["obs"], rec)
            if not s:
                continue
            rank = (rec.get("official") or {}).get("rank")
            if rank is not None:
                s["rank"] = rank
            s["day"] = t.get("day")
            row[name] = s
            people.setdefault(name, {"days": {}})["days"][d["date"]] = s
        pseudo.append({"date": d["date"], "models": row})
    for name, st_ in model_stats(pseudo).items():     # same decay weights as the model rows
        people[name]["summary"] = st_
    today = None
    T = verif.get("today")
    if T and T.get("obs") and T["obs"].get("wind_max_kt") is not None and team.get(T["date"]):
        t = team[T["date"]]
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
            "note": "display only; scored like the models against the scoreboard's observed values",
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
