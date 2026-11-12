# WxChallenge forecast brief: Yakutat, AK (PAYA)

- Station: **PAYA**
- Target day: **2026-11-13**, scored over 2026-11-13T06Z to 2026-11-14T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-11-13T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-11-12T14:30:06+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 12/12Z | 41.2 | 33.1 | 6.5 | 0.01 |
| RRFS | 12/06Z | 43.0 | 33.1 | 7.7 | 0.02 |
| IFS | 12/06Z | 39.1 | 34.7 | 8.3 | 0.02 |
| IFS_HRES | 12/06Z | 38.5 | 33.1 | 7.4 | 0.02 |
| GFS | 12/06Z | 43.3 | 40.4 | 10.5 | 0.00 |
| GFS_MOS | 12/06Z | 45.0 | 29.0 | 5.0 | 0.00 |
| NBM | 12/12Z | 40.0 | 29.0 | 5.0 | 0.00 |
| USL | — | — | — | — | — |
| ENS | 12/00Z | 38.8 | 34.9 | 7.2 | 0.01 |
| GEFS | 12/06Z | 37.5 | 34.3 | 9.1 | 0.01 |
| HRRRCAST (precip only) | — | — | — | — | — |
| REFS (precip only) | 12/06Z | — | — | — | 0.01 |
| NBM_QMD (precip only) | 12/06Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **42.6** | **31.6** | **7.3** | **0.01** |

Notes:
- IFS_HRES: not in the consensus
- GFS_MOS: MOS Q06 categories [0, 0, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- USL: failed this run (no USL run for 2026-11-13 available at 2026-11-12 14Z)
- ENS: ensemble mean of 51 members
- GEFS: ensemble mean of 31 members; not in the consensus
- HRRRCAST: failed this run (HRRRCast covers the CONUS HRRR domain only)
- REFS: median of 13 members

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: GFS 0.23, GFS_MOS 0.18, NBM 0.15, IFS 0.14, RRFS 0.11, ENS 0.10, HRRR 0.09
- Low °F weights: GFS_MOS 0.22, RRFS 0.17, HRRR 0.15, IFS 0.14, NBM 0.13, ENS 0.12, GFS 0.07
- Wind kt weights: HRRR 0.23, RRFS 0.17, IFS 0.15, GFS_MOS 0.14, NBM 0.13, GFS 0.09, ENS 0.08
- Precip in weights: IFS 0.16, NBM 0.16, RRFS 0.15, HRRR 0.14, GFS 0.13, GFS_MOS 0.13, ENS 0.13

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 37.3 | 38.0 | 38.7 | 39.4 | 40.1 | 38.8 |
| ENS | 51 | Low °F | 33.6 | 34.4 | 34.8 | 35.5 | 36.0 | 34.9 |
| ENS | 51 | Wind kt | 5.0 | 5.5 | 6.7 | 7.8 | 10.6 | 7.2 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.02 | 0.01 |
| GEFS | 31 | High °F | 36.8 | 37.2 | 37.6 | 37.8 | 38.0 | 37.5 |
| GEFS | 31 | Low °F | 33.6 | 34.0 | 34.3 | 34.6 | 34.8 | 34.3 |
| GEFS | 31 | Wind kt | 6.7 | 7.2 | 8.3 | 10.8 | 12.7 | 9.1 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.05 | 0.01 |
| REFS | 13 | Precip in | 0.00 | 0.01 | 0.01 | 0.02 | 0.08 | 0.03 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 31% | 4% | 0% | 0% |
| GEFS | 32% | 0% | 0% | 0% |
| REFS | 54% | 8% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.01", p90 0.05"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 6% | 3% | 6% | 38% | 38% to 47% | 0.11 (8) |
| NBM | NBS P06 | 9% | 0% | 0% | 20% | 20% to 27% | 0.04 (8) |
| ENS | member fraction | 8% | 0% | 0% | 26% | 31% | 0.05 (8) |
| GEFS | member fraction | 0% | 0% | 0% | 32% | 32% | 0.09 (8) |
| REFS | member fraction | — | — | — | — | 54% | — |
| NBM_QMD | NBM QMD | 10% | 0% | 0% | 24% | 28% | 0.04 (8) |

For reference, always forecasting the period's observed frequency (88% of 6-h blocks wet) scores Brier 0.11.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 34.6 | 33.6 | 37.0 | 36.1 | 42.2 | 35.0 | 34.0 | 36.5 | 37.1 |
| 11-13 07Z | Thu 22:00 | 33.8 | 33.3 |  | 33.8 |  |  |  | 36.3 | 36.9 |
| 11-13 08Z | Thu 23:00 | 33.1 | 33.2 |  | 34.0 |  |  |  | 36.1 | 36.6 |
| 11-13 09Z | Fri 00:00 | 33.1 | 33.3 | 34.9 | 33.4 | 42.3 | 34.0 | 32.0 | 36.0 | 36.3 |
| 11-13 10Z | Fri 01:00 | 33.1 | 33.9 |  | 33.1 |  |  |  | 36.0 | 35.9 |
| 11-13 11Z | Fri 02:00 | 33.2 | 34.4 |  | 34.3 |  |  |  | 36.0 | 35.6 |
| 11-13 12Z | Fri 03:00 | 33.8 | 35.6 | 36.5 | 35.5 | 41.6 | 32.0 | 31.0 | 36.0 | 35.3 |
| 11-13 13Z | Fri 04:00 | 33.9 | 35.2 |  | 35.3 |  |  |  | 36.0 | 35.0 |
| 11-13 14Z | Fri 05:00 | 33.6 | 35.9 |  | 34.4 |  |  |  | 36.0 | 34.7 |
| 11-13 15Z | Fri 06:00 | 33.8 | 35.7 | 36.1 | 35.0 | 41.9 | 30.0 | 30.0 | 36.0 | 34.5 |
| 11-13 16Z | Fri 07:00 | 34.2 | 35.6 |  | 34.3 |  |  |  | 35.8 | 34.4 |
| 11-13 17Z | Fri 08:00 | 34.5 | 38.0 |  | 33.8 |  |  |  | 35.5 | 34.4 |
| 11-13 18Z | Fri 09:00 | 35.1 | 38.0 | 35.3 | 34.2 | 42.2 | 31.0 | 32.0 | 35.6 | 34.7 |
| 11-13 19Z | Fri 10:00 | 36.9 | 38.9 |  | 35.2 |  |  |  | 36.3 | 35.4 |
| 11-13 20Z | Fri 11:00 | 38.7 | 39.7 |  | 36.2 |  |  |  | 37.3 | 36.4 |
| 11-13 21Z | Fri 12:00 | 40.4 | 41.7 | 37.9 | 37.4 | 42.8 | 41.0 | 38.0 | 38.1 | 37.1 |
| 11-13 22Z | Fri 13:00 | 41.2 | 42.7 |  | 38.0 |  |  |  | 38.5 | 37.3 |
| 11-13 23Z | Fri 14:00 | 41.0 | 42.1 |  | 38.5 |  |  |  | 38.6 | 37.2 |
| 11-14 00Z | Fri 15:00 | 40.2 | 41.1 | 39.0 | 38.3 | 41.7 | 43.0 | 39.0 | 38.5 | 37.0 |
| 11-14 01Z | Fri 16:00 | 39.6 | 39.8 |  | 36.9 |  |  |  | 38.2 | 36.8 |
| 11-14 02Z | Fri 17:00 | 40.3 | 39.4 |  | 37.1 |  |  |  | 37.6 | 36.5 |
| 11-14 03Z | Fri 18:00 | 38.6 | 39.0 | 37.4 | 36.3 | 41.1 | 38.0 | 35.0 | 37.2 | 36.3 |
| 11-14 04Z | Fri 19:00 | 38.1 | 39.0 |  | 35.6 |  |  |  | 37.0 | 36.2 |
| 11-14 05Z | Fri 20:00 | 38.7 | 39.4 |  | 34.8 |  |  |  | 37.0 | 36.2 |
| 11-14 06Z | Fri 21:00 | 39.5 | 39.4 | 36.7 | 35.9 | 40.8 | 37.0 | 33.0 | 37.0 | 36.1 |

Dewpoint (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 33.7 | 32.1 | 32.5 | 31.6 | 33.0 | 33.0 | 33.0 | 33.2 | 28.2 |
| 11-13 07Z | Thu 22:00 | 32.3 | 31.7 |  | 29.4 |  |  |  | 32.6 | 27.4 |
| 11-13 08Z | Thu 23:00 | 31.5 | 31.2 |  | 28.9 |  |  |  | 32.0 | 26.5 |
| 11-13 09Z | Fri 00:00 | 31.4 | 30.8 | 30.1 | 28.9 | 32.1 | 32.0 | 31.0 | 31.7 | 25.6 |
| 11-13 10Z | Fri 01:00 | 31.0 | 30.3 |  | 29.3 |  |  |  | 32.0 | 24.7 |
| 11-13 11Z | Fri 02:00 | 30.2 | 30.3 |  | 32.6 |  |  |  | 32.6 | 23.8 |
| 11-13 12Z | Fri 03:00 | 31.4 | 30.8 | 34.5 | 33.9 | 29.8 | 30.0 | 30.0 | 33.0 | 22.9 |
| 11-13 13Z | Fri 04:00 | 31.5 | 31.1 |  | 33.3 |  |  |  | 33.0 | 22.2 |
| 11-13 14Z | Fri 05:00 | 32.2 | 31.9 |  | 32.3 |  |  |  | 32.8 | 21.7 |
| 11-13 15Z | Fri 06:00 | 32.0 | 29.7 | 33.4 | 32.9 | 28.1 | 28.0 | 28.0 | 32.7 | 21.3 |
| 11-13 16Z | Fri 07:00 | 31.7 | 29.0 |  | 31.6 |  |  |  | 32.5 | 21.2 |
| 11-13 17Z | Fri 08:00 | 32.1 | 25.6 |  | 31.0 |  |  |  | 32.3 | 21.1 |
| 11-13 18Z | Fri 09:00 | 33.0 | 27.6 | 32.1 | 31.6 | 26.5 | 29.0 | 30.0 | 32.4 | 21.4 |
| 11-13 19Z | Fri 10:00 | 33.2 | 25.2 |  | 32.6 |  |  |  | 33.0 | 21.9 |
| 11-13 20Z | Fri 11:00 | 34.1 | 28.5 |  | 33.4 |  |  |  | 33.8 | 22.6 |
| 11-13 21Z | Fri 12:00 | 35.0 | 28.8 | 35.1 | 35.2 | 25.3 | 33.0 | 34.0 | 34.1 | 23.4 |
| 11-13 22Z | Fri 13:00 | 35.3 | 28.1 |  | 33.4 |  |  |  | 33.5 | 24.0 |
| 11-13 23Z | Fri 14:00 | 36.0 | 31.0 |  | 30.9 |  |  |  | 32.2 | 24.6 |
| 11-14 00Z | Fri 15:00 | 35.7 | 33.1 | 29.6 | 29.0 | 27.6 | 33.0 | 33.0 | 31.1 | 25.1 |
| 11-14 01Z | Fri 16:00 | 34.7 | 33.8 |  | 27.9 |  |  |  | 30.3 | 25.3 |
| 11-14 02Z | Fri 17:00 | 32.0 | 32.3 |  | 28.2 |  |  |  | 29.6 | 25.4 |
| 11-14 03Z | Fri 18:00 | 33.0 | 31.6 | 28.6 | 27.8 | 27.5 | 34.0 | 31.0 | 29.2 | 25.6 |
| 11-14 04Z | Fri 19:00 | 34.7 | 33.2 |  | 30.3 |  |  |  | 29.2 | 26.0 |
| 11-14 05Z | Fri 20:00 | 36.4 | 34.7 |  | 31.6 |  |  |  | 29.6 | 26.5 |
| 11-14 06Z | Fri 21:00 | 37.8 | 36.1 | 31.0 | 30.7 | 29.4 | 34.0 | 31.0 | 30.1 | 27.0 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 96 | 94 | 84 | 84 | 70 | 92 | 96 | 88 | 70 |
| 11-13 07Z | Thu 22:00 | 94 | 94 |  | 84 |  |  |  | 86 | 69 |
| 11-13 08Z | Thu 23:00 | 94 | 92 |  | 81 |  |  |  | 85 | 67 |
| 11-13 09Z | Fri 00:00 | 93 | 90 | 82 | 83 | 67 | 92 | 96 | 84 | 65 |
| 11-13 10Z | Fri 01:00 | 92 | 87 |  | 86 |  |  |  | 85 | 64 |
| 11-13 11Z | Fri 02:00 | 89 | 85 |  | 93 |  |  |  | 87 | 62 |
| 11-13 12Z | Fri 03:00 | 91 | 83 | 92 | 94 | 63 | 92 | 96 | 89 | 60 |
| 11-13 13Z | Fri 04:00 | 91 | 85 |  | 92 |  |  |  | 89 | 59 |
| 11-13 14Z | Fri 05:00 | 95 | 85 |  | 92 |  |  |  | 88 | 59 |
| 11-13 15Z | Fri 06:00 | 93 | 79 | 90 | 92 | 58 | 92 | 92 | 88 | 58 |
| 11-13 16Z | Fri 07:00 | 90 | 77 |  | 90 |  |  |  | 88 | 58 |
| 11-13 17Z | Fri 08:00 | 91 | 61 |  | 89 |  |  |  | 88 | 58 |
| 11-13 18Z | Fri 09:00 | 92 | 66 | 88 | 90 | 53 | 92 | 92 | 88 | 58 |
| 11-13 19Z | Fri 10:00 | 86 | 58 |  | 90 |  |  |  | 88 | 58 |
| 11-13 20Z | Fri 11:00 | 83 | 64 |  | 89 |  |  |  | 87 | 57 |
| 11-13 21Z | Fri 12:00 | 81 | 60 | 90 | 92 | 50 | 73 | 85 | 85 | 57 |
| 11-13 22Z | Fri 13:00 | 79 | 56 |  | 83 |  |  |  | 82 | 58 |
| 11-13 23Z | Fri 14:00 | 82 | 65 |  | 74 |  |  |  | 78 | 60 |
| 11-14 00Z | Fri 15:00 | 84 | 73 | 69 | 69 | 57 | 68 | 79 | 75 | 62 |
| 11-14 01Z | Fri 16:00 | 82 | 79 |  | 70 |  |  |  | 73 | 63 |
| 11-14 02Z | Fri 17:00 | 72 | 75 |  | 70 |  |  |  | 73 | 64 |
| 11-14 03Z | Fri 18:00 | 80 | 75 | 70 | 71 | 58 | 85 | 85 | 73 | 65 |
| 11-14 04Z | Fri 19:00 | 87 | 80 |  | 81 |  |  |  | 73 | 66 |
| 11-14 05Z | Fri 20:00 | 91 | 83 |  | 88 |  |  |  | 75 | 68 |
| 11-14 06Z | Fri 21:00 | 94 | 88 | 80 | 81 | 64 | 89 | 92 | 76 | 70 |

Wind speed (kt) at the hour:

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 4.5 | 4.6 | 6.3 | 5.5 | 6.2 | 3.0 | 3.0 | 4.7 | 5.9 |
| 11-13 07Z | Thu 22:00 | 4.5 | 4.2 |  | 2.4 |  |  |  | 3.5 | 5.8 |
| 11-13 08Z | Thu 23:00 | 4.4 | 4.6 |  | 0.6 |  |  |  | 2.2 | 5.6 |
| 11-13 09Z | Fri 00:00 | 4.3 | 3.3 | 0.4 | 0.4 | 6.5 | 1.0 | 0.0 | 1.5 | 5.5 |
| 11-13 10Z | Fri 01:00 | 4.4 | 3.2 |  | 1.9 |  |  |  | 2.1 | 5.7 |
| 11-13 11Z | Fri 02:00 | 4.4 | 3.5 |  | 5.2 |  |  |  | 3.6 | 6.0 |
| 11-13 12Z | Fri 03:00 | 4.6 | 4.3 | 6.3 | 5.9 | 8.5 | 1.0 | 3.0 | 4.7 | 6.4 |
| 11-13 13Z | Fri 04:00 | 5.6 | 5.6 |  | 5.2 |  |  |  | 5.0 | 6.4 |
| 11-13 14Z | Fri 05:00 | 5.4 | 4.9 |  | 4.6 |  |  |  | 4.9 | 6.4 |
| 11-13 15Z | Fri 06:00 | 5.6 | 5.0 | 5.5 | 4.8 | 9.6 | 1.0 | 3.0 | 4.5 | 6.5 |
| 11-13 16Z | Fri 07:00 | 5.4 | 5.2 |  | 2.7 |  |  |  | 3.8 | 6.6 |
| 11-13 17Z | Fri 08:00 | 6.0 | 3.0 |  | 1.3 |  |  |  | 2.9 | 6.8 |
| 11-13 18Z | Fri 09:00 | 6.1 | 4.3 | 1.4 | 0.7 | 5.2 | 3.0 | 3.0 | 2.2 | 7.0 |
| 11-13 19Z | Fri 10:00 | 5.6 | 5.9 |  | 0.8 |  |  |  | 1.7 | 7.0 |
| 11-13 20Z | Fri 11:00 | 5.4 | 4.3 |  | 0.4 |  |  |  | 1.6 | 6.9 |
| 11-13 21Z | Fri 12:00 | 5.0 | 3.3 | 1.5 | 2.2 | 4.3 | 3.0 | 3.0 | 1.6 | 6.8 |
| 11-13 22Z | Fri 13:00 | 5.0 | 3.1 |  | 2.6 |  |  |  | 1.4 | 6.6 |
| 11-13 23Z | Fri 14:00 | 4.6 | 3.8 |  | 0.9 |  |  |  | 1.2 | 6.3 |
| 11-14 00Z | Fri 15:00 | 4.9 | 3.6 | 0.3 | 0.3 | 9.5 | 5.0 | 5.0 | 1.4 | 6.2 |
| 11-14 01Z | Fri 16:00 | 5.0 | 2.5 |  | 0.7 |  |  |  | 1.6 | 6.2 |
| 11-14 02Z | Fri 17:00 | 5.0 | 2.1 |  | 1.0 |  |  |  | 2.1 | 6.3 |
| 11-14 03Z | Fri 18:00 | 3.0 | 2.7 | 0.7 | 0.5 | 6.6 | 4.0 | 4.0 | 2.6 | 6.4 |
| 11-14 04Z | Fri 19:00 | 2.5 | 4.7 |  | 3.8 |  |  |  | 3.1 | 6.5 |
| 11-14 05Z | Fri 20:00 | 5.5 | 4.6 |  | 2.8 |  |  |  | 3.9 | 6.6 |
| 11-14 06Z | Fri 21:00 | 6.5 | 4.5 | 2.8 | 2.2 | 7.3 | 4.0 | 4.0 | 4.4 | 6.9 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 07Z | Thu 22:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 08Z | Thu 23:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 09Z | Fri 00:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 10Z | Fri 01:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 11Z | Fri 02:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 12Z | Fri 03:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 13Z | Fri 04:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 14Z | Fri 05:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 15Z | Fri 06:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 16Z | Fri 07:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 17Z | Fri 08:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 18Z | Fri 09:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 19Z | Fri 10:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 20Z | Fri 11:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 21Z | Fri 12:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 22Z | Fri 13:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-13 23Z | Fri 14:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-14 00Z | Fri 15:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-14 01Z | Fri 16:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-14 02Z | Fri 17:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 |
| 11-14 03Z | Fri 18:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-14 04Z | Fri 19:00 | 0.00 | 0.00 |  | 0.00 |  | 0.01 | 0.00 |
| 11-14 05Z | Fri 20:00 | 0.00 | 0.00 |  | 0.02 |  | 0.01 | 0.01 |
| 11-14 06Z | Fri 21:00 | 0.01 | 0.02 | 0.02 | 0.02 | 0.00 | 0.01 | 0.01 |

Total cloud cover (%):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 94 | 43 | 59 | 59 | 68 | 75 | 58 | 76 | 76 |
| 11-13 07Z | Thu 22:00 | 96 | 78 |  | 87 |  |  | 75 | 74 | 75 |
| 11-13 08Z | Thu 23:00 | 100 | 64 |  | 69 |  |  | 69 | 70 | 76 |
| 11-13 09Z | Fri 00:00 | 100 | 99 | 48 | 47 | 77 | 0 | 77 | 69 | 76 |
| 11-13 10Z | Fri 01:00 | 100 | 100 |  | 14 |  |  | 81 | 73 | 71 |
| 11-13 11Z | Fri 02:00 | 9 | 100 |  | 51 |  |  | 63 | 80 | 65 |
| 11-13 12Z | Fri 03:00 | 100 | 100 | 98 | 98 | 95 | 0 | 77 | 85 | 63 |
| 11-13 13Z | Fri 04:00 | 100 | 100 |  | 95 |  |  | 77 | 86 | 68 |
| 11-13 14Z | Fri 05:00 | 100 | 100 |  | 100 |  |  |  | 86 | 78 |
| 11-13 15Z | Fri 06:00 | 100 | 100 | 100 | 100 | 100 | 0 | 84 | 87 | 86 |
| 11-13 16Z | Fri 07:00 | 100 | 95 |  | 99 |  |  |  | 90 | 91 |
| 11-13 17Z | Fri 08:00 | 100 | 100 |  | 100 |  |  |  | 95 | 95 |
| 11-13 18Z | Fri 09:00 | 100 | 100 | 100 | 100 | 100 | 44 | 88 | 98 | 98 |
| 11-13 19Z | Fri 10:00 | 100 | 100 |  | 100 |  |  |  | 99 | 99 |
| 11-13 20Z | Fri 11:00 | 100 | 100 |  | 100 |  |  |  | 99 | 99 |
| 11-13 21Z | Fri 12:00 | 100 | 100 | 100 | 100 | 100 | 19 | 93 | 100 | 100 |
| 11-13 22Z | Fri 13:00 | 100 | 100 |  | 100 |  |  |  | 99 | 100 |
| 11-13 23Z | Fri 14:00 | 100 | 100 |  | 100 |  |  |  | 98 | 100 |
| 11-14 00Z | Fri 15:00 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 98 | 100 |
| 11-14 01Z | Fri 16:00 | 100 | 100 |  | 100 |  |  |  | 98 | 100 |
| 11-14 02Z | Fri 17:00 | 100 | 100 |  | 98 |  |  |  | 98 | 100 |
| 11-14 03Z | Fri 18:00 | 100 | 100 | 100 | 100 | 100 | 100 | 95 | 98 | 100 |
| 11-14 04Z | Fri 19:00 | 100 | 100 |  | 100 |  |  |  | 98 | 100 |
| 11-14 05Z | Fri 20:00 | 100 | 100 |  | 100 |  |  |  | 98 | 100 |
| 11-14 06Z | Fri 21:00 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 98 | 100 |

## Track record this period

Since 2026-10-26 at PAYA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-11-10 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 17 | 6.3 | -0.6 | -0.7 | +0.2 | -0.08 | 0.8 | 1.9 | 2.0 | 0.22 |
| IFS_HRES | 17 | 8.1 | -1.5 | +1.5 | +2.2 | -0.06 | 2.0 | 2.0 | 3.1 | 0.19 |
| IFS | 17 | 8.4 | -1.2 | +2.2 | +2.6 | -0.04 | 1.7 | 2.4 | 3.6 | 0.18 |
| GFS_MOS | 17 | 8.4 | +0.0 | -0.4 | -3.6 | -0.10 | 1.3 | 1.4 | 3.8 | 0.31 |
| NBM | 17 | 8.7 | -1.4 | -1.5 | -4.1 | -0.12 | 1.5 | 2.7 | 4.3 | 0.20 |
| RRFS | 17 | 9.4 | -2.1 | +1.3 | -1.8 | -0.09 | 2.3 | 1.9 | 3.0 | 0.23 |
| HRRR | 17 | 10.3 | -2.7 | +1.4 | -0.9 | -0.05 | 2.9 | 2.3 | 2.1 | 0.30 |
| ENS | 2 | 12.2 | -2.4 | +3.0 | +6.9 | +0.00 | 2.4 | 3.0 | 6.9 | 0.32 |
| USL | 2 | 12.9 | -4.0 | -1.6 | +8.3 | -0.10 | 4.0 | 1.6 | 10.3 | 0.21 |
| GEFS | 2 | 14.6 | -6.9 | +0.4 | -2.5 | -0.32 | 6.9 | 1.5 | 2.5 | 0.33 |
| GFS | 17 | 14.7 | +0.3 | +5.5 | +6.0 | -0.16 | 0.8 | 5.6 | 6.0 | 0.31 |

## Daily verification (all 17 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 7.5 | 7.9 | 1.5 | 2.4 | 8.8 | 2.8 | 0.9 | — | — | — | 4.7 | NBM |
| 10-27 h | 8.5 | 8.5 | 12.5 | 9.5 | 17.0 | 0.5 | 6.5 | — | — | — | 6.5 | GFS_MOS |
| 10-28 h | 10.5 | 12.0 | 13.0 | 12.5 | 20.5 | 4.0 | 11.0 | — | — | — | 2.0 | CONSENSUS |
| 10-29 h | 11.5 | 12.5 | 14.5 | 13.5 | 18.0 | 3.0 | 11.5 | — | — | — | 3.5 | GFS_MOS |
| 10-30 h | 9.7 | 11.3 | 10.2 | 9.0 | 13.4 | 8.8 | 5.1 | — | — | — | 4.8 | CONSENSUS |
| 10-31 h | 13.6 | 3.7 | 3.9 | 4.4 | 15.2 | 21.1 | 13.9 | — | — | — | 12.5 | RRFS |
| 11-01 h | 13.7 | 14.3 | 6.9 | 8.0 | 19.1 | 4.8 | 7.1 | — | — | — | 4.5 | CONSENSUS |
| 11-02 h | 12.1 | 10.9 | 12.5 | 12.3 | 23.5 | 17.9 | 14.5 | — | — | — | 12.3 | RRFS |
| 11-03 h | 6.8 | 4.3 | 6.9 | 7.0 | 17.1 | 10.8 | 6.6 | — | — | — | 4.7 | RRFS |
| 11-04 h | 9.1 | 4.9 | 5.5 | 4.7 | 3.9 | 4.7 | 7.1 | — | — | — | 3.9 | GFS |
| 11-05 h | 7.3 | 3.4 | 3.4 | 5.1 | 9.6 | 13.1 | 11.1 | — | — | — | 6.0 | RRFS |
| 11-06 h | 16.7 | 9.7 | 5.3 | 5.7 | 8.6 | 8.1 | 11.7 | — | — | — | 6.8 | IFS |
| 11-07 h | 7.9 | 9.6 | 7.8 | 7.5 | 18.0 | 7.7 | 4.2 | — | — | — | 8.5 | NBM |
| 11-08 h | 6.4 | 13.7 | 8.0 | 7.0 | 9.9 | 6.0 | 6.2 | — | — | — | 3.9 | CONSENSUS |
| 11-09 h | 8.5 | 9.3 | 7.7 | 7.8 | 16.9 | 10.6 | 9.2 | — | — | — | 6.1 | CONSENSUS |
| 11-10 | 16.8 | 16.8 | 14.2 | 13.0 | 26.8 | 16.3 | 13.6 | 17.7 | 16.7 | 21.5 | 14.4 | IFS_HRES |
| 11-11 | 7.8 | 7.7 | 8.4 | 8.4 | 4.2 | 3.3 | 7.8 | 8.1 | 7.6 | 7.6 | 2.8 | CONSENSUS |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 43 | +4 | +3 | +0 | -1 | +1 | +0 | +0 | — | — | — | +1 |
| 10-27 h | 49 | -3 | -3 | -4 | -4 | +1 | +0 | -3 | — | — | — | -2 |
| 10-28 h | 47 | -1 | -4 | -4 | -5 | -1 | +3 | -5 | — | — | — | +0 |
| 10-29 h | 44 | -1 | -2 | -1 | -2 | -2 | +1 | -4 | — | — | — | -1 |
| 10-30 h | 42 | -2 | +0 | +2 | +2 | +1 | +2 | +1 | — | — | — | +1 |
| 10-31 h | 46 | -2 | +0 | +0 | +0 | -2 | +0 | +0 | — | — | — | +0 |
| 11-01 h | 46 | -5 | -2 | -3 | -3 | +0 | +0 | -2 | — | — | — | -1 |
| 11-02 h | 43 | -3 | -1 | -3 | -3 | +2 | +2 | +0 | — | — | — | +0 |
| 11-03 h | 45 | -2 | -2 | +1 | +1 | +1 | +1 | -1 | — | — | — | +0 |
| 11-04 h | 47 | -3 | -1 | +2 | +2 | +0 | -1 | +0 | — | — | — | +0 |
| 11-05 h | 46 | -3 | -2 | -1 | -2 | +1 | +2 | +0 | — | — | — | +0 |
| 11-06 h | 46 | -1 | -2 | +0 | -1 | +1 | +2 | +0 | — | — | — | +0 |
| 11-07 h | 45 | -2 | -1 | -1 | -2 | +1 | +0 | +0 | — | — | — | +0 |
| 11-08 h | 43 | -2 | -3 | -1 | -1 | +0 | -1 | -2 | — | — | — | -1 |
| 11-09 h | 48 | -4 | -4 | -2 | -2 | +1 | -1 | -2 | — | — | — | -1 |
| 11-10 | 50 | -6 | -6 | -4 | -4 | -1 | -3 | -4 | -5 | -4 | -9 | -3 |
| 11-11 | 47 | -3 | -1 | -1 | -1 | +0 | -1 | -2 | -3 | -1 | -5 | -1 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 36 | +1 | +2 | +1 | +0 | +5 | +0 | +0 | — | — | — | +2 |
| 10-27 h | 28 | +5 | +5 | +7 | +5 | +15 | +0 | +2 | — | — | — | +4 |
| 10-28 h | 25 | +9 | +8 | +8 | +7 | +18 | +0 | +5 | — | — | — | +2 |
| 10-29 h | 23 | +10 | +10 | +12 | +10 | +16 | +0 | +6 | — | — | — | +2 |
| 10-30 h | 28 | +4 | +4 | +5 | +4 | +10 | -3 | +1 | — | — | — | -2 |
| 10-31 h | 41 | -1 | +0 | -1 | -2 | +1 | -1 | -5 | — | — | — | -4 |
| 11-01 h | 35 | +0 | +3 | +1 | -1 | +8 | +3 | -1 | — | — | — | +0 |
| 11-02 h | 36 | -1 | -3 | +1 | +0 | +5 | +0 | -4 | — | — | — | -3 |
| 11-03 h | 36 | +2 | +1 | +2 | +2 | +6 | -2 | -3 | — | — | — | -2 |
| 11-04 h | 41 | -4 | -1 | +0 | +0 | -1 | -1 | -5 | — | — | — | -3 |
| 11-05 h | 40 | -1 | +0 | -1 | -2 | +0 | -2 | -5 | — | — | — | -3 |
| 11-06 h | 40 | +0 | +0 | +0 | +0 | +1 | -1 | -4 | — | — | — | -2 |
| 11-07 h | 36 | -1 | -1 | +0 | +0 | +4 | -2 | -2 | — | — | — | -2 |
| 11-08 h | 32 | +2 | +1 | +5 | +4 | +6 | -3 | -2 | — | — | — | +0 |
| 11-09 h | 32 | +2 | +0 | +4 | +3 | +7 | +1 | -1 | — | — | — | +1 |
| 11-10 | 36 | +3 | +2 | +1 | +0 | +7 | +3 | +1 | +0 | +4 | +2 | +2 |
| 11-11 | 39 | +1 | +1 | +1 | +1 | +2 | +0 | -2 | -3 | +2 | -1 | -1 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 5 | +1 | +1 | +1 | +2 | +4 | +0 | -1 | — | — | — | +1 |
| 10-27 h | 7 | -1 | -1 | -3 | -1 | +2 | -1 | -3 | — | — | — | -1 |
| 10-28 h | 5 | +1 | +0 | -2 | -1 | +3 | -2 | -2 | — | — | — | +0 |
| 10-29 h | 5 | +1 | -1 | -3 | -3 | +0 | -4 | -3 | — | — | — | -1 |
| 10-30 h | 16 | -6 | -6 | +1 | +0 | +3 | -3 | -5 | — | — | — | -3 |
| 10-31 h | 26 | -3 | -5 | +1 | +0 | +11 | -9 | -4 | — | — | — | -3 |
| 11-01 h | 12 | +0 | -5 | -1 | -2 | +14 | -3 | -5 | — | — | — | -1 |
| 11-02 h | 14 | -3 | -5 | +0 | -1 | +0 | -7 | -5 | — | — | — | -2 |
| 11-03 h | 15 | +2 | -1 | +1 | +0 | +2 | -1 | -4 | — | — | — | +1 |
| 11-04 h | 14 | +0 | +0 | +3 | +1 | +5 | -2 | -4 | — | — | — | +1 |
| 11-05 h | 14 | -2 | -2 | -1 | -1 | +7 | -4 | -4 | — | — | — | -1 |
| 11-06 h | 25 | -8 | -5 | +6 | +4 | +7 | -6 | -8 | — | — | — | -1 |
| 11-07 h | 15 | +1 | +5 | +4 | +3 | +13 | -1 | -4 | — | — | — | +4 |
| 11-08 h | 9 | +0 | -2 | +4 | +4 | +7 | -4 | -2 | — | — | — | +1 |
| 11-09 h | 31 | -3 | -5 | +1 | +2 | +0 | -10 | -8 | — | — | — | -3 |
| 11-10 | 19 | +3 | +3 | +13 | +12 | +15 | +1 | +1 | +19 | +11 | -2 | +7 |
| 11-11 | 19 | +1 | -2 | +9 | +9 | +4 | -4 | -7 | -2 | +3 | -3 | +1 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 0.07 | -0.05 | -0.06 | +0.00 | +0.01 | +0.02 | -0.07 | -0.01 | — | — | — | -0.03 |
| 10-27 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-28 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-29 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-30 h | 0.11 | -0.02 | -0.11 | +0.09 | +0.10 | +0.03 | -0.06 | +0.02 | — | — | — | -0.01 |
| 10-31 h | 1.44 | +0.91 | +0.12 | +0.24 | +0.24 | +0.67 | +1.56 | +0.69 | — | — | — | +0.70 |
| 11-01 h | 0.21 | +0.54 | +0.35 | -0.08 | -0.10 | -0.13 | +0.01 | +0.06 | — | — | — | +0.13 |
| 11-02 h | 1.38 | -0.66 | -0.44 | -0.85 | -0.88 | -1.22 | -1.06 | -0.80 | — | — | — | -0.83 |
| 11-03 h | 0.64 | +0.18 | -0.08 | -0.24 | -0.27 | -0.48 | -0.42 | -0.06 | — | — | — | -0.18 |
| 11-04 h | 0.51 | +0.21 | -0.15 | +0.20 | +0.22 | +0.04 | -0.09 | +0.01 | — | — | — | +0.04 |
| 11-05 h | 0.75 | -0.23 | -0.04 | -0.09 | -0.06 | -0.38 | -0.48 | -0.33 | — | — | — | -0.25 |
| 11-06 h | 1.17 | -0.92 | -0.52 | -0.23 | -0.27 | -0.31 | -0.21 | -0.37 | — | — | — | -0.43 |
| 11-07 h | 0.36 | +0.30 | +0.37 | +0.34 | +0.26 | +0.51 | +0.38 | -0.01 | — | — | — | +0.31 |
| 11-08 h | 0.00 | +0.06 | +0.26 | +0.00 | +0.00 | +0.01 | +0.00 | +0.03 | — | — | — | +0.06 |
| 11-09 h | 0.45 | +0.05 | -0.14 | -0.06 | -0.09 | -0.36 | -0.18 | -0.11 | — | — | — | -0.13 |
| 11-10 | 0.89 | -0.51 | -0.56 | -0.27 | -0.30 | -0.72 | -0.67 | -0.60 | -0.32 | -0.32 | -0.66 | -0.49 |
| 11-11 | 0.53 | -0.18 | -0.25 | +0.19 | +0.19 | -0.02 | +0.03 | -0.03 | +0.11 | +0.31 | +0.01 | +0.03 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 17 | +13 | 16 | +15 | 17 |
| RRFS | 17 | +6 | 17 | +10 | 16 |
| IFS | 17 | +12 | 16 | +14 | 18 |
| IFS_HRES | 17 | +11 | 16 | +14 | 17 |
| GFS | 17 | +13 | 16 | +16 | 16 |
| GFS_MOS | 17 | +2 | 11 | +10 | 13 |
| NBM | 17 | +6 | 15 | +7 | 12 |
| USL | 2 | +8 | 8 | +25 | 25 |
| ENS | 2 | +5 | 6 | +22 | 22 |
| GEFS | 2 | +6 | 8 | +21 | 21 |

Night clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 100% | — | -17 | -22 | -1 | +0 | -17 | +0 | -16 | — | — | — |
| 10-27 h | 20% | — | -4 | -16 | +29 | +35 | +19 | -12 | -9 | — | — | — |
| 10-28 h | 0% | — | +20 | +0 | +34 | +34 | +0 | +0 | +10 | — | — | — |
| 10-29 h | 0% | — | +2 | +0 | +7 | +7 | +0 | +0 | +5 | — | — | — |
| 10-30 h | 75% | — | +18 | +11 | -10 | -12 | +6 | -73 | -4 | — | — | — |
| 10-31 h | 100% | — | +0 | +0 | +0 | +0 | +0 | +0 | -2 | — | — | — |
| 11-01 h | 85% | — | +14 | -13 | -29 | -39 | +14 | +15 | -8 | — | — | — |
| 11-02 h | 98% | — | +1 | -22 | -2 | +0 | +2 | +2 | -10 | — | — | — |
| 11-03 h | 80% | — | +20 | +8 | +20 | +19 | +20 | +20 | +13 | — | — | — |
| 11-04 h | 100% | — | -10 | -17 | -6 | -6 | +0 | +0 | -13 | — | — | — |
| 11-05 h | 100% | — | +0 | -20 | -3 | -3 | -10 | +0 | -12 | — | — | — |
| 11-06 h | 100% | — | +0 | -6 | +0 | +0 | -3 | +0 | -6 | — | — | — |
| 11-07 h | 89% | — | +11 | +0 | +8 | +7 | +8 | +11 | +3 | — | — | — |
| 11-08 h | 40% | — | +60 | +60 | +52 | +53 | +60 | -18 | +51 | — | — | — |
| 11-09 h | 48% | 100% | +51 | +52 | +52 | +52 | +52 | +35 | +44 | — | — | — |
| 11-10 | 83% | 100% | +16 | +13 | +13 | +6 | +17 | +8 | +7 | +17 | +11 | +14 |
| 11-11 | 100% | 100% | -2 | -3 | +0 | +0 | +0 | +0 | -7 | +0 | -1 | -2 |

Day clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 100% | — | -11 | -15 | -3 | +0 | -3 | -18 | -17 | — | — | — |
| 10-27 h | 0% | — | +4 | +0 | +18 | +18 | +0 | +0 | +4 | — | — | — |
| 10-28 h | 0% | — | +1 | +0 | +24 | +25 | +1 | +0 | +2 | — | — | — |
| 10-29 h | 10% | — | +4 | +51 | +10 | +8 | -10 | -10 | +17 | — | — | — |
| 10-30 h | 33% | — | +67 | +64 | +67 | +67 | +67 | +48 | +57 | — | — | — |
| 10-31 h | 100% | — | +0 | -15 | -4 | -2 | +0 | +0 | -8 | — | — | — |
| 11-01 h | 59% | — | +37 | +2 | -13 | -13 | +39 | +41 | +6 | — | — | — |
| 11-02 h | 94% | — | -3 | -6 | -1 | +4 | +6 | +6 | -5 | — | — | — |
| 11-03 h | 100% | — | -3 | +0 | +0 | +0 | +0 | +0 | -3 | — | — | — |
| 11-04 h | 61% | — | +34 | +24 | +36 | +35 | +37 | +31 | +21 | — | — | — |
| 11-05 h | 80% | — | +16 | +14 | +19 | +19 | +17 | +20 | +8 | — | — | — |
| 11-06 h | 100% | — | +0 | -1 | +0 | +0 | +0 | +0 | -4 | — | — | — |
| 11-07 h | 52% | — | +21 | -18 | +38 | +37 | +19 | +26 | -3 | — | — | — |
| 11-08 h | 80% | — | +20 | +20 | +10 | +4 | +20 | -5 | +13 | — | — | — |
| 11-09 h | 100% | 100% | -4 | +0 | -13 | -8 | +0 | +0 | -6 | — | — | — |
| 11-10 | 56% | 100% | +44 | +44 | +44 | +44 | +44 | +19 | +34 | +44 | +41 | +38 |
| 11-11 | 93% | 97% | +7 | +6 | +5 | +6 | +7 | +7 | +2 | +7 | +4 | +6 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 17 | +0.3 | 1.8 | -0.2 | 1.4 |
| RRFS | 17 | -0.1 | 1.4 | -1.1 | 2.0 |
| IFS | 17 | -0.4 | 1.6 | -1.9 | 2.1 |
| IFS_HRES | 17 | -0.9 | 1.8 | -2.2 | 2.4 |
| GFS | 17 | -1.1 | 2.4 | -3.2 | 3.6 |
| GFS_MOS | 17 | -0.9 | 1.7 | -1.8 | 2.1 |
| NBM | 17 | -1.3 | 1.9 | -0.7 | 1.5 |
| USL | 2 | -3.6 | 3.6 | -4.1 | 4.1 |
| ENS | 2 | -0.6 | 0.6 | -2.2 | 2.2 |
| GEFS | 2 | -7.2 | 7.2 | -8.3 | 8.3 |

Night dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 39.6 | -0.8 | -0.4 | -0.4 | -0.4 | -1.9 | -1.6 | -1.1 | — | — | — |
| 10-27 h | 31.5 | +3.2 | +2.5 | +2.7 | +1.8 | +0.2 | +0.1 | +0.2 | — | — | — |
| 10-28 h | 27.8 | +4.6 | -0.2 | +4.6 | +3.6 | -1.1 | -1.4 | +1.2 | — | — | — |
| 10-29 h | 24.7 | +8.4 | +5.6 | +5.3 | +4.5 | -0.5 | -0.9 | +2.5 | — | — | — |
| 10-30 h | 26.8 | +5.8 | +5.0 | +0.8 | -1.3 | +3.2 | -0.7 | +2.9 | — | — | — |
| 10-31 h | 40.5 | -0.1 | +0.3 | +1.3 | +1.2 | +0.6 | -2.5 | -0.6 | — | — | — |
| 11-01 h | 37.6 | -0.8 | +1.8 | -1.1 | -2.1 | +2.7 | +2.7 | -0.8 | — | — | — |
| 11-02 h | 36.9 | +0.1 | -2.8 | -1.4 | -1.9 | +1.0 | +0.1 | -2.3 | — | — | — |
| 11-03 h | 36.7 | +0.5 | +0.3 | -2.0 | -2.7 | +0.8 | -0.2 | -1.0 | — | — | — |
| 11-04 h | 42.3 | -2.9 | -1.8 | -0.9 | -1.1 | -3.2 | -2.7 | -2.4 | — | — | — |
| 11-05 h | 40.2 | -0.2 | -0.1 | -0.8 | -1.1 | -1.3 | -1.0 | -3.1 | — | — | — |
| 11-06 h | 40.0 | -2.2 | -4.4 | -3.0 | -3.3 | -5.5 | -2.0 | -5.1 | — | — | — |
| 11-07 h | 39.1 | +0.7 | +0.3 | +0.7 | +0.9 | +0.6 | +0.0 | +0.0 | — | — | — |
| 11-08 h | 32.5 | -0.2 | -1.1 | -2.7 | -3.2 | -5.7 | -3.1 | -3.4 | — | — | — |
| 11-09 h | 31.2 | +2.0 | +0.2 | +0.0 | -0.8 | +2.4 | +3.4 | +0.5 | — | — | — |
| 11-10 | 39.5 | -0.5 | -0.6 | -0.2 | -0.4 | -1.6 | -2.1 | -0.8 | -2.2 | +0.0 | -5.3 |
| 11-11 | 40.0 | -2.5 | -0.3 | -2.1 | -2.4 | -4.0 | -2.0 | -2.7 | -4.8 | -1.1 | -8.8 |

Day dewpoint: observed mean (°F) and each model's error (forecast - observed, °F):

| Date | Obs | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-26 h | 40.9 | +0.5 | -0.1 | -0.1 | +0.1 | -5.8 | -1.6 | -0.3 | — | — | — |
| 10-27 h | 37.2 | +0.5 | -0.5 | -2.5 | -2.8 | -6.6 | -6.9 | -2.0 | — | — | — |
| 10-28 h | 33.1 | +5.5 | +2.1 | +0.4 | +0.1 | -8.2 | -5.6 | -1.6 | — | — | — |
| 10-29 h | 32.0 | +5.8 | +3.5 | +0.5 | -0.6 | -7.7 | -5.5 | -1.8 | — | — | — |
| 10-30 h | 31.1 | +2.6 | +3.5 | +0.2 | -0.9 | +2.4 | -1.4 | +5.1 | — | — | — |
| 10-31 h | 42.7 | -1.4 | +0.6 | +0.6 | +0.4 | -1.4 | -2.1 | +0.5 | — | — | — |
| 11-01 h | 37.1 | +0.3 | +1.7 | -1.7 | -2.5 | +0.5 | +1.5 | +1.1 | — | — | — |
| 11-02 h | 38.0 | -0.2 | +0.0 | -0.4 | -0.7 | +0.7 | +0.6 | +1.2 | — | — | — |
| 11-03 h | 37.6 | -0.6 | -1.8 | -4.6 | -5.5 | -2.6 | -0.6 | -0.3 | — | — | — |
| 11-04 h | 40.8 | -0.3 | +0.0 | -2.5 | -2.9 | -1.4 | +0.1 | +0.4 | — | — | — |
| 11-05 h | 38.8 | -2.1 | -2.7 | -2.3 | -2.3 | -1.5 | -0.2 | -0.9 | — | — | — |
| 11-06 h | 42.0 | -1.5 | -2.8 | -2.0 | -1.7 | -1.7 | -3.0 | -1.8 | — | — | — |
| 11-07 h | 37.5 | +0.2 | -0.9 | +0.9 | +1.1 | -2.2 | +0.3 | +0.2 | — | — | — |
| 11-08 h | 37.0 | -1.2 | -2.4 | -7.4 | -8.2 | -6.5 | -5.4 | -3.3 | — | — | — |
| 11-09 h | 37.0 | -0.8 | -3.2 | -1.9 | -2.0 | -4.1 | -2.3 | -1.1 | — | — | — |
| 11-10 | 37.9 | -1.1 | -4.3 | -1.6 | -1.8 | -5.3 | -0.4 | -1.4 | -3.1 | -2.5 | -7.9 |
| 11-11 | 42.3 | -1.8 | -0.7 | -2.3 | -2.2 | -4.1 | -1.9 | -1.9 | -4.9 | -1.9 | -8.7 |

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | GEFS | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: |
| 11-10 | 0.89" (wet: 06-12, 12-18, 00-06) | 71/32/23/89 | 99/59/16/80 | 100/98/63/100 | 100/42/13/87 | 24h 100% | 99/58/16/80 |
| 11-11 | 0.53" (wet: 06-12, 12-18, 18-00, 00-06) | 59/76/89/85 | 81/90/95/98 | 100/100/100/100 | 42/84/100/100 | 24h 100% | 81/90/95/98 |

## Today so far (2026-11-12, through 2026-11-12T13:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 44.1 °F, low 39.0 °F, max wind 12 kt, precip 0.13" (8 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 11/18Z | -2.6 | 2.6 | 40 (-4) | 34 (-5) pending | +0.6 | 0.25 | +0.12 |
| RRFS | 11/18Z | +0.0 | 0.8 | 43 (-1) | 34 (-5) pending | +3.5 | 0.18 | +0.05 |
| IFS | 11/12Z | -1.0 | 1.2 | 43 (-1) | 34 (-4) pending | +4.0 | 0.48 | +0.35 |
| IFS_HRES | 11/12Z | -1.9 | 1.9 | 42 (-2) | 34 (-5) pending | +4.3 | 0.43 | +0.30 |
| GFS | 11/18Z | +2.4 | 2.4 | 46 (+2) | 40 (+1) | +7.1 | 0.22 | +0.09 |
| GFS_MOS | 11/18Z | -0.2 | 1.2 | 45 (+1) | 35 (-4) pending | +1.6 | — | — |
| NBM | 11/22Z | -3.3 | 3.3 | 42 (-2) | 34 (-5) pending | +1.4 | — | — |
| USL | 11/22Z | -1.2 | 1.2 | 43 (-1) | 34 (-5) pending | +0.2 | 0.37 | +0.24 |
| ENS | 11/12Z | -0.6 | 1.1 | 43 (-2) | 36 (-3) pending | +4.2 | 0.36 | +0.23 |
| GEFS | 11/18Z | -1.1 | 1.2 | 42 (-2) | 36 (-3) pending | +2.3 | 0.19 | +0.06 |

## Clouds so far today (2026-11-12, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (AKST) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 100 | 100 | 100 | 75 | 100 | 100 | 100 | 100 | 86 | 95 | 92 | 94 |
| 11-12 07Z | Wed 22:00 | 100 | 100 | 100 | 96 |  | 100 |  |  | 93 | 96 | 94 | 94 |
| 11-12 08Z | Wed 23:00 | 100 | 100 | 100 | 94 |  | 100 |  |  | 93 | 98 | 95 | 95 |
| 11-12 09Z | Thu 00:00 | 100 | 100 | 100 | 83 | 100 | 100 | 100 | 100 | 91 | 100 | 96 | 96 |
| 11-12 10Z | Thu 01:00 | 100 | 100 | 100 | 85 |  | 100 |  |  | 86 | 99 | 92 | 95 |
| 11-12 11Z | Thu 02:00 | 98 | 75 | 100 | 70 |  | 100 |  |  | 92 | 96 | 87 | 94 |
| 11-12 12Z | Thu 03:00 | 84 | 44 | 100 | 64 | 72 | 80 | 7 | 100 | 82 | 91 | 84 | 92 |
| 11-12 13Z | Thu 04:00 | 100 | 44 | 100 | 16 |  | 100 |  |  | 71 | 84 | 86 | 88 |
| 11-12 14Z | Thu 05:00 | 100 | 100 | 100 | 37 |  | 100 |  |  | 83 | 76 | 90 | 84 |

## Dewpoint so far today (2026-11-12, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (AKST) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 41.0 | 96 | 37.6 | 36.6 | 39.9 | 40.1 | 40.5 | 41.0 | 40.0 | 39.0 | 40.1 | 38.2 |
| 11-12 07Z | Wed 22:00 | 41.0 | 96 | 39.1 | 40.4 |  | 39.7 |  |  |  | 39.0 | 40.0 | 38.2 |
| 11-12 08Z | Wed 23:00 | 41.0 | 89 | 39.3 | 40.4 |  | 39.1 |  |  |  | 39.0 | 39.8 | 38.2 |
| 11-12 09Z | Thu 00:00 | 39.0 | 82 | 39.1 | 40.2 | 39.8 | 39.7 | 40.1 | 40.0 | 39.0 | 38.0 | 39.5 | 38.0 |
| 11-12 10Z | Thu 01:00 | 37.0 | 82 | 36.6 | 40.7 |  | 39.3 |  |  |  | 38.0 | 39.2 | 37.6 |
| 11-12 11Z | Thu 02:00 | 39.0 | 86 | 36.9 | 39.7 |  | 39.2 |  |  |  | 36.0 | 38.7 | 37.0 |
| 11-12 12Z | Thu 03:00 | 37.0 | 89 | 37.9 | 38.2 | 38.0 | 38.2 | 36.3 | 38.0 | 37.0 | 35.0 | 38.3 | 36.4 |
| 11-12 13Z | Thu 04:00 | 37.9 | 92 | 37.6 | 37.3 |  | 37.5 |  |  |  | 35.0 | 37.8 | 35.7 |
| 11-12 14Z | Thu 05:00 | 37.9 | 96 | 36.6 | 37.8 |  | 36.7 |  |  |  | 35.0 | 37.3 | 34.9 |
| Bias so far |  |  |  | -1.1 | +0.1 | +0.2 | -0.1 | +0.0 | +0.7 | -0.3 | -1.9 | +0.0 | -1.8 |

## Newest runs vs obs so far today (2026-11-12)

The runs that have come out since today's deadline (HRRR, RRFS, IFS, GFS, GFS_MOS, NBM; fetched 2026-11-12 14:30Z), against the METAR nearest each hour since each run's first valid time. These runs are not scored for today; use them to judge whether the newest guidance has the current pattern right before trusting what it says for the target day. A run already a few degrees off a few hours in usually stays off. Compare its bias with the submitted run of the same model over the same hours: if the newest run is no better, its change for the target day deserves less weight. Text guidance (GFS_MOS, NBM) often starts after the last report, so it has no hours to compare yet.

How each run is doing so far (forecast - observed; Hours = hours compared). Cloud bias is in percentage points against the METAR sky cover. Precip = the run's total since its first valid time / what was observed over the same span:

| Model | Run | From | Hours | Temp bias | Temp MAE | Submitted run temp bias | Td bias | Wind bias | Cloud bias | Precip fcst / obs |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 12/12Z | 13Z | 2 | +0.4 | 0.5 | -1.4 | +1.1 | +1.2 | +28 | 0.00 / 0.01 |
| RRFS | 12/12Z | 13Z | 2 | -1.7 | 1.7 | +0.3 | -1.6 | -1.1 | -46 | 0.00 / 0.01 |
| IFS | 12/06Z | 09Z | 2 | -0.5 | 1.0 | -0.9 | +0.8 | +6.0 | +0 | 0.13 / 0.04 |
| GFS | 12/06Z | 09Z | 2 | +3.3 | 3.3 | +2.2 | -0.2 | +11.2 | +24 | 0.06 / 0.04 |
| GFS_MOS | 12/06Z | 12Z | 1 | +3.1 | 3.1 | +1.1 | +2.0 | +1.0 | +56 | — |
| NBM | 12/12Z | 18Z | 0 | — | — | — | — | — | — | — |

Rest of today (after the last report to 06Z; hourly values, so 3-hourly guidance can miss the true extreme). Day high/low = the run's extreme for the rest of the day combined with the observed high 44.1 / low 39.0 °F so far:

| Model | Run | Hours left | Max T | Min T | Max wind | Day high | Day low |
| --- | --- | --: | --: | --: | --: | --: | --: |
| HRRR | 12/12Z | 16 | 41.1 | 34.6 | 9.9 | 44.1 | 34.6 |
| RRFS | 12/12Z | 16 | 42.1 | 37.1 | 11.2 | 44.1 | 37.1 |
| IFS | 12/06Z | 6 | 38.8 | 36.4 | 10.8 | 44.1 | 36.4 |
| GFS | 12/06Z | 6 | 43.5 | 40.2 | 11.9 | 44.1 | 39.0 |
| GFS_MOS | 12/06Z | 6 | 42.0 | 35.0 | 7.0 | 44.1 | 35.0 |
| NBM | 12/12Z | 5 | 40.0 | 34.0 | 7.0 | 44.1 | 34.0 |

Hour by hour (°F, kt; obs blank after the last report):

| UTC | Local (AKST) | Obs T | Obs Td | Obs wind | HRRR T | HRRR Td | HRRR wind | RRFS T | RRFS Td | RRFS wind | IFS T | IFS Td | IFS wind | GFS T | GFS Td | GFS wind | GFS_MOS T | GFS_MOS Td | GFS_MOS wind | NBM T | NBM Td | NBM wind |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 09Z | Thu 00:00 | 44.1 | 39.0 | 10 |  |  |  |  |  |  | 42.6 | 39.4 | 20 | 45.1 | 39.9 | 22 |  |  |  |  |  |  |
| 11-12 10Z | Thu 01:00 | 42.1 | 37.0 | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 11Z | Thu 02:00 | 43.0 | 39.0 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 12Z | Thu 03:00 | 39.9 | 37.0 | 7 |  |  |  |  |  |  | 40.4 | 38.1 | 9 | 45.5 | 35.8 | 18 | 43.0 | 39.0 | 8 |  |  |  |
| 11-12 13Z | Thu 04:00 | 39.9 | 37.9 | 7 | 39.7 | 39.1 | 6 | 38.3 | 36.3 | 3 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 14Z | Thu 05:00 | 39.0 | 37.9 | 3 | 39.9 | 38.8 | 6 | 37.2 | 36.2 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 15Z | Thu 06:00 |  |  |  | 38.9 | 38.2 | 6 | 37.1 | 36.6 | 5 | 37.9 | 36.4 | 10 | 43.5 | 37.0 | 12 | 42.0 | 38.0 | 4 |  |  |  |
| 11-12 16Z | Thu 07:00 |  |  |  | 37.8 | 36.5 | 5 | 38.2 | 36.5 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 17Z | Thu 08:00 |  |  |  | 38.5 | 36.8 | 9 | 38.7 | 35.7 | 7 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 18Z | Thu 09:00 |  |  |  | 36.4 | 36.0 | 9 | 38.9 | 36.4 | 3 | 36.4 | 35.5 | 6 | 41.3 | 36.7 | 6 | 41.0 | 37.0 | 6 | 35.0 | 35.0 | 6 |
| 11-12 19Z | Thu 10:00 |  |  |  | 36.1 | 35.5 | 8 | 39.6 | 37.0 | 2 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 20Z | Thu 11:00 |  |  |  | 38.6 | 36.6 | 6 | 40.9 | 36.2 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 21Z | Thu 12:00 |  |  |  | 40.4 | 37.7 | 6 | 41.5 | 36.4 | 4 | 37.6 | 35.9 | 8 | 42.6 | 35.3 | 7 | 41.0 | 38.0 | 6 | 39.0 | 38.0 | 6 |
| 11-12 22Z | Thu 13:00 |  |  |  | 40.9 | 37.2 | 5 | 42.1 | 35.3 | 7 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 23Z | Thu 14:00 |  |  |  | 41.1 | 36.4 | 6 | 39.7 | 36.2 | 11 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 00Z | Thu 15:00 |  |  |  | 40.1 | 37.8 | 10 | 37.7 | 35.3 | 8 | 38.3 | 37.2 | 5 | 41.9 | 34.6 | 6 | 40.0 | 37.0 | 7 | 40.0 | 38.0 | 7 |
| 11-13 01Z | Thu 16:00 |  |  |  | 39.5 | 38.3 | 10 | 38.1 | 35.5 | 8 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 02Z | Thu 17:00 |  |  |  | 38.4 | 37.1 | 9 | 37.5 | 35.5 | 8 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 03Z | Thu 18:00 |  |  |  | 36.4 | 35.7 | 9 | 38.5 | 36.4 | 5 | 38.8 | 35.5 | 11 | 40.2 | 34.5 | 12 | 38.0 | 35.0 | 6 | 36.0 | 36.0 | 6 |
| 11-13 04Z | Thu 19:00 |  |  |  | 36.0 | 35.6 | 7 | 38.1 | 36.0 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 05Z | Thu 20:00 |  |  |  | 35.6 | 35.1 | 4 | 37.6 | 36.4 | 3 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 06Z | Thu 21:00 |  |  |  | 34.6 | 33.7 | 4 | 38.0 | 36.6 | 3 | 37.0 | 32.5 | 6 | 42.2 | 33.0 | 6 | 35.0 | 33.0 | 3 | 34.0 | 33.0 | 3 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (AJK): https://forecast.weather.gov/product.php?site=ajk&issuedby=ajk&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
