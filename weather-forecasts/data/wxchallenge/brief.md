# WxChallenge forecast brief: Minneapolis, MN (KMSP)

- Station: **KMSP**
- Target day: **2026-10-29**, scored over 2026-10-29T06Z to 2026-10-30T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-29T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-28T22:12:09+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 28/18Z | 51.3 | 40.1 | 9.4 | 0.00 |
| RRFS | 28/18Z | 52.0 | 42.8 | 9.8 | 0.00 |
| IFS | 28/12Z | 55.1 | 43.3 | 6.8 | 0.00 |
| IFS_HRES | 28/12Z | 55.2 | 43.5 | 6.7 | 0.00 |
| GFS | 28/12Z | 56.7 | 45.1 | 8.7 | 0.00 |
| GFS_MOS | 28/12Z | 57.0 | 46.0 | 11.0 | 0.00 |
| NBM | 28/21Z | 56.0 | 42.0 | 8.0 | 0.01 |
| USL | 28/12Z | 58.0 | 43.0 | 12.0 | 0.00 |
| ENS | 28/06Z | 54.9 | 43.2 | 7.6 | 0.00 |
| GEFS | 28/12Z | 55.8 | 46.5 | 9.2 | 0.00 |
| HRRRCAST (precip only) | 28/12Z | — | — | — | 0.01 |
| REFS (precip only) | 28/18Z | — | — | — | 0.00 |
| NBM_QMD (precip only) | 28/12Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **55.8** | **43.0** | **13.0** | **0.00** |

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

- High °F weights: RRFS 0.16, GFS 0.14, NBM 0.13, GFS_MOS 0.12, USL 0.12, HRRR 0.12, IFS 0.10, ENS 0.10 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Low °F weights: NBM 0.17, IFS 0.16, ENS 0.16, HRRR 0.11, USL 0.11, RRFS 0.10, GFS_MOS 0.09, GFS 0.09 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Wind kt weights: GFS_MOS 0.16, NBM 0.16, HRRR 0.13, RRFS 0.12, USL 0.12, GFS 0.11, IFS 0.10, ENS 0.10 (no track record yet: USL) (using parent's track record: ENS from IFS)
- Precip in weights: GFS_MOS 0.14, NBM 0.13, RRFS 0.13, GFS 0.12, USL 0.12, HRRR 0.12, IFS 0.12, ENS 0.12 (no track record yet: USL) (using parent's track record: ENS from IFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 53.7 | 54.2 | 54.9 | 55.5 | 55.9 | 54.9 |
| ENS | 51 | Low °F | 41.9 | 42.7 | 43.1 | 43.9 | 44.6 | 43.2 |
| ENS | 51 | Wind kt | 6.5 | 6.8 | 7.3 | 8.4 | 9.1 | 7.6 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| GEFS | 31 | High °F | 54.0 | 54.6 | 55.5 | 56.8 | 57.7 | 55.8 |
| GEFS | 31 | Low °F | 45.1 | 45.9 | 46.9 | 47.2 | 47.6 | 46.5 |
| GEFS | 31 | Wind kt | 8.1 | 8.7 | 9.4 | 9.8 | 10.1 | 9.2 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.01 | 0.01 | 0.02 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 0% | 0% | 0% | 0% |
| GEFS | 0% | 0% | 0% | 0% |
| HRRRCAST | 28% | 0% | 0% | 0% |
| REFS | 0% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.00", p90 0.00"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 1% | 0% | 3% | 1% | 3% to 5% | 0.07 (4) |
| NBM | NBS P06 | 0% | 0% | 2% | 2% | 2% to 4% | 0.07 (4) |
| ENS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.24 (4) |
| GEFS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.21 (4) |
| HRRRCAST | member fraction | — | — | — | — | 28% | — |
| REFS | member fraction | — | — | — | — | 0% | — |
| NBM_QMD | NBM QMD | 0% | 0% | 0% | 0% | 0% | 0.08 (4) |

For reference, always forecasting the period's observed frequency (25% of 6-h blocks wet) scores Brier 0.19.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, IFS_HRES, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly; ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Dewpoint and relative humidity (context, not scored): the models' 2 m dewpoint (GFS_MOS, NBM and USL from their own guidance; ENS and GEFS the mean of their members). Moist air (a high dewpoint) slows the overnight cooling, and the low rarely falls far below the evening dewpoint on a calm night; RH near 100% means fog or low cloud is possible.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles the mean of their members. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-29 06Z | Thu 01:00 | 51.3 | 51.8 | 49.8 | 50.5 | 52.7 | 56.0 | 52.0 | 54.0 | 50.5 | 54.0 |
| 10-29 07Z | Thu 02:00 | 49.3 | 49.7 |  | 48.7 |  |  |  | 52.0 | 49.0 | 52.7 |
| 10-29 08Z | Thu 03:00 | 48.0 | 48.3 |  | 47.7 |  |  |  | 51.0 | 47.7 | 51.4 |
| 10-29 09Z | Thu 04:00 | 46.8 | 47.9 | 46.8 | 46.9 | 49.7 | 51.0 | 46.0 | 49.0 | 46.5 | 50.2 |
| 10-29 10Z | Thu 05:00 | 45.5 | 46.6 |  | 46.3 |  |  |  | 48.0 | 45.2 | 48.9 |
| 10-29 11Z | Thu 06:00 | 44.4 | 45.5 |  | 45.2 |  |  |  | 46.0 | 43.9 | 47.6 |
| 10-29 12Z | Thu 07:00 | 43.0 | 44.1 | 43.8 | 44.2 | 45.9 | 47.0 | 42.0 | 45.0 | 43.3 | 46.8 |
| 10-29 13Z | Thu 08:00 | 41.8 | 42.8 |  | 43.5 |  |  |  | 44.0 | 43.7 | 46.6 |
| 10-29 14Z | Thu 09:00 | 43.4 | 44.1 |  | 45.2 |  |  |  | 45.0 | 44.8 | 46.9 |
| 10-29 15Z | Thu 10:00 | 45.2 | 45.3 | 46.3 | 47.0 | 47.2 | 48.0 | 46.0 | 48.0 | 46.2 | 47.6 |
| 10-29 16Z | Thu 11:00 | 46.5 | 46.8 |  | 48.6 |  |  |  | 51.0 | 48.1 | 49.1 |
| 10-29 17Z | Thu 12:00 | 47.6 | 48.1 |  | 50.4 |  |  |  | 53.0 | 50.3 | 51.1 |
| 10-29 18Z | Thu 13:00 | 49.0 | 49.6 | 52.0 | 52.3 | 53.6 | 53.0 | 50.0 | 55.0 | 52.1 | 52.8 |
| 10-29 19Z | Thu 14:00 | 50.0 | 50.8 |  | 53.8 |  |  |  | 56.0 | 53.6 | 54.1 |
| 10-29 20Z | Thu 15:00 | 51.1 | 51.6 |  | 54.9 |  |  |  | 57.0 | 54.7 | 55.2 |
| 10-29 21Z | Thu 16:00 | 51.3 | 52.0 | 54.8 | 55.2 | 56.6 | 56.0 | 52.0 | 57.0 | 54.8 | 55.5 |
| 10-29 22Z | Thu 17:00 | 50.6 | 51.5 |  | 54.6 |  |  |  | 56.0 | 53.5 | 54.8 |
| 10-29 23Z | Thu 18:00 | 47.9 | 49.2 |  | 51.4 |  |  |  | 54.0 | 51.2 | 53.3 |
| 10-30 00Z | Thu 19:00 | 45.9 | 47.1 | 49.7 | 49.6 | 52.3 | 52.0 | 50.0 | 51.0 | 49.2 | 52.0 |
| 10-30 01Z | Thu 20:00 | 44.5 | 46.3 |  | 48.6 |  |  |  | 50.0 | 48.1 | 51.2 |
| 10-30 02Z | Thu 21:00 | 43.5 | 45.1 |  | 48.8 |  |  |  | 47.0 | 47.3 | 50.5 |
| 10-30 03Z | Thu 22:00 | 42.6 | 45.2 | 47.4 | 48.7 | 49.7 | 48.0 | 45.0 | 46.0 | 46.6 | 49.8 |
| 10-30 04Z | Thu 23:00 | 41.6 | 44.3 |  | 46.9 |  |  |  | 45.0 | 46.1 | 49.1 |
| 10-30 05Z | Fri 00:00 | 40.8 | 44.4 |  | 47.6 |  |  |  | 44.0 | 45.8 | 48.5 |
| 10-30 06Z | Fri 01:00 | 40.1 | 45.0 | 46.6 | 47.2 | 48.2 | 46.0 | 43.0 | 44.0 | 45.4 | 47.9 |

Dewpoint (°F):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-29 06Z | Thu 01:00 | 49.5 | 47.8 | 46.7 | 47.7 | 44.3 | 50.0 | 48.0 | 49.0 | 48.4 | 41.0 |
| 10-29 07Z | Thu 02:00 | 47.1 | 47.3 |  | 45.4 |  |  |  | 47.0 | 46.4 | 39.2 |
| 10-29 08Z | Thu 03:00 | 45.7 | 46.5 |  | 44.2 |  |  |  | 45.0 | 44.7 | 38.3 |
| 10-29 09Z | Thu 04:00 | 45.2 | 44.9 | 42.9 | 43.5 | 39.3 | 46.0 | 42.0 | 44.0 | 43.2 | 37.4 |
| 10-29 10Z | Thu 05:00 | 44.2 | 44.7 |  | 43.1 |  |  |  | 43.0 | 42.1 | 36.6 |
| 10-29 11Z | Thu 06:00 | 42.6 | 42.9 |  | 42.6 |  |  |  | 42.0 | 41.1 | 35.8 |
| 10-29 12Z | Thu 07:00 | 41.0 | 40.6 | 41.1 | 41.7 | 36.7 | 41.0 | 40.0 | 41.0 | 40.4 | 35.1 |
| 10-29 13Z | Thu 08:00 | 39.8 | 39.5 |  | 40.7 |  |  |  | 40.0 | 39.7 | 34.5 |
| 10-29 14Z | Thu 09:00 | 39.1 | 38.0 |  | 40.4 |  |  |  | 39.0 | 39.1 | 34.0 |
| 10-29 15Z | Thu 10:00 | 38.9 | 37.5 | 38.2 | 38.9 | 34.1 | 38.0 | 38.0 | 39.0 | 38.7 | 33.8 |
| 10-29 16Z | Thu 11:00 | 38.8 | 37.6 |  | 37.9 |  |  |  | 39.0 | 38.6 | 33.7 |
| 10-29 17Z | Thu 12:00 | 39.8 | 38.3 |  | 38.5 |  |  |  | 38.0 | 38.7 | 33.8 |
| 10-29 18Z | Thu 13:00 | 40.6 | 39.2 | 38.5 | 38.7 | 32.2 | 36.0 | 38.0 | 38.0 | 38.8 | 33.7 |
| 10-29 19Z | Thu 14:00 | 40.7 | 39.7 |  | 39.2 |  |  |  | 37.0 | 39.0 | 33.7 |
| 10-29 20Z | Thu 15:00 | 40.9 | 40.4 |  | 39.9 |  |  |  | 37.0 | 39.5 | 33.7 |
| 10-29 21Z | Thu 16:00 | 41.2 | 41.0 | 40.2 | 40.3 | 31.4 | 34.0 | 38.0 | 38.0 | 40.0 | 33.7 |
| 10-29 22Z | Thu 17:00 | 41.7 | 41.5 |  | 41.2 |  |  |  | 38.0 | 40.8 | 33.8 |
| 10-29 23Z | Thu 18:00 | 43.5 | 42.5 |  | 42.5 |  |  |  | 39.0 | 41.4 | 33.9 |
| 10-30 00Z | Thu 19:00 | 43.3 | 43.1 | 41.5 | 42.1 | 32.1 | 34.0 | 37.0 | 40.0 | 41.6 | 33.8 |
| 10-30 01Z | Thu 20:00 | 42.7 | 43.4 |  | 41.9 |  |  |  | 40.0 | 41.5 | 33.7 |
| 10-30 02Z | Thu 21:00 | 42.4 | 43.3 |  | 42.5 |  |  |  | 40.0 | 41.3 | 33.5 |
| 10-30 03Z | Thu 22:00 | 41.6 | 43.3 | 41.4 | 42.7 | 31.7 | 35.0 | 38.0 | 40.0 | 41.2 | 33.3 |
| 10-30 04Z | Thu 23:00 | 40.8 | 43.1 |  | 42.2 |  |  |  | 40.0 | 41.2 | 33.0 |
| 10-30 05Z | Fri 00:00 | 40.0 | 43.4 |  | 42.4 |  |  |  | 39.0 | 41.3 | 32.8 |
| 10-30 06Z | Fri 01:00 | 39.6 | 43.6 | 41.5 | 42.4 | 31.1 | 34.0 | 37.0 | 39.0 | 41.3 | 32.6 |

Relative humidity (%), from each model's temperature and dewpoint (ensembles: the mean of their members' RH):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-29 06Z | Thu 01:00 | 94 | 86 | 89 | 90 | 73 | 80 | 86 | 83 | 92 | 62 |
| 10-29 07Z | Thu 02:00 | 92 | 91 |  | 88 |  |  |  | 83 | 91 | 60 |
| 10-29 08Z | Thu 03:00 | 92 | 93 |  | 88 |  |  |  | 80 | 89 | 61 |
| 10-29 09Z | Thu 04:00 | 94 | 89 | 86 | 88 | 67 | 83 | 86 | 83 | 88 | 62 |
| 10-29 10Z | Thu 05:00 | 95 | 93 |  | 89 |  |  |  | 83 | 89 | 62 |
| 10-29 11Z | Thu 06:00 | 93 | 91 |  | 91 |  |  |  | 86 | 90 | 63 |
| 10-29 12Z | Thu 07:00 | 93 | 87 | 90 | 91 | 70 | 80 | 93 | 86 | 89 | 64 |
| 10-29 13Z | Thu 08:00 | 93 | 88 |  | 90 |  |  |  | 86 | 86 | 62 |
| 10-29 14Z | Thu 09:00 | 85 | 79 |  | 83 |  |  |  | 79 | 80 | 61 |
| 10-29 15Z | Thu 10:00 | 78 | 74 | 73 | 73 | 60 | 68 | 73 | 71 | 75 | 58 |
| 10-29 16Z | Thu 11:00 | 74 | 70 |  | 66 |  |  |  | 63 | 70 | 55 |
| 10-29 17Z | Thu 12:00 | 74 | 69 |  | 64 |  |  |  | 57 | 64 | 51 |
| 10-29 18Z | Thu 13:00 | 73 | 67 | 60 | 60 | 44 | 52 | 63 | 53 | 60 | 48 |
| 10-29 19Z | Thu 14:00 | 70 | 66 |  | 58 |  |  |  | 49 | 58 | 46 |
| 10-29 20Z | Thu 15:00 | 68 | 65 |  | 57 |  |  |  | 47 | 56 | 44 |
| 10-29 21Z | Thu 16:00 | 68 | 66 | 58 | 57 | 38 | 43 | 59 | 49 | 57 | 44 |
| 10-29 22Z | Thu 17:00 | 71 | 69 |  | 60 |  |  |  | 51 | 62 | 45 |
| 10-29 23Z | Thu 18:00 | 85 | 78 |  | 72 |  |  |  | 57 | 69 | 47 |
| 10-30 00Z | Thu 19:00 | 91 | 86 | 73 | 75 | 46 | 50 | 61 | 66 | 75 | 50 |
| 10-30 01Z | Thu 20:00 | 93 | 90 |  | 78 |  |  |  | 68 | 78 | 51 |
| 10-30 02Z | Thu 21:00 | 96 | 93 |  | 79 |  |  |  | 77 | 80 | 52 |
| 10-30 03Z | Thu 22:00 | 96 | 93 | 80 | 80 | 50 | 61 | 76 | 79 | 82 | 53 |
| 10-30 04Z | Thu 23:00 | 97 | 96 |  | 84 |  |  |  | 83 | 83 | 54 |
| 10-30 05Z | Fri 00:00 | 97 | 96 |  | 82 |  |  |  | 82 | 84 | 55 |
| 10-30 06Z | Fri 01:00 | 98 | 95 | 82 | 83 | 51 | 63 | 79 | 82 | 86 | 55 |

Wind speed (kt) at the hour:

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-29 06Z | Thu 01:00 | 5.5 | 6.2 | 6.7 | 6.7 | 6.9 | 9.0 | 8.0 | 8.0 | 7.5 | 8.2 |
| 10-29 07Z | Thu 02:00 | 4.2 | 3.4 |  | 5.5 |  |  |  | 7.0 | 7.2 | 8.1 |
| 10-29 08Z | Thu 03:00 | 5.2 | 3.5 |  | 5.8 |  |  |  | 7.0 | 6.7 | 8.0 |
| 10-29 09Z | Thu 04:00 | 5.2 | 6.1 | 4.8 | 5.0 | 7.0 | 7.0 | 7.0 | 6.0 | 6.2 | 7.9 |
| 10-29 10Z | Thu 05:00 | 3.8 | 4.7 |  | 5.7 |  |  |  | 6.0 | 5.8 | 7.6 |
| 10-29 11Z | Thu 06:00 | 4.9 | 6.1 |  | 5.4 |  |  |  | 6.0 | 5.4 | 7.3 |
| 10-29 12Z | Thu 07:00 | 4.9 | 6.8 | 5.3 | 5.3 | 6.6 | 6.0 | 6.0 | 6.0 | 5.3 | 7.2 |
| 10-29 13Z | Thu 08:00 | 4.3 | 7.0 |  | 5.6 |  |  |  | 6.0 | 5.6 | 7.7 |
| 10-29 14Z | Thu 09:00 | 6.1 | 8.7 |  | 5.4 |  |  |  | 7.0 | 5.9 | 8.5 |
| 10-29 15Z | Thu 10:00 | 8.2 | 9.8 | 6.8 | 6.4 | 8.7 | 10.0 | 8.0 | 7.0 | 6.2 | 8.9 |
| 10-29 16Z | Thu 11:00 | 9.4 | 9.4 |  | 6.4 |  |  |  | 8.0 | 6.1 | 8.7 |
| 10-29 17Z | Thu 12:00 | 9.4 | 8.5 |  | 5.7 |  |  |  | 8.0 | 5.9 | 8.2 |
| 10-29 18Z | Thu 13:00 | 8.8 | 7.8 | 5.4 | 5.5 | 7.8 | 11.0 | 8.0 | 8.0 | 5.6 | 7.7 |
| 10-29 19Z | Thu 14:00 | 8.0 | 7.1 |  | 5.3 |  |  |  | 8.0 | 5.4 | 7.3 |
| 10-29 20Z | Thu 15:00 | 7.1 | 6.4 |  | 4.6 |  |  |  | 8.0 | 5.0 | 7.0 |
| 10-29 21Z | Thu 16:00 | 5.7 | 5.2 | 5.0 | 4.7 | 7.5 | 9.0 | 7.0 | 7.0 | 4.6 | 6.5 |
| 10-29 22Z | Thu 17:00 | 4.5 | 5.2 |  | 3.7 |  |  |  | 7.0 | 3.8 | 5.6 |
| 10-29 23Z | Thu 18:00 | 4.0 | 3.1 |  | 2.2 |  |  |  | 5.0 | 2.9 | 4.7 |
| 10-30 00Z | Thu 19:00 | 4.1 | 3.6 | 2.6 | 2.5 | 3.9 | 6.0 | 2.0 | 4.0 | 2.2 | 3.9 |
| 10-30 01Z | Thu 20:00 | 3.8 | 2.3 |  | 2.2 |  |  |  | 4.0 | 1.8 | 3.4 |
| 10-30 02Z | Thu 21:00 | 3.7 | 2.0 |  | 1.8 |  |  |  | 3.0 | 1.6 | 3.1 |
| 10-30 03Z | Thu 22:00 | 3.6 | 1.0 | 1.2 | 1.0 | 2.7 | 5.0 | 0.0 | 3.0 | 1.7 | 2.8 |
| 10-30 04Z | Thu 23:00 | 3.8 | 1.2 |  | 2.5 |  |  |  | 3.0 | 1.6 | 2.6 |
| 10-30 05Z | Fri 00:00 | 2.4 | 1.8 |  | 1.9 |  |  |  | 2.0 | 1.6 | 2.3 |
| 10-30 06Z | Fri 01:00 | 2.1 | 1.6 | 1.3 | 1.2 | 1.9 | 3.0 | 0.0 | 3.0 | 1.6 | 2.3 |

Precipitation (in), accumulated since the start of the day (06Z): 0.00 in every model (HRRR, RRFS, IFS, IFS_HRES, GFS, USL, ENS, GEFS) all day.

Total cloud cover (%):

| UTC | Local (CDT) | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-29 06Z | Thu 01:00 | 3 | 0 | 0 | 0 | 0 | 0 | 14 | 24 | 0 | 8 |
| 10-29 07Z | Thu 02:00 | 0 | 0 |  | 0 |  |  | 12 | 22 | 0 | 3 |
| 10-29 08Z | Thu 03:00 | 0 | 0 |  | 0 |  |  | 11 | 26 | 0 | 1 |
| 10-29 09Z | Thu 04:00 | 2 | 0 | 0 | 0 | 0 | 0 | 12 | 28 | 0 | 0 |
| 10-29 10Z | Thu 05:00 | 1 | 0 |  | 0 |  |  | 11 | 32 | 0 | 0 |
| 10-29 11Z | Thu 06:00 | 1 | 0 |  | 0 |  |  | 7 | 40 | 0 | 0 |
| 10-29 12Z | Thu 07:00 | 2 | 0 | 0 | 0 | 3 | 0 | 1 | 45 | 0 | 0 |
| 10-29 13Z | Thu 08:00 | 1 | 0 |  | 0 |  |  | 1 | 43 | 1 | 0 |
| 10-29 14Z | Thu 09:00 | 0 | 0 |  | 0 |  |  | 1 | 37 | 1 | 0 |
| 10-29 15Z | Thu 10:00 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 30 | 1 | 0 |
| 10-29 16Z | Thu 11:00 | 12 | 6 |  | 0 |  |  | 0 | 20 | 1 | 0 |
| 10-29 17Z | Thu 12:00 | 13 | 5 |  | 0 |  |  | 3 | 9 | 1 | 1 |
| 10-29 18Z | Thu 13:00 | 16 | 4 | 0 | 0 | 0 | 19 | 3 | 1 | 1 | 1 |
| 10-29 19Z | Thu 14:00 | 14 | 3 |  | 0 |  |  | 1 | 0 | 1 | 1 |
| 10-29 20Z | Thu 15:00 | 10 | 0 |  | 0 |  |  | 1 | 0 | 1 | 1 |
| 10-29 21Z | Thu 16:00 | 5 | 1 | 0 | 1 | 4 | 0 | 4 | 0 | 2 | 0 |
| 10-29 22Z | Thu 17:00 | 7 | 0 |  | 1 |  |  | 2 | 5 | 4 | 3 |
| 10-29 23Z | Thu 18:00 | 1 | 1 |  | 17 |  |  |  | 13 | 7 | 6 |
| 10-30 00Z | Thu 19:00 | 2 | 9 | 22 | 9 | 7 | 0 | 7 | 19 | 12 | 10 |
| 10-30 01Z | Thu 20:00 | 2 | 39 |  | 73 |  |  |  | 20 | 25 | 14 |
| 10-30 02Z | Thu 21:00 | 17 | 69 |  | 91 |  |  |  | 18 | 41 | 19 |
| 10-30 03Z | Thu 22:00 | 7 | 35 | 70 | 52 | 63 | 0 | 14 | 19 | 55 | 22 |
| 10-30 04Z | Thu 23:00 | 6 | 41 |  | 100 |  |  |  | 35 | 64 | 25 |
| 10-30 05Z | Fri 00:00 | 5 | 78 |  | 98 |  |  |  | 59 | 70 | 26 |
| 10-30 06Z | Fri 01:00 | 24 | 79 | 98 | 98 | 86 | 0 | 46 | 73 | 72 | 27 |

## Track record this period

Since 2026-10-12 at KMSP (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-27 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| USL | 1 | 4.9 | -2.0 | +0.0 | +1.0 | +0.08 | 2.0 | 0.0 | 1.0 | 0.08 |
| CONSENSUS | 16 | 5.8 | -0.9 | +0.1 | -1.9 | +0.02 | 1.9 | 1.0 | 2.5 | 0.06 |
| NBM | 16 | 7.4 | -0.6 | +0.2 | -3.9 | +0.00 | 2.3 | 1.3 | 4.0 | 0.05 |
| GFS_MOS | 16 | 8.0 | -0.9 | +0.3 | -3.7 | +0.00 | 2.4 | 3.0 | 4.0 | 0.03 |
| ENS | 1 | 8.2 | +0.0 | +1.0 | -5.0 | +0.18 | 0.0 | 1.0 | 5.0 | 0.18 |
| GEFS | 1 | 8.5 | -3.0 | +0.0 | -5.0 | +0.10 | 3.0 | 0.0 | 5.0 | 0.10 |
| RRFS | 16 | 8.6 | -0.6 | -1.5 | -5.3 | +0.01 | 1.8 | 2.7 | 5.3 | 0.06 |
| HRRR | 16 | 8.9 | -2.1 | -2.1 | -5.0 | +0.03 | 2.4 | 2.3 | 5.0 | 0.08 |
| GFS | 16 | 10.0 | -0.7 | +2.9 | -6.0 | +0.03 | 2.2 | 3.1 | 6.0 | 0.07 |
| IFS | 16 | 10.5 | -1.3 | +0.4 | -6.5 | +0.04 | 3.1 | 1.5 | 6.5 | 0.09 |
| IFS_HRES | 16 | 10.6 | -1.0 | +0.9 | -6.3 | +0.03 | 3.3 | 1.9 | 6.3 | 0.08 |

## Daily verification (all 16 days this period)

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

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 16 | +13 | 15 | +9 | 10 |
| RRFS | 16 | +3 | 9 | +9 | 13 |
| IFS | 16 | +1 | 10 | -2 | 7 |
| IFS_HRES | 16 | +0 | 12 | -1 | 7 |
| GFS | 16 | +7 | 15 | +2 | 12 |
| GFS_MOS | 16 | -2 | 3 | +2 | 12 |
| NBM | 16 | -3 | 12 | -6 | 11 |
| USL | 1 | +0 | 0 | -1 | 1 |
| ENS | 1 | -8 | 8 | -25 | 25 |
| GEFS | 1 | -2 | 2 | -4 | 4 |

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

## Dewpoint (context only, not scored)

Each scored run's 2 m dewpoint vs the observed dewpoint, in °F (forecast - observed: positive = too moist, negative = too dry), averaged over the same night (06Z to sunrise, drives the low) and day (sun up, drives the high) hours as the cloud section. Observed = the METAR nearest each hour; models are interpolated to every hour. A model that runs too moist at night tends to hold its low too warm, too dry to drop it too far. — = no data (the ensembles and USL only from when their dewpoints were kept). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 16 | +0.1 | 1.6 | +1.3 | 1.8 |
| RRFS | 16 | +0.2 | 1.5 | +0.9 | 1.2 |
| IFS | 16 | +1.7 | 2.2 | +2.1 | 2.6 |
| IFS_HRES | 16 | +1.8 | 2.2 | +2.2 | 3.0 |
| GFS | 16 | -1.4 | 2.6 | -2.4 | 2.5 |
| GFS_MOS | 16 | +0.0 | 2.1 | +0.1 | 2.1 |
| NBM | 16 | +0.7 | 1.4 | +0.1 | 1.2 |
| USL | 1 | +0.1 | 0.1 | -0.8 | 0.8 |
| ENS | 1 | +2.7 | 2.7 | +1.5 | 1.5 |
| GEFS | 1 | -3.8 | 3.8 | -2.3 | 2.3 |

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

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| 10-27 | 0.14" (wet: 06-12) | 73/46/3/1 | 87/52/5/5 | 100/94/24/14 | 97/90/6/6 | 24h 100% | 24h 100% | 83/52/3/4 |

## Today so far (2026-10-28, through 2026-10-28T21:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 70.0 °F, low 53.1 °F, max wind 13 kt, precip 0.01" (16 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 27/18Z | -3.9 | 3.9 | 66 (-4) | 50 (-3) pending | -0.8 | 0.05 | +0.04 |
| RRFS | 27/18Z | -3.6 | 3.6 | 67 (-3) | 50 (-3) | -1.0 | 0.04 | +0.03 |
| IFS | 27/12Z | -3.3 | 3.3 | 68 (-2) | 48 (-5) | -1.6 | 0.16 | +0.15 |
| IFS_HRES | 27/12Z | -2.4 | 2.6 | 68 (-2) | 50 (-4) | -1.6 | 0.08 | +0.07 |
| GFS | 27/18Z | -3.0 | 3.0 | 69 (-1) | 51 (-2) | -0.9 | 0.07 | +0.06 |
| GFS_MOS | 27/18Z | -1.0 | 1.1 | 68 (-2) | 52 (-1) | +0.9 | — | — |
| NBM | 27/22Z | -1.9 | 1.9 | 70 (+0) pending | 51 (-2) | +0.9 | — | — |
| USL | 27/22Z | -1.7 | 1.7 | 70 (+0) pending | 51 (-2) | +0.4 | 0.01 | +0.00 |
| ENS | 27/06Z | -2.8 | 2.8 | 67 (-3) | 49 (-4) | -0.9 | 0.11 | +0.10 |
| GEFS | 27/18Z | -1.8 | 1.8 | 67 (-3) | 52 (-1) | +0.0 | 0.14 | +0.13 |

## Clouds so far today (2026-10-28, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-19 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (CDT) | GOES | METAR | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 06Z | Wed 01:00 | 100 |  | 100 | 100 | 3 | 5 | 1 | 100 | 81 | 54 | 14 | 10 |
| 10-28 07Z | Wed 02:00 | 100 | 100 | 100 | 100 |  | 13 |  |  | 88 | 56 | 16 | 18 |
| 10-28 08Z | Wed 03:00 | 100 | 100 | 100 | 100 |  | 17 |  |  | 81 | 58 | 16 | 30 |
| 10-28 09Z | Wed 04:00 | 100 | 100 | 100 | 100 | 0 | 12 | 60 | 100 | 73 | 61 | 17 | 39 |
| 10-28 10Z | Wed 05:00 | 100 | 100 | 100 | 99 |  | 27 |  |  | 63 | 65 | 18 | 42 |
| 10-28 11Z | Wed 06:00 | 100 | 100 | 100 | 100 |  | 45 |  |  | 67 | 69 | 20 | 44 |
| 10-28 12Z | Wed 07:00 | 100 | 100 | 100 | 100 | 48 | 44 | 14 | 100 | 70 | 73 | 22 | 44 |
| 10-28 13Z | Wed 08:00 | 76 | 100 | 100 | 100 |  | 36 |  |  | 77 | 77 | 28 | 43 |
| 10-28 14Z | Wed 09:00 | 93 | 75 | 100 | 84 |  | 28 |  |  | 76 | 79 | 36 | 41 |
| 10-28 15Z | Wed 10:00 | 81 | 75 | 100 | 94 | 28 | 57 | 46 | 100 | 73 | 81 | 43 | 42 |
| 10-28 16Z | Wed 11:00 | 49 | 44 | 49 | 70 |  | 21 |  |  | 62 | 75 | 48 | 47 |
| 10-28 17Z | Wed 12:00 | 80 | 75 | 100 | 46 |  | 49 |  |  | 70 | 62 | 52 | 54 |
| 10-28 18Z | Wed 13:00 | 77 | 75 | 97 | 38 | 56 | 48 | 86 | 100 | 59 | 51 | 55 | 60 |
| 10-28 19Z | Wed 14:00 | 26 | 75 | 80 | 50 |  | 48 |  |  | 62 | 41 | 58 | 65 |
| 10-28 20Z | Wed 15:00 | 100 | 75 | 74 | 52 |  | 71 |  |  | 76 | 31 | 61 | 70 |
| 10-28 21Z | Wed 16:00 | 98 | 75 | 100 | 83 | 100 | 100 | 100 | 100 | 66 | 31 | 66 | 75 |
| 10-28 22Z | Wed 17:00 | 94 | 75 | 52 | 100 |  | 99 |  |  | 74 | 49 | 76 | 83 |

## Dewpoint so far today (2026-10-28, observed vs forecast)

Observed dewpoint (°F) and RH (%) from the METAR nearest each hour, against the dewpoint of the runs submitted for today. Bias so far = forecast - observed over the hours both have (positive = too moist). A model running too moist often runs its low too warm, too dry its low too cold. Context only, not scored.

| UTC | Local (CDT) | Obs Td | Obs RH | HRRR | RRFS | IFS | IFS_HRES | GFS | GFS_MOS | NBM | USL | ENS | GEFS | AIFS | AIFS_ENS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-28 07Z | Wed 02:00 | 48.9 | 86 | 49.8 | 47.5 |  | 50.0 |  |  |  | 50.0 | 49.9 | 48.2 |  | 47.7 |
| 10-28 08Z | Wed 03:00 | 50.0 | 89 | 50.1 | 48.1 |  | 49.8 |  |  |  | 50.0 | 49.8 | 48.7 |  | 47.3 |
| 10-28 09Z | Wed 04:00 | 51.1 | 90 | 50.2 | 48.3 | 48.4 | 48.9 | 49.2 | 50.0 | 51.0 | 50.0 | 49.6 | 49.2 |  | 47.1 |
| 10-28 10Z | Wed 05:00 | 51.1 | 93 | 50.3 | 48.8 |  | 48.8 |  |  |  | 50.0 | 49.2 | 49.6 |  | 47.0 |
| 10-28 11Z | Wed 06:00 | 52.0 | 93 | 50.3 | 49.5 |  | 49.3 |  |  |  | 50.0 | 48.8 | 50.1 |  | 47.2 |
| 10-28 12Z | Wed 07:00 | 53.1 | 97 | 50.6 | 49.7 | 47.5 | 49.0 | 50.2 | 51.0 | 51.0 | 50.0 | 49.0 | 50.7 | 47.8 | 47.7 |
| 10-28 13Z | Wed 08:00 | 54.0 | 93 | 51.0 | 50.0 |  | 49.8 |  |  |  | 51.0 | 50.5 | 51.3 |  | 48.8 |
| 10-28 14Z | Wed 09:00 | 54.0 | 90 | 51.7 | 50.6 |  | 52.7 |  |  |  | 52.0 | 52.7 | 51.9 |  | 50.3 |
| 10-28 15Z | Wed 10:00 | 54.0 | 87 | 53.3 | 51.8 | 55.7 | 56.3 | 53.4 | 53.0 | 54.0 | 53.0 | 54.7 | 52.3 |  | 51.9 |
| 10-28 16Z | Wed 11:00 | 54.0 | 78 | 54.7 | 53.2 |  | 57.4 |  |  |  | 54.0 | 56.0 | 52.4 |  | 53.4 |
| 10-28 17Z | Wed 12:00 | 54.0 | 72 | 55.6 | 55.6 |  | 57.2 |  |  |  | 55.0 | 56.8 | 52.0 |  | 54.8 |
| 10-28 18Z | Wed 13:00 | 54.0 | 65 | 56.3 | 56.5 | 57.3 | 56.7 | 52.8 | 55.0 | 56.0 | 56.0 | 57.3 | 51.9 | 56.1 | 55.9 |
| 10-28 19Z | Wed 14:00 | 55.9 | 65 | 58.0 | 57.5 |  | 56.2 |  |  |  | 57.0 | 57.9 | 52.7 |  | 56.9 |
| 10-28 20Z | Wed 15:00 | 57.0 | 63 | 59.8 | 59.0 |  | 57.4 |  |  |  | 57.0 | 58.4 | 54.0 |  | 58.0 |
| 10-28 21Z | Wed 16:00 | 57.9 | 65 | 61.4 | 60.1 | 58.0 | 59.0 | 55.8 | 56.0 | 57.0 | 58.0 | 58.8 | 55.4 |  | 58.9 |
| 10-28 22Z | Wed 17:00 | 61.0 | 75 | 61.6 | 61.0 |  | 60.5 |  |  |  | 58.0 | 59.2 | 56.6 |  | 59.6 |
| Bias so far |  |  |  | +0.2 | -0.9 | -0.6 | -0.2 | -1.7 | -1.0 | -0.2 | -0.7 | -0.2 | -2.2 | -1.6 | -1.8 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (MPX): https://forecast.weather.gov/product.php?site=mpx&issuedby=mpx&product=afd&format=ci&version=1&glossary=1
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
