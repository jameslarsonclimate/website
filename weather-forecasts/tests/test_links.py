"""Offline tests for wxc_links (forecast-evolution panel config)."""

import json
from pathlib import Path

import pytest

import wxc_links
from wxc_stations import STATIONS, Station

PAGE = Path(__file__).resolve().parent.parent / "wxchallenge" / "index.html"


def test_region_from_station():
    cfg = wxc_links.build_config(STATIONS["KTPA"])
    assert cfg["pivotal"]["region"] == "us_se"
    assert cfg["satellite_url"].startswith("https://slider.cira.colostate.edu/?sat=goes-19")


@pytest.mark.parametrize("region", [None, "", wxc_links.FILL])
def test_region_fallback_logged(region, capsys):
    st = Station("KXYZ", "Nowhere", 40.0, -100.0, pivotal_region=region)
    cfg = wxc_links.build_config(st)
    assert cfg["pivotal"]["region"] == "conus"
    assert "using 'conus'" in capsys.readouterr().out
    assert cfg["satellite_url"] == wxc_links.SLIDER_DEFAULT      # no slider_url -> SLIDER home


def test_fill_entries_skipped(monkeypatch, capsys):
    monkeypatch.setattr(wxc_links, "PRODUCTS", [("Radar", "ref1km_ptype"), ("Mystery", wxc_links.FILL)])
    monkeypatch.setattr(wxc_links, "CSU_ZOOM_URL", wxc_links.FILL)
    monkeypatch.setattr(wxc_links, "WPC_IMAGES", [("12 h", "92fndfd.gif"), ("24 h", " <FILL> ")])
    st = Station("KXYZ", "Nowhere", 40.0, -100.0, pivotal_region="us_se", slider_url=wxc_links.FILL)
    cfg = wxc_links.build_config(st)
    assert [p["p"] for p in cfg["pivotal"]["products"]] == ["ref1km_ptype"]
    assert cfg["csu_url"] is None
    assert [i["label"] for i in cfg["wpc"]["images"]] == ["12 h"]
    assert cfg["satellite_url"] == wxc_links.SLIDER_DEFAULT
    assert set(cfg["skipped"]) == {"product Mystery", "CSU Zoom URL", "WPC 24 h", "slider_url"}
    assert wxc_links.FILL not in json.dumps(cfg["pivotal"]) + json.dumps(cfg["wpc"])
    assert "skipped" in capsys.readouterr().out


def test_csu_url_used_when_filled(monkeypatch):
    monkeypatch.setattr(wxc_links, "CSU_ZOOM_URL", "https://example.edu/zoom")
    cfg = wxc_links.build_config(STATIONS["KTPA"])
    assert cfg["csu_url"] == "https://example.edu/zoom" and "CSU Zoom URL" not in cfg["skipped"]


def test_embedded_json_valid_and_script_safe():
    st = Station("KXYZ", "Odd </script><!-- name & co", 40.0, -100.0, pivotal_region="us_se")
    cfg = wxc_links.build_config(st)
    html = ('<p>before</p>\n<script type="application/json" id="evo-config">\nold\n</script>\n'
            '<script>keep()</script>')
    out = wxc_links.embed_config(html, cfg)
    block = wxc_links.CONFIG_RE.search(out).group(2)
    assert "</" not in block and "<!--" not in block
    assert json.loads(block) == cfg
    assert out.startswith("<p>before</p>") and out.endswith("<script>keep()</script>")
    assert wxc_links.embed_config(out, cfg) == out                     # idempotent


def test_embed_requires_block():
    with pytest.raises(ValueError):
        wxc_links.embed_config("<html></html>", {})


def test_real_page_has_block(tmp_path):
    page = tmp_path / "index.html"
    page.write_text(PAGE.read_text(encoding="utf-8"), encoding="utf-8")
    wxc_links.update_page(page, STATIONS["KTPA"])
    cfg = wxc_links.read_config(page.read_text(encoding="utf-8"))
    assert cfg["station"] == "KTPA"
    assert [p["p"] for p in cfg["pivotal"]["products"]] == ["ref1km_ptype", "sfcwind_mslp", "sim_ir", "qpf_acc"]
    assert [i["url"].rsplit("/", 1)[1] for i in cfg["wpc"]["images"]] == \
        ["92fndfd.gif", "94fndfd.gif", "96fndfd.gif", "98fndfd.gif"]
    assert wxc_links.update_page(page, STATIONS["KTPA"]) is False       # unchanged on a re-run
