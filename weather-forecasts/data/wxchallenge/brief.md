# WxChallenge forecast brief: Yakutat, AK (PAYA)

- Station: **PAYA**
- Target day: **2026-11-12**, scored over 2026-11-12T06Z to 2026-11-13T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-11-12T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-11-11T23:00:05+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 11/18Z | 40.1 | 34.4 | 9.4 | 0.74 |
| RRFS | 11/18Z | 43.0 | 33.6 | 13.5 | 0.44 |
| IFS | 11/12Z | 42.8 | 34.5 | 11.5 | 0.97 |
| IFS_HRES | 11/12Z | 42.2 | 33.7 | 17.4 | 1.02 |
| GFS | 11/18Z | 46.1 | 40.1 | 14.5 | 0.37 |
| GFS_MOS | 11/18Z | 45.0 | 35.0 | 12.0 | 0.32 |
| NBM | 11/22Z | 42.0 | 34.0 | 10.0 | 0.33 |
| USL | 11/22Z | 43.0 | 34.0 | 15.0 | 0.45 |
| ENS | 11/12Z | 42.6 | 35.9 | 13.8 | 0.71 |
| GEFS | 11/12Z | 41.6 | 36.9 | 11.4 | 0.32 |
| HRRRCAST (precip only) | — | — | — | — | — |
| REFS (precip only) | 11/18Z | — | — | — | 0.53 |
| NBM_QMD (precip only) | 11/12Z | — | — | — | 0.54 |
| **CONSENSUS** |  | **44.1** | **33.8** | **12.5** | **0.55** |

Notes:
- IFS_HRES: not in the consensus
- GFS_MOS: MOS Q06 categories [2, 1, 1, 1] -> midpoints
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

- High °F weights: GFS 0.19, GFS_MOS 0.15, NBM 0.14, IFS 0.12, USL 0.12, ENS 0.12, RRFS 0.09, HRRR 0.08 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Low °F weights: GFS_MOS 0.18, RRFS 0.15, HRRR 0.13, IFS 0.12, USL 0.12, ENS 0.12, NBM 0.12, GFS 0.06 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Wind kt weights: HRRR 0.17, RRFS 0.14, IFS 0.13, USL 0.13, ENS 0.13, GFS_MOS 0.11, NBM 0.11, GFS 0.07 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Precip in weights: IFS 0.14, ENS 0.14, NBM 0.13, RRFS 0.13, USL 0.13, HRRR 0.12, GFS 0.11, GFS_MOS 0.11 (no track record yet: USL) (using parent's track record: ENS from IFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 41.7 | 42.1 | 42.6 | 43.1 | 43.5 | 42.6 |
| ENS | 51 | Low °F | 34.4 | 35.3 | 36.0 | 36.5 | 37.4 | 35.9 |
| ENS | 51 | Wind kt | 10.0 | 11.6 | 13.5 | 16.4 | 17.8 | 13.8 |
| ENS | 51 | Precip in | 0.49 | 0.64 | 0.71 | 0.82 | 0.89 | 0.71 |
| GEFS | 31 | High °F | 40.4 | 41.0 | 41.6 | 42.3 | 42.8 | 41.6 |
| GEFS | 31 | Low °F | 35.6 | 36.2 | 37.0 | 37.6 | 38.3 | 36.9 |
| GEFS | 31 | Wind kt | 8.8 | 9.7 | 11.1 | 12.2 | 14.9 | 11.4 |
| GEFS | 31 | Precip in | 0.17 | 0.20 | 0.32 | 0.38 | 0.56 | 0.32 |
| REFS | 14 | Precip in | 0.30 | 0.43 | 0.53 | 0.67 | 0.77 | 0.54 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 100% | 98% | 86% |
| GEFS | 100% | 97% | 58% | 13% |
| REFS | 100% | 100% | 93% | 50% |

NBM QMD calibrated 24-h precip percentiles: p10 0.25", p25 0.39", p50 0.54", p75 0.85", p90 1.12"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 82% | 61% | 61% | 49% | 82% to 99% | 0.15 (4) |
| NBM | NBS P06 | 94% | 92% | 83% | 52% | 94% to 100% | 0.06 (4) |
| ENS | member fraction | 100% | 100% | 92% | 84% | 100% | 0.10 (4) |
| GEFS | member fraction | 100% | 94% | 77% | 52% | 100% | 0.09 (4) |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 94% | 92% | 83% | 52% | 100% | 0.06 (4) |

For reference, always forecasting the period's observed frequency (75% of 6-h blocks wet) scores Brier 0.19.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 40.1 | 40.9 | 42.1 | 41.3 | 45.8 | 43.0 | 40.0 | 43.0 | 42.3 | 41.3 |
| 11-12 07Z | Wed 22:00 | 39.7 | 42.9 |  | 40.4 |  |  |  | 42.0 | 42.1 | 41.3 |
| 11-12 08Z | Wed 23:00 | 39.8 | 42.8 |  | 39.9 |  |  |  | 42.0 | 41.9 | 41.3 |
| 11-12 09Z | Thu 00:00 | 39.9 | 42.9 | 41.7 | 41.0 | 44.3 | 42.0 | 39.0 | 42.0 | 41.6 | 41.2 |
| 11-12 10Z | Thu 01:00 | 39.9 | 42.6 |  | 40.3 |  |  |  | 41.0 | 41.5 | 40.9 |
| 11-12 11Z | Thu 02:00 | 39.1 | 42.3 |  | 42.2 |  |  |  | 40.0 | 41.3 | 40.6 |
| 11-12 12Z | Thu 03:00 | 38.8 | 41.0 | 40.5 | 39.7 | 44.1 | 41.0 | 38.0 | 40.0 | 41.0 | 40.2 |
| 11-12 13Z | Thu 04:00 | 38.3 | 39.8 |  | 37.9 |  |  |  | 39.0 | 40.2 | 39.8 |
| 11-12 14Z | Thu 05:00 | 37.7 | 39.8 |  | 37.4 |  |  |  | 38.0 | 39.2 | 39.2 |
| 11-12 15Z | Thu 06:00 | 37.7 | 38.4 | 37.0 | 36.4 | 42.1 | 40.0 | 36.0 | 38.0 | 38.3 | 38.8 |
| 11-12 16Z | Thu 07:00 | 37.0 | 38.3 |  | 36.1 |  |  |  | 37.0 | 37.7 | 38.3 |
| 11-12 17Z | Thu 08:00 | 34.4 | 36.0 |  | 35.5 |  |  |  | 36.0 | 37.2 | 38.0 |
| 11-12 18Z | Thu 09:00 | 35.7 | 35.7 | 36.0 | 35.6 | 41.5 | 40.0 | 35.0 | 37.0 | 37.0 | 37.9 |
| 11-12 19Z | Thu 10:00 | 36.8 | 36.7 |  | 35.4 |  |  |  | 39.0 | 37.3 | 38.3 |
| 11-12 20Z | Thu 11:00 | 37.6 | 37.6 |  | 35.6 |  |  |  | 39.0 | 38.1 | 39.0 |
| 11-12 21Z | Thu 12:00 | 37.1 | 38.5 | 36.8 | 36.6 | 40.6 | 42.0 | 39.0 | 39.0 | 38.6 | 39.5 |
| 11-12 22Z | Thu 13:00 | 39.0 | 39.5 |  | 37.9 |  |  |  | 39.0 | 38.8 | 39.4 |
| 11-12 23Z | Thu 14:00 | 39.1 | 39.4 |  | 38.0 |  |  |  | 40.0 | 38.9 | 39.2 |
| 11-13 00Z | Thu 15:00 | 38.5 | 37.3 | 37.2 | 36.4 | 40.6 | 42.0 | 40.0 | 40.0 | 38.8 | 38.9 |
| 11-13 01Z | Thu 16:00 | 37.7 | 35.9 |  | 36.2 |  |  |  | 39.0 | 38.4 | 38.6 |
| 11-13 02Z | Thu 17:00 | 37.1 | 35.1 |  | 36.0 |  |  |  | 38.0 | 37.9 | 38.2 |
| 11-13 03Z | Thu 18:00 | 37.0 | 36.5 | 35.7 | 34.5 | 41.6 | 39.0 | 36.0 | 37.0 | 37.4 | 37.9 |
| 11-13 04Z | Thu 19:00 | 36.1 | 36.6 |  | 34.2 |  |  |  | 37.0 | 37.1 | 37.8 |
| 11-13 05Z | Thu 20:00 | 35.6 | 34.4 |  | 33.7 |  |  |  | 36.0 | 36.7 | 37.7 |
| 11-13 06Z | Thu 21:00 | 34.8 | 33.7 | 35.1 | 33.7 | 42.7 | 35.0 | 34.0 | 35.0 | 36.4 | 37.5 |

Dewpoint (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 37.6 | 36.6 | 39.9 | 40.1 | 40.5 | 41.0 | 40.0 | 39.0 | 40.1 | 38.1 |
| 11-12 07Z | Wed 22:00 | 39.1 | 40.4 |  | 39.7 |  |  |  | 39.0 | 40.0 | 37.9 |
| 11-12 08Z | Wed 23:00 | 39.3 | 40.4 |  | 39.1 |  |  |  | 39.0 | 39.8 | 37.9 |
| 11-12 09Z | Thu 00:00 | 39.1 | 40.2 | 39.8 | 39.7 | 40.1 | 40.0 | 39.0 | 38.0 | 39.5 | 37.7 |
| 11-12 10Z | Thu 01:00 | 36.6 | 40.7 |  | 39.3 |  |  |  | 38.0 | 39.2 | 37.3 |
| 11-12 11Z | Thu 02:00 | 36.9 | 39.7 |  | 39.2 |  |  |  | 36.0 | 38.7 | 36.9 |
| 11-12 12Z | Thu 03:00 | 37.9 | 38.2 | 38.0 | 38.2 | 36.3 | 38.0 | 37.0 | 35.0 | 38.3 | 36.4 |
| 11-12 13Z | Thu 04:00 | 37.6 | 37.3 |  | 37.5 |  |  |  | 35.0 | 37.8 | 35.9 |
| 11-12 14Z | Thu 05:00 | 36.6 | 37.8 |  | 36.7 |  |  |  | 35.0 | 37.3 | 35.3 |
| 11-12 15Z | Thu 06:00 | 37.0 | 36.2 | 35.1 | 34.8 | 36.4 | 37.0 | 35.0 | 34.0 | 36.8 | 34.6 |
| 11-12 16Z | Thu 07:00 | 36.3 | 36.2 |  | 35.2 |  |  |  | 34.0 | 36.2 | 33.8 |
| 11-12 17Z | Thu 08:00 | 34.4 | 34.8 |  | 34.3 |  |  |  | 33.0 | 35.6 | 32.9 |
| 11-12 18Z | Thu 09:00 | 34.9 | 34.4 | 35.0 | 34.8 | 34.3 | 37.0 | 35.0 | 33.0 | 35.3 | 32.1 |
| 11-12 19Z | Thu 10:00 | 35.5 | 35.2 |  | 34.8 |  |  |  | 34.0 | 35.5 | 31.7 |
| 11-12 20Z | Thu 11:00 | 36.2 | 35.3 |  | 34.6 |  |  |  | 35.0 | 36.0 | 31.5 |
| 11-12 21Z | Thu 12:00 | 36.5 | 35.3 | 35.4 | 35.5 | 35.0 | 36.0 | 38.0 | 35.0 | 36.3 | 31.3 |
| 11-12 22Z | Thu 13:00 | 36.7 | 36.0 |  | 36.5 |  |  |  | 36.0 | 36.3 | 31.4 |
| 11-12 23Z | Thu 14:00 | 36.9 | 35.7 |  | 37.0 |  |  |  | 36.0 | 36.2 | 31.6 |
| 11-13 00Z | Thu 15:00 | 36.6 | 35.3 | 34.9 | 35.0 | 34.7 | 36.0 | 38.0 | 35.0 | 35.9 | 31.7 |
| 11-13 01Z | Thu 16:00 | 35.8 | 34.8 |  | 33.4 |  |  |  | 35.0 | 35.6 | 31.5 |
| 11-13 02Z | Thu 17:00 | 35.6 | 34.4 |  | 33.1 |  |  |  | 34.0 | 35.0 | 31.1 |
| 11-13 03Z | Thu 18:00 | 35.3 | 34.4 | 32.4 | 32.0 | 32.1 | 35.0 | 36.0 | 33.0 | 34.4 | 30.7 |
| 11-13 04Z | Thu 19:00 | 34.6 | 34.6 |  | 31.7 |  |  |  | 33.0 | 33.7 | 30.2 |
| 11-13 05Z | Thu 20:00 | 34.0 | 33.0 |  | 30.7 |  |  |  | 32.0 | 32.9 | 29.5 |
| 11-13 06Z | Thu 21:00 | 33.0 | 31.8 | 30.7 | 29.7 | 30.4 | 32.0 | 33.0 | 31.0 | 32.3 | 28.8 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 91 | 85 | 92 | 95 | 82 | 93 | 100 | 86 | 92 | 88 |
| 11-12 07Z | Wed 22:00 | 98 | 91 |  | 97 |  |  |  | 89 | 92 | 88 |
| 11-12 08Z | Wed 23:00 | 98 | 91 |  | 97 |  |  |  | 89 | 92 | 88 |
| 11-12 09Z | Thu 00:00 | 97 | 90 | 93 | 95 | 85 | 93 | 100 | 86 | 92 | 87 |
| 11-12 10Z | Thu 01:00 | 88 | 93 |  | 96 |  |  |  | 89 | 92 | 87 |
| 11-12 11Z | Thu 02:00 | 92 | 90 |  | 89 |  |  |  | 85 | 91 | 87 |
| 11-12 12Z | Thu 03:00 | 97 | 90 | 91 | 94 | 74 | 89 | 96 | 82 | 90 | 86 |
| 11-12 13Z | Thu 04:00 | 97 | 91 |  | 98 |  |  |  | 85 | 91 | 86 |
| 11-12 14Z | Thu 05:00 | 96 | 92 |  | 97 |  |  |  | 89 | 93 | 86 |
| 11-12 15Z | Thu 06:00 | 97 | 92 | 93 | 94 | 80 | 89 | 96 | 85 | 94 | 85 |
| 11-12 16Z | Thu 07:00 | 97 | 92 |  | 96 |  |  |  | 89 | 94 | 84 |
| 11-12 17Z | Thu 08:00 | 100 | 95 |  | 95 |  |  |  | 89 | 94 | 82 |
| 11-12 18Z | Thu 09:00 | 97 | 95 | 96 | 97 | 75 | 89 | 100 | 85 | 94 | 80 |
| 11-12 19Z | Thu 10:00 | 95 | 94 |  | 98 |  |  |  | 82 | 93 | 77 |
| 11-12 20Z | Thu 11:00 | 95 | 91 |  | 96 |  |  |  | 85 | 92 | 75 |
| 11-12 21Z | Thu 12:00 | 98 | 88 | 95 | 96 | 80 | 79 | 96 | 85 | 91 | 73 |
| 11-12 22Z | Thu 13:00 | 91 | 87 |  | 95 |  |  |  | 89 | 91 | 73 |
| 11-12 23Z | Thu 14:00 | 92 | 86 |  | 96 |  |  |  | 85 | 90 | 74 |
| 11-13 00Z | Thu 15:00 | 93 | 92 | 91 | 95 | 79 | 79 | 92 | 82 | 90 | 75 |
| 11-13 01Z | Thu 16:00 | 93 | 96 |  | 89 |  |  |  | 85 | 89 | 76 |
| 11-13 02Z | Thu 17:00 | 94 | 97 |  | 89 |  |  |  | 85 | 89 | 76 |
| 11-13 03Z | Thu 18:00 | 93 | 92 | 88 | 90 | 69 | 85 | 100 | 85 | 89 | 75 |
| 11-13 04Z | Thu 19:00 | 94 | 92 |  | 90 |  |  |  | 85 | 88 | 74 |
| 11-13 05Z | Thu 20:00 | 94 | 95 |  | 89 |  |  |  | 85 | 86 | 72 |
| 11-13 06Z | Thu 21:00 | 93 | 93 | 84 | 85 | 62 | 89 | 96 | 85 | 85 | 71 |

Wind speed (kt) at the hour:

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 11.3 | 14.1 | 12.6 | 12.2 | 18.8 | 12.0 | 9.0 | 9.0 | 13.9 | 10.1 |
| 11-12 07Z | Wed 22:00 | 12.0 | 12.5 |  | 11.7 |  |  |  | 9.0 | 13.2 | 9.8 |
| 11-12 08Z | Wed 23:00 | 9.6 | 11.3 |  | 11.0 |  |  |  | 8.0 | 13.0 | 9.8 |
| 11-12 09Z | Thu 00:00 | 4.2 | 12.0 | 11.5 | 10.8 | 13.5 | 11.0 | 10.0 | 8.0 | 13.0 | 9.8 |
| 11-12 10Z | Thu 01:00 | 9.4 | 11.1 |  | 17.4 |  |  |  | 8.0 | 12.0 | 9.2 |
| 11-12 11Z | Thu 02:00 | 8.9 | 13.5 |  | 12.2 |  |  |  | 7.0 | 11.3 | 8.7 |
| 11-12 12Z | Thu 03:00 | 5.2 | 12.5 | 11.4 | 10.9 | 14.5 | 7.0 | 8.0 | 7.0 | 10.9 | 8.4 |
| 11-12 13Z | Thu 04:00 | 5.4 | 6.4 |  | 9.9 |  |  |  | 6.0 | 9.5 | 7.9 |
| 11-12 14Z | Thu 05:00 | 7.8 | 5.7 |  | 8.1 |  |  |  | 6.0 | 8.4 | 7.7 |
| 11-12 15Z | Thu 06:00 | 7.5 | 6.5 | 7.9 | 7.0 | 10.9 | 4.0 | 6.0 | 5.0 | 8.3 | 7.6 |
| 11-12 16Z | Thu 07:00 | 6.5 | 7.6 |  | 4.7 |  |  |  | 4.0 | 7.5 | 7.3 |
| 11-12 17Z | Thu 08:00 | 4.3 | 8.7 |  | 1.7 |  |  |  | 4.0 | 6.0 | 7.0 |
| 11-12 18Z | Thu 09:00 | 3.7 | 8.2 | 3.5 | 2.7 | 4.7 | 5.0 | 6.0 | 4.0 | 5.1 | 6.9 |
| 11-12 19Z | Thu 10:00 | 4.7 | 7.1 |  | 4.8 |  |  |  | 5.0 | 4.6 | 6.5 |
| 11-12 20Z | Thu 11:00 | 7.8 | 6.7 |  | 4.6 |  |  |  | 5.0 | 4.5 | 6.2 |
| 11-12 21Z | Thu 12:00 | 6.7 | 6.2 | 5.1 | 4.5 | 7.1 | 8.0 | 6.0 | 5.0 | 4.7 | 6.1 |
| 11-12 22Z | Thu 13:00 | 8.8 | 7.7 |  | 5.4 |  |  |  | 5.0 | 4.9 | 5.9 |
| 11-12 23Z | Thu 14:00 | 7.4 | 7.4 |  | 2.4 |  |  |  | 5.0 | 5.8 | 6.0 |
| 11-13 00Z | Thu 15:00 | 4.6 | 7.8 | 5.1 | 4.2 | 8.5 | 7.0 | 7.0 | 6.0 | 6.6 | 6.3 |
| 11-13 01Z | Thu 16:00 | 3.6 | 5.1 |  | 6.5 |  |  |  | 6.0 | 6.5 | 6.4 |
| 11-13 02Z | Thu 17:00 | 3.6 | 4.0 |  | 5.9 |  |  |  | 6.0 | 6.3 | 6.7 |
| 11-13 03Z | Thu 18:00 | 3.5 | 4.0 | 5.8 | 5.0 | 9.3 | 6.0 | 6.0 | 5.0 | 6.1 | 7.0 |
| 11-13 04Z | Thu 19:00 | 3.8 | 3.3 |  | 4.6 |  |  |  | 5.0 | 5.2 | 7.0 |
| 11-13 05Z | Thu 20:00 | 4.5 | 3.2 |  | 3.4 |  |  |  | 4.0 | 4.1 | 7.0 |
| 11-13 06Z | Thu 21:00 | 4.6 | 4.4 | 2.3 | 1.6 | 6.0 | 3.0 | 3.0 | 4.0 | 3.3 | 6.9 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 | 0.00 | 0.00 |
| 11-12 07Z | Wed 22:00 | 0.01 | 0.06 |  | 0.06 |  | 0.08 | 0.06 | 0.02 |
| 11-12 08Z | Wed 23:00 | 0.08 | 0.12 |  | 0.13 |  | 0.13 | 0.11 | 0.04 |
| 11-12 09Z | Thu 00:00 | 0.12 | 0.14 | 0.19 | 0.20 | 0.11 | 0.18 | 0.17 | 0.07 |
| 11-12 10Z | Thu 01:00 | 0.14 | 0.15 |  | 0.34 |  | 0.23 | 0.21 | 0.09 |
| 11-12 11Z | Thu 02:00 | 0.15 | 0.17 |  | 0.35 |  | 0.28 | 0.26 | 0.11 |
| 11-12 12Z | Thu 03:00 | 0.21 | 0.17 | 0.39 | 0.40 | 0.20 | 0.32 | 0.31 | 0.14 |
| 11-12 13Z | Thu 04:00 | 0.25 | 0.18 |  | 0.42 |  | 0.35 | 0.34 | 0.15 |
| 11-12 14Z | Thu 05:00 | 0.25 | 0.18 |  | 0.43 |  | 0.37 | 0.36 | 0.17 |
| 11-12 15Z | Thu 06:00 | 0.31 | 0.18 | 0.53 | 0.56 | 0.24 | 0.38 | 0.39 | 0.18 |
| 11-12 16Z | Thu 07:00 | 0.36 | 0.18 |  | 0.61 |  | 0.39 | 0.42 | 0.20 |
| 11-12 17Z | Thu 08:00 | 0.55 | 0.20 |  | 0.64 |  | 0.39 | 0.46 | 0.22 |
| 11-12 18Z | Thu 09:00 | 0.56 | 0.27 | 0.64 | 0.67 | 0.27 | 0.39 | 0.49 | 0.24 |
| 11-12 19Z | Thu 10:00 | 0.57 | 0.30 |  | 0.75 |  | 0.39 | 0.53 | 0.24 |
| 11-12 20Z | Thu 11:00 | 0.66 | 0.35 |  | 0.79 |  | 0.40 | 0.56 | 0.25 |
| 11-12 21Z | Thu 12:00 | 0.72 | 0.38 | 0.78 | 0.81 | 0.32 | 0.41 | 0.59 | 0.26 |
| 11-12 22Z | Thu 13:00 | 0.73 | 0.44 |  | 0.82 |  | 0.41 | 0.61 | 0.27 |
| 11-12 23Z | Thu 14:00 | 0.73 | 0.44 |  | 0.84 |  | 0.41 | 0.63 | 0.28 |
| 11-13 00Z | Thu 15:00 | 0.73 | 0.44 | 0.91 | 0.95 | 0.35 | 0.41 | 0.65 | 0.29 |
| 11-13 01Z | Thu 16:00 | 0.73 | 0.44 |  | 1.01 |  | 0.41 | 0.67 | 0.29 |
| 11-13 02Z | Thu 17:00 | 0.74 | 0.44 |  | 1.01 |  | 0.41 | 0.68 | 0.30 |
| 11-13 03Z | Thu 18:00 | 0.74 | 0.44 | 0.96 | 1.01 | 0.37 | 0.41 | 0.69 | 0.31 |
| 11-13 04Z | Thu 19:00 | 0.74 | 0.44 |  | 1.01 |  | 0.41 | 0.70 | 0.31 |
| 11-13 05Z | Thu 20:00 | 0.74 | 0.44 |  | 1.02 |  | 0.41 | 0.70 | 0.32 |
| 11-13 06Z | Thu 21:00 | 0.74 | 0.44 | 0.97 | 1.02 | 0.37 | 0.41 | 0.71 | 0.32 |

Total cloud cover (%):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-12 06Z | Wed 21:00 | 100 | 75 | 100 | 100 | 100 | 100 | 86 | 95 | 92 | 92 |
| 11-12 07Z | Wed 22:00 | 100 | 96 |  | 100 |  |  | 93 | 96 | 94 | 93 |
| 11-12 08Z | Wed 23:00 | 100 | 94 |  | 100 |  |  | 93 | 98 | 95 | 95 |
| 11-12 09Z | Thu 00:00 | 100 | 83 | 100 | 100 | 100 | 100 | 91 | 100 | 96 | 97 |
| 11-12 10Z | Thu 01:00 | 100 | 85 |  | 100 |  |  | 86 | 99 | 92 | 97 |
| 11-12 11Z | Thu 02:00 | 100 | 70 |  | 100 |  |  | 92 | 96 | 87 | 96 |
| 11-12 12Z | Thu 03:00 | 100 | 64 | 72 | 80 | 7 | 100 | 82 | 91 | 84 | 96 |
| 11-12 13Z | Thu 04:00 | 100 | 16 |  | 100 |  |  | 71 | 84 | 86 | 94 |
| 11-12 14Z | Thu 05:00 | 100 | 37 |  | 100 |  |  | 83 | 76 | 90 | 93 |
| 11-12 15Z | Thu 06:00 | 100 | 33 | 100 | 99 | 87 | 100 | 74 | 71 | 94 | 92 |
| 11-12 16Z | Thu 07:00 | 100 | 97 |  | 99 |  |  | 88 | 72 | 94 | 91 |
| 11-12 17Z | Thu 08:00 | 100 | 100 |  | 100 |  |  | 81 | 76 | 94 | 90 |
| 11-12 18Z | Thu 09:00 | 100 | 100 | 100 | 100 | 99 | 100 | 87 | 81 | 94 | 90 |
| 11-12 19Z | Thu 10:00 | 100 | 100 |  | 100 |  |  | 94 | 89 | 95 | 91 |
| 11-12 20Z | Thu 11:00 | 100 | 100 |  | 100 |  |  | 93 | 96 | 95 | 93 |
| 11-12 21Z | Thu 12:00 | 100 | 98 | 98 | 98 | 100 | 100 | 91 | 100 | 95 | 94 |
| 11-12 22Z | Thu 13:00 | 100 | 84 |  | 95 |  |  | 88 | 100 | 93 | 94 |
| 11-12 23Z | Thu 14:00 | 100 | 35 |  | 79 |  |  | 74 | 100 | 89 | 95 |
| 11-13 00Z | Thu 15:00 | 100 | 11 | 94 | 92 | 100 | 100 | 64 | 100 | 86 | 95 |
| 11-13 01Z | Thu 16:00 | 100 | 9 |  | 100 |  |  |  | 100 | 82 | 93 |
| 11-13 02Z | Thu 17:00 | 100 | 79 |  | 38 |  |  |  | 100 | 78 | 92 |
| 11-13 03Z | Thu 18:00 | 85 | 85 | 59 | 57 | 92 | 100 | 85 | 100 | 75 | 90 |
| 11-13 04Z | Thu 19:00 | 98 | 70 |  | 51 |  |  |  | 100 | 76 | 88 |
| 11-13 05Z | Thu 20:00 | 100 | 24 |  | 91 |  |  |  | 99 | 77 | 85 |
| 11-13 06Z | Thu 21:00 | 100 | 100 | 98 | 99 | 100 | 75 | 84 | 99 | 77 | 83 |

## Track record this period

Since 2026-10-26 at PAYA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-11-10 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 16 | 6.6 | -0.6 | -0.6 | +0.1 | -0.09 | 0.7 | 2.0 | 2.1 | 0.24 |
| IFS_HRES | 16 | 8.1 | -1.6 | +1.5 | +1.6 | -0.08 | 2.1 | 2.1 | 2.6 | 0.19 |
| IFS | 16 | 8.4 | -1.2 | +2.4 | +2.1 | -0.07 | 1.8 | 2.6 | 3.1 | 0.18 |
| GFS_MOS | 16 | 8.8 | +0.1 | -0.5 | -3.6 | -0.12 | 1.3 | 1.6 | 3.8 | 0.34 |
| NBM | 16 | 8.8 | -1.4 | -1.5 | -3.9 | -0.12 | 1.5 | 2.8 | 4.0 | 0.21 |
| RRFS | 16 | 9.6 | -2.3 | +1.3 | -1.7 | -0.08 | 2.5 | 2.0 | 3.0 | 0.23 |
| HRRR | 16 | 10.4 | -2.6 | +1.4 | -1.1 | -0.04 | 2.9 | 2.5 | 2.2 | 0.31 |
| GFS | 16 | 15.4 | +0.3 | +5.9 | +6.2 | -0.18 | 0.9 | 6.0 | 6.2 | 0.34 |
| ENS | 1 | 16.7 | -4.0 | +4.0 | +11.0 | -0.32 | 4.0 | 4.0 | 11.0 | 0.32 |
| USL | 1 | 17.7 | -5.0 | +0.0 | +19.0 | -0.32 | 5.0 | 0.0 | 19.0 | 0.32 |
| GEFS | 1 | 21.5 | -9.0 | +2.0 | -2.0 | -0.66 | 9.0 | 2.0 | 2.0 | 0.66 |

## Daily verification (all 16 days this period)

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

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 16 | +15 | 18 | +16 | 18 |
| RRFS | 16 | +7 | 19 | +11 | 17 |
| IFS | 16 | +13 | 18 | +15 | 20 |
| IFS_HRES | 16 | +12 | 18 | +15 | 18 |
| GFS | 16 | +14 | 17 | +17 | 18 |
| GFS_MOS | 16 | +2 | 13 | +11 | 14 |
| NBM | 16 | +7 | 15 | +8 | 13 |
| USL | 1 | +17 | 17 | +44 | 44 |
| ENS | 1 | +11 | 11 | +41 | 41 |
| GEFS | 1 | +14 | 14 | +38 | 38 |

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

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 16 | +0.7 | 1.7 | -0.1 | 1.3 |
| RRFS | 16 | -0.1 | 1.5 | -1.1 | 2.1 |
| IFS | 16 | -0.2 | 1.5 | -1.8 | 2.1 |
| IFS_HRES | 16 | -0.7 | 1.8 | -2.2 | 2.4 |
| GFS | 16 | -0.8 | 2.2 | -3.2 | 3.5 |
| GFS_MOS | 16 | -0.7 | 1.7 | -1.8 | 2.1 |
| NBM | 16 | -1.1 | 1.8 | -0.6 | 1.4 |
| USL | 1 | -2.2 | 2.2 | -3.1 | 3.1 |
| ENS | 1 | +0.0 | 0.0 | -2.5 | 2.5 |
| GEFS | 1 | -5.3 | 5.3 | -7.9 | 7.9 |

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

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | GEFS | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: |
| 11-10 | 0.89" (wet: 06-12, 12-18, 00-06) | 71/32/23/89 | 99/59/16/80 | 100/98/63/100 | 100/42/13/87 | 24h 100% | 99/58/16/80 |

## Today so far (2026-11-11, through 2026-11-11T22:45Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 46.9 °F, low 39.0 °F, max wind 21 kt, precip 0.23" (16 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 10/18Z | +0.0 | 1.2 | 44 (-2) | 40 (+1) | +2.1 | 0.14 | -0.09 |
| RRFS | 10/18Z | +0.5 | 1.3 | 46 (-1) | 40 (+1) | +0.1 | 0.16 | -0.07 |
| IFS | 10/12Z | +0.3 | 1.7 | 46 (-1) | 40 (+1) | +0.8 | 0.45 | +0.22 |
| IFS_HRES | 10/12Z | -0.8 | 1.5 | 46 (-1) | 40 (+1) | +0.7 | 0.47 | +0.24 |
| GFS | 10/18Z | +1.3 | 2.1 | 47 (+0) pending | 41 (+2) | +3.1 | 0.30 | +0.07 |
| GFS_MOS | 10/18Z | -0.3 | 1.4 | 46 (-1) | 39 (+0) | -0.2 | — | — |
| NBM | 10/22Z | -2.8 | 2.8 | 45 (-2) | 37 (-2) | -0.9 | — | — |
| USL | 10/22Z | -3.1 | 3.1 | 44 (-3) | 36 (-3) | -0.2 | 0.32 | +0.09 |
| ENS | 10/12Z | +0.5 | 1.6 | 46 (-1) | 41 (+2) | +1.4 | 0.52 | +0.29 |
| GEFS | 10/18Z | -3.2 | 3.2 | 42 (-4) | 38 (-2) | +3.5 | 0.25 | +0.02 |

## Clouds so far today (2026-11-11, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (AKST) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 100 | 97 | 100 |
| 11-11 07Z | Tue 22:00 | 100 | 100 | 76 | 97 |  | 100 |  |  | 91 | 100 | 97 | 97 |
| 11-11 08Z | Tue 23:00 | 100 | 100 | 100 | 86 |  | 99 |  |  | 88 | 100 | 98 | 94 |
| 11-11 09Z | Wed 00:00 | 100 | 100 | 100 | 82 | 100 | 100 | 100 | 100 | 84 | 100 | 100 | 92 |
| 11-11 10Z | Wed 01:00 | 100 | 100 | 100 | 96 |  | 100 |  |  | 91 | 100 | 100 | 93 |
| 11-11 11Z | Wed 02:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 93 | 100 | 100 | 97 |
| 11-11 12Z | Wed 03:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 95 | 100 | 100 | 99 |
| 11-11 13Z | Wed 04:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 95 | 100 | 100 | 100 |
| 11-11 14Z | Wed 05:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 95 | 100 | 100 | 100 |
| 11-11 15Z | Wed 06:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 97 | 100 | 100 | 100 |
| 11-11 16Z | Wed 07:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 96 | 100 | 100 | 100 |
| 11-11 17Z | Wed 08:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 96 | 100 | 100 | 99 |
| 11-11 18Z | Wed 09:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 100 | 100 | 99 |
| 11-11 19Z | Wed 10:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 96 | 100 | 99 | 99 |
| 11-11 20Z | Wed 11:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 94 | 100 | 99 | 99 |
| 11-11 21Z | Wed 12:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 100 | 99 | 99 |
| 11-11 22Z | Wed 13:00 | 100 | 75 | 100 | 100 |  | 100 |  |  | 94 | 100 | 96 | 99 |
| 11-11 23Z | Wed 14:00 |  | 100 | 100 | 100 |  | 100 |  |  | 96 | 100 | 94 | 100 |

## Dewpoint so far today (2026-11-11, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (AKST) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 42.1 | 93 | 40.4 | 42.2 | 40.6 | 40.2 | 40.8 | 38.0 | 40.0 | 38.0 | 41.3 | 35.0 |
| 11-11 07Z | Tue 22:00 | 41.0 | 93 | 39.7 | 41.8 |  | 39.7 |  |  |  | 38.0 | 40.4 | 34.3 |
| 11-11 08Z | Tue 23:00 | 39.9 | 89 | 37.1 | 40.7 |  | 35.8 |  |  |  | 36.0 | 38.8 | 33.1 |
| 11-11 09Z | Wed 00:00 | 39.9 | 89 | 36.5 | 39.3 | 34.3 | 33.5 | 36.4 | 39.0 | 37.0 | 36.0 | 37.5 | 31.8 |
| 11-11 10Z | Wed 01:00 | 39.9 | 100 | 37.4 | 37.8 |  | 33.3 |  |  |  | 35.0 | 37.4 | 30.8 |
| 11-11 11Z | Wed 02:00 | 39.9 | 100 | 35.4 | 38.2 |  | 37.3 |  |  |  | 34.0 | 37.9 | 29.7 |
| 11-11 12Z | Wed 03:00 | 39.0 | 97 | 36.3 | 38.0 | 37.5 | 37.5 | 33.3 | 38.0 | 36.0 | 34.0 | 38.3 | 29.1 |
| 11-11 13Z | Wed 04:00 | 39.0 | 97 | 35.2 | 38.7 |  | 37.5 |  |  |  | 34.0 | 38.6 | 29.2 |
| 11-11 14Z | Wed 05:00 | 41.0 | 93 | 33.8 | 40.7 |  | 38.8 |  |  |  | 34.0 | 38.9 | 29.7 |
| 11-11 15Z | Wed 06:00 | 39.9 | 96 | 38.4 | 39.9 | 39.6 | 39.7 | 34.3 | 37.0 | 37.0 | 34.0 | 39.1 | 30.2 |
| 11-11 16Z | Wed 07:00 | 39.9 | 100 | 39.7 | 39.3 |  | 38.9 |  |  |  | 35.0 | 39.2 | 30.5 |
| 11-11 17Z | Wed 08:00 | 39.0 | 97 | 40.0 | 39.7 |  | 39.1 |  |  |  | 35.0 | 39.4 | 30.9 |
| 11-11 18Z | Wed 09:00 | 39.9 | 96 | 39.2 | 40.4 | 40.1 | 40.0 | 38.9 | 38.0 | 38.0 | 36.0 | 39.5 | 31.3 |
| 11-11 19Z | Wed 10:00 | 42.1 | 97 | 39.1 | 41.8 |  | 39.4 |  |  |  | 37.0 | 39.9 | 31.7 |
| 11-11 20Z | Wed 11:00 | 42.1 | 100 | 39.9 | 42.3 |  | 39.8 |  |  |  | 37.0 | 40.3 | 32.2 |
| 11-11 21Z | Wed 12:00 | 43.0 | 93 | 40.5 | 42.0 | 39.4 | 39.5 | 37.4 | 41.0 | 41.0 | 38.0 | 40.6 | 32.9 |
| 11-11 22Z | Wed 13:00 | 44.1 | 90 | 41.7 | 42.2 |  | 38.9 |  |  |  | 38.0 | 40.8 | 34.2 |
| 11-11 23Z | Wed 14:00 | 43.0 | 93 | 43.0 | 42.2 |  | 42.9 |  |  |  | 38.0 | 40.9 | 35.8 |
| Bias so far |  |  |  | -2.3 | -0.4 | -2.0 | -2.4 | -3.8 | -2.1 | -2.5 | -4.9 | -1.4 | -9.0 |

## Newest runs vs obs so far today (2026-11-11)

The runs that have come out since today's deadline (HRRR, RRFS, IFS, GFS, GFS_MOS, NBM; fetched 2026-11-11 23:00Z), against the METAR nearest each hour since each run's first valid time. These runs are not scored for today; use them to judge whether the newest guidance has the current pattern right before trusting what it says for the target day. A run already a few degrees off a few hours in usually stays off. Compare its bias with the submitted run of the same model over the same hours: if the newest run is no better, its change for the target day deserves less weight. Text guidance (GFS_MOS, NBM) often starts after the last report, so it has no hours to compare yet.

How each run is doing so far (forecast - observed; Hours = hours compared). Cloud bias is in percentage points against the METAR sky cover. Precip = the run's total since its first valid time / what was observed over the same span:

| Model | Run | From | Hours | Temp bias | Temp MAE | Submitted run temp bias | Td bias | Wind bias | Cloud bias | Precip fcst / obs |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 11/18Z | 19Z | 5 | -3.2 | 3.2 | -0.7 | -3.3 | -2.2 | +5 | 0.03 / 0.03 |
| RRFS | 11/18Z | 19Z | 5 | -1.4 | 1.6 | -1.0 | -2.4 | -3.1 | +4 | 0.09 / 0.03 |
| IFS | 11/12Z | 15Z | 3 | -2.0 | 2.0 | -1.0 | -1.8 | -1.6 | +0 | 0.48 / 0.17 |
| GFS | 11/18Z | 21Z | 1 | -2.6 | 2.6 | -1.7 | -4.6 | -1.2 | +0 | 0.00 / 0.00 |
| GFS_MOS | 11/18Z | 00Z | 0 | — | — | — | — | — | — | — |
| NBM | 11/22Z | 03Z | 0 | — | — | — | — | — | — | — |

Rest of today (after the last report to 06Z; hourly values, so 3-hourly guidance can miss the true extreme). Day high/low = the run's extreme for the rest of the day combined with the observed high 46.9 / low 39.0 °F so far:

| Model | Run | Hours left | Max T | Min T | Max wind | Day high | Day low |
| --- | --- | --: | --: | --: | --: | --: | --: |
| HRRR | 11/18Z | 7 | 41.1 | 39.6 | 18.4 | 46.9 | 39.0 |
| RRFS | 11/18Z | 7 | 43.4 | 40.9 | 14.1 | 46.9 | 39.0 |
| IFS | 11/12Z | 3 | 45.4 | 42.1 | 16.3 | 46.9 | 39.0 |
| GFS | 11/18Z | 3 | 45.9 | 45.8 | 21.1 | 46.9 | 39.0 |
| GFS_MOS | 11/18Z | 3 | 45.0 | 43.0 | 14.0 | 46.9 | 39.0 |
| NBM | 11/22Z | 2 | 41.0 | 40.0 | 10.0 | 46.9 | 39.0 |

Hour by hour (°F, kt; obs blank after the last report):

| UTC | Local (AKST) | Obs T | Obs Td | Obs wind | HRRR T | HRRR Td | HRRR wind | RRFS T | RRFS Td | RRFS wind | IFS T | IFS Td | IFS wind | GFS T | GFS Td | GFS wind | GFS_MOS T | GFS_MOS Td | GFS_MOS wind | NBM T | NBM Td | NBM wind |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 15Z | Wed 06:00 | 41.0 | 39.9 | 3 |  |  |  |  |  |  | 40.0 | 39.3 | 3 |  |  |  |  |  |  |  |  |  |
| 11-11 16Z | Wed 07:00 | 39.9 | 39.9 | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 17Z | Wed 08:00 | 39.9 | 39.0 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 18Z | Wed 09:00 | 41.0 | 39.9 | 0 |  |  |  |  |  |  | 40.2 | 38.5 | 6 |  |  |  |  |  |  |  |  |  |
| 11-11 19Z | Wed 10:00 | 43.0 | 42.1 | 4 | 40.1 | 39.2 | 4 | 42.0 | 40.0 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 20Z | Wed 11:00 | 42.1 | 42.1 | 4 | 40.5 | 38.6 | 6 | 42.7 | 39.8 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 21Z | Wed 12:00 | 45.0 | 43.0 | 18 | 42.0 | 39.9 | 8 | 43.2 | 40.4 | 8 | 40.8 | 39.5 | 8 | 42.4 | 38.4 | 17 |  |  |  |  |  |  |
| 11-11 22Z | Wed 13:00 | 46.9 | 44.1 | 21 | 42.3 | 40.7 | 13 | 44.0 | 41.8 | 17 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 23Z | Wed 14:00 | 45.0 | 43.0 | 14 | 41.3 | 39.3 | 19 | 43.1 | 40.5 | 11 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 00Z | Wed 15:00 |  |  |  | 41.1 | 38.6 | 18 | 43.4 | 41.8 | 6 | 45.4 | 40.0 | 14 | 45.8 | 41.5 | 16 | 45.0 | 43.0 | 14 |  |  |  |
| 11-12 01Z | Wed 16:00 |  |  |  | 40.7 | 39.1 | 11 | 42.6 | 39.8 | 8 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 02Z | Wed 17:00 |  |  |  | 40.6 | 39.5 | 6 | 42.3 | 40.4 | 7 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 03Z | Wed 18:00 |  |  |  | 40.5 | 39.3 | 7 | 41.5 | 38.4 | 8 | 42.3 | 40.0 | 16 | 45.9 | 39.8 | 21 | 44.0 | 42.0 | 14 | 41.0 | 41.0 | 10 |
| 11-12 04Z | Wed 19:00 |  |  |  | 40.0 | 37.8 | 14 | 42.0 | 40.4 | 8 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 05Z | Wed 20:00 |  |  |  | 39.6 | 38.5 | 7 | 42.0 | 36.6 | 11 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-12 06Z | Wed 21:00 |  |  |  | 40.1 | 37.6 | 11 | 40.9 | 36.6 | 14 | 42.1 | 39.9 | 13 | 45.8 | 40.5 | 19 | 43.0 | 41.0 | 12 | 40.0 | 40.0 | 9 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (AJK): https://forecast.weather.gov/product.php?site=ajk&issuedby=ajk&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
