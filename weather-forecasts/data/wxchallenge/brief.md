# WxChallenge forecast brief: Yakutat, AK (PAYA)

- Station: **PAYA**
- Target day: **2026-11-10**, scored over 2026-11-10T06Z to 2026-11-11T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-11-10T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-11-09T16:00:08+00:00 (refreshed several times an hour while the forecast job runs)
- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)

## How to use this brief (for AI assistants)

1. Look at all model forecasts for the target day, then the **CONSENSUS** row.
2. Check the track-record table. A model with a large, consistent bias (|bias| close to its MAE) is reliably off in that direction. The consensus tries to remove some of that bias.
3. For precip, enter roughly the ensemble **median**, not the mean: errors are charged per 0.01" and most heavily near zero. When the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.
4. Use "Today so far" (the day currently in progress, not the target day) to see which models are handling the current pattern; persistent errors there often carry into the target day. "Newest runs vs obs so far today" does the same for the runs out since the deadline (e.g. the latest HRRR): check whether they have today right before leaning on their changes for the target day.
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
| HRRR | 09/12Z | 43.9 | 39.2 | 20.0 | 0.24 |
| RRFS | 09/12Z | 44.3 | 37.9 | 21.7 | 0.25 |
| IFS | 09/06Z | 47.9 | 37.7 | 32.9 | 0.62 |
| IFS_HRES | 09/06Z | 47.4 | 37.4 | 31.4 | 0.62 |
| GFS | 09/06Z | 47.7 | 41.3 | 30.9 | 0.22 |
| GFS_MOS | 09/06Z | 46.0 | 37.0 | 18.0 | 0.22 |
| NBM | 09/15Z | 46.0 | 37.0 | 21.0 | 0.26 |
| USL | — | — | — | — | — |
| ENS | 09/06Z | 47.4 | 40.6 | 29.4 | 0.50 |
| GEFS | 09/06Z | 40.8 | 37.2 | 16.7 | 0.22 |
| HRRRCAST (precip only) | — | — | — | — | — |
| REFS (precip only) | 09/12Z | — | — | — | 0.33 |
| NBM_QMD (precip only) | 09/06Z | — | — | — | 0.51 |
| **CONSENSUS** |  | **46.8** | **37.5** | **25.3** | **0.34** |

Notes:
- IFS_HRES: not in the consensus
- GFS_MOS: MOS Q06 categories [1, 0, 0, 2] -> midpoints
- NBM: NBS Q06 amounts
- USL: failed this run (no USL run for 2026-11-10 available at 2026-11-09 16Z)
- ENS: ensemble mean of 51 members
- GEFS: ensemble mean of 31 members; not in the consensus
- HRRRCAST: failed this run (HRRRCast covers the CONUS HRRR domain only)
- REFS: median of 14 members

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: GFS 0.19, NBM 0.17, GFS_MOS 0.17, IFS 0.13, ENS 0.13, RRFS 0.12, HRRR 0.09 (using parent's track record: ENS from IFS)
- Low °F weights: GFS_MOS 0.22, RRFS 0.16, HRRR 0.15, IFS 0.14, ENS 0.14, NBM 0.12, GFS 0.07 (using parent's track record: ENS from IFS)
- Wind kt weights: HRRR 0.19, IFS 0.17, ENS 0.17, RRFS 0.15, GFS_MOS 0.13, NBM 0.11, GFS 0.08 (using parent's track record: ENS from IFS)
- Precip in weights: IFS 0.15, NBM 0.15, ENS 0.15, RRFS 0.15, GFS 0.13, HRRR 0.13, GFS_MOS 0.13 (using parent's track record: ENS from IFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 45.6 | 46.5 | 47.4 | 48.2 | 49.1 | 47.4 |
| ENS | 51 | Low °F | 39.0 | 39.9 | 40.8 | 41.5 | 42.1 | 40.6 |
| ENS | 51 | Wind kt | 25.0 | 27.1 | 29.5 | 32.3 | 33.6 | 29.4 |
| ENS | 51 | Precip in | 0.31 | 0.37 | 0.47 | 0.63 | 0.71 | 0.50 |
| GEFS | 31 | High °F | 39.5 | 40.1 | 40.8 | 41.5 | 42.6 | 40.8 |
| GEFS | 31 | Low °F | 35.9 | 36.5 | 37.3 | 38.0 | 38.1 | 37.2 |
| GEFS | 31 | Wind kt | 14.1 | 14.9 | 15.8 | 16.8 | 19.9 | 16.7 |
| GEFS | 31 | Precip in | 0.11 | 0.13 | 0.20 | 0.32 | 0.37 | 0.22 |
| REFS | 14 | Precip in | 0.21 | 0.24 | 0.33 | 0.44 | 0.58 | 0.36 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 100% | 90% | 41% |
| GEFS | 100% | 90% | 36% | 0% |
| REFS | 100% | 100% | 64% | 21% |

NBM QMD calibrated 24-h precip percentiles: p10 0.12", p25 0.28", p50 0.51", p75 0.68", p90 0.88"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 72% | 31% | 34% | 78% | 78% to 97% | — |
| NBM | NBS P06 | 98% | 93% | 31% | 63% | 98% to 100% | — |
| ENS | member fraction | 100% | 96% | 67% | 100% | 100% | — |
| GEFS | member fraction | 94% | 45% | 29% | 94% | 100% | — |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 98% | 71% | 31% | 63% | 100% | — |

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 06Z | Mon 21:00 | 42.1 | 42.9 | 45.3 | 44.7 | 43.6 | 43.0 | 41.0 | 45.2 | 38.5 |
| 11-10 07Z | Mon 22:00 | 42.7 | 43.0 |  | 45.9 |  |  |  | 45.5 | 38.5 |
| 11-10 08Z | Mon 23:00 | 42.8 | 43.3 |  | 45.0 |  |  |  | 45.6 | 38.5 |
| 11-10 09Z | Tue 00:00 | 42.6 | 43.6 | 44.8 | 44.4 | 44.6 | 43.0 | 41.0 | 45.4 | 38.6 |
| 11-10 10Z | Tue 01:00 | 41.3 | 43.9 |  | 43.6 |  |  |  | 45.1 | 38.6 |
| 11-10 11Z | Tue 02:00 | 41.9 | 44.3 |  | 44.2 |  |  |  | 44.6 | 38.6 |
| 11-10 12Z | Tue 03:00 | 40.7 | 42.4 | 44.2 | 43.8 | 42.7 | 42.0 | 40.0 | 43.9 | 38.6 |
| 11-10 13Z | Tue 04:00 | 41.7 | 42.1 |  | 41.2 |  |  |  | 43.1 | 38.6 |
| 11-10 14Z | Tue 05:00 | 40.6 | 42.3 |  | 39.1 |  |  |  | 42.2 | 38.5 |
| 11-10 15Z | Tue 06:00 | 40.9 | 41.8 | 40.1 | 39.8 | 43.2 | 41.0 | 39.0 | 41.6 | 38.5 |
| 11-10 16Z | Tue 07:00 | 40.2 | 41.3 |  | 39.7 |  |  |  | 41.2 | 38.4 |
| 11-10 17Z | Tue 08:00 | 39.2 | 38.7 |  | 38.2 |  |  |  | 41.2 | 38.3 |
| 11-10 18Z | Tue 09:00 | 39.4 | 38.0 | 38.2 | 37.4 | 43.2 | 40.0 | 39.0 | 41.6 | 38.4 |
| 11-10 19Z | Tue 10:00 | 40.0 | 39.7 |  | 40.5 |  |  |  | 43.0 | 38.9 |
| 11-10 20Z | Tue 11:00 | 41.8 | 41.5 |  | 43.5 |  |  |  | 44.8 | 39.5 |
| 11-10 21Z | Tue 12:00 | 43.0 | 42.2 | 45.3 | 45.1 | 44.3 | 44.0 | 44.0 | 46.1 | 40.0 |
| 11-10 22Z | Tue 13:00 | 43.9 | 43.2 |  | 44.2 |  |  |  | 46.4 | 40.0 |
| 11-10 23Z | Tue 14:00 | 43.8 | 42.7 |  | 45.6 |  |  |  | 46.2 | 39.9 |
| 11-11 00Z | Tue 15:00 | 43.3 | 42.0 | 47.2 | 46.9 | 43.9 | 44.0 | 44.0 | 45.7 | 39.7 |
| 11-11 01Z | Tue 16:00 | 41.7 | 42.0 |  | 47.4 |  |  |  | 44.9 | 39.6 |
| 11-11 02Z | Tue 17:00 | 41.1 | 42.7 |  | 44.5 |  |  |  | 43.9 | 39.4 |
| 11-11 03Z | Tue 18:00 | 40.5 | 42.4 | 42.8 | 42.1 | 45.6 | 41.0 | 41.0 | 43.2 | 39.3 |
| 11-11 04Z | Tue 19:00 | 40.9 | 42.6 |  | 41.9 |  |  |  | 43.2 | 39.0 |
| 11-11 05Z | Tue 20:00 | 39.5 | 42.1 |  | 42.4 |  |  |  | 43.6 | 38.8 |
| 11-11 06Z | Tue 21:00 | 40.8 | 41.5 | 46.7 | 46.3 | 44.5 | 41.0 | 40.0 | 43.9 | 38.5 |

Dewpoint (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 06Z | Mon 21:00 | 38.6 | 37.8 | 41.4 | 41.7 | 39.2 | 37.0 | 40.0 | 41.7 | 31.6 |
| 11-10 07Z | Mon 22:00 | 39.4 | 38.8 |  | 41.3 |  |  |  | 41.9 | 32.2 |
| 11-10 08Z | Mon 23:00 | 39.7 | 39.1 |  | 39.7 |  |  |  | 41.5 | 33.0 |
| 11-10 09Z | Tue 00:00 | 40.1 | 40.8 | 40.5 | 40.3 | 39.7 | 37.0 | 40.0 | 41.0 | 33.6 |
| 11-10 10Z | Tue 01:00 | 39.1 | 40.0 |  | 40.6 |  |  |  | 40.8 | 34.0 |
| 11-10 11Z | Tue 02:00 | 39.6 | 40.4 |  | 39.8 |  |  |  | 40.6 | 34.2 |
| 11-10 12Z | Tue 03:00 | 38.7 | 40.4 | 39.9 | 40.1 | 37.5 | 36.0 | 39.0 | 40.2 | 34.2 |
| 11-10 13Z | Tue 04:00 | 40.1 | 39.5 |  | 39.7 |  |  |  | 39.7 | 34.0 |
| 11-10 14Z | Tue 05:00 | 39.4 | 40.2 |  | 37.9 |  |  |  | 39.1 | 33.6 |
| 11-10 15Z | Tue 06:00 | 37.9 | 39.1 | 37.9 | 37.7 | 36.0 | 37.0 | 37.0 | 38.3 | 33.0 |
| 11-10 16Z | Tue 07:00 | 37.4 | 38.5 |  | 37.9 |  |  |  | 37.5 | 32.0 |
| 11-10 17Z | Tue 08:00 | 36.0 | 36.2 |  | 35.9 |  |  |  | 36.6 | 30.8 |
| 11-10 18Z | Tue 09:00 | 35.0 | 35.4 | 35.4 | 35.1 | 33.1 | 37.0 | 35.0 | 35.9 | 29.9 |
| 11-10 19Z | Tue 10:00 | 34.6 | 34.6 |  | 36.0 |  |  |  | 35.4 | 29.6 |
| 11-10 20Z | Tue 11:00 | 37.0 | 35.0 |  | 35.4 |  |  |  | 34.9 | 29.7 |
| 11-10 21Z | Tue 12:00 | 37.8 | 34.4 | 34.4 | 34.1 | 31.9 | 37.0 | 38.0 | 34.4 | 29.7 |
| 11-10 22Z | Tue 13:00 | 37.8 | 33.0 |  | 34.3 |  |  |  | 34.1 | 29.8 |
| 11-10 23Z | Tue 14:00 | 38.1 | 31.5 |  | 31.8 |  |  |  | 34.0 | 30.1 |
| 11-11 00Z | Tue 15:00 | 36.2 | 32.3 | 31.0 | 30.0 | 32.5 | 37.0 | 37.0 | 34.1 | 30.2 |
| 11-11 01Z | Tue 16:00 | 36.7 | 32.3 |  | 27.9 |  |  |  | 35.1 | 30.3 |
| 11-11 02Z | Tue 17:00 | 38.6 | 33.0 |  | 34.8 |  |  |  | 36.2 | 30.2 |
| 11-11 03Z | Tue 18:00 | 37.8 | 33.8 | 39.4 | 39.7 | 35.7 | 36.0 | 38.0 | 36.9 | 30.3 |
| 11-11 04Z | Tue 19:00 | 36.5 | 34.1 |  | 39.8 |  |  |  | 37.5 | 30.5 |
| 11-11 05Z | Tue 20:00 | 34.3 | 36.2 |  | 38.8 |  |  |  | 37.7 | 30.8 |
| 11-11 06Z | Tue 21:00 | 38.2 | 38.3 | 32.0 | 31.1 | 35.1 | 36.0 | 37.0 | 37.5 | 30.7 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 06Z | Mon 21:00 | 87 | 82 | 86 | 89 | 84 | 79 | 96 | 88 | 76 |
| 11-10 07Z | Mon 22:00 | 88 | 85 |  | 84 |  |  |  | 87 | 78 |
| 11-10 08Z | Mon 23:00 | 89 | 85 |  | 82 |  |  |  | 86 | 80 |
| 11-10 09Z | Tue 00:00 | 91 | 90 | 85 | 85 | 83 | 79 | 96 | 85 | 82 |
| 11-10 10Z | Tue 01:00 | 92 | 86 |  | 89 |  |  |  | 85 | 83 |
| 11-10 11Z | Tue 02:00 | 91 | 86 |  | 84 |  |  |  | 86 | 84 |
| 11-10 12Z | Tue 03:00 | 93 | 93 | 85 | 87 | 82 | 79 | 96 | 87 | 84 |
| 11-10 13Z | Tue 04:00 | 94 | 90 |  | 94 |  |  |  | 88 | 84 |
| 11-10 14Z | Tue 05:00 | 95 | 92 |  | 95 |  |  |  | 89 | 83 |
| 11-10 15Z | Tue 06:00 | 89 | 90 | 92 | 92 | 76 | 86 | 92 | 89 | 81 |
| 11-10 16Z | Tue 07:00 | 90 | 90 |  | 93 |  |  |  | 87 | 78 |
| 11-10 17Z | Tue 08:00 | 88 | 91 |  | 91 |  |  |  | 84 | 74 |
| 11-10 18Z | Tue 09:00 | 84 | 90 | 90 | 91 | 67 | 89 | 85 | 80 | 72 |
| 11-10 19Z | Tue 10:00 | 81 | 82 |  | 84 |  |  |  | 75 | 69 |
| 11-10 20Z | Tue 11:00 | 83 | 78 |  | 73 |  |  |  | 69 | 68 |
| 11-10 21Z | Tue 12:00 | 82 | 74 | 65 | 65 | 62 | 76 | 79 | 64 | 67 |
| 11-10 22Z | Tue 13:00 | 79 | 67 |  | 68 |  |  |  | 63 | 67 |
| 11-10 23Z | Tue 14:00 | 80 | 64 |  | 58 |  |  |  | 63 | 68 |
| 11-11 00Z | Tue 15:00 | 76 | 68 | 53 | 52 | 64 | 76 | 76 | 65 | 69 |
| 11-11 01Z | Tue 16:00 | 82 | 68 |  | 46 |  |  |  | 69 | 69 |
| 11-11 02Z | Tue 17:00 | 91 | 68 |  | 69 |  |  |  | 75 | 70 |
| 11-11 03Z | Tue 18:00 | 90 | 71 | 88 | 91 | 68 | 82 | 89 | 80 | 70 |
| 11-11 04Z | Tue 19:00 | 84 | 72 |  | 92 |  |  |  | 81 | 72 |
| 11-11 05Z | Tue 20:00 | 81 | 79 |  | 87 |  |  |  | 80 | 73 |
| 11-11 06Z | Tue 21:00 | 90 | 88 | 56 | 55 | 69 | 82 | 89 | 79 | 74 |

Wind speed (kt) at the hour:

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 06Z | Mon 21:00 | 20.0 | 21.7 | 32.9 | 31.4 | 30.9 | 18.0 | 21.0 | 29.2 | 15.2 |
| 11-10 07Z | Mon 22:00 | 19.0 | 21.5 |  | 28.7 |  |  |  | 28.8 | 14.9 |
| 11-10 08Z | Mon 23:00 | 18.3 | 20.2 |  | 26.2 |  |  |  | 26.8 | 14.7 |
| 11-10 09Z | Tue 00:00 | 15.8 | 16.9 | 25.0 | 23.7 | 26.6 | 15.0 | 18.0 | 24.5 | 14.3 |
| 11-10 10Z | Tue 01:00 | 13.3 | 12.9 |  | 21.2 |  |  |  | 22.0 | 13.3 |
| 11-10 11Z | Tue 02:00 | 16.4 | 14.4 |  | 20.5 |  |  |  | 19.2 | 12.0 |
| 11-10 12Z | Tue 03:00 | 15.2 | 9.4 | 18.2 | 16.5 | 15.1 | 9.0 | 12.0 | 16.4 | 11.0 |
| 11-10 13Z | Tue 04:00 | 12.3 | 9.9 |  | 10.5 |  |  |  | 13.4 | 10.1 |
| 11-10 14Z | Tue 05:00 | 12.3 | 9.9 |  | 8.8 |  |  |  | 11.0 | 9.4 |
| 11-10 15Z | Tue 06:00 | 7.5 | 7.8 | 6.3 | 5.5 | 11.0 | 4.0 | 8.0 | 9.8 | 9.0 |
| 11-10 16Z | Tue 07:00 | 7.5 | 6.3 |  | 6.5 |  |  |  | 8.6 | 8.6 |
| 11-10 17Z | Tue 08:00 | 6.2 | 4.5 |  | 5.0 |  |  |  | 7.5 | 8.4 |
| 11-10 18Z | Tue 09:00 | 5.2 | 3.8 | 5.7 | 5.4 | 8.6 | 3.0 | 7.0 | 7.2 | 8.2 |
| 11-10 19Z | Tue 10:00 | 5.7 | 5.6 |  | 4.9 |  |  |  | 7.0 | 8.2 |
| 11-10 20Z | Tue 11:00 | 5.1 | 5.6 |  | 6.1 |  |  |  | 7.3 | 8.3 |
| 11-10 21Z | Tue 12:00 | 5.1 | 4.9 | 6.0 | 5.2 | 7.7 | 6.0 | 9.0 | 7.9 | 8.6 |
| 11-10 22Z | Tue 13:00 | 4.2 | 5.3 |  | 8.4 |  |  |  | 8.3 | 8.6 |
| 11-10 23Z | Tue 14:00 | 5.4 | 11.0 |  | 11.8 |  |  |  | 8.9 | 8.9 |
| 11-11 00Z | Tue 15:00 | 5.9 | 9.7 | 10.0 | 9.4 | 11.8 | 11.0 | 10.0 | 9.8 | 9.5 |
| 11-11 01Z | Tue 16:00 | 12.0 | 10.0 |  | 12.6 |  |  |  | 11.0 | 10.2 |
| 11-11 02Z | Tue 17:00 | 14.5 | 12.7 |  | 13.8 |  |  |  | 12.9 | 11.3 |
| 11-11 03Z | Tue 18:00 | 2.8 | 11.7 | 19.5 | 18.4 | 19.2 | 16.0 | 11.0 | 14.2 | 12.1 |
| 11-11 04Z | Tue 19:00 | 3.7 | 14.3 |  | 18.7 |  |  |  | 14.5 | 11.9 |
| 11-11 05Z | Tue 20:00 | 5.1 | 15.6 |  | 15.3 |  |  |  | 14.8 | 11.3 |
| 11-11 06Z | Tue 21:00 | 13.8 | 13.8 | 14.8 | 13.2 | 14.2 | 10.0 | 8.0 | 14.6 | 10.8 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| 11-10 06Z | Mon 21:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-10 07Z | Mon 22:00 | 0.00 | 0.01 |  | 0.04 |  | 0.03 | 0.03 |
| 11-10 08Z | Mon 23:00 | 0.00 | 0.02 |  | 0.06 |  | 0.07 | 0.05 |
| 11-10 09Z | Tue 00:00 | 0.01 | 0.04 | 0.08 | 0.08 | 0.04 | 0.10 | 0.08 |
| 11-10 10Z | Tue 01:00 | 0.01 | 0.04 |  | 0.10 |  | 0.12 | 0.09 |
| 11-10 11Z | Tue 02:00 | 0.04 | 0.05 |  | 0.13 |  | 0.14 | 0.10 |
| 11-10 12Z | Tue 03:00 | 0.20 | 0.05 | 0.15 | 0.14 | 0.07 | 0.17 | 0.12 |
| 11-10 13Z | Tue 04:00 | 0.24 | 0.05 |  | 0.17 |  | 0.20 | 0.12 |
| 11-10 14Z | Tue 05:00 | 0.24 | 0.10 |  | 0.23 |  | 0.23 | 0.12 |
| 11-10 15Z | Tue 06:00 | 0.24 | 0.11 | 0.28 | 0.28 | 0.12 | 0.26 | 0.13 |
| 11-10 16Z | Tue 07:00 | 0.24 | 0.11 |  | 0.31 |  | 0.27 | 0.13 |
| 11-10 17Z | Tue 08:00 | 0.24 | 0.11 |  | 0.31 |  | 0.28 | 0.13 |
| 11-10 18Z | Tue 09:00 | 0.24 | 0.11 | 0.30 | 0.31 | 0.12 | 0.29 | 0.13 |
| 11-10 19Z | Tue 10:00 | 0.24 | 0.11 |  | 0.31 |  | 0.29 | 0.13 |
| 11-10 20Z | Tue 11:00 | 0.24 | 0.11 |  | 0.31 |  | 0.29 | 0.13 |
| 11-10 21Z | Tue 12:00 | 0.24 | 0.11 | 0.30 | 0.31 | 0.12 | 0.29 | 0.13 |
| 11-10 22Z | Tue 13:00 | 0.24 | 0.11 |  | 0.32 |  | 0.30 | 0.14 |
| 11-10 23Z | Tue 14:00 | 0.24 | 0.11 |  | 0.32 |  | 0.31 | 0.14 |
| 11-11 00Z | Tue 15:00 | 0.24 | 0.11 | 0.32 | 0.32 | 0.12 | 0.31 | 0.15 |
| 11-11 01Z | Tue 16:00 | 0.24 | 0.11 |  | 0.32 |  | 0.34 | 0.16 |
| 11-11 02Z | Tue 17:00 | 0.24 | 0.11 |  | 0.34 |  | 0.37 | 0.17 |
| 11-11 03Z | Tue 18:00 | 0.24 | 0.12 | 0.41 | 0.41 | 0.18 | 0.39 | 0.18 |
| 11-11 04Z | Tue 19:00 | 0.24 | 0.15 |  | 0.54 |  | 0.43 | 0.19 |
| 11-11 05Z | Tue 20:00 | 0.24 | 0.20 |  | 0.61 |  | 0.46 | 0.21 |
| 11-11 06Z | Tue 21:00 | 0.24 | 0.25 | 0.62 | 0.62 | 0.22 | 0.50 | 0.22 |

Total cloud cover (%):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 06Z | Mon 21:00 | 100 | 100 | 100 | 100 | 100 | 100 | 97 | 99 | 99 |
| 11-10 07Z | Mon 22:00 | 95 | 100 |  | 97 |  |  | 95 | 94 | 100 |
| 11-10 08Z | Mon 23:00 | 100 | 100 |  | 100 |  |  | 96 | 89 | 100 |
| 11-10 09Z | Tue 00:00 | 84 | 100 | 89 | 89 | 100 | 100 | 93 | 86 | 100 |
| 11-10 10Z | Tue 01:00 | 100 | 47 |  | 45 |  |  | 95 | 88 | 100 |
| 11-10 11Z | Tue 02:00 | 100 | 75 |  | 80 |  |  | 96 | 91 | 100 |
| 11-10 12Z | Tue 03:00 | 100 | 100 | 98 | 99 | 100 | 100 | 94 | 94 | 100 |
| 11-10 13Z | Tue 04:00 | 100 | 100 |  | 100 |  |  | 91 | 95 | 99 |
| 11-10 14Z | Tue 05:00 | 100 | 100 |  | 98 |  |  | 77 | 96 | 98 |
| 11-10 15Z | Tue 06:00 | 100 | 89 | 92 | 92 | 100 | 75 | 87 | 97 | 98 |
| 11-10 16Z | Tue 07:00 | 100 | 100 |  | 98 |  |  | 85 | 96 | 97 |
| 11-10 17Z | Tue 08:00 | 67 | 75 |  | 86 |  |  |  | 95 | 96 |
| 11-10 18Z | Tue 09:00 | 100 | 100 | 100 | 100 | 100 | 75 | 88 | 95 | 95 |
| 11-10 19Z | Tue 10:00 | 100 | 100 |  | 100 |  |  |  | 96 | 95 |
| 11-10 20Z | Tue 11:00 | 100 | 100 |  | 99 |  |  |  | 97 | 96 |
| 11-10 21Z | Tue 12:00 | 100 | 100 | 100 | 100 | 100 | 75 | 82 | 98 | 96 |
| 11-10 22Z | Tue 13:00 | 100 | 100 |  | 100 |  |  |  | 98 | 96 |
| 11-10 23Z | Tue 14:00 | 100 | 100 |  | 100 |  |  |  | 97 | 95 |
| 11-11 00Z | Tue 15:00 | 100 | 100 | 95 | 95 | 100 | 100 | 92 | 96 | 95 |
| 11-11 01Z | Tue 16:00 | 100 | 100 |  | 84 |  |  |  | 97 | 95 |
| 11-11 02Z | Tue 17:00 | 100 | 100 |  | 100 |  |  |  | 98 | 95 |
| 11-11 03Z | Tue 18:00 | 100 | 100 | 100 | 100 | 100 | 100 | 91 | 98 | 96 |
| 11-11 04Z | Tue 19:00 | 97 | 100 |  | 100 |  |  |  | 97 | 96 |
| 11-11 05Z | Tue 20:00 | 25 | 100 |  | 78 |  |  |  | 95 | 96 |
| 11-11 06Z | Tue 21:00 | 100 | 100 | 100 | 100 | 100 | 100 | 89 | 94 | 96 |

## Track record this period

Since 2026-10-26 at PAYA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-11-10 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 14 | 6.0 | -0.2 | -1.2 | -0.2 | -0.04 | 0.4 | 2.1 | 1.5 | 0.23 |
| IFS_HRES | 14 | 7.8 | -1.2 | +1.5 | +0.6 | -0.06 | 1.9 | 2.3 | 1.7 | 0.18 |
| IFS | 14 | 8.0 | -0.8 | +2.3 | +1.1 | -0.04 | 1.5 | 2.6 | 2.3 | 0.18 |
| GFS_MOS | 14 | 8.1 | +0.7 | -1.1 | -3.4 | -0.04 | 1.1 | 1.5 | 3.4 | 0.32 |
| NBM | 14 | 8.4 | -1.0 | -1.9 | -4.0 | -0.07 | 1.1 | 3.3 | 4.0 | 0.18 |
| RRFS | 14 | 9.1 | -1.6 | +1.4 | -1.9 | -0.02 | 1.8 | 2.2 | 2.9 | 0.20 |
| HRRR | 14 | 10.1 | -2.0 | +1.2 | -1.3 | +0.01 | 2.4 | 2.5 | 2.1 | 0.31 |
| GFS | 14 | 14.5 | +0.4 | +5.6 | +5.9 | -0.09 | 0.9 | 5.8 | 5.9 | 0.29 |

## Daily verification (all 14 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 7.5 | 7.9 | 1.5 | 2.4 | 8.8 | 2.8 | 0.9 | 4.7 | NBM |
| 10-27 h | 8.5 | 8.5 | 12.5 | 9.5 | 17.0 | 0.5 | 6.5 | 6.5 | GFS_MOS |
| 10-28 h | 10.5 | 12.0 | 13.0 | 12.5 | 20.5 | 4.0 | 11.0 | 2.0 | CONSENSUS |
| 10-29 h | 11.5 | 12.5 | 14.5 | 13.5 | 18.0 | 3.0 | 11.5 | 3.5 | GFS_MOS |
| 10-30 h | 9.7 | 11.3 | 10.2 | 9.0 | 13.4 | 8.8 | 5.1 | 4.8 | CONSENSUS |
| 10-31 h | 13.6 | 3.7 | 3.9 | 4.4 | 15.2 | 21.1 | 13.9 | 12.5 | RRFS |
| 11-01 h | 13.7 | 14.3 | 6.9 | 8.0 | 19.1 | 4.8 | 7.1 | 4.5 | CONSENSUS |
| 11-02 h | 12.1 | 10.9 | 12.5 | 12.3 | 23.5 | 17.9 | 14.5 | 12.3 | RRFS |
| 11-03 h | 6.8 | 4.3 | 6.9 | 7.0 | 17.1 | 10.8 | 6.6 | 4.7 | RRFS |
| 11-04 h | 9.1 | 4.9 | 5.5 | 4.7 | 3.9 | 4.7 | 7.1 | 3.9 | GFS |
| 11-05 h | 7.3 | 3.4 | 3.4 | 5.1 | 9.6 | 13.1 | 11.1 | 6.0 | RRFS |
| 11-06 h | 16.7 | 9.7 | 5.3 | 5.7 | 8.6 | 8.1 | 11.7 | 6.8 | IFS |
| 11-07 h | 7.9 | 9.6 | 7.8 | 7.5 | 18.0 | 7.7 | 4.2 | 8.5 | NBM |
| 11-08 h | 6.4 | 13.7 | 8.0 | 7.0 | 9.9 | 6.0 | 6.2 | 3.9 | CONSENSUS |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 43 | +4 | +3 | +0 | -1 | +1 | +0 | +0 | +1 |
| 10-27 h | 49 | -3 | -3 | -4 | -4 | +1 | +0 | -3 | -2 |
| 10-28 h | 47 | -1 | -4 | -4 | -5 | -1 | +3 | -5 | +0 |
| 10-29 h | 44 | -1 | -2 | -1 | -2 | -2 | +1 | -4 | -1 |
| 10-30 h | 42 | -2 | +0 | +2 | +2 | +1 | +2 | +1 | +1 |
| 10-31 h | 46 | -2 | +0 | +0 | +0 | -2 | +0 | +0 | +0 |
| 11-01 h | 46 | -5 | -2 | -3 | -3 | +0 | +0 | -2 | -1 |
| 11-02 h | 43 | -3 | -1 | -3 | -3 | +2 | +2 | +0 | +0 |
| 11-03 h | 45 | -2 | -2 | +1 | +1 | +1 | +1 | -1 | +0 |
| 11-04 h | 47 | -3 | -1 | +2 | +2 | +0 | -1 | +0 | +0 |
| 11-05 h | 46 | -3 | -2 | -1 | -2 | +1 | +2 | +0 | +0 |
| 11-06 h | 46 | -1 | -2 | +0 | -1 | +1 | +2 | +0 | +0 |
| 11-07 h | 45 | -2 | -1 | -1 | -2 | +1 | +0 | +0 | +0 |
| 11-08 h | 43 | -2 | -3 | -1 | -1 | +0 | -1 | -2 | -1 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 36 | +1 | +2 | +1 | +0 | +5 | +0 | +0 | +2 |
| 10-27 h | 28 | +5 | +5 | +7 | +5 | +15 | +0 | +2 | +4 |
| 10-28 h | 25 | +9 | +8 | +8 | +7 | +18 | +0 | +5 | +2 |
| 10-29 h | 23 | +10 | +10 | +12 | +10 | +16 | +0 | +6 | +2 |
| 10-30 h | 28 | +4 | +4 | +5 | +4 | +10 | -3 | +1 | -2 |
| 10-31 h | 41 | -1 | +0 | -1 | -2 | +1 | -1 | -5 | -4 |
| 11-01 h | 35 | +0 | +3 | +1 | -1 | +8 | +3 | -1 | +0 |
| 11-02 h | 36 | -1 | -3 | +1 | +0 | +5 | +0 | -4 | -3 |
| 11-03 h | 36 | +2 | +1 | +2 | +2 | +6 | -2 | -3 | -2 |
| 11-04 h | 41 | -4 | -1 | +0 | +0 | -1 | -1 | -5 | -3 |
| 11-05 h | 40 | -1 | +0 | -1 | -2 | +0 | -2 | -5 | -3 |
| 11-06 h | 40 | +0 | +0 | +0 | +0 | +1 | -1 | -4 | -2 |
| 11-07 h | 36 | -1 | -1 | +0 | +0 | +4 | -2 | -2 | -2 |
| 11-08 h | 32 | +2 | +1 | +5 | +4 | +6 | -3 | -2 | +0 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 5 | +1 | +1 | +1 | +2 | +4 | +0 | -1 | +1 |
| 10-27 h | 7 | -1 | -1 | -3 | -1 | +2 | -1 | -3 | -1 |
| 10-28 h | 5 | +1 | +0 | -2 | -1 | +3 | -2 | -2 | +0 |
| 10-29 h | 5 | +1 | -1 | -3 | -3 | +0 | -4 | -3 | -1 |
| 10-30 h | 16 | -6 | -6 | +1 | +0 | +3 | -3 | -5 | -3 |
| 10-31 h | 26 | -3 | -5 | +1 | +0 | +11 | -9 | -4 | -3 |
| 11-01 h | 12 | +0 | -5 | -1 | -2 | +14 | -3 | -5 | -1 |
| 11-02 h | 14 | -3 | -5 | +0 | -1 | +0 | -7 | -5 | -2 |
| 11-03 h | 15 | +2 | -1 | +1 | +0 | +2 | -1 | -4 | +1 |
| 11-04 h | 14 | +0 | +0 | +3 | +1 | +5 | -2 | -4 | +1 |
| 11-05 h | 14 | -2 | -2 | -1 | -1 | +7 | -4 | -4 | -1 |
| 11-06 h | 25 | -8 | -5 | +6 | +4 | +7 | -6 | -8 | -1 |
| 11-07 h | 15 | +1 | +5 | +4 | +3 | +13 | -1 | -4 | +4 |
| 11-08 h | 9 | +0 | -2 | +4 | +4 | +7 | -4 | -2 | +1 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 0.07 | -0.05 | -0.06 | +0.00 | +0.01 | +0.02 | -0.07 | -0.01 | -0.03 |
| 10-27 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-28 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-29 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 10-30 h | 0.11 | -0.02 | -0.11 | +0.09 | +0.10 | +0.03 | -0.06 | +0.02 | -0.01 |
| 10-31 h | 1.44 | +0.91 | +0.12 | +0.24 | +0.24 | +0.67 | +1.56 | +0.69 | +0.70 |
| 11-01 h | 0.21 | +0.54 | +0.35 | -0.08 | -0.10 | -0.13 | +0.01 | +0.06 | +0.13 |
| 11-02 h | 1.38 | -0.66 | -0.44 | -0.85 | -0.88 | -1.22 | -1.06 | -0.80 | -0.83 |
| 11-03 h | 0.64 | +0.18 | -0.08 | -0.24 | -0.27 | -0.48 | -0.42 | -0.06 | -0.18 |
| 11-04 h | 0.51 | +0.21 | -0.15 | +0.20 | +0.22 | +0.04 | -0.09 | +0.01 | +0.04 |
| 11-05 h | 0.75 | -0.23 | -0.04 | -0.09 | -0.06 | -0.38 | -0.48 | -0.33 | -0.25 |
| 11-06 h | 1.17 | -0.92 | -0.52 | -0.23 | -0.27 | -0.31 | -0.21 | -0.37 | -0.43 |
| 11-07 h | 0.36 | +0.30 | +0.37 | +0.34 | +0.26 | +0.51 | +0.38 | -0.01 | +0.31 |
| 11-08 h | 0.00 | +0.06 | +0.26 | +0.00 | +0.00 | +0.01 | +0.00 | +0.03 | +0.06 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 14 | +11 | 14 | +14 | 16 |
| RRFS | 14 | +0 | 16 | +8 | 16 |
| IFS | 14 | +8 | 15 | +15 | 17 |
| IFS_HRES | 14 | +8 | 16 | +14 | 16 |
| GFS | 14 | +9 | 13 | +15 | 16 |
| GFS_MOS | 14 | -3 | 10 | +11 | 15 |
| NBM | 14 | +2 | 13 | +6 | 11 |

Night clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 100% | — | -17 | -22 | -1 | +0 | -17 | +0 | -16 |
| 10-27 h | 20% | — | -4 | -16 | +29 | +35 | +19 | -12 | -9 |
| 10-28 h | 0% | — | +20 | +0 | +34 | +34 | +0 | +0 | +10 |
| 10-29 h | 0% | — | +2 | +0 | +7 | +7 | +0 | +0 | +5 |
| 10-30 h | 75% | — | +18 | +11 | -10 | -12 | +6 | -73 | -4 |
| 10-31 h | 100% | — | +0 | +0 | +0 | +0 | +0 | +0 | -2 |
| 11-01 h | 85% | — | +14 | -13 | -29 | -39 | +14 | +15 | -8 |
| 11-02 h | 98% | — | +1 | -22 | -2 | +0 | +2 | +2 | -10 |
| 11-03 h | 80% | — | +20 | +8 | +20 | +19 | +20 | +20 | +13 |
| 11-04 h | 100% | — | -10 | -17 | -6 | -6 | +0 | +0 | -13 |
| 11-05 h | 100% | — | +0 | -20 | -3 | -3 | -10 | +0 | -12 |
| 11-06 h | 100% | — | +0 | -6 | +0 | +0 | -3 | +0 | -6 |
| 11-07 h | 89% | — | +11 | +0 | +8 | +7 | +8 | +11 | +3 |
| 11-08 h | 40% | — | +60 | +60 | +52 | +53 | +60 | -18 | +51 |

Day clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 100% | — | -11 | -15 | -3 | +0 | -3 | -18 | -17 |
| 10-27 h | 0% | — | +4 | +0 | +18 | +18 | +0 | +0 | +4 |
| 10-28 h | 0% | — | +1 | +0 | +24 | +25 | +1 | +0 | +2 |
| 10-29 h | 10% | — | +4 | +51 | +10 | +8 | -10 | -10 | +17 |
| 10-30 h | 33% | — | +67 | +64 | +67 | +67 | +67 | +48 | +57 |
| 10-31 h | 100% | — | +0 | -15 | -4 | -2 | +0 | +0 | -8 |
| 11-01 h | 59% | — | +37 | +2 | -13 | -13 | +39 | +41 | +6 |
| 11-02 h | 94% | — | -3 | -6 | -1 | +4 | +6 | +6 | -5 |
| 11-03 h | 100% | — | -3 | +0 | +0 | +0 | +0 | +0 | -3 |
| 11-04 h | 61% | — | +34 | +24 | +36 | +35 | +37 | +31 | +21 |
| 11-05 h | 80% | — | +16 | +14 | +19 | +19 | +17 | +20 | +8 |
| 11-06 h | 100% | — | +0 | -1 | +0 | +0 | +0 | +0 | -4 |
| 11-07 h | 52% | — | +21 | -18 | +38 | +37 | +19 | +26 | -3 |
| 11-08 h | 80% | — | +20 | +20 | +10 | +4 | +20 | -5 | +13 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 14 | +0.7 | 1.8 | +0.2 | 1.4 |
| RRFS | 14 | +0.0 | 1.8 | -0.4 | 1.7 |
| IFS | 14 | -0.3 | 1.9 | -1.9 | 2.2 |
| IFS_HRES | 14 | -0.8 | 2.1 | -2.2 | 2.5 |
| GFS | 14 | -1.1 | 2.3 | -2.8 | 3.2 |
| GFS_MOS | 14 | -1.0 | 1.4 | -1.9 | 2.3 |
| NBM | 14 | -1.4 | 2.1 | -0.4 | 1.4 |

Night dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 39.6 | -0.8 | -0.4 | -0.4 | -0.4 | -1.9 | -1.6 | -1.1 |
| 10-27 h | 31.5 | +3.2 | +2.5 | +2.7 | +1.8 | +0.2 | +0.1 | +0.2 |
| 10-28 h | 27.8 | +4.6 | -0.2 | +4.6 | +3.6 | -1.1 | -1.4 | +1.2 |
| 10-29 h | 24.7 | +8.4 | +5.6 | +5.3 | +4.5 | -0.5 | -0.9 | +2.5 |
| 10-30 h | 26.8 | +5.8 | +5.0 | +0.8 | -1.3 | +3.2 | -0.7 | +2.9 |
| 10-31 h | 40.5 | -0.1 | +0.3 | +1.3 | +1.2 | +0.6 | -2.5 | -0.6 |
| 11-01 h | 37.6 | -0.8 | +1.8 | -1.1 | -2.1 | +2.7 | +2.7 | -0.8 |
| 11-02 h | 36.9 | +0.1 | -2.8 | -1.4 | -1.9 | +1.0 | +0.1 | -2.3 |
| 11-03 h | 36.7 | +0.5 | +0.3 | -2.0 | -2.7 | +0.8 | -0.2 | -1.0 |
| 11-04 h | 42.3 | -2.9 | -1.8 | -0.9 | -1.1 | -3.2 | -2.7 | -2.4 |
| 11-05 h | 40.2 | -0.2 | -0.1 | -0.8 | -1.1 | -1.3 | -1.0 | -3.1 |
| 11-06 h | 40.0 | -2.2 | -4.4 | -3.0 | -3.3 | -5.5 | -2.0 | -5.1 |
| 11-07 h | 39.1 | +0.7 | +0.3 | +0.7 | +0.9 | +0.6 | +0.0 | +0.0 |
| 11-08 h | 32.5 | -0.2 | -1.1 | -2.7 | -3.2 | -5.7 | -3.1 | -3.4 |

Day dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM |
| --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 40.9 | +0.5 | -0.1 | -0.1 | +0.1 | -5.8 | -1.6 | -0.3 |
| 10-27 h | 37.2 | +0.5 | -0.5 | -2.5 | -2.8 | -6.6 | -6.9 | -2.0 |
| 10-28 h | 33.1 | +5.5 | +2.1 | +0.4 | +0.1 | -8.2 | -5.6 | -1.6 |
| 10-29 h | 32.0 | +5.8 | +3.5 | +0.5 | -0.6 | -7.7 | -5.5 | -1.8 |
| 10-30 h | 31.1 | +2.6 | +3.5 | +0.2 | -0.9 | +2.4 | -1.4 | +5.1 |
| 10-31 h | 42.7 | -1.4 | +0.6 | +0.6 | +0.4 | -1.4 | -2.1 | +0.5 |
| 11-01 h | 37.1 | +0.3 | +1.7 | -1.7 | -2.5 | +0.5 | +1.5 | +1.1 |
| 11-02 h | 38.0 | -0.2 | +0.0 | -0.4 | -0.7 | +0.7 | +0.6 | +1.2 |
| 11-03 h | 37.6 | -0.6 | -1.8 | -4.6 | -5.5 | -2.6 | -0.6 | -0.3 |
| 11-04 h | 40.8 | -0.3 | +0.0 | -2.5 | -2.9 | -1.4 | +0.1 | +0.4 |
| 11-05 h | 38.8 | -2.1 | -2.7 | -2.3 | -2.3 | -1.5 | -0.2 | -0.9 |
| 11-06 h | 42.0 | -1.5 | -2.8 | -2.0 | -1.7 | -1.7 | -3.0 | -1.8 |
| 11-07 h | 37.5 | +0.2 | -0.9 | +0.9 | +1.1 | -2.2 | +0.3 | +0.2 |
| 11-08 h | 37.0 | -1.2 | -2.4 | -7.4 | -8.2 | -6.5 | -5.4 | -3.3 |

## Today so far (2026-11-09, through 2026-11-09T14:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 42.1 °F, low 32.0 °F, max wind 13 kt, precip 0.00" (9 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 08/18Z | -1.0 | 1.9 | 44 (+2) pending | 34 (+2) | +1.5 | 0.09 | +0.09 |
| RRFS | 08/18Z | -1.7 | 1.7 | 44 (+2) pending | 32 (+0) | +0.5 | 0.01 | +0.01 |
| IFS | 08/12Z | +1.3 | 1.8 | 46 (+4) pending | 36 (+4) | +3.6 | 0.02 | +0.02 |
| IFS_HRES | 08/12Z | +0.9 | 1.5 | 46 (+4) pending | 35 (+3) | +2.4 | 0.02 | +0.02 |
| GFS | 08/18Z | +5.2 | 5.4 | 49 (+7) pending | 39 (+7) | +5.0 | 0.01 | +0.01 |
| GFS_MOS | 08/18Z | -0.7 | 1.6 | 47 (+5) pending | 33 (+1) | -1.5 | — | — |
| NBM | 08/23Z | -2.1 | 2.5 | 46 (+4) pending | 31 (-1) | +1.4 | — | — |

## Clouds so far today (2026-11-09, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (AKST) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-09 06Z | Sun 21:00 | 100 |  | 100 | 100 | 97 | 96 | 100 | 75 | 87 |
| 11-09 07Z | Sun 22:00 | 100 | 75 | 100 | 100 |  | 99 |  |  | 88 |
| 11-09 08Z | Sun 23:00 | 100 | 44 | 100 | 100 |  | 100 |  |  | 91 |
| 11-09 09Z | Mon 00:00 | 100 | 19 | 83 | 100 | 100 | 100 | 100 | 75 | 91 |
| 11-09 10Z | Mon 01:00 | 100 | 19 | 100 | 100 |  | 100 |  |  | 92 |
| 11-09 11Z | Mon 02:00 | 100 | 0 | 100 | 100 |  | 100 |  |  | 93 |
| 11-09 12Z | Mon 03:00 | 100 | 0 | 100 | 100 | 100 | 100 | 100 | 75 | 91 |
| 11-09 13Z | Mon 04:00 | 100 | 19 | 100 | 100 |  | 100 |  |  | 92 |
| 11-09 14Z | Mon 05:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 94 |
| 11-09 15Z | Mon 06:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 94 |

## Dewpoint so far today (2026-11-09, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (AKST) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-09 07Z | Sun 22:00 | 30.9 | 92 | 34.2 | 30.7 |  | 30.6 |  |  |  |
| 11-09 08Z | Sun 23:00 | 30.9 | 92 | 33.6 | 30.9 |  | 30.5 |  |  |  |
| 11-09 09Z | Mon 00:00 | 32.0 | 85 | 32.8 | 32.2 | 31.5 | 30.7 | 34.7 | 35.0 | 33.0 |
| 11-09 10Z | Mon 01:00 | 32.0 | 88 | 32.6 | 32.0 |  | 30.8 |  |  |  |
| 11-09 11Z | Mon 02:00 | 30.9 | 82 | 32.0 | 32.5 |  | 30.4 |  |  |  |
| 11-09 12Z | Mon 03:00 | 30.9 | 76 | 33.3 | 30.6 | 30.3 | 29.1 | 33.2 | 35.0 | 30.0 |
| 11-09 13Z | Mon 04:00 | 28.9 | 70 | 32.2 | 31.0 |  | 27.1 |  |  |  |
| 11-09 14Z | Mon 05:00 | 28.9 | 67 | 31.9 | 29.9 |  | 26.2 |  |  |  |
| 11-09 15Z | Mon 06:00 | 27.0 | 55 | 33.5 | 31.5 | 30.7 | 30.2 | 31.6 | 34.0 | 30.0 |
| Bias so far |  |  |  | +2.6 | +1.0 | +0.9 | -0.8 | +3.2 | +4.7 | +1.0 |

## Newest runs vs obs so far today (2026-11-09)

The runs that have come out since today's deadline (HRRR, RRFS, IFS, GFS, GFS_MOS, NBM; fetched 2026-11-09 16:00Z), against the METAR nearest each hour since each run's first valid time. These runs are not scored for today; use them to judge whether the newest guidance has the current pattern right before trusting what it says for the target day. A run already a few degrees off a few hours in usually stays off. Compare its bias with the submitted run of the same model over the same hours: if the newest run is no better, its change for the target day deserves less weight. Text guidance (GFS_MOS, NBM) often starts after the last report, so it has no hours to compare yet.

How each run is doing so far (forecast - observed; Hours = hours compared). Cloud bias is in percentage points against the METAR sky cover. Precip = the run's total since its first valid time / what was observed over the same span:

| Model | Run | From | Hours | Temp bias | Temp MAE | Submitted run temp bias | Td bias | Wind bias | Cloud bias | Precip fcst / obs |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 09/12Z | 13Z | 3 | -4.3 | 4.3 | -3.0 | +1.4 | +2.9 | +27 | 0.02 / 0.00 |
| RRFS | 09/12Z | 13Z | 3 | -3.8 | 3.8 | -3.2 | +0.7 | +1.3 | +27 | 0.00 / 0.00 |
| IFS | 09/06Z | 09Z | 3 | -1.4 | 1.4 | -0.3 | +1.9 | +2.5 | +60 | 0.03 / 0.00 |
| GFS | 09/06Z | 09Z | 3 | +2.4 | 3.6 | +3.1 | +2.4 | +2.5 | +60 | 0.01 / 0.00 |
| GFS_MOS | 09/06Z | 12Z | 2 | -3.5 | 3.5 | -3.0 | +2.1 | -4.5 | +22 | — |
| NBM | 09/15Z | 21Z | 0 | — | — | — | — | — | — | — |

Rest of today (after the last report to 06Z; hourly values, so 3-hourly guidance can miss the true extreme). Day high/low = the run's extreme for the rest of the day combined with the observed high 42.1 / low 32.0 °F so far:

| Model | Run | Hours left | Max T | Min T | Max wind | Day high | Day low |
| --- | --- | --: | --: | --: | --: | --: | --: |
| HRRR | 09/12Z | 15 | 43.1 | 37.7 | 20.0 | 43.1 | 32.0 |
| RRFS | 09/12Z | 15 | 43.3 | 36.0 | 21.7 | 43.3 | 32.0 |
| IFS | 09/06Z | 5 | 45.3 | 38.8 | 32.9 | 45.3 | 32.0 |
| GFS | 09/06Z | 5 | 46.6 | 40.5 | 30.9 | 46.6 | 32.0 |
| GFS_MOS | 09/06Z | 5 | 44.0 | 40.0 | 21.0 | 44.0 | 32.0 |
| NBM | 09/15Z | 4 | 43.0 | 41.0 | 21.0 | 43.0 | 32.0 |

Hour by hour (°F, kt; obs blank after the last report):

| UTC | Local (AKST) | Obs T | Obs Td | Obs wind | HRRR T | HRRR Td | HRRR wind | RRFS T | RRFS Td | RRFS wind | IFS T | IFS Td | IFS wind | GFS T | GFS Td | GFS wind | GFS_MOS T | GFS_MOS Td | GFS_MOS wind | NBM T | NBM Td | NBM wind |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-09 09Z | Mon 00:00 | 36.0 | 32.0 | 6 |  |  |  |  |  |  | 35.7 | 32.0 | 9 | 41.1 | 34.2 | 13 |  |  |  |  |  |  |
| 11-09 10Z | Mon 01:00 | 35.1 | 32.0 | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 11Z | Mon 02:00 | 36.0 | 30.9 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 12Z | Mon 03:00 | 37.9 | 30.9 | 7 |  |  |  |  |  |  | 36.9 | 30.9 | 8 | 41.7 | 31.6 | 10 | 36.0 | 31.0 | 5 |  |  |  |
| 11-09 13Z | Mon 04:00 | 37.9 | 28.9 | 6 | 34.6 | 27.1 | 10 | 35.4 | 28.4 | 9 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 14Z | Mon 05:00 | 39.0 | 28.9 | 8 | 34.8 | 28.7 | 10 | 35.9 | 28.6 | 6 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 15Z | Mon 06:00 | 42.1 | 27.0 | 13 | 36.8 | 33.2 | 16 | 36.4 | 29.9 | 16 | 39.1 | 32.8 | 16 | 40.3 | 31.2 | 11 | 37.0 | 31.0 | 6 |  |  |  |
| 11-09 16Z | Mon 07:00 |  |  |  | 37.7 | 33.8 | 18 | 36.0 | 31.5 | 16 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 17Z | Mon 08:00 |  |  |  | 38.9 | 34.4 | 18 | 37.0 | 31.7 | 17 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 18Z | Mon 09:00 |  |  |  | 39.8 | 35.0 | 20 | 37.7 | 32.5 | 16 | 38.8 | 36.4 | 17 | 40.5 | 33.6 | 17 | 40.0 | 32.0 | 13 |  |  |  |
| 11-09 19Z | Mon 10:00 |  |  |  | 41.1 | 35.2 | 19 | 38.7 | 33.3 | 17 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 20Z | Mon 11:00 |  |  |  | 42.8 | 35.3 | 17 | 40.1 | 33.7 | 16 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 21Z | Mon 12:00 |  |  |  | 42.9 | 35.7 | 18 | 41.4 | 33.9 | 14 | 40.7 | 37.2 | 16 | 42.9 | 33.6 | 20 | 43.0 | 34.0 | 14 | 42.0 | 38.0 | 14 |
| 11-09 22Z | Mon 13:00 |  |  |  | 43.1 | 36.6 | 17 | 42.2 | 32.6 | 14 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-09 23Z | Mon 14:00 |  |  |  | 42.8 | 38.6 | 15 | 42.3 | 33.5 | 14 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 00Z | Mon 15:00 |  |  |  | 43.0 | 38.5 | 17 | 41.7 | 34.4 | 12 | 42.0 | 36.0 | 19 | 45.4 | 32.8 | 20 | 44.0 | 34.0 | 17 | 43.0 | 37.0 | 14 |
| 11-10 01Z | Mon 16:00 |  |  |  | 43.0 | 35.8 | 17 | 41.1 | 35.3 | 11 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 02Z | Mon 17:00 |  |  |  | 42.3 | 34.6 | 17 | 41.5 | 34.5 | 14 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 03Z | Mon 18:00 |  |  |  | 42.0 | 35.7 | 18 | 42.3 | 35.3 | 16 | 42.8 | 36.4 | 21 | 46.6 | 32.7 | 23 | 44.0 | 36.0 | 21 | 41.0 | 38.0 | 19 |
| 11-10 04Z | Mon 19:00 |  |  |  | 42.4 | 38.0 | 18 | 43.3 | 36.6 | 19 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 05Z | Mon 20:00 |  |  |  | 42.2 | 38.3 | 19 | 43.1 | 38.6 | 21 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 06Z | Mon 21:00 |  |  |  | 42.1 | 38.6 | 20 | 42.9 | 37.8 | 22 | 45.3 | 41.4 | 33 | 43.6 | 39.2 | 31 | 43.0 | 37.0 | 18 | 41.0 | 40.0 | 21 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (AJK): https://forecast.weather.gov/product.php?site=ajk&issuedby=ajk&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
