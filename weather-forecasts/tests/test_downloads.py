"""Download/upload efficiency: parallel GRIB reads, small PNGs, one MOS request per run,
skipping a run with no network, and one-line Herbie errors."""
import importlib
import logging
import sys

import pandas as pd
import pytest

import wxc_carryover
import wxc_mos
import wxc_verify


def _main_module():
    return importlib.import_module("getForecast_wxChallenge-pushGitHub")


class _H:
    """FastHerbie stand-in: fails the threaded read like Herbie's cfgrib race, or not."""
    def __init__(self, fail_threaded):
        self.fail_threaded, self.calls = fail_threaded, []

    def xarray(self, search, max_threads=None, backend_kwargs=None):
        self.calls.append(max_threads)
        if max_threads and self.fail_threaded:
            raise AttributeError("'EntryPoint' object has no attribute '_key'")
        return "ds"


def test_grib_read_is_parallel_and_falls_back():
    m = _main_module()
    ok = _H(fail_threaded=False)
    assert m._read_grib(ok, ":2t:") == "ds" and ok.calls == [m.GRIB_THREADS]
    racy = _H(fail_threaded=True)
    assert m._read_grib(racy, ":2t:") == "ds" and racy.calls == [m.GRIB_THREADS, None]


def test_grib_read_no_match_is_not_retried():
    m = _main_module()

    class NoMatch(_H):
        def xarray(self, search, max_threads=None, backend_kwargs=None):
            self.calls.append(max_threads)
            raise ValueError("no match")
    h = NoMatch(False)
    with pytest.raises(ValueError):
        m._read_grib(h, ":nope:")
    assert h.calls == [m.GRIB_THREADS]


def test_save_png_is_palette(tmp_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 3, 2], "o-")
    wxc_verify.save_png(fig, tmp_path / "f.png", dpi=80)
    plt.close(fig)
    with Image.open(tmp_path / "f.png") as im:
        assert im.mode == "P" and im.size == (512, 384)


def test_fetch_mos_one_request_per_run(monkeypatch):
    import requests
    calls = []

    class R:
        def raise_for_status(self):
            pass

        def json(self):
            return {"data": [{"ftime": "2026-10-20 00:00", "tmp": 60}]}
    monkeypatch.setattr(requests, "get", lambda *a, **k: calls.append(k["params"]) or R())
    wxc_mos.fetch_mos.cache_clear()
    try:
        a = wxc_mos.fetch_mos("KXYZ", "GFS")
        b = wxc_mos.fetch_mos("KXYZ", "GFS")
        wxc_mos.fetch_mos("KXYZ", "NBS")
        assert len(calls) == 2 and a is b
    finally:
        wxc_mos.fetch_mos.cache_clear()


@pytest.mark.real_network_check
def test_network_up_retries_then_gives_up(monkeypatch):
    import socket
    import time
    tried, slept = [], []

    def refuse(addr, timeout=None):
        tried.append(addr[0])
        raise OSError("nodename nor servname provided, or not known")
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(time, "sleep", slept.append)
    assert wxc_carryover.network_up(("a", "b"), tries=3, wait_s=7) is False
    assert tried == ["a", "b"] * 3 and slept == [7, 7]

    class Conn:
        def close(self):
            pass
    monkeypatch.setattr(socket, "create_connection", lambda addr, timeout=None: Conn())
    assert wxc_carryover.network_up(("a",)) is True


def test_main_skips_run_when_offline(monkeypatch, capsys):
    m = _main_module()
    monkeypatch.setattr(wxc_carryover, "network_up", lambda *a, **k: False)
    monkeypatch.setattr(m, "get_station", lambda *a: pytest.fail("ran while offline"))
    monkeypatch.setattr(sys, "argv", ["x", "--no-push"])
    m.main()
    assert "No network" in capsys.readouterr().out


def test_herbie_tracebacks_are_dropped(caplog):
    _main_module()
    log = logging.getLogger("herbie.fast")
    with caplog.at_level(logging.ERROR, logger="herbie.fast"):
        log.error("Exception has occured : Max retries exceeded")
        log.error("Exception details : Max retries exceeded")
        log.error("Traceback (most recent call last):\n  File ...")
    assert [r.getMessage() for r in caplog.records] == ["Exception has occured : Max retries exceeded"]
