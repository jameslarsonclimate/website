# WxChallenge forecast brief: Minneapolis, MN (KMSP)

- Station: **KMSP**
- Target day: **2026-10-27**, scored over 2026-10-27T06Z to 2026-10-28T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-27T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-26T21:12:08+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 26/18Z | 53.3 | 44.4 | 11.1 | 0.25 |
| RRFS | 26/18Z | 55.1 | 43.8 | 11.1 | 0.12 |
| IFS | 26/12Z | 58.9 | 44.3 | 9.5 | 0.36 |
| IFS_HRES | 26/12Z | 59.0 | 45.1 | 9.7 | 0.47 |
| GFS | 26/12Z | 56.5 | 43.1 | 9.2 | 0.30 |
| AIFS | 26/12Z | 53.7 | 42.4 | 8.6 | 0.29 |
| GFS_MOS | 26/12Z | 57.0 | 41.0 | 11.0 | 0.42 |
| NBM | 26/20Z | 62.0 | 43.0 | 13.0 | 0.31 |
| USL | 26/12Z | 59.0 | 44.0 | 17.0 | 0.25 |
| ENS | 26/00Z | 60.5 | 45.0 | 11.6 | 0.32 |
| AIFS_ENS | 26/00Z | 53.3 | 42.9 | 10.7 | 0.26 |
| GEFS | 26/12Z | 57.7 | 43.5 | 11.4 | 0.38 |
| HRRRCAST (precip only) | 26/12Z | — | — | — | 0.21 |
| REFS (precip only) | 26/18Z | — | — | — | 0.19 |
| NBM_QMD (precip only) | 26/12Z | — | — | — | 0.48 |
| **CONSENSUS** |  | **57.5** | **43.8** | **15.3** | **0.29** |

Notes:
- IFS_HRES: not in the consensus
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [3, 1, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members (Open-Meteo)
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- HRRRCAST: median of 18 members (experimental AI model)
- REFS: median of 14 members, 18Z + 12Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: RRFS 0.16, HRRR 0.12, GFS 0.12, GFS_MOS 0.10, NBM 0.09, USL 0.09, AIFS 0.09, AIFS_ENS 0.09, IFS 0.07, ENS 0.07 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Low °F weights: NBM 0.15, IFS 0.14, ENS 0.14, AIFS 0.09, USL 0.09, AIFS_ENS 0.09, HRRR 0.09, GFS_MOS 0.08, RRFS 0.08, GFS 0.07 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Wind kt weights: GFS_MOS 0.13, NBM 0.13, HRRR 0.11, RRFS 0.10, GFS 0.09, USL 0.09, AIFS 0.09, AIFS_ENS 0.09, IFS 0.08, ENS 0.08 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Precip in weights: GFS_MOS 0.11, NBM 0.10, RRFS 0.10, AIFS 0.10, USL 0.10, AIFS_ENS 0.10, HRRR 0.10, GFS 0.10, IFS 0.10, ENS 0.10 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 58.1 | 58.9 | 60.9 | 61.8 | 62.8 | 60.5 |
| ENS | 51 | Low °F | 44.3 | 44.7 | 45.1 | 45.5 | 45.7 | 45.0 |
| ENS | 51 | Wind kt | 9.2 | 10.3 | 11.3 | 12.8 | 13.7 | 11.6 |
| ENS | 51 | Precip in | 0.16 | 0.21 | 0.31 | 0.40 | 0.45 | 0.32 |
| AIFS_ENS | 51 | High °F | 49.9 | 51.6 | 53.6 | 55.1 | 56.1 | 53.3 |
| AIFS_ENS | 51 | Low °F | 41.7 | 42.2 | 43.0 | 43.5 | 43.9 | 42.9 |
| AIFS_ENS | 51 | Wind kt | 9.4 | 10.2 | 10.7 | 11.1 | 11.7 | 10.7 |
| AIFS_ENS | 51 | Precip in | 0.17 | 0.19 | 0.26 | 0.31 | 0.40 | 0.26 |
| GEFS | 31 | High °F | 53.8 | 55.7 | 57.9 | 59.1 | 61.6 | 57.7 |
| GEFS | 31 | Low °F | 41.9 | 42.5 | 43.3 | 44.5 | 44.9 | 43.5 |
| GEFS | 31 | Wind kt | 9.5 | 9.9 | 11.1 | 11.9 | 12.8 | 11.4 |
| GEFS | 31 | Precip in | 0.10 | 0.16 | 0.35 | 0.58 | 0.73 | 0.38 |
| HRRRCAST | 18 | Precip in | 0.06 | 0.12 | 0.21 | 0.27 | 0.32 | 0.20 |
| REFS | 14 | Precip in | 0.06 | 0.09 | 0.19 | 0.24 | 0.34 | 0.21 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 98% | 69% | 6% |
| AIFS_ENS | 100% | 92% | 53% | 0% |
| GEFS | 100% | 87% | 61% | 32% |
| HRRRCAST | 100% | 78% | 39% | 0% |
| REFS | 100% | 64% | 29% | 7% |

NBM QMD calibrated 24-h precip percentiles: p10 0.02", p25 0.16", p50 0.48", p75 0.56", p90 0.70"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 82% | 37% | 3% | 0% | 82% to 89% | — |
| NBM | NBS P06 | 83% | 52% | 3% | 6% | 83% to 93% | — |
| ENS | member fraction | 100% | 94% | 24% | 14% | 100% | — |
| AIFS_ENS | member fraction | 98% | 82% | 16% | 35% | 100% | — |
| GEFS | member fraction | 100% | 45% | 3% | 26% | 100% | — |
| HRRRCAST | member fraction | — | — | — | — | 100% | — |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 83% | 52% | 3% | 4% | 92% | — |

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS, AIFS_ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 44.4 | 44.2 | 44.3 | 45.1 | 43.1 | 42.4 | 42.0 | 45.0 | 44.0 | 45.2 | 43.0 | 43.9 |
| 10-27 07Z | Tue 02:00 | 44.7 | 44.8 |  | 45.3 |  |  |  |  | 44.0 | 45.4 | 43.2 | 43.9 |
| 10-27 08Z | Tue 03:00 | 44.8 | 45.6 |  | 45.1 |  |  |  |  | 45.0 | 45.5 | 43.5 | 43.9 |
| 10-27 09Z | Tue 04:00 | 44.4 | 46.5 | 45.7 | 46.0 | 43.6 |  | 42.0 | 45.0 | 45.0 | 45.7 | 43.8 | 43.9 |
| 10-27 10Z | Tue 05:00 | 44.4 | 46.8 |  | 46.6 |  |  |  |  | 45.0 | 45.7 | 44.2 | 44.0 |
| 10-27 11Z | Tue 06:00 | 44.7 | 46.4 |  | 47.4 |  |  |  |  | 45.0 | 45.7 | 44.7 | 44.2 |
| 10-27 12Z | Tue 07:00 | 45.0 | 46.0 | 47.1 | 47.3 | 45.5 | 44.8 | 43.0 | 46.0 | 46.0 | 46.1 | 45.4 | 44.6 |
| 10-27 13Z | Tue 08:00 | 45.6 | 46.2 |  | 47.2 |  |  |  |  | 46.0 | 46.9 | 46.4 | 45.1 |
| 10-27 14Z | Tue 09:00 | 46.5 | 46.8 |  | 48.9 |  |  |  |  | 47.0 | 48.2 | 47.8 | 45.8 |
| 10-27 15Z | Tue 10:00 | 47.6 | 47.9 | 50.6 | 50.5 | 48.0 |  | 48.0 | 51.0 | 48.0 | 49.8 | 49.2 | 46.8 |
| 10-27 16Z | Tue 11:00 | 49.2 | 49.5 |  | 53.2 |  |  |  |  | 50.0 | 52.1 | 50.6 | 48.4 |
| 10-27 17Z | Tue 12:00 | 51.1 | 50.8 |  | 55.7 |  |  |  |  | 52.0 | 54.9 | 51.7 | 50.2 |
| 10-27 18Z | Tue 13:00 | 52.3 | 53.0 | 58.2 | 57.5 | 51.6 | 53.7 | 53.0 | 59.0 | 54.0 | 57.1 | 52.3 | 51.9 |
| 10-27 19Z | Tue 14:00 | 52.7 | 53.2 |  | 57.5 |  |  |  |  | 56.0 | 58.8 | 52.4 | 53.7 |
| 10-27 20Z | Tue 15:00 | 53.1 | 53.0 |  | 57.6 |  |  |  |  | 57.0 | 60.0 | 52.1 | 55.5 |
| 10-27 21Z | Tue 16:00 | 53.3 | 54.9 | 58.2 | 58.6 | 55.9 |  | 56.0 | 62.0 | 58.0 | 60.3 | 51.5 | 56.6 |
| 10-27 22Z | Tue 17:00 | 53.2 | 54.8 |  | 59.0 |  |  |  |  | 57.0 | 59.2 | 50.8 | 56.4 |
| 10-27 23Z | Tue 18:00 | 52.6 | 53.8 |  | 58.5 |  |  |  |  | 56.0 | 57.1 | 50.2 | 55.5 |
| 10-28 00Z | Tue 19:00 | 52.4 | 53.3 | 57.5 | 57.7 | 54.9 | 52.2 | 56.0 | 57.0 | 55.0 | 55.5 | 50.0 | 54.9 |
| 10-28 01Z | Tue 20:00 | 52.3 | 53.0 |  | 57.9 |  |  |  |  | 54.0 | 54.8 | 50.0 | 54.9 |
| 10-28 02Z | Tue 21:00 | 52.4 | 52.5 |  | 57.9 |  |  |  |  | 53.0 | 54.4 | 50.2 | 55.3 |
| 10-28 03Z | Tue 22:00 | 52.3 | 52.2 | 57.9 | 57.7 | 55.3 |  | 56.0 | 55.0 | 53.0 | 54.2 | 50.5 | 55.6 |
| 10-28 04Z | Tue 23:00 | 51.7 | 52.2 |  | 57.8 |  |  |  |  | 53.0 | 53.9 | 50.8 | 55.8 |
| 10-28 05Z | Wed 00:00 | 51.1 | 52.1 |  | 58.3 |  |  |  |  | 53.0 | 53.8 | 51.1 | 56.0 |
| 10-28 06Z | Wed 01:00 | 50.7 | 52.0 | 57.1 | 57.6 | 56.4 | 52.5 | 55.0 | 55.0 | 54.0 | 53.7 | 51.1 | 56.1 |

Dewpoint (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 42.3 | 39.8 | 43.1 | 43.3 | 40.1 | 40.8 | 37.0 | 42.0 | 41.0 | 43.8 | 41.6 | 38.5 |
| 10-27 07Z | Tue 02:00 | 42.4 | 40.3 |  | 43.1 |  |  |  |  | 41.0 | 44.0 | 41.8 | 38.6 |
| 10-27 08Z | Tue 03:00 | 42.5 | 41.1 |  | 43.5 |  |  |  |  | 41.0 | 44.2 | 42.1 | 38.6 |
| 10-27 09Z | Tue 04:00 | 42.2 | 43.1 | 44.1 | 44.7 | 40.6 |  | 38.0 | 43.0 | 41.0 | 44.3 | 42.4 | 38.7 |
| 10-27 10Z | Tue 05:00 | 41.9 | 43.3 |  | 45.1 |  |  |  |  | 41.0 | 44.4 | 42.8 | 38.7 |
| 10-27 11Z | Tue 06:00 | 41.8 | 41.9 |  | 46.1 |  |  |  |  | 41.0 | 44.4 | 43.2 | 38.9 |
| 10-27 12Z | Tue 07:00 | 42.2 | 41.9 | 45.6 | 46.1 | 40.9 | 43.4 | 40.0 | 44.0 | 42.0 | 44.7 | 43.6 | 39.1 |
| 10-27 13Z | Tue 08:00 | 43.2 | 42.6 |  | 45.9 |  |  |  |  | 43.0 | 45.3 | 44.3 | 39.5 |
| 10-27 14Z | Tue 09:00 | 44.3 | 43.7 |  | 47.5 |  |  |  |  | 44.0 | 46.1 | 45.1 | 40.1 |
| 10-27 15Z | Tue 10:00 | 45.7 | 45.0 | 48.1 | 48.6 | 43.7 |  | 43.0 | 46.0 | 45.0 | 47.2 | 46.0 | 41.0 |
| 10-27 16Z | Tue 11:00 | 47.5 | 46.8 |  | 51.3 |  |  |  |  | 46.0 | 48.6 | 46.7 | 42.0 |
| 10-27 17Z | Tue 12:00 | 49.5 | 48.1 |  | 53.8 |  |  |  |  | 47.0 | 50.2 | 47.3 | 43.1 |
| 10-27 18Z | Tue 13:00 | 51.4 | 49.8 | 54.7 | 55.9 | 47.7 | 49.9 | 46.0 | 50.0 | 48.0 | 51.4 | 47.6 | 44.2 |
| 10-27 19Z | Tue 14:00 | 50.6 | 51.6 |  | 55.9 |  |  |  |  | 49.0 | 51.7 | 47.6 | 45.4 |
| 10-27 20Z | Tue 15:00 | 50.4 | 50.1 |  | 55.4 |  |  |  |  | 49.0 | 51.5 | 47.3 | 46.5 |
| 10-27 21Z | Tue 16:00 | 50.8 | 50.9 | 54.6 | 55.4 | 49.9 |  | 48.0 | 51.0 | 49.0 | 51.3 | 47.0 | 47.5 |
| 10-27 22Z | Tue 17:00 | 51.2 | 51.0 |  | 55.0 |  |  |  |  | 49.0 | 51.2 | 46.5 | 48.3 |
| 10-27 23Z | Tue 18:00 | 51.5 | 50.8 |  | 54.6 |  |  |  |  | 49.0 | 51.0 | 46.1 | 49.0 |
| 10-28 00Z | Tue 19:00 | 51.5 | 50.8 | 53.8 | 54.8 | 51.4 | 49.0 | 49.0 | 49.0 | 49.0 | 50.8 | 46.0 | 49.5 |
| 10-28 01Z | Tue 20:00 | 51.5 | 50.7 |  | 55.0 |  |  |  |  | 49.0 | 50.6 | 46.1 | 50.0 |
| 10-28 02Z | Tue 21:00 | 51.6 | 49.9 |  | 55.3 |  |  |  |  | 49.0 | 50.5 | 46.5 | 50.6 |
| 10-28 03Z | Tue 22:00 | 51.5 | 49.8 | 54.9 | 55.7 | 52.0 |  | 50.0 | 51.0 | 49.0 | 50.4 | 47.0 | 51.1 |
| 10-28 04Z | Tue 23:00 | 50.3 | 49.9 |  | 56.0 |  |  |  |  | 50.0 | 50.6 | 47.4 | 51.5 |
| 10-28 05Z | Wed 00:00 | 49.6 | 49.9 |  | 56.3 |  |  |  |  | 51.0 | 50.8 | 47.8 | 51.8 |
| 10-28 06Z | Wed 01:00 | 49.3 | 49.9 | 55.1 | 56.0 | 55.2 | 50.2 | 50.0 | 52.0 | 51.0 | 51.0 | 48.1 | 52.0 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 92 | 84 | 96 | 93 | 89 | 94 | 82 | 89 | 89 | 95 | 95 | 81 |
| 10-27 07Z | Tue 02:00 | 92 | 84 |  | 92 |  |  |  |  | 89 | 95 | 95 | 82 |
| 10-27 08Z | Tue 03:00 | 92 | 84 |  | 94 |  |  |  |  | 86 | 95 | 95 | 82 |
| 10-27 09Z | Tue 04:00 | 92 | 88 | 94 | 95 | 89 |  | 86 | 93 | 86 | 95 | 95 | 82 |
| 10-27 10Z | Tue 05:00 | 91 | 88 |  | 94 |  |  |  |  | 86 | 95 | 95 | 82 |
| 10-27 11Z | Tue 06:00 | 89 | 84 |  | 95 |  |  |  |  | 86 | 95 | 94 | 81 |
| 10-27 12Z | Tue 07:00 | 90 | 86 | 94 | 96 | 84 | 95 | 89 | 93 | 86 | 95 | 93 | 81 |
| 10-27 13Z | Tue 08:00 | 91 | 87 |  | 95 |  |  |  |  | 89 | 94 | 92 | 81 |
| 10-27 14Z | Tue 09:00 | 92 | 89 |  | 95 |  |  |  |  | 89 | 93 | 90 | 81 |
| 10-27 15Z | Tue 10:00 | 93 | 90 | 91 | 93 | 85 |  | 83 | 83 | 89 | 91 | 89 | 80 |
| 10-27 16Z | Tue 11:00 | 94 | 90 |  | 93 |  |  |  |  | 86 | 88 | 87 | 79 |
| 10-27 17Z | Tue 12:00 | 94 | 90 |  | 93 |  |  |  |  | 83 | 84 | 85 | 77 |
| 10-27 18Z | Tue 13:00 | 97 | 89 | 88 | 94 | 86 | 87 | 77 | 72 | 80 | 81 | 84 | 75 |
| 10-27 19Z | Tue 14:00 | 93 | 94 |  | 94 |  |  |  |  | 77 | 77 | 84 | 73 |
| 10-27 20Z | Tue 15:00 | 91 | 90 |  | 92 |  |  |  |  | 75 | 74 | 84 | 72 |
| 10-27 21Z | Tue 16:00 | 91 | 86 | 88 | 89 | 80 |  | 74 | 67 | 72 | 72 | 85 | 72 |
| 10-27 22Z | Tue 17:00 | 93 | 87 |  | 87 |  |  |  |  | 75 | 75 | 85 | 75 |
| 10-27 23Z | Tue 18:00 | 96 | 90 |  | 87 |  |  |  |  | 77 | 80 | 86 | 79 |
| 10-28 00Z | Tue 19:00 | 97 | 91 | 87 | 90 | 88 | 89 | 77 | 75 | 80 | 84 | 86 | 82 |
| 10-28 01Z | Tue 20:00 | 97 | 92 |  | 90 |  |  |  |  | 83 | 86 | 87 | 84 |
| 10-28 02Z | Tue 21:00 | 97 | 91 |  | 91 |  |  |  |  | 86 | 87 | 87 | 84 |
| 10-28 03Z | Tue 22:00 | 97 | 92 | 90 | 93 | 89 |  | 80 | 86 | 86 | 87 | 88 | 85 |
| 10-28 04Z | Tue 23:00 | 95 | 92 |  | 94 |  |  |  |  | 90 | 88 | 88 | 85 |
| 10-28 05Z | Wed 00:00 | 95 | 92 |  | 93 |  |  |  |  | 93 | 90 | 89 | 86 |
| 10-28 06Z | Wed 01:00 | 95 | 93 | 93 | 94 | 96 | 92 | 83 | 90 | 90 | 91 | 89 | 87 |

Wind speed (kt) at the hour:

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 8.1 | 9.3 | 8.6 | 8.7 | 7.7 | 8.6 | 11.0 | 11.0 | 10.0 | 9.1 | 9.5 | 9.4 |
| 10-27 07Z | Tue 02:00 | 8.3 | 7.6 |  | 9.3 |  |  |  |  | 10.0 | 9.5 | 9.6 | 9.7 |
| 10-27 08Z | Tue 03:00 | 8.8 | 9.0 |  | 8.8 |  |  |  |  | 11.0 | 9.9 | 9.9 | 10.2 |
| 10-27 09Z | Tue 04:00 | 8.5 | 2.3 | 9.5 | 9.7 | 9.2 |  | 11.0 | 12.0 | 11.0 | 10.2 | 10.1 | 10.5 |
| 10-27 10Z | Tue 05:00 | 11.1 | 11.1 |  | 8.9 |  |  |  |  | 11.0 | 10.5 | 10.2 | 10.3 |
| 10-27 11Z | Tue 06:00 | 10.6 | 10.4 |  | 8.9 |  |  |  |  | 10.0 | 10.8 | 10.2 | 10.0 |
| 10-27 12Z | Tue 07:00 | 9.6 | 9.8 | 9.5 | 9.0 | 7.0 | 8.4 | 10.0 | 13.0 | 10.0 | 11.0 | 9.8 | 9.7 |
| 10-27 13Z | Tue 08:00 | 9.4 | 9.9 |  | 9.7 |  |  |  |  | 10.0 | 11.0 | 9.0 | 9.4 |
| 10-27 14Z | Tue 09:00 | 10.5 | 9.6 |  | 9.4 |  |  |  |  | 10.0 | 10.8 | 8.2 | 9.2 |
| 10-27 15Z | Tue 10:00 | 8.8 | 7.5 | 8.8 | 8.1 | 7.7 |  | 7.0 | 12.0 | 9.0 | 10.2 | 7.8 | 8.8 |
| 10-27 16Z | Tue 11:00 | 6.1 | 6.9 |  | 8.2 |  |  |  |  | 9.0 | 9.1 | 8.2 | 8.0 |
| 10-27 17Z | Tue 12:00 | 7.2 | 8.2 |  | 6.4 |  |  |  |  | 8.0 | 8.2 | 9.0 | 7.3 |
| 10-27 18Z | Tue 13:00 | 6.7 | 7.5 | 7.4 | 6.6 | 6.2 | 7.4 | 7.0 | 11.0 | 8.0 | 7.7 | 9.5 | 6.6 |
| 10-27 19Z | Tue 14:00 | 6.5 | 7.2 |  | 6.3 |  |  |  |  | 7.0 | 7.4 | 9.4 | 5.9 |
| 10-27 20Z | Tue 15:00 | 6.5 | 6.2 |  | 5.5 |  |  |  |  | 7.0 | 7.2 | 8.6 | 5.3 |
| 10-27 21Z | Tue 16:00 | 5.8 | 5.7 | 5.2 | 4.8 | 4.3 |  | 8.0 | 10.0 | 7.0 | 7.0 | 7.6 | 4.9 |
| 10-27 22Z | Tue 17:00 | 5.2 | 5.1 |  | 5.2 |  |  |  |  | 6.0 | 6.2 | 6.5 | 4.6 |
| 10-27 23Z | Tue 18:00 | 4.0 | 5.1 |  | 4.4 |  |  |  |  | 6.0 | 5.1 | 5.7 | 4.4 |
| 10-28 00Z | Tue 19:00 | 2.5 | 3.5 | 5.1 | 4.8 | 3.4 | 3.9 | 6.0 | 7.0 | 5.0 | 4.6 | 5.3 | 4.4 |
| 10-28 01Z | Tue 20:00 | 2.8 | 3.1 |  | 5.4 |  |  |  |  | 5.0 | 4.9 | 5.2 | 4.5 |
| 10-28 02Z | Tue 21:00 | 3.1 | 3.6 |  | 6.0 |  |  |  |  | 6.0 | 5.7 | 5.3 | 5.3 |
| 10-28 03Z | Tue 22:00 | 3.5 | 2.3 | 5.9 | 5.4 | 5.2 |  | 7.0 | 8.0 | 6.0 | 6.2 | 5.7 | 6.0 |
| 10-28 04Z | Tue 23:00 | 5.6 | 1.0 |  | 5.2 |  |  |  |  | 6.0 | 6.2 | 6.1 | 6.3 |
| 10-28 05Z | Wed 00:00 | 6.4 | 2.5 |  | 6.2 |  |  |  |  | 5.0 | 6.1 | 6.5 | 6.4 |
| 10-28 06Z | Wed 01:00 | 6.9 | 2.8 | 5.7 | 5.4 | 4.3 | 5.2 | 5.0 | 7.0 | 5.0 | 6.0 | 6.6 | 6.5 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 |
| 10-27 07Z | Tue 02:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.03 | 0.03 | 0.03 | 0.07 |
| 10-27 08Z | Tue 03:00 | 0.03 | 0.00 |  | 0.07 |  |  | 0.05 | 0.06 | 0.07 | 0.15 |
| 10-27 09Z | Tue 04:00 | 0.05 | 0.01 | 0.12 | 0.16 | 0.26 |  | 0.08 | 0.09 | 0.10 | 0.22 |
| 10-27 10Z | Tue 05:00 | 0.17 | 0.10 |  | 0.26 |  |  | 0.11 | 0.14 | 0.13 | 0.26 |
| 10-27 11Z | Tue 06:00 | 0.19 | 0.10 |  | 0.29 |  |  | 0.14 | 0.19 | 0.17 | 0.31 |
| 10-27 12Z | Tue 07:00 | 0.19 | 0.10 | 0.28 | 0.33 | 0.28 | 0.20 | 0.17 | 0.25 | 0.20 | 0.35 |
| 10-27 13Z | Tue 08:00 | 0.24 | 0.11 |  | 0.35 |  |  | 0.19 | 0.27 | 0.21 | 0.36 |
| 10-27 14Z | Tue 09:00 | 0.24 | 0.12 |  | 0.35 |  |  | 0.21 | 0.28 | 0.21 | 0.37 |
| 10-27 15Z | Tue 10:00 | 0.24 | 0.12 | 0.32 | 0.37 | 0.29 |  | 0.22 | 0.30 | 0.22 | 0.37 |
| 10-27 16Z | Tue 11:00 | 0.25 | 0.12 |  | 0.42 |  |  | 0.22 | 0.30 | 0.22 | 0.37 |
| 10-27 17Z | Tue 12:00 | 0.25 | 0.12 |  | 0.43 |  |  | 0.22 | 0.31 | 0.23 | 0.38 |
| 10-27 18Z | Tue 13:00 | 0.25 | 0.12 | 0.35 | 0.45 | 0.29 | 0.26 | 0.22 | 0.31 | 0.24 | 0.38 |
| 10-27 19Z | Tue 14:00 | 0.25 | 0.12 |  | 0.46 |  |  | 0.22 | 0.31 | 0.24 | 0.38 |
| 10-27 20Z | Tue 15:00 | 0.25 | 0.12 |  | 0.46 |  |  | 0.22 | 0.31 | 0.24 | 0.38 |
| 10-27 21Z | Tue 16:00 | 0.25 | 0.12 | 0.35 | 0.46 | 0.29 |  | 0.22 | 0.31 | 0.24 | 0.38 |
| 10-27 22Z | Tue 17:00 | 0.25 | 0.12 |  | 0.46 |  |  | 0.22 | 0.31 | 0.24 | 0.38 |
| 10-27 23Z | Tue 18:00 | 0.25 | 0.12 |  | 0.46 |  |  | 0.22 | 0.31 | 0.24 | 0.38 |
| 10-28 00Z | Tue 19:00 | 0.25 | 0.12 | 0.35 | 0.46 | 0.29 | 0.28 | 0.22 | 0.31 | 0.24 | 0.38 |
| 10-28 01Z | Tue 20:00 | 0.25 | 0.12 |  | 0.46 |  |  | 0.22 | 0.32 | 0.24 | 0.38 |
| 10-28 02Z | Tue 21:00 | 0.25 | 0.12 |  | 0.46 |  |  | 0.22 | 0.32 | 0.25 | 0.38 |
| 10-28 03Z | Tue 22:00 | 0.25 | 0.12 | 0.35 | 0.46 | 0.29 |  | 0.22 | 0.32 | 0.25 | 0.38 |
| 10-28 04Z | Tue 23:00 | 0.25 | 0.12 |  | 0.47 |  |  | 0.22 | 0.32 | 0.25 | 0.38 |
| 10-28 05Z | Wed 00:00 | 0.25 | 0.12 |  | 0.47 |  |  | 0.22 | 0.32 | 0.25 | 0.38 |
| 10-28 06Z | Wed 01:00 | 0.25 | 0.12 | 0.36 | 0.47 | 0.30 | 0.28 | 0.22 | 0.32 | 0.26 | 0.38 |

Total cloud cover (%):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 100 | 76 | 81 | 87 | 100 | 89 | 100 | 85 | 100 | 95 | 97 | 100 |
| 10-27 07Z | Tue 02:00 | 100 | 92 |  | 86 |  |  |  | 81 | 100 | 95 | 95 | 100 |
| 10-27 08Z | Tue 03:00 | 100 | 97 |  | 100 |  |  |  | 83 | 100 | 96 | 92 | 100 |
| 10-27 09Z | Tue 04:00 | 73 | 100 | 98 | 100 | 100 |  | 100 | 87 | 100 | 96 | 90 | 100 |
| 10-27 10Z | Tue 05:00 | 100 | 80 |  | 99 |  |  |  | 84 | 100 | 92 | 87 | 100 |
| 10-27 11Z | Tue 06:00 | 100 | 71 |  | 50 |  |  |  | 66 | 100 | 87 | 85 | 99 |
| 10-27 12Z | Tue 07:00 | 100 | 67 | 98 | 82 | 100 | 85 | 100 | 68 | 100 | 85 | 84 | 99 |
| 10-27 13Z | Tue 08:00 | 100 | 76 |  | 84 |  |  |  | 70 | 100 | 88 | 85 | 98 |
| 10-27 14Z | Tue 09:00 | 100 | 96 |  | 100 |  |  |  | 68 | 100 | 94 | 87 | 98 |
| 10-27 15Z | Tue 10:00 | 100 | 99 | 100 | 95 | 100 |  | 100 | 69 | 100 | 99 | 90 | 97 |
| 10-27 16Z | Tue 11:00 | 100 | 100 |  | 99 |  |  |  | 85 | 100 | 98 | 92 | 96 |
| 10-27 17Z | Tue 12:00 | 100 | 100 |  | 100 |  |  |  | 90 | 100 | 96 | 93 | 94 |
| 10-27 18Z | Tue 13:00 | 100 | 100 | 100 | 100 | 100 | 97 | 100 | 91 | 100 | 93 | 93 | 91 |
| 10-27 19Z | Tue 14:00 | 100 | 100 |  | 100 |  |  |  | 88 | 100 | 80 | 88 | 88 |
| 10-27 20Z | Tue 15:00 | 100 | 100 |  | 98 |  |  |  | 84 | 100 | 62 | 80 | 84 |
| 10-27 21Z | Tue 16:00 | 100 | 85 | 100 | 100 | 100 |  | 100 | 89 | 100 | 48 | 71 | 79 |
| 10-27 22Z | Tue 17:00 | 100 | 99 |  | 100 |  |  |  |  | 100 | 38 | 62 | 72 |
| 10-27 23Z | Tue 18:00 | 100 | 100 |  | 100 |  |  |  |  | 100 | 29 | 55 | 64 |
| 10-28 00Z | Tue 19:00 | 100 | 100 | 100 | 100 | 94 | 75 | 100 | 74 | 99 | 23 | 51 | 59 |
| 10-28 01Z | Tue 20:00 | 100 | 100 |  | 100 |  |  |  |  | 95 | 21 | 52 | 60 |
| 10-28 02Z | Tue 21:00 | 100 | 100 |  | 100 |  |  |  |  | 86 | 20 | 55 | 62 |
| 10-28 03Z | Tue 22:00 | 100 | 100 | 100 | 100 | 100 |  | 100 | 59 | 82 | 21 | 60 | 65 |
| 10-28 04Z | Tue 23:00 | 100 | 100 |  | 100 |  |  |  |  | 86 | 28 | 66 | 65 |
| 10-28 05Z | Wed 00:00 | 100 | 99 |  | 96 |  |  |  |  | 94 | 38 | 71 | 65 |
| 10-28 06Z | Wed 01:00 | 100 | 90 | 48 | 51 | 100 | 81 | 100 | 73 | 98 | 44 | 74 | 64 |

## Track record this period

Since 2026-10-12 at KMSP (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-27 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 14 | 5.4 | -1.0 | -0.1 | -2.2 | -0.01 | 1.7 | 1.0 | 2.8 | 0.04 |
| NBM | 14 | 7.6 | -0.9 | +0.3 | -4.0 | -0.03 | 2.8 | 1.4 | 4.1 | 0.03 |
| GFS_MOS | 14 | 8.0 | -0.6 | +1.1 | -3.7 | -0.01 | 2.5 | 2.9 | 4.0 | 0.02 |
| RRFS | 14 | 8.4 | -0.1 | -2.1 | -5.4 | -0.02 | 1.3 | 3.2 | 5.4 | 0.04 |
| HRRR | 14 | 8.5 | -1.7 | -2.7 | -4.9 | +0.00 | 1.9 | 2.8 | 4.9 | 0.06 |
| GFS | 14 | 10.0 | -0.1 | +3.7 | -5.8 | +0.01 | 1.9 | 3.7 | 5.8 | 0.06 |
| AIFS | 14 | 10.2 | -2.9 | -2.2 | -6.0 | +0.02 | 3.0 | 2.7 | 6.0 | 0.05 |
| IFS_HRES | 14 | 10.4 | -1.2 | +0.6 | -6.2 | -0.01 | 3.6 | 1.8 | 6.2 | 0.06 |
| IFS | 14 | 10.8 | -1.4 | +0.2 | -6.5 | +0.01 | 3.6 | 1.6 | 6.5 | 0.08 |

## Daily verification (all 14 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 1.9 | 10.0 | 7.3 | 9.4 | 8.1 | 14.0 | 13.0 | 9.0 | 6.3 | HRRR |
| 10-13 h | 5.3 | 5.8 | 12.3 | 15.1 | 11.7 | 8.3 | 8.2 | 12.2 | 7.9 | HRRR |
| 10-14 h | 6.4 | 8.0 | 12.5 | 13.5 | 7.5 | 5.5 | 7.5 | 8.0 | 2.0 | CONSENSUS |
| 10-15 h | 12.5 | 13.5 | 19.6 | 16.8 | 8.1 | 9.2 | 10.0 | 14.0 | 7.5 | CONSENSUS |
| 10-16 h | 16.3 | 10.1 | 6.5 | 7.9 | 12.0 | 17.8 | 4.8 | 7.0 | 9.9 | GFS_MOS |
| 10-17 h | 10.0 | 10.0 | 8.0 | 7.0 | 12.0 | 11.0 | 5.0 | 6.5 | 5.0 | GFS_MOS |
| 10-18 h | 13.5 | 9.5 | 15.5 | 14.5 | 6.5 | 11.5 | 14.0 | 11.5 | 9.5 | GFS |
| 10-19 h | 5.0 | 6.0 | 8.0 | 7.0 | 9.0 | 10.0 | 4.0 | 6.5 | 1.0 | CONSENSUS |
| 10-20 h | 8.5 | 7.0 | 9.0 | 7.5 | 8.5 | 8.5 | 5.0 | 8.5 | 3.0 | CONSENSUS |
| 10-21 h | 7.5 | 8.0 | 8.5 | 9.5 | 9.0 | 4.5 | 5.5 | 5.0 | 3.5 | CONSENSUS |
| 10-22 h | 2.5 | 6.0 | 6.0 | 5.5 | 7.5 | 7.5 | 8.5 | 2.5 | 1.5 | CONSENSUS |
| 10-23 h | 9.0 | 8.9 | 11.7 | 8.1 | 14.3 | 7.4 | 5.0 | 5.5 | 4.1 | CONSENSUS |
| 10-24 h | 9.0 | 8.3 | 17.1 | 13.2 | 13.8 | 15.4 | 11.5 | 6.8 | 8.6 | NBM |
| 10-25 h | 11.5 | 7.2 | 8.9 | 10.4 | 12.3 | 12.8 | 9.7 | 3.5 | 6.3 | NBM |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 81 | +0 | +4 | +1 | +2 | +2 | -6 | -4 | +3 | +0 |
| 10-13 h | 57 | +0 | +2 | +5 | +5 | +8 | +1 | +5 | +8 | +4 |
| 10-14 h | 55 | -3 | +3 | +6 | +6 | +5 | -2 | +5 | +5 | -1 |
| 10-15 h | 51 | +2 | +2 | +4 | +3 | +1 | -2 | +5 | +4 | +1 |
| 10-16 h | 53 | -6 | -1 | -1 | -2 | -1 | -3 | -2 | -1 | -4 |
| 10-17 h | 60 | -4 | -3 | -2 | -1 | +1 | -4 | -1 | -4 | -3 |
| 10-18 h | 70 | -4 | -3 | -9 | -8 | -2 | -7 | -7 | -8 | -6 |
| 10-19 h | 66 | -1 | +0 | -5 | -4 | +0 | -3 | +0 | -4 | -1 |
| 10-20 h | 69 | -2 | +0 | -3 | -3 | -1 | -1 | -1 | -3 | -1 |
| 10-21 h | 74 | -2 | -2 | -6 | -6 | -2 | -4 | -1 | -3 | -2 |
| 10-22 h | 75 | -1 | +1 | -3 | -3 | +0 | -3 | -1 | -1 | +0 |
| 10-23 h | 76 | -2 | +0 | -2 | -2 | -4 | -2 | -1 | -2 | -1 |
| 10-24 h | 75 | -1 | +0 | -2 | -2 | -2 | -3 | -4 | +0 | -1 |
| 10-25 h | 55 | +0 | -1 | +3 | +4 | +1 | -2 | +2 | +0 | +1 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 55 | +0 | +4 | +3 | +4 | +2 | +0 | +6 | +4 | +3 |
| 10-13 h | 53 | -2 | +0 | -2 | -2 | +0 | -4 | +0 | +1 | -1 |
| 10-14 h | 46 | +1 | -3 | +4 | +5 | +0 | +1 | -1 | +1 | +0 |
| 10-15 h | 45 | +0 | +1 | +3 | +3 | +0 | +2 | +1 | +1 | +0 |
| 10-16 h | 40 | -5 | -3 | +0 | +0 | +4 | -7 | +0 | -2 | -2 |
| 10-17 h | 36 | -2 | -3 | +1 | +1 | +7 | -3 | -2 | +0 | +0 |
| 10-18 h | 48 | -7 | -4 | -3 | -3 | +2 | -2 | -6 | -2 | -3 |
| 10-19 h | 44 | -2 | -4 | -1 | -1 | +7 | -5 | +3 | +1 | +0 |
| 10-20 h | 46 | -4 | -4 | -2 | -1 | +4 | -4 | +2 | -3 | -1 |
| 10-21 h | 48 | -4 | -5 | +1 | +2 | +6 | +0 | +3 | +1 | +1 |
| 10-22 h | 49 | -1 | -4 | -2 | -2 | +7 | -4 | +7 | -1 | +0 |
| 10-23 h | 56 | -4 | -3 | +1 | +1 | +4 | +1 | +1 | +1 | +0 |
| 10-24 h | 51 | -2 | +3 | +1 | +1 | +3 | -2 | +4 | +3 | +2 |
| 10-25 h | 48 | -3 | -2 | +1 | +2 | +2 | -3 | -3 | +0 | -1 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 15 | -3 | -4 | -5 | -6 | -5 | -8 | -6 | -4 | -5 |
| 10-13 h | 14 | -5 | -6 | -5 | -4 | -5 | -5 | -4 | -4 | -5 |
| 10-14 h | 12 | -4 | -4 | -5 | -5 | -5 | -5 | -3 | -4 | -2 |
| 10-15 h | 15 | -3 | -3 | -3 | -3 | -4 | -5 | +1 | +0 | +0 |
| 10-16 h | 26 | -9 | -9 | -11 | -11 | -10 | -12 | -4 | -8 | -7 |
| 10-17 h | 20 | -8 | -8 | -10 | -10 | -8 | -8 | -4 | -5 | -4 |
| 10-18 h | 17 | -5 | -5 | -7 | -7 | -5 | -5 | -2 | -3 | -1 |
| 10-19 h | 9 | -4 | -4 | -4 | -4 | -4 | -4 | -2 | -3 | +0 |
| 10-20 h | 15 | -5 | -6 | -8 | -7 | -7 | -7 | -4 | -5 | -2 |
| 10-21 h | 8 | -3 | -2 | -3 | -3 | -2 | -1 | -3 | -2 | +1 |
| 10-22 h | 7 | -1 | -2 | -2 | -1 | -1 | -1 | +1 | +1 | +3 |
| 10-23 h | 19 | -6 | -7 | -7 | -7 | -7 | -8 | -6 | -5 | -3 |
| 10-24 h | 20 | -8 | -9 | -10 | -10 | -9 | -8 | -7 | -6 | -4 |
| 10-25 h | 14 | -4 | -6 | -9 | -8 | -8 | -8 | -7 | -7 | -3 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 0.00 | +0.01 | +0.00 | +0.02 | +0.01 | +0.04 | +0.10 | +0.00 | +0.00 | +0.02 |
| 10-13 h | 0.03 | -0.02 | -0.02 | +0.07 | +0.18 | -0.03 | -0.02 | -0.03 | -0.03 | -0.01 |
| 10-14 h | 0.00 | +0.01 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-15 h | 0.69 | -0.51 | -0.51 | -0.58 | -0.52 | -0.35 | -0.23 | -0.27 | -0.51 | -0.42 |
| 10-16 h | 0.07 | +0.02 | -0.04 | +0.00 | -0.01 | -0.05 | +0.05 | -0.02 | +0.00 | -0.01 |
| 10-17 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-18 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-19 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-20 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-21 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-22 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-23 h | 0.00 | +0.00 | +0.06 | +0.14 | +0.04 | +0.07 | +0.01 | +0.00 | +0.00 | +0.04 |
| 10-24 h | 0.00 | +0.05 | +0.02 | +0.28 | +0.14 | +0.11 | +0.18 | +0.00 | +0.02 | +0.09 |
| 10-25 h | 0.02 | +0.19 | +0.03 | -0.01 | -0.01 | +0.15 | +0.10 | +0.03 | +0.00 | +0.07 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 14 | +17 | 18 | +11 | 12 |
| RRFS | 14 | +7 | 8 | +12 | 15 |
| IFS | 14 | +2 | 12 | -3 | 9 |
| IFS_HRES | 14 | +2 | 14 | +0 | 9 |
| GFS | 14 | +9 | 19 | +2 | 15 |
| AIFS | 14 | +8 | 13 | +4 | 7 |
| GFS_MOS | 14 | -2 | 4 | +2 | 15 |
| NBM | 14 | +1 | 11 | -4 | 10 |

Night clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 46% | — | +43 | +9 | -11 | +10 | +23 | +30 | -9 | +10 |
| 10-13 h | 100% | — | +0 | -5 | +0 | -1 | +0 | -6 | +0 | -20 |
| 10-14 h | 100% | — | +0 | +0 | -3 | -4 | -100 | -10 | -11 | -32 |
| 10-15 h | 92% | — | +8 | +8 | +2 | +4 | +8 | +2 | -8 | -8 |
| 10-16 h | 100% | — | +0 | -7 | -6 | -11 | +0 | -17 | +0 | -14 |
| 10-17 h | 0% | — | +3 | +0 | +0 | +0 | +5 | +0 | +0 | +7 |
| 10-18 h | 0% | — | +4 | +0 | +4 | +7 | +26 | +31 | +0 | +5 |
| 10-19 h | 0% | — | +84 | +76 | +54 | +52 | +74 | +39 | +0 | +32 |
| 10-20 h | 0% | — | +3 | +2 | +0 | +1 | +0 | +0 | +0 | +3 |
| 10-21 h | 0% | — | +0 | +0 | +6 | +7 | +3 | +10 | +0 | +2 |
| 10-22 h | 0% | — | +48 | +10 | +27 | +29 | +17 | +18 | +0 | +17 |
| 10-23 h | 23% | — | +46 | +0 | -21 | -22 | +19 | +6 | -18 | +6 |
| 10-24 h | 53% | — | -6 | +3 | -22 | -25 | +18 | +16 | +6 | -2 |
| 10-25 h | 100% | — | +0 | -3 | +0 | +0 | +0 | -6 | +0 | -14 |

Day clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 28% | — | +66 | +34 | +41 | +43 | -5 | +33 | +27 | +12 |
| 10-13 h | 96% | — | +4 | +1 | -11 | -18 | -69 | -9 | -18 | -24 |
| 10-14 h | 80% | — | +20 | -11 | -48 | -50 | -30 | +10 | -32 | -26 |
| 10-15 h | 100% | — | +0 | +0 | +0 | +0 | +0 | -1 | +0 | -11 |
| 10-16 h | 54% | — | +7 | -19 | -17 | -13 | -18 | -9 | +3 | -10 |
| 10-17 h | 0% | — | +2 | +0 | +0 | +0 | +2 | +2 | +0 | +3 |
| 10-18 h | 24% | — | +31 | +3 | +21 | +16 | -11 | +9 | -17 | -3 |
| 10-19 h | 47% | — | +27 | +13 | -9 | +6 | +2 | +5 | -42 | -11 |
| 10-20 h | 0% | — | +1 | +1 | +0 | +0 | +0 | +0 | +2 | +5 |
| 10-21 h | 9% | — | -8 | +0 | -7 | -7 | +16 | -2 | +16 | -4 |
| 10-22 h | 0% | — | +2 | +70 | +0 | +0 | +18 | +6 | +30 | +12 |
| 10-23 h | 68% | — | +17 | +19 | -7 | +4 | +32 | +1 | +2 | -13 |
| 10-24 h | 46% | — | +12 | +27 | +0 | +6 | +19 | +19 | +24 | +6 |
| 10-25 h | 96% | — | +2 | +3 | +0 | -1 | +4 | -3 | +4 | -8 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 14 | +0.5 | 1.5 | +1.6 | 2.2 |
| RRFS | 14 | +0.7 | 1.4 | +0.9 | 1.3 |
| IFS | 14 | +1.6 | 2.3 | +2.1 | 2.6 |
| IFS_HRES | 14 | +1.7 | 2.3 | +2.0 | 2.9 |
| GFS | 14 | -1.0 | 2.5 | -2.3 | 2.4 |
| AIFS | 14 | -0.2 | 1.5 | +0.4 | 1.2 |
| GFS_MOS | 14 | +0.4 | 2.1 | +0.8 | 1.9 |
| NBM | 14 | +0.8 | 1.5 | +0.3 | 1.2 |

Night dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 56.3 | +3.1 | +3.0 | +5.3 | +5.7 | +2.1 | +1.0 | +1.7 | +1.4 |
| 10-13 h | 49.5 | -1.1 | +1.7 | +0.5 | +1.0 | -1.1 | -0.2 | +1.5 | +2.2 |
| 10-14 h | 43.9 | -0.4 | -3.0 | -2.1 | -2.3 | -4.1 | -2.1 | -2.6 | -1.2 |
| 10-15 h | 43.9 | +0.2 | -0.6 | +0.8 | +1.4 | -3.1 | -0.4 | -0.2 | +0.4 |
| 10-16 h | 43.0 | -0.1 | -1.2 | -2.9 | -2.2 | -4.3 | -2.6 | -6.0 | -1.5 |
| 10-17 h | 30.3 | +3.1 | +2.5 | +3.8 | +3.8 | -10.9 | -1.1 | -5.3 | +0.2 |
| 10-18 h | 32.7 | +4.6 | +0.8 | +2.6 | +2.6 | -2.7 | +0.9 | -0.7 | +3.0 |
| 10-19 h | 36.8 | +3.1 | +4.2 | +5.2 | +5.2 | +0.7 | +2.5 | +2.9 | +5.6 |
| 10-20 h | 42.7 | +0.5 | -0.1 | +0.9 | +1.0 | -1.8 | -2.3 | -0.4 | -0.3 |
| 10-21 h | 40.8 | -1.3 | -0.3 | +5.0 | +5.1 | +2.0 | +2.3 | +3.5 | +2.2 |
| 10-22 h | 48.3 | -0.7 | -1.1 | -0.8 | -0.5 | -0.7 | -3.6 | +2.7 | -1.3 |
| 10-23 h | 52.2 | -0.5 | +0.6 | +2.5 | +2.5 | +2.0 | +0.7 | +0.8 | +1.2 |
| 10-24 h | 48.9 | -1.8 | +0.3 | +1.6 | +1.5 | -0.8 | +0.1 | +1.8 | -0.9 |
| 10-25 h | 40.7 | +1.2 | +2.4 | -0.1 | +0.1 | +2.4 | +1.0 | +1.0 | +0.3 |

Day dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 58.1 | +1.7 | +2.2 | +1.9 | +3.5 | -0.2 | -0.6 | +0.7 | -0.7 |
| 10-13 h | 46.4 | +1.0 | +1.2 | -0.9 | -0.9 | -2.5 | -2.0 | +0.6 | +0.4 |
| 10-14 h | 41.2 | -0.6 | -2.1 | -2.8 | -2.8 | -2.4 | -1.2 | -0.2 | -2.3 |
| 10-15 h | 46.6 | +0.0 | -0.9 | -0.9 | +0.5 | -1.4 | -0.3 | -2.9 | +0.4 |
| 10-16 h | 31.7 | +2.5 | -0.6 | +0.8 | +1.0 | -5.8 | +1.6 | +1.1 | +1.0 |
| 10-17 h | 28.0 | +9.4 | +5.9 | +6.8 | +6.5 | -6.9 | +2.4 | -3.4 | +2.8 |
| 10-18 h | 36.2 | +3.5 | +0.9 | +4.7 | +4.6 | -5.6 | +0.7 | -1.4 | +3.3 |
| 10-19 h | 41.2 | +3.1 | +1.9 | +5.1 | +5.2 | -2.2 | +1.8 | -1.2 | +2.3 |
| 10-20 h | 41.7 | +1.9 | +0.1 | +4.3 | +4.0 | -2.6 | -0.6 | +0.9 | -0.1 |
| 10-21 h | 47.1 | +1.0 | +1.5 | +3.7 | +4.1 | -1.7 | +0.9 | +1.3 | +0.1 |
| 10-22 h | 52.7 | -0.1 | +0.0 | +0.3 | +0.9 | -1.4 | -1.4 | -0.1 | -2.1 |
| 10-23 h | 49.3 | -1.4 | +0.5 | +1.5 | +1.3 | +0.8 | +0.5 | +3.8 | -0.7 |
| 10-24 h | 49.8 | -1.3 | +0.4 | +3.2 | +2.9 | +0.1 | -0.7 | +0.8 | -0.7 |
| 10-25 h | 32.0 | +3.3 | +1.7 | -0.7 | -2.8 | -2.7 | +2.2 | +5.6 | +0.8 |

## Today so far (2026-10-26, through 2026-10-26T21:03Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 48.9 °F, low 42.1 °F, max wind 11 kt, precip 0.26" (15 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 25/18Z | +1.0 | 1.0 | 50 (+1) | 43 (+0) | -0.2 | 0.17 | -0.09 |
| RRFS | 25/18Z | +1.8 | 1.8 | 50 (+1) | 44 (+2) | +0.0 | 0.21 | -0.05 |
| IFS | 25/12Z | +1.8 | 1.9 | 49 (+0) | 44 (+2) | -1.5 | 0.16 | -0.10 |
| IFS_HRES | 25/12Z | +2.3 | 2.3 | 50 (+2) | 45 (+3) | -1.7 | 0.16 | -0.10 |
| GFS | 25/18Z | +0.7 | 1.2 | 48 (-1) | 42 (+0) pending | -1.2 | 0.11 | -0.15 |
| AIFS | 25/12Z | -0.8 | 1.2 | 46 (-3) | 42 (+0) | -0.8 | 0.22 | -0.04 |
| GFS_MOS | 25/18Z | -1.4 | 2.6 | 48 (-1) | 39 (-3) | +0.9 | — | — |
| NBM | 25/23Z | +1.9 | 2.1 | 49 (+0) | 43 (+1) | +0.7 | — | — |

## Clouds so far today (2026-10-26, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-19 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (CDT) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 06Z | Mon 01:00 | 100 |  | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 92 |
| 10-26 07Z | Mon 02:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 85 |
| 10-26 08Z | Mon 03:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 89 |
| 10-26 09Z | Mon 04:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |  | 100 | 90 |
| 10-26 10Z | Mon 05:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 88 |
| 10-26 11Z | Mon 06:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 89 |
| 10-26 12Z | Mon 07:00 | 100 | 100 | 100 | 97 | 100 | 100 | 100 | 100 | 100 | 86 |
| 10-26 13Z | Mon 08:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 87 |
| 10-26 14Z | Mon 09:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 84 |
| 10-26 15Z | Mon 10:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |  | 100 | 88 |
| 10-26 16Z | Mon 11:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 90 |
| 10-26 17Z | Mon 12:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 91 |
| 10-26 18Z | Mon 13:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 91 |
| 10-26 19Z | Mon 14:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 93 |
| 10-26 20Z | Mon 15:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 90 |
| 10-26 21Z | Mon 16:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |  | 100 | 92 |

## Dewpoint so far today (2026-10-26, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (CDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 07Z | Mon 02:00 | 34.0 | 56 | 32.9 | 29.9 |  | 34.4 |  |  |  |  |
| 10-26 08Z | Mon 03:00 | 34.0 | 61 | 31.8 | 29.6 |  | 35.8 |  |  |  |  |
| 10-26 09Z | Mon 04:00 | 35.1 | 66 | 30.5 | 29.5 | 37.4 | 37.2 | 33.3 |  | 34.0 | 35.0 |
| 10-26 10Z | Mon 05:00 | 35.1 | 68 | 30.5 | 30.6 |  | 36.2 |  |  |  |  |
| 10-26 11Z | Mon 06:00 | 36.0 | 73 | 30.5 | 31.6 |  | 36.2 |  |  |  |  |
| 10-26 12Z | Mon 07:00 | 37.0 | 76 | 30.9 | 32.8 | 37.0 | 37.2 | 29.7 | 37.4 | 33.0 | 35.0 |
| 10-26 13Z | Mon 08:00 | 36.0 | 73 | 32.2 | 34.8 |  | 37.8 |  |  |  |  |
| 10-26 14Z | Mon 09:00 | 34.0 | 67 | 34.7 | 36.8 |  | 37.0 |  |  |  |  |
| 10-26 15Z | Mon 10:00 | 35.1 | 70 | 35.5 | 36.0 | 35.0 | 36.1 | 28.6 |  | 33.0 | 36.0 |
| 10-26 16Z | Mon 11:00 | 37.0 | 76 | 35.4 | 37.5 |  | 36.1 |  |  |  |  |
| 10-26 17Z | Mon 12:00 | 39.0 | 86 | 37.9 | 39.7 |  | 36.6 |  |  |  |  |
| 10-26 18Z | Mon 13:00 | 39.9 | 89 | 39.0 | 41.1 | 37.5 | 38.4 | 33.7 | 37.9 | 35.0 | 36.0 |
| 10-26 19Z | Mon 14:00 | 39.9 | 89 | 39.7 | 41.2 |  | 40.3 |  |  |  |  |
| 10-26 20Z | Mon 15:00 | 39.9 | 89 | 40.4 | 42.3 |  | 43.1 |  |  |  |  |
| 10-26 21Z | Mon 16:00 | 39.9 | 89 | 41.1 | 42.2 | 43.3 | 43.7 | 35.1 |  | 37.0 | 36.0 |
| Bias so far |  |  |  | -1.9 | -1.1 | +0.6 | +0.9 | -5.3 | -0.8 | -3.0 | -1.8 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (MPX): https://forecast.weather.gov/product.php?site=mpx&issuedby=mpx&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
