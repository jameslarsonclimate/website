import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(autouse=True)
def _isolated_cache(tmp_path, monkeypatch):
    """Never read or write the real model-result cache during tests."""
    import wxc_cache
    monkeypatch.setattr(wxc_cache, "CACHE_DIR", tmp_path / "cache")
