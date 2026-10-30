# WxChallenge forecast brief: Minneapolis, MN (KMSP)

- Station: **KMSP**
- Target day: **2026-10-31**, scored over 2026-10-31T06Z to 2026-11-01T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-31T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-30T19:12:56+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 30/12Z | 58.5 | 46.6 | 8.3 | 0.08 |
| RRFS | 30/12Z | 58.8 | 48.1 | 5.8 | 0.01 |
| IFS | 30/06Z | 58.9 | 44.2 | 5.3 | 0.01 |
| IFS_HRES | 30/06Z | 59.2 | 45.0 | 5.7 | 0.02 |
| GFS | 30/12Z | 58.6 | 51.7 | 6.7 | 0.01 |
| GFS_MOS | 30/12Z | 61.0 | 47.0 | 8.0 | 0.00 |
| NBM | 30/18Z | 58.0 | 46.0 | 9.0 | 0.04 |
| USL | 30/12Z | 57.0 | 47.0 | 12.0 | 0.03 |
| ENS | 30/06Z | 59.0 | 46.0 | 5.9 | 0.03 |
| GEFS | 30/12Z | 59.1 | 51.3 | 8.3 | 0.02 |
| HRRRCAST (precip only) | — | — | — | — | — |
| REFS (precip only) | 30/12Z | — | — | — | 0.01 |
| NBM_QMD (precip only) | 30/12Z | — | — | — | 0.08 |
| **CONSENSUS** |  | **59.7** | **46.9** | **12.2** | **0.03** |

Notes:
- IFS_HRES: not in the consensus
- GFS_MOS: MOS Q06 categories [0, 0, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members
- GEFS: ensemble mean of 31 members; not in the consensus
- HRRRCAST: failed this run (no complete 00/06/12/18Z HRRRCast cycle covering the day yet)
- REFS: median of 14 members

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: USL 0.20, GFS 0.13, NBM 0.13, GFS_MOS 0.12, RRFS 0.12, ENS 0.11, IFS 0.10, HRRR 0.10
- Low °F weights: USL 0.39, ENS 0.13, NBM 0.12, IFS 0.10, HRRR 0.07, RRFS 0.07, GFS 0.06, GFS_MOS 0.06
- Wind kt weights: USL 0.22, GFS_MOS 0.14, NBM 0.13, HRRR 0.12, RRFS 0.11, GFS 0.10, IFS 0.09, ENS 0.08
- Precip in weights: GFS_MOS 0.14, NBM 0.13, HRRR 0.13, GFS 0.13, RRFS 0.13, IFS 0.12, USL 0.12, ENS 0.11

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 56.5 | 58.4 | 59.0 | 60.1 | 61.1 | 59.0 |
| ENS | 51 | Low °F | 43.9 | 44.6 | 45.8 | 47.5 | 48.7 | 46.0 |
| ENS | 51 | Wind kt | 4.9 | 5.3 | 5.8 | 6.6 | 7.1 | 5.9 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.02 | 0.08 | 0.03 |
| GEFS | 31 | High °F | 56.3 | 57.5 | 59.1 | 61.0 | 62.4 | 59.1 |
| GEFS | 31 | Low °F | 50.4 | 50.9 | 51.3 | 51.9 | 52.4 | 51.3 |
| GEFS | 31 | Wind kt | 7.2 | 7.3 | 8.0 | 9.1 | 9.4 | 8.3 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.02 | 0.05 | 0.02 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.01 | 0.04 | 0.09 | 0.03 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 49% | 6% | 2% | 0% |
| GEFS | 42% | 3% | 0% | 0% |
| REFS | 50% | 7% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.08", p75 0.15", p90 0.19"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 17% | 21% | 11% | 13% | 21% to 49% | 0.04 (12) |
| NBM | NBS P06 | 26% | 59% | 17% | 11% | 59% to 78% | 0.03 (12) |
| ENS | member fraction | 0% | 14% | 24% | 22% | 49% | 0.09 (12) |
| GEFS | member fraction | 0% | 10% | 13% | 26% | 42% | 0.08 (12) |
| REFS | member fraction | — | — | — | — | 50% | — |
| NBM_QMD | NBM QMD | 17% | 52% | 15% | 4% | 68% | 0.04 (12) |

For reference, always forecasting the period's observed frequency (25% of 6-h blocks wet) scores Brier 0.19.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-31 06Z | Sat 01:00 | 46.6 | 48.1 | 45.2 | 45.3 | 52.2 | 50.0 | 47.0 | 47.0 | 47.0 | 51.5 |
| 10-31 07Z | Sat 02:00 | 47.0 | 48.7 |  | 45.1 |  |  |  | 47.0 | 46.9 | 51.6 |
| 10-31 08Z | Sat 03:00 | 47.3 | 48.8 |  | 45.1 |  |  |  | 47.0 | 46.7 | 51.8 |
| 10-31 09Z | Sat 04:00 | 47.2 | 49.2 | 44.4 | 45.1 | 52.3 | 50.0 | 48.0 | 47.0 | 46.6 | 51.9 |
| 10-31 10Z | Sat 05:00 | 47.4 | 49.0 |  | 45.0 |  |  |  | 47.0 | 46.5 | 51.9 |
| 10-31 11Z | Sat 06:00 | 47.8 | 48.9 |  | 47.0 |  |  |  | 47.0 | 46.6 | 51.9 |
| 10-31 12Z | Sat 07:00 | 48.2 | 49.0 | 46.7 | 47.9 | 51.8 | 50.0 | 49.0 | 48.0 | 47.0 | 52.0 |
| 10-31 13Z | Sat 08:00 | 47.9 | 49.0 |  | 48.0 |  |  |  | 48.0 | 47.8 | 52.2 |
| 10-31 14Z | Sat 09:00 | 48.3 | 49.5 |  | 49.3 |  |  |  | 49.0 | 49.0 | 52.4 |
| 10-31 15Z | Sat 10:00 | 49.7 | 50.4 | 50.9 | 51.6 | 51.9 | 52.0 | 52.0 | 50.0 | 50.5 | 53.0 |
| 10-31 16Z | Sat 11:00 | 51.8 | 51.3 |  | 52.9 |  |  |  | 51.0 | 52.4 | 54.2 |
| 10-31 17Z | Sat 12:00 | 54.1 | 54.1 |  | 54.9 |  |  |  | 53.0 | 54.5 | 55.9 |
| 10-31 18Z | Sat 13:00 | 56.4 | 56.3 | 56.2 | 56.8 | 56.3 | 57.0 | 56.0 | 54.0 | 56.3 | 57.2 |
| 10-31 19Z | Sat 14:00 | 58.5 | 57.2 |  | 58.7 |  |  |  | 55.0 | 57.6 | 58.1 |
| 10-31 20Z | Sat 15:00 | 57.7 | 58.0 |  | 59.2 |  |  |  | 56.0 | 58.5 | 58.6 |
| 10-31 21Z | Sat 16:00 | 57.5 | 58.4 | 58.8 | 59.1 | 57.9 | 60.0 | 58.0 | 56.0 | 58.9 | 58.8 |
| 10-31 22Z | Sat 17:00 | 56.3 | 58.2 |  | 58.9 |  |  |  | 56.0 | 58.5 | 58.5 |
| 10-31 23Z | Sat 18:00 | 54.7 | 57.4 |  | 57.2 |  |  |  | 55.0 | 57.5 | 57.8 |
| 11-01 00Z | Sat 19:00 | 54.6 | 56.8 | 56.7 | 57.5 | 56.3 | 59.0 | 55.0 | 55.0 | 56.6 | 57.3 |
| 11-01 01Z | Sat 20:00 | 54.6 | 56.6 |  | 57.1 |  |  |  | 55.0 | 56.1 | 57.1 |
| 11-01 02Z | Sat 21:00 | 54.2 | 56.6 |  | 57.1 |  |  |  | 54.0 | 55.7 | 57.0 |
| 11-01 03Z | Sat 22:00 | 52.2 | 56.2 | 56.4 | 56.3 | 55.9 | 57.0 | 54.0 | 54.0 | 55.3 | 56.9 |
| 11-01 04Z | Sat 23:00 | 51.9 | 55.0 |  | 56.4 |  |  |  | 54.0 | 55.0 | 56.8 |
| 11-01 05Z | Sun 00:00 | 53.0 | 54.4 |  | 56.0 |  |  |  | 54.0 | 54.8 | 56.8 |
| 11-01 06Z | Sun 01:00 | 53.8 | 54.6 | 55.4 | 55.6 | 55.8 | 54.0 | 54.0 | 54.0 | 54.5 | 56.6 |

Dewpoint (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-31 06Z | Sat 01:00 | 41.6 | 40.0 | 38.6 | 30.7 | 39.0 | 37.0 | 39.0 | 39.3 | 31.0 |
| 10-31 07Z | Sat 02:00 | 42.2 | 40.2 |  |  |  |  | 39.0 | 39.3 | 32.2 |
| 10-31 08Z | Sat 03:00 | 42.6 | 40.7 |  |  |  |  | 40.0 | 39.4 | 33.8 |
| 10-31 09Z | Sat 04:00 | 42.3 | 40.7 | 38.2 | 33.2 | 41.0 | 41.0 | 41.0 | 39.5 | 35.2 |
| 10-31 10Z | Sat 05:00 | 42.7 | 40.9 |  |  |  |  | 41.0 | 39.7 | 36.4 |
| 10-31 11Z | Sat 06:00 | 43.1 | 42.1 |  |  |  |  | 42.0 | 39.9 | 37.6 |
| 10-31 12Z | Sat 07:00 | 43.0 | 43.0 | 39.9 | 38.1 | 43.0 | 45.0 | 43.0 | 40.5 | 38.8 |
| 10-31 13Z | Sat 08:00 | 44.1 | 44.0 |  |  |  |  | 44.0 | 41.5 | 39.9 |
| 10-31 14Z | Sat 09:00 | 46.0 | 44.7 |  |  |  |  | 45.0 | 42.7 | 40.9 |
| 10-31 15Z | Sat 10:00 | 46.4 | 45.6 | 44.4 | 42.7 | 44.0 | 48.0 | 46.0 | 44.0 | 42.1 |
| 10-31 16Z | Sat 11:00 | 47.9 | 46.7 |  |  |  |  | 47.0 | 45.5 | 43.5 |
| 10-31 17Z | Sat 12:00 | 49.8 | 48.1 |  |  |  |  | 47.0 | 47.1 | 45.1 |
| 10-31 18Z | Sat 13:00 | 51.4 | 49.2 | 47.9 | 47.7 | 47.0 | 50.0 | 48.0 | 48.5 | 46.5 |
| 10-31 19Z | Sat 14:00 | 53.0 | 50.0 |  |  |  |  | 49.0 | 49.7 | 47.9 |
| 10-31 20Z | Sat 15:00 | 53.2 | 50.8 |  |  |  |  | 51.0 | 50.7 | 49.2 |
| 10-31 21Z | Sat 16:00 | 53.9 | 51.6 | 51.1 | 52.7 | 49.0 | 51.0 | 51.0 | 51.6 | 50.1 |
| 10-31 22Z | Sat 17:00 | 53.8 | 52.1 |  |  |  |  | 52.0 | 52.2 | 51.0 |
| 10-31 23Z | Sat 18:00 | 53.7 | 52.2 |  |  |  |  | 52.0 | 52.5 | 51.6 |
| 11-01 00Z | Sat 19:00 | 53.6 | 52.4 | 51.7 | 52.1 | 51.0 | 52.0 | 51.0 | 52.8 | 52.0 |
| 11-01 01Z | Sat 20:00 | 53.5 | 53.2 |  |  |  |  | 52.0 | 52.9 | 52.3 |
| 11-01 02Z | Sat 21:00 | 53.2 | 53.4 |  |  |  |  | 52.0 | 53.1 | 52.5 |
| 11-01 03Z | Sat 22:00 | 51.6 | 53.3 | 53.3 | 53.0 | 51.0 | 52.0 | 52.0 | 53.2 | 52.6 |
| 11-01 04Z | Sat 23:00 | 51.3 | 53.1 |  |  |  |  | 52.0 | 53.3 | 52.5 |
| 11-01 05Z | Sun 00:00 | 52.5 | 53.3 |  |  |  |  | 52.0 | 53.3 | 52.3 |
| 11-01 06Z | Sun 01:00 | 53.2 | 53.7 | 54.1 | 52.6 | 49.0 | 53.0 | 52.0 | 53.3 | 52.1 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (CDT) | HRRR | RRFS | IFS | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-31 06Z | Sat 01:00 | 83 | 73 | 78 | 44 | 66 | 68 | 74 | 74 | 45 |
| 10-31 07Z | Sat 02:00 | 83 | 72 |  |  |  |  | 74 | 75 | 47 |
| 10-31 08Z | Sat 03:00 | 84 | 73 |  |  |  |  | 77 | 76 | 50 |
| 10-31 09Z | Sat 04:00 | 83 | 72 | 79 | 48 | 71 | 77 | 80 | 76 | 53 |
| 10-31 10Z | Sat 05:00 | 84 | 74 |  |  |  |  | 80 | 77 | 55 |
| 10-31 11Z | Sat 06:00 | 84 | 77 |  |  |  |  | 83 | 78 | 58 |
| 10-31 12Z | Sat 07:00 | 82 | 80 | 77 | 59 | 77 | 86 | 83 | 78 | 61 |
| 10-31 13Z | Sat 08:00 | 87 | 83 |  |  |  |  | 86 | 79 | 63 |
| 10-31 14Z | Sat 09:00 | 92 | 83 |  |  |  |  | 86 | 79 | 65 |
| 10-31 15Z | Sat 10:00 | 88 | 84 | 78 | 71 | 74 | 86 | 86 | 79 | 67 |
| 10-31 16Z | Sat 11:00 | 86 | 84 |  |  |  |  | 86 | 78 | 67 |
| 10-31 17Z | Sat 12:00 | 85 | 80 |  |  |  |  | 80 | 76 | 67 |
| 10-31 18Z | Sat 13:00 | 83 | 77 | 74 | 73 | 69 | 80 | 80 | 75 | 68 |
| 10-31 19Z | Sat 14:00 | 82 | 77 |  |  |  |  | 80 | 75 | 69 |
| 10-31 20Z | Sat 15:00 | 85 | 77 |  |  |  |  | 83 | 75 | 71 |
| 10-31 21Z | Sat 16:00 | 88 | 78 | 76 | 83 | 67 | 77 | 83 | 77 | 73 |
| 10-31 22Z | Sat 17:00 | 91 | 80 |  |  |  |  | 86 | 80 | 76 |
| 10-31 23Z | Sat 18:00 | 96 | 83 |  |  |  |  | 90 | 84 | 80 |
| 11-01 00Z | Sat 19:00 | 96 | 85 | 83 | 86 | 75 | 90 | 86 | 87 | 83 |
| 11-01 01Z | Sat 20:00 | 96 | 88 |  |  |  |  | 90 | 89 | 84 |
| 11-01 02Z | Sat 21:00 | 96 | 89 |  |  |  |  | 93 | 91 | 85 |
| 11-01 03Z | Sat 22:00 | 98 | 90 | 89 | 90 | 80 | 93 | 93 | 93 | 86 |
| 11-01 04Z | Sat 23:00 | 98 | 93 |  |  |  |  | 93 | 94 | 86 |
| 11-01 05Z | Sun 00:00 | 98 | 96 |  |  |  |  | 93 | 95 | 85 |
| 11-01 06Z | Sun 01:00 | 98 | 97 | 95 | 89 | 83 | 96 | 93 | 96 | 85 |

Wind speed (kt) at the hour:

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-31 06Z | Sat 01:00 | 3.3 | 3.6 | 4.4 | 4.7 | 5.4 | 6.0 | 7.0 | 6.0 | 4.5 | 6.5 |
| 10-31 07Z | Sat 02:00 | 3.0 | 3.5 |  | 4.7 |  |  |  | 6.0 | 4.5 | 6.6 |
| 10-31 08Z | Sat 03:00 | 3.0 | 3.7 |  | 4.7 |  |  |  | 7.0 | 4.6 | 6.6 |
| 10-31 09Z | Sat 04:00 | 3.2 | 4.4 | 4.4 | 4.8 | 5.2 | 6.0 | 7.0 | 7.0 | 4.7 | 6.7 |
| 10-31 10Z | Sat 05:00 | 4.6 | 3.6 |  | 4.5 |  |  |  | 7.0 | 4.9 | 6.8 |
| 10-31 11Z | Sat 06:00 | 3.1 | 3.3 |  | 5.0 |  |  |  | 7.0 | 5.0 | 6.9 |
| 10-31 12Z | Sat 07:00 | 2.7 | 4.3 | 4.5 | 4.8 | 5.7 | 6.0 | 8.0 | 7.0 | 5.2 | 7.1 |
| 10-31 13Z | Sat 08:00 | 3.3 | 4.1 |  | 5.4 |  |  |  | 7.0 | 5.2 | 7.3 |
| 10-31 14Z | Sat 09:00 | 4.2 | 5.0 |  | 5.7 |  |  |  | 8.0 | 5.1 | 7.6 |
| 10-31 15Z | Sat 10:00 | 5.6 | 5.7 | 5.3 | 5.3 | 6.1 | 6.0 | 8.0 | 8.0 | 5.1 | 7.8 |
| 10-31 16Z | Sat 11:00 | 6.7 | 5.4 |  | 5.4 |  |  |  | 8.0 | 5.1 | 7.6 |
| 10-31 17Z | Sat 12:00 | 8.3 | 5.8 |  | 5.4 |  |  |  | 8.0 | 5.1 | 7.3 |
| 10-31 18Z | Sat 13:00 | 8.0 | 4.9 | 4.7 | 4.9 | 6.7 | 8.0 | 9.0 | 7.0 | 5.1 | 7.0 |
| 10-31 19Z | Sat 14:00 | 7.8 | 4.8 |  | 4.6 |  |  |  | 7.0 | 5.0 | 6.7 |
| 10-31 20Z | Sat 15:00 | 7.9 | 4.5 |  | 4.7 |  |  |  | 7.0 | 4.8 | 6.4 |
| 10-31 21Z | Sat 16:00 | 6.2 | 4.7 | 4.6 | 4.4 | 4.0 | 8.0 | 8.0 | 7.0 | 4.7 | 6.2 |
| 10-31 22Z | Sat 17:00 | 5.9 | 4.2 |  | 4.3 |  |  |  | 7.0 | 4.8 | 6.0 |
| 10-31 23Z | Sat 18:00 | 4.0 | 5.4 |  | 4.6 |  |  |  | 7.0 | 4.9 | 5.9 |
| 11-01 00Z | Sat 19:00 | 4.6 | 4.7 | 5.0 | 4.7 | 5.9 | 7.0 | 7.0 | 7.0 | 5.0 | 5.9 |
| 11-01 01Z | Sat 20:00 | 4.4 | 4.7 |  | 4.8 |  |  |  | 6.0 | 5.0 | 5.9 |
| 11-01 02Z | Sat 21:00 | 5.1 | 4.5 |  | 4.9 |  |  |  | 6.0 | 5.0 | 6.1 |
| 11-01 03Z | Sat 22:00 | 4.8 | 4.5 | 5.0 | 5.4 | 4.7 | 6.0 | 7.0 | 6.0 | 5.1 | 6.1 |
| 11-01 04Z | Sat 23:00 | 4.2 | 4.7 |  | 4.7 |  |  |  | 6.0 | 5.0 | 5.9 |
| 11-01 05Z | Sun 00:00 | 4.2 | 4.4 |  | 4.5 |  |  |  | 6.0 | 4.8 | 5.7 |
| 11-01 06Z | Sun 01:00 | 4.8 | 4.4 | 4.6 | 4.4 | 4.0 | 5.0 | 6.0 | 6.0 | 4.7 | 5.5 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-31 06Z | Sat 01:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-31 07Z | Sat 02:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 10-31 08Z | Sat 03:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 10-31 09Z | Sat 04:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-31 10Z | Sat 05:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 10-31 11Z | Sat 06:00 | 0.00 | 0.00 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 10-31 12Z | Sat 07:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-31 13Z | Sat 08:00 | 0.01 | 0.01 |  | 0.02 |  | 0.00 | 0.00 | 0.00 |
| 10-31 14Z | Sat 09:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.00 | 0.00 |
| 10-31 15Z | Sat 10:00 | 0.08 | 0.01 | 0.01 | 0.02 | 0.01 | 0.00 | 0.00 | 0.00 |
| 10-31 16Z | Sat 11:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.00 | 0.00 |
| 10-31 17Z | Sat 12:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.01 | 0.00 |
| 10-31 18Z | Sat 13:00 | 0.08 | 0.01 | 0.01 | 0.02 | 0.01 | 0.00 | 0.01 | 0.00 |
| 10-31 19Z | Sat 14:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.01 | 0.01 |
| 10-31 20Z | Sat 15:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.01 | 0.01 |
| 10-31 21Z | Sat 16:00 | 0.08 | 0.01 | 0.01 | 0.02 | 0.01 | 0.00 | 0.01 | 0.01 |
| 10-31 22Z | Sat 17:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.01 | 0.01 |
| 10-31 23Z | Sat 18:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.02 | 0.01 |
| 11-01 00Z | Sat 19:00 | 0.08 | 0.01 | 0.01 | 0.02 | 0.01 | 0.00 | 0.02 | 0.01 |
| 11-01 01Z | Sat 20:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.02 | 0.01 |
| 11-01 02Z | Sat 21:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.02 | 0.01 |
| 11-01 03Z | Sat 22:00 | 0.08 | 0.01 | 0.01 | 0.02 | 0.01 | 0.00 | 0.02 | 0.01 |
| 11-01 04Z | Sat 23:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.02 | 0.01 |
| 11-01 05Z | Sun 00:00 | 0.08 | 0.01 |  | 0.02 |  | 0.00 | 0.03 | 0.02 |
| 11-01 06Z | Sun 01:00 | 0.08 | 0.01 | 0.01 | 0.02 | 0.01 | 0.00 | 0.03 | 0.02 |

Total cloud cover (%):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-31 06Z | Sat 01:00 | 100 | 100 | 14 | 22 | 100 | 100 | 85 | 97 | 61 | 96 |
| 10-31 07Z | Sat 02:00 | 100 | 100 |  | 26 |  |  | 86 | 98 | 62 | 96 |
| 10-31 08Z | Sat 03:00 | 100 | 100 |  | 14 |  |  | 85 | 100 | 66 | 97 |
| 10-31 09Z | Sat 04:00 | 100 | 94 | 6 | 17 | 100 | 100 | 90 | 100 | 71 | 97 |
| 10-31 10Z | Sat 05:00 | 100 | 96 |  | 100 |  |  | 89 | 100 | 75 | 98 |
| 10-31 11Z | Sat 06:00 | 100 | 100 |  | 100 |  |  | 91 | 100 | 79 | 98 |
| 10-31 12Z | Sat 07:00 | 100 | 100 | 100 | 100 | 100 | 100 | 86 | 100 | 84 | 99 |
| 10-31 13Z | Sat 08:00 | 100 | 100 |  | 100 |  |  | 85 | 100 | 87 | 98 |
| 10-31 14Z | Sat 09:00 | 100 | 100 |  | 83 |  |  | 83 | 100 | 91 | 98 |
| 10-31 15Z | Sat 10:00 | 100 | 100 | 91 | 100 | 100 | 100 | 84 | 100 | 94 | 98 |
| 10-31 16Z | Sat 11:00 | 100 | 98 |  | 96 |  |  | 75 | 100 | 95 | 98 |
| 10-31 17Z | Sat 12:00 | 100 | 100 |  | 98 |  |  | 79 | 100 | 96 | 98 |
| 10-31 18Z | Sat 13:00 | 35 | 100 | 98 | 98 | 100 | 100 | 79 | 100 | 96 | 99 |
| 10-31 19Z | Sat 14:00 | 100 | 100 |  | 100 |  |  | 88 | 100 | 97 | 99 |
| 10-31 20Z | Sat 15:00 | 100 | 87 |  | 100 |  |  |  | 100 | 98 | 100 |
| 10-31 21Z | Sat 16:00 | 100 | 96 | 100 | 99 | 100 | 100 | 92 | 100 | 99 | 100 |
| 10-31 22Z | Sat 17:00 | 100 | 95 |  | 97 |  |  |  | 99 | 98 | 100 |
| 10-31 23Z | Sat 18:00 | 100 | 85 |  | 100 |  |  |  | 98 | 96 | 99 |
| 11-01 00Z | Sat 19:00 | 100 | 100 | 100 | 100 | 100 | 100 | 79 | 96 | 94 | 99 |
| 11-01 01Z | Sat 20:00 | 100 | 100 |  | 100 |  |  |  | 93 | 93 | 99 |
| 11-01 02Z | Sat 21:00 | 92 | 99 |  | 100 |  |  |  | 88 | 93 | 98 |
| 11-01 03Z | Sat 22:00 | 100 | 100 | 100 | 100 | 100 | 100 | 81 | 85 | 93 | 98 |
| 11-01 04Z | Sat 23:00 | 100 | 100 |  | 100 |  |  |  | 88 | 94 | 98 |
| 11-01 05Z | Sun 00:00 | 100 | 100 |  | 99 |  |  |  | 96 | 96 | 98 |
| 11-01 06Z | Sun 01:00 | 100 | 100 | 100 | 100 | 100 | 100 | 91 | 100 | 97 | 98 |

## Track record this period

Since 2026-10-12 at KMSP (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-27 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 18 | 6.4 | -1.3 | +0.0 | -2.5 | +0.04 | 2.1 | 0.9 | 2.9 | 0.08 |
| USL | 3 | 6.6 | -1.3 | +0.0 | -2.1 | +0.14 | 1.3 | 0.0 | 2.7 | 0.14 |
| NBM | 18 | 7.8 | -0.9 | +0.1 | -4.7 | +0.02 | 2.3 | 1.2 | 4.8 | 0.06 |
| GFS_MOS | 18 | 8.5 | -1.1 | +0.6 | -4.4 | +0.02 | 2.3 | 2.8 | 4.6 | 0.05 |
| RRFS | 18 | 9.4 | -1.6 | -1.3 | -6.0 | +0.04 | 2.5 | 2.3 | 6.0 | 0.09 |
| HRRR | 18 | 9.5 | -2.9 | -2.1 | -5.6 | +0.04 | 3.2 | 2.3 | 5.6 | 0.08 |
| GFS | 18 | 10.2 | -1.0 | +2.5 | -6.6 | +0.04 | 2.1 | 2.7 | 6.6 | 0.08 |
| IFS | 18 | 11.3 | -1.7 | +0.0 | -7.3 | +0.08 | 3.2 | 1.5 | 7.3 | 0.12 |
| IFS_HRES | 18 | 11.4 | -1.4 | +0.7 | -7.1 | +0.10 | 3.3 | 1.7 | 7.1 | 0.14 |
| GEFS | 3 | 12.6 | -2.9 | +1.8 | -8.0 | +0.14 | 2.9 | 1.8 | 8.0 | 0.14 |
| ENS | 3 | 12.9 | -2.7 | -0.4 | -8.7 | +0.18 | 2.7 | 1.0 | 8.7 | 0.18 |

## Daily verification (all 18 days this period)

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
| 10-29 | 13.5 | 9.0 | 7.5 | 8.5 | 6.5 | 6.0 | 7.4 | 1.5 | 7.0 | 8.5 | 3.5 | USL |

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
| 10-29 | 58 | -7 | -6 | -3 | -3 | -1 | +0 | -2 | +0 | -3 | -1 | -2 |

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
| 10-29 | 43 | -3 | +0 | +0 | +1 | +2 | +3 | -1 | +0 | +0 | +4 | +0 |

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
| 10-29 | 16 | -7 | -6 | -9 | -9 | -7 | -6 | -8 | -3 | -8 | -7 | -3 |

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
| 10-29 | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 | +0.00 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 18 | +11 | 12 | +8 | 9 |
| RRFS | 18 | +3 | 7 | +7 | 11 |
| IFS | 18 | -7 | 16 | -3 | 7 |
| IFS_HRES | 18 | -7 | 17 | -2 | 8 |
| GFS | 18 | +0 | 19 | +1 | 10 |
| GFS_MOS | 18 | -2 | 2 | +3 | 12 |
| NBM | 18 | -3 | 13 | -6 | 9 |
| USL | 3 | +3 | 28 | -6 | 6 |
| ENS | 3 | -30 | 30 | -15 | 15 |
| GEFS | 3 | -23 | 23 | -7 | 7 |

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
| 10-29 | 0% | 0% | +1 | +0 | +0 | +0 | +0 | +0 | +9 | +43 | +0 | +0 |

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
| 10-29 | 6% | 1% | +2 | -4 | -4 | -4 | -5 | -4 | -2 | -2 | -4 | -5 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 18 | +0.2 | 1.5 | +1.4 | 1.8 |
| RRFS | 18 | +0.1 | 1.6 | +0.9 | 1.2 |
| IFS | 18 | +1.2 | 2.0 | +1.9 | 2.3 |
| IFS_HRES | 17 | +1.5 | 2.1 | +2.0 | 2.7 |
| GFS | 18 | -1.5 | 2.5 | -2.5 | 2.6 |
| GFS_MOS | 18 | +0.1 | 1.8 | -0.1 | 1.9 |
| NBM | 18 | +0.6 | 1.2 | +0.0 | 1.1 |
| USL | 3 | +0.2 | 0.7 | -0.4 | 0.7 |
| ENS | 3 | +0.5 | 1.4 | +1.3 | 1.3 |
| GEFS | 3 | -3.5 | 3.5 | -2.7 | 2.7 |

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
| 10-29 | 43.4 | +1.7 | +1.6 | +0.1 | — | -2.8 | +1.3 | -0.2 | +1.1 | +0.4 | -5.0 |

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
| 10-29 | 37.4 | +3.0 | +2.1 | +2.0 | — | -4.2 | -0.8 | +0.7 | +0.4 | +2.0 | -3.1 |

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| 10-27 | 0.14" (wet: 06-12) | 73/46/3/1 | 87/52/5/5 | 100/94/24/14 | 97/90/6/6 | 24h 100% | 24h 100% | 83/52/3/4 |
| 10-28 | 0.04" (wet: 18-00, 00-06) | 0/9/87/63 | 8/16/79/78 | 4/39/98/98 | 0/42/100/97 | 24h 100% | 24h 100% | 8/16/79/78 |
| 10-29 | 0.00" (dry) | 0/0/2/0 | 0/0/1/2 | 0/0/0/0 | 0/0/0/0 | 24h 28% | 24h 0% | 0/0/0/0 |

## Today so far (2026-10-30, through 2026-10-30T18:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 54.0 °F, low 39.9 °F, max wind 9 kt, precip 0.00" (13 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 29/18Z | -1.2 | 2.1 | 53 (-1) | 41 (+1) | -1.0 | 0.00 | +0.00 |
| RRFS | 29/18Z | -2.0 | 2.0 | 55 (+1) pending | 38 (-2) | -1.4 | 0.00 | +0.00 |
| IFS | 29/12Z | +0.7 | 2.0 | 55 (+1) pending | 42 (+2) | -1.7 | 0.00 | +0.00 |
| IFS_HRES | 29/12Z | +0.3 | 1.5 | 55 (+1) pending | 42 (+2) | -1.7 | 0.00 | +0.00 |
| GFS | 29/18Z | +1.7 | 2.6 | 57 (+3) pending | 45 (+5) | -1.4 | 0.00 | +0.00 |
| GFS_MOS | 29/18Z | -1.2 | 1.2 | 57 (+3) pending | 39 (-1) | +0.1 | — | — |
| NBM | 29/22Z | -2.8 | 2.8 | 53 (-1) | 39 (-1) | -1.3 | — | — |
| USL | 29/22Z | -1.3 | 1.5 | 57 (+3) pending | 40 (+0) | +0.2 | 0.00 | +0.00 |
| ENS | 29/06Z | -0.4 | 0.9 | 56 (+2) pending | 42 (+2) | -1.8 | 0.00 | +0.00 |
| GEFS | 29/18Z | +1.5 | 2.6 | 54 (+0) pending | 45 (+5) | -0.6 | 0.00 | +0.00 |

## Clouds so far today (2026-10-30, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-19 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (CDT) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-30 06Z | Fri 01:00 | 78 |  | 100 | 25 | 95 | 98 | 84 | 0 | 66 | 50 | 73 | 68 |
| 10-30 07Z | Fri 02:00 | 99 | 44 | 100 | 71 |  | 86 |  |  | 62 | 56 | 74 | 69 |
| 10-30 08Z | Fri 03:00 | 100 | 0 | 100 | 100 |  | 99 |  |  | 52 | 63 | 74 | 66 |
| 10-30 09Z | Fri 04:00 | 99 | 19 | 100 | 69 | 86 | 88 | 97 | 0 | 54 | 68 | 72 | 63 |
| 10-30 10Z | Fri 05:00 | 0 | 19 | 100 | 65 |  | 99 |  |  | 55 | 75 | 70 | 64 |
| 10-30 11Z | Fri 06:00 | 89 | 19 | 100 | 29 |  | 96 |  |  | 37 | 84 | 66 | 66 |
| 10-30 12Z | Fri 07:00 | 100 | 44 | 14 | 15 | 92 | 88 | 35 | 0 | 29 | 87 | 63 | 67 |
| 10-30 13Z | Fri 08:00 | 100 | 44 | 18 | 100 |  | 87 |  |  | 31 | 83 | 61 | 64 |
| 10-30 14Z | Fri 09:00 | 92 | 44 | 77 | 100 |  | 92 |  |  | 47 | 77 | 59 | 59 |
| 10-30 15Z | Fri 10:00 | 32 | 75 | 43 | 100 | 100 | 98 | 100 | 19 | 40 | 76 | 60 | 60 |
| 10-30 16Z | Fri 11:00 | 100 | 75 | 41 | 98 |  | 99 |  |  | 48 | 80 | 67 | 71 |
| 10-30 17Z | Fri 12:00 | 73 | 75 | 100 | 100 |  | 99 |  |  | 68 | 85 | 76 | 87 |
| 10-30 18Z | Fri 13:00 | 100 | 75 | 100 | 100 | 100 | 100 | 100 | 75 | 64 | 90 | 80 | 99 |
| 10-30 19Z | Fri 14:00 | 100 | 75 | 100 | 100 |  | 98 |  |  | 63 | 87 | 72 | 99 |

## Dewpoint so far today (2026-10-30, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (CDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-30 07Z | Fri 02:00 | 36.0 | 73 | 41.4 | 41.2 |  | 40.3 |  |  |  | 38.0 | 39.2 | 31.5 |
| 10-30 08Z | Fri 03:00 | 37.0 | 76 | 41.5 | 40.6 |  | 40.5 |  |  |  | 38.0 | 39.2 | 31.2 |
| 10-30 09Z | Fri 04:00 | 35.1 | 68 | 40.5 | 40.1 | 39.8 | 40.5 | 30.2 | 33.0 | 36.0 | 37.0 | 39.2 | 31.0 |
| 10-30 10Z | Fri 05:00 | 36.0 | 79 | 39.9 | 40.0 |  | 40.5 |  |  |  | 37.0 | 39.0 | 30.8 |
| 10-30 11Z | Fri 06:00 | 36.0 | 82 | 40.5 | 39.9 |  | 40.5 |  |  |  | 37.0 | 38.6 | 30.5 |
| 10-30 12Z | Fri 07:00 | 36.0 | 82 | 40.2 | 38.0 | 39.6 | 39.9 | 30.0 | 32.0 | 36.0 | 36.0 | 38.4 | 30.3 |
| 10-30 13Z | Fri 08:00 | 35.1 | 76 | 39.5 | 37.6 |  | 38.8 |  |  |  | 36.0 | 38.5 | 30.0 |
| 10-30 14Z | Fri 09:00 | 35.1 | 70 | 39.6 | 39.0 |  | 39.5 |  |  |  | 36.0 | 38.6 | 29.9 |
| 10-30 15Z | Fri 10:00 | 36.0 | 66 | 39.6 | 38.2 | 38.5 | 38.8 | 29.2 | 32.0 | 35.0 | 36.0 | 38.8 | 29.8 |
| 10-30 16Z | Fri 11:00 | 37.0 | 61 | 40.3 | 38.2 |  | 38.2 |  |  |  | 36.0 | 39.1 | 29.8 |
| 10-30 17Z | Fri 12:00 | 37.0 | 54 | 41.3 | 38.8 |  | 38.2 |  |  |  | 36.0 | 39.1 | 30.0 |
| 10-30 18Z | Fri 13:00 | 36.0 | 52 | 41.7 | 39.0 | 38.6 | 38.6 | 28.8 | 33.0 | 36.0 | 36.0 | 39.1 | 30.0 |
| 10-30 19Z | Fri 14:00 | 36.0 | 50 | 41.7 | 39.0 |  | 39.2 |  |  |  | 36.0 | 39.1 | 30.3 |
| Bias so far |  |  |  | +4.6 | +3.2 | +3.3 | +3.5 | -6.2 | -3.3 | +0.0 | +0.5 | +2.9 | -5.6 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (MPX): https://forecast.weather.gov/product.php?site=mpx&issuedby=mpx&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
