# WxChallenge forecast brief: Olympia, WA (KOLM)

- Station: **KOLM**
- Target day: **2026-10-15**, scored over 2026-10-15T06Z to 2026-10-16T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-15T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-14T21:48:09+00:00 (refreshed several times an hour while the forecast job runs)
- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)

## How to use this brief (for AI assistants)

1. Start from the **CONSENSUS** row. It is already bias-corrected and skill-weighted using this period's verification (method below).
2. Check the track-record table: a model with a large, consistent bias (|bias| close to its MAE) is reliably off in that direction. The consensus already removes most of that bias; lean further only if the last few days (daily verification tables) show the bias growing.
3. Use the ensemble percentiles for uncertainty. For **precip**, enter roughly the ensemble **median**, not the mean: points are charged per 0.01" of error, and charged most heavily near zero, so the median minimizes expected points. Check the chance-of-rain table: when the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.
4. Use "Today so far" (the day currently in progress, not the target day) to see which models are handling the current pattern; persistent errors there often carry into tomorrow.
5. Check the clouds section: when a model's low or high misses line up with its cloud misses (too clear at night -> low too cold, too cloudy at night -> low too warm; too clear by day -> high too warm, too cloudy by day -> high too cool), ask whether its cloud forecast for the target day has the same problem before trusting its temperatures.
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
| HRRR | 14/18Z | 77.7 | 44.1 | 4.4 | 0.00 |
| RRFS | 14/18Z | 73.6 | 47.5 | 5.0 | 0.00 |
| IFS | 14/12Z | 69.1 | 47.1 | 4.5 | 0.00 |
| GFS | 14/12Z | 73.1 | 45.7 | 4.0 | 0.00 |
| AIFS | 14/12Z | 70.5 | 46.2 | 4.9 | 0.00 |
| GFS_MOS | 14/12Z | 70.0 | 40.0 | 4.0 | 0.00 |
| NBM | 14/18Z | 70.0 | 44.0 | 6.0 | 0.00 |
| USL | 14/12Z | 70.0 | 43.0 | 8.0 | 0.00 |
| ENS | 14/06Z | 70.3 | 48.4 | 4.7 | 0.00 |
| AIFS_ENS | 14/06Z | 71.5 | 48.6 | 5.8 | 0.00 |
| GEFS | 14/12Z | 71.7 | 46.1 | 4.3 | 0.00 |
| HRRRCAST (precip only) | 14/06Z | — | — | — | 0.00 |
| REFS (precip only) | 14/18Z | — | — | — | 0.00 |
| NBM_QMD (precip only) | 14/12Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **71.9** | **41.4** | **7.8** | **0.00** |

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

- High °F weights: NBM 0.16, USL 0.12, RRFS 0.11, HRRR 0.10, AIFS 0.10, AIFS_ENS 0.10, GFS_MOS 0.09, IFS 0.08, ENS 0.08, GFS 0.07 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Low °F weights: GFS_MOS 0.15, NBM 0.13, USL 0.12, HRRR 0.10, GFS 0.09, AIFS 0.09, AIFS_ENS 0.09, IFS 0.08, ENS 0.08, RRFS 0.07 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Wind kt weights: USL 0.24, RRFS 0.12, HRRR 0.10, GFS_MOS 0.09, NBM 0.09, IFS 0.08, ENS 0.08, GFS 0.07, AIFS 0.07, AIFS_ENS 0.07 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Precip in weights: USL 0.10, HRRR 0.10, RRFS 0.10, GFS 0.10, AIFS 0.10, GFS_MOS 0.10, NBM 0.10, AIFS_ENS 0.10, IFS 0.10, ENS 0.10 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 68.8 | 69.5 | 70.5 | 71.0 | 71.5 | 70.3 |
| ENS | 51 | Low °F | 47.5 | 47.9 | 48.4 | 48.9 | 49.6 | 48.4 |
| ENS | 51 | Wind kt | 4.2 | 4.4 | 4.6 | 5.0 | 5.2 | 4.7 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| AIFS_ENS | 51 | High °F | 68.7 | 70.2 | 71.1 | 72.7 | 73.7 | 71.5 |
| AIFS_ENS | 51 | Low °F | 46.2 | 47.6 | 48.6 | 50.0 | 50.8 | 48.6 |
| AIFS_ENS | 51 | Wind kt | 4.6 | 5.0 | 5.8 | 6.6 | 7.2 | 5.8 |
| AIFS_ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| GEFS | 31 | High °F | 69.7 | 70.8 | 71.9 | 72.8 | 73.5 | 71.7 |
| GEFS | 31 | Low °F | 45.4 | 45.6 | 46.1 | 46.5 | 46.8 | 46.1 |
| GEFS | 31 | Wind kt | 3.9 | 4.1 | 4.3 | 4.5 | 4.8 | 4.3 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 0% | 0% | 0% | 0% |
| AIFS_ENS | 0% | 0% | 0% | 0% |
| GEFS | 0% | 0% | 0% | 0% |
| HRRRCAST | 28% | 0% | 0% | 0% |
| REFS | 0% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.00", p90 0.00"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 0% | 2% | 1% | 1% | 2% to 4% | 0.00 (4) |
| NBM | NBS P06 | 0% | 0% | 0% | 0% | 0% to 0% | 0.00 (4) |
| ENS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.01 (4) |
| AIFS_ENS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.00 (4) |
| GEFS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.00 (4) |
| HRRRCAST | member fraction | — | — | — | — | 28% | — |
| REFS | member fraction | — | — | — | — | 0% | — |
| NBM_QMD | NBM QMD | 0% | 0% | 0% | 0% | 0% | 0.00 (4) |

For reference, always forecasting the period's observed frequency (0% of 6-h blocks wet) scores Brier 0.00.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles none. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-15 06Z | Wed 23:00 | 52.4 | 52.4 | 50.9 | 49.1 | 51.6 | 50.0 | 50.0 | 50.0 | 52.1 | 52.8 | 51.3 |
| 10-15 07Z | Thu 00:00 | 51.1 | 51.2 |  |  |  |  |  | 48.0 | 51.1 | 51.4 | 50.3 |
| 10-15 08Z | Thu 01:00 | 49.9 | 50.5 |  |  |  |  |  | 47.0 | 50.4 | 50.3 | 49.6 |
| 10-15 09Z | Thu 02:00 | 49.0 | 49.7 | 48.0 | 47.1 |  | 46.0 | 47.0 | 46.0 | 49.8 | 49.4 | 48.9 |
| 10-15 10Z | Thu 03:00 | 48.1 | 48.5 |  |  |  |  |  | 45.0 | 49.4 | 48.9 | 48.3 |
| 10-15 11Z | Thu 04:00 | 47.1 | 48.0 |  |  |  |  |  | 45.0 | 49.1 | 48.7 | 47.8 |
| 10-15 12Z | Thu 05:00 | 45.4 | 47.8 | 47.2 | 46.2 | 46.2 | 44.0 | 46.0 | 45.0 | 49.0 | 48.9 | 47.5 |
| 10-15 13Z | Thu 06:00 | 44.6 | 48.3 |  |  |  |  |  | 44.0 | 48.8 | 49.7 | 46.7 |
| 10-15 14Z | Thu 07:00 | 44.1 | 49.4 |  |  |  |  |  | 43.0 | 48.6 | 50.9 | 46.1 |
| 10-15 15Z | Thu 08:00 | 45.9 | 50.3 | 49.2 | 46.1 |  | 43.0 | 46.0 | 44.0 | 49.5 | 52.4 | 46.9 |
| 10-15 16Z | Thu 09:00 | 49.0 | 50.9 |  |  |  |  |  | 47.0 | 51.9 | 54.2 | 50.1 |
| 10-15 17Z | Thu 10:00 | 52.5 | 52.3 |  |  |  |  |  | 52.0 | 55.2 | 56.1 | 54.7 |
| 10-15 18Z | Thu 11:00 | 59.6 | 57.2 | 56.1 | 60.6 | 56.6 | 55.0 | 55.0 | 55.0 | 58.7 | 58.0 | 59.2 |
| 10-15 19Z | Thu 12:00 | 66.7 | 62.5 |  |  |  |  |  | 60.0 | 62.3 | 60.4 | 63.4 |
| 10-15 20Z | Thu 13:00 | 71.7 | 67.2 |  |  |  |  |  | 63.0 | 66.1 | 63.3 | 67.4 |
| 10-15 21Z | Thu 14:00 | 75.0 | 70.5 | 66.7 | 71.5 |  | 66.0 | 67.0 | 66.0 | 68.8 | 66.4 | 70.2 |
| 10-15 22Z | Thu 15:00 | 77.1 | 72.5 |  |  |  |  |  | 68.0 | 70.1 | 69.1 | 71.6 |
| 10-15 23Z | Thu 16:00 | 77.7 | 73.6 |  |  |  |  |  | 69.0 | 70.3 | 71.0 | 71.7 |
| 10-16 00Z | Thu 17:00 | 76.8 | 72.9 | 68.0 | 70.9 | 70.5 | 69.0 | 69.0 | 68.0 | 69.3 | 71.5 | 70.3 |
| 10-16 01Z | Thu 18:00 | 71.2 | 68.4 |  |  |  |  |  | 65.0 | 66.5 | 70.2 | 66.4 |
| 10-16 02Z | Thu 19:00 | 66.0 | 63.7 |  |  |  |  |  | 60.0 | 62.4 | 67.5 | 60.8 |
| 10-16 03Z | Thu 20:00 | 63.0 | 61.2 | 57.4 | 56.9 |  | 55.0 | 57.0 | 56.0 | 58.9 | 64.0 | 56.5 |
| 10-16 04Z | Thu 21:00 | 60.3 | 59.8 |  |  |  |  |  | 53.0 | 56.8 | 60.1 | 54.6 |
| 10-16 05Z | Thu 22:00 | 58.5 | 58.4 |  |  |  |  |  | 51.0 | 55.3 | 56.6 | 53.8 |
| 10-16 06Z | Thu 23:00 | 56.9 | 56.9 | 53.1 | 52.1 | 53.7 | 45.0 | 51.0 | 49.0 | 54.1 | 53.9 | 53.0 |

Wind speed (kt) at the hour:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-15 06Z | Wed 23:00 | 4.0 | 2.4 | 3.2 | 3.3 | 4.9 | 1.0 | 4.0 | 5.0 | 3.9 | 5.1 | 2.8 |
| 10-15 07Z | Thu 00:00 | 3.6 | 2.4 |  |  |  |  |  | 5.0 | 4.0 | 5.2 | 3.0 |
| 10-15 08Z | Thu 01:00 | 3.4 | 3.3 |  |  |  |  |  | 4.0 | 4.2 | 5.2 | 3.1 |
| 10-15 09Z | Thu 02:00 | 3.2 | 2.3 | 3.1 | 3.0 |  | 1.0 | 4.0 | 4.0 | 4.3 | 5.2 | 3.2 |
| 10-15 10Z | Thu 03:00 | 3.3 | 1.2 |  |  |  |  |  | 5.0 | 4.2 | 5.1 | 3.2 |
| 10-15 11Z | Thu 04:00 | 3.2 | 1.7 |  |  |  |  |  | 5.0 | 4.0 | 5.0 | 3.2 |
| 10-15 12Z | Thu 05:00 | 1.5 | 1.0 | 4.0 | 3.1 | 4.4 | 1.0 | 3.0 | 5.0 | 3.9 | 4.9 | 3.2 |
| 10-15 13Z | Thu 06:00 | 0.8 | 2.3 |  |  |  |  |  | 5.0 | 3.9 | 4.8 | 3.2 |
| 10-15 14Z | Thu 07:00 | 1.0 | 2.8 |  |  |  |  |  | 5.0 | 3.9 | 4.6 | 3.2 |
| 10-15 15Z | Thu 08:00 | 1.8 | 3.6 | 3.9 | 3.2 |  | 1.0 | 5.0 | 4.0 | 4.0 | 4.4 | 3.4 |
| 10-15 16Z | Thu 09:00 | 2.2 | 2.9 |  |  |  |  |  | 5.0 | 3.8 | 4.2 | 3.6 |
| 10-15 17Z | Thu 10:00 | 3.0 | 3.0 |  |  |  |  |  | 5.0 | 3.7 | 4.0 | 4.0 |
| 10-15 18Z | Thu 11:00 | 3.0 | 2.9 | 3.4 | 4.0 | 4.2 | 2.0 | 6.0 | 5.0 | 3.6 | 3.9 | 4.2 |
| 10-15 19Z | Thu 12:00 | 2.6 | 3.7 |  |  |  |  |  | 5.0 | 3.8 | 3.9 | 4.2 |
| 10-15 20Z | Thu 13:00 | 2.3 | 3.4 |  |  |  |  |  | 6.0 | 4.2 | 3.9 | 4.1 |
| 10-15 21Z | Thu 14:00 | 2.3 | 3.6 | 4.5 | 3.9 |  | 4.0 | 5.0 | 6.0 | 4.4 | 4.0 | 4.0 |
| 10-15 22Z | Thu 15:00 | 3.2 | 4.2 |  |  |  |  |  | 6.0 | 4.1 | 4.1 | 3.8 |
| 10-15 23Z | Thu 16:00 | 3.9 | 5.0 |  |  |  |  |  | 5.0 | 3.6 | 4.1 | 3.5 |
| 10-16 00Z | Thu 17:00 | 4.4 | 5.0 | 3.1 | 3.1 | 3.9 | 3.0 | 3.0 | 5.0 | 3.1 | 4.1 | 3.2 |
| 10-16 01Z | Thu 18:00 | 4.2 | 3.8 |  |  |  |  |  | 5.0 | 2.9 | 3.9 | 2.6 |
| 10-16 02Z | Thu 19:00 | 4.4 | 3.6 |  |  |  |  |  | 4.0 | 2.8 | 3.6 | 2.1 |
| 10-16 03Z | Thu 20:00 | 3.4 | 1.8 | 2.5 | 2.3 |  | 2.0 | 0.0 | 3.0 | 2.8 | 3.3 | 1.8 |
| 10-16 04Z | Thu 21:00 | 3.0 | 2.3 |  |  |  |  |  | 3.0 | 2.7 | 3.1 | 1.8 |
| 10-16 05Z | Thu 22:00 | 2.3 | 2.9 |  |  |  |  |  | 3.0 | 2.7 | 2.9 | 2.1 |
| 10-16 06Z | Thu 23:00 | 1.4 | 2.2 | 3.5 | 1.9 | 2.6 | 1.0 | 0.0 | 3.0 | 2.8 | 2.9 | 2.4 |

Precipitation (in), accumulated since the start of the day (06Z): 0.00 in every model (HRRR, RRFS, IFS, GFS, AIFS, USL, ENS, AIFS_ENS, GEFS) all day.

Total cloud cover (%):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-15 06Z | Wed 23:00 | 0 | 0 | 0 | 0 | 2 | 0 | 4 | 1 |
| 10-15 07Z | Thu 00:00 | 1 | 5 |  |  |  |  |  | 0 |
| 10-15 08Z | Thu 01:00 | 7 | 13 |  |  |  |  |  | 0 |
| 10-15 09Z | Thu 02:00 | 19 | 28 | 2 | 5 |  | 0 | 20 | 0 |
| 10-15 10Z | Thu 03:00 | 100 | 43 |  |  |  |  |  | 0 |
| 10-15 11Z | Thu 04:00 | 100 | 61 |  |  |  |  |  | 1 |
| 10-15 12Z | Thu 05:00 | 100 | 68 | 72 | 9 | 57 | 0 | 55 | 2 |
| 10-15 13Z | Thu 06:00 | 100 | 71 |  |  |  |  |  | 6 |
| 10-15 14Z | Thu 07:00 | 100 | 79 |  |  |  |  |  | 11 |
| 10-15 15Z | Thu 08:00 | 100 | 86 | 100 | 17 |  | 19 | 66 | 15 |
| 10-15 16Z | Thu 09:00 | 100 | 85 |  |  |  |  |  | 14 |
| 10-15 17Z | Thu 10:00 | 88 | 58 |  |  |  |  |  | 10 |
| 10-15 18Z | Thu 11:00 | 38 | 18 | 44 | 5 | 22 | 19 | 41 | 8 |
| 10-15 19Z | Thu 12:00 | 6 | 6 |  |  |  |  |  | 12 |
| 10-15 20Z | Thu 13:00 | 90 | 32 |  |  |  |  |  | 18 |
| 10-15 21Z | Thu 14:00 | 45 | 0 | 4 | 86 |  | 0 | 6 | 23 |
| 10-15 22Z | Thu 15:00 | 0 | 0 |  |  |  |  |  | 24 |
| 10-15 23Z | Thu 16:00 | 0 | 0 |  |  |  |  |  | 22 |
| 10-16 00Z | Thu 17:00 | 2 | 0 | 8 | 100 | 2 | 0 | 5 | 23 |
| 10-16 01Z | Thu 18:00 | 34 | 0 |  |  |  |  |  | 30 |
| 10-16 02Z | Thu 19:00 | 66 | 0 |  |  |  |  |  | 41 |
| 10-16 03Z | Thu 20:00 | 63 | 0 | 39 | 100 |  | 0 | 9 | 47 |
| 10-16 04Z | Thu 21:00 | 72 | 0 |  |  |  |  |  | 47 |
| 10-16 05Z | Thu 22:00 | 95 | 0 |  |  |  |  |  | 46 |
| 10-16 06Z | Thu 23:00 | 35 | 0 | 9 | 59 | 25 | 0 | 12 | 44 |

## Track record this period

Since 2026-09-28 at KOLM (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-13 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| ENS | 1 | 4.5 | +0.0 | +3.0 | -3.0 | +0.00 | 0.0 | 3.0 | 3.0 | 0.00 |
| AIFS_ENS | 1 | 5.5 | -2.0 | +2.0 | -3.0 | +0.00 | 2.0 | 2.0 | 3.0 | 0.00 |
| CONSENSUS | 16 | 5.6 | -0.2 | +1.6 | -0.9 | +0.00 | 1.2 | 3.2 | 2.3 | 0.00 |
| USL | 3 | 5.8 | -1.4 | +2.5 | +0.4 | +0.00 | 1.4 | 3.9 | 1.0 | 0.00 |
| NBM | 16 | 6.4 | +0.6 | +1.8 | -3.3 | -0.01 | 0.8 | 3.4 | 3.8 | 0.01 |
| GFS_MOS | 16 | 6.5 | +0.3 | +1.6 | -3.2 | +0.01 | 2.0 | 2.9 | 3.5 | 0.01 |
| HRRR | 16 | 8.4 | +0.9 | +3.8 | -2.7 | -0.01 | 1.8 | 4.5 | 3.1 | 0.01 |
| RRFS | 16 | 9.4 | -0.5 | +6.3 | -2.6 | +0.01 | 1.6 | 6.4 | 2.7 | 0.01 |
| AIFS | 16 | 9.6 | -1.5 | +4.8 | -4.9 | +0.01 | 1.8 | 5.3 | 5.2 | 0.01 |
| GFS | 16 | 10.0 | +0.7 | +4.2 | -4.5 | +0.01 | 2.5 | 5.0 | 4.6 | 0.01 |
| GEFS | 1 | 10.5 | -5.0 | +4.0 | -3.0 | +0.00 | 5.0 | 4.0 | 3.0 | 0.00 |
| IFS | 16 | 10.6 | -2.2 | +6.0 | -4.0 | +0.01 | 2.3 | 6.3 | 4.1 | 0.01 |

## Daily verification (all 16 days this period)

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
| 10-13 | 2.0 | 7.4 | 7.0 | 10.5 | 5.0 | 3.5 | 3.5 | 5.5 | 4.5 | 5.5 | 10.5 | 4.5 | HRRR |

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
| 10-13 | 63 | +1 | -4 | -3 | -5 | -2 | -3 | +0 | -3 | +0 | -2 | -5 | -2 |

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
| 10-13 | 39 | +0 | +2 | +2 | +4 | +1 | +0 | -2 | -2 | +3 | +2 | +4 | -2 |

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
| 10-13 | 7 | -2 | -2 | -4 | -3 | -4 | -1 | -3 | +1 | -3 | -3 | -3 | +1 |

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
| 10-13 | 0.00 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 16 | +1 | 25 | +15 | 29 |
| RRFS | 16 | -5 | 25 | +12 | 27 |
| IFS | 16 | -1 | 23 | +7 | 20 |
| GFS | 16 | -1 | 35 | +5 | 23 |
| AIFS | 16 | +4 | 22 | +8 | 26 |
| GFS_MOS | 16 | -2 | 33 | +7 | 28 |
| NBM | 16 | -8 | 26 | +0 | 17 |
| USL | 3 | -17 | 17 | -8 | 8 |

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

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-13 | 0.00" (dry) | 2/7/9/3 | 7/9/6/3 | 0/2/2/16 | 2/0/0/2 | 0/0/0/10 | 24h 22% | 24h 7% | 0/0/0/0 |

## Today so far (2026-10-14, through 2026-10-14T20:54Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 64.9 °F, low 53.1 °F, max wind 8.0 kt, precip 0.00" (15 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 13/18Z | -3.1 | 3.1 | 66 (+1) pending | 50 (-4) | +0.8 | 0.00 | +0.00 |
| RRFS | 13/18Z | -1.2 | 2.3 | 69 (+4) pending | 51 (-2) | -0.4 | 0.00 | +0.00 |
| IFS | 13/12Z | -2.2 | 2.2 | 66 (+1) pending | 51 (-2) pending | -1.3 | 0.01 | +0.01 |
| GFS | 13/12Z | -3.2 | 3.2 | 64 (+0) | 49 (-4) pending | -1.8 | 0.00 | +0.00 |
| AIFS | 13/12Z | -3.7 | 3.7 | 66 (+1) pending | 50 (-4) | -2.8 | 0.02 | +0.02 |
| GFS_MOS | 13/18Z | -6.4 | 6.4 | 67 (+2) pending | 43 (-10) | -1.8 | — | — |
| NBM | 13/18Z | -5.1 | 5.1 | 66 (+1) pending | 46 (-7) | -1.2 | — | — |
| USL | 13/22Z | -5.0 | 5.0 | 63 (-2) | 48 (-5) pending | +0.3 | 0.00 | +0.00 |
| ENS | 13/06Z | -2.7 | 2.8 | 66 (+1) pending | 50 (-3) | -0.6 | 0.01 | +0.01 |
| AIFS_ENS | 13/12Z | -2.5 | 2.8 | 66 (+1) pending | 51 (-2) | -2.3 | 0.02 | +0.02 |
| GEFS | 13/18Z | -3.1 | 3.2 | 67 (+2) pending | 50 (-3) | -2.2 | 0.01 | +0.01 |

## Clouds so far today (2026-10-14, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (PDT) | GOES | METAR | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-14 06Z | Tue 23:00 | 100 |  | 100 | 88 | 100 | 82 | 89 | 100 | 84 | 92 |
| 10-14 07Z | Wed 00:00 | 100 | 100 | 100 | 67 |  |  |  |  |  | 91 |
| 10-14 08Z | Wed 01:00 | 100 | 100 | 100 | 36 |  |  |  |  |  | 91 |
| 10-14 09Z | Wed 02:00 | 100 | 100 | 87 | 49 | 100 | 100 |  | 100 | 83 | 91 |
| 10-14 10Z | Wed 03:00 | 100 | 100 | 96 | 81 |  |  |  |  |  | 89 |
| 10-14 11Z | Wed 04:00 | 100 | 100 | 100 | 100 |  |  |  |  |  | 87 |
| 10-14 12Z | Wed 05:00 | 100 | 100 | 100 | 100 | 100 | 72 | 92 | 100 | 89 | 86 |
| 10-14 13Z | Wed 06:00 | 100 | 100 | 100 | 78 |  |  |  |  |  | 87 |
| 10-14 14Z | Wed 07:00 | 100 | 100 | 100 | 57 |  |  |  |  |  | 89 |
| 10-14 15Z | Wed 08:00 | 18 | 100 | 100 | 64 | 100 | 100 |  | 100 | 90 | 91 |
| 10-14 16Z | Wed 09:00 | 70 | 100 | 100 | 53 |  |  |  |  |  | 90 |
| 10-14 17Z | Wed 10:00 | 97 | 100 | 97 | 52 |  |  |  |  |  | 87 |
| 10-14 18Z | Wed 11:00 | 99 | 100 | 47 | 100 | 86 | 79 | 58 | 100 | 88 | 86 |
| 10-14 19Z | Wed 12:00 | 100 | 100 | 63 | 57 |  |  |  |  |  | 90 |
| 10-14 20Z | Wed 13:00 | 98 | 100 | 100 | 56 |  |  |  |  |  | 95 |
| 10-14 21Z | Wed 14:00 | 100 | 100 | 100 | 52 | 77 | 100 |  | 100 | 67 | 98 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (SEW): https://forecast.weather.gov/product.php?site=SEW&issuedby=SEW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
