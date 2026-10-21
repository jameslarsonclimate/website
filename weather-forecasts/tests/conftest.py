import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(autouse=True)
def _isolated_cache(tmp_path, monkeypatch):
    """Never read or write the real model-result cache during tests."""
    import wxc_cache
    monkeypatch.setattr(wxc_cache, "CACHE_DIR", tmp_path / "cache")


def pytest_configure(config):
    config.addinivalue_line("markers", "real_network_check: keep wxc_carryover.network_up (no stub)")


@pytest.fixture(autouse=True)
def _assume_online(request, monkeypatch):
    """main()'s start-up connectivity check would open real sockets; tests fake every source."""
    import wxc_carryover
    if request.node.get_closest_marker("real_network_check"):
        return
    monkeypatch.setattr(wxc_carryover, "network_up", lambda *a, **k: True)
