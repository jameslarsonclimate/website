# WxChallenge forecast brief: Olympia, WA (KOLM)

- Station: **KOLM**
- Target day: **2026-10-17**, scored over 2026-10-17T06Z to 2026-10-18T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-17T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-16T22:48:08+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 16/18Z | 61.0 | 49.8 | 8.6 | 0.06 |
| RRFS | 16/18Z | 63.8 | 47.9 | 7.9 | 0.06 |
| IFS | 16/12Z | 61.4 | 46.0 | 7.2 | 0.04 |
| GFS | 16/12Z | 63.7 | 44.9 | 6.8 | 0.03 |
| AIFS | 16/12Z | 61.0 | 46.6 | 7.6 | 0.05 |
| GFS_MOS | 16/18Z | 67.0 | 43.0 | 8.0 | 0.10 |
| NBM | 16/18Z | 64.0 | 44.0 | 9.0 | 0.02 |
| USL | 16/22Z | 63.0 | 43.0 | 13.0 | 0.04 |
| ENS | 16/00Z | 63.3 | 48.1 | 8.0 | 0.07 |
| AIFS_ENS | 16/12Z | 61.7 | 47.7 | 8.4 | 0.05 |
| GEFS | 16/12Z | 64.3 | 44.6 | 7.0 | 0.08 |
| HRRRCAST (precip only) | 16/06Z | — | — | — | 0.00 |
| REFS (precip only) | 16/18Z | — | — | — | 0.04 |
| NBM_QMD (precip only) | 16/12Z | — | — | — | 0.04 |
| **CONSENSUS** |  | **62.8** | **42.1** | **11.3** | **0.05** |

Notes:
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [1, 1, 0, 0] -> midpoints
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

- High °F weights: NBM 0.16, ENS 0.12, AIFS 0.10, USL 0.10, IFS 0.09, AIFS_ENS 0.09, GFS_MOS 0.09, RRFS 0.09, HRRR 0.08, GFS 0.07
- Low °F weights: GFS_MOS 0.17, NBM 0.14, USL 0.11, HRRR 0.10, GFS 0.09, AIFS 0.09, AIFS_ENS 0.09, IFS 0.07, RRFS 0.07, ENS 0.07
- Wind kt weights: USL 0.22, RRFS 0.11, HRRR 0.10, AIFS_ENS 0.10, NBM 0.09, GFS_MOS 0.09, ENS 0.08, IFS 0.08, GFS 0.07, AIFS 0.07
- Precip in weights: USL 0.10, HRRR 0.10, RRFS 0.10, GFS 0.10, GFS_MOS 0.10, NBM 0.10, ENS 0.10, AIFS_ENS 0.10, IFS 0.10, AIFS 0.10

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 62.6 | 63.0 | 63.3 | 63.7 | 64.1 | 63.3 |
| ENS | 51 | Low °F | 46.4 | 46.7 | 48.0 | 49.4 | 49.8 | 48.1 |
| ENS | 51 | Wind kt | 6.7 | 7.5 | 7.8 | 8.4 | 9.0 | 8.0 |
| ENS | 51 | Precip in | 0.02 | 0.05 | 0.06 | 0.08 | 0.12 | 0.07 |
| AIFS_ENS | 51 | High °F | 60.1 | 61.1 | 61.6 | 62.4 | 63.0 | 61.7 |
| AIFS_ENS | 51 | Low °F | 45.7 | 46.4 | 47.5 | 49.1 | 50.0 | 47.7 |
| AIFS_ENS | 51 | Wind kt | 6.9 | 7.5 | 8.2 | 9.0 | 10.2 | 8.4 |
| AIFS_ENS | 51 | Precip in | 0.00 | 0.02 | 0.05 | 0.07 | 0.12 | 0.05 |
| GEFS | 31 | High °F | 62.3 | 63.4 | 64.5 | 65.2 | 65.8 | 64.3 |
| GEFS | 31 | Low °F | 43.5 | 43.9 | 44.8 | 45.3 | 45.7 | 44.6 |
| GEFS | 31 | Wind kt | 6.5 | 6.6 | 6.8 | 7.3 | 7.7 | 7.0 |
| GEFS | 31 | Precip in | 0.04 | 0.05 | 0.07 | 0.10 | 0.11 | 0.08 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.01 | 0.04 | 0.06 | 0.09 | 0.04 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 18% | 0% | 0% |
| AIFS_ENS | 78% | 12% | 0% | 0% |
| GEFS | 100% | 13% | 0% | 0% |
| HRRRCAST | 28% | 0% | 0% | 0% |
| REFS | 64% | 14% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.04", p75 0.19", p90 0.27"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 65% | 50% | 2% | 1% | 65% to 83% | 0.01 (12) |
| NBM | NBS P06 | 58% | 26% | 0% | 0% | 58% to 69% | 0.00 (12) |
| ENS | member fraction | 98% | 84% | 0% | 0% | 100% | 0.02 (12) |
| AIFS_ENS | member fraction | 72% | 33% | 4% | 2% | 78% | 0.01 (12) |
| GEFS | member fraction | 100% | 55% | 0% | 0% | 100% | 0.01 (12) |
| HRRRCAST | member fraction | — | — | — | — | 28% | — |
| REFS | member fraction | — | — | — | — | 64% | — |
| NBM_QMD | NBM QMD | 66% | 14% | 0% | 9% | 69% | 0.00 (12) |

For reference, always forecasting the period's observed frequency (0% of 6-h blocks wet) scores Brier 0.00.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; the ensembles have none). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles none. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 53.9 | 55.3 | 53.8 | 53.3 | 52.8 | 55.0 | 53.0 | 52.0 | 54.8 | 54.5 | 53.7 |
| 10-17 07Z | Sat 00:00 | 53.4 | 54.8 |  |  |  |  |  | 52.0 | 54.6 | 53.7 | 53.6 |
| 10-17 08Z | Sat 01:00 | 53.0 | 55.2 |  |  |  |  |  | 53.0 | 54.8 | 53.7 | 54.0 |
| 10-17 09Z | Sat 02:00 | 54.9 | 56.4 | 53.6 | 54.8 |  | 54.0 | 53.0 | 54.0 | 55.1 | 54.3 | 54.5 |
| 10-17 10Z | Sat 03:00 | 54.9 | 56.7 |  |  |  |  |  | 54.0 | 55.5 | 55.2 | 55.1 |
| 10-17 11Z | Sat 04:00 | 55.1 | 56.3 |  |  |  |  |  | 55.0 | 56.0 | 56.2 | 55.7 |
| 10-17 12Z | Sat 05:00 | 55.1 | 56.4 | 54.3 | 56.0 | 55.1 | 53.0 | 55.0 | 55.0 | 56.2 | 56.8 | 55.8 |
| 10-17 13Z | Sat 06:00 | 53.2 | 56.2 |  |  |  |  |  | 54.0 | 55.7 | 57.3 | 54.8 |
| 10-17 14Z | Sat 07:00 | 50.8 | 55.0 |  |  |  |  |  | 53.0 | 54.9 | 57.8 | 53.3 |
| 10-17 15Z | Sat 08:00 | 49.8 | 54.1 | 53.7 | 53.0 |  | 52.0 | 54.0 | 53.0 | 54.7 | 58.4 | 52.7 |
| 10-17 16Z | Sat 09:00 | 52.4 | 56.1 |  |  |  |  |  | 54.0 | 55.7 | 58.9 | 53.8 |
| 10-17 17Z | Sat 10:00 | 54.2 | 57.8 |  |  |  |  |  | 56.0 | 57.3 | 59.4 | 55.8 |
| 10-17 18Z | Sat 11:00 | 57.2 | 59.5 | 57.8 | 57.2 | 58.7 | 60.0 | 57.0 | 57.0 | 58.8 | 59.7 | 57.9 |
| 10-17 19Z | Sat 12:00 | 58.9 | 61.2 |  |  |  |  |  | 59.0 | 60.6 | 60.2 | 60.2 |
| 10-17 20Z | Sat 13:00 | 60.4 | 62.6 |  |  |  |  |  | 61.0 | 62.3 | 60.8 | 62.6 |
| 10-17 21Z | Sat 14:00 | 61.0 | 63.5 | 61.4 | 63.3 |  | 65.0 | 62.0 | 61.0 | 63.3 | 61.3 | 64.0 |
| 10-17 22Z | Sat 15:00 | 61.0 | 63.8 |  |  |  |  |  | 62.0 | 63.2 | 61.5 | 64.3 |
| 10-17 23Z | Sat 16:00 | 60.2 | 63.2 |  |  |  |  |  | 61.0 | 62.4 | 61.4 | 63.6 |
| 10-18 00Z | Sat 17:00 | 59.4 | 61.0 | 58.5 | 60.6 | 61.0 | 63.0 | 62.0 | 60.0 | 60.8 | 60.8 | 61.8 |
| 10-18 01Z | Sat 18:00 | 56.8 | 58.9 |  |  |  |  |  | 57.0 | 58.0 | 59.3 | 58.1 |
| 10-18 02Z | Sat 19:00 | 54.6 | 55.1 |  |  |  |  |  | 53.0 | 54.5 | 57.1 | 53.4 |
| 10-18 03Z | Sat 20:00 | 53.5 | 52.8 | 50.0 | 47.9 |  | 51.0 | 50.0 | 49.0 | 51.6 | 54.6 | 49.5 |
| 10-18 04Z | Sat 21:00 | 52.4 | 50.9 |  |  |  |  |  | 46.0 | 49.9 | 52.0 | 47.2 |
| 10-18 05Z | Sat 22:00 | 52.2 | 49.2 |  |  |  |  |  | 45.0 | 48.9 | 49.6 | 45.8 |
| 10-18 06Z | Sat 23:00 | 50.2 | 47.9 | 46.2 | 46.3 | 46.6 | 43.0 | 44.0 | 44.0 | 48.1 | 47.7 | 44.6 |

Dewpoint (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 52.7 | 52.3 | 53.0 | 51.6 | 49.8 | 48.0 | 51.0 | 51.0 |
| 10-17 07Z | Sat 00:00 | 52.5 | 54.1 |  |  |  |  |  | 51.0 |
| 10-17 08Z | Sat 01:00 | 52.2 | 54.5 |  |  |  |  |  | 52.0 |
| 10-17 09Z | Sat 02:00 | 53.1 | 55.1 | 53.0 | 52.0 |  | 48.0 | 51.0 | 52.0 |
| 10-17 10Z | Sat 03:00 | 53.4 | 54.7 |  |  |  |  |  | 52.0 |
| 10-17 11Z | Sat 04:00 | 53.8 | 54.6 |  |  |  |  |  | 53.0 |
| 10-17 12Z | Sat 05:00 | 53.4 | 51.5 | 53.7 | 53.4 | 52.8 | 48.0 | 54.0 | 53.0 |
| 10-17 13Z | Sat 06:00 | 51.2 | 53.0 |  |  |  |  |  | 53.0 |
| 10-17 14Z | Sat 07:00 | 49.1 | 52.0 |  |  |  |  |  | 52.0 |
| 10-17 15Z | Sat 08:00 | 48.4 | 49.9 | 52.8 | 49.8 |  | 49.0 | 54.0 | 51.0 |
| 10-17 16Z | Sat 09:00 | 48.5 | 48.7 |  |  |  |  |  | 51.0 |
| 10-17 17Z | Sat 10:00 | 46.8 | 46.3 |  |  |  |  |  | 51.0 |
| 10-17 18Z | Sat 11:00 | 45.7 | 44.0 | 49.3 | 44.3 | 46.7 | 49.0 | 50.0 | 50.0 |
| 10-17 19Z | Sat 12:00 | 43.7 | 41.1 |  |  |  |  |  | 48.0 |
| 10-17 20Z | Sat 13:00 | 41.5 | 38.8 |  |  |  |  |  | 46.0 |
| 10-17 21Z | Sat 14:00 | 40.8 | 39.5 | 43.2 | 38.2 |  | 45.0 | 42.0 | 44.0 |
| 10-17 22Z | Sat 15:00 | 40.5 | 39.7 |  |  |  |  |  | 44.0 |
| 10-17 23Z | Sat 16:00 | 40.0 | 41.4 |  |  |  |  |  | 44.0 |
| 10-18 00Z | Sat 17:00 | 40.5 | 46.9 | 44.5 | 41.6 | 40.6 | 42.0 | 43.0 | 44.0 |
| 10-18 01Z | Sat 18:00 | 41.9 | 43.2 |  |  |  |  |  | 44.0 |
| 10-18 02Z | Sat 19:00 | 45.5 | 43.4 |  |  |  |  |  | 44.0 |
| 10-18 03Z | Sat 20:00 | 46.4 | 44.4 | 45.3 | 42.5 |  | 41.0 | 44.0 | 44.0 |
| 10-18 04Z | Sat 21:00 | 45.8 | 44.3 |  |  |  |  |  | 43.0 |
| 10-18 05Z | Sat 22:00 | 47.6 | 44.4 |  |  |  |  |  | 42.0 |
| 10-18 06Z | Sat 23:00 | 46.8 | 44.4 | 44.2 | 41.4 | 42.5 | 39.0 | 42.0 | 41.0 |

Relative humidity (%), from each model's temperature and dewpoint:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 96 | 90 | 97 | 94 | 90 | 77 | 93 | 96 |
| 10-17 07Z | Sat 00:00 | 97 | 97 |  |  |  |  |  | 96 |
| 10-17 08Z | Sat 01:00 | 97 | 97 |  |  |  |  |  | 96 |
| 10-17 09Z | Sat 02:00 | 94 | 95 | 98 | 90 |  | 80 | 93 | 93 |
| 10-17 10Z | Sat 03:00 | 95 | 93 |  |  |  |  |  | 93 |
| 10-17 11Z | Sat 04:00 | 95 | 94 |  |  |  |  |  | 93 |
| 10-17 12Z | Sat 05:00 | 94 | 84 | 98 | 91 | 92 | 83 | 96 | 93 |
| 10-17 13Z | Sat 06:00 | 93 | 89 |  |  |  |  |  | 96 |
| 10-17 14Z | Sat 07:00 | 94 | 90 |  |  |  |  |  | 96 |
| 10-17 15Z | Sat 08:00 | 95 | 86 | 97 | 89 |  | 89 | 100 | 93 |
| 10-17 16Z | Sat 09:00 | 87 | 76 |  |  |  |  |  | 90 |
| 10-17 17Z | Sat 10:00 | 76 | 65 |  |  |  |  |  | 83 |
| 10-17 18Z | Sat 11:00 | 65 | 56 | 73 | 62 | 64 | 67 | 77 | 77 |
| 10-17 19Z | Sat 12:00 | 57 | 48 |  |  |  |  |  | 67 |
| 10-17 20Z | Sat 13:00 | 50 | 41 |  |  |  |  |  | 58 |
| 10-17 21Z | Sat 14:00 | 47 | 41 | 51 | 39 |  | 48 | 48 | 54 |
| 10-17 22Z | Sat 15:00 | 47 | 41 |  |  |  |  |  | 52 |
| 10-17 23Z | Sat 16:00 | 47 | 45 |  |  |  |  |  | 54 |
| 10-18 00Z | Sat 17:00 | 50 | 60 | 60 | 50 | 47 | 46 | 50 | 55 |
| 10-18 01Z | Sat 18:00 | 57 | 56 |  |  |  |  |  | 62 |
| 10-18 02Z | Sat 19:00 | 71 | 65 |  |  |  |  |  | 71 |
| 10-18 03Z | Sat 20:00 | 77 | 73 | 84 | 81 |  | 69 | 80 | 83 |
| 10-18 04Z | Sat 21:00 | 78 | 78 |  |  |  |  |  | 89 |
| 10-18 05Z | Sat 22:00 | 84 | 83 |  |  |  |  |  | 89 |
| 10-18 06Z | Sat 23:00 | 88 | 88 | 93 | 83 | 86 | 86 | 93 | 89 |

Wind speed (kt) at the hour:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 7.8 | 6.8 | 6.2 | 4.4 | 6.9 | 3.0 | 7.0 | 6.0 | 5.6 | 6.9 | 4.6 |
| 10-17 07Z | Sat 00:00 | 7.8 | 7.3 |  |  |  |  |  | 6.0 | 5.8 | 7.1 | 4.7 |
| 10-17 08Z | Sat 01:00 | 7.0 | 7.3 |  |  |  |  |  | 7.0 | 6.2 | 7.1 | 5.0 |
| 10-17 09Z | Sat 02:00 | 7.4 | 7.8 | 6.3 | 5.2 |  | 4.0 | 8.0 | 7.0 | 6.7 | 7.0 | 5.3 |
| 10-17 10Z | Sat 03:00 | 8.6 | 7.5 |  |  |  |  |  | 7.0 | 7.0 | 7.0 | 5.5 |
| 10-17 11Z | Sat 04:00 | 7.1 | 7.8 |  |  |  |  |  | 7.0 | 7.2 | 6.9 | 5.7 |
| 10-17 12Z | Sat 05:00 | 6.7 | 6.8 | 7.1 | 5.8 | 7.6 | 8.0 | 9.0 | 7.0 | 7.2 | 6.8 | 6.0 |
| 10-17 13Z | Sat 06:00 | 5.0 | 5.5 |  |  |  |  |  | 7.0 | 6.8 | 6.7 | 5.9 |
| 10-17 14Z | Sat 07:00 | 5.0 | 4.9 |  |  |  |  |  | 7.0 | 6.3 | 6.7 | 5.8 |
| 10-17 15Z | Sat 08:00 | 5.3 | 4.9 | 5.5 | 6.3 |  | 7.0 | 7.0 | 7.0 | 5.9 | 6.8 | 5.7 |
| 10-17 16Z | Sat 09:00 | 5.2 | 5.9 |  |  |  |  |  | 7.0 | 5.9 | 7.0 | 5.9 |
| 10-17 17Z | Sat 10:00 | 6.0 | 6.3 |  |  |  |  |  | 8.0 | 6.1 | 7.3 | 6.4 |
| 10-17 18Z | Sat 11:00 | 6.9 | 6.1 | 6.8 | 6.6 | 6.5 | 5.0 | 8.0 | 8.0 | 6.5 | 7.4 | 6.7 |
| 10-17 19Z | Sat 12:00 | 6.8 | 7.3 |  |  |  |  |  | 8.0 | 6.7 | 7.4 | 6.5 |
| 10-17 20Z | Sat 13:00 | 7.0 | 7.0 |  |  |  |  |  | 8.0 | 6.9 | 7.2 | 6.2 |
| 10-17 21Z | Sat 14:00 | 7.3 | 7.0 | 7.2 | 6.8 |  | 7.0 | 8.0 | 8.0 | 7.0 | 7.0 | 6.1 |
| 10-17 22Z | Sat 15:00 | 7.3 | 6.6 |  |  |  |  |  | 7.0 | 6.8 | 6.7 | 5.9 |
| 10-17 23Z | Sat 16:00 | 6.0 | 6.5 |  |  |  |  |  | 6.0 | 6.5 | 6.3 | 5.8 |
| 10-18 00Z | Sat 17:00 | 5.8 | 7.9 | 6.3 | 3.9 | 5.2 | 6.0 | 6.0 | 6.0 | 6.0 | 5.9 | 5.4 |
| 10-18 01Z | Sat 18:00 | 5.5 | 5.2 |  |  |  |  |  | 5.0 | 5.4 | 5.4 | 4.5 |
| 10-18 02Z | Sat 19:00 | 3.6 | 3.8 |  |  |  |  |  | 5.0 | 4.7 | 4.8 | 3.5 |
| 10-18 03Z | Sat 20:00 | 3.2 | 3.5 | 3.8 | 2.7 |  | 4.0 | 0.0 | 4.0 | 3.9 | 4.2 | 2.8 |
| 10-18 04Z | Sat 21:00 | 4.2 | 3.6 |  |  |  |  |  | 4.0 | 2.9 | 3.7 | 2.2 |
| 10-18 05Z | Sat 22:00 | 3.5 | 3.1 |  |  |  |  |  | 4.0 | 2.4 | 3.4 | 1.6 |
| 10-18 06Z | Sat 23:00 | 3.5 | 2.8 | 2.0 | 1.8 | 2.2 | 2.0 | 0.0 | 4.0 | 2.4 | 3.3 | 1.4 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-17 07Z | Sat 00:00 | 0.00 | 0.00 |  |  |  | 0.00 | 0.00 | 0.01 | 0.00 |
| 10-17 08Z | Sat 01:00 | 0.00 | 0.00 |  |  |  | 0.00 | 0.01 | 0.01 | 0.01 |
| 10-17 09Z | Sat 02:00 | 0.02 | 0.00 | 0.00 | 0.00 |  | 0.00 | 0.01 | 0.02 | 0.01 |
| 10-17 10Z | Sat 03:00 | 0.05 | 0.01 |  |  |  | 0.00 | 0.03 | 0.03 | 0.03 |
| 10-17 11Z | Sat 04:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.04 | 0.03 | 0.05 |
| 10-17 12Z | Sat 05:00 | 0.05 | 0.06 | 0.03 | 0.03 | 0.04 | 0.00 | 0.05 | 0.04 | 0.07 |
| 10-17 13Z | Sat 06:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.06 | 0.04 | 0.07 |
| 10-17 14Z | Sat 07:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.06 | 0.04 | 0.07 |
| 10-17 15Z | Sat 08:00 | 0.05 | 0.06 | 0.04 | 0.03 |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 16Z | Sat 09:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 17Z | Sat 10:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 18Z | Sat 11:00 | 0.05 | 0.06 | 0.04 | 0.03 | 0.05 | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 19Z | Sat 12:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 20Z | Sat 13:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 21Z | Sat 14:00 | 0.05 | 0.06 | 0.04 | 0.03 |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 22Z | Sat 15:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-17 23Z | Sat 16:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-18 00Z | Sat 17:00 | 0.05 | 0.06 | 0.04 | 0.03 | 0.05 | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-18 01Z | Sat 18:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-18 02Z | Sat 19:00 | 0.05 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-18 03Z | Sat 20:00 | 0.05 | 0.06 | 0.04 | 0.03 |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-18 04Z | Sat 21:00 | 0.06 | 0.06 |  |  |  | 0.00 | 0.07 | 0.05 | 0.07 |
| 10-18 05Z | Sat 22:00 | 0.06 | 0.06 |  |  |  | 0.00 | 0.07 | 0.06 | 0.07 |
| 10-18 06Z | Sat 23:00 | 0.06 | 0.06 | 0.04 | 0.03 | 0.05 | 0.00 | 0.07 | 0.06 | 0.07 |

Total cloud cover (%):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 84 | 100 | 98 | 100 | 94 | 44 | 40 | 27 |
| 10-17 07Z | Sat 00:00 | 82 | 100 |  |  |  |  |  | 50 |
| 10-17 08Z | Sat 01:00 | 100 | 100 |  |  |  |  |  | 80 |
| 10-17 09Z | Sat 02:00 | 100 | 100 | 100 | 100 |  | 100 | 92 | 97 |
| 10-17 10Z | Sat 03:00 | 100 | 99 |  |  |  |  |  | 100 |
| 10-17 11Z | Sat 04:00 | 100 | 100 |  |  |  |  |  | 100 |
| 10-17 12Z | Sat 05:00 | 100 | 100 | 100 | 100 | 99 | 100 | 97 | 97 |
| 10-17 13Z | Sat 06:00 | 100 | 100 |  |  |  |  |  | 91 |
| 10-17 14Z | Sat 07:00 | 100 | 100 |  |  |  |  |  | 86 |
| 10-17 15Z | Sat 08:00 | 100 | 100 | 44 | 22 |  | 100 | 91 | 80 |
| 10-17 16Z | Sat 09:00 | 100 | 25 |  |  |  |  |  | 72 |
| 10-17 17Z | Sat 10:00 | 97 | 5 |  |  |  |  |  | 60 |
| 10-17 18Z | Sat 11:00 | 2 | 10 | 42 | 94 | 43 | 75 | 26 | 48 |
| 10-17 19Z | Sat 12:00 | 0 | 7 |  |  |  |  |  | 42 |
| 10-17 20Z | Sat 13:00 | 1 | 72 |  |  |  |  |  | 42 |
| 10-17 21Z | Sat 14:00 | 20 | 2 | 98 | 23 |  | 19 | 22 | 41 |
| 10-17 22Z | Sat 15:00 | 24 | 7 |  |  |  |  |  | 38 |
| 10-17 23Z | Sat 16:00 | 93 | 6 |  |  |  |  |  | 37 |
| 10-18 00Z | Sat 17:00 | 90 | 11 | 98 | 3 | 94 | 19 | 41 | 36 |
| 10-18 01Z | Sat 18:00 | 40 | 7 |  |  |  |  |  | 37 |
| 10-18 02Z | Sat 19:00 | 64 | 2 |  |  |  |  |  | 39 |
| 10-18 03Z | Sat 20:00 | 100 | 3 | 19 | 19 |  | 0 | 27 | 41 |
| 10-18 04Z | Sat 21:00 | 100 | 2 |  |  |  |  |  | 42 |
| 10-18 05Z | Sat 22:00 | 100 | 19 |  |  |  |  |  | 41 |
| 10-18 06Z | Sat 23:00 | 55 | 1 | 1 | 47 | 13 | 19 | 28 | 38 |

## Track record this period

Since 2026-09-28 at KOLM (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-13 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 18 | 5.4 | +0.3 | +1.5 | -0.9 | +0.00 | 1.5 | 2.8 | 2.1 | 0.00 |
| NBM | 18 | 6.4 | +0.8 | +2.0 | -3.3 | +0.00 | 1.0 | 3.3 | 3.8 | 0.01 |
| GFS_MOS | 18 | 6.5 | +0.7 | +1.3 | -3.6 | +0.01 | 2.1 | 2.6 | 3.8 | 0.01 |
| USL | 5 | 6.6 | -1.0 | +3.4 | -0.4 | +0.00 | 1.9 | 4.2 | 1.2 | 0.00 |
| HRRR | 18 | 8.8 | +1.8 | +4.0 | -2.8 | +0.00 | 2.5 | 4.6 | 3.2 | 0.01 |
| AIFS_ENS | 3 | 9.3 | +0.8 | +5.5 | -3.3 | +0.01 | 2.1 | 5.5 | 3.3 | 0.01 |
| AIFS | 18 | 9.7 | -0.8 | +5.0 | -4.8 | +0.01 | 1.9 | 5.5 | 5.0 | 0.01 |
| RRFS | 18 | 10.0 | +0.6 | +6.5 | -2.7 | +0.01 | 2.2 | 6.6 | 2.8 | 0.01 |
| GFS | 18 | 10.2 | +1.2 | +4.5 | -4.6 | +0.01 | 2.8 | 5.1 | 4.7 | 0.01 |
| IFS | 18 | 10.6 | -1.6 | +6.2 | -4.1 | +0.01 | 2.0 | 6.4 | 4.2 | 0.01 |
| ENS | 2 | 11.2 | +1.6 | +7.5 | -4.0 | +0.01 | 1.6 | 7.5 | 4.0 | 0.01 |
| GEFS | 3 | 11.8 | +0.6 | +5.7 | -4.7 | +0.00 | 3.7 | 5.7 | 4.7 | 0.00 |

## Daily verification (all 18 days this period)

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

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 18 | +0 | 21 | +9 | 27 |
| RRFS | 18 | -9 | 26 | +2 | 29 |
| IFS | 18 | -4 | 22 | +1 | 21 |
| GFS | 18 | -8 | 35 | +1 | 22 |
| AIFS | 18 | -1 | 22 | -1 | 29 |
| GFS_MOS | 18 | -8 | 34 | -1 | 29 |
| NBM | 18 | -11 | 26 | -5 | 19 |
| USL | 5 | -17 | 17 | -13 | 13 |

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

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles have no dewpoint; USL only from when it started for this city). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 18 | +0.0 | 3.0 | -3.0 | 3.1 |
| RRFS | 18 | +2.8 | 4.0 | -1.1 | 1.3 |
| IFS | 18 | +1.5 | 2.6 | +0.1 | 1.0 |
| GFS | 18 | +0.3 | 2.6 | -2.4 | 2.6 |
| AIFS | 18 | +0.5 | 2.2 | -0.5 | 1.7 |
| GFS_MOS | 18 | -0.2 | 1.8 | -0.9 | 2.6 |
| NBM | 18 | +0.8 | 2.1 | +0.1 | 1.5 |
| USL | 5 | +0.6 | 1.7 | +0.4 | 1.9 |

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

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-13 | 0.00" (dry) | 2/7/9/3 | 7/9/6/3 | 0/2/2/16 | 2/0/0/2 | 0/0/0/10 | 24h 22% | 24h 7% | 0/0/0/0 |
| 10-14 | 0.00" (dry) | 9/20/1/2 | 10/11/3/0 | 6/39/8/0 | 33/26/2/0 | 3/29/0/0 | 24h 0% | 24h 7% | 0/9/0/0 |
| 10-15 | 0.00" (dry) | 0/0/1/1 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 0/0/0/0 | 24h 28% | 24h 0% | 0/0/0/0 |

## Today so far (2026-10-16, through 2026-10-16T21:54Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 78.1 °F, low 37.0 °F, max wind 5.0 kt, precip 0.00" (16 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 15/18Z | +6.5 | 6.6 | 77 (-1) | 47 (+10) | +3.0 | 0.00 | +0.00 |
| RRFS | 15/18Z | +7.6 | 7.8 | 76 (-2) | 46 (+9) | +2.4 | 0.00 | +0.00 |
| IFS | 15/12Z | +7.4 | 8.4 | 75 (-3) | 49 (+12) | +1.3 | 0.00 | +0.00 |
| GFS | 15/12Z | +7.1 | 8.0 | 74 (-4) | 48 (+11) | +1.0 | 0.00 | +0.00 |
| AIFS | 15/12Z | +5.0 | 9.5 | 70 (-8) | 47 (+10) | +0.4 | 0.00 | +0.00 |
| GFS_MOS | 15/12Z | -1.1 | 4.1 | 69 (-9) | 37 (+0) | -0.4 | — | — |
| NBM | 15/18Z | +3.7 | 5.9 | 75 (-3) | 43 (+6) | -0.5 | — | — |
| USL | 15/12Z | +1.7 | 3.7 | 74 (-4) | 40 (+3) | +1.9 | 0.00 | +0.00 |
| ENS | 15/06Z | +9.0 | 9.3 | 76 (-2) | 50 (+13) | +1.4 | 0.00 | +0.00 |
| AIFS_ENS | 15/12Z | +6.0 | 8.5 | 74 (-4) | 47 (+10) | +1.3 | 0.00 | +0.00 |
| GEFS | 15/12Z | +6.7 | 7.4 | 74 (-4) | 47 (+10) | +0.8 | 0.00 | +0.00 |

## Clouds so far today (2026-10-16, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (PDT) | GOES | METAR | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-16 06Z | Thu 23:00 | 0 | 0 | 100 | 20 | 30 | 87 | 10 | 19 | 11 | 45 |
| 10-16 07Z | Fri 00:00 | 0 | 0 | 100 | 20 |  |  |  |  |  | 42 |
| 10-16 08Z | Fri 01:00 | 0 | 100 | 100 | 3 |  |  |  |  |  | 39 |
| 10-16 09Z | Fri 02:00 | 13 | 100 | 100 | 2 | 77 | 86 |  | 44 | 40 | 38 |
| 10-16 10Z | Fri 03:00 | 17 | 100 | 97 | 6 |  |  |  |  |  | 38 |
| 10-16 11Z | Fri 04:00 | 40 | 100 | 100 | 22 |  |  |  |  |  | 41 |
| 10-16 12Z | Fri 05:00 | 18 | 100 | 100 | 100 | 92 | 100 | 33 | 100 | 47 | 42 |
| 10-16 13Z | Fri 06:00 | 15 | 100 | 7 | 100 |  |  |  |  |  | 41 |
| 10-16 14Z | Fri 07:00 | 10 | 100 | 26 | 28 |  |  |  |  |  | 40 |
| 10-16 15Z | Fri 08:00 | 0 | 100 | 84 | 100 | 36 | 100 |  | 100 | 57 | 40 |
| 10-16 16Z | Fri 09:00 | 98 | 100 | 100 | 92 |  |  |  |  |  | 43 |
| 10-16 17Z | Fri 10:00 | 99 | 19 | 100 | 100 |  |  |  |  |  | 49 |
| 10-16 18Z | Fri 11:00 | 100 | 0 | 100 | 100 | 62 | 100 | 66 | 19 | 47 | 56 |
| 10-16 19Z | Fri 12:00 | 55 | 0 | 98 | 100 |  |  |  |  |  | 69 |
| 10-16 20Z | Fri 13:00 | 80 | 0 | 92 | 100 |  |  |  |  |  | 86 |
| 10-16 21Z | Fri 14:00 | 7 | 0 | 95 | 100 | 27 | 100 |  | 0 | 66 | 97 |
| 10-16 22Z | Fri 15:00 | 0 | 0 | 100 | 100 |  |  |  |  |  | 86 |

## Dewpoint so far today (2026-10-16, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (PDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-16 06Z | Thu 23:00 | 44.1 | 97 | 47.6 | 49.7 | 46.5 | 46.6 | 44.4 | 42.0 | 47.0 | 46.0 |
| 10-16 07Z | Fri 00:00 | 44.1 | 100 | 46.6 | 49.4 |  |  |  |  |  | 45.0 |
| 10-16 08Z | Fri 01:00 | 42.1 | 100 | 46.3 | 49.1 |  |  |  |  |  | 44.0 |
| 10-16 09Z | Fri 02:00 | 39.9 | 100 | 45.8 | 48.6 | 43.3 | 46.0 |  | 40.0 | 44.0 | 43.0 |
| 10-16 10Z | Fri 03:00 | 39.9 | 100 | 45.3 | 48.0 |  |  |  |  |  | 42.0 |
| 10-16 11Z | Fri 04:00 | 39.9 | 100 | 44.9 | 47.1 |  |  |  |  |  | 41.0 |
| 10-16 12Z | Fri 05:00 | 39.0 | 100 | 44.2 | 47.0 | 41.9 | 44.8 | 40.2 | 39.0 | 41.0 | 41.0 |
| 10-16 13Z | Fri 06:00 | 39.9 | 100 | 43.4 | 45.4 |  |  |  |  |  | 40.0 |
| 10-16 14Z | Fri 07:00 | 39.0 | 100 | 42.3 | 45.6 |  |  |  |  |  | 39.0 |
| 10-16 15Z | Fri 08:00 | 39.0 | 100 | 41.8 | 43.7 | 41.6 | 39.7 |  | 40.0 | 39.0 | 39.0 |
| 10-16 16Z | Fri 09:00 | 42.1 | 97 | 43.1 | 44.2 |  |  |  |  |  | 41.0 |
| 10-16 17Z | Fri 10:00 | 48.0 | 100 | 47.8 | 41.0 |  |  |  |  |  | 44.0 |
| 10-16 18Z | Fri 11:00 | 48.9 | 83 | 46.8 | 38.7 | 43.5 | 37.0 | 42.9 | 45.0 | 45.0 | 45.0 |
| 10-16 19Z | Fri 12:00 | 45.0 | 47 | 42.6 | 38.8 |  |  |  |  |  | 45.0 |
| 10-16 20Z | Fri 13:00 | 46.0 | 39 | 38.4 | 38.3 |  |  |  |  |  | 45.0 |
| 10-16 21Z | Fri 14:00 | 43.0 | 32 | 38.1 | 38.1 | 42.4 | 38.4 |  | 45.0 | 45.0 | 45.0 |
| 10-16 22Z | Fri 15:00 | 43.0 | 29 | 42.6 | 40.5 |  |  |  |  |  | 46.0 |
| Bias so far |  |  |  | +1.5 | +1.8 | +0.9 | -0.2 | -1.5 | -0.5 | +1.2 | +0.5 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (SEW): https://forecast.weather.gov/product.php?site=SEW&issuedby=SEW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
