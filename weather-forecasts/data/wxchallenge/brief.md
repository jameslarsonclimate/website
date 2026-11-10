# WxChallenge forecast brief: Yakutat, AK (PAYA)

- Station: **PAYA**
- Target day: **2026-11-11**, scored over 2026-11-11T06Z to 2026-11-12T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-11-11T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-11-10T23:24:07+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 10/18Z | 44.4 | 40.2 | 20.4 | 0.35 |
| RRFS | 10/18Z | 45.6 | 40.4 | 17.4 | 0.28 |
| IFS | 10/12Z | 46.2 | 40.1 | 28.0 | 0.72 |
| IFS_HRES | 10/12Z | 46.0 | 39.6 | 27.5 | 0.72 |
| GFS | 10/18Z | 47.2 | 41.3 | 23.0 | 0.51 |
| GFS_MOS | 10/18Z | 46.0 | 39.0 | 15.0 | 0.56 |
| NBM | 10/22Z | 45.0 | 37.0 | 12.0 | 0.50 |
| USL | 10/22Z | 44.0 | 36.0 | 17.0 | 0.64 |
| ENS | 10/12Z | 45.7 | 40.8 | 21.6 | 0.84 |
| GEFS | 10/12Z | 42.6 | 37.6 | 17.3 | 0.50 |
| HRRRCAST (precip only) | — | — | — | — | — |
| REFS (precip only) | 10/18Z | — | — | — | 0.38 |
| NBM_QMD (precip only) | 10/12Z | — | — | — | 0.77 |
| **CONSENSUS** |  | **46.1** | **38.4** | **20.4** | **0.56** |

Notes:
- IFS_HRES: not in the consensus
- GFS_MOS: MOS Q06 categories [1, 2, 2, 2] -> midpoints
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

- High °F weights: GFS 0.17, GFS_MOS 0.15, NBM 0.14, IFS 0.12, USL 0.12, ENS 0.12, RRFS 0.10, HRRR 0.08 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Low °F weights: GFS_MOS 0.20, RRFS 0.15, HRRR 0.13, IFS 0.12, USL 0.12, ENS 0.12, NBM 0.11, GFS 0.06 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Wind kt weights: HRRR 0.16, IFS 0.16, ENS 0.16, RRFS 0.12, USL 0.12, GFS_MOS 0.10, NBM 0.09, GFS 0.07 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Precip in weights: IFS 0.13, NBM 0.13, ENS 0.13, RRFS 0.13, USL 0.13, HRRR 0.11, GFS 0.11, GFS_MOS 0.11 (no track record yet: USL) (using parent's track record: ENS from IFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 44.6 | 45.2 | 45.8 | 46.4 | 46.6 | 45.7 |
| ENS | 51 | Low °F | 39.5 | 39.9 | 40.9 | 41.5 | 42.4 | 40.8 |
| ENS | 51 | Wind kt | 17.3 | 18.5 | 20.6 | 24.4 | 26.6 | 21.6 |
| ENS | 51 | Precip in | 0.62 | 0.72 | 0.82 | 0.92 | 1.04 | 0.84 |
| GEFS | 31 | High °F | 41.5 | 41.9 | 42.8 | 43.1 | 43.6 | 42.6 |
| GEFS | 31 | Low °F | 36.9 | 37.4 | 37.6 | 37.9 | 38.0 | 37.6 |
| GEFS | 31 | Wind kt | 13.2 | 14.0 | 16.9 | 19.5 | 24.1 | 17.3 |
| GEFS | 31 | Precip in | 0.31 | 0.35 | 0.49 | 0.62 | 0.75 | 0.50 |
| REFS | 14 | Precip in | 0.27 | 0.33 | 0.38 | 0.67 | 0.80 | 0.46 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 100% | 100% | 100% |
| GEFS | 100% | 100% | 97% | 45% |
| REFS | 100% | 100% | 93% | 29% |

NBM QMD calibrated 24-h precip percentiles: p10 0.44", p25 0.54", p50 0.77", p75 1.07", p90 1.20"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 59% | 76% | 89% | 85% | 89% to 100% | — |
| NBM | NBS P06 | 81% | 90% | 95% | 98% | 98% to 100% | — |
| ENS | member fraction | 100% | 100% | 100% | 100% | 100% | — |
| GEFS | member fraction | 36% | 97% | 97% | 100% | 100% | — |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 81% | 90% | 95% | 98% | 100% | — |

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 43.8 | 45.5 | 42.5 | 41.8 | 43.1 | 42.0 | 41.0 | 42.0 | 43.9 | 40.1 |
| 11-11 07Z | Tue 22:00 | 42.2 | 44.9 |  | 41.9 |  |  |  | 41.0 | 43.8 | 39.7 |
| 11-11 08Z | Tue 23:00 | 40.7 | 44.7 |  | 44.0 |  |  |  | 40.0 | 43.7 | 39.1 |
| 11-11 09Z | Wed 00:00 | 41.0 | 43.4 | 43.3 | 42.8 | 44.2 | 42.0 | 40.0 | 39.0 | 43.5 | 38.6 |
| 11-11 10Z | Wed 01:00 | 40.7 | 41.5 |  | 41.9 |  |  |  | 38.0 | 43.1 | 38.4 |
| 11-11 11Z | Wed 02:00 | 40.2 | 41.5 |  | 40.7 |  |  |  | 38.0 | 42.8 | 38.4 |
| 11-11 12Z | Wed 03:00 | 41.1 | 41.9 | 43.1 | 42.0 | 44.2 | 42.0 | 38.0 | 37.0 | 42.4 | 38.3 |
| 11-11 13Z | Wed 04:00 | 41.4 | 41.4 |  | 39.6 |  |  |  | 37.0 | 42.0 | 38.1 |
| 11-11 14Z | Wed 05:00 | 42.7 | 41.6 |  | 40.0 |  |  |  | 38.0 | 41.6 | 38.0 |
| 11-11 15Z | Wed 06:00 | 41.3 | 41.1 | 41.0 | 40.4 | 42.7 | 40.0 | 37.0 | 38.0 | 41.3 | 38.0 |
| 11-11 16Z | Wed 07:00 | 41.6 | 40.4 |  | 39.9 |  |  |  | 38.0 | 41.3 | 38.0 |
| 11-11 17Z | Wed 08:00 | 41.0 | 40.8 |  | 39.8 |  |  |  | 38.0 | 41.4 | 38.1 |
| 11-11 18Z | Wed 09:00 | 41.7 | 41.6 | 41.4 | 40.8 | 41.9 | 41.0 | 38.0 | 38.0 | 41.6 | 38.4 |
| 11-11 19Z | Wed 10:00 | 42.8 | 42.6 |  | 40.6 |  |  |  | 39.0 | 41.9 | 38.7 |
| 11-11 20Z | Wed 11:00 | 43.8 | 43.2 |  | 40.8 |  |  |  | 40.0 | 42.3 | 39.2 |
| 11-11 21Z | Wed 12:00 | 43.6 | 43.4 | 41.6 | 41.1 | 43.3 | 43.0 | 42.0 | 40.0 | 42.8 | 39.5 |
| 11-11 22Z | Wed 13:00 | 44.0 | 43.6 |  | 41.0 |  |  |  | 41.0 | 43.3 | 39.8 |
| 11-11 23Z | Wed 14:00 | 44.4 | 44.4 |  | 45.1 |  |  |  | 41.0 | 43.8 | 40.1 |
| 11-12 00Z | Wed 15:00 | 43.0 | 43.3 | 46.2 | 46.0 | 41.6 | 44.0 | 43.0 | 41.0 | 44.2 | 40.3 |
| 11-12 01Z | Wed 16:00 | 42.4 | 43.0 |  | 44.8 |  |  |  | 41.0 | 44.2 | 40.7 |
| 11-12 02Z | Wed 17:00 | 43.3 | 42.6 |  | 41.7 |  |  |  | 42.0 | 44.0 | 41.2 |
| 11-12 03Z | Wed 18:00 | 43.0 | 42.8 | 42.4 | 41.9 | 45.8 | 43.0 | 41.0 | 43.0 | 43.8 | 41.5 |
| 11-12 04Z | Wed 19:00 | 41.7 | 43.2 |  | 41.8 |  |  |  | 43.0 | 43.4 | 41.6 |
| 11-12 05Z | Wed 20:00 | 42.2 | 42.7 |  | 41.9 |  |  |  | 43.0 | 43.1 | 41.7 |
| 11-12 06Z | Wed 21:00 | 41.7 | 43.3 | 41.1 | 40.3 | 44.9 | 42.0 | 41.0 | 42.0 | 42.8 | 41.6 |

Dewpoint (°F):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 40.4 | 42.2 | 40.6 | 40.2 | 40.8 | 38.0 | 40.0 | 38.0 | 41.3 | 34.5 |
| 11-11 07Z | Tue 22:00 | 39.7 | 41.8 |  | 39.7 |  |  |  | 38.0 | 40.4 | 33.7 |
| 11-11 08Z | Tue 23:00 | 37.1 | 40.7 |  | 35.8 |  |  |  | 36.0 | 38.8 | 32.4 |
| 11-11 09Z | Wed 00:00 | 36.5 | 39.3 | 34.3 | 33.5 | 36.4 | 39.0 | 37.0 | 36.0 | 37.5 | 31.2 |
| 11-11 10Z | Wed 01:00 | 37.4 | 37.8 |  | 33.3 |  |  |  | 35.0 | 37.4 | 30.3 |
| 11-11 11Z | Wed 02:00 | 35.4 | 38.2 |  | 37.3 |  |  |  | 34.0 | 37.9 | 29.6 |
| 11-11 12Z | Wed 03:00 | 36.3 | 38.0 | 37.5 | 37.5 | 33.3 | 38.0 | 36.0 | 34.0 | 38.3 | 29.2 |
| 11-11 13Z | Wed 04:00 | 35.2 | 38.7 |  | 37.5 |  |  |  | 34.0 | 38.6 | 29.6 |
| 11-11 14Z | Wed 05:00 | 33.8 | 40.7 |  | 38.8 |  |  |  | 34.0 | 38.9 | 30.4 |
| 11-11 15Z | Wed 06:00 | 38.4 | 39.9 | 39.6 | 39.7 | 34.3 | 37.0 | 37.0 | 34.0 | 39.1 | 31.0 |
| 11-11 16Z | Wed 07:00 | 39.7 | 39.3 |  | 38.9 |  |  |  | 35.0 | 39.2 | 31.3 |
| 11-11 17Z | Wed 08:00 | 40.0 | 39.7 |  | 39.1 |  |  |  | 35.0 | 39.4 | 31.4 |
| 11-11 18Z | Wed 09:00 | 39.2 | 40.4 | 40.1 | 40.0 | 38.9 | 38.0 | 38.0 | 36.0 | 39.5 | 31.7 |
| 11-11 19Z | Wed 10:00 | 39.1 | 41.8 |  | 39.4 |  |  |  | 37.0 | 39.9 | 32.2 |
| 11-11 20Z | Wed 11:00 | 39.9 | 42.3 |  | 39.8 |  |  |  | 37.0 | 40.3 | 32.8 |
| 11-11 21Z | Wed 12:00 | 40.5 | 42.0 | 39.4 | 39.5 | 37.4 | 41.0 | 41.0 | 38.0 | 40.6 | 33.4 |
| 11-11 22Z | Wed 13:00 | 41.7 | 42.2 |  | 38.9 |  |  |  | 38.0 | 40.8 | 34.3 |
| 11-11 23Z | Wed 14:00 | 43.0 | 42.2 |  | 42.9 |  |  |  | 38.0 | 40.9 | 35.4 |
| 11-12 00Z | Wed 15:00 | 40.2 | 40.5 | 41.0 | 40.7 | 38.9 | 42.0 | 42.0 | 38.0 | 40.9 | 36.2 |
| 11-12 01Z | Wed 16:00 | 40.0 | 41.6 |  | 38.2 |  |  |  | 38.0 | 40.9 | 36.8 |
| 11-12 02Z | Wed 17:00 | 40.2 | 41.4 |  | 40.0 |  |  |  | 39.0 | 40.9 | 37.4 |
| 11-12 03Z | Wed 18:00 | 39.8 | 41.3 | 40.2 | 40.6 | 40.6 | 41.0 | 41.0 | 39.0 | 40.8 | 37.6 |
| 11-12 04Z | Wed 19:00 | 38.9 | 41.1 |  | 40.6 |  |  |  | 38.0 | 40.7 | 37.7 |
| 11-12 05Z | Wed 20:00 | 40.5 | 40.4 |  | 40.5 |  |  |  | 38.0 | 40.5 | 37.5 |
| 11-12 06Z | Wed 21:00 | 39.4 | 41.0 | 39.7 | 39.6 | 37.6 | 40.0 | 40.0 | 37.0 | 40.3 | 37.3 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 88 | 88 | 93 | 94 | 92 | 86 | 96 | 86 | 91 | 80 |
| 11-11 07Z | Tue 22:00 | 91 | 89 |  | 92 |  |  |  | 89 | 88 | 79 |
| 11-11 08Z | Tue 23:00 | 87 | 86 |  | 73 |  |  |  | 85 | 83 | 77 |
| 11-11 09Z | Wed 00:00 | 84 | 85 | 70 | 69 | 74 | 89 | 89 | 89 | 80 | 75 |
| 11-11 10Z | Wed 01:00 | 88 | 87 |  | 71 |  |  |  | 89 | 81 | 72 |
| 11-11 11Z | Wed 02:00 | 83 | 88 |  | 88 |  |  |  | 85 | 83 | 70 |
| 11-11 12Z | Wed 03:00 | 83 | 86 | 80 | 84 | 65 | 86 | 92 | 89 | 86 | 70 |
| 11-11 13Z | Wed 04:00 | 78 | 90 |  | 92 |  |  |  | 89 | 88 | 71 |
| 11-11 14Z | Wed 05:00 | 71 | 97 |  | 95 |  |  |  | 85 | 90 | 74 |
| 11-11 15Z | Wed 06:00 | 89 | 95 | 95 | 97 | 72 | 89 | 100 | 85 | 92 | 76 |
| 11-11 16Z | Wed 07:00 | 93 | 96 |  | 96 |  |  |  | 89 | 92 | 77 |
| 11-11 17Z | Wed 08:00 | 96 | 96 |  | 97 |  |  |  | 89 | 92 | 77 |
| 11-11 18Z | Wed 09:00 | 91 | 95 | 95 | 97 | 89 | 89 | 100 | 92 | 92 | 77 |
| 11-11 19Z | Wed 10:00 | 87 | 97 |  | 95 |  |  |  | 92 | 93 | 77 |
| 11-11 20Z | Wed 11:00 | 86 | 97 |  | 96 |  |  |  | 89 | 93 | 78 |
| 11-11 21Z | Wed 12:00 | 89 | 95 | 92 | 94 | 80 | 93 | 96 | 92 | 92 | 79 |
| 11-11 22Z | Wed 13:00 | 92 | 95 |  | 92 |  |  |  | 89 | 91 | 81 |
| 11-11 23Z | Wed 14:00 | 95 | 92 |  | 92 |  |  |  | 89 | 89 | 83 |
| 11-12 00Z | Wed 15:00 | 90 | 90 | 82 | 82 | 90 | 93 | 96 | 89 | 88 | 85 |
| 11-12 01Z | Wed 16:00 | 91 | 95 |  | 78 |  |  |  | 89 | 88 | 86 |
| 11-12 02Z | Wed 17:00 | 89 | 95 |  | 94 |  |  |  | 89 | 89 | 86 |
| 11-12 03Z | Wed 18:00 | 88 | 94 | 92 | 95 | 82 | 93 | 100 | 86 | 89 | 86 |
| 11-12 04Z | Wed 19:00 | 90 | 92 |  | 95 |  |  |  | 82 | 90 | 86 |
| 11-12 05Z | Wed 20:00 | 94 | 92 |  | 95 |  |  |  | 82 | 91 | 85 |
| 11-12 06Z | Wed 21:00 | 91 | 92 | 95 | 97 | 75 | 93 | 96 | 82 | 91 | 85 |

Wind speed (kt) at the hour:

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 20.4 | 17.4 | 16.5 | 15.4 | 13.6 | 11.0 | 11.0 | 7.0 | 17.9 | 13.9 |
| 11-11 07Z | Tue 22:00 | 17.1 | 16.6 |  | 12.7 |  |  |  | 7.0 | 14.7 | 12.3 |
| 11-11 08Z | Tue 23:00 | 9.9 | 12.7 |  | 9.2 |  |  |  | 6.0 | 10.5 | 10.5 |
| 11-11 09Z | Wed 00:00 | 7.8 | 8.1 | 5.1 | 4.2 | 8.5 | 4.0 | 6.0 | 5.0 | 7.5 | 9.4 |
| 11-11 10Z | Wed 01:00 | 7.2 | 6.2 |  | 4.7 |  |  |  | 4.0 | 5.0 | 8.6 |
| 11-11 11Z | Wed 02:00 | 5.9 | 3.8 |  | 3.9 |  |  |  | 4.0 | 3.2 | 8.3 |
| 11-11 12Z | Wed 03:00 | 6.2 | 4.5 | 1.5 | 1.0 | 7.1 | 2.0 | 0.0 | 4.0 | 2.9 | 8.3 |
| 11-11 13Z | Wed 04:00 | 6.3 | 3.5 |  | 1.9 |  |  |  | 4.0 | 2.6 | 8.0 |
| 11-11 14Z | Wed 05:00 | 5.9 | 4.0 |  | 4.9 |  |  |  | 5.0 | 3.1 | 8.0 |
| 11-11 15Z | Wed 06:00 | 8.0 | 4.2 | 3.3 | 2.1 | 11.0 | 4.0 | 0.0 | 5.0 | 4.5 | 8.1 |
| 11-11 16Z | Wed 07:00 | 9.4 | 3.6 |  | 3.0 |  |  |  | 5.0 | 5.2 | 7.9 |
| 11-11 17Z | Wed 08:00 | 9.0 | 3.1 |  | 5.7 |  |  |  | 5.0 | 6.0 | 8.0 |
| 11-11 18Z | Wed 09:00 | 4.2 | 4.0 | 8.6 | 8.0 | 7.0 | 6.0 | 5.0 | 5.0 | 6.3 | 8.2 |
| 11-11 19Z | Wed 10:00 | 4.6 | 2.7 |  | 7.9 |  |  |  | 5.0 | 6.9 | 8.4 |
| 11-11 20Z | Wed 11:00 | 5.0 | 1.7 |  | 8.9 |  |  |  | 5.0 | 9.0 | 9.0 |
| 11-11 21Z | Wed 12:00 | 4.0 | 2.6 | 6.2 | 5.5 | 5.9 | 7.0 | 9.0 | 6.0 | 10.0 | 9.6 |
| 11-11 22Z | Wed 13:00 | 8.4 | 4.3 |  | 13.4 |  |  |  | 7.0 | 9.5 | 10.0 |
| 11-11 23Z | Wed 14:00 | 9.8 | 7.3 |  | 27.5 |  |  |  | 8.0 | 13.1 | 11.1 |
| 11-12 00Z | Wed 15:00 | 13.8 | 5.7 | 28.0 | 26.8 | 16.8 | 15.0 | 12.0 | 10.0 | 16.2 | 12.2 |
| 11-12 01Z | Wed 16:00 | 14.0 | 6.3 |  | 15.2 |  |  |  | 10.0 | 15.9 | 12.7 |
| 11-12 02Z | Wed 17:00 | 12.4 | 4.6 |  | 9.4 |  |  |  | 11.0 | 14.8 | 13.9 |
| 11-12 03Z | Wed 18:00 | 13.9 | 7.0 | 8.9 | 8.1 | 22.7 | 12.0 | 11.0 | 11.0 | 14.5 | 14.8 |
| 11-12 04Z | Wed 19:00 | 13.7 | 8.5 |  | 8.5 |  |  |  | 11.0 | 13.8 | 14.4 |
| 11-12 05Z | Wed 20:00 | 11.6 | 8.8 |  | 9.9 |  |  |  | 11.0 | 13.1 | 13.3 |
| 11-12 06Z | Wed 21:00 | 10.7 | 7.7 | 6.2 | 5.9 | 23.0 | 12.0 | 10.0 | 10.0 | 12.9 | 12.5 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.07 | 0.00 | 0.00 |
| 11-11 07Z | Tue 22:00 | 0.00 | 0.01 |  | 0.04 |  | 0.12 | 0.02 | 0.00 |
| 11-11 08Z | Tue 23:00 | 0.00 | 0.04 |  | 0.04 |  | 0.14 | 0.04 | 0.00 |
| 11-11 09Z | Wed 00:00 | 0.00 | 0.04 | 0.04 | 0.04 | 0.06 | 0.14 | 0.06 | 0.01 |
| 11-11 10Z | Wed 01:00 | 0.01 | 0.04 |  | 0.05 |  | 0.14 | 0.07 | 0.01 |
| 11-11 11Z | Wed 02:00 | 0.01 | 0.04 |  | 0.06 |  | 0.14 | 0.09 | 0.01 |
| 11-11 12Z | Wed 03:00 | 0.01 | 0.05 | 0.07 | 0.07 | 0.06 | 0.14 | 0.11 | 0.01 |
| 11-11 13Z | Wed 04:00 | 0.01 | 0.05 |  | 0.08 |  | 0.14 | 0.13 | 0.01 |
| 11-11 14Z | Wed 05:00 | 0.01 | 0.07 |  | 0.15 |  | 0.14 | 0.16 | 0.02 |
| 11-11 15Z | Wed 06:00 | 0.03 | 0.08 | 0.15 | 0.15 | 0.07 | 0.14 | 0.18 | 0.02 |
| 11-11 16Z | Wed 07:00 | 0.04 | 0.08 |  | 0.20 |  | 0.14 | 0.23 | 0.04 |
| 11-11 17Z | Wed 08:00 | 0.04 | 0.08 |  | 0.29 |  | 0.14 | 0.28 | 0.05 |
| 11-11 18Z | Wed 09:00 | 0.04 | 0.09 | 0.32 | 0.33 | 0.18 | 0.15 | 0.33 | 0.06 |
| 11-11 19Z | Wed 10:00 | 0.04 | 0.12 |  | 0.38 |  | 0.17 | 0.37 | 0.08 |
| 11-11 20Z | Wed 11:00 | 0.04 | 0.14 |  | 0.42 |  | 0.20 | 0.41 | 0.10 |
| 11-11 21Z | Wed 12:00 | 0.04 | 0.15 | 0.41 | 0.42 | 0.22 | 0.24 | 0.45 | 0.11 |
| 11-11 22Z | Wed 13:00 | 0.12 | 0.15 |  | 0.42 |  | 0.28 | 0.49 | 0.16 |
| 11-11 23Z | Wed 14:00 | 0.14 | 0.16 |  | 0.48 |  | 0.33 | 0.53 | 0.21 |
| 11-12 00Z | Wed 15:00 | 0.20 | 0.26 | 0.47 | 0.48 | 0.35 | 0.39 | 0.57 | 0.26 |
| 11-12 01Z | Wed 16:00 | 0.25 | 0.26 |  | 0.48 |  | 0.44 | 0.61 | 0.31 |
| 11-12 02Z | Wed 17:00 | 0.27 | 0.26 |  | 0.57 |  | 0.48 | 0.66 | 0.36 |
| 11-12 03Z | Wed 18:00 | 0.27 | 0.27 | 0.60 | 0.61 | 0.45 | 0.52 | 0.70 | 0.41 |
| 11-12 04Z | Wed 19:00 | 0.35 | 0.27 |  | 0.66 |  | 0.55 | 0.74 | 0.44 |
| 11-12 05Z | Wed 20:00 | 0.35 | 0.28 |  | 0.68 |  | 0.58 | 0.79 | 0.47 |
| 11-12 06Z | Wed 21:00 | 0.35 | 0.28 | 0.72 | 0.72 | 0.51 | 0.61 | 0.84 | 0.50 |

Total cloud cover (%):

| UTC | Local (AKST) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-11 06Z | Tue 21:00 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 100 | 97 | 97 |
| 11-11 07Z | Tue 22:00 | 76 | 97 |  | 100 |  |  | 91 | 100 | 97 | 92 |
| 11-11 08Z | Tue 23:00 | 100 | 86 |  | 99 |  |  | 88 | 100 | 98 | 87 |
| 11-11 09Z | Wed 00:00 | 100 | 82 | 100 | 100 | 100 | 100 | 84 | 100 | 100 | 85 |
| 11-11 10Z | Wed 01:00 | 100 | 96 |  | 100 |  |  | 91 | 100 | 100 | 88 |
| 11-11 11Z | Wed 02:00 | 100 | 100 |  | 100 |  |  | 93 | 100 | 100 | 95 |
| 11-11 12Z | Wed 03:00 | 100 | 100 | 100 | 100 | 100 | 100 | 95 | 100 | 100 | 100 |
| 11-11 13Z | Wed 04:00 | 100 | 100 |  | 100 |  |  | 95 | 100 | 100 | 100 |
| 11-11 14Z | Wed 05:00 | 100 | 100 |  | 100 |  |  | 95 | 100 | 100 | 100 |
| 11-11 15Z | Wed 06:00 | 100 | 100 | 100 | 100 | 100 | 100 | 97 | 100 | 100 | 100 |
| 11-11 16Z | Wed 07:00 | 100 | 100 |  | 100 |  |  | 96 | 100 | 100 | 99 |
| 11-11 17Z | Wed 08:00 | 100 | 100 |  | 100 |  |  | 96 | 100 | 100 | 98 |
| 11-11 18Z | Wed 09:00 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 100 | 100 | 97 |
| 11-11 19Z | Wed 10:00 | 100 | 100 |  | 100 |  |  | 96 | 100 | 99 | 96 |
| 11-11 20Z | Wed 11:00 | 100 | 100 |  | 100 |  |  | 94 | 100 | 99 | 94 |
| 11-11 21Z | Wed 12:00 | 100 | 100 | 100 | 100 | 100 | 100 | 96 | 100 | 99 | 94 |
| 11-11 22Z | Wed 13:00 | 100 | 100 |  | 100 |  |  | 94 | 100 | 96 | 95 |
| 11-11 23Z | Wed 14:00 | 100 | 100 |  | 100 |  |  | 96 | 100 | 94 | 98 |
| 11-12 00Z | Wed 15:00 | 100 | 96 | 92 | 91 | 100 | 100 | 90 | 100 | 92 | 99 |
| 11-12 01Z | Wed 16:00 | 100 | 74 |  | 84 |  |  |  | 100 | 90 | 98 |
| 11-12 02Z | Wed 17:00 | 100 | 72 |  | 92 |  |  |  | 100 | 90 | 97 |
| 11-12 03Z | Wed 18:00 | 100 | 69 | 98 | 99 | 100 | 100 | 88 | 100 | 90 | 96 |
| 11-12 04Z | Wed 19:00 | 100 | 60 |  | 98 |  |  |  | 98 | 91 | 96 |
| 11-12 05Z | Wed 20:00 | 100 | 24 |  | 85 |  |  |  | 95 | 94 | 96 |
| 11-12 06Z | Wed 21:00 | 100 | 41 | 100 | 100 | 71 | 100 | 73 | 91 | 95 | 96 |

## Track record this period

Since 2026-10-26 at PAYA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-11-10 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 15 | 6.0 | -0.3 | -0.9 | -0.5 | -0.05 | 0.5 | 2.0 | 1.7 | 0.22 |
| IFS_HRES | 15 | 7.8 | -1.3 | +1.7 | +0.7 | -0.06 | 1.9 | 2.4 | 1.8 | 0.17 |
| IFS | 15 | 8.0 | -0.9 | +2.5 | +1.1 | -0.04 | 1.5 | 2.8 | 2.2 | 0.17 |
| GFS_MOS | 15 | 8.3 | +0.5 | -0.9 | -4.0 | -0.06 | 1.1 | 1.4 | 4.0 | 0.30 |
| NBM | 15 | 8.4 | -1.1 | -1.8 | -4.3 | -0.07 | 1.2 | 3.0 | 4.3 | 0.17 |
| RRFS | 15 | 9.1 | -1.8 | +1.3 | -2.2 | -0.03 | 2.0 | 2.0 | 3.1 | 0.20 |
| HRRR | 15 | 10.0 | -2.3 | +1.3 | -1.4 | +0.01 | 2.5 | 2.4 | 2.2 | 0.29 |
| GFS | 15 | 14.6 | +0.4 | +5.8 | +5.4 | -0.12 | 0.9 | 5.9 | 5.4 | 0.30 |

## Daily verification (all 15 days this period)

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
| 11-09 h | 8.5 | 9.3 | 7.7 | 7.8 | 16.9 | 10.6 | 9.2 | 6.1 | CONSENSUS |

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
| 11-09 h | 48 | -4 | -4 | -2 | -2 | +1 | -1 | -2 | -1 |

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
| 11-09 h | 32 | +2 | +0 | +4 | +3 | +7 | +1 | -1 | +1 |

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
| 11-09 h | 31 | -3 | -5 | +1 | +2 | +0 | -10 | -8 | -3 |

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
| 11-09 h | 0.45 | +0.05 | -0.14 | -0.06 | -0.09 | -0.36 | -0.18 | -0.11 | -0.13 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 15 | +15 | 18 | +12 | 15 |
| RRFS | 15 | +6 | 20 | +7 | 14 |
| IFS | 15 | +13 | 19 | +12 | 17 |
| IFS_HRES | 15 | +12 | 20 | +12 | 15 |
| GFS | 15 | +14 | 17 | +13 | 14 |
| GFS_MOS | 15 | +1 | 13 | +10 | 13 |
| NBM | 15 | +7 | 16 | +5 | 11 |

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
| 11-09 h | 48% | 100% | +51 | +52 | +52 | +52 | +52 | +35 | +44 |

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
| 11-09 h | 100% | 100% | -4 | +0 | -13 | -8 | +0 | +0 | -6 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 15 | +0.8 | 1.8 | +0.1 | 1.4 |
| RRFS | 15 | +0.0 | 1.6 | -0.7 | 1.8 |
| IFS | 15 | -0.2 | 1.7 | -1.9 | 2.2 |
| IFS_HRES | 15 | -0.8 | 1.9 | -2.2 | 2.5 |
| GFS | 15 | -0.7 | 2.3 | -2.9 | 3.3 |
| GFS_MOS | 15 | -0.6 | 1.6 | -2.0 | 2.3 |
| NBM | 15 | -1.2 | 1.9 | -0.5 | 1.4 |

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
| 11-09 h | 31.2 | +2.0 | +0.2 | +0.0 | -0.8 | +2.4 | +3.4 | +0.5 |

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
| 11-09 h | 37.0 | -0.8 | -3.2 | -1.9 | -2.0 | -4.1 | -2.3 | -1.1 |

## Today so far (2026-11-10, through 2026-11-10T22:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 46.9 °F, low 36.0 °F, max wind 22 kt, precip 0.44" (17 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 09/18Z | -0.7 | 1.8 | 44 (-3) | 39 (+3) | +2.6 | 0.20 | -0.24 |
| RRFS | 09/18Z | -0.3 | 1.6 | 44 (-3) | 38 (+2) | +2.1 | 0.12 | -0.32 |
| IFS | 09/12Z | -0.5 | 1.5 | 46 (-1) | 37 (+1) | +4.6 | 0.35 | -0.09 |
| IFS_HRES | 09/12Z | -1.1 | 2.0 | 46 (-1) | 36 (+0) | +3.8 | 0.33 | -0.11 |
| GFS | 09/18Z | +2.5 | 2.9 | 48 (+2) pending | 43 (+7) | +8.7 | 0.06 | -0.38 |
| GFS_MOS | 09/18Z | +0.8 | 1.7 | 47 (+0) | 39 (+3) | +1.1 | — | — |
| NBM | 09/22Z | -1.4 | 2.5 | 46 (-1) | 37 (+1) | +3.8 | — | — |
| USL | 09/22Z | -0.9 | 1.5 | 45 (-2) | 36 (+0) | +2.9 | 0.49 | +0.05 |
| ENS | 09/12Z | +0.8 | 1.6 | 46 (+0) | 40 (+4) | +5.5 | 0.31 | -0.13 |
| GEFS | 09/18Z | -2.6 | 3.3 | 41 (-6) | 38 (+2) | +3.6 | 0.14 | -0.30 |

## Clouds so far today (2026-11-10, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (AKST) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 06Z | Mon 21:00 | 100 |  | 100 | 100 | 100 | 100 | 100 | 100 | 97 | 100 | 100 | 100 |
| 11-10 07Z | Mon 22:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 96 | 100 | 97 | 100 |
| 11-10 08Z | Mon 23:00 | 100 | 100 | 100 | 100 |  | 99 |  |  | 96 | 100 | 94 | 100 |
| 11-10 09Z | Tue 00:00 | 100 | 100 | 85 | 100 | 94 | 95 | 100 | 100 | 90 | 100 | 91 | 100 |
| 11-10 10Z | Tue 01:00 | 100 | 100 | 100 | 83 |  | 74 |  |  | 87 | 100 | 91 | 99 |
| 11-10 11Z | Tue 02:00 | 100 | 100 | 100 | 95 |  | 76 |  |  | 93 | 100 | 92 | 97 |
| 11-10 12Z | Tue 03:00 | 100 | 100 | 100 | 100 | 97 | 99 | 100 | 100 | 94 | 100 | 93 | 96 |
| 11-10 13Z | Tue 04:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 93 | 100 | 93 | 96 |
| 11-10 14Z | Tue 05:00 | 100 | 100 | 100 | 100 |  | 72 |  |  | 90 | 100 | 94 | 96 |
| 11-10 15Z | Tue 06:00 | 100 | 100 | 100 | 98 | 95 | 95 | 100 | 75 | 89 | 100 | 94 | 96 |
| 11-10 16Z | Tue 07:00 | 100 | 0 | 100 | 92 |  | 64 |  |  | 86 | 100 | 95 | 93 |
| 11-10 17Z | Tue 08:00 | 100 | 0 | 100 | 89 |  | 91 |  |  | 74 | 100 | 96 | 89 |
| 11-10 18Z | Tue 09:00 | 100 | 0 | 100 | 100 | 100 | 100 | 100 | 75 | 85 | 100 | 98 | 88 |
| 11-10 19Z | Tue 10:00 | 100 | 19 | 100 | 100 |  | 100 |  |  | 87 | 100 | 98 | 90 |
| 11-10 20Z | Tue 11:00 | 100 | 0 | 100 | 100 |  | 100 |  |  | 89 | 100 | 98 | 94 |
| 11-10 21Z | Tue 12:00 | 100 | 75 | 100 | 100 | 100 | 100 | 100 | 75 | 93 | 100 | 98 | 97 |
| 11-10 22Z | Tue 13:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 91 | 100 | 98 | 98 |
| 11-10 23Z | Tue 14:00 | 100 | 100 | 100 | 100 |  | 100 |  |  | 94 | 100 | 98 | 98 |

## Dewpoint so far today (2026-11-10, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (AKST) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 07Z | Mon 22:00 | 39.9 | 82 | 39.4 | 38.1 |  | 41.5 |  |  |  | 39.0 | 41.6 | 34.0 |
| 11-10 08Z | Mon 23:00 | 39.9 | 82 | 40.2 | 39.7 |  | 40.8 |  |  |  | 39.0 | 41.2 | 34.9 |
| 11-10 09Z | Tue 00:00 | 39.9 | 82 | 40.5 | 39.8 | 41.0 | 41.2 | 40.7 | 39.0 | 40.0 | 39.0 | 40.8 | 35.6 |
| 11-10 10Z | Tue 01:00 | 41.0 | 89 | 40.2 | 39.5 |  | 41.4 |  |  |  | 39.0 | 40.6 | 35.8 |
| 11-10 11Z | Tue 02:00 | 41.0 | 86 | 38.5 | 40.9 |  | 40.4 |  |  |  | 39.0 | 40.3 | 35.7 |
| 11-10 12Z | Tue 03:00 | 41.0 | 86 | 39.8 | 39.9 | 39.8 | 39.7 | 38.6 | 37.0 | 39.0 | 38.0 | 39.9 | 35.4 |
| 11-10 13Z | Tue 04:00 | 39.9 | 92 | 40.0 | 40.6 |  | 38.4 |  |  |  | 37.0 | 39.3 | 34.9 |
| 11-10 14Z | Tue 05:00 | 39.9 | 92 | 39.8 | 39.2 |  | 38.0 |  |  |  | 36.0 | 38.7 | 34.2 |
| 11-10 15Z | Tue 06:00 | 39.0 | 93 | 38.4 | 37.8 | 37.5 | 37.3 | 35.5 | 36.0 | 37.0 | 35.0 | 38.0 | 33.3 |
| 11-10 16Z | Tue 07:00 | 37.0 | 92 | 36.4 | 37.1 |  | 35.5 |  |  |  | 34.0 | 36.9 | 32.2 |
| 11-10 17Z | Tue 08:00 | 36.0 | 89 | 34.5 | 35.8 |  | 33.2 |  |  |  | 33.0 | 35.7 | 30.8 |
| 11-10 18Z | Tue 09:00 | 36.0 | 100 | 35.4 | 35.1 | 33.7 | 33.1 | 32.6 | 37.0 | 35.0 | 34.0 | 34.9 | 29.9 |
| 11-10 19Z | Tue 10:00 | 37.0 | 100 | 35.2 | 35.0 |  | 35.0 |  |  |  | 34.0 | 34.8 | 29.7 |
| 11-10 20Z | Tue 11:00 | 39.0 | 100 | 36.6 | 33.7 |  | 35.5 |  |  |  | 35.0 | 34.9 | 29.8 |
| 11-10 21Z | Tue 12:00 | 41.0 | 96 | 37.3 | 34.4 | 35.7 | 35.4 | 32.5 | 38.0 | 37.0 | 35.0 | 35.1 | 29.9 |
| 11-10 22Z | Tue 13:00 | 39.9 | 82 | 35.9 | 33.9 |  | 36.1 |  |  |  | 35.0 | 35.4 | 30.0 |
| 11-10 23Z | Tue 14:00 | 35.1 | 63 | 38.6 | 31.5 |  | 38.1 |  |  |  | 35.0 | 35.9 | 30.2 |
| Bias so far |  |  |  | -0.9 | -1.8 | -1.8 | -1.3 | -3.4 | -2.0 | -1.8 | -2.7 | -1.1 | -6.2 |

## Newest runs vs obs so far today (2026-11-10)

The runs that have come out since today's deadline (HRRR, RRFS, IFS, GFS, GFS_MOS, NBM; fetched 2026-11-10 23:24Z), against the METAR nearest each hour since each run's first valid time. These runs are not scored for today; use them to judge whether the newest guidance has the current pattern right before trusting what it says for the target day. A run already a few degrees off a few hours in usually stays off. Compare its bias with the submitted run of the same model over the same hours: if the newest run is no better, its change for the target day deserves less weight. Text guidance (GFS_MOS, NBM) often starts after the last report, so it has no hours to compare yet.

How each run is doing so far (forecast - observed; Hours = hours compared). Cloud bias is in percentage points against the METAR sky cover. Precip = the run's total since its first valid time / what was observed over the same span:

| Model | Run | From | Hours | Temp bias | Temp MAE | Submitted run temp bias | Td bias | Wind bias | Cloud bias | Precip fcst / obs |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 10/18Z | 19Z | 5 | -0.4 | 1.9 | +0.3 | -2.3 | +3.8 | +41 | 0.00 / 0.00 |
| RRFS | 10/18Z | 19Z | 5 | +1.1 | 2.7 | +0.1 | -2.7 | +2.0 | +39 | 0.00 / 0.00 |
| IFS | 10/12Z | 15Z | 3 | +2.0 | 2.8 | +0.3 | -3.3 | +3.7 | +39 | 0.00 / 0.00 |
| GFS | 10/18Z | 21Z | 1 | +3.4 | 3.4 | +2.5 | -7.3 | +2.5 | +25 | 0.00 / 0.00 |
| GFS_MOS | 10/18Z | 00Z | 0 | — | — | — | — | — | — | — |
| NBM | 10/22Z | 03Z | 0 | — | — | — | — | — | — | — |

Rest of today (after the last report to 06Z; hourly values, so 3-hourly guidance can miss the true extreme). Day high/low = the run's extreme for the rest of the day combined with the observed high 46.9 / low 36.0 °F so far:

| Model | Run | Hours left | Max T | Min T | Max wind | Day high | Day low |
| --- | --- | --: | --: | --: | --: | --: | --: |
| HRRR | 10/18Z | 7 | 44.1 | 42.1 | 21.0 | 46.9 | 36.0 |
| RRFS | 10/18Z | 7 | 45.5 | 42.6 | 17.5 | 46.9 | 36.0 |
| IFS | 10/12Z | 3 | 42.5 | 41.9 | 20.4 | 46.9 | 36.0 |
| GFS | 10/18Z | 3 | 44.7 | 43.1 | 13.9 | 46.9 | 36.0 |
| GFS_MOS | 10/18Z | 3 | 44.0 | 42.0 | 12.0 | 46.9 | 36.0 |
| NBM | 10/22Z | 2 | 41.0 | 41.0 | 11.0 | 46.9 | 36.0 |

Hour by hour (°F, kt; obs blank after the last report):

| UTC | Local (AKST) | Obs T | Obs Td | Obs wind | HRRR T | HRRR Td | HRRR wind | RRFS T | RRFS Td | RRFS wind | IFS T | IFS Td | IFS wind | GFS T | GFS Td | GFS wind | GFS_MOS T | GFS_MOS Td | GFS_MOS wind | NBM T | NBM Td | NBM wind |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 11-10 15Z | Tue 06:00 | 41.0 | 39.0 | 3 |  |  |  |  |  |  | 39.8 | 38.2 | 9 |  |  |  |  |  |  |  |  |  |
| 11-10 16Z | Tue 07:00 | 39.0 | 37.0 | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 17Z | Tue 08:00 | 39.0 | 36.0 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 18Z | Tue 09:00 | 36.0 | 36.0 | 5 |  |  |  |  |  |  | 40.0 | 34.5 | 7 |  |  |  |  |  |  |  |  |  |
| 11-10 19Z | Tue 10:00 | 37.0 | 37.0 | 0 | 38.3 | 35.7 | 4 | 40.7 | 35.1 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 20Z | Tue 11:00 | 39.0 | 39.0 | 0 | 41.2 | 35.3 | 6 | 42.8 | 35.0 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 21Z | Tue 12:00 | 42.1 | 41.0 | 3 | 42.5 | 34.8 | 6 | 44.0 | 35.5 | 6 | 45.3 | 33.3 | 6 | 45.5 | 33.7 | 6 |  |  |  |  |  |  |
| 11-10 22Z | Tue 13:00 | 45.0 | 39.9 | 5 | 42.9 | 37.8 | 11 | 44.0 | 37.0 | 4 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-10 23Z | Tue 14:00 | 46.9 | 35.1 | 6 | 43.2 | 36.9 | 6 | 43.9 | 36.0 | 6 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 00Z | Tue 15:00 |  |  |  | 43.2 | 36.6 | 8 | 43.1 | 35.7 | 8 | 41.9 | 36.9 | 11 | 44.7 | 34.4 | 11 | 44.0 | 42.0 | 4 |  |  |  |
| 11-11 01Z | Tue 16:00 |  |  |  | 42.1 | 35.7 | 9 | 42.6 | 34.4 | 9 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 02Z | Tue 17:00 |  |  |  | 42.8 | 37.9 | 13 | 42.6 | 37.3 | 17 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 03Z | Tue 18:00 |  |  |  | 42.8 | 40.1 | 21 | 43.2 | 37.5 | 14 | 41.9 | 39.4 | 20 | 43.3 | 34.5 | 14 | 42.0 | 40.0 | 12 | 41.0 | 38.0 | 11 |
| 11-11 04Z | Tue 19:00 |  |  |  | 44.1 | 41.5 | 21 | 43.2 | 38.6 | 14 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 05Z | Tue 20:00 |  |  |  | 44.0 | 41.3 | 21 | 44.8 | 41.3 | 18 |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-11 06Z | Tue 21:00 |  |  |  | 43.8 | 40.4 | 20 | 45.5 | 42.2 | 17 | 42.5 | 40.6 | 16 | 43.1 | 40.8 | 14 | 42.0 | 38.0 | 11 | 41.0 | 40.0 | 11 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (AJK): https://forecast.weather.gov/product.php?site=ajk&issuedby=ajk&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
