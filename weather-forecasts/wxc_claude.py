"""
"Claude" as a WxChallenge forecaster: DISPLAY ONLY. Nothing here submits anything to
wxchallenge.com, and Claude's forecasts never go into the consensus, the models' totals or the
summary. They are scored like a team forecaster (wxc_team.scores) and show up on the scoreboard
when a reader types "Claude" into the "Add a Colorado State forecaster" box.

How a forecast is made
  * Python collects every input. Claude gets no tools (`claude -p --tools ""`), so a forecast
    depends only on what it was given, and a hindcast can't look anything up.
  * Live (three runs the day before, at 18Z, 21Z and 23:50Z; see SLOTS): the page's brief
    (data/wxchallenge/brief.md, which includes the consensus), the latest Area Forecast
    Discussion (IEM's AFOS archive, plain text), and Claude's own notes for the station. Each
    run is kept and scored on its own (the page's split view); the latest before 00Z is ranked.
  * Hindcast (a day D already past): an as-of brief rebuilt from only what was known at 23Z on
    D-1: the model runs out by then, and the verification of days up to D-2 (D-1 wasn't over
    yet). Plus the AFD in effect at 23Z D-1, and the notes as they stood then. It has fewer
    sections than the live brief (no ensembles, PoP, clouds, dewpoints or "today so far"), so a
    hindcast is a slightly harder test than a live day.
  * A forecast that finishes after the 00Z deadline is thrown away (logged as missed), never
    saved as live.

Notes (Claude's memory for a station)
  * New city: a station study first: ten years of daily climate for these dates (IEM), the
    period's observations, and the models' track record so far. Claude writes short notes.
  * The notes are revised after every NOTES_EVERY newly verified days of Claude's own
    forecasts, using only days verified before the forecast being made.
  * Each version is kept (claude_forecaster/notes/<ICAO>/<as_of>.md), and each forecast records
    the version it used.

Privacy: the raw records live in claude_forecaster/ (gitignored), not data/wxchallenge (which the
pipeline pushes), so tomorrow's forecast isn't public before the deadline. Only scored days reach
the page, through team.json.

  python wxc_claude.py auto              what the schedule runs: the live forecast in its
                                         window; otherwise a new city's study and hindcasts
  python wxc_claude.py live [--dry-run]  forecast the next day now (--dry-run: print, don't save)
  python wxc_claude.py late DATE         forecast DATE now from the current brief, after its
                                         deadline (marked "late"; counts as a live day)
  python wxc_claude.py hindcast [--days N] [--dry-run]
                                         study (if needed) + hindcast the period's missed days
  python wxc_claude.py brief DATE        print the as-of brief for DATE (no Claude call)
  python wxc_claude.py status            Claude's record so far
"""

import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import wxc_brief
import wxc_verify
from wxc_verify import VARS, DATA

ROOT = Path(__file__).resolve().parent
HOME_DIR = ROOT / "claude_forecaster"
RUNS = HOME_DIR / "runs.jsonl"
NOTES_DIR = HOME_DIR / "notes"
INPUTS_DIR = HOME_DIR / "inputs"          # the exact prompt each forecast was given (audit)
LOG = HOME_DIR / "log.jsonl"
TOKEN_FILE = HOME_DIR / ".oauth_token"    # optional: from `claude setup-token`

NAME = "Claude"
MODEL = "claude-opus-5-5"
EFFORT = "high"
CALL_TIMEOUT_S = 1200
AS_OF_HOUR = 23                 # 23Z the day before the target day: an hour before the deadline
# Live runs for day D, at fixed UTC times on D-1 (11:00, 14:00, 16:50 MST). Each is saved and
# scored on its own (the page's split view); the latest one before the 00Z deadline is THE
# forecast. A run that starts late (laptop asleep) takes the newest slot whose time has passed.
SLOTS = [("18Z", 18, 0), ("21Z", 21, 0), ("2350Z", 23, 50)]
HINDCAST_SLOT = "2350Z"         # hindcasts (as of 23Z) sit in the last run's row in the split view
BRIEF_MAX_AGE = timedelta(minutes=40)
BRIEF_WAIT = timedelta(minutes=15)
HINDCAST_DAYS = 16
NOTES_EVERY = 2
AFD_MAX_CHARS = 14000
CLIMO_YEARS = 10
CLIMO_HALF_WINDOW = 10          # days either side of the city's dates
IEM = "https://mesonet.agron.iastate.edu"
UA = "Mozilla/5.0 (compatible; weather-forecasts page; AI forecaster inputs)"

FORECAST_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string",
                      "description": "Your forecast reasoning, a few short paragraphs."},
        "summary": {"type": "string",
                    "description": "One or two sentences: the main call and why (max 300 chars)."},
        "tmax_f": {"type": "integer"},
        "tmin_f": {"type": "integer"},
        "wind_max_kt": {"type": "integer"},
        "precip_in": {"type": "number"},
    },
    "required": ["reasoning", "summary", "tmax_f", "tmin_f", "wind_max_kt", "precip_in"],
}
NOTES_SCHEMA = {
    "type": "object",
    "properties": {"notes": {"type": "string", "description": "The full station notes, Markdown."}},
    "required": ["notes"],
}

SYSTEM = """You are an experienced operational meteorologist entering the WxChallenge forecasting \
contest. You forecast one station's high, low, max sustained wind and liquid precipitation for one \
contest day, 06Z to 06Z UTC. You have no tools: everything you know about the situation is in the \
message (a data brief from the forecaster's own verification page, the NWS Area Forecast \
Discussion, and your own notes from earlier days at this station). Do not assume anything \
happened that the message doesn't show. Your goal is the lowest WxChallenge error points: \
1 point per degree F (high, low), 0.5 per kt (wind), and per 0.01 inch of precip 0.4 points up to \
0.10, 0.3 to 0.25, 0.2 to 0.50, 0.1 above. Use the consensus and the models' track records as a \
strong baseline and depart from them only for a reason you can state. Whole degrees F, whole kt, \
precip to 0.01 inch (0.00 for none or a trace)."""


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
def _now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _as_of(day: date) -> datetime:
    """23Z on the day before `day` (when the live forecast for `day` runs)."""
    return datetime(day.year, day.month, day.day, AS_OF_HOUR, tzinfo=timezone.utc) - timedelta(days=1)


def _deadline(day: date) -> datetime:
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc)


def _t(iso: str) -> datetime:
    t = datetime.fromisoformat(iso)
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def read_runs() -> list:
    return wxc_verify.read_jsonl(RUNS) if RUNS.exists() else []


def _append(path: Path, row: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(row, separators=(",", ":")) + "\n")


def log(event: str, **kw):
    _append(LOG, {"at_utc": _now().isoformat(), "event": event, **kw})
    print(f"  [{event}] " + ", ".join(f"{k}={v}" for k, v in kw.items()))


def _get(url: str, params: dict, timeout: int = 60):
    import requests
    for attempt in range(3):
        r = requests.get(url, params=params, timeout=timeout, headers={"User-Agent": UA})
        if r.status_code == 429 or "Too many requests" in r.text[:200]:
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
        return r
    r.raise_for_status()
    return r


# ----------------------------------------------------------------------------
# inputs: AFD, climatology, as-of brief
# ----------------------------------------------------------------------------
def fetch_afd(wfo: Optional[str], as_of: datetime) -> str:
    """The AFD from `wfo` in effect at `as_of` (the newest one issued by then), plain text."""
    if not wfo:
        return "(No forecast office configured for this station: no AFD.)"
    try:
        r = _get(f"{IEM}/cgi-bin/afos/retrieve.py",
                 {"pil": f"AFD{wfo.upper()}", "limit": 1, "fmt": "text",
                  "edate": as_of.strftime("%Y-%m-%dT%H:%MZ")})
        text = r.text.strip()
    except Exception as exc:
        return f"(AFD unavailable: {type(exc).__name__})"
    if len(text) < 100:
        return "(AFD unavailable: empty response.)"
    if len(text) > AFD_MAX_CHARS:
        text = text[:AFD_MAX_CHARS] + "\n[... truncated]"
    return text


def _iem_id(icao: str):
    """(id, network) of the station's IEM ASOS entry."""
    for sid in ([icao[1:], icao] if icao.startswith("K") else [icao]):
        try:
            rows = _get(f"{IEM}/api/1/station/{sid}.json", {}).json().get("data") or []
        except Exception:
            rows = []
        for r in rows:
            if str(r.get("network", "")).endswith("_ASOS"):
                return r["id"], r["network"]
        time.sleep(1)
    return None, None


def climatology(icao: str, days: list) -> str:
    """Daily climate around `days` (calendar dates) over the past CLIMO_YEARS years, from IEM's
    ASOS daily summaries (local calendar days, not the contest's 06Z-06Z, so context only)."""
    import csv, io, statistics as st
    sid, net = _iem_id(icao)
    if not sid:
        return "(No IEM daily climate found for this station.)"
    first, last = min(days), max(days)
    y1 = first.year - CLIMO_YEARS
    try:
        r = _get(f"{IEM}/cgi-bin/request/daily.py",
                 [("network", net), ("stations", sid), ("year1", y1), ("month1", 1), ("day1", 1),
                  ("year2", first.year - 1), ("month2", 12), ("day2", 31),
                  *[("var", v) for v in ("max_temp_f", "min_temp_f", "precip_in", "max_wind_speed_kts")],
                  ("format", "csv"), ("na", "blank")], timeout=120)
    except Exception as exc:
        return f"(IEM daily climate unavailable: {type(exc).__name__})"

    def doy_dist(d: date, ref: date) -> int:
        a = date(2001, d.month, min(d.day, 28)).toordinal()
        b = date(2001, ref.month, min(ref.day, 28)).toordinal()
        x = abs(a - b)
        return min(x, 365 - x)

    mid = first + (last - first) / 2
    win = (last - first).days // 2 + CLIMO_HALF_WINDOW
    rows = []
    for row in csv.DictReader(io.StringIO(r.text)):
        try:
            d = date.fromisoformat(row["day"])
        except (KeyError, ValueError):
            continue
        if doy_dist(d, mid) <= win:
            rows.append(row)
    if not rows:
        return "(IEM daily climate: no days in the window.)"

    def col(k):
        out = []
        for row in rows:
            try:
                out.append(float(row[k]))
            except (TypeError, ValueError):
                pass
        return out

    def q(xs, p):
        xs = sorted(xs)
        return xs[min(len(xs) - 1, max(0, round(p * (len(xs) - 1))))] if xs else None

    lines = [f"IEM daily summaries for {sid} ({net}), {y1} to {first.year - 1}, days within {win} "
             f"days of {mid.strftime('%b %d')} each year ({len(rows)} days). Local calendar days.", "",
             "| Variable | p10 | p25 | Median | p75 | p90 | Mean |", "|---|---|---|---|---|---|---|"]
    for k, name in (("max_temp_f", "High °F"), ("min_temp_f", "Low °F"),
                    ("max_wind_speed_kts", "Max wind kt"), ("precip_in", "Precip in")):
        xs = col(k)
        if xs:
            f = (lambda x: f"{x:.2f}") if k == "precip_in" else (lambda x: f"{x:.0f}")
            lines.append(f"| {name} | " + " | ".join(f(q(xs, p)) for p in (.1, .25, .5, .75, .9))
                         + f" | {f(st.mean(xs))} |")
    pr = col("precip_in")
    if pr:
        lines += ["", f"Share of days with measurable precip (>= 0.01\"): {sum(p >= 0.01 for p in pr) / len(pr):.0%}; "
                  f">= 0.25\": {sum(p >= 0.25 for p in pr) / len(pr):.0%}; >= 1.00\": {sum(p >= 1 for p in pr) / len(pr):.0%}."]
    return "\n".join(lines)


def _load(name: str):
    p = DATA / name
    return json.loads(p.read_text()) if p.exists() else None


def models_as_of(runs: list, station: str, day: str, as_of: datetime) -> dict:
    """Per model, the newest forecast for `day` out by `as_of` that has values (live runs win
    over hindcast rows, as in wxc_verify.forecasts_for_day)."""
    cands = sorted((r for r in runs if r["station"] == station and r["target_date"] == day
                    and _t(r["generated_at_utc"]) <= as_of), key=lambda r: r["generated_at_utc"])
    out = {}
    for r in cands:
        hind = bool(r.get("hindcast"))
        for name, fc in r["models"].items():
            if name in wxc_verify.RETIRED or (hind and name in out and not out[name][1]):
                continue
            if all(fc.get(v) is not None for v in VARS):
                out[name] = (fc, hind)
    return {n: fc for n, (fc, _) in out.items()}


def asof_brief(day: date, station=None, now: Optional[datetime] = None) -> tuple:
    """(brief text, info) for `day` from only what was known at 23Z on day-1."""
    import wxc_stations
    station = station or wxc_stations.get_station()
    as_of = _as_of(day)
    verif = _load("verification.json") or {}
    runs = wxc_verify.read_runs()
    models = models_as_of(runs, station.icao, day.isoformat(), as_of)
    if not models:
        raise RuntimeError(f"no model runs for {station.icao} {day} out by {as_of:%Y-%m-%d %HZ}")
    # verification: only days over by as_of (day-1 ends at 06Z on day, after as_of)
    last_ok = (day - timedelta(days=2)).isoformat()
    prior = [d for d in (verif.get("days") or []) if d["date"] <= last_ok and d.get("models")]
    prior = [{**d, "obs_pending": []} for d in prior]
    # the brief's track record and model order without anything that came later
    summ = wxc_verify.model_stats(prior) if prior else {}
    order_pref = (_load("forecast.json") or {}).get("meta", {}).get("models") or []
    order = [m for m in order_pref if m in models] + sorted(m for m in models if m not in order_pref)
    fc = {"generated_at_utc": as_of.isoformat(),
          "meta": {"site": f"{station.name} ({station.icao})", "station": station.icao,
                   "wfo": station.wfo, "tz": station.tz, "target_date": day.isoformat(),
                   "valid_range_utc": [f"{day}T06", f"{day + timedelta(days=1)}T06"],
                   "models": order, "afd_url": station.afd_url},
          "models": {n: dict(m) for n, m in models.items()}}
    v = {"station": station.icao, "city_start": verif.get("city_start"),
         "period_start": verif.get("period_start"), "half_life_days": verif.get("half_life_days"),
         "days": prior, "summary": summ}
    # the hourly series, only if that file was written by as_of
    series = wxc_verify.load_series(station.icao, day, "submitted")
    if series and _t(series.get("generated_at_utc", "9999-01-01T00:00:00+00:00")) > as_of:
        series = None
    text = wxc_brief.build_brief(fc, v, None, now=as_of, series=series)
    note = (f"> Hindcast brief, rebuilt with only what was known at {as_of:%Y-%m-%d %H}Z: model runs "
            f"out by then and verification through {last_ok}. The live brief's ensemble, PoP, cloud, "
            "dewpoint and \"today so far\" sections are not available here.\n\n")
    head, _, rest = text.partition("\n\n")
    return head + "\n\n" + note + rest, {"as_of": as_of.isoformat(), "n_models": len(models),
                                         "verified_through": last_ok, "series": bool(series)}


# ----------------------------------------------------------------------------
# notes
# ----------------------------------------------------------------------------
def notes_versions(icao: str) -> list:
    """[(as_of datetime, path)] oldest first."""
    d = NOTES_DIR / icao
    out = []
    for p in d.glob("*.md") if d.exists() else []:
        try:
            out.append((datetime.strptime(p.stem, "%Y%m%dT%H%MZ").replace(tzinfo=timezone.utc), p))
        except ValueError:
            pass
    return sorted(out)


def notes_at(icao: str, as_of: datetime):
    """(text, version) of the newest notes written for `as_of` or earlier."""
    vs = [(t, p) for t, p in notes_versions(icao) if t <= as_of]
    if not vs:
        return None, None
    t, p = vs[-1]
    return p.read_text(), p.stem


def save_notes(icao: str, as_of: datetime, text: str) -> str:
    d = NOTES_DIR / icao
    d.mkdir(parents=True, exist_ok=True)
    stem = as_of.strftime("%Y%m%dT%H%MZ")
    (d / f"{stem}.md").write_text(text.strip() + "\n")
    return stem


def _verified_claude_days(icao: str, upto: str) -> list:
    """Claude's forecasts for days <= upto that have observations, with the models' scores."""
    verif = _load("verification.json") or {}
    days = {d["date"]: d for d in verif.get("days") or [] if d.get("models")}
    out = []
    for day, rec in sorted(best_records(icao).items()):
        if day <= upto and day in days:
            s = wxc_verify.score_day(rec["forecast"], days[day]["obs"])
            if s:
                out.append((day, rec, s, days[day]))
    return out


def study_prompt(station, first_day: date) -> str:
    as_of = _as_of(first_day)
    brief, _ = asof_brief(first_day, station)
    verif = _load("verification.json") or {}
    span = [first_day + timedelta(days=i) for i in range(CITY_SPAN_DAYS)]
    return "\n\n".join([
        f"# Station study: {station.name} ({station.icao})",
        f"You are about to forecast this station for WxChallenge, starting with {first_day} "
        f"(it is now {as_of:%Y-%m-%d %H}Z). Write your station notes: what you will want to remember "
        "every day here. Cover the local climate for these dates, local effects (terrain, water, "
        "wind regimes, precip habits), which models have been reliable or biased here and by how much, "
        "and any rules of thumb for this contest's variables. At most about 450 words, Markdown, "
        "concrete numbers where you have them.",
        "## Climate for these dates",
        climatology(station.icao, span),
        f"## The forecast brief as of {as_of:%Y-%m-%d %H}Z (track record and the verified days so far; "
        f"the period started {verif.get('period_start')})",
        brief,
    ])


CITY_SPAN_DAYS = 14


def update_prompt(station, notes: str, done: list, as_of: datetime) -> str:
    rows = ["| Date | Kind | Your forecast (H/L/W/P) | Observed | Your points | Consensus pts | Best model (pts) | Your summary |",
            "|---|---|---|---|---|---|---|---|"]
    for day, rec, s, d in done:
        f, o = rec["forecast"], d["obs"]
        mp = {n: m["points"] for n, m in d["models"].items()}
        best = min((n for n in mp if n != "CONSENSUS"), key=mp.get, default=None)
        rows.append(f"| {day} | {'hindcast' if rec.get('hindcast') else 'live'} | "
                    f"{f['tmax_f']}/{f['tmin_f']}/{f['wind_max_kt']}/{f['precip_in']:.2f} | "
                    f"{o['tmax_f']}/{o['tmin_f']}/{o['wind_max_kt']}/{o['precip_in']:.2f} | "
                    f"{s['points']:.1f} | {mp.get('CONSENSUS', float('nan')):.1f} | "
                    f"{best} ({mp.get(best, float('nan')):.1f}) | {rec.get('summary', '')[:200]} |")
    return "\n\n".join([
        f"# Revise your station notes: {station.name} ({station.icao}), as of {as_of:%Y-%m-%d %H}Z",
        "Below are your current notes and how your forecasts have verified. Rewrite the notes: keep "
        "what held up, correct what didn't, and add any lesson from your misses (e.g. a bias of yours "
        "to correct). At most about 450 words, Markdown.",
        "## Current notes", notes or "(none yet)",
        "## Your verified forecasts", "\n".join(rows),
    ])


def maybe_update_notes(station, as_of: datetime, call=None, dry_run=False):
    """Write a new notes version when NOTES_EVERY more of Claude's days have verified. Only days
    over by as_of count: at 23Z on day X, day X is still running (it ends 06Z on X+1), so <= X-1."""
    call = call or call_claude
    upto = (as_of.date() - timedelta(days=1)).isoformat()
    notes, ver = notes_at(station.icao, as_of)
    done = _verified_claude_days(station.icao, upto)
    covered = 0
    if ver:
        meta = HOME_DIR / "notes" / station.icao / f"{ver}.json"
        covered = json.loads(meta.read_text()).get("n_verified", 0) if meta.exists() else 0
    if len(done) - covered < NOTES_EVERY or dry_run:
        return ver
    out = call(update_prompt(station, notes, done, as_of), NOTES_SCHEMA,
               system="You are an experienced operational meteorologist keeping concise station notes.")
    ver = save_notes(station.icao, as_of, out["notes"])
    (NOTES_DIR / station.icao / f"{ver}.json").write_text(json.dumps({"n_verified": len(done), "upto": upto}))
    log("notes_updated", station=station.icao, version=ver, n_verified=len(done))
    return ver


def ensure_study(station, first_day: date, call=None, dry_run=False):
    """Station notes before the first forecast at a station (a new city)."""
    call = call or call_claude
    as_of = _as_of(first_day)
    if notes_at(station.icao, as_of)[0] is not None:
        return
    if notes_versions(station.icao):
        return                       # notes exist, only newer than this hindcast's start
    prompt = study_prompt(station, first_day)
    if dry_run:
        print(prompt[:3000] + "\n[...]")
        return
    out = call(prompt, NOTES_SCHEMA,
               system="You are an experienced operational meteorologist preparing to forecast a new station.")
    ver = save_notes(station.icao, as_of, out["notes"])
    (NOTES_DIR / station.icao / f"{ver}.json").write_text(json.dumps({"n_verified": 0, "study": True}))
    log("study", station=station.icao, version=ver)


# ----------------------------------------------------------------------------
# the Claude call
# ----------------------------------------------------------------------------
def claude_bin() -> str:
    """The claude CLI: $CLAUDE_BIN, PATH, ~/.local/bin, or the newest copy bundled with the
    desktop app (its path changes with each version, so it's looked up every time)."""
    for c in (os.environ.get("CLAUDE_BIN"), shutil.which("claude"),
              str(Path.home() / ".local/bin/claude"), str(Path.home() / ".claude/local/claude")):
        if c and os.access(c, os.X_OK):
            return c
    pat = str(Path.home() / "Library/Application Support/Claude/claude-code/*/*/claude.app/Contents/MacOS/claude")
    found = sorted(glob.glob(pat), key=lambda p: [int(x) if x.isdigit() else x
                                                   for x in p.split("claude-code/")[1].split("/")[0].split(".")])
    if found:
        return found[-1]
    raise FileNotFoundError("claude CLI not found; set CLAUDE_BIN")


def _clean_env() -> dict:
    """A plain environment: the variables a Claude Code session sets for its own tools would
    point the child at that session's auth, not the user's."""
    env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "LANG", "TMPDIR") if k in os.environ}
    env["PATH"] = "/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin"
    tok = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    if not tok and TOKEN_FILE.exists():
        tok = TOKEN_FILE.read_text().strip()
    if tok:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = tok
    return env


def call_claude(prompt: str, schema: dict, system: str = SYSTEM) -> dict:
    """One headless call: no tools, no MCP servers, no settings/hooks, nothing saved."""
    HOME_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [claude_bin(), "-p", "--model", MODEL, "--effort", EFFORT, "--tools", "",
           "--strict-mcp-config", "--setting-sources", "", "--no-session-persistence",
           "--system-prompt", system, "--output-format", "json", "--json-schema", json.dumps(schema)]
    t0 = time.time()
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=CALL_TIMEOUT_S,
                       cwd=HOME_DIR, env=_clean_env())
    try:
        res = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude: no JSON (exit {p.returncode}): {(p.stderr or p.stdout)[:300]}")
    if res.get("is_error"):
        raise RuntimeError(f"claude: {str(res.get('result'))[:300]}")
    out = res.get("structured_output")
    if out is None:
        txt = str(res.get("result") or "").strip()
        if "```" in txt:
            txt = txt.split("```")[1].removeprefix("json").strip()
        out = json.loads(txt)
    out["_meta"] = {"seconds": round(time.time() - t0, 1), "cost_usd": res.get("total_cost_usd"),
                    "usage": {k: (res.get("usage") or {}).get(k) for k in
                              ("input_tokens", "output_tokens", "cache_read_input_tokens")}}
    return out


def validate(out: dict) -> dict:
    f = {"tmax_f": int(round(out["tmax_f"])), "tmin_f": int(round(out["tmin_f"])),
         "wind_max_kt": int(round(out["wind_max_kt"])), "precip_in": round(max(0.0, float(out["precip_in"])), 2)}
    if not (-80 <= f["tmin_f"] <= f["tmax_f"] <= 130):
        raise ValueError(f"temperatures out of range: {f}")
    if not (0 <= f["wind_max_kt"] <= 150) or f["precip_in"] > 20:
        raise ValueError(f"wind/precip out of range: {f}")
    return f


def forecast_prompt(brief: str, afd: str, notes: Optional[str], day: date, as_of: datetime) -> str:
    return "\n\n".join([
        f"# Your WxChallenge forecast for {day} (06Z {day} to 06Z {day + timedelta(days=1)}); "
        f"it is now {as_of:%Y-%m-%d %H:%M}Z, the deadline is {day} 00Z.",
        "## Your station notes (from earlier days)", notes or "(none yet)",
        "## NWS Area Forecast Discussion (the newest one issued by now)", afd,
        "## The forecast brief", brief,
        "Give your reasoning, a one- or two-sentence summary, and your four numbers.",
    ])


def make_forecast(station, day: date, as_of: datetime, brief: str, kind: str, call=None,
                  dry_run=False, brief_info=None, slot: Optional[str] = None) -> Optional[dict]:
    call = call or call_claude
    afd = fetch_afd(station.wfo, as_of)
    notes, ver = notes_at(station.icao, as_of)
    prompt = forecast_prompt(brief, afd, notes, day, as_of)
    digest = hashlib.sha256(prompt.encode()).hexdigest()[:16]
    if dry_run:
        print(f"--- prompt for {day} ({kind}): {len(prompt):,} chars, notes {ver}, sha {digest}")
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    (INPUTS_DIR / f"{station.icao}_{day}_{kind}{'_dry' if dry_run else ''}.md").write_text(prompt)
    out = None
    for attempt in range(2):
        try:
            out = call(prompt, FORECAST_SCHEMA)
            fc = validate(out)
            break
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            print(f"  attempt {attempt + 1}: bad forecast ({exc})")
            out = None
    if out is None:
        log("failed", station=station.icao, day=day.isoformat(), kind=kind)
        return None
    rec = {"station": station.icao, "target_date": day.isoformat(), "kind": kind,
           "hindcast": kind == "hindcast", "as_of_utc": as_of.isoformat(),
           "slot": slot or (HINDCAST_SLOT if kind == "hindcast" else slot_for(as_of, day) or SLOTS[-1][0]),
           "issued_at_utc": _now().isoformat(), "model": MODEL, "effort": EFFORT,
           "forecast": fc, "summary": str(out.get("summary", ""))[:400],
           "reasoning": out.get("reasoning", ""), "notes_version": ver, "input_sha": digest,
           "brief": brief_info or {}, "call": out.get("_meta")}
    if kind == "live" and _now() >= _deadline(day):
        log("missed_deadline", station=station.icao, day=day.isoformat(), issued=rec["issued_at_utc"])
        return None
    if dry_run:
        print(json.dumps({k: rec[k] for k in ("forecast", "summary", "notes_version", "call")}, indent=1))
        return rec
    _append(RUNS, rec)
    log("forecast", station=station.icao, day=day.isoformat(), kind=kind, **fc)
    return rec


# ----------------------------------------------------------------------------
# records for scoring (wxc_team.scores)
# ----------------------------------------------------------------------------
def slot_for(t: datetime, day: date) -> Optional[str]:
    """The newest of `day`'s run slots (on day-1, UTC) at or before t; None before the first."""
    prev = day - timedelta(days=1)
    out = None
    for name, h, m in SLOTS:
        if datetime(prev.year, prev.month, prev.day, h, m, tzinfo=timezone.utc) <= t:
            out = name
    return out


def rec_slot(r: dict) -> str:
    """A record's slot (records from before slots existed: from their issue time)."""
    if r.get("slot"):
        return r["slot"]
    if r.get("hindcast"):
        return HINDCAST_SLOT
    return slot_for(_t(r["issued_at_utc"]), date.fromisoformat(r["target_date"])) or SLOTS[0][0]


def best_records(icao: str) -> dict:
    """{date: record}: per day THE forecast: the latest live (or late) one, else the newest
    hindcast."""
    key = lambda r: (not r.get("hindcast"), r["issued_at_utc"])      # noqa: E731
    out = {}
    for r in read_runs():
        if r.get("station") != icao:
            continue
        cur = out.get(r["target_date"])
        if cur is None or key(r) > key(cur):
            out[r["target_date"]] = r
    return out


def slot_records(icao: str) -> dict:
    """{slot: {date: record}}: each run slot's live forecasts (the latest per slot and day), and
    the hindcasts in HINDCAST_SLOT on days that slot has no live forecast."""
    out = {name: {} for name, _, _ in SLOTS}
    hind = {}
    for r in sorted(read_runs(), key=lambda r: r["issued_at_utc"]):
        if r.get("station") != icao:
            continue
        if r.get("hindcast"):
            hind[r["target_date"]] = r
        else:
            out.setdefault(rec_slot(r), {})[r["target_date"]] = r
    for d, r in hind.items():
        out[HINDCAST_SLOT].setdefault(d, r)
    return {k: v for k, v in out.items() if v}


# ----------------------------------------------------------------------------
# live and hindcast runs
# ----------------------------------------------------------------------------
def _brief_fresh(day: date) -> Optional[str]:
    """brief.md's text when it's for `day` and recent enough, else None."""
    fc = _load("forecast.json") or {}
    if (fc.get("meta") or {}).get("target_date") != day.isoformat() or not wxc_brief.BRIEF.exists():
        return None
    gen = _t(fc["generated_at_utc"])
    if _now() - gen > BRIEF_MAX_AGE:
        return None
    return wxc_brief.BRIEF.read_text()


def _kick_pipeline():
    subprocess.run(["launchctl", "kickstart", f"gui/{os.getuid()}/com.jglarson.wxchallenge"],
                   capture_output=True)


def late(day: date, call=None) -> Optional[dict]:
    """A forecast for `day` made now, after its deadline, from the current brief (the last one
    for that day): kind "late". It counts as a live day (James: timing within about the hour
    around the deadline is fine), unlike a hindcast."""
    import wxc_stations
    station = wxc_stations.get_station()
    fc = _load("forecast.json") or {}
    if (fc.get("meta") or {}).get("target_date") != day.isoformat():
        raise SystemExit(f"brief.md is for {(fc.get('meta') or {}).get('target_date')}, not {day}")
    now = _now()
    maybe_update_notes(station, now, call=call)
    return make_forecast(station, day, now, wxc_brief.BRIEF.read_text(), "late", call=call,
                         brief_info={"generated_at_utc": fc.get("generated_at_utc"), "source": "brief.md"})


def live(dry_run=False, call=None, now: Optional[datetime] = None) -> Optional[dict]:
    import wxc_stations
    station = wxc_stations.get_station()
    now = now or _now()
    day = now.date() + timedelta(days=1)
    slot = slot_for(now, day)
    if slot is None:
        if not dry_run:
            print(f"Before the first run slot ({SLOTS[0][0]}) for {day}: nothing to do.")
            return None
        slot = SLOTS[0][0]
    if not dry_run and any(r["target_date"] == day.isoformat() and not r.get("hindcast")
                           and r["station"] == station.icao and rec_slot(r) == slot for r in read_runs()):
        print(f"Already forecast {station.icao} {day} in the {slot} slot.")
        return None
    brief = _brief_fresh(day)
    if brief is None and not dry_run:
        _kick_pipeline()
        t0 = time.time()
        while brief is None and time.time() - t0 < BRIEF_WAIT.total_seconds() \
                and _now() < _deadline(day) - timedelta(minutes=20):
            time.sleep(30)
            brief = _brief_fresh(day)
    if brief is None:
        fc = _load("forecast.json") or {}
        if (fc.get("meta") or {}).get("target_date") != day.isoformat():
            log("no_brief", station=station.icao, day=day.isoformat())
            return None
        brief = wxc_brief.BRIEF.read_text()          # stale; its header says how old
    if notes_at(station.icao, now)[0] is None:
        ensure_study(station, day, call=call, dry_run=dry_run)
    maybe_update_notes(station, now, call=call, dry_run=dry_run)
    gen = (_load("forecast.json") or {}).get("generated_at_utc")
    return make_forecast(station, day, now, brief, "live", call=call, dry_run=dry_run,
                         brief_info={"generated_at_utc": gen, "source": "brief.md"}, slot=slot)


def hindcast_days(icao: str, n: int = HINDCAST_DAYS, now: Optional[datetime] = None) -> list:
    """The period's days with model runs whose deadline has passed and that Claude hasn't
    forecast, newest n."""
    now = now or _now()
    have = set(best_records(icao))
    runs = wxc_verify.read_runs()
    days = sorted({r["target_date"] for r in runs if r["station"] == icao})
    verif = _load("verification.json") or {}
    start = verif.get("period_start") or "0000"
    days = [d for d in days if d >= start and _deadline(date.fromisoformat(d)) <= now]
    return [date.fromisoformat(d) for d in days[-n:] if d not in have]


def hindcast(n: int = HINDCAST_DAYS, dry_run=False, call=None) -> list:
    import wxc_stations
    station = wxc_stations.get_station()
    todo = hindcast_days(station.icao, n)
    print(f"{station.icao}: {len(todo)} day(s) to hindcast: {', '.join(d.isoformat() for d in todo) or 'none'}")
    if not todo:
        return []
    ensure_study(station, todo[0], call=call, dry_run=dry_run)
    out = []
    for day in todo:
        as_of = _as_of(day)
        brief, info = asof_brief(day, station)
        maybe_update_notes(station, as_of, call=call, dry_run=dry_run)
        rec = make_forecast(station, day, as_of, brief, "hindcast", call=call, dry_run=dry_run, brief_info=info)
        if rec:
            out.append(rec)
        if dry_run:
            break
    return out


def auto():
    """The schedule's entry point: the run slot due now (if any, and not done yet), then a new
    city's study and hindcasts of any missed days."""
    live()
    hindcast()


def status():
    import wxc_stations
    icao = wxc_stations.get_station().icao
    verif = _load("verification.json") or {}
    days = {d["date"]: d for d in verif.get("days") or [] if d.get("models")}
    print(f"{NAME} at {icao}: model {MODEL}, effort {EFFORT}")
    print(f"{'date':10} {'kind':8} {'H/L/W/P':16} {'obs':16} {'pts':>5} {'cons':>5}")
    for day, rec in sorted(best_records(icao).items()):
        f = rec["forecast"]
        d = days.get(day)
        s = wxc_verify.score_day(f, d["obs"]) if d else None
        o = d["obs"] if d else None
        c = (d or {}).get("models", {}).get("CONSENSUS", {}).get("points")
        print(f"{day} {rec['kind']:8} {f['tmax_f']}/{f['tmin_f']}/{f['wind_max_kt']}/{f['precip_in']:.2f}".ljust(37)
              + (f"{o['tmax_f']}/{o['tmin_f']}/{o['wind_max_kt']}/{o['precip_in']:.2f}".ljust(17) if o else " " * 17)
              + (f"{s['points']:5.1f}" if s else "    —") + (f" {c:5.1f}" if c is not None else "     —"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["auto", "live", "late", "hindcast", "brief", "status"])
    ap.add_argument("date", nargs="?")
    ap.add_argument("--days", type=int, default=HINDCAST_DAYS)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.cmd == "auto":
        auto()
    elif a.cmd == "live":
        live(dry_run=a.dry_run)
    elif a.cmd == "late":
        late(date.fromisoformat(a.date))
    elif a.cmd == "hindcast":
        hindcast(a.days, dry_run=a.dry_run)
    elif a.cmd == "brief":
        text, info = asof_brief(date.fromisoformat(a.date))
        print(text)
        print(info, file=sys.stderr)
    else:
        status()


if __name__ == "__main__":
    main()
