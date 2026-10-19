# WxChallenge forecast brief: Olympia, WA (KOLM)

- Station: **KOLM**
- Target day: **2026-10-20**, scored over 2026-10-20T06Z to 2026-10-21T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-20T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-19T20:30:09+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 19/18Z | 66.6 | 41.3 | 8.0 | 0.00 |
| RRFS | 19/18Z | 63.0 | 43.1 | 8.9 | 0.00 |
| IFS | 19/12Z | 62.4 | 43.8 | 7.0 | 0.00 |
| GFS | 19/12Z | 64.3 | 40.5 | 7.0 | 0.00 |
| AIFS | 19/12Z | 61.7 | 42.1 | 6.4 | 0.00 |
| GFS_MOS | 19/12Z | 66.0 | 36.0 | 5.0 | 0.00 |
| NBM | 19/18Z | 64.0 | 36.0 | 9.0 | 0.00 |
| USL | 19/12Z | 62.0 | 38.0 | 11.0 | 0.00 |
| ENS | 19/06Z | 63.1 | 44.6 | 6.9 | 0.00 |
| AIFS_ENS | 19/06Z | 61.4 | 42.3 | 6.4 | 0.00 |
| GEFS | 19/12Z | 64.6 | 42.0 | 6.3 | 0.00 |
| HRRRCAST (precip only) | 19/12Z | — | — | — | 0.01 |
| REFS (precip only) | 19/18Z | — | — | — | 0.00 |
| NBM_QMD (precip only) | 19/12Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **64.2** | **35.8** | **10.6** | **0.00** |

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

- High °F weights: NBM 0.15, RRFS 0.11, GFS_MOS 0.10, ENS 0.10, HRRR 0.09, IFS 0.09, USL 0.09, AIFS 0.09, GFS 0.09, AIFS_ENS 0.08
- Low °F weights: GFS_MOS 0.17, NBM 0.14, USL 0.13, HRRR 0.09, GFS 0.09, AIFS 0.09, RRFS 0.08, IFS 0.08, AIFS_ENS 0.07, ENS 0.06
- Wind kt weights: USL 0.19, RRFS 0.11, HRRR 0.11, NBM 0.10, AIFS_ENS 0.09, ENS 0.09, IFS 0.08, GFS_MOS 0.08, GFS 0.07, AIFS 0.07
- Precip in weights: GFS 0.10, NBM 0.10, USL 0.10, HRRR 0.10, RRFS 0.10, IFS 0.10, AIFS 0.10, GFS_MOS 0.10, AIFS_ENS 0.10, ENS 0.10

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 62.4 | 62.8 | 63.1 | 63.8 | 64.2 | 63.1 |
| ENS | 51 | Low °F | 43.5 | 44.0 | 44.5 | 45.1 | 45.6 | 44.6 |
| ENS | 51 | Wind kt | 5.8 | 6.2 | 6.9 | 7.4 | 8.1 | 6.9 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| AIFS_ENS | 51 | High °F | 59.2 | 60.3 | 61.4 | 62.6 | 63.4 | 61.4 |
| AIFS_ENS | 51 | Low °F | 39.6 | 41.5 | 42.6 | 43.8 | 44.7 | 42.3 |
| AIFS_ENS | 51 | Wind kt | 4.9 | 5.4 | 6.3 | 7.1 | 8.3 | 6.4 |
| AIFS_ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| GEFS | 31 | High °F | 62.5 | 63.6 | 64.7 | 65.7 | 66.2 | 64.6 |
| GEFS | 31 | Low °F | 41.0 | 41.4 | 41.9 | 42.6 | 42.8 | 42.0 |
| GEFS | 31 | Wind kt | 5.8 | 5.8 | 6.2 | 6.7 | 6.9 | 6.3 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 0% | 0% | 0% | 0% |
| AIFS_ENS | 4% | 0% | 0% | 0% |
| GEFS | 0% | 0% | 0% | 0% |
| HRRRCAST | 28% | 0% | 0% | 0% |
| REFS | 0% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.00", p90 0.00"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 1% | 2% | 1% | 1% | 2% to 5% | 0.02 (24) |
| NBM | NBS P06 | 2% | 4% | 3% | 2% | 4% to 11% | 0.01 (24) |
| ENS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.04 (24) |
| AIFS_ENS | member fraction | 0% | 2% | 2% | 0% | 4% | 0.02 (24) |
| GEFS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.01 (24) |
| HRRRCAST | member fraction | — | — | — | — | 28% | — |
| REFS | member fraction | — | — | — | — | 0% | — |
| NBM_QMD | NBM QMD | 0% | 0% | 0% | 0% | 0% | 0.01 (20) |

For reference, always forecasting the period's observed frequency (4% of 6-h blocks wet) scores Brier 0.04.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; the ensembles have none). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles none. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-20 06Z | Mon 23:00 | 46.9 | 47.3 | 46.4 | 44.8 | 45.6 | 45.0 | 43.0 | 43.0 | 47.5 | 46.1 | 46.5 |
| 10-20 07Z | Tue 00:00 | 46.2 | 46.4 |  |  |  |  |  | 42.0 | 46.9 | 44.8 | 45.7 |
| 10-20 08Z | Tue 01:00 | 45.3 | 45.5 |  |  |  |  |  | 41.0 | 46.6 | 43.8 | 45.1 |
| 10-20 09Z | Tue 02:00 | 44.4 | 45.2 | 44.7 | 44.2 |  | 42.0 | 41.0 | 41.0 | 46.4 | 43.0 | 44.6 |
| 10-20 10Z | Tue 03:00 | 43.6 | 45.4 |  |  |  |  |  | 40.0 | 46.1 | 42.6 | 44.1 |
| 10-20 11Z | Tue 04:00 | 42.9 | 44.8 |  |  |  |  |  | 40.0 | 45.8 | 42.6 | 43.7 |
| 10-20 12Z | Tue 05:00 | 42.1 | 44.3 | 44.5 | 42.8 | 42.1 | 39.0 | 41.0 | 40.0 | 45.6 | 42.9 | 43.4 |
| 10-20 13Z | Tue 06:00 | 41.6 | 44.4 |  |  |  |  |  | 39.0 | 45.1 | 43.7 | 42.7 |
| 10-20 14Z | Tue 07:00 | 41.3 | 43.7 |  |  |  |  |  | 39.0 | 44.6 | 45.0 | 42.0 |
| 10-20 15Z | Tue 08:00 | 41.5 | 43.5 | 44.0 | 41.1 |  | 40.0 | 41.0 | 39.0 | 45.3 | 46.7 | 42.8 |
| 10-20 16Z | Tue 09:00 | 44.5 | 47.4 |  |  |  |  |  | 42.0 | 47.9 | 48.6 | 46.3 |
| 10-20 17Z | Tue 10:00 | 51.9 | 51.2 |  |  |  |  |  | 47.0 | 51.6 | 50.4 | 51.3 |
| 10-20 18Z | Tue 11:00 | 57.0 | 54.4 | 54.2 | 56.0 | 51.9 | 54.0 | 54.0 | 51.0 | 55.1 | 52.1 | 55.7 |
| 10-20 19Z | Tue 12:00 | 60.5 | 57.1 |  |  |  |  |  | 55.0 | 58.1 | 53.9 | 59.0 |
| 10-20 20Z | Tue 13:00 | 63.0 | 59.5 |  |  |  |  |  | 58.0 | 60.7 | 56.1 | 61.7 |
| 10-20 21Z | Tue 14:00 | 64.8 | 61.5 | 61.4 | 63.5 |  | 62.0 | 62.0 | 60.0 | 62.5 | 58.3 | 63.5 |
| 10-20 22Z | Tue 15:00 | 66.1 | 62.5 |  |  |  |  |  | 61.0 | 63.1 | 60.1 | 64.5 |
| 10-20 23Z | Tue 16:00 | 66.6 | 62.9 |  |  |  |  |  | 62.0 | 62.8 | 61.2 | 64.6 |
| 10-21 00Z | Tue 17:00 | 65.5 | 62.3 | 60.5 | 62.1 | 61.7 | 64.0 | 63.0 | 60.0 | 61.5 | 61.3 | 63.2 |
| 10-21 01Z | Tue 18:00 | 60.2 | 58.7 |  |  |  |  |  | 57.0 | 58.5 | 60.0 | 59.5 |
| 10-21 02Z | Tue 19:00 | 55.7 | 55.1 |  |  |  |  |  | 52.0 | 54.5 | 57.5 | 54.3 |
| 10-21 03Z | Tue 20:00 | 52.8 | 52.4 | 50.3 | 48.2 |  | 52.0 | 50.0 | 48.0 | 51.3 | 54.4 | 50.1 |
| 10-21 04Z | Tue 21:00 | 51.0 | 50.2 |  |  |  |  |  | 45.0 | 49.7 | 51.0 | 48.0 |
| 10-21 05Z | Tue 22:00 | 49.6 | 48.7 |  |  |  |  |  | 43.0 | 49.0 | 47.9 | 46.9 |
| 10-21 06Z | Tue 23:00 | 48.1 | 47.5 | 47.6 | 44.3 | 45.8 | 43.0 | 44.0 | 41.0 | 48.4 | 45.6 | 46.0 |

Dewpoint (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-20 06Z | Mon 23:00 | 44.7 | 41.4 | 41.4 | 40.5 | 42.0 | 39.0 | 41.0 | 40.0 |
| 10-20 07Z | Tue 00:00 | 44.5 | 44.0 |  |  |  |  |  | 40.0 |
| 10-20 08Z | Tue 01:00 | 43.9 | 43.6 |  |  |  |  |  | 40.0 |
| 10-20 09Z | Tue 02:00 | 43.1 | 43.9 | 41.0 | 41.6 |  | 38.0 | 41.0 | 40.0 |
| 10-20 10Z | Tue 03:00 | 42.5 | 44.1 |  |  |  |  |  | 40.0 |
| 10-20 11Z | Tue 04:00 | 41.6 | 43.8 |  |  |  |  |  | 39.0 |
| 10-20 12Z | Tue 05:00 | 40.8 | 43.4 | 43.0 | 41.2 | 39.1 | 36.0 | 41.0 | 39.0 |
| 10-20 13Z | Tue 06:00 | 40.4 | 43.4 |  |  |  |  |  | 39.0 |
| 10-20 14Z | Tue 07:00 | 40.1 | 43.1 |  |  |  |  |  | 38.0 |
| 10-20 15Z | Tue 08:00 | 40.1 | 43.2 | 42.6 | 40.0 |  | 37.0 | 41.0 | 38.0 |
| 10-20 16Z | Tue 09:00 | 42.4 | 45.3 |  |  |  |  |  | 41.0 |
| 10-20 17Z | Tue 10:00 | 44.6 | 46.2 |  |  |  |  |  | 43.0 |
| 10-20 18Z | Tue 11:00 | 44.4 | 46.4 | 46.6 | 42.2 | 41.1 | 42.0 | 46.0 | 45.0 |
| 10-20 19Z | Tue 12:00 | 44.1 | 46.3 |  |  |  |  |  | 45.0 |
| 10-20 20Z | Tue 13:00 | 43.8 | 45.5 |  |  |  |  |  | 44.0 |
| 10-20 21Z | Tue 14:00 | 42.9 | 43.3 | 46.5 | 40.8 |  | 40.0 | 45.0 | 44.0 |
| 10-20 22Z | Tue 15:00 | 41.1 | 42.3 |  |  |  |  |  | 43.0 |
| 10-20 23Z | Tue 16:00 | 39.6 | 42.4 |  |  |  |  |  | 43.0 |
| 10-21 00Z | Tue 17:00 | 39.3 | 42.3 | 45.2 | 40.4 | 42.4 | 40.0 | 43.0 | 42.0 |
| 10-21 01Z | Tue 18:00 | 40.3 | 41.8 |  |  |  |  |  | 42.0 |
| 10-21 02Z | Tue 19:00 | 41.2 | 41.8 |  |  |  |  |  | 42.0 |
| 10-21 03Z | Tue 20:00 | 41.6 | 42.0 | 43.4 | 39.5 |  | 40.0 | 42.0 | 40.0 |
| 10-21 04Z | Tue 21:00 | 41.7 | 42.3 |  |  |  |  |  | 39.0 |
| 10-21 05Z | Tue 22:00 | 42.0 | 41.6 |  |  |  |  |  | 39.0 |
| 10-21 06Z | Tue 23:00 | 42.4 | 41.6 | 42.0 | 37.9 | 40.9 | 38.0 | 41.0 | 38.0 |

Relative humidity (%), from each model's temperature and dewpoint:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-20 06Z | Mon 23:00 | 92 | 80 | 83 | 85 | 87 | 79 | 93 | 89 |
| 10-20 07Z | Tue 00:00 | 94 | 91 |  |  |  |  |  | 93 |
| 10-20 08Z | Tue 01:00 | 95 | 93 |  |  |  |  |  | 96 |
| 10-20 09Z | Tue 02:00 | 95 | 95 | 87 | 91 |  | 86 | 100 | 96 |
| 10-20 10Z | Tue 03:00 | 96 | 95 |  |  |  |  |  | 100 |
| 10-20 11Z | Tue 04:00 | 95 | 96 |  |  |  |  |  | 96 |
| 10-20 12Z | Tue 05:00 | 95 | 97 | 94 | 94 | 89 | 89 | 100 | 96 |
| 10-20 13Z | Tue 06:00 | 95 | 96 |  |  |  |  |  | 100 |
| 10-20 14Z | Tue 07:00 | 95 | 98 |  |  |  |  |  | 96 |
| 10-20 15Z | Tue 08:00 | 95 | 99 | 95 | 96 |  | 89 | 100 | 96 |
| 10-20 16Z | Tue 09:00 | 92 | 92 |  |  |  |  |  | 96 |
| 10-20 17Z | Tue 10:00 | 76 | 83 |  |  |  |  |  | 86 |
| 10-20 18Z | Tue 11:00 | 63 | 74 | 75 | 60 | 67 | 64 | 74 | 80 |
| 10-20 19Z | Tue 12:00 | 55 | 67 |  |  |  |  |  | 69 |
| 10-20 20Z | Tue 13:00 | 49 | 60 |  |  |  |  |  | 60 |
| 10-20 21Z | Tue 14:00 | 45 | 51 | 58 | 43 |  | 44 | 54 | 55 |
| 10-20 22Z | Tue 15:00 | 40 | 48 |  |  |  |  |  | 52 |
| 10-20 23Z | Tue 16:00 | 37 | 47 |  |  |  |  |  | 50 |
| 10-21 00Z | Tue 17:00 | 38 | 48 | 57 | 45 | 49 | 41 | 48 | 51 |
| 10-21 01Z | Tue 18:00 | 48 | 53 |  |  |  |  |  | 57 |
| 10-21 02Z | Tue 19:00 | 58 | 61 |  |  |  |  |  | 69 |
| 10-21 03Z | Tue 20:00 | 66 | 68 | 77 | 72 |  | 64 | 74 | 74 |
| 10-21 04Z | Tue 21:00 | 70 | 74 |  |  |  |  |  | 79 |
| 10-21 05Z | Tue 22:00 | 75 | 76 |  |  |  |  |  | 86 |
| 10-21 06Z | Tue 23:00 | 81 | 80 | 81 | 78 | 83 | 82 | 89 | 89 |

Wind speed (kt) at the hour:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-20 06Z | Mon 23:00 | 3.0 | 2.8 | 4.8 | 2.7 | 4.8 | 1.0 | 5.0 | 5.0 | 4.6 | 5.1 | 3.3 |
| 10-20 07Z | Tue 00:00 | 3.0 | 3.8 |  |  |  |  |  | 5.0 | 4.8 | 5.2 | 3.3 |
| 10-20 08Z | Tue 01:00 | 3.6 | 4.2 |  |  |  |  |  | 5.0 | 5.0 | 5.3 | 3.3 |
| 10-20 09Z | Tue 02:00 | 4.0 | 4.5 | 4.6 | 2.0 |  | 1.0 | 5.0 | 5.0 | 5.1 | 5.3 | 3.3 |
| 10-20 10Z | Tue 03:00 | 4.2 | 4.1 |  |  |  |  |  | 5.0 | 5.2 | 5.3 | 3.3 |
| 10-20 11Z | Tue 04:00 | 4.4 | 4.5 |  |  |  |  |  | 5.0 | 5.2 | 5.3 | 3.2 |
| 10-20 12Z | Tue 05:00 | 4.3 | 5.4 | 5.2 | 3.3 | 5.9 | 1.0 | 5.0 | 5.0 | 5.2 | 5.4 | 3.2 |
| 10-20 13Z | Tue 06:00 | 3.3 | 5.0 |  |  |  |  |  | 5.0 | 5.1 | 5.4 | 3.2 |
| 10-20 14Z | Tue 07:00 | 2.9 | 4.7 |  |  |  |  |  | 5.0 | 5.0 | 5.5 | 3.1 |
| 10-20 15Z | Tue 08:00 | 4.7 | 4.6 | 4.6 | 2.5 |  | 2.0 | 6.0 | 5.0 | 5.0 | 5.6 | 3.3 |
| 10-20 16Z | Tue 09:00 | 4.7 | 6.5 |  |  |  |  |  | 5.0 | 5.2 | 5.6 | 4.1 |
| 10-20 17Z | Tue 10:00 | 5.7 | 7.0 |  |  |  |  |  | 6.0 | 5.5 | 5.6 | 5.2 |
| 10-20 18Z | Tue 11:00 | 6.7 | 8.5 | 5.2 | 6.4 | 6.4 | 3.0 | 9.0 | 7.0 | 5.9 | 5.6 | 6.0 |
| 10-20 19Z | Tue 12:00 | 6.9 | 8.5 |  |  |  |  |  | 7.0 | 6.3 | 5.6 | 6.2 |
| 10-20 20Z | Tue 13:00 | 7.6 | 8.8 |  |  |  |  |  | 7.0 | 6.8 | 5.5 | 6.2 |
| 10-20 21Z | Tue 14:00 | 8.0 | 8.9 | 7.0 | 7.0 |  | 5.0 | 8.0 | 7.0 | 6.9 | 5.4 | 6.0 |
| 10-20 22Z | Tue 15:00 | 7.9 | 8.8 |  |  |  |  |  | 7.0 | 6.4 | 5.3 | 5.6 |
| 10-20 23Z | Tue 16:00 | 7.6 | 8.0 |  |  |  |  |  | 7.0 | 5.6 | 5.1 | 5.1 |
| 10-21 00Z | Tue 17:00 | 7.4 | 7.0 | 5.2 | 4.3 | 4.7 | 4.0 | 6.0 | 6.0 | 4.9 | 4.9 | 4.6 |
| 10-21 01Z | Tue 18:00 | 5.9 | 5.8 |  |  |  |  |  | 6.0 | 4.5 | 4.7 | 4.0 |
| 10-21 02Z | Tue 19:00 | 4.6 | 4.6 |  |  |  |  |  | 5.0 | 4.1 | 4.4 | 3.3 |
| 10-21 03Z | Tue 20:00 | 4.5 | 4.0 | 3.7 | 3.4 |  | 2.0 | 3.0 | 5.0 | 3.8 | 4.1 | 2.9 |
| 10-21 04Z | Tue 21:00 | 4.0 | 2.3 |  |  |  |  |  | 4.0 | 3.3 | 3.8 | 2.7 |
| 10-21 05Z | Tue 22:00 | 3.6 | 3.3 |  |  |  |  |  | 4.0 | 2.8 | 3.6 | 2.7 |
| 10-21 06Z | Tue 23:00 | 2.9 | 1.3 | 2.5 | 3.2 | 3.1 | 1.0 | 0.0 | 4.0 | 2.4 | 3.4 | 2.7 |

Precipitation (in), accumulated since the start of the day (06Z): 0.00 in every model (HRRR, RRFS, IFS, GFS, AIFS, USL, ENS, AIFS_ENS, GEFS) all day.

Total cloud cover (%):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-20 06Z | Mon 23:00 | 100 | 100 | 95 | 54 | 86 | 19 | 66 | 92 |
| 10-20 07Z | Tue 00:00 | 100 | 100 |  |  |  |  |  | 93 |
| 10-20 08Z | Tue 01:00 | 100 | 97 |  |  |  |  |  | 91 |
| 10-20 09Z | Tue 02:00 | 100 | 99 | 70 | 24 |  | 44 | 52 | 90 |
| 10-20 10Z | Tue 03:00 | 100 | 95 |  |  |  |  |  | 91 |
| 10-20 11Z | Tue 04:00 | 100 | 98 |  |  |  |  |  | 91 |
| 10-20 12Z | Tue 05:00 | 45 | 33 | 94 | 100 | 55 | 100 | 67 | 90 |
| 10-20 13Z | Tue 06:00 | 100 | 11 |  |  |  |  |  | 77 |
| 10-20 14Z | Tue 07:00 | 100 | 5 |  |  |  |  |  | 55 |
| 10-20 15Z | Tue 08:00 | 100 | 19 | 72 | 32 |  | 100 | 40 | 39 |
| 10-20 16Z | Tue 09:00 | 98 | 12 |  |  |  |  |  | 33 |
| 10-20 17Z | Tue 10:00 | 72 | 17 |  |  |  |  |  | 27 |
| 10-20 18Z | Tue 11:00 | 41 | 11 | 6 | 5 | 16 | 19 | 32 | 23 |
| 10-20 19Z | Tue 12:00 | 11 | 1 |  |  |  |  |  | 20 |
| 10-20 20Z | Tue 13:00 | 1 | 0 |  |  |  |  |  | 16 |
| 10-20 21Z | Tue 14:00 | 0 | 0 | 2 | 6 |  | 0 | 14 | 13 |
| 10-20 22Z | Tue 15:00 | 0 | 0 |  |  |  |  |  | 10 |
| 10-20 23Z | Tue 16:00 | 0 | 0 |  |  |  |  |  | 7 |
| 10-21 00Z | Tue 17:00 | 0 | 0 | 0 | 0 | 7 | 0 | 3 | 5 |
| 10-21 01Z | Tue 18:00 | 0 | 0 |  |  |  |  |  | 11 |
| 10-21 02Z | Tue 19:00 | 0 | 0 |  |  |  |  |  | 24 |
| 10-21 03Z | Tue 20:00 | 0 | 0 | 1 | 0 |  | 0 | 13 | 31 |
| 10-21 04Z | Tue 21:00 | 13 | 0 |  |  |  |  |  | 23 |
| 10-21 05Z | Tue 22:00 | 4 | 0 |  |  |  |  |  | 10 |
| 10-21 06Z | Tue 23:00 | 18 | 0 | 2 | 0 | 13 | 19 | 17 | 3 |

## Track record this period

Since 2026-09-28 at KOLM (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-13 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 21 | 5.8 | -0.6 | +1.6 | -1.0 | +0.01 | 1.9 | 3.0 | 1.9 | 0.01 |
| NBM | 21 | 6.6 | -0.1 | +2.3 | -3.4 | +0.00 | 1.4 | 3.4 | 3.7 | 0.01 |
| GFS_MOS | 21 | 7.1 | -0.3 | +1.5 | -4.1 | +0.01 | 2.3 | 2.7 | 4.3 | 0.01 |
| USL | 8 | 7.3 | -2.1 | +2.8 | -0.6 | +0.00 | 2.7 | 3.8 | 1.7 | 0.00 |
| HRRR | 21 | 9.3 | +0.6 | +4.9 | -2.8 | +0.00 | 2.6 | 5.4 | 3.1 | 0.01 |
| RRFS | 21 | 10.2 | -0.1 | +6.6 | -3.0 | +0.01 | 2.2 | 6.7 | 3.0 | 0.01 |
| AIFS | 21 | 10.6 | -1.9 | +5.6 | -4.7 | +0.01 | 2.7 | 6.0 | 4.9 | 0.01 |
| GFS | 21 | 10.7 | +0.0 | +5.0 | -4.8 | +0.01 | 2.9 | 5.6 | 4.9 | 0.01 |
| IFS | 21 | 11.2 | -2.3 | +6.7 | -4.2 | +0.01 | 2.6 | 6.8 | 4.3 | 0.01 |
| GEFS | 6 | 12.0 | -1.0 | +6.1 | -5.2 | +0.01 | 2.9 | 6.1 | 5.2 | 0.01 |
| AIFS_ENS | 6 | 12.0 | -1.8 | +6.9 | -3.9 | +0.01 | 3.1 | 6.9 | 3.9 | 0.01 |
| ENS | 5 | 13.9 | -1.4 | +8.9 | -4.2 | +0.01 | 2.5 | 8.9 | 4.2 | 0.01 |

## Daily verification (all 21 days this period)

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
| 10-18 | 10.0 | 10.5 | 16.0 | 12.5 | 15.0 | 10.5 | 6.5 | 7.5 | 17.0 | 15.5 | 12.0 | 5.5 | CONSENSUS |

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
| 10-18 | 61 | -1 | +0 | -3 | -1 | -2 | +0 | -1 | -2 | -2 | -2 | +0 | -1 |

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
| 10-18 | 31 | +8 | +9 | +11 | +9 | +10 | +7 | +4 | +5 | +13 | +11 | +9 | +4 |

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
| 10-18 | 11 | -2 | -3 | -4 | -5 | -6 | -7 | -3 | -1 | -4 | -5 | -6 | -1 |

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
| 10-18 | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 21 | +1 | 20 | +21 | 35 |
| RRFS | 21 | -9 | 28 | +10 | 30 |
| IFS | 21 | -3 | 21 | +11 | 26 |
| GFS | 21 | -4 | 31 | +10 | 26 |
| AIFS | 21 | -2 | 23 | +10 | 32 |
| GFS_MOS | 21 | -6 | 29 | +0 | 28 |
| NBM | 21 | -10 | 25 | +2 | 20 |
| USL | 8 | -13 | 19 | +4 | 18 |

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
| 10-18 | 22% | 5% | -20 | -20 | -17 | -20 | -2 | -14 | -7 | -9 |

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
| 10-18 | 40% | 60% | +51 | +22 | +31 | +31 | +29 | -26 | +15 | -1 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles have no dewpoint; USL only from when it started for this city). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 21 | +0.7 | 2.9 | -2.7 | 2.7 |
| RRFS | 21 | +3.2 | 4.0 | -1.2 | 1.4 |
| IFS | 21 | +1.9 | 2.7 | +0.3 | 1.0 |
| GFS | 21 | +1.0 | 2.7 | -2.5 | 2.7 |
| AIFS | 21 | +0.7 | 2.1 | -0.5 | 1.5 |
| GFS_MOS | 21 | -0.3 | 2.1 | -0.8 | 2.3 |
| NBM | 21 | +1.1 | 2.1 | +0.3 | 1.5 |
| USL | 8 | +0.8 | 1.5 | +0.5 | 1.7 |

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
| 10-18 | 36.5 | +3.3 | +4.6 | +5.4 | +4.6 | +3.8 | +3.2 | +3.7 | +2.1 |

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
| 10-18 | 41.9 | -4.0 | -1.4 | +0.6 | -3.2 | -1.8 | -2.8 | -1.2 | -1.3 |

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-13 | 0.00" (dry) | 2/7/9/3 | 7/9/6/3 | 0/2/2/16 | 2/0/0/2 | 0/0/0/10 | 24h 22% | 24h 7% | 0/0/0/0 |
| 10-14 | 0.00" (dry) | 9/20/1/2 | 10/11/3/0 | 6/39/8/0 | 33/26/2/0 | 3/29/0/0 | 24h 0% | 24h 7% | 0/9/0/0 |
| 10-15 | 0.00" (dry) | 0/0/1/1 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 24h 28% | 24h 0% | 0/0/0/0 |
| 10-16 | 0.00" (dry) | 0/2/1/5 | 0/1/1/1 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 24h 11% | 24h 0% | 0/0/0/0 |
| 10-17 | 0.01" (wet: 06-12) | 65/50/2/1 | 58/26/0/0 | 98/84/0/0 | 72/33/4/2 | 100/36/0/0 | 24h 28% | 24h 64% | 66/14/0/9 |
| 10-18 | 0.00" (dry) | 2/2/1/1 | 0/0/0/1 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 24h 28% | 24h 0% | 24h 0% |

## Today so far (2026-10-19, through 2026-10-19T19:54Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 61.0 °F, low 35.6 °F, max wind 4 kt, precip 0.00" (14 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 18/18Z | +1.6 | 1.9 | 63 (+2) pending | 44 (+9) | +2.1 | 0.00 | +0.00 |
| RRFS | 18/18Z | +3.6 | 3.7 | 63 (+2) pending | 46 (+11) | +2.4 | 0.00 | +0.00 |
| IFS | 18/12Z | +2.0 | 2.3 | 61 (+0) | 42 (+7) | +1.0 | 0.00 | +0.00 |
| GFS | 18/12Z | +2.0 | 2.2 | 62 (+1) pending | 43 (+7) | +0.6 | 0.00 | +0.00 |
| AIFS | 18/12Z | +0.6 | 3.5 | 60 (-1) | 43 (+7) | +0.9 | 0.00 | +0.00 |
| GFS_MOS | 18/12Z | -2.6 | 3.3 | 62 (+1) pending | 35 (-1) | +0.8 | — | — |
| NBM | 18/18Z | -2.3 | 2.8 | 61 (+0) pending | 35 (-1) | -0.5 | — | — |
| USL | 18/12Z | -1.9 | 2.7 | 60 (-1) | 40 (+4) | +2.5 | 0.00 | +0.00 |
| ENS | 18/06Z | +2.7 | 3.1 | 60 (-1) | 45 (+10) | +1.0 | 0.00 | +0.00 |
| AIFS_ENS | 18/12Z | +2.0 | 3.3 | 61 (+0) | 44 (+8) | +1.3 | 0.00 | +0.00 |
| GEFS | 18/12Z | +1.4 | 1.7 | 62 (+1) pending | 42 (+6) | +0.6 | 0.00 | +0.00 |

## Clouds so far today (2026-10-19, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (PDT) | GOES | METAR | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-19 06Z | Sun 23:00 | 100 |  | 100 | 100 | 100 | 100 | 100 | 100 | 91 | 100 |
| 10-19 07Z | Mon 00:00 | 100 | 0 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 08Z | Mon 01:00 | 100 | 19 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 09Z | Mon 02:00 | 100 | 0 | 100 | 100 | 100 | 100 |  | 100 | 93 | 99 |
| 10-19 10Z | Mon 03:00 | 100 | 19 | 100 | 100 |  |  |  |  |  | 94 |
| 10-19 11Z | Mon 04:00 | 100 | 75 | 100 | 100 |  |  |  |  |  | 84 |
| 10-19 12Z | Mon 05:00 | 100 | 0 | 100 | 100 | 100 | 100 | 93 | 100 | 93 | 79 |
| 10-19 13Z | Mon 06:00 | 28 | 0 | 100 | 100 |  |  |  |  |  | 83 |
| 10-19 14Z | Mon 07:00 | 91 | 0 | 100 | 100 |  |  |  |  |  | 92 |
| 10-19 15Z | Mon 08:00 | 88 | 100 | 100 | 100 | 96 | 100 |  | 100 | 88 | 98 |
| 10-19 16Z | Mon 09:00 | 1 | 0 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 17Z | Mon 10:00 | 0 | 0 | 100 | 100 |  |  |  |  |  | 100 |
| 10-19 18Z | Mon 11:00 | 0 | 0 | 100 | 100 | 17 | 100 | 58 | 100 | 84 | 100 |
| 10-19 19Z | Mon 12:00 | 0 | 0 | 100 | 100 |  |  |  |  |  | 92 |
| 10-19 20Z | Mon 13:00 | 7 | 0 | 100 | 100 |  |  |  |  |  | 81 |

## Dewpoint so far today (2026-10-19, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (PDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-19 07Z | Mon 00:00 | 41.0 | 89 | 41.2 | 45.2 |  |  |  |  |  | 40.0 |
| 10-19 08Z | Mon 01:00 | 41.0 | 86 | 41.2 | 45.2 |  |  |  |  |  | 40.0 |
| 10-19 09Z | Mon 02:00 | 41.0 | 86 | 41.2 | 45.4 | 42.4 | 40.5 |  | 37.0 | 40.0 | 40.0 |
| 10-19 10Z | Mon 03:00 | 42.1 | 90 | 41.3 | 45.7 |  |  |  |  |  | 40.0 |
| 10-19 11Z | Mon 04:00 | 42.1 | 90 | 41.4 | 45.8 |  |  |  |  |  | 39.0 |
| 10-19 12Z | Mon 05:00 | 42.1 | 90 | 41.9 | 45.7 | 43.2 | 40.6 | 38.4 | 37.0 | 40.0 | 39.0 |
| 10-19 13Z | Mon 06:00 | 39.9 | 96 | 42.1 | 45.7 |  |  |  |  |  | 39.0 |
| 10-19 14Z | Mon 07:00 | 37.0 | 97 | 41.6 | 45.3 |  |  |  |  |  | 39.0 |
| 10-19 15Z | Mon 08:00 | 36.0 | 100 | 41.2 | 45.0 | 41.7 | 39.5 |  | 38.0 | 39.0 | 40.0 |
| 10-19 16Z | Mon 09:00 | 41.0 | 93 | 41.1 | 43.3 |  |  |  |  |  | 41.0 |
| 10-19 17Z | Mon 10:00 | 43.0 | 83 | 41.3 | 42.8 |  |  |  |  |  | 43.0 |
| 10-19 18Z | Mon 11:00 | 44.1 | 69 | 41.0 | 44.6 | 42.8 | 39.9 | 42.2 | 42.0 | 44.0 | 44.0 |
| 10-19 19Z | Mon 12:00 | 44.1 | 62 | 40.5 | 44.0 |  |  |  |  |  | 44.0 |
| 10-19 20Z | Mon 13:00 | 44.1 | 54 | 37.9 | 43.2 |  |  |  |  |  | 44.0 |
| Bias so far |  |  |  | -0.3 | +3.5 | +1.7 | -0.7 | -2.8 | -2.3 | -0.1 | -0.5 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (SEW): https://forecast.weather.gov/product.php?site=SEW&issuedby=SEW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
