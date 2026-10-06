"""
A compact, plain-text (Markdown) brief of the WxChallenge data for AI assistants.

The page renders its tables with JavaScript, so a tool that fetches the page without running
scripts sees only "Loading…". This module condenses forecast.json, verification.json and
today.json into data/wxchallenge/brief.md (a few KB): the target day's guidance, the
consensus and its weights, ensemble spread, precip chances, each model's track record this
period, recent days' errors, and how today is going so far, plus the scoring rules and a
short method for turning it all into a forecast.

The brief is not linked visibly on the page: llms.txt at the site root and a visually
hidden link at the bottom of wxchallenge/index.html point to it.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "wxchallenge"
BRIEF = DATA / "brief.md"
SITE = "https://jameslarsonclimate.github.io/website/weather-forecasts"

VARS = ["tmax_f", "tmin_f", "wind_max_kt", "precip_in"]
VAR_NAMES = {"tmax_f": "High °F", "tmin_f": "Low °F", "wind_max_kt": "Wind kt", "precip_in": 'Precip in'}
ENS_VARS = {"tmax_f": "High °F", "tmin_f": "Low °F", "wind_max_kt": "Wind kt", "precip_in": "Precip in"}
BLOCKS = ["06-12", "12-18", "18-00", "00-06"]
RECENT_DAYS = 8
STALE_HOURS = 3


def _f(x, v):
    """A value at its variable's precision ('—' when missing)."""
    if x is None:
        return "—"
    return f"{x:.2f}" if v == "precip_in" else f"{x:.1f}"


def _s(x, v, digits=None):
    """A signed difference at its variable's precision (never '-0')."""
    if x is None:
        return "—"
    d = digits if digits is not None else 2 if v == "precip_in" else 1
    x = round(x, d) + 0.0          # + 0.0 turns -0.0 into 0.0
    return f"{x:+.{d}f}"


def _pct(p):
    return "—" if p is None else f"{round(100 * p)}%"


def _hhz(iso):
    """'2026-10-06T18' -> '06/18Z' (day/hour of the model run)."""
    if not iso:
        return "—"
    return f"{iso[8:10]}/{iso[11:13]}Z"


def _row(cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"


def _table(head, rows, right_from=1):
    align = ["---"] * right_from + ["--:"] * (len(head) - right_from)
    return "\n".join([_row(head), _row(align), *(_row(r) for r in rows)])


def _model_order(fc, verif):
    order = [m for m in fc.get("meta", {}).get("models", []) if m in fc.get("models", {})]
    extra = [m for m in verif.get("summary", {}) if m not in order]
    return order + extra


# ----------------------------------------------------------------------------
# sections
# ----------------------------------------------------------------------------
def _header(fc, now):
    meta = fc["meta"]
    gen = fc.get("generated_at_utc", "")
    target = meta["target_date"]
    start, end = meta.get("valid_range_utc", ["", ""])
    lines = [
        f"# WxChallenge forecast brief: {meta.get('site', meta.get('station'))}",
        "",
        f"- Station: **{meta['station']}**",
        f"- Target day: **{target}**, scored over {start}Z to {end}Z (UTC, 06Z to 06Z)",
        f"- Submission deadline: {target}T00Z (forecasts for a day are due at 00Z that day)",
        f"- Generated: {gen} (refreshed several times an hour while the forecast job runs)",
        "- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)",
    ]
    try:
        age = now - datetime.fromisoformat(gen)
        if age > timedelta(hours=STALE_HOURS):
            lines.append(f"- **Warning: this brief is {age.total_seconds() / 3600:.0f} h old; "
                         "the models below may be superseded.**")
    except (TypeError, ValueError):
        pass
    return "\n".join(lines)


def _howto():
    return "\n".join([
        "## How to use this brief (for AI assistants)",
        "",
        "1. Start from the **CONSENSUS** row. It is already bias-corrected and skill-weighted using "
        "this period's verification (method below).",
        "2. Check the track-record table: a model with a large, consistent bias (|bias| close to its "
        "MAE) is reliably off in that direction. The consensus already removes most of that bias; "
        "lean further only if the last few days (recent-errors table) show the bias growing.",
        "3. Use the ensemble percentiles for uncertainty. For **precip**, enter roughly the ensemble "
        "**median**, not the mean: points are charged per 0.01\" of error, and charged most heavily "
        "near zero, so the median minimizes expected points. Check the chance-of-rain table: when "
        "the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.",
        "4. Use \"Today so far\" (the day currently in progress, not the target day) to see which "
        "models are handling the current pattern; persistent errors there often carry into tomorrow.",
        "5. Give whole °F for high/low, whole kt for wind, and precip to 0.01\". State the reasoning "
        "for any departure from the consensus.",
    ])


def _scoring():
    return "\n".join([
        "## Scoring (error points; lower is better)",
        "",
        "- High and low temperature: 1 point per °F of error.",
        "- Max sustained wind: 0.5 point per kt of error.",
        "- Precipitation: per 0.01\" between forecast and observed: 0.4 pt for amounts 0.00 to 0.10\", "
        "0.3 for 0.11 to 0.25\", 0.2 for 0.26 to 0.50\", 0.1 above 0.50\". A trace counts as 0.00.",
        "- Forecasts are rounded as submitted (whole °F and kt, 0.01\") before scoring.",
    ])


def _guidance(fc, order):
    rows = []
    for name in order:
        m = fc["models"].get(name)
        if not m or name == "CONSENSUS":
            continue
        tag = " (precip only)" if m.get("precip_only") else ""
        rows.append([f"{name}{tag}", _hhz(m.get("init_time_utc")),
                     *(_f(m.get(v), v) for v in VARS)])
    c = fc["models"].get("CONSENSUS")
    if c:
        rows.append(["**CONSENSUS**", "", *(f"**{_f(c.get(v), v)}**" for v in VARS)])
    notes = []
    for name in order:
        m = fc["models"].get(name) or {}
        n = m.get("note") or m.get("precip_note")
        if n:
            notes.append(f"- {name}: {n}")
        if m.get("error"):
            notes.append(f"- {name}: failed this run ({m['error'][:80]})")
    out = ["## Guidance for the target day", "",
           "Run = day/hour (UTC) of the model initialization.", "",
           _table(["Model", "Run", *VAR_NAMES.values()], rows, right_from=2)]
    if notes:
        out += ["", "Notes:", *notes]
    out += ["", "GEFS is shown but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) "
            "and NBM QMD are not in the consensus either; they inform the precip choice."]
    return "\n".join(out)


def _consensus(fc):
    c = fc["models"].get("CONSENSUS")
    if not c or not c.get("method"):
        return ""
    out = ["## Consensus method", ""]
    methods = {d.get("method") for d in c["method"].values()}
    for m in methods:
        out.append(f"- {m}. Precip is weighted but not bias-corrected.")
    out.append("")
    for v in VARS:
        d = c["method"].get(v)
        if not d:
            continue
        w = sorted(d.get("weights", {}).items(), key=lambda kv: -kv[1])
        line = f"- {VAR_NAMES[v]} weights: " + ", ".join(f"{n} {x:.2f}" for n, x in w)
        if d.get("excluded_outliers"):
            line += f" (outliers excluded: {', '.join(d['excluded_outliers'])})"
        if d.get("not_yet_verified"):
            line += f" (no track record yet: {', '.join(d['not_yet_verified'])})"
        out.append(line)
    return "\n".join(out)


def _ensembles(fc, order):
    rows = []
    for name in order:
        m = fc["models"].get(name) or {}
        e = m.get("ensemble")
        if not e:
            continue
        for v in VARS:
            st = (e.get("stats") or {}).get(v)
            if not st:
                continue
            rows.append([name, e.get("n_members", "—"), ENS_VARS[v],
                         *(_f(st.get(k), v) for k in ("p10", "p25", "p50", "p75", "p90")),
                         _f(st.get("mean"), v)])
    if not rows:
        return ""
    out = ["## Ensemble spread (target day)", "",
           _table(["Ensemble", "Members", "Variable", "p10", "p25", "Median", "p75", "p90", "Mean"],
                  rows, right_from=3)]
    probs = []
    for name in order:
        m = fc["models"].get(name) or {}
        pp = ((m.get("ensemble") or {}).get("stats") or {}).get("precip_prob")
        if pp:
            probs.append([name, *(_pct(pp.get(k)) for k in ("0.01", "0.10", "0.25", "0.50"))])
    qmd = (fc["models"].get("NBM_QMD") or {}).get("pop", {}).get("q24_in")
    if probs:
        out += ["", "Share of members reaching each 24-h precip amount:", "",
                _table(["Ensemble", '≥0.01"', '≥0.10"', '≥0.25"', '≥0.50"'], probs)]
    if qmd:
        out += ["", "NBM QMD calibrated 24-h precip percentiles: " +
                ", ".join(f"p{k} {v:.2f}\"" for k, v in qmd.items())]
    return "\n".join(out)


def _pop(fc, verif, order):
    summ = (verif.get("pop") or {}).get("summary", {})
    rows = []
    for name in order:
        p = (fc["models"].get(name) or {}).get("pop")
        if not p:
            continue
        if p.get("p24") is not None:
            p24 = _pct(p["p24"])
        elif p.get("p24_range"):
            p24 = f"{_pct(p['p24_range'][0])} to {_pct(p['p24_range'][1])}"
        else:
            p24 = "—"
        s = summ.get(name, {})
        brier = f"{s['brier_6h']:.2f} ({s.get('n_blocks', 0)})" if s.get("brier_6h") is not None else "—"
        rows.append([name, p.get("basis", ""), *(_pct(p.get("blocks", {}).get(b)) for b in BLOCKS),
                     p24, brier])
    if not rows:
        return ""
    base = (verif.get("pop") or {}).get("base_rate") or {}
    out = ["## Chance of measurable precip (≥0.01\") on the target day", "",
           "6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances "
           "(lower is better; number of blocks verified in brackets).", "",
           _table(["Source", "Basis", *BLOCKS, "24 h", "Brier 6h (n)"], rows, right_from=2)]
    if base.get("brier_6h") is not None:
        out += ["", f"For reference, always forecasting the period's observed frequency "
                f"({_pct(base.get('freq_6h'))} of 6-h blocks wet) scores Brier {base['brier_6h']:.2f}."]
    return "\n".join(out)


def _track_record(verif):
    summ = verif.get("summary", {})
    if not summ:
        return ""
    rows = []
    for name, s in sorted(summ.items(), key=lambda kv: kv[1].get("mean_points", 1e9)):
        rows.append([name, s.get("n_days", "—"), f"{s.get('mean_points', 0):.1f}",
                     *(_s(s.get("bias", {}).get(v), v) for v in VARS),
                     *(_f(s.get("mae", {}).get(v), v) for v in VARS)])
    hl = verif.get("half_life_days", {})
    hl_txt = ", ".join(f"{VAR_NAMES[v]} {hl[v]:g} d" for v in VARS if v in hl)
    head = ["Model", "Days", "Pts/day",
            "Bias high", "Bias low", "Bias wind", "Bias precip",
            "MAE high", "MAE low", "MAE wind", "MAE precip"]
    return "\n".join([
        "## Track record this period", "",
        f"Since {verif.get('period_start', '?')} at {verif.get('station')} (forecast - observed, so "
        f"negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward "
        f"recent days (half-lives: {hl_txt}). Days before {verif.get('city_start', '?')} are "
        "hindcasts (model runs from 23Z the evening before, as they would have been submitted). "
        "Sorted best first by mean error points per day.", "",
        _table(head, rows)])


def _recent(verif, order):
    days = [d for d in verif.get("days", []) if d.get("models")][-RECENT_DAYS:]
    if not days:
        return ""
    obs_rows = []
    for d in days:
        o = d.get("obs", {})
        pend = d.get("obs_pending") or []
        cells = []
        for v in VARS:
            x = o.get(v)
            txt = "—" if x is None else _f(x, v) if v == "precip_in" else f"{x:g}"
            cells.append(("~" if v in pend else "") + txt)
        obs_rows.append([d["date"] + (" (hindcast)" if d.get("hindcast") else ""), *cells])
    names = [n for n in order if any(n in d["models"] for d in days)]
    err_rows, pts_rows = [], []
    for n in names:
        errs, pts = [n], [n]
        for d in days:
            s = d["models"].get(n)
            if not s:
                errs.append("—"); pts.append("—")
                continue
            e = s.get("error", {})
            errs.append("/".join(_s(e[v], v, None if v == "precip_in" else 0) if e.get(v) is not None
                                 else "?" for v in VARS))
            pts.append(f"{s['points']:.1f}" if s.get("points") is not None else "—")
        err_rows.append(errs)
        pts_rows.append(pts)
    dates = [d["date"][5:] for d in days]
    return "\n".join([
        f"## Recent days (last {len(days)} verified)", "",
        "Observed (~ = still preliminary):", "",
        _table(["Date", *VAR_NAMES.values()], obs_rows),
        "", "Errors as forecast - observed, high/low/wind/precip:", "",
        _table(["Model", *dates], err_rows),
        "", "Error points per day:", "",
        _table(["Model", *dates], pts_rows)])


def _today(today):
    if not today or not today.get("models"):
        return ""
    o = today.get("obs", {})
    rows = []
    for n, m in today["models"].items():
        def hl(key):
            f, e = m.get(f"{key}_fcst"), m.get(f"{key}_err")
            if f is None:
                return "—"
            txt = f"{f:.0f} ({_s(e, 't', 0)})" if e is not None else f"{f:.0f}"
            return txt + (" pending" if m.get(f"{key}_pending") else "")
        rows.append([n, _hhz(m.get("init_time_utc")), _s(m.get("temp_bias"), "t"),
                     _f(m.get("temp_mae"), "t"), hl("high"), hl("low"), _s(m.get("wind_bias"), "w"),
                     _f(m.get("precip_so_far"), "precip_in"), _s(m.get("precip_err"), "precip_in")])
    return "\n".join([
        f"## Today so far ({today.get('date')}, through {today.get('through_utc')}Z)", "",
        "This is the day in progress (not the target day), scored against the runs submitted before "
        "its deadline. Observed so far: "
        f"high {_f(o.get('high'), 't')} °F, low {_f(o.get('low'), 't')} °F, max wind {o.get('wind', '—')} kt, "
        f"precip {_f(o.get('precip'), 'precip_in')}\" ({o.get('n_obs', '?')} hourly obs).", "",
        "Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value "
        "and (in brackets) its difference from the observed extreme so far; \"pending\" means the "
        "model's expected time of that extreme hasn't passed, so the observed value can still change.", "",
        _table(["Model", "Run", "Temp bias", "Temp MAE", "High (err)", "Low (err)", "Wind bias",
                "Precip so far", "Precip err"], rows, right_from=2)])


def _links():
    d = f"{SITE}/data/wxchallenge"
    return "\n".join([
        "## Raw data", "",
        f"- Forecast (all models, ensemble members, consensus weights): {d}/forecast.json",
        f"- Verification (every day, every model, observations, PoP calibration): {d}/verification.json",
        f"- Today so far: {d}/today.json",
        f"- Human page: {SITE}/wxchallenge/",
    ])


def build_brief(fc: dict, verif: dict, today: dict | None = None, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    order = _model_order(fc, verif)
    sections = [_header(fc, now), _howto(), _scoring(), _guidance(fc, order), _consensus(fc),
                _ensembles(fc, order), _pop(fc, verif, order), _track_record(verif),
                _recent(verif, order), _today(today), _links()]
    return "\n\n".join(s for s in sections if s) + "\n"


def write_brief(data_dir: Path = DATA, out: Path | None = None) -> Path:
    """Read the published JSON files from data_dir and write brief.md next to them."""
    data_dir = Path(data_dir)

    def load(name):
        p = data_dir / name
        return json.loads(p.read_text()) if p.exists() else None

    fc, verif, today = load("forecast.json"), load("verification.json") or {}, load("today.json")
    if not fc:
        raise FileNotFoundError(data_dir / "forecast.json")
    # today.json can be left over from another station or an earlier day; only use it when it matches
    if today and today.get("station") not in (None, fc["meta"].get("station")):
        today = None
    out = Path(out or data_dir / "brief.md")
    out.write_text(build_brief(fc, verif, today), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(f"Wrote {write_brief()}")
