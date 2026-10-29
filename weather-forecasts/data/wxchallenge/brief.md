# WxChallenge forecast brief: Minneapolis, MN (KMSP)

- Station: **KMSP**
- Target day: **2026-10-30**, scored over 2026-10-30T06Z to 2026-10-31T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-30T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-29T17:30:06+00:00 (refreshed several times an hour while the forecast job runs)
- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)

## How to use this brief (for AI assistants)

1. Look at all model forecasts for the target day, then the **CONSENSUS** row.
2. Check the track-record table. A model with a large, consistent bias (|bias| close to its MAE) is reliably off in that direction. The consensus tries to remove some of that bias.
3. For precip, enter roughly the ensemble **median**, not the mean: errors are charged per 0.01" and most heavily near zero. When the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.
4. Use "Today so far" (the day currently in progress, not the target day) to see which models are handling the current pattern; persistent errors there often carry into the target day.
5. Think about what might be missing from the data or what would be helpful to know. Start with the cloud and dewpoint sections (too clear at night -> low too cold; too moist -> low too warm). If anything of note, suggest what to look for on the GOES or model spatial maps to nudge the forecast one way or another.
6. Read the latest AFD for the forecaster's view of the pattern.
7. Give whole °F for high/low, whole kt for wind, and precip to 0.01". State your reasoning, especially for any departure from the consensus.

## Scoring (error points; lower is better)

- High and low temperature: 1 point per °F of error.
- Max sustained wind: 0.5 point per kt of error.
- Precipitation: per 0.01" between forecast and observed: 0.4 pt for amounts 0.00 to 0.10", 0.3 for 0.11 to 0.25", 0.2 for 0.26 to 0.50", 0.1 above 0.50". A trace counts as 0.00.
- Forecasts are rounded as submitted (whole °F and kt, 0.01") before scoring.

## Guidance for the target day

Run = day/hour (UTC) of the model initialization.

| Model | Run | High °F | Low °F | Wind kt | Precip in |
| --- | --- | --: | --: | --: | --: |
| HRRR | 29/12Z | 51.0 | 38.2 | 4.8 | 0.00 |
| RRFS | 29/12Z | 53.3 | 36.6 | 5.9 | 0.00 |
| IFS | 29/06Z | 55.7 | 40.5 | 4.6 | 0.00 |
| IFS_HRES | 29/06Z | 56.1 | 40.4 | 5.0 | 0.00 |
| GFS | 29/12Z | 56.2 | 44.5 | 6.1 | 0.00 |
| GFS_MOS | 29/12Z | 57.0 | 39.0 | 8.0 | 0.00 |
| NBM | 29/16Z | 53.0 | 39.0 | 7.0 | 0.00 |
| USL | 29/12Z | 57.0 | 40.0 | 11.0 | 0.00 |
| ENS | 29/06Z | 55.5 | 41.6 | 5.4 | 0.00 |
| GEFS | 29/06Z | 55.2 | 44.7 | 7.5 | 0.00 |
| HRRRCAST (precip only) | 29/06Z | — | — | — | 0.00 |
| REFS (precip only) | 29/12Z | — | — | — | 0.00 |
| NBM_QMD (precip only) | 29/06Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **55.9** | **40.0** | **10.9** | **0.00** |

Notes:
- IFS_HRES: not in the consensus
- GFS_MOS: MOS Q06 categories [0, 0, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members
- GEFS: ensemble mean of 31 members; not in the consensus
- HRRRCAST: median of 18 members
- REFS: median of 14 members

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: USL 0.15, RRFS 0.14, GFS 0.13, NBM 0.13, GFS_MOS 0.12, ENS 0.12, HRRR 0.11, IFS 0.10
- Low °F weights: USL 0.41, NBM 0.12, ENS 0.10, IFS 0.10, HRRR 0.08, RRFS 0.07, GFS 0.06, GFS_MOS 0.06
- Wind kt weights: USL 0.23, GFS_MOS 0.14, NBM 0.14, HRRR 0.12, RRFS 0.11, GFS 0.10, IFS 0.09, ENS 0.07
- Precip in weights: GFS_MOS 0.14, NBM 0.14, HRRR 0.13, GFS 0.13, RRFS 0.13, IFS 0.12, USL 0.11, ENS 0.10

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 53.9 | 54.8 | 55.6 | 56.4 | 56.7 | 55.5 |
| ENS | 51 | Low °F | 39.6 | 40.5 | 41.6 | 42.8 | 43.4 | 41.6 |
| ENS | 51 | Wind kt | 4.3 | 4.8 | 5.3 | 6.1 | 6.5 | 5.4 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| GEFS | 31 | High °F | 52.3 | 54.0 | 55.3 | 56.4 | 57.3 | 55.2 |
| GEFS | 31 | Low °F | 43.5 | 44.0 | 44.5 | 45.4 | 46.3 | 44.7 |
| GEFS | 31 | Wind kt | 6.4 | 6.6 | 7.2 | 8.2 | 8.9 | 7.5 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 2% | 0% | 0% | 0% |
| GEFS | 3% | 0% | 0% | 0% |
| HRRRCAST | 22% | 0% | 0% | 0% |
| REFS | 0% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.00", p90 0.00"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 1% | 1% | 3% | 3% | 3% to 8% | 0.06 (8) |
| NBM | NBS P06 | 1% | 0% | 1% | 0% | 1% to 2% | 0.05 (8) |
| ENS | member fraction | 0% | 0% | 2% | 2% | 2% | 0.14 (8) |
| GEFS | member fraction | 0% | 0% | 0% | 3% | 3% | 0.13 (8) |
| HRRRCAST | member fraction | — | — | — | — | 22% | — |
| REFS | member fraction | — | — | — | — | 0% | — |
| NBM_QMD | NBM QMD | 0% | 0% | 0% | 0% | 0% | 0.05 (8) |

For reference, always forecasting the period's observed frequency (38% of 6-h blocks wet) scores Brier 0.23.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-30 06Z | Fri 01:00 | 43.5 | 40.6 | 45.6 | 46.4 | 48.0 | 45.0 | 43.0 | 44.0 | 44.5 | 47.6 |
| 10-30 07Z | Fri 02:00 | 43.4 | 40.1 |  | 45.4 |  |  |  | 44.0 | 44.1 | 47.1 |
| 10-30 08Z | Fri 03:00 | 43.1 | 40.1 |  | 45.2 |  |  |  | 44.0 | 43.8 | 46.7 |
| 10-30 09Z | Fri 04:00 | 43.0 | 39.0 | 44.1 | 44.6 | 47.6 | 43.0 | 41.0 | 43.0 | 43.4 | 46.2 |
| 10-30 10Z | Fri 05:00 | 41.6 | 40.8 |  | 42.2 |  |  |  | 42.0 | 42.7 | 45.6 |
| 10-30 11Z | Fri 06:00 | 40.2 | 38.4 |  | 41.8 |  |  |  | 41.0 | 41.8 | 45.0 |
| 10-30 12Z | Fri 07:00 | 39.3 | 37.3 | 41.3 | 41.1 | 45.0 | 41.0 | 40.0 | 41.0 | 41.6 | 44.7 |
| 10-30 13Z | Fri 08:00 | 38.2 | 36.6 |  | 40.4 |  |  |  | 40.0 | 42.4 | 44.9 |
| 10-30 14Z | Fri 09:00 | 40.2 | 40.1 |  | 42.5 |  |  |  | 42.0 | 43.9 | 45.4 |
| 10-30 15Z | Fri 10:00 | 42.9 | 43.7 | 45.3 | 45.3 | 47.4 | 45.0 | 44.0 | 45.0 | 45.7 | 46.3 |
| 10-30 16Z | Fri 11:00 | 44.9 | 45.8 |  | 48.4 |  |  |  | 48.0 | 48.0 | 48.0 |
| 10-30 17Z | Fri 12:00 | 46.8 | 48.1 |  | 51.3 |  |  |  | 51.0 | 50.8 | 50.1 |
| 10-30 18Z | Fri 13:00 | 48.4 | 50.2 | 52.9 | 53.4 | 52.9 | 53.0 | 51.0 | 53.0 | 53.0 | 51.9 |
| 10-30 19Z | Fri 14:00 | 49.6 | 52.1 |  | 55.0 |  |  |  | 55.0 | 54.5 | 53.4 |
| 10-30 20Z | Fri 15:00 | 50.6 | 52.7 |  | 55.9 |  |  |  | 56.0 | 55.4 | 54.7 |
| 10-30 21Z | Fri 16:00 | 51.0 | 53.0 | 55.7 | 56.1 | 56.2 | 55.0 | 53.0 | 56.0 | 55.4 | 55.2 |
| 10-30 22Z | Fri 17:00 | 50.2 | 52.6 |  | 55.2 |  |  |  | 55.0 | 54.1 | 54.7 |
| 10-30 23Z | Fri 18:00 | 47.4 | 51.3 |  | 51.5 |  |  |  | 52.0 | 51.8 | 53.4 |
| 10-31 00Z | Fri 19:00 | 44.8 | 50.6 | 49.6 | 49.6 | 52.5 | 51.0 | 48.0 | 51.0 | 49.9 | 52.4 |
| 10-31 01Z | Fri 20:00 | 43.2 | 47.1 |  | 48.4 |  |  |  | 49.0 | 48.9 | 51.8 |
| 10-31 02Z | Fri 21:00 | 41.9 | 45.8 |  | 47.2 |  |  |  | 48.0 | 48.2 | 51.3 |
| 10-31 03Z | Fri 22:00 | 40.9 | 43.9 | 46.6 | 46.7 | 52.5 | 47.0 | 45.0 | 47.0 | 47.6 | 51.0 |
| 10-31 04Z | Fri 23:00 | 40.0 | 42.5 |  | 47.1 |  |  |  | 46.0 | 47.2 | 50.6 |
| 10-31 05Z | Sat 00:00 | 39.3 | 41.5 |  | 47.7 |  |  |  | 45.0 | 46.8 | 50.4 |
| 10-31 06Z | Sat 01:00 | 38.7 | 40.6 | 46.4 | 47.6 | 51.1 | 49.0 | 45.0 | 44.0 | 46.5 | 50.2 |

Dewpoint (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-30 06Z | Fri 01:00 | 40.3 | 39.4 | 38.7 | 39.9 | 30.9 | 34.0 | 37.0 | 38.0 | 39.1 | 31.9 |
| 10-30 07Z | Fri 02:00 | 39.6 | 39.2 |  | 40.0 |  |  |  | 38.0 | 39.2 | 31.7 |
| 10-30 08Z | Fri 03:00 | 39.9 | 39.0 |  | 39.9 |  |  |  | 37.0 | 39.2 | 31.5 |
| 10-30 09Z | Fri 04:00 | 40.3 | 38.3 | 38.9 | 40.0 | 29.8 | 33.0 | 37.0 | 37.0 | 39.2 | 31.3 |
| 10-30 10Z | Fri 05:00 | 40.1 | 38.9 |  | 39.0 |  |  |  | 37.0 | 39.0 | 31.1 |
| 10-30 11Z | Fri 06:00 | 39.4 | 37.5 |  | 38.8 |  |  |  | 36.0 | 38.6 | 30.8 |
| 10-30 12Z | Fri 07:00 | 38.7 | 36.7 | 37.9 | 38.2 | 30.0 | 32.0 | 36.0 | 36.0 | 38.4 | 30.5 |
| 10-30 13Z | Fri 08:00 | 37.7 | 36.2 |  | 37.7 |  |  |  | 36.0 | 38.5 | 30.2 |
| 10-30 14Z | Fri 09:00 | 38.1 | 37.6 |  | 38.7 |  |  |  | 36.0 | 38.6 | 29.9 |
| 10-30 15Z | Fri 10:00 | 38.9 | 37.7 | 38.5 | 39.0 | 29.3 | 32.0 | 35.0 | 36.0 | 38.8 | 29.7 |
| 10-30 16Z | Fri 11:00 | 39.6 | 38.4 |  | 38.8 |  |  |  | 36.0 | 39.1 | 29.6 |
| 10-30 17Z | Fri 12:00 | 40.6 | 39.3 |  | 38.5 |  |  |  | 36.0 | 39.1 | 29.5 |
| 10-30 18Z | Fri 13:00 | 40.7 | 39.7 | 38.7 | 39.0 | 28.4 | 32.0 | 36.0 | 36.0 | 39.1 | 29.4 |
| 10-30 19Z | Fri 14:00 | 41.3 | 40.0 |  | 39.5 |  |  |  | 35.0 | 39.1 | 29.6 |
| 10-30 20Z | Fri 15:00 | 42.3 | 39.3 |  | 39.9 |  |  |  | 35.0 | 39.3 | 29.9 |
| 10-30 21Z | Fri 16:00 | 42.6 | 39.4 | 40.2 | 40.3 | 29.2 | 32.0 | 35.0 | 35.0 | 39.8 | 30.3 |
| 10-30 22Z | Fri 17:00 | 42.8 | 40.1 |  | 41.4 |  |  |  | 35.0 | 40.4 | 30.8 |
| 10-30 23Z | Fri 18:00 | 43.9 | 40.7 |  | 41.6 |  |  |  | 36.0 | 41.0 | 31.2 |
| 10-31 00Z | Fri 19:00 | 43.2 | 41.1 | 41.3 | 41.2 | 31.1 | 32.0 | 36.0 | 37.0 | 41.1 | 31.4 |
| 10-31 01Z | Fri 20:00 | 42.0 | 41.7 |  | 40.9 |  |  |  | 37.0 | 40.9 | 31.4 |
| 10-31 02Z | Fri 21:00 | 40.6 | 41.2 |  | 40.6 |  |  |  | 37.0 | 40.5 | 31.2 |
| 10-31 03Z | Fri 22:00 | 39.7 | 41.2 | 40.0 | 40.5 | 31.0 | 35.0 | 37.0 | 37.0 | 40.2 | 31.3 |
| 10-31 04Z | Fri 23:00 | 38.7 | 40.8 |  | 40.6 |  |  |  | 37.0 | 40.1 | 32.0 |
| 10-31 05Z | Sat 00:00 | 38.0 | 40.0 |  | 41.0 |  |  |  | 37.0 | 40.0 | 32.9 |
| 10-31 06Z | Sat 01:00 | 37.4 | 39.0 | 40.1 | 41.2 | 31.5 | 40.0 | 37.0 | 37.0 | 40.1 | 34.1 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-30 06Z | Fri 01:00 | 88 | 95 | 77 | 78 | 51 | 65 | 79 | 79 | 81 | 54 |
| 10-30 07Z | Fri 02:00 | 86 | 97 |  | 81 |  |  |  | 79 | 83 | 55 |
| 10-30 08Z | Fri 03:00 | 88 | 96 |  | 82 |  |  |  | 76 | 84 | 55 |
| 10-30 09Z | Fri 04:00 | 90 | 97 | 82 | 84 | 50 | 68 | 86 | 79 | 85 | 56 |
| 10-30 10Z | Fri 05:00 | 94 | 93 |  | 88 |  |  |  | 82 | 87 | 57 |
| 10-30 11Z | Fri 06:00 | 97 | 97 |  | 89 |  |  |  | 82 | 88 | 57 |
| 10-30 12Z | Fri 07:00 | 98 | 98 | 88 | 89 | 55 | 70 | 85 | 82 | 88 | 57 |
| 10-30 13Z | Fri 08:00 | 98 | 98 |  | 90 |  |  |  | 85 | 86 | 56 |
| 10-30 14Z | Fri 09:00 | 92 | 91 |  | 86 |  |  |  | 79 | 82 | 54 |
| 10-30 15Z | Fri 10:00 | 86 | 79 | 77 | 78 | 49 | 60 | 70 | 71 | 77 | 52 |
| 10-30 16Z | Fri 11:00 | 82 | 75 |  | 69 |  |  |  | 63 | 71 | 49 |
| 10-30 17Z | Fri 12:00 | 79 | 71 |  | 61 |  |  |  | 56 | 64 | 45 |
| 10-30 18Z | Fri 13:00 | 75 | 67 | 58 | 58 | 39 | 45 | 56 | 52 | 59 | 42 |
| 10-30 19Z | Fri 14:00 | 73 | 63 |  | 56 |  |  |  | 47 | 56 | 40 |
| 10-30 20Z | Fri 15:00 | 73 | 60 |  | 55 |  |  |  | 45 | 55 | 39 |
| 10-30 21Z | Fri 16:00 | 73 | 60 | 56 | 55 | 35 | 41 | 50 | 45 | 55 | 39 |
| 10-30 22Z | Fri 17:00 | 76 | 62 |  | 60 |  |  |  | 47 | 60 | 40 |
| 10-30 23Z | Fri 18:00 | 88 | 67 |  | 69 |  |  |  | 54 | 66 | 43 |
| 10-31 00Z | Fri 19:00 | 94 | 70 | 73 | 73 | 44 | 48 | 63 | 59 | 72 | 45 |
| 10-31 01Z | Fri 20:00 | 95 | 81 |  | 75 |  |  |  | 63 | 74 | 46 |
| 10-31 02Z | Fri 21:00 | 95 | 84 |  | 78 |  |  |  | 66 | 75 | 46 |
| 10-31 03Z | Fri 22:00 | 95 | 90 | 78 | 79 | 44 | 63 | 73 | 68 | 75 | 47 |
| 10-31 04Z | Fri 23:00 | 95 | 94 |  | 78 |  |  |  | 71 | 77 | 49 |
| 10-31 05Z | Sat 00:00 | 95 | 94 |  | 77 |  |  |  | 73 | 78 | 51 |
| 10-31 06Z | Sat 01:00 | 95 | 94 | 79 | 78 | 47 | 71 | 73 | 76 | 79 | 54 |

Wind speed (kt) at the hour:

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-30 06Z | Fri 01:00 | 2.8 | 2.4 |  | 2.1 | 2.5 | 4.0 | 0.0 | 3.0 | 2.2 | 2.2 |
| 10-30 07Z | Fri 02:00 | 3.2 | 3.3 |  | 2.0 |  |  |  | 4.0 | 2.1 | 2.3 |
| 10-30 08Z | Fri 03:00 | 2.7 | 1.7 |  | 2.5 |  |  |  | 4.0 | 2.2 | 2.6 |
| 10-30 09Z | Fri 04:00 | 2.7 | 2.4 |  | 2.6 | 3.1 | 4.0 | 1.0 | 4.0 | 2.4 | 3.0 |
| 10-30 10Z | Fri 05:00 | 2.8 | 2.5 |  | 2.3 |  |  |  | 5.0 | 2.7 | 3.4 |
| 10-30 11Z | Fri 06:00 | 2.6 | 1.9 |  | 3.6 |  |  |  | 5.0 | 3.1 | 3.8 |
| 10-30 12Z | Fri 07:00 | 3.2 | 3.2 |  | 4.1 | 3.6 | 5.0 | 4.0 | 5.0 | 3.4 | 4.1 |
| 10-30 13Z | Fri 08:00 | 3.3 | 3.6 |  | 3.9 |  |  |  | 5.0 | 3.6 | 4.4 |
| 10-30 14Z | Fri 09:00 | 3.0 | 3.2 |  | 4.2 |  |  |  | 6.0 | 3.8 | 4.7 |
| 10-30 15Z | Fri 10:00 | 4.4 | 5.9 | 3.9 | 4.0 | 4.2 | 6.0 | 5.0 | 6.0 | 4.0 | 5.0 |
| 10-30 16Z | Fri 11:00 | 4.8 | 5.8 |  | 4.4 |  |  |  | 6.0 | 4.1 | 5.2 |
| 10-30 17Z | Fri 12:00 | 4.8 | 5.9 |  | 4.6 |  |  |  | 7.0 | 4.2 | 5.4 |
| 10-30 18Z | Fri 13:00 | 4.7 | 5.3 | 3.9 | 4.3 | 5.0 | 7.0 | 6.0 | 7.0 | 4.3 | 5.7 |
| 10-30 19Z | Fri 14:00 | 4.5 | 5.4 |  | 4.5 |  |  |  | 7.0 | 4.5 | 5.9 |
| 10-30 20Z | Fri 15:00 | 4.5 | 5.2 |  | 4.7 |  |  |  | 7.0 | 4.7 | 6.1 |
| 10-30 21Z | Fri 16:00 | 4.3 | 5.4 |  | 5.0 | 5.7 | 7.0 | 7.0 | 7.0 | 4.9 | 6.3 |
| 10-30 22Z | Fri 17:00 | 4.0 | 4.9 |  | 4.3 |  |  |  | 7.0 | 4.9 | 6.3 |
| 10-30 23Z | Fri 18:00 | 3.7 | 3.6 |  | 4.1 |  |  |  | 7.0 | 4.8 | 6.2 |
| 10-31 00Z | Fri 19:00 | 3.8 | 4.7 |  | 4.8 | 5.3 | 8.0 | 7.0 | 6.0 | 4.8 | 6.2 |
| 10-31 01Z | Fri 20:00 | 3.8 | 3.4 |  | 4.9 |  |  |  | 6.0 | 4.9 | 6.4 |
| 10-31 02Z | Fri 21:00 | 3.7 | 4.6 |  | 4.9 |  |  |  | 6.0 | 5.0 | 6.7 |
| 10-31 03Z | Fri 22:00 | 3.6 | 2.2 | 4.6 | 4.7 | 6.1 | 6.0 | 6.0 | 6.0 | 5.1 | 6.9 |
| 10-31 04Z | Fri 23:00 | 3.6 | 3.7 |  | 4.7 |  |  |  | 6.0 | 5.1 | 7.1 |
| 10-31 05Z | Sat 00:00 | 3.5 | 4.2 |  | 4.6 |  |  |  | 6.0 | 4.9 | 7.1 |
| 10-31 06Z | Sat 01:00 | 3.6 | 4.0 | 4.2 | 4.6 | 5.9 | 6.0 | 6.0 | 6.0 | 4.8 | 7.2 |

Precipitation (in), accumulated since the start of the day (06Z): 0.00 in every model (HRRR, RRFS, IFS, IFS_HRES, GFS, USL, ENS, GEFS) all day.

Total cloud cover (%):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-30 06Z | Fri 01:00 | 100 | 18 | 56 | 95 | 96 | 0 | 63 | 77 | 73 | 60 |
| 10-30 07Z | Fri 02:00 | 100 | 100 |  | 95 |  |  | 67 | 87 | 74 | 61 |
| 10-30 08Z | Fri 03:00 | 100 | 80 |  | 92 |  |  | 42 | 93 | 74 | 59 |
| 10-30 09Z | Fri 04:00 | 100 | 100 | 81 | 3 | 58 | 0 | 41 | 94 | 72 | 58 |
| 10-30 10Z | Fri 05:00 | 44 | 100 |  | 40 |  |  | 31 | 80 | 70 | 61 |
| 10-30 11Z | Fri 06:00 | 14 | 1 |  | 55 |  |  | 27 | 53 | 66 | 66 |
| 10-30 12Z | Fri 07:00 | 8 | 3 | 81 | 69 | 5 | 0 | 20 | 34 | 63 | 69 |
| 10-30 13Z | Fri 08:00 | 9 | 32 |  | 77 |  |  | 23 | 42 | 61 | 66 |
| 10-30 14Z | Fri 09:00 | 100 | 95 |  | 73 |  |  | 42 | 65 | 59 | 61 |
| 10-30 15Z | Fri 10:00 | 100 | 100 | 73 | 70 | 100 | 19 | 35 | 77 | 60 | 60 |
| 10-30 16Z | Fri 11:00 | 100 | 100 |  | 69 |  |  | 51 | 67 | 67 | 67 |
| 10-30 17Z | Fri 12:00 | 100 | 100 |  | 95 |  |  | 51 | 49 | 76 | 79 |
| 10-30 18Z | Fri 13:00 | 100 | 100 | 86 | 97 | 100 | 44 | 46 | 43 | 80 | 88 |
| 10-30 19Z | Fri 14:00 | 100 | 100 |  | 81 |  |  |  | 49 | 72 | 90 |
| 10-30 20Z | Fri 15:00 | 100 | 100 |  | 70 |  |  |  | 55 | 58 | 90 |
| 10-30 21Z | Fri 16:00 | 100 | 56 | 39 | 7 | 20 | 75 | 29 | 60 | 49 | 89 |
| 10-30 22Z | Fri 17:00 | 100 | 78 |  | 0 |  |  |  | 59 | 46 | 84 |
| 10-30 23Z | Fri 18:00 | 90 | 55 |  | 2 |  |  |  | 52 | 48 | 78 |
| 10-31 00Z | Fri 19:00 | 12 | 71 | 5 | 20 | 76 | 100 | 12 | 49 | 51 | 76 |
| 10-31 01Z | Fri 20:00 | 12 | 100 |  | 38 |  |  |  | 51 | 56 | 79 |
| 10-31 02Z | Fri 21:00 | 100 | 100 |  | 99 |  |  |  | 56 | 63 | 86 |
| 10-31 03Z | Fri 22:00 | 100 | 100 | 91 | 94 | 100 | 100 | 43 | 57 | 68 | 92 |
| 10-31 04Z | Fri 23:00 | 100 | 100 |  | 99 |  |  |  | 56 | 68 | 93 |
| 10-31 05Z | Sat 00:00 | 100 | 100 |  | 91 |  |  |  | 54 | 66 | 92 |
| 10-31 06Z | Sat 01:00 | 100 | 57 | 62 | 59 | 100 | 100 | 61 | 52 | 66 | 93 |

## Track record this period

Since 2026-10-12 at KMSP (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-27 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 17 | 6.6 | -1.2 | +0.0 | -2.4 | +0.05 | 2.1 | 1.0 | 2.9 | 0.09 |
| NBM | 17 | 7.8 | -0.8 | +0.2 | -4.5 | +0.02 | 2.3 | 1.2 | 4.6 | 0.06 |
| GFS_MOS | 17 | 8.7 | -1.2 | +0.4 | -4.2 | +0.02 | 2.6 | 2.8 | 4.4 | 0.05 |
| USL | 2 | 9.2 | -2.0 | +0.0 | -1.5 | +0.21 | 2.0 | 0.0 | 2.5 | 0.21 |
| HRRR | 17 | 9.3 | -2.5 | -2.0 | -5.4 | +0.04 | 2.8 | 2.2 | 5.4 | 0.09 |
| RRFS | 17 | 9.5 | -1.1 | -1.4 | -5.9 | +0.04 | 2.1 | 2.5 | 5.9 | 0.10 |
| GFS | 17 | 10.4 | -0.9 | +2.6 | -6.5 | +0.05 | 2.2 | 2.8 | 6.5 | 0.08 |
| IFS | 17 | 11.5 | -1.6 | +0.0 | -7.1 | +0.08 | 3.2 | 1.6 | 7.1 | 0.14 |
| IFS_HRES | 17 | 11.6 | -1.3 | +0.7 | -6.9 | +0.10 | 3.3 | 1.8 | 6.9 | 0.15 |
| GEFS | 2 | 14.7 | -4.0 | +0.5 | -8.6 | +0.21 | 4.0 | 0.5 | 8.6 | 0.21 |
| ENS | 2 | 15.8 | -2.6 | -0.6 | -9.1 | +0.27 | 2.6 | 1.5 | 9.1 | 0.27 |

## Daily verification (all 17 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 1.9 | 10.0 | 7.3 | 9.4 | 8.1 | 13.0 | 9.0 | — | — | — | 6.9 | HRRR |
| 10-13 h | 5.3 | 5.8 | 12.3 | 15.1 | 11.7 | 8.2 | 12.2 | — | — | — | 8.9 | HRRR |
| 10-14 h | 6.4 | 8.0 | 12.5 | 13.5 | 7.5 | 7.5 | 8.0 | — | — | — | 2.0 | CONSENSUS |
| 10-15 h | 12.5 | 13.5 | 19.6 | 16.8 | 8.1 | 10.0 | 14.0 | — | — | — | 9.2 | GFS |
| 10-16 h | 16.3 | 10.1 | 6.5 | 7.9 | 12.0 | 4.8 | 7.0 | — | — | — | 8.8 | GFS_MOS |
| 10-17 h | 10.0 | 10.0 | 8.0 | 7.0 | 12.0 | 5.0 | 6.5 | — | — | — | 5.0 | GFS_MOS |
| 10-18 h | 13.5 | 9.5 | 15.5 | 14.5 | 6.5 | 14.0 | 11.5 | — | — | — | 10.5 | GFS |
| 10-19 h | 5.0 | 6.0 | 8.0 | 7.0 | 9.0 | 4.0 | 6.5 | — | — | — | 2.0 | CONSENSUS |
| 10-20 h | 8.5 | 7.0 | 9.0 | 7.5 | 8.5 | 5.0 | 8.5 | — | — | — | 3.0 | CONSENSUS |
| 10-21 h | 7.5 | 8.0 | 8.5 | 9.5 | 9.0 | 5.5 | 5.0 | — | — | — | 3.5 | CONSENSUS |
| 10-22 h | 2.5 | 6.0 | 6.0 | 5.5 | 7.5 | 8.5 | 2.5 | — | — | — | 2.5 | HRRR |
| 10-23 h | 9.0 | 8.9 | 11.7 | 8.1 | 14.3 | 5.0 | 5.5 | — | — | — | 4.1 | CONSENSUS |
| 10-24 h | 9.0 | 8.3 | 17.1 | 13.2 | 13.8 | 11.5 | 6.8 | — | — | — | 8.2 | NBM |
| 10-25 h | 11.5 | 7.2 | 8.9 | 10.4 | 12.3 | 9.7 | 3.5 | — | — | — | 6.3 | NBM |
| 10-26 h | 8.7 | 9.3 | 6.8 | 9.4 | 6.7 | 5.7 | 3.7 | — | — | — | 4.7 | NBM |
| 10-27 | 14.3 | 9.6 | 11.0 | 14.2 | 13.3 | 10.9 | 8.5 | 4.9 | 8.2 | 8.5 | 7.7 | USL |
| 10-28 | 16.4 | 23.6 | 27.5 | 28.1 | 16.4 | 18.7 | 14.6 | 13.5 | 23.4 | 20.9 | 18.5 | USL |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 81 | +0 | +4 | +1 | +2 | +2 | -4 | +3 | — | — | — | +1 |
| 10-13 h | 57 | +0 | +2 | +5 | +5 | +8 | +5 | +8 | — | — | — | +5 |
| 10-14 h | 55 | -3 | +3 | +6 | +6 | +5 | +5 | +5 | — | — | — | -1 |
| 10-15 h | 51 | +2 | +2 | +4 | +3 | +1 | +5 | +4 | — | — | — | +2 |
| 10-16 h | 53 | -6 | -1 | -1 | -2 | -1 | -2 | -1 | — | — | — | -4 |
| 10-17 h | 60 | -4 | -3 | -2 | -1 | +1 | -1 | -4 | — | — | — | -3 |
| 10-18 h | 70 | -4 | -3 | -9 | -8 | -2 | -7 | -8 | — | — | — | -6 |
| 10-19 h | 66 | -1 | +0 | -5 | -4 | +0 | +0 | -4 | — | — | — | -1 |
| 10-20 h | 69 | -2 | +0 | -3 | -3 | -1 | -1 | -3 | — | — | — | -1 |
| 10-21 h | 74 | -2 | -2 | -6 | -6 | -2 | -1 | -3 | — | — | — | -2 |
| 10-22 h | 75 | -1 | +1 | -3 | -3 | +0 | -1 | -1 | — | — | — | +0 |
| 10-23 h | 76 | -2 | +0 | -2 | -2 | -4 | -1 | -2 | — | — | — | -1 |
| 10-24 h | 75 | -1 | +0 | -2 | -2 | -2 | -4 | +0 | — | — | — | -1 |
| 10-25 h | 55 | +0 | -1 | +3 | +4 | +1 | +2 | +0 | — | — | — | +1 |
| 10-26 h | 49 | +1 | +1 | +0 | +2 | -1 | -1 | +0 | — | — | — | +1 |
| 10-27 | 61 | -8 | -6 | -2 | -2 | -5 | -3 | +1 | -2 | +0 | -3 | -3 |
| 10-28 | 72 | -6 | -5 | -4 | -4 | -3 | -4 | -2 | -2 | -5 | -5 | -4 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 55 | +0 | +4 | +3 | +4 | +2 | +6 | +4 | — | — | — | +3 |
| 10-13 h | 53 | -2 | +0 | -2 | -2 | +0 | +0 | +1 | — | — | — | -1 |
| 10-14 h | 46 | +1 | -3 | +4 | +5 | +0 | -1 | +1 | — | — | — | +0 |
| 10-15 h | 45 | +0 | +1 | +3 | +3 | +0 | +1 | +1 | — | — | — | +0 |
| 10-16 h | 40 | -5 | -3 | +0 | +0 | +4 | +0 | -2 | — | — | — | -1 |
| 10-17 h | 36 | -2 | -3 | +1 | +1 | +7 | -2 | +0 | — | — | — | +0 |
| 10-18 h | 48 | -7 | -4 | -3 | -3 | +2 | -6 | -2 | — | — | — | -4 |
| 10-19 h | 44 | -2 | -4 | -1 | -1 | +7 | +3 | +1 | — | — | — | +1 |
| 10-20 h | 46 | -4 | -4 | -2 | -1 | +4 | +2 | -3 | — | — | — | -1 |
| 10-21 h | 48 | -4 | -5 | +1 | +2 | +6 | +3 | +1 | — | — | — | +1 |
| 10-22 h | 49 | -1 | -4 | -2 | -2 | +7 | +7 | -1 | — | — | — | +1 |
| 10-23 h | 56 | -4 | -3 | +1 | +1 | +4 | +1 | +1 | — | — | — | +0 |
| 10-24 h | 51 | -2 | +3 | +1 | +1 | +3 | +4 | +3 | — | — | — | +2 |
| 10-25 h | 48 | -3 | -2 | +1 | +2 | +2 | -3 | +0 | — | — | — | -1 |
| 10-26 h | 42 | +1 | +2 | +2 | +3 | +0 | -3 | +1 | — | — | — | +1 |
| 10-27 | 44 | +0 | +0 | +0 | +1 | -1 | -3 | -1 | +0 | +1 | +0 | +0 |
| 10-28 | 51 | -1 | -1 | -3 | -1 | +0 | +1 | +0 | +0 | -2 | +1 | -1 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 15 | -3 | -4 | -5 | -6 | -5 | -6 | -4 | — | — | — | -5 |
| 10-13 h | 14 | -5 | -6 | -5 | -4 | -5 | -4 | -4 | — | — | — | -5 |
| 10-14 h | 12 | -4 | -4 | -5 | -5 | -5 | -3 | -4 | — | — | — | -2 |
| 10-15 h | 15 | -3 | -3 | -3 | -3 | -4 | +1 | +0 | — | — | — | +0 |
| 10-16 h | 26 | -9 | -9 | -11 | -11 | -10 | -4 | -8 | — | — | — | -6 |
| 10-17 h | 20 | -8 | -8 | -10 | -10 | -8 | -4 | -5 | — | — | — | -4 |
| 10-18 h | 17 | -5 | -5 | -7 | -7 | -5 | -2 | -3 | — | — | — | -1 |
| 10-19 h | 9 | -4 | -4 | -4 | -4 | -4 | -2 | -3 | — | — | — | +0 |
| 10-20 h | 15 | -5 | -6 | -8 | -7 | -7 | -4 | -5 | — | — | — | -2 |
| 10-21 h | 8 | -3 | -2 | -3 | -3 | -2 | -3 | -2 | — | — | — | +1 |
| 10-22 h | 7 | -1 | -2 | -2 | -1 | -1 | +1 | +1 | — | — | — | +3 |
| 10-23 h | 19 | -6 | -7 | -7 | -7 | -7 | -6 | -5 | — | — | — | -3 |
| 10-24 h | 20 | -8 | -9 | -10 | -10 | -9 | -7 | -6 | — | — | — | -4 |
| 10-25 h | 14 | -4 | -6 | -9 | -8 | -8 | -7 | -7 | — | — | — | -3 |
| 10-26 h | 15 | -5 | -4 | -6 | -6 | -6 | -3 | -3 | — | — | — | +0 |
| 10-27 | 17 | -6 | -6 | -7 | -7 | -8 | -5 | -4 | +1 | -5 | -5 | -2 |
| 10-28 | 23 | -11 | -13 | -15 | -15 | -13 | -10 | -11 | -4 | -13 | -12 | -8 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 0.00 | +0.01 | +0.00 | +0.02 | +0.01 | +0.04 | +0.00 | +0.00 | — | — | — | +0.01 |
| 10-13 h | 0.03 | -0.02 | -0.02 | +0.07 | +0.18 | -0.03 | -0.03 | -0.03 | — | — | — | -0.01 |
| 10-14 h | 0.00 | +0.01 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-15 h | 0.69 | -0.51 | -0.51 | -0.58 | -0.52 | -0.35 | -0.27 | -0.51 | — | — | — | -0.45 |
| 10-16 h | 0.07 | +0.02 | -0.04 | +0.00 | -0.01 | -0.05 | -0.02 | +0.00 | — | — | — | -0.02 |
| 10-17 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-18 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-19 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-20 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-21 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-22 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-23 h | 0.00 | +0.00 | +0.06 | +0.14 | +0.04 | +0.07 | +0.00 | +0.00 | — | — | — | +0.04 |
| 10-24 h | 0.00 | +0.05 | +0.02 | +0.28 | +0.14 | +0.11 | +0.00 | +0.02 | — | — | — | +0.08 |
| 10-25 h | 0.02 | +0.19 | +0.03 | -0.01 | -0.01 | +0.15 | +0.03 | +0.00 | — | — | — | +0.07 |
| 10-26 h | 0.38 | +0.30 | +0.31 | +0.09 | +0.07 | +0.15 | +0.01 | +0.06 | — | — | — | +0.15 |
| 10-27 | 0.14 | +0.11 | -0.02 | +0.22 | +0.33 | +0.11 | +0.08 | +0.17 | +0.08 | +0.18 | +0.10 | +0.13 |
| 10-28 | 0.04 | +0.11 | +0.42 | +0.57 | +0.83 | +0.21 | +0.30 | +0.22 | +0.34 | +0.36 | +0.31 | +0.34 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 17 | +12 | 13 | +9 | 10 |
| RRFS | 17 | +3 | 8 | +8 | 12 |
| IFS | 17 | -8 | 18 | -3 | 7 |
| IFS_HRES | 17 | -7 | 19 | -2 | 8 |
| GFS | 17 | +0 | 21 | +2 | 11 |
| GFS_MOS | 17 | -2 | 3 | +4 | 13 |
| NBM | 17 | -5 | 13 | -6 | 10 |
| USL | 2 | -20 | 20 | -8 | 8 |
| ENS | 2 | -46 | 46 | -22 | 22 |
| GEFS | 2 | -36 | 36 | -9 | 9 |

Night clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 46% | — | +43 | +9 | -11 | +10 | +23 | -9 | +10 | — | — | — |
| 10-13 h | 100% | — | +0 | -5 | +0 | -1 | +0 | +0 | -20 | — | — | — |
| 10-14 h | 100% | — | +0 | +0 | -3 | -4 | -100 | -11 | -32 | — | — | — |
| 10-15 h | 92% | — | +8 | +8 | +2 | +4 | +8 | -8 | -8 | — | — | — |
| 10-16 h | 100% | — | +0 | -7 | -6 | -11 | +0 | +0 | -14 | — | — | — |
| 10-17 h | 0% | — | +3 | +0 | +0 | +0 | +5 | +0 | +7 | — | — | — |
| 10-18 h | 0% | — | +4 | +0 | +4 | +7 | +26 | +0 | +5 | — | — | — |
| 10-19 h | 0% | — | +84 | +76 | +54 | +52 | +74 | +0 | +32 | — | — | — |
| 10-20 h | 0% | — | +3 | +2 | +0 | +1 | +0 | +0 | +3 | — | — | — |
| 10-21 h | 0% | — | +0 | +0 | +6 | +7 | +3 | +0 | +2 | — | — | — |
| 10-22 h | 0% | — | +48 | +10 | +27 | +29 | +17 | +0 | +17 | — | — | — |
| 10-23 h | 23% | — | +46 | +0 | -21 | -22 | +19 | -18 | +6 | — | — | — |
| 10-24 h | 53% | — | -6 | +3 | -22 | -25 | +18 | +6 | -2 | — | — | — |
| 10-25 h | 100% | — | +0 | -3 | +0 | +0 | +0 | +0 | -14 | — | — | — |
| 10-26 h | 100% | 100% | +0 | +0 | +0 | +0 | +0 | +0 | -12 | — | — | — |
| 10-27 | 100% | 100% | -4 | -17 | -6 | -14 | +0 | +0 | -17 | +0 | -8 | -2 |
| 10-28 | 100% | 100% | +0 | +0 | -85 | -77 | -70 | +0 | -25 | -38 | -82 | -68 |

Day clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 28% | — | +66 | +34 | +41 | +43 | -5 | +27 | +12 | — | — | — |
| 10-13 h | 96% | — | +4 | +1 | -11 | -18 | -69 | -18 | -24 | — | — | — |
| 10-14 h | 80% | — | +20 | -11 | -48 | -50 | -30 | -32 | -26 | — | — | — |
| 10-15 h | 100% | — | +0 | +0 | +0 | +0 | +0 | +0 | -11 | — | — | — |
| 10-16 h | 54% | — | +7 | -19 | -17 | -13 | -18 | +3 | -10 | — | — | — |
| 10-17 h | 0% | — | +2 | +0 | +0 | +0 | +2 | +0 | +3 | — | — | — |
| 10-18 h | 24% | — | +31 | +3 | +21 | +16 | -11 | -17 | -3 | — | — | — |
| 10-19 h | 47% | — | +27 | +13 | -9 | +6 | +2 | -42 | -11 | — | — | — |
| 10-20 h | 0% | — | +1 | +1 | +0 | +0 | +0 | +2 | +5 | — | — | — |
| 10-21 h | 9% | — | -8 | +0 | -7 | -7 | +16 | +16 | -4 | — | — | — |
| 10-22 h | 0% | — | +2 | +70 | +0 | +0 | +18 | +30 | +12 | — | — | — |
| 10-23 h | 68% | — | +17 | +19 | -7 | +4 | +32 | +2 | -13 | — | — | — |
| 10-24 h | 46% | — | +12 | +27 | +0 | +6 | +19 | +24 | +6 | — | — | — |
| 10-25 h | 96% | — | +2 | +3 | +0 | -1 | +4 | +4 | -8 | — | — | — |
| 10-26 h | 100% | 100% | +0 | +0 | +0 | +0 | +0 | +0 | -10 | — | — | — |
| 10-27 | 100% | 100% | +0 | -4 | +0 | -2 | +0 | +0 | -19 | -1 | -25 | -4 |
| 10-28 | 74% | 77% | +12 | -1 | -11 | -15 | -1 | +26 | -4 | -15 | -19 | -13 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 17 | +0.0 | 1.5 | +1.2 | 1.7 |
| RRFS | 17 | -0.1 | 1.6 | +0.8 | 1.1 |
| IFS | 17 | +1.3 | 2.2 | +1.9 | 2.3 |
| IFS_HRES | 17 | +1.5 | 2.1 | +2.0 | 2.7 |
| GFS | 17 | -1.4 | 2.4 | -2.4 | 2.5 |
| GFS_MOS | 17 | -0.1 | 1.9 | +0.0 | 2.0 |
| NBM | 17 | +0.7 | 1.3 | +0.0 | 1.2 |
| USL | 2 | -0.3 | 0.4 | -0.8 | 0.8 |
| ENS | 2 | +0.6 | 1.9 | +0.9 | 0.9 |
| GEFS | 2 | -2.6 | 2.6 | -2.5 | 2.5 |

Night dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 56.3 | +3.1 | +3.0 | +5.3 | +5.7 | +2.1 | +1.7 | +1.4 | — | — | — |
| 10-13 h | 49.5 | -1.1 | +1.7 | +0.5 | +1.0 | -1.1 | +1.5 | +2.2 | — | — | — |
| 10-14 h | 43.9 | -0.4 | -3.0 | -2.1 | -2.3 | -4.1 | -2.6 | -1.2 | — | — | — |
| 10-15 h | 43.9 | +0.2 | -0.6 | +0.8 | +1.4 | -3.1 | -0.2 | +0.4 | — | — | — |
| 10-16 h | 43.0 | -0.1 | -1.2 | -2.9 | -2.2 | -4.3 | -6.0 | -1.5 | — | — | — |
| 10-17 h | 30.3 | +3.1 | +2.5 | +3.8 | +3.8 | -10.9 | -5.3 | +0.2 | — | — | — |
| 10-18 h | 32.7 | +4.6 | +0.8 | +2.6 | +2.6 | -2.7 | -0.7 | +3.0 | — | — | — |
| 10-19 h | 36.8 | +3.1 | +4.2 | +5.2 | +5.2 | +0.7 | +2.9 | +5.6 | — | — | — |
| 10-20 h | 42.7 | +0.5 | -0.1 | +0.9 | +1.0 | -1.8 | -0.4 | -0.3 | — | — | — |
| 10-21 h | 40.8 | -1.3 | -0.3 | +5.0 | +5.1 | +2.0 | +3.5 | +2.2 | — | — | — |
| 10-22 h | 48.3 | -0.7 | -1.1 | -0.8 | -0.5 | -0.7 | +2.7 | -1.3 | — | — | — |
| 10-23 h | 52.2 | -0.5 | +0.6 | +2.5 | +2.5 | +2.0 | +0.8 | +1.2 | — | — | — |
| 10-24 h | 48.9 | -1.8 | +0.3 | +1.6 | +1.5 | -0.8 | +1.8 | -0.9 | — | — | — |
| 10-25 h | 40.7 | +1.2 | +2.4 | -0.1 | +0.1 | +2.4 | +1.0 | +0.3 | — | — | — |
| 10-26 h | 35.2 | -3.8 | -3.9 | +1.2 | +0.7 | -3.7 | -1.2 | -0.2 | — | — | — |
| 10-27 | 41.6 | +0.6 | +0.0 | +2.6 | +3.0 | -1.9 | -2.3 | +1.4 | +0.1 | +2.7 | -3.8 |
| 10-28 | 50.7 | -0.6 | -2.3 | -2.2 | -1.3 | -1.3 | -0.4 | +0.6 | -0.7 | -1.2 | -1.5 |

Day dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-12 h | 58.1 | +1.7 | +2.2 | +1.9 | +3.5 | -0.2 | +0.7 | -0.7 | — | — | — |
| 10-13 h | 46.4 | +1.0 | +1.2 | -0.9 | -0.9 | -2.5 | +0.6 | +0.4 | — | — | — |
| 10-14 h | 41.2 | -0.6 | -2.1 | -2.8 | -2.8 | -2.4 | -0.2 | -2.3 | — | — | — |
| 10-15 h | 46.6 | +0.0 | -0.9 | -0.9 | +0.5 | -1.4 | -2.9 | +0.4 | — | — | — |
| 10-16 h | 31.7 | +2.5 | -0.6 | +0.8 | +1.0 | -5.8 | +1.1 | +1.0 | — | — | — |
| 10-17 h | 28.0 | +9.4 | +5.9 | +6.8 | +6.5 | -6.9 | -3.4 | +2.8 | — | — | — |
| 10-18 h | 36.2 | +3.5 | +0.9 | +4.7 | +4.6 | -5.6 | -1.4 | +3.3 | — | — | — |
| 10-19 h | 41.2 | +3.1 | +1.9 | +5.1 | +5.2 | -2.2 | -1.2 | +2.3 | — | — | — |
| 10-20 h | 41.7 | +1.9 | +0.1 | +4.3 | +4.0 | -2.6 | +0.9 | -0.1 | — | — | — |
| 10-21 h | 47.1 | +1.0 | +1.5 | +3.7 | +4.1 | -1.7 | +1.3 | +0.1 | — | — | — |
| 10-22 h | 52.7 | -0.1 | +0.0 | +0.3 | +0.9 | -1.4 | -0.1 | -2.1 | — | — | — |
| 10-23 h | 49.3 | -1.4 | +0.5 | +1.5 | +1.3 | +0.8 | +3.8 | -0.7 | — | — | — |
| 10-24 h | 49.8 | -1.3 | +0.4 | +3.2 | +2.9 | +0.1 | +0.8 | -0.7 | — | — | — |
| 10-25 h | 32.0 | +3.3 | +1.7 | -0.7 | -2.8 | -2.7 | +5.6 | +0.8 | — | — | — |
| 10-26 h | 38.1 | -0.1 | +1.5 | +0.7 | +1.5 | -5.5 | -3.1 | -2.1 | — | — | — |
| 10-27 | 48.1 | +0.6 | +0.1 | +3.9 | +4.6 | -0.6 | -2.2 | +0.4 | -0.8 | +1.5 | -2.3 |
| 10-28 | 56.2 | +0.6 | -0.1 | +0.1 | +0.5 | -2.0 | -1.6 | -0.7 | -0.8 | +0.3 | -2.7 |

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| 10-27 | 0.14" (wet: 06-12) | 73/46/3/1 | 87/52/5/5 | 100/94/24/14 | 97/90/6/6 | 24h 100% | 24h 100% | 83/52/3/4 |
| 10-28 | 0.04" (wet: 18-00, 00-06) | 0/9/87/63 | 8/16/79/78 | 4/39/98/98 | 0/42/100/97 | 24h 100% | 24h 100% | 8/16/79/78 |

## Today so far (2026-10-29, through 2026-10-29T16:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 52.0 °F, low 44.1 °F, max wind 13 kt, precip 0.00" (11 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 28/18Z | -1.9 | 1.9 | 51 (-1) | 40 (-4) pending | -1.4 | 0.00 | +0.00 |
| RRFS | 28/18Z | -1.2 | 1.5 | 52 (+0) pending | 43 (-1) | -0.7 | 0.00 | +0.00 |
| IFS | 28/12Z | -1.0 | 1.0 | 55 (+3) pending | 43 (-1) | -1.6 | 0.00 | +0.00 |
| IFS_HRES | 28/12Z | -0.8 | 1.0 | 55 (+3) pending | 44 (-1) | -1.7 | 0.00 | +0.00 |
| GFS | 28/18Z | +1.4 | 1.7 | 57 (+5) pending | 45 (+1) | -0.1 | 0.00 | +0.00 |
| GFS_MOS | 28/18Z | +2.9 | 2.9 | 58 (+6) | 46 (+2) | +0.9 | — | — |
| NBM | 28/23Z | -1.7 | 1.7 | 56 (+4) | 42 (-2) | -0.2 | — | — |
| USL | 28/22Z | +1.0 | 1.3 | 58 (+6) pending | 43 (-1) | +0.3 | 0.00 | +0.00 |
| ENS | 28/06Z | -1.3 | 1.3 | 55 (+3) pending | 43 (-1) | -1.3 | 0.00 | +0.00 |
| GEFS | 28/18Z | +1.8 | 2.1 | 57 (+5) pending | 47 (+3) | +0.5 | 0.00 | +0.00 |

## Clouds so far today (2026-10-29, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-19 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (CDT) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-29 06Z | Thu 01:00 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 10 | 66 | 0 | 2 |
| 10-29 07Z | Thu 02:00 | 0 | 0 | 0 | 0 |  | 0 |  |  | 11 | 58 | 0 | 0 |
| 10-29 08Z | Thu 03:00 | 0 | 0 | 0 | 0 |  | 0 |  |  | 9 | 52 | 0 | 0 |
| 10-29 09Z | Thu 04:00 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 12 | 48 | 0 | 0 |
| 10-29 10Z | Thu 05:00 | 0 | 0 | 1 | 0 |  | 0 |  |  | 11 | 38 | 0 | 0 |
| 10-29 11Z | Thu 06:00 | 0 | 0 | 1 | 0 |  | 0 |  |  | 7 | 23 | 0 | 0 |
| 10-29 12Z | Thu 07:00 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 13 | 0 | 0 |
| 10-29 13Z | Thu 08:00 | 0 | 0 | 1 | 0 |  | 0 |  |  | 2 | 11 | 1 | 0 |
| 10-29 14Z | Thu 09:00 | 0 | 0 | 0 | 0 |  | 0 |  |  | 1 | 10 | 1 | 0 |
| 10-29 15Z | Thu 10:00 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0 |
| 10-29 16Z | Thu 11:00 | 0 | 0 | 12 | 6 |  | 0 |  |  | 4 | 5 | 1 | 0 |
| 10-29 17Z | Thu 12:00 | 0 | 0 | 13 | 5 |  | 0 |  |  | 3 | 2 | 1 | 0 |

## Dewpoint so far today (2026-10-29, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (CDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-29 07Z | Thu 02:00 | 45.0 | 83 | 47.1 | 47.3 |  |  |  |  | 47.0 | 46.4 | 39.9 |
| 10-29 08Z | Thu 03:00 | 45.0 | 86 | 45.7 | 46.5 |  |  |  |  | 46.0 | 44.7 | 39.0 |
| 10-29 09Z | Thu 04:00 | 44.1 | 86 | 45.2 | 44.9 | 42.9 | 39.9 | 45.0 | 42.0 | 44.0 | 43.2 | 38.3 |
| 10-29 10Z | Thu 05:00 | 43.0 | 89 | 44.2 | 44.7 |  |  |  |  | 43.0 | 42.1 | 37.3 |
| 10-29 11Z | Thu 06:00 | 42.1 | 90 | 42.6 | 42.9 |  |  |  |  | 41.0 | 41.1 | 36.5 |
| 10-29 12Z | Thu 07:00 | 41.0 | 86 | 41.0 | 40.6 | 41.1 | 37.1 | 41.0 | 40.0 | 41.0 | 40.4 | 35.8 |
| 10-29 13Z | Thu 08:00 | 39.9 | 85 | 39.8 | 39.5 |  |  |  |  | 40.0 | 39.7 | 35.0 |
| 10-29 14Z | Thu 09:00 | 39.9 | 79 | 39.1 | 38.0 |  |  |  |  | 39.0 | 39.1 | 34.4 |
| 10-29 15Z | Thu 10:00 | 39.0 | 71 | 38.9 | 37.5 | 38.2 | 34.1 | 38.0 | 38.0 | 38.0 | 38.7 | 33.9 |
| 10-29 16Z | Thu 11:00 | 37.9 | 63 | 38.8 | 37.6 |  |  |  |  | 38.0 | 38.6 | 33.9 |
| 10-29 17Z | Thu 12:00 | 37.0 | 56 | 39.8 | 38.3 |  |  |  |  | 37.0 | 38.7 | 34.0 |
| Bias so far |  |  |  | +0.8 | +0.4 | -0.6 | -4.3 | +0.0 | -1.4 | +0.0 | -0.1 | -5.1 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (MPX): https://forecast.weather.gov/product.php?site=mpx&issuedby=mpx&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
