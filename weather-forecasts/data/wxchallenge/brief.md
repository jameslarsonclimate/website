# WxChallenge forecast brief: Minneapolis, MN (KMSP)

- Station: **KMSP**
- Target day: **2026-10-28**, scored over 2026-10-28T06Z to 2026-10-29T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-28T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-27T21:24:09+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 27/18Z | 65.8 | 50.3 | 12.0 | 0.15 |
| RRFS | 27/18Z | 66.9 | 50.4 | 9.6 | 0.46 |
| IFS | 27/12Z | 67.9 | 48.0 | 8.0 | 0.61 |
| IFS_HRES | 27/12Z | 68.0 | 49.6 | 8.0 | 0.87 |
| GFS | 27/12Z | 68.4 | 52.6 | 10.1 | 0.18 |
| AIFS | 27/12Z | 62.2 | 48.8 | 8.3 | 0.53 |
| GFS_MOS | 27/12Z | 69.0 | 52.0 | 14.0 | 0.10 |
| NBM | 27/20Z | 70.0 | 51.0 | 12.0 | 0.26 |
| USL | 27/12Z | 69.0 | 51.0 | 16.0 | 0.26 |
| ENS | 27/06Z | 67.3 | 49.1 | 9.5 | 0.40 |
| GEFS | 27/12Z | 68.3 | 52.7 | 11.9 | 0.25 |
| AIFS_ENS | 27/12Z | 65.0 | 47.0 | 10.3 | 0.41 |
| HRRRCAST (precip only) | 27/12Z | — | — | — | 0.14 |
| REFS (precip only) | 27/18Z | — | — | — | 0.21 |
| NBM_QMD (precip only) | 27/12Z | — | — | — | 0.51 |
| **CONSENSUS** |  | **68.0** | **50.1** | **15.1** | **0.33** |

Notes:
- IFS_HRES: not in the consensus
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [0, 0, 1, 1] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- HRRRCAST: median of 18 members (experimental AI model)
- REFS: median of 14 members, 18Z + 12Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS and IFS_HRES (the IFS run at its native 9 km, hourly; IFS is the same run on the 0.25 deg open-data grid) are shown and scored but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: RRFS 0.16, HRRR 0.12, GFS 0.12, GFS_MOS 0.10, NBM 0.09, USL 0.09, AIFS 0.08, AIFS_ENS 0.08, IFS 0.07, ENS 0.07 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Low °F weights: NBM 0.14, IFS 0.13, ENS 0.13, AIFS 0.09, USL 0.09, AIFS_ENS 0.09, HRRR 0.09, GFS_MOS 0.08, RRFS 0.08, GFS 0.07 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Wind kt weights: GFS_MOS 0.13, NBM 0.13, HRRR 0.11, RRFS 0.10, GFS 0.09, USL 0.09, AIFS 0.09, AIFS_ENS 0.09, IFS 0.08, ENS 0.08 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)
- Precip in weights: GFS_MOS 0.11, NBM 0.10, AIFS 0.10, AIFS_ENS 0.10, GFS 0.10, USL 0.10, RRFS 0.10, HRRR 0.10, IFS 0.10, ENS 0.10 (no track record yet: USL) (using parent's track record: ENS from IFS, AIFS_ENS from AIFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 65.1 | 66.4 | 67.3 | 68.5 | 69.1 | 67.3 |
| ENS | 51 | Low °F | 47.4 | 48.0 | 49.0 | 49.6 | 51.6 | 49.1 |
| ENS | 51 | Wind kt | 7.7 | 8.3 | 9.7 | 10.7 | 11.5 | 9.5 |
| ENS | 51 | Precip in | 0.17 | 0.25 | 0.35 | 0.50 | 0.68 | 0.40 |
| GEFS | 31 | High °F | 66.8 | 67.3 | 68.5 | 69.0 | 69.8 | 68.3 |
| GEFS | 31 | Low °F | 51.3 | 52.0 | 52.8 | 53.5 | 54.0 | 52.7 |
| GEFS | 31 | Wind kt | 10.3 | 10.8 | 11.6 | 12.8 | 13.7 | 11.9 |
| GEFS | 31 | Precip in | 0.13 | 0.14 | 0.24 | 0.29 | 0.45 | 0.25 |
| AIFS_ENS | 51 | High °F | 62.7 | 64.2 | 65.4 | 66.0 | 66.6 | 65.0 |
| AIFS_ENS | 51 | Low °F | 44.9 | 46.0 | 47.0 | 48.0 | 49.5 | 47.0 |
| AIFS_ENS | 51 | Wind kt | 8.6 | 9.6 | 10.3 | 10.9 | 11.8 | 10.3 |
| AIFS_ENS | 51 | Precip in | 0.19 | 0.23 | 0.33 | 0.55 | 0.76 | 0.41 |
| HRRRCAST | 18 | Precip in | 0.02 | 0.04 | 0.14 | 0.21 | 0.31 | 0.15 |
| REFS | 14 | Precip in | 0.08 | 0.15 | 0.21 | 0.30 | 0.56 | 0.29 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 98% | 74% | 26% |
| GEFS | 100% | 90% | 39% | 6% |
| AIFS_ENS | 100% | 100% | 71% | 31% |
| HRRRCAST | 100% | 56% | 17% | 0% |
| REFS | 100% | 86% | 36% | 14% |

NBM QMD calibrated 24-h precip percentiles: p10 0.14", p25 0.29", p50 0.51", p75 0.69", p90 0.89"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 3% | 6% | 63% | 46% | 63% to 82% | — |
| NBM | NBS P06 | 9% | 16% | 79% | 78% | 79% to 96% | — |
| ENS | member fraction | 4% | 39% | 98% | 98% | 100% | — |
| GEFS | member fraction | 0% | 23% | 100% | 100% | 100% | — |
| AIFS_ENS | member fraction | 4% | 71% | 100% | 59% | 100% | — |
| HRRRCAST | member fraction | — | — | — | — | 100% | — |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 8% | 16% | 79% | 78% | 100% | — |

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS, AIFS_ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 51.1 | 50.6 | 51.1 | 51.9 | 52.6 | 50.8 | 55.0 | 53.0 | 54.0 | 51.9 | 54.0 | 50.3 |
| 10-28 07Z | Wed 02:00 | 50.9 | 50.4 |  | 51.4 |  |  |  |  | 54.0 | 51.5 | 53.9 | 49.8 |
| 10-28 08Z | Wed 03:00 | 50.8 | 50.6 |  | 51.2 |  |  |  |  | 53.0 | 51.1 | 53.8 | 49.1 |
| 10-28 09Z | Wed 04:00 | 50.9 | 50.7 | 49.2 | 50.1 | 53.0 |  | 54.0 | 52.0 | 53.0 | 50.8 | 53.7 | 48.5 |
| 10-28 10Z | Wed 05:00 | 51.0 | 50.7 |  | 49.8 |  |  |  |  | 53.0 | 50.1 | 53.4 | 48.1 |
| 10-28 11Z | Wed 06:00 | 51.2 | 51.1 |  | 50.2 |  |  |  |  | 52.0 | 49.4 | 53.1 | 48.2 |
| 10-28 12Z | Wed 07:00 | 51.4 | 51.3 | 48.2 | 49.6 | 53.2 | 48.8 | 54.0 | 51.0 | 52.0 | 49.5 | 53.3 | 48.9 |
| 10-28 13Z | Wed 08:00 | 51.7 | 51.6 |  | 50.4 |  |  |  |  | 52.0 | 51.1 | 54.2 | 50.6 |
| 10-28 14Z | Wed 09:00 | 52.4 | 52.4 |  | 53.4 |  |  |  |  | 53.0 | 53.5 | 55.5 | 53.1 |
| 10-28 15Z | Wed 10:00 | 55.1 | 54.2 | 56.5 | 57.4 | 58.2 |  | 58.0 | 57.0 | 56.0 | 56.1 | 57.3 | 56.1 |
| 10-28 16Z | Wed 11:00 | 57.3 | 55.1 |  | 60.8 |  |  |  |  | 59.0 | 59.2 | 59.6 | 59.1 |
| 10-28 17Z | Wed 12:00 | 59.7 | 59.5 |  | 64.5 |  |  |  |  | 61.0 | 62.5 | 62.4 | 61.7 |
| 10-28 18Z | Wed 13:00 | 60.8 | 62.3 | 65.8 | 66.8 | 60.2 | 62.2 | 65.0 | 65.0 | 63.0 | 65.0 | 64.7 | 63.4 |
| 10-28 19Z | Wed 14:00 | 62.1 | 65.2 |  | 67.2 |  |  |  |  | 65.0 | 66.4 | 66.4 | 64.2 |
| 10-28 20Z | Wed 15:00 | 62.8 | 66.1 |  | 68.0 |  |  |  |  | 67.0 | 67.0 | 67.6 | 64.6 |
| 10-28 21Z | Wed 16:00 | 65.8 | 66.5 | 66.7 | 67.5 | 65.4 |  | 67.0 | 68.0 | 68.0 | 66.7 | 68.1 | 64.6 |
| 10-28 22Z | Wed 17:00 | 64.0 | 65.5 |  | 63.1 |  |  |  |  | 67.0 | 65.1 | 67.6 | 64.2 |
| 10-28 23Z | Wed 18:00 | 63.0 | 64.9 |  | 60.4 |  |  |  |  | 65.0 | 62.6 | 66.4 | 63.5 |
| 10-29 00Z | Wed 19:00 | 63.5 | 63.8 | 60.2 | 59.6 | 63.4 | 61.3 | 66.0 | 63.0 | 64.0 | 60.6 | 65.2 | 62.4 |
| 10-29 01Z | Wed 20:00 | 63.2 | 63.0 |  | 59.0 |  |  |  |  | 63.0 | 59.5 | 64.4 | 60.8 |
| 10-29 02Z | Wed 21:00 | 61.0 | 62.3 |  | 58.8 |  |  |  |  | 62.0 | 58.9 | 63.5 | 58.5 |
| 10-29 03Z | Wed 22:00 | 57.8 | 61.2 | 57.9 | 58.1 | 61.5 |  | 62.0 | 60.0 | 62.0 | 57.9 | 62.3 | 56.0 |
| 10-29 04Z | Wed 23:00 | 54.4 | 60.4 |  | 56.6 |  |  |  |  | 60.0 | 56.3 | 60.5 | 53.3 |
| 10-29 05Z | Thu 00:00 | 52.2 | 59.0 |  | 54.6 |  |  |  |  | 58.0 | 54.3 | 58.3 | 50.8 |
| 10-29 06Z | Thu 01:00 | 50.3 | 56.5 | 51.8 | 52.5 | 54.4 | 49.0 | 57.0 | 54.0 | 56.0 | 52.4 | 56.4 | 48.7 |

Dewpoint (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 49.6 | 47.0 | 49.6 | 50.5 | 51.3 | 48.7 | 50.0 | 52.0 | 51.0 | 50.1 | 51.0 | 47.9 |
| 10-28 07Z | Wed 02:00 | 49.8 | 47.5 |  | 50.0 |  |  |  |  | 51.0 | 49.9 | 51.0 | 47.7 |
| 10-28 08Z | Wed 03:00 | 50.1 | 48.1 |  | 49.8 |  |  |  |  | 51.0 | 49.8 | 51.3 | 47.3 |
| 10-28 09Z | Wed 04:00 | 50.2 | 48.3 | 48.4 | 48.9 | 51.6 |  | 50.0 | 51.0 | 51.0 | 49.6 | 51.4 | 47.1 |
| 10-28 10Z | Wed 05:00 | 50.3 | 48.8 |  | 48.8 |  |  |  |  | 51.0 | 49.2 | 51.6 | 47.0 |
| 10-28 11Z | Wed 06:00 | 50.3 | 49.5 |  | 49.3 |  |  |  |  | 51.0 | 48.8 | 51.7 | 47.2 |
| 10-28 12Z | Wed 07:00 | 50.6 | 49.7 | 47.5 | 49.0 | 52.0 | 47.8 | 50.0 | 51.0 | 51.0 | 49.0 | 51.9 | 47.7 |
| 10-28 13Z | Wed 08:00 | 51.0 | 50.0 |  | 49.8 |  |  |  |  | 51.0 | 50.5 | 51.8 | 48.8 |
| 10-28 14Z | Wed 09:00 | 51.7 | 50.6 |  | 52.7 |  |  |  |  | 52.0 | 52.7 | 51.6 | 50.3 |
| 10-28 15Z | Wed 10:00 | 53.3 | 51.8 | 55.7 | 56.3 | 53.1 |  | 53.0 | 54.0 | 53.0 | 54.7 | 51.6 | 51.9 |
| 10-28 16Z | Wed 11:00 | 54.7 | 53.2 |  | 57.4 |  |  |  |  | 54.0 | 56.0 | 51.8 | 53.4 |
| 10-28 17Z | Wed 12:00 | 55.6 | 55.6 |  | 57.2 |  |  |  |  | 55.0 | 56.8 | 51.9 | 54.8 |
| 10-28 18Z | Wed 13:00 | 56.3 | 56.5 | 57.3 | 56.7 | 51.7 | 56.1 | 55.0 | 56.0 | 55.0 | 57.3 | 52.1 | 55.9 |
| 10-28 19Z | Wed 14:00 | 58.0 | 57.5 |  | 56.2 |  |  |  |  | 56.0 | 57.9 | 52.8 | 56.9 |
| 10-28 20Z | Wed 15:00 | 59.8 | 59.0 |  | 57.4 |  |  |  |  | 56.0 | 58.4 | 53.9 | 58.0 |
| 10-28 21Z | Wed 16:00 | 61.4 | 60.1 | 58.0 | 59.0 | 53.6 |  | 55.0 | 57.0 | 57.0 | 58.8 | 55.0 | 58.9 |
| 10-28 22Z | Wed 17:00 | 61.6 | 61.0 |  | 60.5 |  |  |  |  | 57.0 | 59.2 | 56.1 | 59.6 |
| 10-28 23Z | Wed 18:00 | 61.6 | 61.4 |  | 59.9 |  |  |  |  | 57.0 | 59.3 | 57.1 | 59.7 |
| 10-29 00Z | Wed 19:00 | 62.6 | 61.3 | 58.9 | 58.6 | 58.8 | 58.2 | 56.0 | 58.0 | 58.0 | 59.0 | 57.6 | 59.1 |
| 10-29 01Z | Wed 20:00 | 61.9 | 60.9 |  | 58.3 |  |  |  |  | 58.0 | 58.6 | 58.0 | 57.7 |
| 10-29 02Z | Wed 21:00 | 59.0 | 60.4 |  | 58.3 |  |  |  |  | 58.0 | 58.1 | 58.2 | 55.5 |
| 10-29 03Z | Wed 22:00 | 55.1 | 59.3 | 56.8 | 57.4 | 58.8 |  | 55.0 | 57.0 | 59.0 | 57.2 | 57.4 | 52.9 |
| 10-29 04Z | Wed 23:00 | 52.2 | 58.4 |  | 55.9 |  |  |  |  | 57.0 | 55.5 | 55.3 | 50.0 |
| 10-29 05Z | Thu 00:00 | 50.0 | 56.3 |  | 54.0 |  |  |  |  | 54.0 | 53.4 | 52.3 | 47.4 |
| 10-29 06Z | Thu 01:00 | 48.6 | 54.4 | 50.9 | 51.6 | 48.3 | 45.8 | 50.0 | 52.0 | 52.0 | 51.3 | 49.5 | 45.3 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 95 | 87 | 95 | 95 | 95 | 92 | 83 | 96 | 90 | 94 | 90 | 92 |
| 10-28 07Z | Wed 02:00 | 96 | 90 |  | 95 |  |  |  |  | 90 | 95 | 90 | 92 |
| 10-28 08Z | Wed 03:00 | 97 | 91 |  | 95 |  |  |  |  | 93 | 95 | 91 | 93 |
| 10-28 09Z | Wed 04:00 | 97 | 91 | 97 | 96 | 95 |  | 86 | 96 | 93 | 96 | 92 | 95 |
| 10-28 10Z | Wed 05:00 | 97 | 93 |  | 96 |  |  |  |  | 93 | 97 | 94 | 96 |
| 10-28 11Z | Wed 06:00 | 97 | 94 |  | 97 |  |  |  |  | 96 | 98 | 95 | 96 |
| 10-28 12Z | Wed 07:00 | 97 | 94 | 97 | 98 | 96 | 96 | 86 | 100 | 96 | 98 | 95 | 96 |
| 10-28 13Z | Wed 08:00 | 97 | 94 |  | 98 |  |  |  |  | 96 | 98 | 92 | 94 |
| 10-28 14Z | Wed 09:00 | 97 | 94 |  | 97 |  |  |  |  | 96 | 97 | 87 | 90 |
| 10-28 15Z | Wed 10:00 | 94 | 92 | 97 | 96 | 83 |  | 83 | 90 | 90 | 95 | 81 | 86 |
| 10-28 16Z | Wed 11:00 | 91 | 93 |  | 89 |  |  |  |  | 83 | 89 | 75 | 82 |
| 10-28 17Z | Wed 12:00 | 86 | 87 |  | 77 |  |  |  |  | 81 | 82 | 69 | 78 |
| 10-28 18Z | Wed 13:00 | 85 | 81 | 74 | 70 | 74 | 80 | 70 | 73 | 75 | 76 | 64 | 77 |
| 10-28 19Z | Wed 14:00 | 86 | 76 |  | 68 |  |  |  |  | 73 | 74 | 62 | 77 |
| 10-28 20Z | Wed 15:00 | 90 | 78 |  | 69 |  |  |  |  | 68 | 74 | 62 | 79 |
| 10-28 21Z | Wed 16:00 | 86 | 80 | 74 | 74 | 66 |  | 65 | 68 | 68 | 76 | 63 | 82 |
| 10-28 22Z | Wed 17:00 | 92 | 85 |  | 91 |  |  |  |  | 70 | 81 | 67 | 85 |
| 10-28 23Z | Wed 18:00 | 95 | 88 |  | 98 |  |  |  |  | 75 | 89 | 72 | 87 |
| 10-29 00Z | Wed 19:00 | 97 | 92 | 95 | 96 | 85 | 90 | 70 | 84 | 81 | 95 | 77 | 89 |
| 10-29 01Z | Wed 20:00 | 96 | 93 |  | 98 |  |  |  |  | 84 | 97 | 80 | 90 |
| 10-29 02Z | Wed 21:00 | 93 | 93 |  | 98 |  |  |  |  | 87 | 97 | 83 | 90 |
| 10-29 03Z | Wed 22:00 | 91 | 93 | 96 | 98 | 91 |  | 78 | 90 | 90 | 97 | 84 | 89 |
| 10-29 04Z | Wed 23:00 | 92 | 93 |  | 98 |  |  |  |  | 90 | 97 | 83 | 89 |
| 10-29 05Z | Thu 00:00 | 92 | 91 |  | 98 |  |  |  |  | 87 | 97 | 81 | 88 |
| 10-29 06Z | Thu 01:00 | 94 | 93 | 97 | 97 | 80 | 89 | 77 | 93 | 86 | 96 | 78 | 88 |

Wind speed (kt) at the hour:

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 5.5 | 6.2 | 4.8 | 4.6 | 3.5 | 5.6 | 5.0 | 6.0 | 5.0 | 5.9 | 4.8 | 5.9 |
| 10-28 07Z | Wed 02:00 | 4.2 | 4.7 |  | 4.5 |  |  |  |  | 5.0 | 5.6 | 4.5 | 5.4 |
| 10-28 08Z | Wed 03:00 | 3.6 | 2.5 |  | 4.3 |  |  |  |  | 5.0 | 5.3 | 4.3 | 4.8 |
| 10-28 09Z | Wed 04:00 | 2.4 | 2.0 | 4.2 | 3.8 | 3.3 |  | 4.0 | 5.0 | 4.0 | 4.9 | 4.2 | 4.1 |
| 10-28 10Z | Wed 05:00 | 2.4 | 2.5 |  | 4.0 |  |  |  |  | 4.0 | 4.5 | 4.0 | 3.6 |
| 10-28 11Z | Wed 06:00 | 2.9 | 2.9 |  | 3.8 |  |  |  |  | 4.0 | 4.2 | 3.9 | 3.5 |
| 10-28 12Z | Wed 07:00 | 4.5 | 2.8 | 3.1 | 3.1 | 3.4 | 3.6 | 5.0 | 4.0 | 4.0 | 4.1 | 4.1 | 3.7 |
| 10-28 13Z | Wed 08:00 | 3.5 | 5.1 |  | 3.4 |  |  |  |  | 5.0 | 4.4 | 4.6 | 4.4 |
| 10-28 14Z | Wed 09:00 | 6.0 | 6.5 |  | 5.7 |  |  |  |  | 5.0 | 4.9 | 5.5 | 5.6 |
| 10-28 15Z | Wed 10:00 | 6.5 | 6.2 | 5.9 | 5.5 | 5.2 |  | 7.0 | 7.0 | 6.0 | 5.5 | 6.4 | 6.8 |
| 10-28 16Z | Wed 11:00 | 7.5 | 5.8 |  | 5.2 |  |  |  |  | 7.0 | 6.0 | 7.5 | 7.9 |
| 10-28 17Z | Wed 12:00 | 8.8 | 7.8 |  | 6.2 |  |  |  |  | 7.0 | 6.5 | 8.7 | 8.6 |
| 10-28 18Z | Wed 13:00 | 9.5 | 8.1 | 6.4 | 7.2 | 7.8 | 8.3 | 12.0 | 11.0 | 8.0 | 7.0 | 9.7 | 8.7 |
| 10-28 19Z | Wed 14:00 | 8.5 | 9.3 |  | 7.7 |  |  |  |  | 9.0 | 7.5 | 10.5 | 7.9 |
| 10-28 20Z | Wed 15:00 | 7.5 | 9.6 |  | 8.0 |  |  |  |  | 10.0 | 8.0 | 11.3 | 7.0 |
| 10-28 21Z | Wed 16:00 | 9.1 | 9.4 | 6.4 | 7.0 | 10.1 |  | 14.0 | 12.0 | 10.0 | 8.0 | 11.6 | 6.8 |
| 10-28 22Z | Wed 17:00 | 8.2 | 6.9 |  | 3.5 |  |  |  |  | 10.0 | 7.5 | 11.1 | 7.6 |
| 10-28 23Z | Wed 18:00 | 6.4 | 8.3 |  | 4.1 |  |  |  |  | 10.0 | 7.6 | 10.5 | 8.9 |
| 10-29 00Z | Wed 19:00 | 12.0 | 7.4 | 7.2 | 6.1 | 8.5 | 7.5 | 10.0 | 12.0 | 9.0 | 8.1 | 10.0 | 9.8 |
| 10-29 01Z | Wed 20:00 | 11.8 | 9.4 |  | 3.8 |  |  |  |  | 9.0 | 7.7 | 9.2 | 9.8 |
| 10-29 02Z | Wed 21:00 | 11.0 | 8.6 |  | 4.5 |  |  |  |  | 8.0 | 7.0 | 8.8 | 9.2 |
| 10-29 03Z | Wed 22:00 | 11.3 | 8.1 | 6.6 | 6.1 | 6.6 |  | 9.0 | 10.0 | 8.0 | 6.8 | 8.8 | 8.4 |
| 10-29 04Z | Wed 23:00 | 8.2 | 7.8 |  | 6.6 |  |  |  |  | 8.0 | 6.7 | 8.6 | 7.6 |
| 10-29 05Z | Thu 00:00 | 7.8 | 5.8 |  | 6.7 |  |  |  |  | 10.0 | 7.0 | 8.8 | 7.1 |
| 10-29 06Z | Thu 01:00 | 7.8 | 8.2 | 8.0 | 7.4 | 8.5 | 6.5 | 10.0 | 9.0 | 10.0 | 7.4 | 9.4 | 6.9 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 07Z | Wed 02:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 08Z | Wed 03:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 09Z | Wed 04:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 10Z | Wed 05:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 11Z | Wed 06:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 12Z | Wed 07:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-28 13Z | Wed 08:00 | 0.00 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.01 |
| 10-28 14Z | Wed 09:00 | 0.01 | 0.00 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.02 |
| 10-28 15Z | Wed 10:00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 |  | 0.00 | 0.00 | 0.00 | 0.03 |
| 10-28 16Z | Wed 11:00 | 0.01 | 0.01 |  | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.03 |
| 10-28 17Z | Wed 12:00 | 0.01 | 0.01 |  | 0.00 |  |  | 0.00 | 0.01 | 0.00 | 0.04 |
| 10-28 18Z | Wed 13:00 | 0.05 | 0.01 | 0.00 | 0.00 | 0.00 | 0.06 | 0.00 | 0.01 | 0.00 | 0.05 |
| 10-28 19Z | Wed 14:00 | 0.05 | 0.02 |  | 0.00 |  |  | 0.00 | 0.02 | 0.02 | 0.11 |
| 10-28 20Z | Wed 15:00 | 0.05 | 0.03 |  | 0.00 |  |  | 0.00 | 0.03 | 0.04 | 0.16 |
| 10-28 21Z | Wed 16:00 | 0.05 | 0.03 | 0.01 | 0.01 | 0.03 |  | 0.01 | 0.04 | 0.06 | 0.22 |
| 10-28 22Z | Wed 17:00 | 0.05 | 0.04 |  | 0.09 |  |  | 0.03 | 0.12 | 0.11 | 0.27 |
| 10-28 23Z | Wed 18:00 | 0.08 | 0.04 |  | 0.45 |  |  | 0.05 | 0.20 | 0.15 | 0.33 |
| 10-29 00Z | Wed 19:00 | 0.15 | 0.07 | 0.54 | 0.71 | 0.12 | 0.49 | 0.07 | 0.28 | 0.19 | 0.38 |
| 10-29 01Z | Wed 20:00 | 0.15 | 0.44 |  | 0.84 |  |  | 0.10 | 0.32 | 0.21 | 0.39 |
| 10-29 02Z | Wed 21:00 | 0.15 | 0.46 |  | 0.86 |  |  | 0.14 | 0.36 | 0.23 | 0.39 |
| 10-29 03Z | Wed 22:00 | 0.15 | 0.46 | 0.61 | 0.87 | 0.18 |  | 0.18 | 0.40 | 0.25 | 0.40 |
| 10-29 04Z | Wed 23:00 | 0.15 | 0.46 |  | 0.87 |  |  | 0.21 | 0.40 | 0.25 | 0.40 |
| 10-29 05Z | Thu 00:00 | 0.15 | 0.46 |  | 0.87 |  |  | 0.22 | 0.40 | 0.25 | 0.41 |
| 10-29 06Z | Thu 01:00 | 0.15 | 0.46 | 0.61 | 0.87 | 0.18 | 0.53 | 0.22 | 0.40 | 0.25 | 0.41 |

Total cloud cover (%):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 100 | 100 | 3 | 5 | 45 | 39 | 100 | 82 | 63 | 14 | 25 | 56 |
| 10-28 07Z | Wed 02:00 | 100 | 100 |  | 13 |  |  |  | 86 | 66 | 16 | 29 | 55 |
| 10-28 08Z | Wed 03:00 | 100 | 100 |  | 17 |  |  |  | 76 | 70 | 16 | 35 | 54 |
| 10-28 09Z | Wed 04:00 | 100 | 100 | 0 | 12 | 62 |  | 100 | 64 | 75 | 17 | 40 | 54 |
| 10-28 10Z | Wed 05:00 | 100 | 99 |  | 27 |  |  |  | 52 | 77 | 18 | 41 | 54 |
| 10-28 11Z | Wed 06:00 | 100 | 100 |  | 45 |  |  |  | 60 | 78 | 20 | 40 | 55 |
| 10-28 12Z | Wed 07:00 | 100 | 100 | 48 | 44 | 2 | 52 | 100 | 64 | 76 | 22 | 39 | 56 |
| 10-28 13Z | Wed 08:00 | 100 | 100 |  | 36 |  |  |  | 71 | 70 | 28 | 39 | 58 |
| 10-28 14Z | Wed 09:00 | 100 | 84 |  | 28 |  |  |  | 71 | 62 | 36 | 38 | 62 |
| 10-28 15Z | Wed 10:00 | 100 | 94 | 28 | 57 | 40 |  | 100 | 70 | 58 | 43 | 40 | 66 |
| 10-28 16Z | Wed 11:00 | 49 | 70 |  | 21 |  |  |  | 62 | 62 | 48 | 43 | 70 |
| 10-28 17Z | Wed 12:00 | 100 | 46 |  | 49 |  |  |  | 66 | 70 | 52 | 47 | 74 |
| 10-28 18Z | Wed 13:00 | 97 | 38 | 56 | 48 | 75 | 81 | 100 | 75 | 74 | 55 | 52 | 77 |
| 10-28 19Z | Wed 14:00 | 80 | 50 |  | 48 |  |  |  | 64 | 75 | 58 | 58 | 80 |
| 10-28 20Z | Wed 15:00 | 74 | 52 |  | 71 |  |  |  | 67 | 77 | 61 | 66 | 84 |
| 10-28 21Z | Wed 16:00 | 100 | 83 | 100 | 100 | 100 |  | 100 | 65 | 78 | 66 | 72 | 88 |
| 10-28 22Z | Wed 17:00 | 52 | 100 |  | 99 |  |  |  |  | 77 | 76 | 80 | 91 |
| 10-28 23Z | Wed 18:00 | 100 | 95 |  | 100 |  |  |  |  | 73 | 89 | 88 | 91 |
| 10-29 00Z | Wed 19:00 | 86 | 56 | 100 | 100 | 100 | 85 | 100 | 74 | 71 | 95 | 94 | 88 |
| 10-29 01Z | Wed 20:00 | 100 | 89 |  | 100 |  |  |  |  | 77 | 81 | 92 | 79 |
| 10-29 02Z | Wed 21:00 | 100 | 76 |  | 68 |  |  |  |  | 86 | 57 | 87 | 65 |
| 10-29 03Z | Wed 22:00 | 79 | 55 | 23 | 24 | 40 |  | 100 | 85 | 90 | 38 | 80 | 48 |
| 10-29 04Z | Wed 23:00 | 24 | 96 |  | 9 |  |  |  |  | 89 | 28 | 65 | 31 |
| 10-29 05Z | Thu 00:00 | 7 | 80 |  | 0 |  |  |  |  | 86 | 20 | 47 | 16 |
| 10-29 06Z | Thu 01:00 | 26 | 27 | 0 | 0 | 0 | 1 | 19 | 47 | 83 | 13 | 31 | 6 |

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

## Today so far (2026-10-27, through 2026-10-27T21:00Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 55.9 °F, low 44.1 °F, max wind 14 kt, precip 0.14" (15 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 26/18Z | -0.5 | 0.7 | 53 (-3) | 44 (+0) | -1.6 | 0.25 | +0.11 |
| RRFS | 26/18Z | +0.3 | 1.2 | 55 (-1) | 44 (+0) | -1.9 | 0.12 | -0.02 |
| IFS | 26/12Z | +2.5 | 2.6 | 59 (+3) | 44 (+0) | -1.5 | 0.35 | +0.21 |
| IFS_HRES | 26/12Z | +2.5 | 2.5 | 59 (+3) pending | 45 (+1) | -1.9 | 0.46 | +0.32 |
| GFS | 26/18Z | -0.7 | 1.2 | 56 (+0) pending | 43 (-1) | -2.1 | 0.24 | +0.10 |
| AIFS | 26/12Z | -0.3 | 0.8 | 54 (-2) | 42 (-2) | -2.1 | 0.27 | +0.13 |
| GFS_MOS | 26/18Z | -0.7 | 1.7 | 58 (+2) pending | 41 (-3) | -0.4 | — | — |
| NBM | 26/22Z | +2.9 | 2.9 | 62 (+6) pending | 43 (-1) | +1.8 | — | — |
| USL | 26/22Z | +1.4 | 1.5 | 59 (+3) pending | 44 (+0) | -0.5 | 0.22 | +0.08 |
| ENS | 26/00Z | +2.3 | 2.3 | 60 (+5) pending | 45 (+1) | -0.5 | 0.31 | +0.17 |
| AIFS_ENS | 26/12Z | +0.5 | 1.2 | 55 (-1) | 43 (-1) | -1.4 | 0.30 | +0.16 |
| GEFS | 26/18Z | +0.1 | 1.0 | 58 (+2) pending | 44 (+0) | -0.9 | 0.24 | +0.10 |

## Clouds so far today (2026-10-27, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-19 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (CDT) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 100 | 100 | 100 | 76 | 81 | 87 | 100 | 89 | 100 | 90 | 100 | 95 | 100 | 95 |
| 10-27 07Z | Tue 02:00 | 100 | 100 | 100 | 92 |  | 86 |  |  |  | 88 | 100 | 95 | 99 | 94 |
| 10-27 08Z | Tue 03:00 | 100 | 100 | 100 | 97 |  | 100 |  |  |  | 85 | 100 | 96 | 98 | 92 |
| 10-27 09Z | Tue 04:00 | 100 | 100 | 73 | 100 | 98 | 100 | 100 |  | 100 | 86 | 100 | 96 | 98 | 90 |
| 10-27 10Z | Tue 05:00 | 100 | 100 | 100 | 80 |  | 99 |  |  |  | 85 | 100 | 92 | 98 | 89 |
| 10-27 11Z | Tue 06:00 | 100 | 100 | 100 | 71 |  | 50 |  |  |  | 73 | 100 | 87 | 98 | 88 |
| 10-27 12Z | Tue 07:00 | 97 | 100 | 100 | 67 | 98 | 82 | 100 | 85 | 100 | 71 | 100 | 85 | 98 | 87 |
| 10-27 13Z | Tue 08:00 | 100 | 100 | 100 | 76 |  | 84 |  |  |  | 64 | 100 | 88 | 99 | 88 |
| 10-27 14Z | Tue 09:00 | 100 | 100 | 100 | 96 |  | 100 |  |  |  | 74 | 100 | 94 | 99 | 90 |
| 10-27 15Z | Tue 10:00 | 100 | 100 | 100 | 99 | 100 | 95 | 100 |  | 100 | 84 | 100 | 99 | 99 | 92 |
| 10-27 16Z | Tue 11:00 | 100 | 100 | 100 | 100 |  | 99 |  |  |  | 85 | 100 | 98 | 99 | 95 |
| 10-27 17Z | Tue 12:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 85 | 100 | 96 | 99 | 97 |
| 10-27 18Z | Tue 13:00 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 97 | 100 | 83 | 100 | 93 | 99 | 98 |
| 10-27 19Z | Tue 14:00 | 100 | 100 | 100 | 100 |  | 100 |  |  |  | 89 | 100 | 80 | 98 | 96 |
| 10-27 20Z | Tue 15:00 | 100 | 100 | 100 | 100 |  | 98 |  |  |  | 79 | 100 | 62 | 96 | 94 |
| 10-27 21Z | Tue 16:00 | 100 | 100 | 100 | 85 | 100 | 100 | 100 |  | 100 | 85 | 100 | 48 | 94 | 91 |

## Dewpoint so far today (2026-10-27, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (CDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | AIFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-27 06Z | Tue 01:00 | 41.0 | 86 | 42.3 | 39.8 | 43.1 | 43.3 | 39.4 | 40.8 | 38.0 | 42.0 | 41.0 | 43.8 | 37.4 | 41.2 |
| 10-27 07Z | Tue 02:00 | 41.0 | 86 | 42.4 | 40.3 |  | 43.1 |  |  |  |  | 41.0 | 44.0 | 37.3 | 41.5 |
| 10-27 08Z | Tue 03:00 | 42.1 | 90 | 42.5 | 41.1 |  | 43.5 |  |  |  |  | 41.0 | 44.2 | 37.3 | 41.9 |
| 10-27 09Z | Tue 04:00 | 42.1 | 90 | 42.2 | 43.1 | 44.1 | 44.7 | 39.4 |  | 39.0 | 43.0 | 42.0 | 44.3 | 37.4 | 42.3 |
| 10-27 10Z | Tue 05:00 | 42.1 | 93 | 41.9 | 43.3 |  | 45.1 |  |  |  |  | 42.0 | 44.4 | 37.8 | 42.7 |
| 10-27 11Z | Tue 06:00 | 39.9 | 85 | 41.8 | 41.9 |  | 46.1 |  |  |  |  | 42.0 | 44.4 | 38.4 | 43.3 |
| 10-27 12Z | Tue 07:00 | 43.0 | 93 | 42.2 | 41.9 | 45.6 | 46.1 | 40.5 | 43.4 | 41.0 | 44.0 | 43.0 | 44.7 | 39.1 | 44.0 |
| 10-27 13Z | Tue 08:00 | 43.0 | 89 | 43.2 | 42.6 |  | 45.9 |  |  |  |  | 43.0 | 45.3 | 39.9 | 45.1 |
| 10-27 14Z | Tue 09:00 | 43.0 | 86 | 44.3 | 43.7 |  | 47.5 |  |  |  |  | 44.0 | 46.1 | 40.7 | 46.3 |
| 10-27 15Z | Tue 10:00 | 44.1 | 86 | 45.7 | 45.0 | 48.1 | 48.6 | 43.3 |  | 44.0 | 46.0 | 45.0 | 47.2 | 41.8 | 47.6 |
| 10-27 16Z | Tue 11:00 | 46.0 | 83 | 47.5 | 46.8 |  | 51.3 |  |  |  |  | 46.0 | 48.6 | 43.1 | 48.8 |
| 10-27 17Z | Tue 12:00 | 48.0 | 86 | 49.5 | 48.1 |  | 53.8 |  |  |  |  | 48.0 | 50.2 | 44.5 | 49.9 |
| 10-27 18Z | Tue 13:00 | 48.9 | 89 | 51.4 | 49.8 | 54.7 | 55.9 | 48.5 | 49.9 | 46.0 | 50.0 | 49.0 | 51.4 | 45.9 | 50.6 |
| 10-27 19Z | Tue 14:00 | 50.0 | 86 | 50.6 | 51.6 |  | 55.9 |  |  |  |  | 49.0 | 51.7 | 47.4 | 50.9 |
| 10-27 20Z | Tue 15:00 | 52.0 | 90 | 50.4 | 50.1 |  | 55.4 |  |  |  |  | 49.0 | 51.5 | 48.8 | 50.8 |
| 10-27 21Z | Tue 16:00 | 51.1 | 93 | 50.8 | 50.9 | 54.6 | 55.4 | 51.7 |  | 48.0 | 51.0 | 49.0 | 51.3 | 49.9 | 50.6 |
| Bias so far |  |  |  | +0.7 | +0.2 | +3.3 | +4.0 | -1.2 | +0.4 | -2.4 | +1.0 | -0.2 | +2.2 | -3.2 | +1.3 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (MPX): https://forecast.weather.gov/product.php?site=mpx&issuedby=mpx&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
