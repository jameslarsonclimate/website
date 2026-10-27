# WxChallenge forecast brief: Minneapolis, MN (KMSP)

- Station: **KMSP**
- Target day: **2026-10-28**, scored over 2026-10-28T06Z to 2026-10-29T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-28T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-27T14:01:55+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 27/12Z | 62.7 | 50.9 | 13.0 | 0.28 |
| RRFS | 27/06Z | 65.9 | 52.0 | 12.9 | 0.11 |
| IFS | 27/06Z | 67.4 | 49.6 | 7.7 | 0.40 |
| IFS_HRES | 27/06Z | 67.7 | 51.6 | 8.3 | 0.73 |
| GFS | 27/06Z | 66.0 | 52.2 | 9.7 | 0.17 |
| AIFS | 27/06Z | 62.4 | 49.9 | 8.0 | 0.53 |
| GFS_MOS | 27/06Z | 68.0 | 52.0 | 15.0 | 0.10 |
| NBM | 27/14Z | 70.0 | 51.0 | 12.0 | 0.26 |
| USL | — | — | — | — | — |
| ENS | 27/00Z | 66.9 | 48.9 | 9.8 | 0.33 |
| AIFS_ENS | 27/00Z | 64.5 | 48.3 | 9.9 | 0.35 |
| GEFS | 27/06Z | 67.5 | 52.5 | 11.5 | 0.28 |
| HRRRCAST (precip only) | 27/06Z | — | — | — | 0.08 |
| REFS (precip only) | 27/12Z | — | — | — | 0.18 |
| NBM_QMD (precip only) | 27/06Z | — | — | — | 0.45 |
| **CONSENSUS** |  | **66.8** | **50.6** | **15.5** | **0.28** |

Notes:
- RRFS: TMAX/TMIN unavailable (RuntimeError: Processing failed: ("Connection broken: ConnectionResetError(54, 'Connection reset by peer')", ConnectionResetError(54, ); newest cycle unavailable, used previous
- IFS_HRES: not in the consensus
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [0, 0, 1, 1] -> midpoints
- NBM: NBS Q06 amounts
- USL: failed this run (no USL run for 2026-10-28 available at 2026-10-27 15Z)
- ENS: ensemble mean of 51 members (Open-Meteo)
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- HRRRCAST: median of 18 members (experimental AI model)
- REFS: median of 14 members, 12Z + 06Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: RRFS 0.17, HRRR 0.14, GFS 0.13, GFS_MOS 0.11, NBM 0.10, AIFS 0.09, AIFS_ENS 0.09, IFS 0.08, ENS 0.08 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Low °F weights: NBM 0.16, IFS 0.14, ENS 0.14, AIFS 0.10, AIFS_ENS 0.10, HRRR 0.10, GFS_MOS 0.09, RRFS 0.09, GFS 0.08 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Wind kt weights: GFS_MOS 0.15, NBM 0.14, HRRR 0.12, RRFS 0.11, GFS 0.10, AIFS 0.10, AIFS_ENS 0.10, IFS 0.09, ENS 0.09 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Precip in weights: GFS_MOS 0.12, NBM 0.12, AIFS 0.11, AIFS_ENS 0.11, GFS 0.11, RRFS 0.11, HRRR 0.11, IFS 0.11, ENS 0.11 (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 64.8 | 65.7 | 66.8 | 68.2 | 68.9 | 66.9 |
| ENS | 51 | Low °F | 46.5 | 48.0 | 49.1 | 49.8 | 51.1 | 48.9 |
| ENS | 51 | Wind kt | 8.2 | 8.8 | 9.3 | 10.8 | 12.0 | 9.8 |
| ENS | 51 | Precip in | 0.18 | 0.24 | 0.32 | 0.42 | 0.52 | 0.33 |
| AIFS_ENS | 51 | High °F | 62.4 | 63.2 | 64.4 | 65.8 | 67.1 | 64.5 |
| AIFS_ENS | 51 | Low °F | 44.0 | 46.1 | 48.8 | 50.4 | 51.4 | 48.3 |
| AIFS_ENS | 51 | Wind kt | 8.2 | 8.8 | 9.9 | 10.8 | 11.9 | 9.9 |
| AIFS_ENS | 51 | Precip in | 0.14 | 0.22 | 0.31 | 0.50 | 0.66 | 0.35 |
| GEFS | 31 | High °F | 64.2 | 65.6 | 67.9 | 68.5 | 70.3 | 67.5 |
| GEFS | 31 | Low °F | 50.6 | 51.6 | 52.6 | 53.5 | 54.0 | 52.5 |
| GEFS | 31 | Wind kt | 9.7 | 10.8 | 11.4 | 12.1 | 13.1 | 11.5 |
| GEFS | 31 | Precip in | 0.14 | 0.18 | 0.25 | 0.35 | 0.45 | 0.28 |
| HRRRCAST | 18 | Precip in | 0.02 | 0.06 | 0.08 | 0.14 | 0.28 | 0.12 |
| REFS | 14 | Precip in | 0.08 | 0.11 | 0.18 | 0.30 | 0.57 | 0.28 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 96% | 65% | 14% |
| AIFS_ENS | 100% | 100% | 63% | 22% |
| GEFS | 100% | 90% | 48% | 10% |
| HRRRCAST | 89% | 39% | 11% | 0% |
| REFS | 100% | 86% | 36% | 21% |

NBM QMD calibrated 24-h precip percentiles: p10 0.22", p25 0.26", p50 0.45", p75 0.73", p90 0.96"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 3% | 15% | 47% | 47% | 47% to 77% | — |
| NBM | NBS P06 | 21% | 27% | 86% | 76% | 86% to 98% | — |
| ENS | member fraction | 0% | 24% | 98% | 98% | 100% | — |
| AIFS_ENS | member fraction | 4% | 63% | 100% | 72% | 100% | — |
| GEFS | member fraction | 0% | 36% | 100% | 94% | 100% | — |
| HRRRCAST | member fraction | — | — | — | — | 89% | — |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 21% | 27% | 86% | 76% | 100% | — |

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS, AIFS_ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 51.2 | 52.5 | 51.4 | 52.4 | 52.2 | 50.8 | 54.0 | 53.0 | 52.8 | 51.7 | 53.7 |
| 10-28 07Z | Wed 02:00 | 51.1 | 52.4 |  | 52.2 |  |  |  |  | 52.2 | 51.4 | 53.5 |
| 10-28 08Z | Wed 03:00 | 51.2 | 52.4 |  | 51.6 |  |  |  |  | 51.5 | 50.8 | 53.4 |
| 10-28 09Z | Wed 04:00 | 51.4 | 52.3 | 50.4 | 52.1 | 52.6 |  | 53.0 | 52.0 | 50.8 | 50.2 | 53.3 |
| 10-28 10Z | Wed 05:00 | 51.4 | 52.2 |  | 51.7 |  |  |  |  | 49.9 | 49.8 | 53.0 |
| 10-28 11Z | Wed 06:00 | 51.6 | 52.0 |  | 52.3 |  |  |  |  | 49.0 | 49.8 | 52.8 |
| 10-28 12Z | Wed 07:00 | 51.8 | 52.4 | 49.8 | 51.8 | 54.0 | 50.3 | 53.0 | 51.0 | 49.1 | 50.4 | 53.0 |
| 10-28 13Z | Wed 08:00 | 52.2 | 52.5 |  | 52.6 |  |  |  |  | 50.7 | 51.8 | 53.9 |
| 10-28 14Z | Wed 09:00 | 53.2 | 53.2 |  | 54.7 |  |  |  |  | 53.2 | 54.0 | 55.1 |
| 10-28 15Z | Wed 10:00 | 55.2 | 55.1 | 57.0 | 57.9 | 56.1 |  | 58.0 | 57.0 | 56.0 | 56.6 | 56.6 |
| 10-28 16Z | Wed 11:00 | 57.5 | 58.0 |  | 60.9 |  |  |  |  | 59.1 | 59.2 | 58.3 |
| 10-28 17Z | Wed 12:00 | 59.4 | 59.9 |  | 64.7 |  |  |  |  | 62.5 | 61.5 | 60.3 |
| 10-28 18Z | Wed 13:00 | 61.7 | 61.8 | 65.8 | 65.0 | 59.7 | 62.4 | 65.0 | 65.0 | 65.0 | 63.0 | 62.3 |
| 10-28 19Z | Wed 14:00 | 60.4 | 63.9 |  | 63.1 |  |  |  |  | 66.2 | 63.7 | 64.3 |
| 10-28 20Z | Wed 15:00 | 60.6 | 65.1 |  | 66.7 |  |  |  |  | 66.5 | 64.2 | 66.3 |
| 10-28 21Z | Wed 16:00 | 62.7 | 65.9 | 66.6 | 67.7 | 65.0 |  | 67.0 | 67.0 | 66.1 | 64.2 | 67.5 |
| 10-28 22Z | Wed 17:00 | 61.8 | 65.0 |  | 66.8 |  |  |  |  | 64.7 | 63.9 | 67.1 |
| 10-28 23Z | Wed 18:00 | 61.6 | 63.8 |  | 61.3 |  |  |  |  | 62.7 | 63.3 | 66.0 |
| 10-29 00Z | Wed 19:00 | 62.5 | 62.8 | 59.9 | 61.3 | 63.9 | 61.1 | 65.0 | 63.0 | 61.0 | 62.4 | 64.7 |
| 10-29 01Z | Wed 20:00 | 62.4 | 63.2 |  | 59.4 |  |  |  |  | 60.0 | 61.0 | 63.8 |
| 10-29 02Z | Wed 21:00 | 60.7 | 63.1 |  | 58.6 |  |  |  |  | 59.3 | 59.0 | 62.9 |
| 10-29 03Z | Wed 22:00 | 57.9 | 62.3 | 57.2 | 58.3 | 61.8 |  | 62.0 | 59.0 | 58.3 | 56.8 | 61.8 |
| 10-29 04Z | Wed 23:00 | 54.9 | 61.1 |  | 57.0 |  |  |  |  | 56.7 | 54.4 | 60.3 |
| 10-29 05Z | Thu 00:00 | 53.1 | 59.5 |  | 55.3 |  |  |  |  | 54.8 | 52.2 | 58.6 |
| 10-29 06Z | Thu 01:00 | 50.9 | 57.2 | 51.8 | 52.7 | 55.2 | 49.9 | 57.0 | 54.0 | 53.1 | 50.3 | 56.9 |

Dewpoint (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 49.8 | 50.4 | 50.4 | 51.2 | 51.3 | 49.1 | 50.0 | 52.0 | 51.2 | 49.4 | 50.2 |
| 10-28 07Z | Wed 02:00 | 50.0 | 50.5 |  | 51.1 |  |  |  |  | 50.8 | 49.2 | 50.3 |
| 10-28 08Z | Wed 03:00 | 50.3 | 50.6 |  | 50.6 |  |  |  |  | 50.4 | 49.0 | 50.7 |
| 10-28 09Z | Wed 04:00 | 50.5 | 50.6 | 49.4 | 51.1 | 51.6 |  | 50.0 | 52.0 | 49.9 | 48.7 | 50.9 |
| 10-28 10Z | Wed 05:00 | 50.7 | 50.8 |  | 50.7 |  |  |  |  | 49.2 | 48.6 | 51.0 |
| 10-28 11Z | Wed 06:00 | 51.1 | 51.5 |  | 51.4 |  |  |  |  | 48.5 | 48.7 | 51.0 |
| 10-28 12Z | Wed 07:00 | 51.2 | 51.5 | 49.1 | 51.1 | 53.0 | 49.3 | 50.0 | 51.0 | 48.7 | 49.1 | 51.0 |
| 10-28 13Z | Wed 08:00 | 51.6 | 51.5 |  | 51.9 |  |  |  |  | 50.2 | 50.0 | 50.8 |
| 10-28 14Z | Wed 09:00 | 52.4 | 52.3 |  | 53.9 |  |  |  |  | 52.5 | 51.2 | 50.5 |
| 10-28 15Z | Wed 10:00 | 53.8 | 53.9 | 56.0 | 56.2 | 52.7 |  | 52.0 | 54.0 | 54.6 | 52.6 | 50.4 |
| 10-28 16Z | Wed 11:00 | 55.5 | 55.8 |  | 56.2 |  |  |  |  | 55.9 | 53.9 | 50.6 |
| 10-28 17Z | Wed 12:00 | 57.1 | 56.7 |  | 56.5 |  |  |  |  | 56.6 | 55.1 | 51.0 |
| 10-28 18Z | Wed 13:00 | 58.3 | 56.6 | 56.7 | 55.8 | 53.2 | 56.0 | 55.0 | 56.0 | 57.1 | 56.0 | 51.5 |
| 10-28 19Z | Wed 14:00 | 58.0 | 56.6 |  | 58.3 |  |  |  |  | 57.6 | 56.9 | 52.4 |
| 10-28 20Z | Wed 15:00 | 57.6 | 57.2 |  | 57.6 |  |  |  |  | 58.1 | 57.8 | 53.5 |
| 10-28 21Z | Wed 16:00 | 58.7 | 59.4 | 58.3 | 57.9 | 53.7 |  | 55.0 | 58.0 | 58.5 | 58.6 | 54.7 |
| 10-28 22Z | Wed 17:00 | 59.8 | 60.2 |  | 58.0 |  |  |  |  | 58.9 | 59.1 | 55.6 |
| 10-28 23Z | Wed 18:00 | 60.4 | 60.7 |  | 59.9 |  |  |  |  | 59.0 | 59.3 | 56.4 |
| 10-29 00Z | Wed 19:00 | 61.8 | 60.5 | 58.9 | 59.9 | 57.0 | 58.2 | 55.0 | 58.0 | 58.8 | 58.9 | 56.9 |
| 10-29 01Z | Wed 20:00 | 61.0 | 60.8 |  | 58.3 |  |  |  |  | 58.6 | 57.8 | 57.5 |
| 10-29 02Z | Wed 21:00 | 59.2 | 61.6 |  | 57.9 |  |  |  |  | 58.1 | 56.0 | 57.8 |
| 10-29 03Z | Wed 22:00 | 55.7 | 60.5 | 56.6 | 57.7 | 58.8 |  | 55.0 | 58.0 | 57.3 | 53.9 | 57.3 |
| 10-29 04Z | Wed 23:00 | 52.8 | 58.2 |  | 56.5 |  |  |  |  | 55.8 | 51.7 | 55.7 |
| 10-29 05Z | Thu 00:00 | 50.7 | 57.0 |  | 54.6 |  |  |  |  | 53.9 | 49.5 | 53.2 |
| 10-29 06Z | Thu 01:00 | 49.4 | 56.0 | 50.9 | 51.9 | 51.8 | 47.2 | 50.0 | 53.0 | 52.0 | 47.8 | 50.8 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 95 | 93 | 96 | 96 | 97 | 94 | 86 | 96 | 94 | 92 | 88 |
| 10-28 07Z | Wed 02:00 | 96 | 93 |  | 96 |  |  |  |  | 95 | 92 | 89 |
| 10-28 08Z | Wed 03:00 | 97 | 94 |  | 96 |  |  |  |  | 96 | 94 | 91 |
| 10-28 09Z | Wed 04:00 | 97 | 94 | 96 | 96 | 96 |  | 90 | 100 | 97 | 95 | 92 |
| 10-28 10Z | Wed 05:00 | 97 | 95 |  | 96 |  |  |  |  | 97 | 96 | 93 |
| 10-28 11Z | Wed 06:00 | 98 | 98 |  | 97 |  |  |  |  | 98 | 96 | 94 |
| 10-28 12Z | Wed 07:00 | 98 | 97 | 97 | 97 | 96 | 96 | 90 | 100 | 98 | 95 | 93 |
| 10-28 13Z | Wed 08:00 | 98 | 96 |  | 97 |  |  |  |  | 98 | 93 | 90 |
| 10-28 14Z | Wed 09:00 | 97 | 97 |  | 97 |  |  |  |  | 97 | 90 | 85 |
| 10-28 15Z | Wed 10:00 | 95 | 96 | 96 | 94 | 88 |  | 80 | 90 | 95 | 87 | 80 |
| 10-28 16Z | Wed 11:00 | 93 | 92 |  | 85 |  |  |  |  | 89 | 83 | 76 |
| 10-28 17Z | Wed 12:00 | 92 | 89 |  | 75 |  |  |  |  | 81 | 80 | 71 |
| 10-28 18Z | Wed 13:00 | 89 | 83 | 72 | 72 | 79 | 80 | 70 | 73 | 76 | 78 | 68 |
| 10-28 19Z | Wed 14:00 | 92 | 77 |  | 84 |  |  |  |  | 74 | 79 | 65 |
| 10-28 20Z | Wed 15:00 | 90 | 76 |  | 73 |  |  |  |  | 75 | 80 | 64 |
| 10-28 21Z | Wed 16:00 | 87 | 80 | 75 | 71 | 67 |  | 65 | 73 | 77 | 82 | 64 |
| 10-28 22Z | Wed 17:00 | 93 | 84 |  | 73 |  |  |  |  | 82 | 85 | 67 |
| 10-28 23Z | Wed 18:00 | 96 | 90 |  | 95 |  |  |  |  | 88 | 87 | 72 |
| 10-29 00Z | Wed 19:00 | 98 | 92 | 96 | 95 | 78 | 90 | 70 | 84 | 93 | 88 | 76 |
| 10-29 01Z | Wed 20:00 | 95 | 92 |  | 96 |  |  |  |  | 95 | 89 | 80 |
| 10-29 02Z | Wed 21:00 | 95 | 95 |  | 98 |  |  |  |  | 96 | 90 | 83 |
| 10-29 03Z | Wed 22:00 | 92 | 94 | 98 | 98 | 90 |  | 78 | 96 | 97 | 90 | 85 |
| 10-29 04Z | Wed 23:00 | 93 | 90 |  | 98 |  |  |  |  | 97 | 91 | 85 |
| 10-29 05Z | Thu 00:00 | 92 | 91 |  | 97 |  |  |  |  | 97 | 91 | 83 |
| 10-29 06Z | Thu 01:00 | 95 | 96 | 97 | 97 | 88 | 90 | 77 | 96 | 96 | 91 | 80 |

Wind speed (kt) at the hour:

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 5.5 | 2.8 | 4.9 | 4.8 | 3.6 | 5.0 | 5.0 | 7.0 | 5.9 | 6.1 | 5.2 |
| 10-28 07Z | Wed 02:00 | 5.3 | 2.8 |  | 4.3 |  |  |  |  | 5.5 | 5.7 | 5.0 |
| 10-28 08Z | Wed 03:00 | 3.8 | 1.2 |  | 4.1 |  |  |  |  | 4.9 | 4.9 | 4.9 |
| 10-28 09Z | Wed 04:00 | 2.3 | 1.0 | 4.3 | 4.0 | 3.6 |  | 5.0 | 5.0 | 4.4 | 4.2 | 4.7 |
| 10-28 10Z | Wed 05:00 | 2.2 | 3.1 |  | 4.6 |  |  |  |  | 3.9 | 3.7 | 4.5 |
| 10-28 11Z | Wed 06:00 | 2.6 | 4.4 |  | 3.6 |  |  |  |  | 3.7 | 3.6 | 4.3 |
| 10-28 12Z | Wed 07:00 | 3.6 | 5.1 | 3.4 | 3.2 | 3.8 | 3.4 | 5.0 | 5.0 | 3.8 | 3.9 | 4.4 |
| 10-28 13Z | Wed 08:00 | 4.0 | 5.3 |  | 3.7 |  |  |  |  | 4.1 | 4.5 | 4.7 |
| 10-28 14Z | Wed 09:00 | 4.7 | 4.8 |  | 5.9 |  |  |  |  | 4.8 | 5.4 | 5.3 |
| 10-28 15Z | Wed 10:00 | 5.2 | 5.5 | 5.7 | 5.5 | 4.8 |  | 8.0 | 7.0 | 5.4 | 6.5 | 6.1 |
| 10-28 16Z | Wed 11:00 | 5.7 | 6.0 |  | 5.2 |  |  |  |  | 5.8 | 7.5 | 6.9 |
| 10-28 17Z | Wed 12:00 | 6.6 | 7.3 |  | 6.1 |  |  |  |  | 6.3 | 8.2 | 8.0 |
| 10-28 18Z | Wed 13:00 | 7.7 | 6.6 | 7.7 | 8.1 | 7.4 | 8.0 | 12.0 | 11.0 | 6.7 | 8.3 | 8.9 |
| 10-28 19Z | Wed 14:00 | 8.4 | 7.4 |  | 4.8 |  |  |  |  | 7.5 | 7.7 | 9.6 |
| 10-28 20Z | Wed 15:00 | 8.1 | 9.4 |  | 7.3 |  |  |  |  | 8.3 | 7.1 | 10.2 |
| 10-28 21Z | Wed 16:00 | 8.7 | 9.4 | 7.3 | 7.1 | 9.7 |  | 15.0 | 12.0 | 8.5 | 7.0 | 10.5 |
| 10-28 22Z | Wed 17:00 | 7.9 | 8.4 |  | 7.6 |  |  |  |  | 8.1 | 7.8 | 10.4 |
| 10-28 23Z | Wed 18:00 | 7.8 | 6.7 |  | 5.9 |  |  |  |  | 8.2 | 8.8 | 10.3 |
| 10-29 00Z | Wed 19:00 | 13.0 | 12.9 | 6.5 | 8.3 | 9.1 | 7.0 | 13.0 | 11.0 | 8.6 | 9.4 | 9.9 |
| 10-29 01Z | Wed 20:00 | 11.6 | 11.0 |  | 6.7 |  |  |  |  | 8.3 | 9.1 | 9.1 |
| 10-29 02Z | Wed 21:00 | 10.3 | 9.4 |  | 5.8 |  |  |  |  | 7.9 | 8.4 | 8.6 |
| 10-29 03Z | Wed 22:00 | 9.6 | 7.6 | 5.1 | 5.0 | 8.5 |  | 10.0 | 10.0 | 7.6 | 7.5 | 8.6 |
| 10-29 04Z | Wed 23:00 | 7.6 | 9.5 |  | 6.8 |  |  |  |  | 7.2 | 6.9 | 8.3 |
| 10-29 05Z | Thu 00:00 | 8.2 | 5.4 |  | 6.4 |  |  |  |  | 7.3 | 6.8 | 8.7 |
| 10-29 06Z | Thu 01:00 | 8.2 | 6.1 | 6.4 | 5.7 | 8.6 | 6.6 | 10.0 | 9.0 | 7.8 | 6.9 | 9.5 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 07Z | Wed 02:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 |
| 10-28 08Z | Wed 03:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 |
| 10-28 09Z | Wed 04:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  | 0.00 | 0.00 | 0.00 |
| 10-28 10Z | Wed 05:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 |
| 10-28 11Z | Wed 06:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 |
| 10-28 12Z | Wed 07:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 13Z | Wed 08:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.01 | 0.00 |
| 10-28 14Z | Wed 09:00 | 0.01 | 0.00 |  | 0.00 |  |  | 0.00 | 0.01 | 0.00 |
| 10-28 15Z | Wed 10:00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 |  | 0.00 | 0.02 | 0.00 |
| 10-28 16Z | Wed 11:00 | 0.01 | 0.00 |  | 0.00 |  |  | 0.00 | 0.02 | 0.00 |
| 10-28 17Z | Wed 12:00 | 0.01 | 0.00 |  | 0.00 |  |  | 0.01 | 0.03 | 0.01 |
| 10-28 18Z | Wed 13:00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.02 | 0.07 | 0.01 | 0.03 | 0.01 |
| 10-28 19Z | Wed 14:00 | 0.01 | 0.01 |  | 0.11 |  |  | 0.02 | 0.08 | 0.03 |
| 10-28 20Z | Wed 15:00 | 0.03 | 0.01 |  | 0.11 |  |  | 0.03 | 0.12 | 0.04 |
| 10-28 21Z | Wed 16:00 | 0.03 | 0.02 | 0.02 | 0.11 | 0.03 |  | 0.05 | 0.17 | 0.06 |
| 10-28 22Z | Wed 17:00 | 0.03 | 0.03 |  | 0.11 |  |  | 0.10 | 0.21 | 0.10 |
| 10-28 23Z | Wed 18:00 | 0.04 | 0.03 |  | 0.29 |  |  | 0.15 | 0.26 | 0.15 |
| 10-29 00Z | Wed 19:00 | 0.24 | 0.06 | 0.20 | 0.46 | 0.09 | 0.49 | 0.20 | 0.31 | 0.20 |
| 10-29 01Z | Wed 20:00 | 0.28 | 0.06 |  | 0.54 |  |  | 0.24 | 0.31 | 0.23 |
| 10-29 02Z | Wed 21:00 | 0.28 | 0.09 |  | 0.72 |  |  | 0.29 | 0.32 | 0.25 |
| 10-29 03Z | Wed 22:00 | 0.28 | 0.11 | 0.40 | 0.73 | 0.17 |  | 0.33 | 0.33 | 0.28 |
| 10-29 04Z | Wed 23:00 | 0.28 | 0.11 |  | 0.73 |  |  | 0.33 | 0.34 | 0.28 |
| 10-29 05Z | Thu 00:00 | 0.28 | 0.11 |  | 0.73 |  |  | 0.33 | 0.34 | 0.28 |
| 10-29 06Z | Thu 01:00 | 0.28 | 0.11 | 0.40 | 0.73 | 0.17 | 0.53 | 0.33 | 0.35 | 0.28 |

Total cloud cover (%):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 100 | 100 | 16 | 32 | 9 | 55 | 100 | 72 | 22 | 67 | 27 |
| 10-28 07Z | Wed 02:00 | 100 | 100 |  | 21 |  |  |  | 66 | 19 | 67 | 28 |
| 10-28 08Z | Wed 03:00 | 100 | 100 |  | 39 |  |  |  | 73 | 13 | 66 | 31 |
| 10-28 09Z | Wed 04:00 | 100 | 100 | 9 | 30 | 6 |  | 100 | 74 | 10 | 66 | 34 |
| 10-28 10Z | Wed 05:00 | 100 | 97 |  | 47 |  |  |  | 70 | 10 | 66 | 36 |
| 10-28 11Z | Wed 06:00 | 100 | 89 |  | 34 |  |  |  | 86 | 13 | 66 | 39 |
| 10-28 12Z | Wed 07:00 | 100 | 100 | 41 | 70 | 75 | 72 | 100 | 90 | 17 | 67 | 43 |
| 10-28 13Z | Wed 08:00 | 100 | 82 |  | 71 |  |  |  | 89 | 25 | 67 | 48 |
| 10-28 14Z | Wed 09:00 | 100 | 87 |  | 0 |  |  |  | 83 | 36 | 67 | 54 |
| 10-28 15Z | Wed 10:00 | 100 | 90 | 50 | 89 | 100 |  | 100 | 81 | 46 | 68 | 60 |
| 10-28 16Z | Wed 11:00 | 99 | 87 |  | 38 |  |  |  |  | 54 | 68 | 67 |
| 10-28 17Z | Wed 12:00 | 98 | 73 |  | 81 |  |  |  |  | 61 | 70 | 74 |
| 10-28 18Z | Wed 13:00 | 98 | 75 | 53 | 77 | 13 | 78 | 100 | 79 | 65 | 71 | 78 |
| 10-28 19Z | Wed 14:00 | 100 | 81 |  | 45 |  |  |  |  | 63 | 74 | 76 |
| 10-28 20Z | Wed 15:00 | 76 | 76 |  | 56 |  |  |  |  | 59 | 79 | 72 |
| 10-28 21Z | Wed 16:00 | 37 | 57 | 41 | 23 | 100 |  | 100 | 69 | 59 | 85 | 70 |
| 10-28 22Z | Wed 17:00 | 100 | 45 |  | 96 |  |  |  |  | 71 | 89 | 75 |
| 10-28 23Z | Wed 18:00 | 100 | 43 |  | 99 |  |  |  |  | 88 | 91 | 84 |
| 10-29 00Z | Wed 19:00 | 100 | 56 | 100 | 87 | 100 | 85 | 100 | 85 | 97 | 90 | 89 |
| 10-29 01Z | Wed 20:00 | 74 | 38 |  | 91 |  |  |  |  | 88 | 83 | 87 |
| 10-29 02Z | Wed 21:00 | 100 | 51 |  | 97 |  |  |  |  | 71 | 72 | 82 |
| 10-29 03Z | Wed 22:00 | 100 | 54 | 23 | 52 | 98 |  | 100 | 66 | 57 | 58 | 75 |
| 10-29 04Z | Wed 23:00 | 84 | 69 |  | 29 |  |  |  |  | 47 | 44 | 65 |
| 10-29 05Z | Thu 00:00 | 60 | 52 |  | 4 |  |  |  |  | 37 | 31 | 54 |
| 10-29 06Z | Thu 01:00 | 22 | 6 | 0 | 0 | 3 | 14 | 44 | 64 | 29 | 22 | 44 |

## Track record this period

Since 2026-10-12 at KMSP (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-27 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 15 | 5.4 | -0.8 | +0.0 | -2.0 | +0.01 | 1.6 | 1.0 | 2.6 | 0.05 |
| NBM | 15 | 7.3 | -0.8 | +0.4 | -3.9 | -0.02 | 2.5 | 1.4 | 4.0 | 0.04 |
| GFS_MOS | 15 | 7.8 | -0.7 | +0.7 | -3.6 | -0.01 | 2.3 | 3.0 | 3.9 | 0.02 |
| HRRR | 15 | 8.5 | -1.4 | -2.3 | -4.9 | +0.03 | 1.8 | 2.6 | 4.9 | 0.08 |
| RRFS | 15 | 8.5 | +0.0 | -1.7 | -5.3 | +0.01 | 1.3 | 3.0 | 5.3 | 0.07 |
| GFS | 15 | 9.8 | -0.2 | +3.3 | -5.8 | +0.02 | 1.8 | 3.3 | 5.8 | 0.07 |
| AIFS | 15 | 10.1 | -2.9 | -2.0 | -6.0 | +0.03 | 3.0 | 2.4 | 6.0 | 0.06 |
| IFS_HRES | 15 | 10.3 | -0.8 | +0.9 | -6.2 | +0.00 | 3.4 | 2.0 | 6.2 | 0.06 |
| IFS | 15 | 10.5 | -1.3 | +0.4 | -6.4 | +0.02 | 3.2 | 1.7 | 6.4 | 0.08 |

## Daily verification (all 15 days this period)

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
| 10-26 h | 8.7 | 9.3 | 6.8 | 9.4 | 6.7 | 8.0 | 5.7 | 3.7 | 4.6 | NBM |

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
| 10-26 h | 49 | +1 | +1 | +0 | +2 | -1 | -3 | -1 | +0 | +1 |

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
| 10-26 h | 42 | +1 | +2 | +2 | +3 | +0 | +0 | -3 | +1 | +1 |

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
| 10-26 h | 15 | -5 | -4 | -6 | -6 | -6 | -6 | -3 | -3 | +0 |

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
| 10-26 h | 0.38 | +0.30 | +0.31 | +0.09 | +0.07 | +0.15 | +0.10 | +0.01 | +0.06 | +0.14 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 15 | +15 | 16 | +10 | 11 |
| RRFS | 15 | +6 | 8 | +11 | 14 |
| IFS | 15 | +2 | 11 | -2 | 8 |
| IFS_HRES | 15 | +2 | 12 | +0 | 8 |
| GFS | 15 | +8 | 17 | +2 | 14 |
| AIFS | 15 | +8 | 12 | +4 | 6 |
| GFS_MOS | 15 | -2 | 3 | +2 | 13 |
| NBM | 15 | -1 | 11 | -5 | 10 |

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
| 10-26 h | 100% | 100% | +0 | +0 | +0 | +0 | +0 | +0 | +0 | -12 |

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
| 10-26 h | 100% | 100% | +0 | +0 | +0 | +0 | +0 | +0 | +0 | -10 |

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 15 | +0.1 | 1.8 | +1.4 | 2.0 |
| RRFS | 15 | +0.2 | 1.7 | +1.0 | 1.3 |
| IFS | 15 | +1.6 | 2.2 | +1.9 | 2.4 |
| IFS_HRES | 15 | +1.6 | 2.1 | +1.9 | 2.8 |
| GFS | 15 | -1.3 | 2.7 | -2.6 | 2.8 |
| AIFS | 15 | +0.0 | 1.5 | +0.3 | 1.1 |
| GFS_MOS | 15 | +0.2 | 2.0 | +0.4 | 2.1 |
| NBM | 15 | +0.7 | 1.3 | +0.0 | 1.3 |

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
| 10-26 h | 35.2 | -3.8 | -3.9 | +1.2 | +0.7 | -3.7 | +1.9 | -1.2 | -0.2 |

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
| 10-26 h | 38.1 | -0.1 | +1.5 | +0.7 | +1.5 | -5.5 | +0.1 | -3.1 | -2.1 |

## Today so far (2026-10-27, through 2026-10-27T13:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 46.9 °F, low 44.1 °F, max wind 14 kt, precip 0.14" (8 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 26/18Z | -0.1 | 0.4 | 53 (+6) pending | 44 (+0) | -1.4 | 0.24 | +0.10 |
| RRFS | 26/18Z | +1.0 | 1.1 | 55 (+8) pending | 44 (+0) | -2.3 | 0.11 | -0.03 |
| IFS | 26/12Z | +1.5 | 1.5 | 59 (+12) pending | 44 (+0) | -1.7 | 0.30 | +0.16 |
| IFS_HRES | 26/12Z | +1.6 | 1.6 | 59 (+12) pending | 45 (+1) | -1.8 | 0.35 | +0.21 |
| GFS | 26/18Z | -0.1 | 0.9 | 56 (+10) pending | 43 (-1) | -2.1 | 0.23 | +0.09 |
| AIFS | 26/12Z | -0.6 | 0.8 | 54 (+7) pending | 42 (-2) | -2.6 | 0.22 | +0.08 |
| GFS_MOS | 26/18Z | -2.1 | 2.1 | 58 (+11) pending | 41 (-3) | -0.6 | — | — |
| NBM | 26/22Z | +0.9 | 0.9 | 62 (+15) pending | 43 (-1) | +1.2 | — | — |
| USL | 26/22Z | +1.1 | 1.1 | 59 (+12) pending | 44 (+0) | -0.2 | 0.21 | +0.07 |
| ENS | 26/00Z | +1.0 | 1.0 | 60 (+14) pending | 45 (+1) | -0.6 | 0.28 | +0.14 |
| AIFS_ENS | 26/12Z | -0.1 | 1.1 | 55 (+8) pending | 43 (-1) | -2.2 | 0.25 | +0.11 |
| GEFS | 26/18Z | -0.1 | 0.5 | 58 (+11) pending | 44 (+0) | -0.9 | 0.21 | +0.07 |

## Clouds so far today (2026-10-27, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-19 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (CDT) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 100 | 100 | 100 | 76 | 81 | 87 | 100 | 89 | 100 | 90 | 100 | 95 | 95 | 100 |
| 10-27 07Z | Tue 02:00 | 100 | 100 | 100 | 92 |  | 86 |  |  |  | 88 | 100 | 95 | 94 | 99 |
| 10-27 08Z | Tue 03:00 | 100 | 100 | 100 | 97 |  | 100 |  |  |  | 85 | 100 | 96 | 92 | 98 |
| 10-27 09Z | Tue 04:00 | 100 | 100 | 73 | 100 | 98 | 100 | 100 |  | 100 | 86 | 100 | 96 | 90 | 98 |
| 10-27 10Z | Tue 05:00 | 100 | 100 | 100 | 80 |  | 99 |  |  |  | 85 | 100 | 92 | 89 | 98 |
| 10-27 11Z | Tue 06:00 | 100 | 100 | 100 | 71 |  | 50 |  |  |  | 73 | 100 | 87 | 88 | 98 |
| 10-27 12Z | Tue 07:00 | 97 | 100 | 100 | 67 | 98 | 82 | 100 | 85 | 100 | 71 | 100 | 85 | 87 | 98 |
| 10-27 13Z | Tue 08:00 | 100 | 100 | 100 | 76 |  | 84 |  |  |  | 64 | 100 | 88 | 88 | 99 |
| 10-27 14Z | Tue 09:00 | 100 | 100 | 100 | 96 |  | 100 |  |  |  | 74 | 100 | 94 | 90 | 99 |

## Dewpoint so far today (2026-10-27, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (CDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 41.0 | 86 | 42.3 | 39.8 | 43.1 | 43.3 | 39.4 | 40.8 | 38.0 | 42.0 | 41.0 | 43.8 | 41.2 | 37.4 |
| 10-27 07Z | Tue 02:00 | 41.0 | 86 | 42.4 | 40.3 |  | 43.1 |  |  |  |  | 41.0 | 44.0 | 41.5 | 37.3 |
| 10-27 08Z | Tue 03:00 | 42.1 | 90 | 42.5 | 41.1 |  | 43.5 |  |  |  |  | 41.0 | 44.2 | 41.9 | 37.3 |
| 10-27 09Z | Tue 04:00 | 42.1 | 90 | 42.2 | 43.1 | 44.1 | 44.7 | 39.4 |  | 39.0 | 43.0 | 42.0 | 44.3 | 42.3 | 37.4 |
| 10-27 10Z | Tue 05:00 | 42.1 | 93 | 41.9 | 43.3 |  | 45.1 |  |  |  |  | 42.0 | 44.4 | 42.7 | 37.8 |
| 10-27 11Z | Tue 06:00 | 39.9 | 85 | 41.8 | 41.9 |  | 46.1 |  |  |  |  | 42.0 | 44.4 | 43.3 | 38.4 |
| 10-27 12Z | Tue 07:00 | 43.0 | 93 | 42.2 | 41.9 | 45.6 | 46.1 | 40.5 | 43.4 | 41.0 | 44.0 | 43.0 | 44.7 | 44.0 | 39.1 |
| 10-27 13Z | Tue 08:00 | 43.0 | 89 | 43.2 | 42.6 |  | 45.9 |  |  |  |  | 43.0 | 45.3 | 45.1 | 39.9 |
| 10-27 14Z | Tue 09:00 | 43.0 | 86 | 44.3 | 43.7 |  | 47.5 |  |  |  |  | 44.0 | 46.1 | 46.3 | 40.7 |
| Bias so far |  |  |  | +0.6 | +0.1 | +2.2 | +3.1 | -2.3 | +0.1 | -2.7 | +1.0 | +0.2 | +2.7 | +1.2 | -3.5 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (MPX): https://forecast.weather.gov/product.php?site=mpx&issuedby=mpx&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
