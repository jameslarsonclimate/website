# WxChallenge forecast brief: Yakutat, AK (PAYA)

- Station: **PAYA**
- Target day: **2026-11-13**, scored over 2026-11-13T06Z to 2026-11-14T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-11-13T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-11-12T23:36:08+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 12/18Z | 41.8 | 33.3 | 6.4 | 0.04 |
| RRFS | 12/18Z | 41.7 | 34.1 | 8.1 | 0.04 |
| IFS | 12/12Z | 39.7 | 34.6 | 6.9 | 0.01 |
| IFS_HRES | 12/12Z | 38.8 | 33.4 | 6.8 | 0.01 |
| GFS | 12/18Z | 42.8 | 41.0 | 10.3 | 0.00 |
| GFS_MOS | 12/18Z | 44.0 | 27.0 | 4.0 | 0.00 |
| NBM | 12/22Z | 40.0 | 29.0 | 4.0 | 0.01 |
| USL | 12/22Z | 40.0 | 29.0 | 8.0 | 0.00 |
| ENS | 12/12Z | 39.4 | 35.0 | 7.8 | 0.03 |
| GEFS | 12/12Z | 37.9 | 34.4 | 9.1 | 0.02 |
| HRRRCAST (precip only) | — | — | — | — | — |
| REFS (precip only) | 12/18Z | — | — | — | 0.03 |
| NBM_QMD (precip only) | 12/12Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **42.3** | **31.2** | **6.9** | **0.02** |

Notes:
- IFS_HRES: not in the consensus
- GFS_MOS: MOS Q06 categories [0, 0, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members
- GEFS: ensemble mean of 31 members; not in the consensus
- HRRRCAST: failed this run (HRRRCast covers the CONUS HRRR domain only)
- REFS: median of 14 members

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: GFS 0.21, GFS_MOS 0.16, NBM 0.14, IFS 0.13, RRFS 0.10, ENS 0.10, HRRR 0.08, USL 0.07
- Low °F weights: GFS_MOS 0.18, USL 0.17, RRFS 0.15, HRRR 0.12, IFS 0.12, NBM 0.11, ENS 0.10, GFS 0.06
- Wind kt weights: HRRR 0.22, RRFS 0.16, IFS 0.15, GFS_MOS 0.13, NBM 0.12, GFS 0.09, ENS 0.09, USL 0.05
- Precip in weights: IFS 0.14, NBM 0.14, USL 0.13, RRFS 0.13, HRRR 0.12, GFS 0.12, GFS_MOS 0.12, ENS 0.12

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 37.8 | 38.5 | 39.1 | 40.1 | 41.3 | 39.4 |
| ENS | 51 | Low °F | 34.0 | 34.4 | 35.1 | 35.6 | 36.0 | 35.0 |
| ENS | 51 | Wind kt | 6.0 | 6.4 | 7.5 | 8.8 | 10.1 | 7.8 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.02 | 0.04 | 0.05 | 0.03 |
| GEFS | 31 | High °F | 37.3 | 37.6 | 37.9 | 38.1 | 38.3 | 37.9 |
| GEFS | 31 | Low °F | 33.8 | 34.1 | 34.4 | 34.9 | 35.2 | 34.4 |
| GEFS | 31 | Wind kt | 6.8 | 7.3 | 8.5 | 10.7 | 12.3 | 9.1 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.04 | 0.02 |
| REFS | 14 | Precip in | 0.00 | 0.01 | 0.03 | 0.05 | 0.08 | 0.04 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 67% | 2% | 0% | 0% |
| GEFS | 26% | 6% | 0% | 0% |
| REFS | 64% | 7% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.02", p90 0.07"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 5% | 1% | 4% | 30% | 30% to 37% | 0.11 (8) |
| NBM | NBS P06 | 32% | 0% | 0% | 57% | 57% to 71% | 0.04 (8) |
| ENS | member fraction | 12% | 0% | 0% | 63% | 67% | 0.05 (8) |
| GEFS | member fraction | 0% | 0% | 0% | 26% | 26% | 0.09 (8) |
| REFS | member fraction | — | — | — | — | 64% | — |
| NBM_QMD | NBM QMD | 22% | 0% | 0% | 16% | 28% | 0.04 (8) |

For reference, always forecasting the period's observed frequency (88% of 6-h blocks wet) scores Brier 0.11.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 37.3 | 37.9 | 36.5 | 35.3 | 42.5 | 34.0 | 34.0 | 37.0 | 36.9 | 37.6 |
| 11-13 07Z | Thu 22:00 | 35.5 | 38.2 |  | 34.3 |  |  |  | 36.0 | 36.6 | 37.2 |
| 11-13 08Z | Thu 23:00 | 34.2 | 37.7 |  | 34.3 |  |  |  | 35.0 | 36.2 | 36.8 |
| 11-13 09Z | Fri 00:00 | 33.4 | 37.0 | 35.1 | 33.8 | 42.3 | 32.0 | 33.0 | 34.0 | 36.0 | 36.5 |
| 11-13 10Z | Fri 01:00 | 33.3 | 35.2 |  | 33.5 |  |  |  | 33.0 | 36.1 | 36.1 |
| 11-13 11Z | Fri 02:00 | 33.7 | 34.2 |  | 33.8 |  |  |  | 33.0 | 36.2 | 35.7 |
| 11-13 12Z | Fri 03:00 | 33.7 | 35.1 | 36.8 | 35.4 | 41.6 | 30.0 | 32.0 | 32.0 | 36.3 | 35.3 |
| 11-13 13Z | Fri 04:00 | 33.8 | 35.0 |  | 35.6 |  |  |  | 32.0 | 36.3 | 35.0 |
| 11-13 14Z | Fri 05:00 | 33.8 | 35.4 |  | 35.2 |  |  |  | 31.0 | 36.2 | 34.7 |
| 11-13 15Z | Fri 06:00 | 33.7 | 36.2 | 35.7 | 34.4 | 41.7 | 28.0 | 31.0 | 31.0 | 36.1 | 34.6 |
| 11-13 16Z | Fri 07:00 | 34.0 | 36.3 |  | 33.8 |  |  |  | 31.0 | 35.8 | 34.5 |
| 11-13 17Z | Fri 08:00 | 34.2 | 36.6 |  | 33.4 |  |  |  | 30.0 | 35.6 | 34.6 |
| 11-13 18Z | Fri 09:00 | 34.5 | 36.5 | 35.3 | 34.3 | 41.8 | 31.0 | 31.0 | 31.0 | 35.7 | 34.9 |
| 11-13 19Z | Fri 10:00 | 36.1 | 39.0 |  | 35.2 |  |  |  | 34.0 | 36.5 | 35.7 |
| 11-13 20Z | Fri 11:00 | 38.1 | 40.2 |  | 36.5 |  |  |  | 36.0 | 37.7 | 36.7 |
| 11-13 21Z | Fri 12:00 | 39.8 | 41.2 | 38.2 | 37.7 | 42.2 | 40.0 | 38.0 | 38.0 | 38.6 | 37.4 |
| 11-13 22Z | Fri 13:00 | 40.9 | 41.3 |  | 38.2 |  |  |  | 39.0 | 39.0 | 37.6 |
| 11-13 23Z | Fri 14:00 | 41.8 | 41.6 |  | 38.8 |  |  |  | 39.0 | 39.1 | 37.4 |
| 11-14 00Z | Fri 15:00 | 41.4 | 41.3 | 39.3 | 38.6 | 41.7 | 42.0 | 39.0 | 39.0 | 39.1 | 37.2 |
| 11-14 01Z | Fri 16:00 | 39.2 | 40.4 |  | 37.9 |  |  |  | 37.0 | 38.9 | 36.9 |
| 11-14 02Z | Fri 17:00 | 38.6 | 39.7 |  | 37.2 |  |  |  | 35.0 | 38.5 | 36.5 |
| 11-14 03Z | Fri 18:00 | 38.3 | 40.3 | 38.4 | 37.1 | 41.4 | 38.0 | 35.0 | 33.0 | 38.2 | 36.1 |
| 11-14 04Z | Fri 19:00 | 39.0 | 40.9 |  | 36.8 |  |  |  | 33.0 | 37.8 | 36.1 |
| 11-14 05Z | Fri 20:00 | 39.1 | 40.9 |  | 35.6 |  |  |  | 32.0 | 37.5 | 36.1 |
| 11-14 06Z | Fri 21:00 | 38.9 | 39.2 | 36.8 | 35.9 | 41.7 | 37.0 | 34.0 | 32.0 | 37.4 | 36.1 |

Dewpoint (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 35.4 | 36.2 | 33.5 | 32.6 | 34.9 | 34.0 | 34.0 | 33.0 | 33.8 | 29.0 |
| 11-13 07Z | Thu 22:00 | 34.0 | 36.6 |  | 30.9 |  |  |  | 33.0 | 33.1 | 27.8 |
| 11-13 08Z | Thu 23:00 | 32.7 | 36.0 |  | 30.1 |  |  |  | 32.0 | 32.4 | 26.7 |
| 11-13 09Z | Fri 00:00 | 31.8 | 34.1 | 30.9 | 29.9 | 32.5 | 31.0 | 32.0 | 32.0 | 32.0 | 25.6 |
| 11-13 10Z | Fri 01:00 | 31.2 | 33.2 |  | 29.8 |  |  |  | 32.0 | 32.3 | 24.6 |
| 11-13 11Z | Fri 02:00 | 31.7 | 32.5 |  | 30.9 |  |  |  | 31.0 | 32.9 | 23.6 |
| 11-13 12Z | Fri 03:00 | 32.3 | 30.5 | 34.4 | 33.8 | 30.1 | 29.0 | 31.0 | 31.0 | 33.3 | 22.8 |
| 11-13 13Z | Fri 04:00 | 32.3 | 30.3 |  | 34.2 |  |  |  | 30.0 | 33.3 | 22.2 |
| 11-13 14Z | Fri 05:00 | 32.3 | 30.3 |  | 33.5 |  |  |  | 30.0 | 33.2 | 21.8 |
| 11-13 15Z | Fri 06:00 | 32.3 | 30.8 | 33.0 | 32.7 | 27.7 | 27.0 | 29.0 | 29.0 | 33.0 | 21.6 |
| 11-13 16Z | Fri 07:00 | 32.0 | 31.2 |  | 32.0 |  |  |  | 29.0 | 32.7 | 21.5 |
| 11-13 17Z | Fri 08:00 | 31.7 | 30.8 |  | 31.9 |  |  |  | 28.0 | 32.6 | 21.7 |
| 11-13 18Z | Fri 09:00 | 31.7 | 29.9 | 33.1 | 32.7 | 26.2 | 28.0 | 30.0 | 28.0 | 32.7 | 22.0 |
| 11-13 19Z | Fri 10:00 | 32.5 | 27.0 |  | 33.8 |  |  |  | 29.0 | 33.4 | 22.6 |
| 11-13 20Z | Fri 11:00 | 34.1 | 29.6 |  | 35.2 |  |  |  | 30.0 | 34.3 | 23.3 |
| 11-13 21Z | Fri 12:00 | 34.7 | 30.1 | 37.0 | 37.2 | 25.6 | 32.0 | 35.0 | 31.0 | 34.8 | 24.0 |
| 11-13 22Z | Fri 13:00 | 34.1 | 32.8 |  | 36.6 |  |  |  | 32.0 | 34.3 | 24.5 |
| 11-13 23Z | Fri 14:00 | 29.8 | 32.5 |  | 35.3 |  |  |  | 32.0 | 33.3 | 25.0 |
| 11-14 00Z | Fri 15:00 | 29.8 | 31.6 | 33.9 | 33.5 | 27.7 | 34.0 | 33.0 | 32.0 | 32.3 | 25.4 |
| 11-14 01Z | Fri 16:00 | 32.4 | 31.1 |  | 31.4 |  |  |  | 32.0 | 31.5 | 25.4 |
| 11-14 02Z | Fri 17:00 | 33.1 | 31.8 |  | 30.7 |  |  |  | 31.0 | 30.8 | 25.4 |
| 11-14 03Z | Fri 18:00 | 34.2 | 29.8 | 31.3 | 30.9 | 27.1 | 34.0 | 31.0 | 30.0 | 30.5 | 25.4 |
| 11-14 04Z | Fri 19:00 | 36.5 | 30.5 |  | 30.3 |  |  |  | 30.0 | 30.7 | 25.6 |
| 11-14 05Z | Fri 20:00 | 37.7 | 30.5 |  | 31.9 |  |  |  | 30.0 | 31.2 | 25.9 |
| 11-14 06Z | Fri 21:00 | 37.9 | 36.1 | 32.5 | 32.5 | 28.2 | 34.0 | 31.0 | 30.0 | 31.9 | 26.4 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 93 | 94 | 89 | 90 | 74 | 100 | 100 | 85 | 89 | 71 |
| 11-13 07Z | Thu 22:00 | 94 | 94 |  | 87 |  |  |  | 89 | 87 | 69 |
| 11-13 08Z | Thu 23:00 | 94 | 94 |  | 84 |  |  |  | 89 | 86 | 67 |
| 11-13 09Z | Fri 00:00 | 94 | 89 | 84 | 85 | 68 | 96 | 96 | 92 | 85 | 65 |
| 11-13 10Z | Fri 01:00 | 92 | 92 |  | 86 |  |  |  | 96 | 86 | 63 |
| 11-13 11Z | Fri 02:00 | 92 | 93 |  | 89 |  |  |  | 92 | 88 | 61 |
| 11-13 12Z | Fri 03:00 | 95 | 83 | 91 | 94 | 63 | 96 | 96 | 96 | 89 | 60 |
| 11-13 13Z | Fri 04:00 | 94 | 83 |  | 95 |  |  |  | 92 | 89 | 59 |
| 11-13 14Z | Fri 05:00 | 94 | 81 |  | 93 |  |  |  | 96 | 89 | 59 |
| 11-13 15Z | Fri 06:00 | 95 | 81 | 90 | 93 | 57 | 96 | 92 | 92 | 88 | 59 |
| 11-13 16Z | Fri 07:00 | 92 | 82 |  | 93 |  |  |  | 92 | 89 | 59 |
| 11-13 17Z | Fri 08:00 | 90 | 79 |  | 94 |  |  |  | 92 | 89 | 59 |
| 11-13 18Z | Fri 09:00 | 89 | 77 | 92 | 94 | 54 | 88 | 96 | 88 | 89 | 59 |
| 11-13 19Z | Fri 10:00 | 87 | 62 |  | 95 |  |  |  | 82 | 88 | 59 |
| 11-13 20Z | Fri 11:00 | 85 | 66 |  | 95 |  |  |  | 79 | 88 | 58 |
| 11-13 21Z | Fri 12:00 | 82 | 64 | 95 | 98 | 52 | 73 | 89 | 76 | 86 | 58 |
| 11-13 22Z | Fri 13:00 | 77 | 72 |  | 94 |  |  |  | 76 | 83 | 59 |
| 11-13 23Z | Fri 14:00 | 62 | 70 |  | 87 |  |  |  | 76 | 80 | 61 |
| 11-14 00Z | Fri 15:00 | 63 | 68 | 81 | 82 | 57 | 73 | 79 | 76 | 77 | 62 |
| 11-14 01Z | Fri 16:00 | 76 | 69 |  | 77 |  |  |  | 82 | 75 | 63 |
| 11-14 02Z | Fri 17:00 | 80 | 73 |  | 77 |  |  |  | 85 | 74 | 64 |
| 11-14 03Z | Fri 18:00 | 85 | 66 | 75 | 78 | 57 | 85 | 85 | 89 | 74 | 65 |
| 11-14 04Z | Fri 19:00 | 91 | 66 |  | 77 |  |  |  | 89 | 75 | 66 |
| 11-14 05Z | Fri 20:00 | 95 | 66 |  | 86 |  |  |  | 92 | 78 | 67 |
| 11-14 06Z | Fri 21:00 | 96 | 89 | 84 | 87 | 58 | 89 | 89 | 92 | 81 | 68 |

Wind speed (kt) at the hour:

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 8.5 | 1.3 | 5.7 | 4.9 | 7.9 | 2.0 | 4.0 | 5.0 | 5.5 | 6.1 |
| 11-13 07Z | Thu 22:00 | 5.9 | 2.1 |  | 2.4 |  |  |  | 4.0 | 4.1 | 6.0 |
| 11-13 08Z | Thu 23:00 | 4.5 | 3.5 |  | 0.8 |  |  |  | 4.0 | 2.5 | 5.8 |
| 11-13 09Z | Fri 00:00 | 4.5 | 4.1 | 0.5 | 0.3 | 7.0 | 2.0 | 0.0 | 4.0 | 1.9 | 5.8 |
| 11-13 10Z | Fri 01:00 | 4.4 | 4.0 |  | 1.2 |  |  |  | 4.0 | 2.7 | 5.9 |
| 11-13 11Z | Fri 02:00 | 4.7 | 3.3 |  | 3.9 |  |  |  | 4.0 | 4.4 | 6.1 |
| 11-13 12Z | Fri 03:00 | 5.2 | 4.0 | 6.9 | 6.6 | 10.3 | 0.0 | 3.0 | 4.0 | 5.6 | 6.2 |
| 11-13 13Z | Fri 04:00 | 5.4 | 3.5 |  | 6.8 |  |  |  | 4.0 | 5.9 | 6.3 |
| 11-13 14Z | Fri 05:00 | 5.5 | 3.4 |  | 5.5 |  |  |  | 4.0 | 5.7 | 6.4 |
| 11-13 15Z | Fri 06:00 | 5.5 | 4.8 | 5.1 | 4.4 | 7.9 | 2.0 | 3.0 | 4.0 | 5.2 | 6.6 |
| 11-13 16Z | Fri 07:00 | 5.9 | 5.3 |  | 3.4 |  |  |  | 4.0 | 4.6 | 6.8 |
| 11-13 17Z | Fri 08:00 | 6.0 | 5.2 |  | 2.4 |  |  |  | 4.0 | 3.7 | 7.1 |
| 11-13 18Z | Fri 09:00 | 5.9 | 5.4 | 1.1 | 0.3 | 4.0 | 2.0 | 3.0 | 4.0 | 3.1 | 7.3 |
| 11-13 19Z | Fri 10:00 | 5.1 | 2.5 |  | 0.9 |  |  |  | 5.0 | 2.4 | 7.3 |
| 11-13 20Z | Fri 11:00 | 4.9 | 4.8 |  | 1.2 |  |  |  | 5.0 | 1.9 | 7.1 |
| 11-13 21Z | Fri 12:00 | 4.5 | 3.9 | 0.6 | 1.2 | 3.4 | 3.0 | 3.0 | 5.0 | 1.8 | 7.0 |
| 11-13 22Z | Fri 13:00 | 4.5 | 3.4 |  | 2.3 |  |  |  | 5.0 | 1.4 | 6.9 |
| 11-13 23Z | Fri 14:00 | 4.1 | 2.9 |  | 1.7 |  |  |  | 5.0 | 1.3 | 6.7 |
| 11-14 00Z | Fri 15:00 | 4.3 | 1.6 | 0.8 | 1.3 | 5.5 | 4.0 | 4.0 | 5.0 | 1.5 | 6.7 |
| 11-14 01Z | Fri 16:00 | 4.4 | 2.7 |  | 0.7 |  |  |  | 5.0 | 1.7 | 6.7 |
| 11-14 02Z | Fri 17:00 | 4.3 | 4.2 |  | 1.5 |  |  |  | 5.0 | 2.1 | 6.8 |
| 11-14 03Z | Fri 18:00 | 3.5 | 3.2 | 3.1 | 3.4 | 4.8 | 4.0 | 4.0 | 4.0 | 2.4 | 7.0 |
| 11-14 04Z | Fri 19:00 | 6.4 | 1.0 |  | 3.9 |  |  |  | 4.0 | 2.7 | 7.0 |
| 11-14 05Z | Fri 20:00 | 6.3 | 1.8 |  | 2.8 |  |  |  | 4.0 | 3.2 | 7.1 |
| 11-14 06Z | Fri 21:00 | 4.3 | 5.8 | 3.7 | 3.4 | 4.0 | 3.0 | 4.0 | 4.0 | 3.8 | 7.3 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 07Z | Thu 22:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 08Z | Thu 23:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 09Z | Fri 00:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 10Z | Fri 01:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 11Z | Fri 02:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 12Z | Fri 03:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 13Z | Fri 04:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 14Z | Fri 05:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 15Z | Fri 06:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 16Z | Fri 07:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 17Z | Fri 08:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 18Z | Fri 09:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 19Z | Fri 10:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 20Z | Fri 11:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 21Z | Fri 12:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-13 22Z | Fri 13:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-13 23Z | Fri 14:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-14 00Z | Fri 15:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-14 01Z | Fri 16:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-14 02Z | Fri 17:00 | 0.00 | 0.01 |  | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 11-14 03Z | Fri 18:00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11-14 04Z | Fri 19:00 | 0.02 | 0.01 |  | 0.00 |  | 0.00 | 0.01 | 0.01 |
| 11-14 05Z | Fri 20:00 | 0.03 | 0.01 |  | 0.01 |  | 0.00 | 0.02 | 0.01 |
| 11-14 06Z | Fri 21:00 | 0.04 | 0.04 | 0.01 | 0.01 | 0.00 | 0.00 | 0.03 | 0.02 |

Total cloud cover (%):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-13 06Z | Thu 21:00 | 100 | 100 | 95 | 95 | 34 | 75 | 75 | 98 | 81 | 69 |
| 11-13 07Z | Thu 22:00 | 100 | 99 |  | 89 |  |  | 69 | 86 | 72 | 63 |
| 11-13 08Z | Thu 23:00 | 16 | 96 |  | 77 |  |  | 53 | 64 | 58 | 59 |
| 11-13 09Z | Fri 00:00 | 100 | 80 | 33 | 34 | 87 | 0 | 60 | 54 | 52 | 58 |
| 11-13 10Z | Fri 01:00 | 100 | 98 |  | 12 |  |  | 75 | 61 | 57 | 62 |
| 11-13 11Z | Fri 02:00 | 100 | 100 |  | 88 |  |  | 74 | 69 | 70 | 69 |
| 11-13 12Z | Fri 03:00 | 100 | 100 | 98 | 98 | 75 | 0 | 78 | 76 | 80 | 76 |
| 11-13 13Z | Fri 04:00 | 83 | 92 |  | 96 |  |  | 73 | 82 | 84 | 81 |
| 11-13 14Z | Fri 05:00 | 100 | 100 |  | 98 |  |  | 70 | 88 | 87 | 86 |
| 11-13 15Z | Fri 06:00 | 100 | 100 | 100 | 100 | 100 | 0 | 81 | 92 | 90 | 90 |
| 11-13 16Z | Fri 07:00 | 100 | 100 |  | 99 |  |  | 84 | 93 | 93 | 93 |
| 11-13 17Z | Fri 08:00 | 100 | 100 |  | 100 |  |  | 86 | 94 | 97 | 97 |
| 11-13 18Z | Fri 09:00 | 100 | 100 | 100 | 100 | 100 | 44 | 88 | 96 | 100 | 100 |
| 11-13 19Z | Fri 10:00 | 100 | 100 |  | 100 |  |  | 90 | 98 | 100 | 100 |
| 11-13 20Z | Fri 11:00 | 100 | 100 |  | 100 |  |  | 91 | 99 | 99 | 100 |
| 11-13 21Z | Fri 12:00 | 100 | 100 | 100 | 100 | 100 | 75 | 92 | 100 | 99 | 100 |
| 11-13 22Z | Fri 13:00 | 100 | 100 |  | 100 |  |  | 94 | 100 | 99 | 100 |
| 11-13 23Z | Fri 14:00 | 100 | 100 |  | 100 |  |  | 94 | 100 | 100 | 100 |
| 11-14 00Z | Fri 15:00 | 100 | 100 | 100 | 100 | 100 | 100 | 95 | 100 | 100 | 100 |
| 11-14 01Z | Fri 16:00 | 100 | 100 |  | 100 |  |  |  | 100 | 100 | 100 |
| 11-14 02Z | Fri 17:00 | 100 | 100 |  | 100 |  |  |  | 100 | 100 | 100 |
| 11-14 03Z | Fri 18:00 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 100 | 100 | 100 |
| 11-14 04Z | Fri 19:00 | 100 | 100 |  | 100 |  |  |  | 100 | 100 | 100 |
| 11-14 05Z | Fri 20:00 | 100 | 100 |  | 100 |  |  |  | 100 | 100 | 100 |
| 11-14 06Z | Fri 21:00 | 100 | 100 | 100 | 100 | 100 | 100 | 97 | 100 | 100 | 100 |

## Track record this period

Since 2026-10-26 at PAYA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-11-10 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 17 | 6.3 | -0.6 | -0.7 | +0.0 | -0.08 | 0.8 | 1.9 | 2.0 | 0.22 |
| IFS_HRES | 17 | 8.1 | -1.5 | +1.5 | +2.0 | -0.06 | 2.0 | 2.0 | 2.9 | 0.19 |
| IFS | 17 | 8.3 | -1.2 | +2.2 | +2.4 | -0.04 | 1.7 | 2.4 | 3.4 | 0.18 |
| GFS_MOS | 17 | 8.5 | +0.0 | -0.4 | -3.8 | -0.10 | 1.3 | 1.4 | 3.9 | 0.31 |
| NBM | 17 | 8.8 | -1.4 | -1.5 | -4.3 | -0.12 | 1.5 | 2.7 | 4.4 | 0.20 |
| RRFS | 17 | 9.5 | -2.1 | +1.3 | -1.9 | -0.09 | 2.3 | 1.9 | 3.1 | 0.23 |
| HRRR | 17 | 10.3 | -2.7 | +1.4 | -1.1 | -0.05 | 2.9 | 2.3 | 2.1 | 0.30 |
| ENS | 2 | 11.7 | -2.4 | +3.0 | +5.9 | +0.00 | 2.4 | 3.0 | 5.9 | 0.32 |
| USL | 2 | 13.4 | -4.0 | -1.6 | +7.3 | -0.10 | 4.0 | 1.6 | 11.4 | 0.21 |
| GFS | 17 | 14.7 | +0.3 | +5.5 | +5.8 | -0.16 | 0.8 | 5.6 | 5.8 | 0.31 |
| GEFS | 2 | 15.1 | -6.9 | +0.4 | -3.5 | -0.32 | 6.9 | 1.5 | 3.5 | 0.33 |

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
| 11-11 | 7.8 | 8.7 | 7.4 | 7.4 | 3.2 | 4.3 | 8.8 | 9.1 | 6.6 | 8.6 | 2.8 | CONSENSUS |

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
| 11-11 | 21 | -1 | -4 | +7 | +7 | +2 | -6 | -9 | -4 | +1 | -5 | -1 |

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

## Today so far (2026-11-12, through 2026-11-12T23:07Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 44.1 °F, low 36.0 °F, max wind 12 kt, precip 0.59" (17 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 11/18Z | -2.0 | 2.0 | 40 (-4) | 34 (-2) | +1.9 | 0.73 | +0.15 |
| RRFS | 11/18Z | -0.4 | 1.0 | 43 (-1) | 34 (-2) pending | +3.8 | 0.44 | -0.15 |
| IFS | 11/12Z | -1.5 | 1.6 | 43 (-1) | 34 (-2) pending | +2.9 | 0.87 | +0.28 |
| IFS_HRES | 11/12Z | -2.1 | 2.1 | 42 (-2) | 34 (-2) pending | +2.5 | 0.85 | +0.26 |
| GFS | 11/18Z | +2.6 | 2.7 | 46 (+2) | 40 (+4) | +5.5 | 0.34 | -0.25 |
| GFS_MOS | 11/18Z | +1.1 | 1.8 | 45 (+1) | 35 (-1) pending | +2.1 | — | — |
| NBM | 11/22Z | -2.4 | 2.4 | 42 (-2) | 34 (-2) pending | +2.1 | — | — |
| USL | 11/22Z | -0.8 | 0.9 | 43 (-1) | 34 (-2) pending | +0.8 | 0.41 | -0.18 |
| ENS | 11/12Z | -0.6 | 1.0 | 43 (-2) | 36 (+0) pending | +3.3 | 0.63 | +0.04 |
| GEFS | 11/18Z | -0.6 | 1.1 | 42 (-2) | 36 (+0) | +2.7 | 0.26 | -0.33 |

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
| 11-12 15Z | Thu 06:00 | 100 | 100 | 100 | 33 | 100 | 99 | 87 | 100 | 74 | 71 | 94 | 80 |
| 11-12 16Z | Thu 07:00 | 100 | 100 | 100 | 97 |  | 99 |  |  | 88 | 72 | 94 | 79 |
| 11-12 17Z | Thu 08:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 81 | 76 | 94 | 80 |
| 11-12 18Z | Thu 09:00 | 100 | 100 | 100 | 100 | 100 | 100 | 99 | 100 | 87 | 81 | 94 | 82 |
| 11-12 19Z | Thu 10:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 94 | 89 | 95 | 84 |
| 11-12 20Z | Thu 11:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 93 | 96 | 95 | 88 |
| 11-12 21Z | Thu 12:00 | 100 | 100 | 100 | 98 | 98 | 98 | 100 | 100 | 91 | 100 | 95 | 92 |
| 11-12 22Z | Thu 13:00 | 100 | 100 | 100 | 84 |  | 95 |  |  | 88 | 100 | 93 | 94 |
| 11-12 23Z | Thu 14:00 | 100 | 100 | 100 | 35 |  | 79 |  |  | 74 | 100 | 89 | 97 |

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
| 11-12 15Z | Thu 06:00 | 37.9 | 96 | 37.0 | 36.2 | 35.1 | 34.8 | 36.4 | 37.0 | 35.0 | 34.0 | 36.8 | 34.0 |
| 11-12 16Z | Thu 07:00 | 35.1 | 93 | 36.3 | 36.2 |  | 35.2 |  |  |  | 34.0 | 36.2 | 32.9 |
| 11-12 17Z | Thu 08:00 | 36.0 | 100 | 34.4 | 34.8 |  | 34.3 |  |  |  | 33.0 | 35.6 | 31.6 |
| 11-12 18Z | Thu 09:00 | 36.0 | 96 | 34.9 | 34.4 | 35.0 | 34.8 | 34.3 | 37.0 | 35.0 | 33.0 | 35.3 | 30.7 |
| 11-12 19Z | Thu 10:00 | 37.0 | 97 | 35.5 | 35.2 |  | 34.8 |  |  |  | 34.0 | 35.5 | 30.2 |
| 11-12 20Z | Thu 11:00 | 37.9 | 96 | 36.2 | 35.3 |  | 34.6 |  |  |  | 35.0 | 36.0 | 30.1 |
| 11-12 21Z | Thu 12:00 | 39.0 | 100 | 36.5 | 35.3 | 35.4 | 35.5 | 35.0 | 36.0 | 38.0 | 35.0 | 36.3 | 30.1 |
| 11-12 22Z | Thu 13:00 | 39.9 | 96 | 36.7 | 36.0 |  | 36.5 |  |  |  | 36.0 | 36.3 | 30.4 |
| 11-12 23Z | Thu 14:00 | 37.9 | 89 | 36.9 | 35.7 |  | 37.0 |  |  |  | 36.0 | 36.2 | 30.9 |
| Bias so far |  |  |  | -1.2 | -0.9 | -1.1 | -1.1 | -1.2 | -0.1 | -1.0 | -2.4 | -0.7 | -4.0 |

## Newest runs vs obs so far today (2026-11-12)

The runs that have come out since today's deadline (HRRR, RRFS, IFS, GFS, GFS_MOS, NBM; fetched 2026-11-12 23:36Z), against the METAR nearest each hour since each run's first valid time. These runs are not scored for today; use them to judge whether the newest guidance has the current pattern right before trusting what it says for the target day. A run already a few degrees off a few hours in usually stays off. Compare its bias with the submitted run of the same model over the same hours: if the newest run is no better, its change for the target day deserves less weight. Text guidance (GFS_MOS, NBM) often starts after the last report, so it has no hours to compare yet.

How each run is doing so far (forecast - observed; Hours = hours compared). Cloud bias is in percentage points against the METAR sky cover. Precip = the run's total since its first valid time / what was observed over the same span:

| Model | Run | From | Hours | Temp bias | Temp MAE | Submitted run temp bias | Td bias | Wind bias | Cloud bias | Precip fcst / obs |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 12/18Z | 19Z | 5 | -0.7 | 1.5 | -1.7 | -2.4 | +5.3 | -2 | 0.07 / 0.18 |
| RRFS | 12/18Z | 19Z | 5 | +0.8 | 1.0 | -1.2 | -1.7 | +3.7 | -4 | 0.01 / 0.18 |
| IFS | 12/12Z | 15Z | 3 | +0.0 | 0.6 | -1.7 | -0.7 | +4.7 | +0 | 0.21 / 0.46 |
| GFS | 12/18Z | 21Z | 1 | +1.2 | 1.2 | +1.6 | -2.1 | +12.6 | +0 | 0.00 / 0.12 |
| GFS_MOS | 12/18Z | 00Z | 0 | — | — | — | — | — | — | — |
| NBM | 12/22Z | 03Z | 0 | — | — | — | — | — | — | — |

Rest of today (after the last report to 06Z; hourly values, so 3-hourly guidance can miss the true extreme). Day high/low = the run's extreme for the rest of the day combined with the observed high 44.1 / low 36.0 °F so far:

| Model | Run | Hours left | Max T | Min T | Max wind | Day high | Day low |
| --- | --- | --: | --: | --: | --: | --: | --: |
| HRRR | 12/18Z | 7 | 37.3 | 35.0 | 8.7 | 44.1 | 35.0 |
| RRFS | 12/18Z | 7 | 39.8 | 37.9 | 7.7 | 44.1 | 36.0 |
| IFS | 12/12Z | 3 | 38.4 | 36.5 | 7.2 | 44.1 | 36.0 |
| GFS | 12/18Z | 3 | 42.5 | 41.3 | 8.2 | 44.1 | 36.0 |
| GFS_MOS | 12/18Z | 3 | 40.0 | 34.0 | 4.0 | 44.1 | 34.0 |
| NBM | 12/22Z | 2 | 36.0 | 34.0 | 6.0 | 44.1 | 34.0 |

Hour by hour (°F, kt; obs blank after the last report):

| UTC | Local (AKST) | Obs T | Obs Td | Obs wind | HRRR T | HRRR Td | HRRR wind | RRFS T | RRFS Td | RRFS wind | IFS T | IFS Td | IFS wind | GFS T | GFS Td | GFS wind | GFS_MOS T | GFS_MOS Td | GFS_MOS wind | NBM T | NBM Td | NBM wind |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 15Z | Thu 06:00 | 39.0 | 37.9 | 6 |  |  |  |  |  |  | 38.6 | 37.0 | 10 |  |  |  |  |  |  |  |  |  |
| 11-12 16Z | Thu 07:00 | 37.0 | 35.1 | 8 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 17Z | Thu 08:00 | 36.0 | 36.0 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 18Z | Thu 09:00 | 37.0 | 36.0 | 4 |  |  |  |  |  |  | 37.9 | 36.9 | 5 |  |  |  |  |  |  |  |  |  |
| 11-12 19Z | Thu 10:00 | 37.9 | 37.0 | 0 | 37.9 | 36.2 | 6 | 39.4 | 36.8 | 3 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 20Z | Thu 11:00 | 39.0 | 37.9 | 3 | 39.5 | 36.3 | 4 | 40.0 | 37.5 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 21Z | Thu 12:00 | 39.0 | 39.0 | 0 | 40.4 | 34.8 | 7 | 40.8 | 37.3 | 5 | 38.4 | 37.0 | 9 | 40.2 | 36.9 | 13 |  |  |  |  |  |  |
| 11-12 22Z | Thu 13:00 | 41.0 | 39.9 | 6 | 38.9 | 35.4 | 12 | 41.1 | 35.7 | 6 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 23Z | Thu 14:00 | 41.0 | 37.9 | 0 | 37.5 | 36.8 | 7 | 40.5 | 35.7 | 10 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 00Z | Thu 15:00 |  |  |  | 35.2 | 35.0 | 7 | 39.8 | 37.1 | 7 | 38.4 | 37.1 | 7 | 41.5 | 36.5 | 8 | 40.0 | 39.0 | 4 |  |  |  |
| 11-13 01Z | Thu 16:00 |  |  |  | 35.0 | 34.7 | 6 | 39.1 | 37.0 | 8 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 02Z | Thu 17:00 |  |  |  | 35.9 | 35.3 | 6 | 39.4 | 36.4 | 7 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 03Z | Thu 18:00 |  |  |  | 36.2 | 35.5 | 5 | 38.6 | 36.2 | 4 | 37.9 | 36.6 | 6 | 41.3 | 35.9 | 8 | 38.0 | 37.0 | 3 | 36.0 | 36.0 | 6 |
| 11-13 04Z | Thu 19:00 |  |  |  | 36.5 | 35.2 | 9 | 38.7 | 36.8 | 2 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 05Z | Thu 20:00 |  |  |  | 36.1 | 35.2 | 8 | 38.2 | 35.7 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-13 06Z | Thu 21:00 |  |  |  | 37.3 | 35.4 | 8 | 37.9 | 36.2 | 1 | 36.5 | 33.5 | 6 | 42.5 | 34.9 | 8 | 34.0 | 34.0 | 2 | 34.0 | 34.0 | 4 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (AJK): https://forecast.weather.gov/product.php?site=ajk&issuedby=ajk&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
