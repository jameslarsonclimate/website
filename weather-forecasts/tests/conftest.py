import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(autouse=True)
def _isolated_cache(tmp_path, monkeypatch):
    """Never read or write the real model-result cache during tests."""
    import wxc_cache
    monkeypatch.setattr(wxc_cache, "CACHE_DIR", tmp_path / "cache")


@pytest.fixture(autouse=True)
def _no_nbm_network(monkeypatch):
    """NBM text comes from AWS (wxc_nbm_text): a test that reaches it without a fake fails."""
    import wxc_nbm_text

    class NoNetwork:
        @staticmethod
        def get(url, *a, **k):
            pytest.fail(f"network call in an offline test: {url}")
    monkeypatch.setattr(wxc_nbm_text, "_session", lambda: NoNetwork)
    wxc_nbm_text.station_block.cache_clear()


@pytest.fixture(autouse=True)
def _no_wxc_results_network(tmp_path, monkeypatch):
    """wxchallenge.com results (wxc_team): never fetched, and never the real team files, in tests."""
    import wxc_team
    fail = lambda *a, **k: pytest.fail("network call in an offline test: results.php")  # noqa: E731
    monkeypatch.setattr(wxc_team, "_post", fail)
    monkeypatch.setattr(wxc_team, "RAW", tmp_path / "team_raw.json")
    monkeypatch.setattr(wxc_team, "OUT", tmp_path / "team.json")


def pytest_configure(config):
    config.addinivalue_line("markers", "real_network_check: keep wxc_carryover.network_up (no stub)")


@pytest.fixture(autouse=True)
def _assume_online(request, monkeypatch):
    """main()'s start-up connectivity check would open real sockets; tests fake every source."""
    import wxc_carryover
    if request.node.get_closest_marker("real_network_check"):
        return
    monkeypatch.setattr(wxc_carryover, "network_up", lambda *a, **k: True)
