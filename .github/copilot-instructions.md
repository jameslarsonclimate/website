This repository contains Python scripts and static site assets that fetch, summarize, and publish weather-model forecasts (HRRR, IFS, GFS, AIFS) for a small set of locations. The site outputs (JSON, PNG, and simple HTML) are stored in `weather-forecasts/data` and `weather-forecasts/images` and intended to be published via GitHub Pages.

Quick entry points
- Primary helpers: `weather-forecasts/functions.py` — utility functions used across scripts (model timing, forecast-range generation, small xarray helpers).
- Main tasks: `weather-forecasts/getForecast_*.py` and `weather-forecasts/getForecast_*.sh` — scripts that call Herbie to fetch model data, summarize it, write JSON under `weather-forecasts/data`, and write small images under `weather-forecasts/images`.
- Static site: `weather-forecasts/index.html` and `weather-forecasts/wxchallenge/index.html` — simple HTML pages that read the JSON payloads.

Big-picture architecture and data flow
- Scripts run on a schedule (cron or CI) to: 1) pick the latest model cycle (`get_latest_forecast_cycle`), 2) compute a forecast step list (`calculate_forecast_range`), 3) request fields via `herbie.FastHerbie`, 4) summarize variables (tmax/tmin, wind, precip), 5) write JSON and small PNG thumbnails, 6) optionally `git add/commit/push` to update GitHub Pages.
- Data outputs are intentionally simple: per-site JSON payloads (e.g., `weather-forecasts/data/wxchallenge/forecast.json`) and small images (`weather-forecasts/images/*/latest.png`). The HTML pages consume these files directly.

Developer workflows and commands
- Run one-off forecast locally (examples):
  - `python3 weather-forecasts/getForecast_wxChallenge-pushGitHub.py`
  - `sh weather-forecasts/getForecast_wxChallenge.sh`
- If using GitHub Pages, scripts attempt a best-effort `git add/commit/push`; local testing should avoid committing unless intended. Use the `git` commands manually when iterating.
- Environment: these scripts expect scientific Python packages (`xarray`, `pandas`, `numpy`, `herbie`, `cfgrib`, `matplotlib`, `Pillow`) available in your Python environment. There is no pinned `requirements.txt` in the repo — create an environment (e.g., conda) with the usual packages for meteorological analysis.

Project conventions and patterns
- Time handling: use the helpers in `weather-forecasts/functions.py` — `get_latest_forecast_cycle(...)` returns a timezone-naive `pd.Timestamp` accounting for model-specific delays. `calculate_forecast_range(...)` returns integer forecast-hour steps tailored per model (HRRR: hourly, IFS/GFS: 3-hour blocks, etc.).
- Units: temperatures are converted from Kelvin to °F, wind speeds to knots (m/s * 1.94384), and precipitation to inches. Many scripts store values rounded to 1–2 decimal places before writing JSON.
- Output layout: JSON payloads contain a `meta` block and a `models` object keyed by model name. Keep the legacy top-level metrics when modifying payload structure because `index.html` expects older keys.
- Image creation: small PNGs are saved using `matplotlib` (typical DPI 150) and placed under `weather-forecasts/images/<variant>/latest.png`.

Integration points and external dependencies
- Data source: scripts use `herbie.FastHerbie` to obtain model GRIB fields. When editing request strings (e.g., `H.xarray("TMP:2 m above")`), match the product names used in existing scripts.
- GitHub Pages: the repo relies on committing generated static assets under `weather-forecasts/data` and `weather-forecasts/images`. The scripts call `git push origin main` by default — CI or scheduled tasks should provide credentials or use workflows that commit artifacts.

Patterns for contributors / AI agents
- When changing model timing or adding models: update `weather-forecasts/functions.py` model_configs (delay/init_hours) and the switch logic in `calculate_forecast_range` to ensure produced fxx ranges match downstream `FastHerbie` requests.
- Add tests only for pure-Python helpers (e.g., `get_latest_forecast_cycle`, `calculate_forecast_range`, `convert_time_to_datetime64`) — data-fetching functions are environment- and network-dependent and should be mocked in unit tests.
- Keep JSON schema backward compatible; the website HTML expects legacy keys. If you change the schema, update `weather-forecasts/index.html` and `weather-forecasts/wxchallenge/index.html` accordingly.

Examples from the codebase
- Timing helper: `get_latest_forecast_cycle(model='HRRR')` in `weather-forecasts/functions.py` — respects model-specific `delay` and `init_hours`.
- Forecast range: `calculate_forecast_range(timestamp, model='IFS')` — returns a range in 3-hour increments and special-cases `timestamp.hour == 0`.
- Payload writing: `getForecast_ATS640-pushGitHub.py` writes `payload` to `weather-forecasts/data/ats640/forecast-away.json` and saves image to `weather-forecasts/images/ats640/latest-away.png`.

If something is unclear
- Ask which environment you will run scripts in (local, CI, or scheduled server) so the instructions can include credentials or workflow examples.
- Point me to any GitHub Actions or cron entries you use and I will add concrete run steps and environment setup guidance.

If you'd like, I can also:
- Add a `requirements.txt` or `environment.yml` with the minimal packages used by the scripts.
- Create a simple `workflow` example to run scripts on a schedule and commit outputs to GitHub Pages.