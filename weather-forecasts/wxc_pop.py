"""
Probability of precipitation (PoP) for the WxChallenge day (06Z-06Z): one record per source,
and its verification. DISPLAY / LEARNING ONLY: never part of the consensus or the scoring.

Event: verified precip >= 0.01" (a trace scores as 0.00, so it is dry). PoP is given for the
24-h day and for the four 6-h blocks 06-12, 12-18, 18-00 and 00-06Z (MOS P06 periods).

Record (stored per model in forecast.json and, for live runs, runs.jsonl under "pop"):
  p24        24-h PoP (0-1), or None when the source only has 6-h PoPs
  p24_range  [max(p), 1 - prod(1 - p)] of the four 6-h PoPs: the bounds of the 24-h PoP when
             only 6-h PoPs exist (MOS). Neither bound is "the" 24-h PoP.
  blocks     {"06-12": p or None, ...}
  n_members  ensemble size (member fractions are raw and uncalibrated), None otherwise
  basis      short description ("MOS P06", "member fraction", "NBM QMD")
  q24_in     NBM QMD only: unconditional 24-h precip percentiles (inches) {"10": .., "50": ..};
             the 50% level is the value that minimises expected WxChallenge precip points
"""

import math
from datetime import date, datetime, timedelta, timezone
from typing import Optional

EVENT_IN = 0.01
BLOCKS = [("06-12", 6), ("12-18", 12), ("18-00", 18), ("00-06", 24)]   # label, start hour after 00Z D
BLOCK_LABELS = [b for b, _ in BLOCKS]
REL_BINS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0000001]


def block_windows(day: date) -> list:
    """[(label, start, end)] in UTC (naive datetimes) for WxChallenge day `day`."""
    d0 = datetime(day.year, day.month, day.day)
    return [(lab, d0 + timedelta(hours=h), d0 + timedelta(hours=h + 6)) for lab, h in BLOCKS]


def block_of_hour_ending(ts) -> str:
    """Block of the hour ending at `ts`: 07..12Z -> 06-12, 13..18Z -> 12-18, 19..00Z -> 18-00,
    01..06Z -> 00-06."""
    h = ts.hour
    if 7 <= h <= 12:
        return "06-12"
    if 13 <= h <= 18:
        return "12-18"
    if h >= 19 or h == 0:
        return "18-00"
    return "00-06"


def p24_bounds(blocks: dict) -> Optional[list]:
    ps = [blocks.get(b) for b in BLOCK_LABELS]
    if any(p is None for p in ps):
        return None
    return [round(max(ps), 3), round(1 - math.prod(1 - p for p in ps), 3)]


def record(p24=None, blocks=None, n_members=None, basis="", q24_in=None, bounds=False) -> Optional[dict]:
    """A PoP record; bounds=True adds p24_range from the 6-h blocks (sources without a 24-h PoP)."""
    blocks = {b: (None if (blocks or {}).get(b) is None else round(float(blocks[b]), 3)) for b in BLOCK_LABELS}
    if p24 is None and all(v is None for v in blocks.values()):
        return None
    rec = {"p24": None if p24 is None else round(float(p24), 3), "blocks": blocks,
           "n_members": n_members, "basis": basis}
    if bounds:
        rec["p24_range"] = p24_bounds(blocks)
    if q24_in:
        rec["q24_in"] = q24_in
    return rec


def wet(x) -> bool:
    return x is not None and x >= EVENT_IN - 1e-9


def from_members(day_totals: list, block_totals: Optional[dict] = None, basis="member fraction") -> Optional[dict]:
    """Member fractions: day_totals = each member's 24-h precip (in); block_totals = {block: [per
    member]} (None or missing blocks when the source has no sub-daily data)."""
    vals = [v for v in day_totals if v is not None and math.isfinite(v)]
    if not vals:
        return None
    frac = lambda xs: sum(wet(x) for x in xs) / len(xs)  # noqa: E731
    blocks = {}
    for b in BLOCK_LABELS:
        xs = [x for x in (block_totals or {}).get(b) or [] if x is not None and math.isfinite(x)]
        blocks[b] = frac(xs) if xs else None
    return record(frac(vals), blocks, n_members=len(vals), basis=basis)


# ----------------------------------------------------------------------------
# verification (live runs only; no PoP hindcasts)
# ----------------------------------------------------------------------------
def _deadline(day: str) -> datetime:
    return datetime.fromisoformat(day).replace(tzinfo=timezone.utc)


def pop_for_day(runs: list, station: str, day: str) -> dict:
    """{model: (pop record, run time)} from the last live pre-deadline run that has a PoP."""
    out = {}
    for r in sorted((r for r in runs if r["station"] == station and r["target_date"] == day
                     and not r.get("hindcast") and datetime.fromisoformat(r["generated_at_utc"]) < _deadline(day)),
                    key=lambda r: r["generated_at_utc"]):
        for name, m in r["models"].items():
            if m.get("pop"):
                out[name] = (m["pop"], r["generated_at_utc"])
    return out


def observed(ob: dict) -> dict:
    """Outcomes (1 wet / 0 dry / None unknown) for the 24-h day and each block."""
    blocks = ob.get("precip_6h_in") or {}
    return {"24h": None if ob.get("precip_in") is None else int(wet(ob["precip_in"])),
            **{b: None if blocks.get(b) is None else int(wet(blocks[b])) for b in BLOCK_LABELS}}


def brier(pairs: list) -> Optional[float]:
    return round(sum((p - o) ** 2 for p, o in pairs) / len(pairs), 4) if pairs else None


def _reliability(pairs: list) -> list:
    out = []
    for lo, hi in zip(REL_BINS, REL_BINS[1:]):
        sel = [(p, o) for p, o in pairs if lo <= p < hi]
        out.append({"bin": [round(lo, 1), round(min(hi, 1.0), 1)], "n": len(sel),
                    "mean_p": round(sum(p for p, _ in sel) / len(sel), 3) if sel else None,
                    "obs_freq": round(sum(o for _, o in sel) / len(sel), 3) if sel else None})
    return out


def verify_pop(runs: list, obs: list, station: str, start: Optional[str] = None) -> dict:
    """
    Per-day PoP and outcomes for `station` since `start` (the scoreboard's PoP tab), Brier scores
    per source (24-h and 6-h blocks), and reliability pooled over every stored day of every city.
    MOS has no 24-h PoP (only bounds), so it is scored on its 6-h blocks only.
    """
    def collect(st, since):
        rows = []
        for o in sorted((o for o in obs if o["station"] == st and o.get("complete", True)
                         and (not since or o["date"] >= since)), key=lambda o: o["date"]):
            rows.append((o, observed(o), pop_for_day(runs, st, o["date"])))
        return rows

    days, per = [], {}
    for o, out, pops in collect(station, start):
        if not pops:
            continue
        days.append({"date": o["date"], "obs": out, "precip_in": o.get("precip_in"),
                     "precip_6h_in": o.get("precip_6h_in"),
                     "models": {k: {"p24": p.get("p24"), "p24_range": p.get("p24_range"),
                                    "blocks": p.get("blocks"), "n_members": p.get("n_members")}
                                for k, (p, _) in pops.items()}})
        for k, (p, _) in pops.items():
            s = per.setdefault(k, {"d": [], "b": []})
            if p.get("p24") is not None and out["24h"] is not None:
                s["d"].append((p["p24"], out["24h"]))
            for b in BLOCK_LABELS:
                pb = (p.get("blocks") or {}).get(b)
                if pb is not None and out[b] is not None:
                    s["b"].append((pb, out[b]))
    summary = {}
    for k, s in per.items():
        summary[k] = {"n_days": len(s["d"]), "brier_24h": brier(s["d"]),
                      "n_blocks": len(s["b"]), "brier_6h": brier(s["b"])}
    # reference: always forecasting the period's observed frequency (known only in hindsight)
    o24 = [d["obs"]["24h"] for d in days if d["obs"]["24h"] is not None]
    ob6 = [d["obs"][b] for d in days for b in BLOCK_LABELS if d["obs"][b] is not None]
    base = {"freq_24h": round(sum(o24) / len(o24), 3) if o24 else None, "n_days": len(o24),
            "freq_6h": round(sum(ob6) / len(ob6), 3) if ob6 else None, "n_blocks": len(ob6)}
    base["brier_24h"] = None if base["freq_24h"] is None else round(base["freq_24h"] * (1 - base["freq_24h"]), 4)
    base["brier_6h"] = None if base["freq_6h"] is None else round(base["freq_6h"] * (1 - base["freq_6h"]), 4)

    # reliability over every city stored (24-h and 6-h forecasts pooled: tiny samples otherwise)
    pooled = {}
    for st in sorted({o["station"] for o in obs}):
        for o, out, pops in collect(st, None):
            for k, (p, _) in pops.items():
                lst = pooled.setdefault(k, [])
                if p.get("p24") is not None and out["24h"] is not None:
                    lst.append((p["p24"], out["24h"]))
                lst += [(p["blocks"][b], out[b]) for b in BLOCK_LABELS
                        if (p.get("blocks") or {}).get(b) is not None and out[b] is not None]
    rel = {k: {"n": len(v), "bins": _reliability(v)} for k, v in pooled.items()}
    return {"event_in": EVENT_IN, "blocks": BLOCK_LABELS, "days": days, "summary": summary,
            "base_rate": base, "reliability": rel}
