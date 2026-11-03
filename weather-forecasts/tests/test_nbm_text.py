"""
Offline tests for the NBM text bulletins read from AWS (wxc_nbm_text): parsing, finding a
station's block by streaming or by a byte window, and the NBM cloud series (SKY + SSD).

    cd weather-forecasts && python -m pytest tests -q
"""
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import wxc_clouds  # noqa: E402
import wxc_mos  # noqa: E402
import wxc_nbm_text as nt  # noqa: E402
import wxc_timeline  # noqa: E402

NBS = (HERE / "fixtures" / "nbm_nbs_KTPA_2026102221.txt").read_text()   # real blocks, 21Z 22 Oct 2026
NBH = (HERE / "fixtures" / "nbm_nbh_KTPA_2026102221.txt").read_text()
INIT = pd.Timestamp("2026-10-22T21:00", tz="UTC")


def _other(icao, prod="NBS"):
    """A short block of another station (header + UTC row)."""
    return f" {icao:<6} NBM V5.0 {prod} GUIDANCE    10/22/2026  2100 UTC\n UTC  00 03\n TMP  50 49\n"


def test_parse_nbs():
    df = nt.parse_block(NBS)
    assert len(df) == 23 and (df["runtime"] == INIT).all()
    assert df["ftime"].iloc[0] == INIT + pd.Timedelta(hours=6)            # FHR 06 -> 03Z
    assert df["ftime"].iloc[-1] == INIT + pd.Timedelta(hours=72)
    assert {"txn", "xnd", "tmp", "dpt", "sky", "ssd", "wsp", "p06", "q06"} <= set(df.columns)
    assert df["txn"].notna().tolist()[3] and df["txn"].dropna().tolist() == [60, 81, 62, 82, 68]
    assert df["p06"].notna().sum() == 11 and df["ftime"][df["p06"].notna()].dt.hour.isin([0, 6, 12, 18]).all()
    # summarize_mos reads these rows exactly like IEM's (checked equal to IEM's 18Z NBS)
    res = wxc_mos.summarize_mos(df, date(2026, 10, 23), "NBS")
    assert res["init_time_utc"] == "2026-10-22T21" and not res.get("error")
    assert res["tmax_f"] is not None and res["tmin_f"] is not None and res["precip_in"] is not None


def test_parse_nbh_hourly_times_and_negative_cells():
    df = nt.parse_block(NBH)
    assert len(df) == 25
    assert list(df["ftime"]) == [INIT + pd.Timedelta(hours=h) for h in range(1, 26)]   # 22Z .. 22Z next day
    assert df["sky"].iloc[:3].tolist() == [1, 0, 2] and df["ssd"].iloc[:4].tolist() == [1, 1, 5, 15]
    assert (df["cig"] == -88).all()                  # 3-character cells that touch ("-88-88") still split
    assert df["ftime"][df["p06"].notna()].dt.hour.tolist() == [6, 12, 18]   # sparse rows stay on their hours


def test_header_without_version():
    """From 13Z 3 Nov 2026 the headers read "NBM  NBS GUIDANCE" (no "V5.0")."""
    old = NBS.splitlines(keepends=True)
    new = old[0].replace("NBM V5.0 NBS", "NBM  NBS")
    assert new != old[0]
    block = new + "".join(old[1:])
    text = _other("KTOI").replace("NBM V5.0", "NBM ") + block + _other("KTPF").replace("NBM V5.0", "NBM ")
    found, i = nt.find_block(text, "KTPA")
    assert found == block and text[i:].startswith(" KTPA")
    assert nt.parse_block(block).equals(nt.parse_block(NBS))


def test_find_block_needs_the_next_header():
    text = _other("KTOI") + NBS + _other("KTPF")
    block, i = nt.find_block(text, "KTPA")
    assert block == NBS and text[i:].startswith(" KTPA")
    assert nt.find_block(_other("KTOI") + NBS, "KTPA") == (None, None)            # may continue
    assert nt.find_block(_other("KTOI") + NBS, "KTPA", complete=False)[0] == NBS   # end of file


class FakeS3:
    """The bucket: one bulletin, honouring Range requests; counts bytes served."""
    def __init__(self, files):
        self.files, self.served, self.ranges = files, 0, []

    def get(self, url, headers=None, stream=False, timeout=None):
        body = self.files.get(url)
        s3 = self

        class R:
            status_code = 404 if body is None else 200
            headers = {}
            content = b""

            def raise_for_status(self):
                pass

            def iter_content(self, n):
                for k in range(0, len(self.content), n):
                    s3.served += min(n, len(self.content) - k)
                    yield self.content[k:k + n]

            def close(self):
                pass
        r = R()
        if body is None:
            return r
        data = body.encode("latin-1")
        rng = (headers or {}).get("Range")
        if rng:
            a, b = (int(x) for x in rng[6:].split("-"))
            self.ranges.append((a, b))
            r.status_code, r.content = 206, data[a:b + 1]
            r.headers = {"Content-Range": f"bytes {a}-{min(b, len(data) - 1)}/{len(data)}"}
            self.served += len(r.content)
        else:
            r.content = data
        return r


def test_station_block_streams_then_reads_a_window(monkeypatch):
    pad = "".join(_other(f"K{i:04d}") for i in range(2000))         # ~140 KB of other stations first
    bulletin = pad + NBS + _other("KTPF")
    s3 = FakeS3({nt.url_for("nbs", INIT): bulletin,
                 nt.url_for("nbs", INIT + pd.Timedelta(hours=1)): bulletin.replace("2100 UTC", "2200 UTC")})
    monkeypatch.setattr(nt, "_session", lambda: s3)
    monkeypatch.setattr(nt, "STREAM_CHUNK", 1000)
    monkeypatch.setattr(nt, "HINT_PAD", 2000)
    # first cycle: streamed until the block is complete, offset remembered
    assert nt.station_block("KTPA", "nbs", INIT) == NBS
    assert s3.ranges == [] and nt._hint_path("KTPA", "nbs").exists()
    # cached: no request at all
    nt.station_block.cache_clear()
    n = s3.served
    assert nt.station_block("KTPA", "nbs", INIT) == NBS and s3.served == n
    # next cycle: only a window around the remembered offset
    s3.served = 0
    blk = nt.station_block("KTPA", "nbs", INIT + pd.Timedelta(hours=1))
    assert blk.startswith(" KTPA") and "2200 UTC" in blk
    assert len(s3.ranges) == 1 and s3.served <= 2 * 2000 + nt.BLOCK_MAX + 1 < len(bulletin)
    # not posted yet -> empty rows, so the caller falls back to an older cycle
    assert nt.fetch("KTPA", "nbs", INIT + pd.Timedelta(hours=2)).empty


def test_window_miss_falls_back_to_streaming(monkeypatch):
    bulletin = "".join(_other(f"K{i:03d}") for i in range(300)) + NBS
    s3 = FakeS3({nt.url_for("nbs", INIT): bulletin})
    monkeypatch.setattr(nt, "_session", lambda: s3)
    monkeypatch.setattr(nt, "HINT_PAD", 500)
    p = nt._hint_path("KTPA", "nbs")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"offset": 10}')                                    # stale: the station moved
    assert nt.station_block("KTPA", "nbs", INIT) == NBS               # last block in the file
    assert len(s3.ranges) == 1


def test_candidate_runtimes_slow_cycles():
    t = datetime(2026, 10, 22, 14, 30, tzinfo=timezone.utc)
    # 14Z not out (needs ~57 min), 13Z (a slow cycle) out after 14:42, so 12Z (slow, 13:42) is next
    assert [x.hour for x in nt.candidate_runtimes(t, 2)] == [12, 11]
    assert [x.hour for x in nt.candidate_runtimes(t.replace(minute=45), 1)] == [13]


def test_newest_falls_back(monkeypatch):
    got = []
    monkeypatch.setattr(nt, "fetch", lambda icao, prod, init: got.append(init.hour) or (
        pd.DataFrame() if init.hour == 20 else pd.DataFrame({"x": [1]})))
    nt.newest("KTPA", "nbs", datetime(2026, 10, 22, 21, 0, tzinfo=timezone.utc))
    assert got == [20, 19]


def test_nbm_cloud_hourly_nbh_then_nbs(monkeypatch):
    rows = {"nbs": nt.parse_block(NBS), "nbh": nt.parse_block(NBH)}
    monkeypatch.setattr(nt, "fetch", lambda icao, prod, init: rows[prod])
    rec = nt.cloud("KTPA", "2026-10-22T21")
    t = pd.to_datetime(rec["times"])
    nbh_end = INIT.tz_convert(None) + pd.Timedelta(hours=25)
    assert (np.diff(t[t <= nbh_end]) == pd.Timedelta(hours=1)).all()        # hourly from NBH
    assert (np.diff(t[t > nbh_end]) == pd.Timedelta(hours=3)).all()         # then NBS
    assert rec["cloud_pct"][:3] == [1.0, 0.0, 2.0] and rec["cloud_sd"][:4] == [1.0, 1.0, 5.0, 15.0]
    # the cloud cache and the day cut keep the SD aligned with its hour
    m = wxc_clouds.merge(None, {"model": "NBM", **rec})
    assert m["cloud_sd"] == rec["cloud_sd"]
    d = wxc_clouds.for_day(m, date(2026, 10, 23))
    assert len(d["cloud_sd"]) == len(d["times"]) == 17 + 3      # 06Z..22Z hourly + 00Z, 03Z, 06Z
    # ... and the timeline sends it to the page as "sd"
    tl = wxc_timeline.clouds_record("KTPA", date(2026, 10, 23), {"NBM": d}, None, datetime.now(timezone.utc))
    c = wxc_timeline._cloud(tl["submitted"]["NBM"], date(2026, 10, 23))
    assert len(c["sd"]) == len(c["pct"])


def test_merge_without_sd_unchanged():
    m = wxc_clouds.merge({"times": ["2026-10-01T06:00"], "cloud_pct": [10.0]},
                         {"times": ["2026-10-01T09:00"], "cloud_pct": [20.0]})
    assert "cloud_sd" not in m


def test_cloud_band_drawn(monkeypatch):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    wxc_clouds.draw_models(ax, {"NBM": {"times": ["2026-10-23T06:00", "2026-10-23T07:00"],
                                        "cloud_pct": [90.0, 5.0], "cloud_sd": [20.0, 10.0]}}, lambda n: {})
    (band,) = ax.collections
    ys = band.get_paths()[0].vertices[:, 1]
    assert ys.max() == 100 and ys.min() == 0                         # clipped to 0-100
    plt.close(fig)
