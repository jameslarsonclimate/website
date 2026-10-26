"""
A compact, plain-text (Markdown) brief of the WxChallenge data for AI assistants.

The page renders its tables with JavaScript, so a tool that fetches the page without running
scripts sees only "Loading…". This module condenses forecast.json, verification.json and
today.json into data/wxchallenge/brief.md (a few KB): the target day's guidance, the
consensus and its weights, ensemble spread, precip chances, each model's track record this
period, recent days' errors, each scored run's cloud forecast vs the observed clouds
(cloud_context.json; context only, not scored), and how today is going so far, plus the
scoring rules and a short method for turning it all into a forecast.

The brief is not linked visibly on the page: llms.txt at the site root and a visually
hidden link at the bottom of wxchallenge/index.html point to it.
"""

import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "wxchallenge"
BRIEF = DATA / "brief.md"
SITE = "https://jameslarsonclimate.github.io/website/weather-forecasts"

VARS = ["tmax_f", "tmin_f", "wind_max_kt", "precip_in"]
VAR_NAMES = {"tmax_f": "High °F", "tmin_f": "Low °F", "wind_max_kt": "Wind kt", "precip_in": 'Precip in'}
ENS_VARS = {"tmax_f": "High °F", "tmin_f": "Low °F", "wind_max_kt": "Wind kt", "precip_in": "Precip in"}
BLOCKS = ["06-12", "12-18", "18-00", "00-06"]
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


def _rh(t, td):
    """Relative humidity (%) from temperature and dewpoint (°F), Magnus formula over water
    (the same as the page's timeline)."""
    if t is None or td is None:
        return None
    es = lambda f: math.exp(17.625 * ((f - 32) / 1.8) / (243.04 + (f - 32) / 1.8))
    return min(100.0, 100 * es(min(td, t)) / es(t))


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
        "1. Look at all model forecasts for the target day, then the **CONSENSUS** row.",
        "2. Check the track-record table. A model with a large, consistent bias (|bias| close to "
        "its MAE) is reliably off in that direction. The consensus tries to remove some of that bias.",
        "3. For precip, enter roughly the ensemble **median**, not the mean: errors are charged per "
        "0.01\" and most heavily near zero. When the calibrated chances (NBM, NBM QMD, MOS) are low, "
        "0.00 is often the best entry.",
        "4. Use \"Today so far\" (the day currently in progress, not the target day) to see which "
        "models are handling the current pattern; persistent errors there often carry into the "
        "target day.",
        "5. Think about what might be missing from the data or what would be helpful to know. Start "
        "with the cloud and dewpoint sections (too clear at night -> low too cold; too moist -> low "
        "too warm). If anything of note, suggest what to look for on the GOES or model spatial maps "
        "to nudge the forecast one way or another.",
        "6. Read the latest AFD for the forecaster's view of the pattern.",
        "7. Give whole °F for high/low, whole kt for wind, and precip to 0.01\". State your "
        "reasoning, especially for any departure from the consensus.",
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
    out += ["", "GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg "
            "open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) "
            "and NBM QMD are not in the consensus either; they inform the precip choice."]
    return "\n".join(out)


def _consensus(fc):
    c = fc["models"].get("CONSENSUS")
    if not c or not c.get("method"):
        return ""
    out = ["## Consensus method", ""]
    methods = {}
    for v in VARS:
        if c["method"].get(v):
            methods.setdefault(c["method"][v].get("method"), []).append(VAR_NAMES[v].split()[0])
    for m, names in methods.items():
        label = f"{', '.join(names)}: " if len(methods) > 1 else ""
        out.append(f"- {label}{m}.")
    out.append("- Precip is weighted but not bias-corrected.")
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
        if d.get("excluded_stale"):
            line += f" (stale runs excluded: {', '.join(d['excluded_stale'])})"
        if d.get("proxy_track_record"):
            line += " (using parent's track record: " + ", ".join(
                f"{n} from {p}" for n, p in d["proxy_track_record"].items()) + ")"
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


def _daily(verif, order):
    """Every verified day this period: one table of error points, then one per variable with the
    observation and each model's error (the page's verification tabs, one row per day)."""
    days = [d for d in verif.get("days", []) if d.get("models")]
    if not days:
        return ""
    names = [n for n in order if any(n in d["models"] for d in days)]
    label = {d["date"]: d["date"][5:] + (" h" if d.get("hindcast") else "") for d in days}

    pts_rows = []
    for d in days:
        pts = {n: s.get("points") for n, s in d["models"].items() if s.get("points") is not None}
        best = min(pts, key=pts.get) if pts else "—"
        pts_rows.append([label[d["date"]], *(f"{pts[n]:.1f}" if n in pts else "—" for n in names), best])
    out = [
        f"## Daily verification (all {len(days)} days this period)", "",
        "One row per day; \"h\" = hindcast day (before the first forecast day for this city). "
        "On hindcast days the CONSENSUS is reconstructed: what the current method would have "
        "submitted using only the earlier days' track record.", "",
        "Error points (lower is better):", "",
        _table(["Date", *names, "Best"], pts_rows)]

    for v in VARS:
        rows = []
        for d in days:
            ob = d.get("obs", {}).get(v)
            ob_txt = "—" if ob is None else _f(ob, v) if v == "precip_in" else f"{ob:g}"
            if v in (d.get("obs_pending") or []):
                ob_txt = "~" + ob_txt
            cells = []
            for n in names:
                e = (d["models"].get(n) or {}).get("error", {}).get(v)
                cells.append("—" if e is None else _s(e, v, None if v == "precip_in" else 0))
            rows.append([label[d["date"]], ob_txt, *cells])
        out += ["", f"{VAR_NAMES[v]}: observed (~ = still preliminary) and each model's error "
                "(forecast - observed, as submitted):", "",
                _table(["Date", "Obs", *names], rows)]
    return "\n".join(out)


def _clouds(verif, clouds, order):
    """Each scored run's cloud forecast vs the observed clouds (cloud_context.json), by night and
    day: context for the high / low misses, never scored."""
    days = [d for d in verif.get("days", []) if d.get("models")]
    if not clouds or not days:
        return ""
    ctx = {d["date"]: clouds.get(d["date"]) or {} for d in days}
    err = lambda d, n, k: ((ctx[d["date"]].get("models") or {}).get(n) or {}).get(f"{k}_err")  # noqa: E731
    names = [n for n in order if any(err(d, n, k) is not None for d in days for k in ("night", "day"))]
    if not names:
        return ""
    label = {d["date"]: d["date"][5:] + (" h" if d.get("hindcast") else "") for d in days}

    rows = []
    for n in names:
        cells, n_days = [], 0
        for k, wv in (("night", "tmin_f"), ("day", "tmax_f")):   # weighted like the low / high
            pairs = [(err(d, n, k), (d.get("decay_weight") or {}).get(wv, 1.0)) for d in days]
            pairs = [(e, w) for e, w in pairs if e is not None]
            n_days = max(n_days, len(pairs))
            if pairs:
                sw = sum(w for _, w in pairs)
                cells += [_s(sum(e * w for e, w in pairs) / sw, None, 0),
                          f"{sum(abs(e) * w for e, w in pairs) / sw:.0f}"]
            else:
                cells += ["—", "—"]
        rows.append([n, n_days, *cells])
    out = [
        "## Clouds (context only, not scored)", "",
        "Each scored run's total cloud cover vs the observed cloud cover, in percentage points "
        "(forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours "
        "from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = "
        "METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations "
        "see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over "
        "the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the "
        "METAR value. At night the satellite mask relies on infrared and often misses low stratus "
        "and fog. — = no data (e.g. a station outage, or a model without a "
        "cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).", "",
        _table(["Model", "Days", "Night bias", "Night MAE", "Day bias", "Day MAE"], rows)]
    for k, title in (("night", "Night clouds"), ("day", "Day clouds")):
        rows = []
        for d in days:
            ob = (ctx[d["date"]].get("obs") or {}).get(f"{k}_pct")
            goes = (ctx[d["date"]].get("obs") or {}).get(f"goes_{k}_pct")
            rows.append([label[d["date"]], "—" if ob is None else f"{ob:.0f}%",
                         "—" if goes is None else f"{goes:.0f}%",
                         *("—" if err(d, n, k) is None else _s(err(d, n, k), None, 0) for n in names)])
        out += ["", f"{title}: observed and each model's error (forecast - observed, percentage points):", "",
                _table(["Date", "Obs", "GOES", *names], rows)]
    return "\n".join(out)


MIN_COVER = 0.5      # a window mean needs at least this share of its hours (as the cloud context)


def _lerp(hs, vs, h):
    """Linear interpolation of a series (hours, values) at hour h; None outside it or at a gap."""
    for i in range(len(hs) - 1):
        if hs[i] <= h <= hs[i + 1]:
            a, b = vs[i], vs[i + 1]
            if h == hs[i]:
                return a
            if h == hs[i + 1]:
                return b
            return None if a is None or b is None else a + (h - hs[i]) / (hs[i + 1] - hs[i]) * (b - a)
    return vs[0] if len(hs) == 1 and hs[0] == h else None


def _model_window(m, win):
    """Mean of a model's dewpoint over the window's whole hours [first, last] (hours since 06Z),
    interpolated to each hour so 3- and 6-hourly runs count every hour."""
    hs, vs = m.get("h") or [], m.get("td") or []
    if not win or len(hs) != len(vs):
        return None
    pts = sorted((h, v) for h, v in zip(hs, vs) if v is not None)
    hours = range(round(win[0]), round(win[1]) + 1)
    got = [x for x in (_lerp([h for h, _ in pts], [v for _, v in pts], j) for j in hours) if x is not None]
    return sum(got) / len(got) if got and len(got) >= MIN_COVER * len(hours) else None


def _obs_window(reports, win):
    """Mean observed dewpoint over the window: per hour, the report nearest the top of the hour
    within 35 minutes."""
    hs, vs = (reports or {}).get("h") or [], (reports or {}).get("td") or []
    if not win or len(hs) != len(vs):
        return None
    hours = range(round(win[0]), round(win[1]) + 1)
    got = []
    for j in hours:
        near = [(abs(h - j), v) for h, v in zip(hs, vs) if v is not None and abs(h - j) <= 35 / 60]
        if near:
            got.append(min(near)[1])
    return sum(got) / len(got) if got and len(got) >= MIN_COVER * len(hours) else None


def _dewpoints(verif, timeline, order):
    """Each scored run's dewpoint vs the observed dewpoint by night and day (from the page's
    timeline.json, the same windows as the cloud section): context, never scored."""
    days = [d for d in verif.get("days", []) if d.get("models")]
    tl = {d["date"]: d for d in (timeline or {}).get("days") or []}
    if not days or not tl:
        return ""
    obs, err = {}, {}             # (date, night/day) -> observed mean; (date, model, night/day) -> error
    for d in days:
        t = tl.get(d["date"]) or {}
        win = t.get("cloud_win") or {}
        for k in ("night", "day"):
            o = _obs_window((t.get("obs") or {}).get("reports"), win.get(k))
            obs[d["date"], k] = o
            for n, m in (t.get("models") or {}).items():
                f = _model_window(m, win.get(k))
                if o is not None and f is not None:
                    err[d["date"], n, k] = f - o
    names = [n for n in order if any((d["date"], n, k) in err for d in days for k in ("night", "day"))]
    if not names:
        return ""
    label = {d["date"]: d["date"][5:] + (" h" if d.get("hindcast") else "") for d in days}

    rows = []
    for n in names:
        cells, n_days = [], 0
        for k, wv in (("night", "tmin_f"), ("day", "tmax_f")):   # weighted like the low / high
            pairs = [(err[d["date"], n, k], (d.get("decay_weight") or {}).get(wv, 1.0))
                     for d in days if (d["date"], n, k) in err]
            n_days = max(n_days, len(pairs))
            if pairs:
                sw = sum(w for _, w in pairs)
                cells += [_s(sum(e * w for e, w in pairs) / sw, "t"),
                          f"{sum(abs(e) * w for e, w in pairs) / sw:.1f}"]
            else:
                cells += ["—", "—"]
        rows.append([n, n_days, *cells])
    out = [
        "## Dewpoint (context only, not scored)", "",
        "Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: "
        "positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, "
        "drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = "
        "the METAR nearest each hour; models are interpolated to every hour. A model that runs too "
        "moist at night tends to hold its low too warm, too dry to drop it too far. — = no data "
        "(the ensembles and USL only from when their dewpoints were kept). Bias / MAE "
        "are decay-weighted like the low (night) and high (day).", "",
        _table(["Model", "Days", "Night bias", "Night MAE", "Day bias", "Day MAE"], rows)]
    for k, title in (("night", "Night dewpoint"), ("day", "Day dewpoint")):
        rows = [[label[d["date"]], _f(obs[d["date"], k], "t"),
                 *(_s(err[d["date"], n, k], "t") if (d["date"], n, k) in err else "—" for n in names)]
                for d in days]
        out += ["", f"{title}: observed mean (°F) and each model's error (forecast - observed, °F):", "",
                _table(["Date", "Obs", *names], rows)]
    return "\n".join(out)


def _pop_daily(verif, order):
    """Each verified day's 6-hour precip chances against what happened."""
    pv = verif.get("pop") or {}
    days = pv.get("days") or []
    if not days:
        return ""
    names = [n for n in order if any(n in d.get("models", {}) for d in days)]

    def chances(m):
        if not m:
            return "—"
        b = m.get("blocks") or {}
        if any(b.get(k) is not None for k in BLOCKS):
            return "/".join("—" if b.get(k) is None else f"{round(100 * b[k])}" for k in BLOCKS)
        return f"24h {_pct(m.get('p24'))}" if m.get("p24") is not None else "—"

    rows = []
    for d in days:
        ob = d.get("obs", {})
        wet = [k for k in BLOCKS if ob.get(k)]
        rows.append([d["date"][5:], f"{_f(d.get('precip_in'), 'precip_in')}\" " +
                     (f"(wet: {', '.join(wet)})" if wet else "(dry)"),
                     *(chances(d["models"].get(n)) for n in names)])
    return "\n".join([
        "## Daily verification of precip chances", "",
        f"Chance (%) of ≥{pv.get('event_in', 0.01):g}\" in each 6-hour block, "
        f"{'/'.join(BLOCKS)} UTC, against the observed precip and which blocks were wet.", "",
        _table(["Date", "Observed", *names], rows, right_from=2)])


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


def _today_clouds(fc, cloud_today, order):
    """Hourly clouds of the day in progress: GOES and METAR against the runs submitted for it."""
    if not cloud_today:
        return ""
    goes = {r["hour"]: r.get("cloud_pct") for r in cloud_today.get("goes") or [] if r.get("hour")}
    metar = {r["hour"]: r.get("sky_pct") for r in cloud_today.get("metar") or [] if r.get("hour")}
    if not goes and not metar:
        return ""
    models = cloud_today.get("models") or {}
    names = [n for n in order if n in models] + [n for n in models if n not in order]
    cells = {}
    for n in names:
        c = models[n]
        avg = c.get("averaged") or [False] * len(c.get("times") or [])
        cells[n] = {t: _cloud_cell(x, a) for t, x, a in zip(c.get("times") or [], c.get("cloud_pct") or [], avg)}
    tz = _station_tz(fc)
    hours = sorted(set(goes) | set(metar))
    rows = [[f"{t[5:10]} {t[11:13]}Z", _local(t, tz), _cloud_cell(goes.get(t)), _cloud_cell(metar.get(t)),
             *(cells[n].get(t, "") for n in names)] for t in hours]
    sat = next((r.get("satellite") for r in cloud_today.get("goes") or [] if r.get("satellite")), None)
    return "\n".join([
        f"## Clouds so far today ({cloud_today.get('date')}, observed vs forecast)", "",
        f"Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within "
        f"15 km of the station ({'GOES-' + sat[1:] + ' ' if sat else ''}Clear Sky Mask, the scan nearest "
        "the top of the hour); at night it relies on infrared and often misses low stratus and fog, so "
        "trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, "
        "OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. "
        "Model columns are the runs submitted for today (* = averaged over the preceding interval). "
        "Context only, not scored.", "",
        _table(["UTC", f"Local ({_zone(hours[0], tz)})" if tz else "Local", "GOES", "METAR", *names],
               rows, right_from=2)])


def _today_humidity(fc, obs, sub, order):
    """Hourly dewpoint of the day in progress: the METAR nearest each hour (and its RH) against the
    runs submitted for today, with each model's mean dewpoint error so far."""
    r = (obs or {}).get("reports") or {}
    times, td, temp = r.get("times") or [], r.get("dewpt_f") or [], r.get("temp_f") or []
    if not times or len(td) != len(times):
        return ""
    best = {}              # top of the hour -> (minutes away, dewpoint, temperature)
    for t, d, x in zip(times, td, temp or [None] * len(times)):
        if d is None:
            continue
        ts = datetime.strptime(t, "%Y-%m-%dT%H:%M")
        hour = (ts + timedelta(minutes=30)).replace(minute=0)
        away = abs((ts - hour).total_seconds()) / 60
        key = hour.strftime("%Y-%m-%dT%H:%M")
        if away <= 35 and (key not in best or away < best[key][0]):
            best[key] = (away, d, x)
    if not best:
        return ""
    models = (sub or {}).get("models") or {}
    names = [n for n in order if n in models] + [n for n in models if n not in order]
    names = [n for n in names if any(v is not None for v in models[n].get("dewpt_f") or [])]
    fc_td = {n: dict(zip(models[n]["times"], models[n]["dewpt_f"])) for n in names}
    tz = _station_tz(fc)
    hours = sorted(best)
    rows = [[f"{t[5:10]} {t[11:13]}Z", _local(t, tz), _f(best[t][1], "t"),
             "" if (rh := _rh(best[t][2], best[t][1])) is None else f"{rh:.0f}",
             *("" if fc_td[n].get(t) is None else _f(fc_td[n][t], "t") for n in names)] for t in hours]
    bias = []
    for n in names:
        errs = [fc_td[n][t] - best[t][1] for t in hours if fc_td[n].get(t) is not None]
        bias.append(_s(sum(errs) / len(errs), "t") if errs else "—")
    rows.append(["Bias so far", "", "", "", *bias])
    return "\n".join([
        f"## Dewpoint so far today ({(obs or {}).get('date')}, observed vs forecast)", "",
        "Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of "
        "the runs submitted for today. Bias so far = forecast - observed over the hours both have "
        "(positive = too moist). A model running too moist often runs its low too warm, too dry its "
        "low too cold. Context only, not scored.", "",
        _table(["UTC", f"Local ({_zone(hours[0], tz)})" if tz else "Local", "Obs Td", "Obs RH", *names],
               rows, right_from=2)])


def _links(fc):
    d = f"{SITE}/data/wxchallenge"
    meta = fc.get("meta", {})
    afd = ([f"- NWS Area Forecast Discussion ({meta.get('wfo')}): {meta['afd_url']}"]
           if meta.get("afd_url") else [])
    return "\n".join([
        "## Raw data", "",
        f"- Forecast (all models, ensemble members, consensus weights): {d}/forecast.json",
        f"- Verification (every day, every model, observations, PoP calibration): {d}/verification.json",
        f"- Today so far: {d}/today.json",
        f"- Cloud forecast vs observed per scored run (not scored): {d}/cloud_context.json",
        *afd,
        f"- Human page: {SITE}/wxchallenge/",
    ])


def _station_tz(fc):
    tz = fc.get("meta", {}).get("tz")
    if not tz:   # forecast.json written before "tz" was added to its meta
        try:
            import wxc_stations
            st = wxc_stations.STATIONS.get(fc["meta"].get("station"))
            tz = st.tz if st else None
        except Exception:
            tz = None
    try:
        return ZoneInfo(tz) if tz else None
    except Exception:
        return None


def _local(t, tz):
    """'2026-10-15T06:00' (UTC) -> 'Wed 23:00' in the station's zone ('' without one)."""
    if not tz:
        return ""
    return datetime.fromisoformat(t).replace(tzinfo=timezone.utc).astimezone(tz).strftime("%a %H:%M")


def _zone(t, tz):
    """The zone's name at UTC time t (DST can change between now and the target day)."""
    return datetime.fromisoformat(t).replace(tzinfo=timezone.utc).astimezone(tz).strftime("%Z") if tz else ""


def _cloud_cell(x, avg=False):
    return "" if x is None else f"{x:.0f}" + ("*" if avg else "")


def _hourly(fc, series, order, cloud_series=None):
    """The models' hourly (or 3-/6-hourly) values through the target day, one table per variable
    (temperature, dewpoint, RH, wind, accumulated precip, cloud cover): a row per UTC hour, a column per model,
    blank where a model has no value at that hour."""
    models = (series or {}).get("models") or {}
    clouds = (cloud_series or {}).get("models") or {}

    def ordered(d):
        return [n for n in order if n in d] + [n for n in d if n not in order]

    # (title, {model: {time: cell text}}) per table, models in page order
    tables = []
    specs = [("temp_f", "Temperature (°F)", "t"), ("dewpt_f", "Dewpoint (°F)", "t"),
             ("wind_kt", "Wind speed (kt) at the hour", "w"),
             ("precip_in", "Precipitation (in), accumulated since the start of the day (06Z)", "precip_in")]
    dry_note = None
    for key, title, v in specs:
        cols = [n for n in ordered(models) if any(x is not None for x in (models[n].get(key) or []))]
        if not cols:
            continue
        raw = {n: dict(zip(models[n]["times"], models[n][key])) for n in cols}
        if key == "precip_in" and all((x or 0) < 0.005 for n in cols for x in raw[n].values()):
            dry_note = (len(tables), f"{title}: 0.00 in every model ({', '.join(cols)}) all day.")
            continue
        tables.append((title, {n: {t: _f(x, v) for t, x in raw[n].items() if x is not None} for n in cols}))
        if key == "dewpt_f":            # RH from each model's own temperature and dewpoint
            rh = {}
            for n in cols:
                temp = dict(zip(models[n]["times"], models[n].get("temp_f") or []))
                own = dict(zip(models[n]["times"], models[n].get("rh_pct") or []))   # ensembles: members' mean
                cells = {t: f"{r:.0f}" for t, x in raw[n].items()
                         if (r := own[t] if own.get(t) is not None else _rh(temp.get(t), x)) is not None}
                if cells:
                    rh[n] = cells
            if rh:
                tables.append(("Relative humidity (%), from each model's temperature and dewpoint "
                               "(ensembles: the mean of their members' RH)", rh))
    cloud_cols = [n for n in ordered(clouds) if any(x is not None for x in (clouds[n].get("cloud_pct") or []))]
    if cloud_cols:
        cells = {}
        for n in cloud_cols:
            c = clouds[n]
            avg = c.get("averaged") or [False] * len(c["times"])
            cells[n] = {t: _cloud_cell(x, a) for t, x, a in zip(c["times"], c["cloud_pct"], avg) if x is not None}
        tables.append(("Total cloud cover (%)", cells))
    if not tables and not dry_note:
        return ""

    tz = _station_tz(fc)
    hours = sorted({t for _, cells in tables for d in cells.values() for t in d}
                   | {t for n in models for t in models[n].get("times") or []})
    zone = _zone(hours[0], tz) if hours else ""

    gen = (series or cloud_series or {}).get("generated_at_utc")
    src = "" if gen == fc.get("generated_at_utc") else f" (from the run at {gen})"
    out = [f"## Hourly guidance through the target day{src}", "",
           "Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, "
           "USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, "
           "AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can "
           "miss the true high/low between output times; the guidance table's daily values "
           "(which also use interval max/min fields where available) are what get scored."]
    if any(title.startswith("Dewpoint") for title, _ in tables):
        out += ["", "Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint "
                "(GFS_MOS, NBM and USL from their own guidance; ENS, AIFS_ENS and GEFS the mean of "
                "their members). Moist air "
                "(a high dewpoint) slows the overnight cooling, and the low rarely falls far below the "
                "evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible."]
    if cloud_cols:
        out += ["", "Cloud cover (context, not scored): total cloud cover from each model's own "
                "output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, "
                "overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval "
                "rather than instantaneous. Clouds overnight hold the low up; clouds by day hold "
                "the high down."]
    for i, (title, cells) in enumerate(tables):
        if dry_note and dry_note[0] == i:
            out += ["", dry_note[1]]
        cols = list(cells)
        rows = []
        for t in hours:
            row = [cells[n].get(t, "") for n in cols]
            if any(row):
                rows.append([f"{t[5:10]} {t[11:13]}Z", _local(t, tz), *row])
        head = ["UTC", f"Local ({zone})" if tz else "Local", *cols]
        out += ["", f"{title}:", "", _table(head, rows, right_from=2)]
    if dry_note and dry_note[0] >= len(tables):
        out += ["", dry_note[1]]
    return "\n".join(out)


def build_brief(fc: dict, verif: dict, today: dict | None = None, now: datetime | None = None,
                clouds: dict | None = None, series: dict | None = None,
                cloud_series: dict | None = None, cloud_today: dict | None = None,
                obs_today: dict | None = None, series_today: dict | None = None,
                timeline: dict | None = None) -> str:
    """clouds: this station's days from cloud_context.json ({date: {...}}), optional.
    series: the target day's hourly model series (series/<ICAO>_<date>_submitted.json), optional.
    cloud_series: the target day's model cloud cover (cloud_forecast.json), optional.
    cloud_today: the day in progress's observed (GOES, METAR) and forecast clouds (cloud_today.json).
    obs_today / series_today: the day in progress's METARs (timeline/<ICAO>_<date>_obs.json) and
    submitted runs (series/<ICAO>_<date>_submitted.json), for its dewpoint so far.
    timeline: the page's timeline.json (the past days' dewpoints)."""
    now = now or datetime.now(timezone.utc)
    order = _model_order(fc, verif)
    sections = [_header(fc, now), _howto(), _scoring(), _guidance(fc, order), _consensus(fc),
                _ensembles(fc, order), _pop(fc, verif, order), _hourly(fc, series, order, cloud_series),
                _track_record(verif),
                _daily(verif, order), _clouds(verif, clouds, order), _dewpoints(verif, timeline, order),
                _pop_daily(verif, order),
                _today(today), _today_clouds(fc, cloud_today, order),
                _today_humidity(fc, obs_today, series_today, order), _links(fc)]
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
    # cloud context (display only): this station's days, if the file exists
    clouds = ((load("cloud_context.json") or {}).get("stations") or {}).get(fc["meta"].get("station")) or None
    # hourly series written by this same run for the target day
    meta = fc["meta"]
    series = load(f"series/{meta.get('station')}_{meta.get('target_date')}_submitted.json")
    cloud_series = load("cloud_forecast.json")
    if cloud_series and (cloud_series.get("station"), cloud_series.get("target_date")) != \
            (meta.get("station"), meta.get("target_date")):
        cloud_series = None          # left over from an earlier day or another city
    cloud_today = load("cloud_today.json")
    if cloud_today and (cloud_today.get("station") != meta.get("station")
                        or (today and cloud_today.get("date") != today.get("date"))):
        cloud_today = None
    # the day in progress's METARs and submitted runs (its dewpoint so far)
    obs_today = series_today = None
    if today and today.get("date"):
        obs_today = load(f"timeline/{meta.get('station')}_{today['date']}_obs.json")
        series_today = load(f"series/{meta.get('station')}_{today['date']}_submitted.json")
    timeline = load("timeline.json")
    if timeline and timeline.get("station") != meta.get("station"):
        timeline = None              # another city's
    out = Path(out or data_dir / "brief.md")
    out.write_text(build_brief(fc, verif, today, clouds=clouds, series=series,
                                  cloud_series=cloud_series, cloud_today=cloud_today,
                                  obs_today=obs_today, series_today=series_today,
                                  timeline=timeline), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(f"Wrote {write_brief()}")
