# WxChallenge forecast brief: Olympia, WA (KOLM)

- Station: **KOLM**
- Target day: **2026-10-19**, scored over 2026-10-19T06Z to 2026-10-20T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-19T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-18T21:48:09+00:00 (refreshed several times an hour while the forecast job runs)
- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)

## How to use this brief (for AI assistants)

1. Start from the **CONSENSUS** row. It is already bias-corrected and skill-weighted using this period's verification (method below).
2. Check the track-record table: a model with a large, consistent bias (|bias| close to its MAE) is reliably off in that direction. The consensus already removes most of that bias; lean further only if the last few days (daily verification tables) show the bias growing.
3. Use the ensemble percentiles for uncertainty. For **precip**, enter roughly the ensemble **median**, not the mean: points are charged per 0.01" of error, and charged most heavily near zero, so the median minimizes expected points. Check the chance-of-rain table: when the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.
4. Use "Today so far" (the day currently in progress, not the target day) to see which models are handling the current pattern; persistent errors there often carry into tomorrow.
5. Check the clouds section: when a model's low or high misses line up with its cloud misses (too clear at night -> low too cold, too cloudy at night -> low too warm; too clear by day -> high too warm, too cloudy by day -> high too cool), ask whether its cloud forecast for the target day has the same problem before trusting its temperatures. Do the same with the dewpoint (the dewpoint section for past days, "Dewpoint so far today" for today): a model running too moist tends to run its low too warm, too dry its low too cold.
6. Read the latest AFD for the forecaster's view of the pattern; it often explains when a model bias learned earlier in the period won't apply.
7. Give whole °F for high/low, whole kt for wind, and precip to 0.01". State the reasoning for any departure from the consensus.

## Scoring (error points; lower is better)

- High and low temperature: 1 point per °F of error.
- Max sustained wind: 0.5 point per kt of error.
- Precipitation: per 0.01" between forecast and observed: 0.4 pt for amounts 0.00 to 0.10", 0.3 for 0.11 to 0.25", 0.2 for 0.26 to 0.50", 0.1 above 0.50". A trace counts as 0.00.
- Forecasts are rounded as submitted (whole °F and kt, 0.01") before scoring.

## Guidance for the target day

Run = day/hour (UTC) of the model initialization.

| Model | Run | High °F | Low °F | Wind kt | Precip in |
| --- | --- | --: | --: | --: | --: |
| HRRR | 18/18Z | 63.0 | 44.3 | 4.6 | 0.00 |
| RRFS | 18/18Z | 62.8 | 46.2 | 5.4 | 0.00 |
| IFS | 18/12Z | 60.6 | 42.2 | 4.4 | 0.00 |
| GFS | 18/12Z | 62.4 | 42.7 | 3.0 | 0.00 |
| AIFS | 18/12Z | 59.6 | 42.6 | 4.2 | 0.00 |
| GFS_MOS | 18/12Z | 62.0 | 35.0 | 4.0 | 0.00 |
| NBM | 18/18Z | 61.0 | 35.0 | 2.0 | 0.00 |
| USL | 18/12Z | 60.0 | 40.0 | 6.0 | 0.00 |
| ENS | 18/06Z | 60.4 | 45.1 | 4.4 | 0.00 |
| AIFS_ENS | 18/12Z | 60.7 | 43.5 | 4.6 | 0.00 |
| GEFS | 18/12Z | 62.2 | 41.9 | 2.8 | 0.00 |
| HRRRCAST (precip only) | 18/12Z | — | — | — | 0.00 |
| REFS (precip only) | 18/18Z | — | — | — | 0.00 |
| NBM_QMD (precip only) | 18/12Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **61.8** | **36.9** | **7.0** | **0.00** |

Notes:
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [0, 0, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members (Open-Meteo)
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- HRRRCAST: median of 18 members (experimental AI model)
- REFS: median of 14 members, 18Z + 12Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS is shown but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: NBM 0.16, RRFS 0.11, IFS 0.10, GFS_MOS 0.10, ENS 0.10, AIFS 0.09, USL 0.09, HRRR 0.09, GFS 0.08, AIFS_ENS 0.08
- Low °F weights: GFS_MOS 0.18, NBM 0.13, USL 0.12, HRRR 0.09, GFS 0.09, AIFS 0.09, AIFS_ENS 0.08, IFS 0.07, RRFS 0.07, ENS 0.06
- Wind kt weights: USL 0.18, RRFS 0.11, HRRR 0.11, AIFS_ENS 0.10, NBM 0.09, GFS_MOS 0.09, ENS 0.09, IFS 0.08, GFS 0.07, AIFS 0.07
- Precip in weights: GFS 0.10, NBM 0.10, USL 0.10, HRRR 0.10, RRFS 0.10, IFS 0.10, AIFS 0.10, GFS_MOS 0.10, AIFS_ENS 0.10, ENS 0.10

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 57.7 | 59.4 | 60.6 | 61.7 | 62.2 | 60.4 |
| ENS | 51 | Low °F | 43.7 | 44.5 | 45.1 | 45.8 | 46.4 | 45.1 |
| ENS | 51 | Wind kt | 3.5 | 3.9 | 4.3 | 4.9 | 5.3 | 4.4 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| AIFS_ENS | 51 | High °F | 58.7 | 59.7 | 60.7 | 61.8 | 63.0 | 60.7 |
| AIFS_ENS | 51 | Low °F | 41.4 | 42.6 | 43.5 | 44.6 | 45.6 | 43.5 |
| AIFS_ENS | 51 | Wind kt | 3.5 | 3.9 | 4.4 | 5.0 | 6.4 | 4.6 |
| AIFS_ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| GEFS | 31 | High °F | 60.5 | 61.3 | 61.8 | 63.4 | 63.6 | 62.2 |
| GEFS | 31 | Low °F | 39.8 | 41.0 | 41.6 | 42.9 | 44.1 | 41.9 |
| GEFS | 31 | Wind kt | 2.3 | 2.4 | 2.7 | 3.0 | 3.5 | 2.8 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 6% | 0% | 0% | 0% |
| AIFS_ENS | 4% | 0% | 0% | 0% |
| GEFS | 0% | 0% | 0% | 0% |
| HRRRCAST | 11% | 0% | 0% | 0% |
| REFS | 0% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.00", p90 0.00"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 2% | 2% | 1% | 1% | 2% to 6% | 0.02 (20) |
| NBM | NBS P06 | 2% | 3% | 2% | 2% | 3% to 9% | 0.01 (20) |
| ENS | member fraction | 0% | 6% | 4% | 2% | 6% | 0.04 (20) |
| AIFS_ENS | member fraction | 2% | 0% | 2% | 2% | 4% | 0.02 (20) |
| GEFS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.01 (20) |
| HRRRCAST | member fraction | — | — | — | — | 11% | — |
| REFS | member fraction | — | — | — | — | 0% | — |
| NBM_QMD | NBM QMD | 0% | 0% | 0% | 0% | 0% | 0.01 (20) |

For reference, always forecasting the period's observed frequency (5% of 6-h blocks wet) scores Brier 0.05.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; the ensembles have none). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles none. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-19 06Z | Sun 23:00 | 44.6 | 47.1 | 46.6 | 45.1 | 45.7 | 41.0 | 42.0 | 43.0 | 47.5 | 46.9 | 46.3 |
| 10-19 07Z | Mon 00:00 | 44.8 | 46.7 |  |  |  |  |  | 42.0 | 47.2 | 45.8 | 45.8 |
| 10-19 08Z | Mon 01:00 | 44.8 | 46.5 |  |  |  |  |  | 42.0 | 47.0 | 44.9 | 45.6 |
| 10-19 09Z | Mon 02:00 | 44.7 | 47.0 | 45.9 | 45.0 |  | 40.0 | 41.0 | 42.0 | 46.9 | 44.3 | 45.3 |
| 10-19 10Z | Mon 03:00 | 44.7 | 47.4 |  |  |  |  |  | 42.0 | 46.7 | 44.0 | 44.8 |
| 10-19 11Z | Mon 04:00 | 44.6 | 47.4 |  |  |  |  |  | 41.0 | 46.7 | 43.9 | 44.4 |
| 10-19 12Z | Mon 05:00 | 44.6 | 47.0 | 45.7 | 45.6 | 42.6 | 39.0 | 40.0 | 41.0 | 46.5 | 44.3 | 43.9 |
| 10-19 13Z | Mon 06:00 | 44.9 | 46.6 |  |  |  |  |  | 41.0 | 45.8 | 45.2 | 42.9 |
| 10-19 14Z | Mon 07:00 | 44.6 | 46.5 |  |  |  |  |  | 40.0 | 45.1 | 46.7 | 42.0 |
| 10-19 15Z | Mon 08:00 | 44.3 | 46.4 | 42.5 | 44.5 |  | 40.0 | 39.0 | 40.0 | 45.5 | 48.5 | 42.6 |
| 10-19 16Z | Mon 09:00 | 46.4 | 49.4 |  |  |  |  |  | 43.0 | 47.8 | 50.4 | 46.0 |
| 10-19 17Z | Mon 10:00 | 50.5 | 53.5 |  |  |  |  |  | 47.0 | 51.3 | 52.2 | 50.9 |
| 10-19 18Z | Mon 11:00 | 54.4 | 56.1 | 55.8 | 54.8 | 51.5 | 52.0 | 52.0 | 51.0 | 54.4 | 53.8 | 55.2 |
| 10-19 19Z | Mon 12:00 | 57.6 | 58.3 |  |  |  |  |  | 54.0 | 56.7 | 55.3 | 58.3 |
| 10-19 20Z | Mon 13:00 | 60.2 | 60.3 |  |  |  |  |  | 56.0 | 58.7 | 57.0 | 60.6 |
| 10-19 21Z | Mon 14:00 | 62.0 | 61.6 | 60.3 | 61.9 |  | 59.0 | 59.0 | 58.0 | 59.9 | 58.7 | 62.0 |
| 10-19 22Z | Mon 15:00 | 62.8 | 62.5 |  |  |  |  |  | 59.0 | 60.3 | 60.0 | 62.1 |
| 10-19 23Z | Mon 16:00 | 63.0 | 62.7 |  |  |  |  |  | 59.0 | 60.1 | 60.7 | 61.2 |
| 10-20 00Z | Mon 17:00 | 62.5 | 62.2 | 58.7 | 59.9 | 59.6 | 60.0 | 60.0 | 58.0 | 59.0 | 60.6 | 59.4 |
| 10-20 01Z | Mon 18:00 | 58.0 | 59.1 |  |  |  |  |  | 55.0 | 56.6 | 59.3 | 56.0 |
| 10-20 02Z | Mon 19:00 | 53.3 | 55.0 |  |  |  |  |  | 51.0 | 53.4 | 56.9 | 51.6 |
| 10-20 03Z | Mon 20:00 | 50.5 | 52.3 | 50.0 | 47.8 |  | 50.0 | 47.0 | 48.0 | 50.7 | 53.9 | 48.2 |
| 10-20 04Z | Mon 21:00 | 48.4 | 50.7 |  |  |  |  |  | 45.0 | 49.1 | 50.8 | 46.5 |
| 10-20 05Z | Mon 22:00 | 46.3 | 49.2 |  |  |  |  |  | 43.0 | 48.2 | 48.1 | 45.7 |
| 10-20 06Z | Mon 23:00 | 44.6 | 48.2 | 46.3 | 42.8 | 44.7 | 44.0 | 41.0 | 42.0 | 47.3 | 46.0 | 45.1 |

Dewpoint (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-19 06Z | Sun 23:00 | 41.4 | 45.3 | 41.1 | 40.4 | 39.0 | 38.0 | 40.0 | 40.0 |
| 10-19 07Z | Mon 00:00 | 41.2 | 45.2 |  |  |  |  |  | 40.0 |
| 10-19 08Z | Mon 01:00 | 41.2 | 45.2 |  |  |  |  |  | 40.0 |
| 10-19 09Z | Mon 02:00 | 41.2 | 45.4 | 42.4 | 40.5 |  | 37.0 | 40.0 | 40.0 |
| 10-19 10Z | Mon 03:00 | 41.3 | 45.7 |  |  |  |  |  | 40.0 |
| 10-19 11Z | Mon 04:00 | 41.4 | 45.8 |  |  |  |  |  | 39.0 |
| 10-19 12Z | Mon 05:00 | 41.9 | 45.7 | 43.2 | 40.6 | 38.4 | 37.0 | 40.0 | 39.0 |
| 10-19 13Z | Mon 06:00 | 42.1 | 45.7 |  |  |  |  |  | 39.0 |
| 10-19 14Z | Mon 07:00 | 41.6 | 45.3 |  |  |  |  |  | 39.0 |
| 10-19 15Z | Mon 08:00 | 41.2 | 45.0 | 41.7 | 39.5 |  | 38.0 | 39.0 | 40.0 |
| 10-19 16Z | Mon 09:00 | 41.1 | 43.3 |  |  |  |  |  | 41.0 |
| 10-19 17Z | Mon 10:00 | 41.3 | 42.8 |  |  |  |  |  | 43.0 |
| 10-19 18Z | Mon 11:00 | 41.0 | 44.6 | 42.8 | 39.9 | 42.2 | 42.0 | 44.0 | 44.0 |
| 10-19 19Z | Mon 12:00 | 40.5 | 44.0 |  |  |  |  |  | 44.0 |
| 10-19 20Z | Mon 13:00 | 37.9 | 43.2 |  |  |  |  |  | 44.0 |
| 10-19 21Z | Mon 14:00 | 35.0 | 42.5 | 41.6 | 38.6 |  | 40.0 | 42.0 | 43.0 |
| 10-19 22Z | Mon 15:00 | 34.8 | 42.1 |  |  |  |  |  | 43.0 |
| 10-19 23Z | Mon 16:00 | 34.8 | 41.3 |  |  |  |  |  | 43.0 |
| 10-20 00Z | Mon 17:00 | 35.3 | 37.7 | 42.4 | 38.4 | 41.5 | 39.0 | 41.0 | 42.0 |
| 10-20 01Z | Mon 18:00 | 36.2 | 40.3 |  |  |  |  |  | 43.0 |
| 10-20 02Z | Mon 19:00 | 35.9 | 42.4 |  |  |  |  |  | 43.0 |
| 10-20 03Z | Mon 20:00 | 37.1 | 43.1 | 42.1 | 37.7 |  | 41.0 | 42.0 | 42.0 |
| 10-20 04Z | Mon 21:00 | 38.4 | 44.3 |  |  |  |  |  | 41.0 |
| 10-20 05Z | Mon 22:00 | 39.8 | 46.5 |  |  |  |  |  | 40.0 |
| 10-20 06Z | Mon 23:00 | 40.2 | 42.9 | 41.5 | 38.8 | 40.3 | 41.0 | 40.0 | 39.0 |

Relative humidity (%), from each model's temperature and dewpoint:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-19 06Z | Sun 23:00 | 88 | 93 | 81 | 83 | 77 | 89 | 93 | 89 |
| 10-19 07Z | Mon 00:00 | 87 | 94 |  |  |  |  |  | 93 |
| 10-19 08Z | Mon 01:00 | 87 | 95 |  |  |  |  |  | 93 |
| 10-19 09Z | Mon 02:00 | 87 | 94 | 88 | 84 |  | 89 | 96 | 93 |
| 10-19 10Z | Mon 03:00 | 88 | 94 |  |  |  |  |  | 93 |
| 10-19 11Z | Mon 04:00 | 88 | 94 |  |  |  |  |  | 93 |
| 10-19 12Z | Mon 05:00 | 90 | 95 | 91 | 83 | 85 | 92 | 100 | 93 |
| 10-19 13Z | Mon 06:00 | 90 | 97 |  |  |  |  |  | 93 |
| 10-19 14Z | Mon 07:00 | 89 | 96 |  |  |  |  |  | 96 |
| 10-19 15Z | Mon 08:00 | 89 | 95 | 97 | 82 |  | 92 | 100 | 100 |
| 10-19 16Z | Mon 09:00 | 82 | 79 |  |  |  |  |  | 93 |
| 10-19 17Z | Mon 10:00 | 71 | 67 |  |  |  |  |  | 86 |
| 10-19 18Z | Mon 11:00 | 60 | 65 | 62 | 57 | 70 | 69 | 74 | 77 |
| 10-19 19Z | Mon 12:00 | 53 | 59 |  |  |  |  |  | 69 |
| 10-19 20Z | Mon 13:00 | 43 | 53 |  |  |  |  |  | 64 |
| 10-19 21Z | Mon 14:00 | 36 | 49 | 50 | 42 |  | 49 | 53 | 57 |
| 10-19 22Z | Mon 15:00 | 35 | 47 |  |  |  |  |  | 55 |
| 10-19 23Z | Mon 16:00 | 35 | 45 |  |  |  |  |  | 55 |
| 10-20 00Z | Mon 17:00 | 36 | 40 | 55 | 45 | 51 | 46 | 49 | 55 |
| 10-20 01Z | Mon 18:00 | 44 | 50 |  |  |  |  |  | 64 |
| 10-20 02Z | Mon 19:00 | 52 | 62 |  |  |  |  |  | 74 |
| 10-20 03Z | Mon 20:00 | 60 | 71 | 74 | 68 |  | 71 | 83 | 80 |
| 10-20 04Z | Mon 21:00 | 68 | 79 |  |  |  |  |  | 86 |
| 10-20 05Z | Mon 22:00 | 78 | 90 |  |  |  |  |  | 89 |
| 10-20 06Z | Mon 23:00 | 84 | 82 | 83 | 86 | 84 | 89 | 96 | 89 |

Wind speed (kt) at the hour:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-19 06Z | Sun 23:00 | 2.6 | 2.3 | 2.4 | 1.7 | 2.7 | 0.0 | 0.0 | 4.0 | 3.1 | 2.4 | 1.8 |
| 10-19 07Z | Mon 00:00 | 2.1 | 1.3 |  |  |  |  |  | 3.0 | 2.6 | 2.2 | 1.4 |
| 10-19 08Z | Mon 01:00 | 2.1 | 0.9 |  |  |  |  |  | 3.0 | 2.2 | 2.0 | 1.1 |
| 10-19 09Z | Mon 02:00 | 2.3 | 1.3 | 1.3 | 0.9 |  | 0.0 | 0.0 | 3.0 | 1.8 | 1.9 | 0.9 |
| 10-19 10Z | Mon 03:00 | 2.2 | 2.1 |  |  |  |  |  | 3.0 | 1.4 | 1.8 | 0.8 |
| 10-19 11Z | Mon 04:00 | 0.6 | 1.9 |  |  |  |  |  | 3.0 | 1.1 | 1.8 | 0.8 |
| 10-19 12Z | Mon 05:00 | 2.9 | 0.5 | 1.1 | 1.0 | 1.4 | 2.0 | 0.0 | 3.0 | 1.0 | 1.7 | 0.9 |
| 10-19 13Z | Mon 06:00 | 2.8 | 2.2 |  |  |  |  |  | 3.0 | 1.0 | 1.6 | 0.9 |
| 10-19 14Z | Mon 07:00 | 3.5 | 3.1 |  |  |  |  |  | 3.0 | 1.1 | 1.5 | 0.9 |
| 10-19 15Z | Mon 08:00 | 3.6 | 4.3 | 1.9 | 2.0 |  | 1.0 | 0.0 | 3.0 | 1.2 | 1.5 | 1.0 |
| 10-19 16Z | Mon 09:00 | 2.6 | 4.4 |  |  |  |  |  | 3.0 | 1.1 | 1.6 | 1.1 |
| 10-19 17Z | Mon 10:00 | 1.9 | 5.4 |  |  |  |  |  | 3.0 | 1.2 | 1.8 | 1.2 |
| 10-19 18Z | Mon 11:00 | 3.4 | 5.2 | 1.1 | 0.5 | 0.7 | 2.0 | 0.0 | 3.0 | 1.5 | 1.9 | 1.3 |
| 10-19 19Z | Mon 12:00 | 3.6 | 4.2 |  |  |  |  |  | 3.0 | 1.6 | 1.8 | 1.3 |
| 10-19 20Z | Mon 13:00 | 3.2 | 4.3 |  |  |  |  |  | 3.0 | 1.8 | 1.7 | 1.6 |
| 10-19 21Z | Mon 14:00 | 3.0 | 3.4 | 1.9 | 0.3 |  | 3.0 | 0.0 | 4.0 | 2.0 | 1.8 | 1.9 |
| 10-19 22Z | Mon 15:00 | 2.6 | 2.7 |  |  |  |  |  | 4.0 | 2.4 | 2.1 | 1.9 |
| 10-19 23Z | Mon 16:00 | 2.4 | 1.5 |  |  |  |  |  | 4.0 | 2.8 | 2.5 | 2.0 |
| 10-20 00Z | Mon 17:00 | 3.0 | 2.4 | 3.5 | 2.6 | 2.1 | 4.0 | 0.0 | 4.0 | 3.2 | 2.8 | 2.1 |
| 10-20 01Z | Mon 18:00 | 4.1 | 3.1 |  |  |  |  |  | 4.0 | 3.1 | 3.0 | 2.1 |
| 10-20 02Z | Mon 19:00 | 4.1 | 4.2 |  |  |  |  |  | 4.0 | 3.1 | 3.2 | 2.0 |
| 10-20 03Z | Mon 20:00 | 4.6 | 4.2 | 4.4 | 3.0 |  | 3.0 | 0.0 | 4.0 | 3.4 | 3.5 | 1.8 |
| 10-20 04Z | Mon 21:00 | 4.5 | 4.2 |  |  |  |  |  | 4.0 | 3.5 | 3.7 | 1.9 |
| 10-20 05Z | Mon 22:00 | 3.9 | 4.1 |  |  |  |  |  | 4.0 | 3.7 | 4.0 | 2.1 |
| 10-20 06Z | Mon 23:00 | 3.5 | 4.2 | 4.2 | 2.7 | 4.2 | 2.0 | 2.0 | 4.0 | 4.0 | 4.3 | 2.4 |

Precipitation (in), accumulated since the start of the day (06Z): 0.00 in every model (HRRR, RRFS, IFS, GFS, AIFS, USL, ENS, AIFS_ENS, GEFS) all day.

Total cloud cover (%):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-19 06Z | Sun 23:00 | 100 | 100 | 100 | 100 | 100 | 100 | 91 | 100 |
| 10-19 07Z | Mon 00:00 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 08Z | Mon 01:00 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 09Z | Mon 02:00 | 100 | 100 | 100 | 100 |  | 100 | 93 | 99 |
| 10-19 10Z | Mon 03:00 | 100 | 100 |  |  |  |  |  | 94 |
| 10-19 11Z | Mon 04:00 | 100 | 100 |  |  |  |  |  | 84 |
| 10-19 12Z | Mon 05:00 | 100 | 100 | 100 | 100 | 93 | 100 | 93 | 79 |
| 10-19 13Z | Mon 06:00 | 100 | 100 |  |  |  |  |  | 83 |
| 10-19 14Z | Mon 07:00 | 100 | 100 |  |  |  |  |  | 92 |
| 10-19 15Z | Mon 08:00 | 100 | 100 | 96 | 100 |  | 100 | 88 | 98 |
| 10-19 16Z | Mon 09:00 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 17Z | Mon 10:00 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 18Z | Mon 11:00 | 100 | 100 | 17 | 100 | 58 | 100 | 84 | 100 |
| 10-19 19Z | Mon 12:00 | 100 | 100 |  |  |  |  |  | 92 |
| 10-19 20Z | Mon 13:00 | 100 | 100 |  |  |  |  |  | 81 |
| 10-19 21Z | Mon 14:00 | 100 | 100 | 56 | 100 |  | 44 | 63 | 72 |
| 10-19 22Z | Mon 15:00 | 100 | 100 |  |  |  |  |  | 68 |
| 10-19 23Z | Mon 16:00 | 100 | 100 |  |  |  |  |  | 67 |
| 10-20 00Z | Mon 17:00 | 100 | 100 | 93 | 84 | 80 | 19 | 52 | 69 |
| 10-20 01Z | Mon 18:00 | 100 | 97 |  |  |  |  |  | 78 |
| 10-20 02Z | Mon 19:00 | 100 | 50 |  |  |  |  |  | 91 |
| 10-20 03Z | Mon 20:00 | 100 | 100 | 100 | 100 |  | 19 | 71 | 98 |
| 10-20 04Z | Mon 21:00 | 61 | 100 |  |  |  |  |  | 99 |
| 10-20 05Z | Mon 22:00 | 41 | 100 |  |  |  |  |  | 100 |
| 10-20 06Z | Mon 23:00 | 82 | 100 | 70 | 92 | 70 | 19 | 44 | 100 |

## Track record this period

Since 2026-09-28 at KOLM (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-13 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 20 | 5.8 | -0.6 | +1.3 | -1.0 | +0.01 | 2.0 | 2.9 | 2.0 | 0.01 |
| NBM | 20 | 6.7 | +0.0 | +2.1 | -3.4 | +0.00 | 1.4 | 3.3 | 3.8 | 0.01 |
| GFS_MOS | 20 | 6.9 | -0.3 | +0.9 | -3.9 | +0.01 | 2.6 | 2.3 | 4.1 | 0.01 |
| USL | 7 | 7.3 | -2.2 | +2.4 | -0.6 | +0.01 | 2.8 | 3.6 | 1.8 | 0.01 |
| HRRR | 20 | 9.3 | +0.8 | +4.6 | -2.9 | +0.00 | 2.8 | 5.1 | 3.2 | 0.01 |
| RRFS | 20 | 10.2 | -0.1 | +6.4 | -2.9 | +0.01 | 2.4 | 6.5 | 3.0 | 0.01 |
| AIFS | 20 | 10.3 | -1.9 | +5.2 | -4.6 | +0.01 | 2.8 | 5.5 | 4.8 | 0.01 |
| GFS | 20 | 10.6 | +0.2 | +4.5 | -4.8 | +0.01 | 3.1 | 5.2 | 4.9 | 0.01 |
| IFS | 20 | 11.0 | -2.2 | +6.2 | -4.2 | +0.01 | 2.6 | 6.4 | 4.3 | 0.01 |
| AIFS_ENS | 5 | 11.3 | -1.8 | +5.9 | -3.6 | +0.01 | 3.4 | 5.9 | 3.6 | 0.01 |
| GEFS | 5 | 12.0 | -1.2 | +5.3 | -5.0 | +0.01 | 3.6 | 5.3 | 5.0 | 0.01 |
| ENS | 4 | 13.1 | -1.2 | +7.7 | -4.2 | +0.02 | 2.6 | 7.7 | 4.2 | 0.02 |

## Daily verification (all 20 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 12.0 | 11.5 | 14.0 | 10.0 | 12.0 | 5.5 | 8.5 | — | — | — | — | 9.0 | GFS_MOS |
| 09-29 h | 11.5 | 10.0 | 11.1 | 13.4 | 5.6 | 4.8 | 10.8 | — | — | — | — | 6.3 | GFS_MOS |
| 09-30 h | 7.5 | 6.0 | 6.0 | 5.5 | 7.0 | 6.0 | 5.5 | — | — | — | — | 4.0 | CONSENSUS |
| 10-01 h | 6.0 | 7.0 | 8.0 | 5.5 | 8.0 | 1.5 | 2.0 | — | — | — | — | 1.0 | CONSENSUS |
| 10-02 h | 9.0 | 10.0 | 11.5 | 8.5 | 10.0 | 6.5 | 3.5 | — | — | — | — | 5.0 | NBM |
| 10-03 h | 10.5 | 10.5 | 10.0 | 13.5 | 10.5 | 9.5 | 8.0 | — | — | — | — | 7.5 | CONSENSUS |
| 10-04 h | 11.0 | 12.5 | 10.0 | 15.0 | 8.0 | 4.0 | 8.5 | — | — | — | — | 5.0 | GFS_MOS |
| 10-05 h | 2.5 | 10.0 | 11.5 | 6.5 | 7.5 | 1.0 | 4.0 | — | — | — | — | 2.0 | GFS_MOS |
| 10-06 h | 3.5 | 8.5 | 8.5 | 9.0 | 4.5 | 5.0 | 4.5 | — | — | — | — | 3.0 | CONSENSUS |
| 10-07 h | 10.5 | 7.0 | 6.0 | 14.0 | 8.5 | 16.0 | 10.0 | — | — | — | — | 10.5 | IFS |
| 10-08 h | 4.5 | 4.5 | 8.5 | 9.5 | 7.0 | 3.5 | 2.0 | — | — | — | — | 4.5 | NBM |
| 10-09 h | 12.7 | 11.9 | 16.0 | 10.5 | 19.2 | 12.0 | 8.3 | — | — | — | — | 9.1 | NBM |
| 10-10 h | 7.5 | 10.0 | 9.4 | 7.8 | 12.8 | 9.0 | 2.5 | — | — | — | — | 4.4 | NBM |
| 10-11 h | 12.0 | 12.0 | 16.0 | 11.5 | 16.0 | 8.5 | 10.0 | 6.5 | — | — | — | 6.5 | USL |
| 10-12 h | 11.0 | 12.0 | 16.5 | 9.0 | 12.5 | 7.5 | 10.5 | 5.5 | — | — | — | 7.0 | USL |
| 10-13 | 2.0 | 7.4 | 7.0 | 10.5 | 5.0 | 3.5 | 3.5 | 5.5 | — | 5.5 | 10.5 | 4.5 | HRRR |
| 10-14 | 7.0 | 11.5 | 9.9 | 8.5 | 8.8 | 4.5 | 4.0 | 8.0 | 9.4 | 9.8 | 10.4 | 0.9 | CONSENSUS |
| 10-15 | 17.5 | 17.0 | 11.0 | 15.5 | 12.0 | 8.0 | 8.5 | 7.5 | 13.0 | 12.5 | 14.5 | 7.5 | CONSENSUS |
| 10-16 | 14.0 | 15.0 | 19.0 | 20.0 | 20.5 | 14.5 | 13.0 | 10.0 | 19.0 | 17.5 | 17.5 | 10.5 | USL |
| 10-17 | 14.0 | 9.5 | 10.2 | 7.4 | 11.1 | 7.1 | 5.4 | 8.2 | 10.9 | 11.1 | 7.0 | 8.6 | NBM |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 67 | -1 | +0 | -2 | +1 | -3 | +1 | +1 | — | — | — | — | +0 |
| 09-29 h | 61 | +0 | -3 | -2 | -4 | +0 | +2 | +0 | — | — | — | — | -1 |
| 09-30 h | 66 | -4 | -2 | -2 | -2 | -2 | -1 | -1 | — | — | — | — | -2 |
| 10-01 h | 71 | +1 | +1 | -4 | +0 | -3 | +1 | -1 | — | — | — | — | +0 |
| 10-02 h | 73 | -4 | -3 | -4 | -2 | -3 | -2 | -1 | — | — | — | — | -2 |
| 10-03 h | 70 | +3 | +1 | -1 | +5 | +1 | +5 | +2 | — | — | — | — | +3 |
| 10-04 h | 72 | +6 | +3 | +1 | +6 | +1 | +2 | +3 | — | — | — | — | +3 |
| 10-05 h | 70 | +1 | -2 | -4 | +2 | -3 | +0 | +1 | — | — | — | — | -1 |
| 10-06 h | 68 | -1 | +1 | -3 | +4 | +0 | +2 | +1 | — | — | — | — | +1 |
| 10-07 h | 68 | +4 | +1 | -1 | +6 | +1 | +4 | +2 | — | — | — | — | +2 |
| 10-08 h | 73 | +1 | +0 | -2 | +4 | -2 | -3 | +0 | — | — | — | — | -1 |
| 10-09 h | 62 | +0 | -1 | -3 | -1 | -4 | +2 | +0 | — | — | — | — | -1 |
| 10-10 h | 59 | +1 | +1 | -2 | +0 | -1 | +1 | +0 | — | — | — | — | +0 |
| 10-11 h | 62 | +2 | +1 | -1 | +0 | -1 | +0 | +1 | +0 | — | — | — | +0 |
| 10-12 h | 64 | +1 | -1 | -2 | +0 | -2 | -2 | +1 | -1 | — | — | — | -1 |
| 10-13 | 63 | +1 | -4 | -3 | -5 | -2 | -3 | +0 | -3 | — | -2 | -5 | -2 |
| 10-14 | 66 | +0 | +3 | +0 | -1 | +0 | +1 | +0 | -3 | +0 | +0 | +1 | +0 |
| 10-15 | 67 | +11 | +7 | +2 | +7 | +4 | +4 | +3 | +2 | +3 | +4 | +5 | +5 |
| 10-16 | 79 | -2 | -3 | -4 | -5 | -8 | -10 | -4 | -5 | -3 | -5 | -4 | -5 |
| 10-17 | 67 | -6 | -3 | -6 | -4 | -6 | +0 | -3 | -4 | -4 | -5 | -3 | -4 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 34 | +9 | +9 | +10 | +7 | +6 | +3 | +5 | — | — | — | — | +7 |
| 09-29 h | 55 | -4 | -2 | -3 | -5 | -2 | +0 | -5 | — | — | — | — | -3 |
| 09-30 h | 47 | -1 | +2 | +1 | +0 | +2 | +2 | -2 | — | — | — | — | +0 |
| 10-01 h | 43 | +4 | +5 | +3 | +4 | +4 | +0 | +0 | — | — | — | — | +1 |
| 10-02 h | 46 | +4 | +6 | +5 | +4 | +4 | +2 | +0 | — | — | — | — | +2 |
| 10-03 h | 46 | +5 | +7 | +6 | +5 | +6 | +1 | +4 | — | — | — | — | +3 |
| 10-04 h | 43 | +4 | +8 | +7 | +7 | +5 | +1 | +4 | — | — | — | — | +2 |
| 10-05 h | 46 | +1 | +8 | +6 | +4 | +3 | -1 | +2 | — | — | — | — | +0 |
| 10-06 h | 48 | +1 | +6 | +3 | +2 | +2 | -1 | +1 | — | — | — | — | -1 |
| 10-07 h | 50 | -3 | +3 | +1 | -3 | -3 | -8 | -5 | — | — | — | — | -6 |
| 10-08 h | 43 | +2 | +4 | +6 | +5 | +4 | +0 | +0 | — | — | — | — | +1 |
| 10-09 h | 40 | +8 | +8 | +8 | +4 | +8 | +5 | +5 | — | — | — | — | +5 |
| 10-10 h | 36 | +5 | +8 | +6 | +5 | +9 | +6 | +2 | — | — | — | — | +4 |
| 10-11 h | 30 | +9 | +10 | +12 | +8 | +11 | +6 | +7 | +6 | — | — | — | +6 |
| 10-12 h | 28 | +10 | +11 | +14 | +9 | +9 | +5 | +7 | +4 | — | — | — | +5 |
| 10-13 | 39 | +0 | +2 | +2 | +4 | +1 | +0 | -2 | -2 | — | +2 | +4 | -2 |
| 10-14 | 44 | +6 | +7 | +7 | +5 | +6 | -1 | +2 | +4 | +7 | +7 | +6 | +0 |
| 10-15 | 40 | +4 | +8 | +7 | +6 | +6 | +1 | +4 | +5 | +8 | +7 | +7 | +2 |
| 10-16 | 37 | +10 | +9 | +12 | +11 | +10 | +0 | +6 | +3 | +13 | +10 | +10 | +4 |
| 10-17 | 45 | +5 | +3 | +1 | -1 | +2 | -2 | -1 | -2 | +3 | +3 | +0 | -3 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 12 | -4 | -5 | -4 | -4 | -6 | -3 | -5 | — | — | — | — | -4 |
| 09-29 h | 15 | -3 | -3 | -4 | -7 | -6 | -3 | -2 | — | — | — | — | -4 |
| 09-30 h | 11 | -5 | -4 | -6 | -7 | -6 | -6 | -5 | — | — | — | — | -4 |
| 10-01 h | 6 | -2 | -2 | -2 | -3 | -2 | -1 | -2 | — | — | — | — | +0 |
| 10-02 h | 10 | -2 | -2 | -5 | -5 | -6 | -5 | -5 | — | — | — | — | -2 |
| 10-03 h | 12 | -5 | -5 | -6 | -7 | -7 | -7 | -4 | — | — | — | — | -3 |
| 10-04 h | 7 | -2 | -3 | -4 | -4 | -4 | -2 | -3 | — | — | — | — | +0 |
| 10-05 h | 5 | -1 | +0 | -3 | -1 | -3 | +0 | -2 | — | — | — | — | +2 |
| 10-06 h | 10 | -3 | -3 | -5 | -6 | -5 | -4 | -5 | — | — | — | — | -2 |
| 10-07 h | 14 | -7 | -6 | -8 | -10 | -9 | -8 | -6 | — | — | — | — | -5 |
| 10-08 h | 4 | +3 | +1 | +1 | +1 | +2 | +1 | +4 | — | — | — | — | +5 |
| 10-09 h | 19 | -7 | -5 | -6 | -7 | -8 | -6 | -5 | — | — | — | — | -3 |
| 10-10 h | 10 | -3 | -2 | -2 | -4 | -4 | -4 | -1 | — | — | — | — | +0 |
| 10-11 h | 12 | -2 | -2 | -6 | -7 | -8 | -5 | -4 | -1 | — | — | — | -1 |
| 10-12 h | 5 | +0 | +0 | -1 | +0 | -3 | +1 | -5 | +1 | — | — | — | +2 |
| 10-13 | 7 | -2 | -2 | -4 | -3 | -4 | -1 | -3 | +1 | — | -3 | -3 | +1 |
| 10-14 | 9 | -2 | -3 | -5 | -5 | -4 | -5 | -4 | -2 | -4 | -4 | -6 | -1 |
| 10-15 | 9 | -5 | -4 | -4 | -5 | -4 | -6 | -3 | -1 | -4 | -3 | -5 | -1 |
| 10-16 | 12 | -4 | -6 | -6 | -8 | -5 | -9 | -6 | -4 | -6 | -5 | -7 | -3 |
| 10-17 | 11 | -2 | -3 | -4 | -4 | -3 | -3 | -2 | +2 | -3 | -3 | -4 | +0 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 09-29 h | 0.22 | -0.18 | +0.16 | +0.19 | +0.03 | -0.02 | +0.05 | -0.15 | — | — | — | — | +0.01 |
| 09-30 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-01 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-02 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-03 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-04 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-05 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-06 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-07 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-08 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-09 h | 0.00 | +0.03 | +0.01 | +0.05 | +0.05 | +0.08 | +0.05 | +0.02 | — | — | — | — | +0.04 |
| 10-10 h | 0.00 | +0.00 | +0.00 | +0.01 | +0.02 | +0.02 | +0.00 | +0.00 | — | — | — | — | +0.01 |
| 10-11 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-12 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-13 | 0.00 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 | +0.00 | +0.00 |
| 10-14 | 0.00 | +0.00 | +0.00 | +0.01 | +0.00 | +0.02 | +0.00 | +0.00 | +0.00 | +0.01 | +0.02 | +0.01 | +0.01 |
| 10-15 | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-16 | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-17 | 0.01 | +0.05 | +0.05 | +0.03 | +0.01 | +0.04 | +0.09 | +0.01 | +0.03 | +0.06 | +0.04 | +0.05 | +0.04 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 20 | +4 | 20 | +18 | 33 |
| RRFS | 20 | -8 | 29 | +9 | 30 |
| IFS | 20 | -1 | 22 | +9 | 25 |
| GFS | 20 | -2 | 33 | +8 | 25 |
| AIFS | 20 | -2 | 26 | +8 | 32 |
| GFS_MOS | 20 | -5 | 31 | +3 | 28 |
| NBM | 20 | -10 | 27 | +1 | 21 |
| USL | 7 | -13 | 21 | +5 | 22 |

Night clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 0% | — | +49 | +38 | +49 | +68 | +62 | +11 | +30 | — |
| 09-29 h | 100% | — | +0 | -1 | +0 | +0 | -1 | +0 | -17 | — |
| 09-30 h | 88% | — | -38 | -47 | -45 | -39 | -12 | +12 | -23 | — |
| 10-01 h | 0% | — | +99 | +99 | +89 | +100 | +100 | +88 | +80 | — |
| 10-02 h | 47% | — | -24 | -10 | -6 | +31 | +14 | +33 | -23 | — |
| 10-03 h | 19% | — | +81 | +76 | +74 | +72 | +68 | +27 | +46 | — |
| 10-04 h | 49% | — | -11 | -19 | -37 | -30 | -17 | -47 | -23 | — |
| 10-05 h | 80% | — | +1 | -22 | +5 | -55 | -7 | -50 | -32 | — |
| 10-06 h | 89% | — | -24 | -20 | -6 | -25 | -17 | -34 | -30 | — |
| 10-07 h | 69% | — | +20 | +5 | +10 | -51 | -26 | -69 | -23 | — |
| 10-08 h | 56% | — | +11 | -14 | -48 | +32 | -10 | -54 | -21 | — |
| 10-09 h | — | — | — | — | — | — | — | — | — | — |
| 10-10 h | 14% | — | -14 | -13 | -8 | +28 | +12 | +86 | +17 | — |
| 10-11 h | 13% | — | -10 | -10 | -9 | -12 | +0 | -5 | -1 | -6 |
| 10-12 h | 0% | 3% | +0 | +0 | +0 | +0 | +10 | +2 | +7 | +0 |
| 10-13 | 89% | 84% | -40 | -51 | -18 | -41 | -27 | -1 | -50 | -43 |
| 10-14 | 97% | 100% | +1 | -24 | +3 | -10 | -8 | +3 | -11 | -8 |
| 10-15 | 69% | 44% | -10 | -28 | -33 | -60 | -35 | -64 | -36 | -23 |
| 10-16 | 78% | 13% | +3 | -44 | -10 | +15 | -52 | -14 | -40 | -37 |
| 10-17 | 61% | 100% | +35 | +39 | +32 | +28 | +33 | +26 | +21 | +20 |

Day clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 34% | — | +20 | +32 | +41 | +52 | +50 | +46 | +16 | — |
| 09-29 h | 100% | — | +0 | -1 | +0 | -4 | -6 | +0 | -17 | — |
| 09-30 h | 19% | — | +67 | +50 | +60 | +77 | +62 | +59 | +25 | — |
| 10-01 h | 2% | — | +98 | +98 | +93 | +98 | +93 | +69 | +66 | — |
| 10-02 h | 70% | — | -6 | -38 | -11 | -4 | -4 | +29 | -22 | — |
| 10-03 h | 54% | — | -18 | -11 | -15 | -45 | -31 | -24 | -14 | — |
| 10-04 h | 56% | — | +36 | -2 | -38 | -36 | -33 | -53 | -19 | — |
| 10-05 h | 56% | — | +44 | +42 | +21 | +16 | +18 | +15 | +14 | — |
| 10-06 h | 50% | — | +46 | +46 | +33 | +11 | +33 | -11 | -1 | — |
| 10-07 h | 52% | — | -17 | -14 | -1 | -48 | -40 | -52 | -17 | — |
| 10-08 h | 36% | — | +55 | +53 | +18 | +6 | +39 | -22 | +15 | — |
| 10-09 h | 22% | — | +39 | +31 | +6 | +36 | +36 | +48 | +23 | — |
| 10-10 h | 52% | — | -41 | -30 | -31 | +4 | -15 | +32 | -9 | — |
| 10-11 h | 18% | — | -15 | -14 | -10 | -18 | -12 | -10 | -5 | -17 |
| 10-12 h | 0% | 0% | +0 | +10 | +1 | +1 | +5 | +10 | +8 | +1 |
| 10-13 | 90% | 94% | +10 | -5 | +9 | +0 | +0 | +10 | -28 | -8 |
| 10-14 | 100% | 87% | -30 | -48 | -29 | -31 | -48 | -23 | -30 | -11 |
| 10-15 | 54% | 44% | -9 | -29 | -20 | -2 | -37 | -46 | -28 | -26 |
| 10-16 | 20% | 40% | +77 | +66 | +32 | +57 | +43 | +9 | +27 | +40 |
| 10-17 | 12% | 49% | +39 | +10 | +58 | +26 | +55 | +36 | +28 | +36 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles have no dewpoint; USL only from when it started for this city). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 20 | +0.4 | 2.8 | -2.5 | 2.6 |
| RRFS | 20 | +3.0 | 3.9 | -1.2 | 1.4 |
| IFS | 20 | +1.5 | 2.4 | +0.3 | 1.1 |
| GFS | 20 | +0.6 | 2.5 | -2.5 | 2.7 |
| AIFS | 20 | +0.4 | 2.0 | -0.4 | 1.5 |
| GFS_MOS | 20 | -0.7 | 2.0 | -0.6 | 2.3 |
| NBM | 20 | +0.8 | 1.9 | +0.4 | 1.5 |
| USL | 7 | +0.5 | 1.4 | +0.8 | 1.8 |

Night dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 37.4 | +4.5 | +7.2 | +2.7 | -0.2 | +3.3 | +1.1 | +2.8 | — |
| 09-29 h | 51.3 | -1.2 | -1.6 | -0.5 | -1.4 | -0.3 | +0.6 | -1.8 | — |
| 09-30 h | 51.8 | -3.5 | -3.0 | -3.1 | -3.5 | -2.1 | -0.2 | -3.7 | — |
| 10-01 h | 45.3 | +2.6 | +2.6 | +0.2 | -2.8 | -1.0 | -1.5 | +0.0 | — |
| 10-02 h | 50.0 | -0.8 | +0.1 | +0.0 | -0.8 | -0.9 | +0.0 | -1.9 | — |
| 10-03 h | 49.9 | +3.6 | +5.6 | +3.4 | +2.1 | +2.8 | -0.2 | +2.8 | — |
| 10-04 h | 46.9 | +3.4 | +6.5 | +2.9 | +3.4 | +2.3 | +0.8 | +3.2 | — |
| 10-05 h | 49.2 | +0.5 | +5.4 | +3.3 | +2.2 | +1.2 | -1.4 | +1.8 | — |
| 10-06 h | 52.6 | -1.5 | +3.1 | +1.0 | -0.2 | -1.5 | -2.6 | -0.2 | — |
| 10-07 h | 51.9 | -3.6 | +1.4 | -0.7 | -4.4 | -5.8 | -6.7 | -2.7 | — |
| 10-08 h | 44.9 | +2.3 | +5.2 | +1.7 | +2.7 | +0.6 | +1.2 | +1.2 | — |
| 10-09 h | — | — | — | — | — | — | — | — | — |
| 10-10 h | 39.4 | +1.6 | +4.2 | +3.6 | +2.8 | +1.5 | +1.9 | +1.7 | — |
| 10-11 h | 35.1 | +4.9 | +6.7 | +5.8 | +3.4 | +4.6 | +2.3 | +5.0 | +2.5 |
| 10-12 h | 31.9 | +0.8 | +6.1 | +4.7 | +3.4 | +4.2 | +4.1 | +3.1 | +2.6 |
| 10-13 | 39.3 | -6.7 | -4.7 | -2.7 | -2.2 | -0.9 | -0.9 | -0.4 | -1.9 |
| 10-14 | 46.4 | -4.0 | +0.2 | -1.6 | -4.0 | -1.9 | -2.8 | -2.1 | -1.0 |
| 10-15 | 45.5 | +2.3 | +3.8 | +2.4 | +1.7 | +1.1 | +0.0 | +1.7 | +1.1 |
| 10-16 | 40.9 | +4.3 | +6.9 | +2.5 | +4.2 | +1.1 | -0.8 | +2.2 | +1.5 |
| 10-17 | 52.5 | -0.2 | +1.0 | +0.7 | -0.4 | -1.3 | -4.4 | -0.2 | -0.4 |

Day dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 44.3 | +0.6 | -0.9 | +2.0 | -0.8 | +1.7 | -0.1 | +1.9 | — |
| 09-29 h | 56.3 | -2.1 | -3.1 | -0.7 | -5.3 | -0.9 | -0.6 | -2.2 | — |
| 09-30 h | 48.3 | +0.2 | -0.1 | +0.2 | +0.9 | +0.5 | +2.0 | +0.1 | — |
| 10-01 h | 50.0 | +1.0 | +0.1 | -1.2 | -5.7 | -2.9 | -2.9 | -1.8 | — |
| 10-02 h | 55.1 | -0.2 | +0.8 | +0.1 | -1.0 | -0.4 | -0.9 | -1.3 | — |
| 10-03 h | 55.1 | -0.9 | +0.0 | +0.4 | -2.9 | -1.0 | -2.8 | -0.3 | — |
| 10-04 h | 53.2 | -1.3 | +1.8 | +1.1 | -1.4 | -0.1 | -1.9 | +0.6 | — |
| 10-05 h | 54.2 | -4.5 | -0.5 | -1.3 | -1.1 | -1.5 | -1.6 | -1.2 | — |
| 10-06 h | 55.2 | -2.9 | -1.7 | -1.3 | -3.6 | -3.2 | -4.0 | -2.4 | — |
| 10-07 h | 52.9 | -3.9 | -0.3 | -0.3 | -5.7 | -4.4 | -5.6 | -2.3 | — |
| 10-08 h | 52.1 | -3.3 | -2.3 | -2.5 | -4.0 | -2.2 | -1.5 | -2.3 | — |
| 10-09 h | 44.0 | -5.8 | -1.8 | +1.2 | +0.7 | +0.6 | +5.2 | +2.6 | — |
| 10-10 h | 41.3 | -2.0 | -0.8 | -0.2 | -1.6 | +0.9 | +1.6 | +1.0 | — |
| 10-11 h | 39.6 | -2.1 | -2.1 | +1.2 | -5.0 | +0.8 | -2.7 | +0.6 | -1.1 |
| 10-12 h | 36.2 | -3.6 | +0.0 | +2.7 | -0.5 | +2.7 | +1.7 | +2.6 | +2.3 |
| 10-13 | 39.2 | -6.9 | -3.5 | -1.2 | +0.5 | +2.2 | +2.8 | +3.1 | +3.5 |
| 10-14 | 50.6 | -1.5 | -0.1 | +0.4 | -2.1 | -0.5 | -1.0 | +0.1 | -0.4 |
| 10-15 | 51.4 | -4.7 | -2.2 | +0.3 | -4.5 | -3.2 | -4.7 | -0.8 | -2.1 |
| 10-16 | 44.5 | -0.2 | -2.7 | +0.0 | -4.5 | +0.1 | -0.2 | +1.0 | +0.6 |
| 10-17 | 44.5 | -1.0 | -0.9 | +2.5 | -1.4 | +0.3 | +1.5 | +2.2 | +2.5 |

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-13 | 0.00" (dry) | 2/7/9/3 | 7/9/6/3 | 0/2/2/16 | 2/0/0/2 | 0/0/0/10 | 24h 22% | 24h 7% | 0/0/0/0 |
| 10-14 | 0.00" (dry) | 9/20/1/2 | 10/11/3/0 | 6/39/8/0 | 33/26/2/0 | 3/29/0/0 | 24h 0% | 24h 7% | 0/9/0/0 |
| 10-15 | 0.00" (dry) | 0/0/1/1 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 24h 28% | 24h 0% | 0/0/0/0 |
| 10-16 | 0.00" (dry) | 0/2/1/5 | 0/1/1/1 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 24h 11% | 24h 0% | 0/0/0/0 |
| 10-17 | 0.01" (wet: 06-12) | 65/50/2/1 | 58/26/0/0 | 98/84/0/0 | 72/33/4/2 | 100/36/0/0 | 24h 28% | 24h 64% | 66/14/0/9 |

## Today so far (2026-10-18, through 2026-10-18T20:54Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 60.1 °F, low 30.9 °F, max wind 9 kt, precip 0.00" (15 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 17/18Z | +4.8 | 4.8 | 60 (+0) pending | 39 (+8) | +2.0 | 0.00 | +0.00 |
| RRFS | 17/18Z | +5.8 | 5.8 | 61 (+1) pending | 40 (+9) | +2.3 | 0.00 | +0.00 |
| IFS | 17/12Z | +5.4 | 6.0 | 58 (-2) | 42 (+11) | +1.6 | 0.00 | +0.00 |
| GFS | 17/12Z | +4.6 | 4.7 | 60 (+0) | 40 (+9) | +0.8 | 0.00 | +0.00 |
| AIFS | 17/12Z | +5.0 | 6.0 | 59 (-1) | 41 (+10) | +1.9 | 0.00 | +0.00 |
| GFS_MOS | 17/12Z | +3.5 | 4.0 | 61 (+1) pending | 38 (+7) | -0.1 | — | — |
| NBM | 17/18Z | +2.2 | 2.9 | 60 (+0) | 35 (+4) | +0.8 | — | — |
| USL | 17/12Z | +1.7 | 2.4 | 59 (-1) | 36 (+5) | +2.6 | 0.00 | +0.00 |
| ENS | 17/06Z | +6.8 | 7.0 | 59 (-1) | 44 (+13) | +1.9 | 0.00 | +0.00 |
| AIFS_ENS | 17/12Z | +5.5 | 6.2 | 59 (-1) | 42 (+11) | +1.7 | 0.00 | +0.00 |
| GEFS | 17/12Z | +4.9 | 4.9 | 61 (+1) pending | 40 (+10) | +0.2 | 0.00 | +0.00 |

## Clouds so far today (2026-10-18, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (PDT) | GOES | METAR | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-18 06Z | Sat 23:00 | 0 |  | 1 | 21 | 7 | 1 | 30 | 0 | 10 | 54 |
| 10-18 07Z | Sun 00:00 | 0 | 0 | 2 | 0 |  |  |  |  |  | 37 |
| 10-18 08Z | Sun 01:00 | 0 | 0 | 1 | 0 |  |  |  |  |  | 15 |
| 10-18 09Z | Sun 02:00 | 0 | 0 | 4 | 0 | 2 | 4 |  | 0 | 9 | 3 |
| 10-18 10Z | Sun 03:00 | 0 | 0 | 2 | 0 |  |  |  |  |  | 2 |
| 10-18 11Z | Sun 04:00 | 0 | 44 | 0 | 0 |  |  |  |  |  | 2 |
| 10-18 12Z | Sun 05:00 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 19 | 10 | 2 |
| 10-18 13Z | Sun 06:00 | 9 | 19 | 2 | 0 |  |  |  |  |  | 1 |
| 10-18 14Z | Sun 07:00 | 32 | 100 | 10 | 2 |  |  |  |  |  | 1 |
| 10-18 15Z | Sun 08:00 | 16 | 100 | 100 | 23 | 26 | 0 |  | 19 | 56 | 0 |
| 10-18 16Z | Sun 09:00 | 39 | 100 | 100 | 28 |  |  |  |  |  | 0 |
| 10-18 17Z | Sun 10:00 | 58 | 100 | 11 | 0 |  |  |  |  |  | 1 |
| 10-18 18Z | Sun 11:00 | 24 | 100 | 90 | 0 | 43 | 62 | 58 | 19 | 53 | 3 |
| 10-18 19Z | Sun 12:00 | 36 | 44 | 100 | 72 |  |  |  |  |  | 14 |
| 10-18 20Z | Sun 13:00 | 6 | 0 | 100 | 69 |  |  |  |  |  | 33 |
| 10-18 21Z | Sun 14:00 | 94 | 0 | 100 | 100 | 100 | 100 |  | 0 | 39 | 44 |

## Dewpoint so far today (2026-10-18, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (PDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-18 07Z | Sun 00:00 | 39.9 | 85 | 39.7 | 41.4 |  |  |  |  |  | 41.0 |
| 10-18 08Z | Sun 01:00 | 39.9 | 100 | 40.2 | 41.7 |  |  |  |  |  | 40.0 |
| 10-18 09Z | Sun 02:00 | 39.0 | 97 | 40.6 | 41.1 | 42.2 | 41.2 |  | 40.0 | 41.0 | 39.0 |
| 10-18 10Z | Sun 03:00 | 37.0 | 100 | 40.5 | 41.7 |  |  |  |  |  | 38.0 |
| 10-18 11Z | Sun 04:00 | 35.1 | 100 | 39.9 | 41.3 |  |  |  |  |  | 38.0 |
| 10-18 12Z | Sun 05:00 | 34.0 | 100 | 39.5 | 40.7 | 41.3 | 40.6 | 38.6 | 39.0 | 39.0 | 37.0 |
| 10-18 13Z | Sun 06:00 | 33.1 | 100 | 38.9 | 40.5 |  |  |  |  |  | 37.0 |
| 10-18 14Z | Sun 07:00 | 34.0 | 100 | 38.7 | 40.1 |  |  |  |  |  | 36.0 |
| 10-18 15Z | Sun 08:00 | 34.0 | 100 | 38.4 | 40.0 | 41.4 | 39.1 |  | 38.0 | 38.0 | 37.0 |
| 10-18 16Z | Sun 09:00 | 37.9 | 100 | 41.1 | 42.9 |  |  |  |  |  | 39.0 |
| 10-18 17Z | Sun 10:00 | 44.1 | 97 | 43.0 | 44.5 |  |  |  |  |  | 42.0 |
| 10-18 18Z | Sun 11:00 | 46.0 | 97 | 43.0 | 43.5 | 44.1 | 40.0 | 41.6 | 41.0 | 44.0 | 43.0 |
| 10-18 19Z | Sun 12:00 | 45.0 | 80 | 39.8 | 42.7 |  |  |  |  |  | 43.0 |
| 10-18 20Z | Sun 13:00 | 44.1 | 62 | 38.4 | 41.3 |  |  |  |  |  | 42.0 |
| 10-18 21Z | Sun 14:00 | 44.1 | 55 | 36.1 | 39.3 | 43.2 | 37.8 |  | 39.0 | 41.0 | 41.0 |
| Bias so far |  |  |  | +0.7 | +2.4 | +3.0 | +0.3 | +0.1 | +0.0 | +1.2 | +0.4 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (SEW): https://forecast.weather.gov/product.php?site=SEW&issuedby=SEW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
