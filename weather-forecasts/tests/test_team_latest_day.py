"""wxc_team.fetch_latest: which day to ask results.php for (offline; a fake site, no network).

How results.php behaves (checked 2026-11-10): a day <= the latest returns that day's page (days
1..N in the date list plus the school's table); a day past the latest returns a page with no
heading and no table while the city is in progress, and clamps to the last day once it is over.
"""
from datetime import date, timedelta

import wxc_team
import wxc_verify

REAL_CITY_START = wxc_team._city_start          # captured before conftest stubs it

PAYA_START = date(2026, 11, 10)                    # Tue; PAYA Day 1
DATES = [PAYA_START + timedelta(days=d) for d in (0, 1, 2, 3, 7, 8, 9, 10)]   # Tue-Fri x 2 weeks
EMPTY = "<html><body><form>no results</form></body></html>"


def _cells(*vals):
    return "".join(f"<TD><CENTER>{v}</CENTER></TD>" for v in vals)


def _csu_row(name, fc, rank=1):
    # rank, prev, ?, name, school, cat, abs, 4 forecast, flag, 4 errors, penalty, points, ..., cum @23
    cells = [rank, "", "", name, "csu", 2, 0, *fc, "", 0, 0, 0, 0, 0, 0.0, "", "", "", "", "", 0.0,
             "", "", ""]
    assert len(cells) >= 27
    return f"<TR>{_cells(*cells)}</TR>"


def page(n, status="As of 15Z"):
    """Day n's results page: heading, date list for days 1..n, one csu forecaster."""
    rows = "".join(f"<TR>{_cells(d.strftime('%Y%m%d'), 45, 37, 30, 0.48, f'Final Day {i}' if i < n else status)}</TR>"
                   for i, d in enumerate(DATES[:n], 1))
    return (f"<h5>Day {n} ({status})</h5><table>{rows}</table>"
            f"<table>{_csu_row('Bigfut', (45, 37, 30, 0.48))}</table>")


class Site:
    """results.php: `latest` days posted; past the latest -> empty, or clamp when `finished`."""
    def __init__(self, latest, finished=False):
        self.latest, self.finished, self.posts = latest, finished, []

    def post(self, year, city, day):
        self.posts.append(day)
        if day <= self.latest:
            return page(day, "Final Day %d" % day if self.finished else "As of 15Z")
        return page(self.latest, f"Final Day {self.latest}") if self.finished else EMPTY


def run(monkeypatch, site, guess):
    monkeypatch.setattr(wxc_team, "_post", lambda s, year, city, day, school="csu": site.post(year, city, day))
    monkeypatch.setattr(wxc_team.time, "sleep", lambda s: None)
    return wxc_team.fetch_latest(None, "26-27", "paya", guess)


def test_expected_day():
    ex = wxc_team.expected_day
    assert ex(PAYA_START, PAYA_START) == 1
    assert ex(PAYA_START, date(2026, 11, 12)) == 3
    assert ex(PAYA_START, date(2026, 11, 14)) == 4           # Sat: still day 4
    assert ex(PAYA_START, date(2026, 11, 17)) == 5           # next Tue
    assert ex(PAYA_START, date(2026, 11, 9)) == 0            # before the city
    assert ex(None, PAYA_START) is None


def test_city_start(tmp_path, monkeypatch):
    f = tmp_path / "verification.json"
    monkeypatch.setattr(wxc_verify, "VERIF", f)
    real = REAL_CITY_START                                   # conftest stubs wxc_team._city_start
    assert real("PAYA") is None                              # missing file
    f.write_text("{not json")
    assert real("PAYA") is None
    f.write_text('{"station": "KMSP", "city_start": "2026-10-27"}')
    assert real("PAYA") is None                              # another city
    f.write_text('{"station": "PAYA", "city_start": null}')
    assert real("PAYA") is None
    f.write_text('{"station": "PAYA", "city_start": "2026-11-10"}')
    assert real("PAYA") == PAYA_START


def test_in_progress_day1_one_post(monkeypatch):
    site = Site(1)
    r = run(monkeypatch, site, wxc_team.expected_day(PAYA_START, PAYA_START))
    assert site.posts == [1] and r["day"] == 1 and "Bigfut" in r["forecasters"]


def test_day3_one_post(monkeypatch):
    site = Site(3)
    r = run(monkeypatch, site, 3)
    assert site.posts == [3] and r["day"] == 3 and sorted(r["dates"]) == [1, 2, 3]


def test_before_06z_steps_down(monkeypatch):
    site = Site(1)                                            # Wed, day-2 table not up yet
    r = run(monkeypatch, site, wxc_team.expected_day(PAYA_START, date(2026, 11, 11)))
    assert site.posts == [2, 1] and r["day"] == 1


def test_finished_city_clamps(monkeypatch):
    site = Site(8, finished=True)
    r = run(monkeypatch, site, 30)
    assert site.posts == [8] and r["day"] == 8 and r["status"] == "Final Day 8"


def test_break_week_overshoot(monkeypatch):
    site = Site(4)                                            # count says 8, site has 4
    r = run(monkeypatch, site, 8)
    assert site.posts == [8, 7, 6, 5, 4] and r["day"] == 4


def test_before_city_starts_no_post(monkeypatch):
    site = Site(0)
    r = run(monkeypatch, site, 0)
    assert site.posts == [] and r["day"] is None and not r["dates"]


def test_unknown_start_walks_down(monkeypatch):
    site = Site(0)
    r = run(monkeypatch, site, None)
    assert site.posts == [8, 7, 6, 5, 4, 3, 2, 1] and r["day"] is None


def test_unknown_start_finds_day(monkeypatch):
    site = Site(2)
    assert run(monkeypatch, site, None)["day"] == 2 and site.posts == [8, 7, 6, 5, 4, 3, 2]


def test_parse_mixed_case_name():
    r = wxc_team.parse_results(page(1).replace("<TD><CENTER>csu</CENTER>", "<TD><CENTER>CSU</CENTER>"))
    assert list(r["forecasters"]) == ["Bigfut"]
    assert r["forecasters"]["Bigfut"]["forecast"] == {"tmax_f": 45, "tmin_f": 37, "wind_max_kt": 30,
                                                      "precip_in": 0.48}
    assert r["dates"][1]["date"] == "2026-11-10"
