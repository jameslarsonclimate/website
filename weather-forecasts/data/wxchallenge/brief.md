# WxChallenge forecast brief: Olympia, WA (KOLM)

- Station: **KOLM**
- Target day: **2026-10-13**, scored over 2026-10-13T06Z to 2026-10-14T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-13T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-12T20:00:09+00:00 (refreshed several times an hour while the forecast job runs)
- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)

## How to use this brief (for AI assistants)

1. Start from the **CONSENSUS** row. It is already bias-corrected and skill-weighted using this period's verification (method below).
2. Check the track-record table: a model with a large, consistent bias (|bias| close to its MAE) is reliably off in that direction. The consensus already removes most of that bias; lean further only if the last few days (daily verification tables) show the bias growing.
3. Use the ensemble percentiles for uncertainty. For **precip**, enter roughly the ensemble **median**, not the mean: points are charged per 0.01" of error, and charged most heavily near zero, so the median minimizes expected points. Check the chance-of-rain table: when the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.
4. Use "Today so far" (the day currently in progress, not the target day) to see which models are handling the current pattern; persistent errors there often carry into tomorrow.
5. Read the latest AFD for the forecaster's view of the pattern; it often explains when a model bias learned earlier in the period won't apply.
6. Give whole °F for high/low, whole kt for wind, and precip to 0.01". State the reasoning for any departure from the consensus.

## Scoring (error points; lower is better)

- High and low temperature: 1 point per °F of error.
- Max sustained wind: 0.5 point per kt of error.
- Precipitation: per 0.01" between forecast and observed: 0.4 pt for amounts 0.00 to 0.10", 0.3 for 0.11 to 0.25", 0.2 for 0.26 to 0.50", 0.1 above 0.50". A trace counts as 0.00.
- Forecasts are rounded as submitted (whole °F and kt, 0.01") before scoring.

## Guidance for the target day

Run = day/hour (UTC) of the model initialization.

| Model | Run | High °F | Low °F | Wind kt | Precip in |
| --- | --- | --: | --: | --: | --: |
| HRRR | 12/18Z | 63.6 | 39.1 | 4.8 | 0.00 |
| RRFS | 12/12Z | 63.9 | 39.3 | 4.6 | 0.00 |
| IFS | 12/12Z | 59.9 | 40.9 | 3.3 | 0.00 |
| GFS | 12/12Z | 56.9 | 41.9 | 3.7 | 0.00 |
| AIFS | 12/12Z | 60.5 | 39.7 | 2.7 | 0.00 |
| GFS_MOS | 12/12Z | 59.0 | 39.0 | 5.0 | 0.00 |
| NBM | 12/18Z | 63.0 | 37.0 | 4.0 | 0.00 |
| USL | 12/12Z | 60.0 | 37.0 | 8.0 | 0.00 |
| ENS | 10/18Z | 63.0 | 42.2 | 4.0 | 0.00 |
| AIFS_ENS | 10/18Z | 61.1 | 43.0 | 4.1 | 0.01 |
| GEFS | 12/12Z | 56.9 | 43.2 | 4.0 | 0.00 |
| HRRRCAST (precip only) | 12/12Z | — | — | — | 0.00 |
| REFS (precip only) | 12/12Z | — | — | — | 0.00 |
| NBM_QMD (precip only) | 12/12Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **61.1** | **36.6** | **7.3** | **0.00** |

Notes:
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [0, 0, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members (Open-Meteo)
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- HRRRCAST: median of 18 members (experimental AI model)
- REFS: median of 14 members, 12Z + 06Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS is shown but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted. Precip is weighted but not bias-corrected.

- High °F weights: NBM 0.19, RRFS 0.15, AIFS 0.12, GFS_MOS 0.12, USL 0.12, HRRR 0.11, IFS 0.10, GFS 0.09 (no track record yet: USL) (stale runs excluded: ENS, AIFS_ENS)
- Low °F weights: GFS_MOS 0.17, NBM 0.17, HRRR 0.12, GFS 0.12, USL 0.12, AIFS 0.10, IFS 0.10, RRFS 0.09 (no track record yet: USL) (stale runs excluded: ENS, AIFS_ENS)
- Wind kt weights: RRFS 0.16, HRRR 0.14, NBM 0.13, GFS_MOS 0.13, USL 0.13, IFS 0.12, GFS 0.10, AIFS 0.10 (no track record yet: USL) (stale runs excluded: ENS, AIFS_ENS)
- Precip in weights: GFS_MOS 0.13, RRFS 0.12, GFS 0.12, AIFS 0.12, NBM 0.12, USL 0.12, HRRR 0.12, IFS 0.12 (no track record yet: USL) (stale runs excluded: ENS, AIFS_ENS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 60.4 | 62.0 | 63.9 | 65.0 | 65.2 | 63.0 |
| ENS | 51 | Low °F | 40.4 | 41.0 | 42.0 | 43.2 | 44.5 | 42.2 |
| ENS | 51 | Wind kt | 2.4 | 2.8 | 3.9 | 4.8 | 5.7 | 4.0 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 |
| AIFS_ENS | 51 | High °F | 56.4 | 59.4 | 60.9 | 63.8 | 64.8 | 61.1 |
| AIFS_ENS | 51 | Low °F | 38.2 | 40.5 | 43.0 | 45.3 | 48.0 | 43.0 |
| AIFS_ENS | 51 | Wind kt | 2.7 | 3.2 | 3.8 | 4.8 | 5.9 | 4.1 |
| AIFS_ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 | 0.01 |
| GEFS | 31 | High °F | 54.8 | 55.4 | 56.6 | 58.4 | 59.0 | 56.9 |
| GEFS | 31 | Low °F | 42.0 | 42.6 | 43.1 | 44.0 | 44.6 | 43.2 |
| GEFS | 31 | Wind kt | 3.3 | 3.5 | 3.9 | 4.3 | 4.6 | 4.0 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 16% | 0% | 0% | 0% |
| AIFS_ENS | 24% | 0% | 0% | 0% |
| GEFS | 10% | 0% | 0% | 0% |
| HRRRCAST | 22% | 0% | 0% | 0% |
| REFS | 7% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.00", p90 0.00"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 2% | 13% | 12% | 4% | 13% to 28% | — |
| NBM | NBS P06 | 7% | 9% | 6% | 3% | 9% to 23% | — |
| ENS | member fraction | 0% | 2% | 2% | 16% | 16% | — |
| AIFS_ENS | member fraction | 2% | 2% | 10% | 18% | 24% | — |
| GEFS | member fraction | 0% | 0% | 10% | 3% | 10% | — |
| HRRRCAST | member fraction | — | — | — | — | 22% | — |
| REFS | member fraction | — | — | — | — | 7% | — |
| NBM_QMD | NBM QMD | 0% | 0% | 0% | 0% | 0% | — |

## Track record this period

Since 2026-09-28 at KOLM (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-13 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 14 | 5.6 | +0.1 | +1.9 | -1.3 | +0.01 | 1.1 | 3.2 | 2.4 | 0.01 |
| NBM | 14 | 6.3 | +0.6 | +1.7 | -3.1 | -0.01 | 0.9 | 3.1 | 3.8 | 0.01 |
| USL | 1 | 6.5 | +0.0 | +6.0 | -1.0 | +0.00 | 0.0 | 6.0 | 1.0 | 0.00 |
| GFS_MOS | 14 | 6.6 | +1.0 | +1.4 | -3.8 | +0.01 | 1.8 | 3.0 | 4.0 | 0.01 |
| HRRR | 14 | 8.6 | +0.9 | +3.5 | -3.0 | -0.01 | 2.0 | 4.5 | 3.5 | 0.01 |
| RRFS | 14 | 9.4 | +0.0 | +6.3 | -2.9 | +0.01 | 1.3 | 6.5 | 3.0 | 0.01 |
| AIFS | 14 | 9.8 | -1.3 | +4.8 | -5.2 | +0.01 | 1.7 | 5.5 | 5.5 | 0.01 |
| GFS | 14 | 10.0 | +1.6 | +3.7 | -5.1 | +0.01 | 2.5 | 4.6 | 5.2 | 0.01 |
| IFS | 14 | 10.5 | -2.1 | +5.6 | -4.3 | +0.01 | 2.2 | 5.9 | 4.4 | 0.01 |

## Daily verification (all 14 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 12.0 | 11.5 | 14.0 | 10.0 | 12.0 | 5.5 | 8.5 | — | 9.0 | GFS_MOS |
| 09-29 h | 11.5 | 10.0 | 11.1 | 13.4 | 5.6 | 4.8 | 10.8 | — | 6.3 | GFS_MOS |
| 09-30 h | 7.5 | 6.0 | 6.0 | 5.5 | 7.0 | 6.0 | 5.5 | — | 4.0 | CONSENSUS |
| 10-01 h | 6.0 | 7.0 | 8.0 | 5.5 | 8.0 | 1.5 | 2.0 | — | 2.0 | GFS_MOS |
| 10-02 h | 9.0 | 10.0 | 11.5 | 8.5 | 10.0 | 6.5 | 3.5 | — | 5.0 | NBM |
| 10-03 h | 10.5 | 10.5 | 10.0 | 13.5 | 10.5 | 9.5 | 8.0 | — | 7.5 | CONSENSUS |
| 10-04 h | 11.0 | 12.5 | 10.0 | 15.0 | 8.0 | 4.0 | 8.5 | — | 6.0 | GFS_MOS |
| 10-05 h | 2.5 | 10.0 | 11.5 | 6.5 | 7.5 | 1.0 | 4.0 | — | 2.0 | GFS_MOS |
| 10-06 h | 3.5 | 8.5 | 8.5 | 9.0 | 4.5 | 5.0 | 4.5 | — | 2.0 | CONSENSUS |
| 10-07 h | 10.5 | 7.0 | 6.0 | 14.0 | 8.5 | 16.0 | 10.0 | — | 10.5 | IFS |
| 10-08 h | 4.5 | 4.5 | 8.5 | 9.5 | 7.0 | 3.5 | 2.0 | — | 4.5 | NBM |
| 10-09 h | 12.7 | 11.9 | 16.0 | 10.5 | 19.2 | 12.0 | 8.3 | — | 9.1 | NBM |
| 10-10 h | 7.5 | 10.0 | 9.4 | 7.8 | 12.8 | 9.0 | 2.5 | — | 4.4 | NBM |
| 10-11 h | 12.0 | 12.0 | 16.0 | 11.5 | 16.0 | 8.5 | 10.0 | 6.5 | 6.5 | USL |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 67 | -1 | +0 | -2 | +1 | -3 | +1 | +1 | — | +0 |
| 09-29 h | 61 | +0 | -3 | -2 | -4 | +0 | +2 | +0 | — | -1 |
| 09-30 h | 66 | -4 | -2 | -2 | -2 | -2 | -1 | -1 | — | -2 |
| 10-01 h | 71 | +1 | +1 | -4 | +0 | -3 | +1 | -1 | — | +0 |
| 10-02 h | 73 | -4 | -3 | -4 | -2 | -3 | -2 | -1 | — | -2 |
| 10-03 h | 70 | +3 | +1 | -1 | +5 | +1 | +5 | +2 | — | +3 |
| 10-04 h | 72 | +6 | +3 | +1 | +6 | +1 | +2 | +3 | — | +3 |
| 10-05 h | 70 | +1 | -2 | -4 | +2 | -3 | +0 | +1 | — | -1 |
| 10-06 h | 68 | -1 | +1 | -3 | +4 | +0 | +2 | +1 | — | +1 |
| 10-07 h | 68 | +4 | +1 | -1 | +6 | +1 | +4 | +2 | — | +2 |
| 10-08 h | 73 | +1 | +0 | -2 | +4 | -2 | -3 | +0 | — | -1 |
| 10-09 h | 62 | +0 | -1 | -3 | -1 | -4 | +2 | +0 | — | -1 |
| 10-10 h | 59 | +1 | +1 | -2 | +0 | -1 | +1 | +0 | — | +0 |
| 10-11 h | 62 | +2 | +1 | -1 | +0 | -1 | +0 | +1 | +0 | +0 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 34 | +9 | +9 | +10 | +7 | +6 | +3 | +5 | — | +7 |
| 09-29 h | 55 | -4 | -2 | -3 | -5 | -2 | +0 | -5 | — | -3 |
| 09-30 h | 47 | -1 | +2 | +1 | +0 | +2 | +2 | -2 | — | +0 |
| 10-01 h | 43 | +4 | +5 | +3 | +4 | +4 | +0 | +0 | — | +2 |
| 10-02 h | 46 | +4 | +6 | +5 | +4 | +4 | +2 | +0 | — | +2 |
| 10-03 h | 46 | +5 | +7 | +6 | +5 | +6 | +1 | +4 | — | +3 |
| 10-04 h | 43 | +4 | +8 | +7 | +7 | +5 | +1 | +4 | — | +3 |
| 10-05 h | 46 | +1 | +8 | +6 | +4 | +3 | -1 | +2 | — | +0 |
| 10-06 h | 48 | +1 | +6 | +3 | +2 | +2 | -1 | +1 | — | +0 |
| 10-07 h | 50 | -3 | +3 | +1 | -3 | -3 | -8 | -5 | — | -6 |
| 10-08 h | 43 | +2 | +4 | +6 | +5 | +4 | +0 | +0 | — | +1 |
| 10-09 h | 40 | +8 | +8 | +8 | +4 | +8 | +5 | +5 | — | +5 |
| 10-10 h | 36 | +5 | +8 | +6 | +5 | +9 | +6 | +2 | — | +4 |
| 10-11 h | 30 | +9 | +10 | +12 | +8 | +11 | +6 | +7 | +6 | +6 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 12 | -4 | -5 | -4 | -4 | -6 | -3 | -5 | — | -4 |
| 09-29 h | 15 | -3 | -3 | -4 | -7 | -6 | -3 | -2 | — | -4 |
| 09-30 h | 11 | -5 | -4 | -6 | -7 | -6 | -6 | -5 | — | -4 |
| 10-01 h | 6 | -2 | -2 | -2 | -3 | -2 | -1 | -2 | — | +0 |
| 10-02 h | 10 | -2 | -2 | -5 | -5 | -6 | -5 | -5 | — | -2 |
| 10-03 h | 12 | -5 | -5 | -6 | -7 | -7 | -7 | -4 | — | -3 |
| 10-04 h | 7 | -2 | -3 | -4 | -4 | -4 | -2 | -3 | — | +0 |
| 10-05 h | 5 | -1 | +0 | -3 | -1 | -3 | +0 | -2 | — | +2 |
| 10-06 h | 10 | -3 | -3 | -5 | -6 | -5 | -4 | -5 | — | -2 |
| 10-07 h | 14 | -7 | -6 | -8 | -10 | -9 | -8 | -6 | — | -5 |
| 10-08 h | 4 | +3 | +1 | +1 | +1 | +2 | +1 | +4 | — | +5 |
| 10-09 h | 19 | -7 | -5 | -6 | -7 | -8 | -6 | -5 | — | -3 |
| 10-10 h | 10 | -3 | -2 | -2 | -4 | -4 | -4 | -1 | — | +0 |
| 10-11 h | 12 | -2 | -2 | -6 | -7 | -8 | -5 | -4 | -1 | -1 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 09-29 h | 0.22 | -0.18 | +0.16 | +0.19 | +0.03 | -0.02 | +0.05 | -0.15 | — | +0.01 |
| 09-30 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-01 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-02 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-03 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-04 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-05 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-06 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-07 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-08 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 |
| 10-09 h | 0.00 | +0.03 | +0.01 | +0.05 | +0.05 | +0.08 | +0.05 | +0.02 | — | +0.04 |
| 10-10 h | 0.00 | +0.00 | +0.00 | +0.01 | +0.02 | +0.02 | +0.00 | +0.00 | — | +0.01 |
| 10-11 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

## Today so far (2026-10-12, through 2026-10-12T19:54Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 60.1 °F, low 28.0 °F, max wind 3 kt, precip 0.00" (14 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 11/18Z | +6.4 | 6.4 | 65 (+5) pending | 38 (+10) | +1.9 | 0.00 | +0.00 |
| RRFS | 11/18Z | +7.9 | 7.9 | 63 (+3) pending | 39 (+11) | +1.6 | 0.00 | +0.00 |
| IFS | 11/12Z | +9.3 | 9.4 | 62 (+2) pending | 42 (+14) | +0.3 | 0.00 | +0.00 |
| GFS | 11/18Z | +5.9 | 5.9 | 64 (+3) pending | 37 (+9) | +1.4 | 0.00 | +0.00 |
| AIFS | 11/12Z | +5.8 | 7.1 | 62 (+2) pending | 37 (+9) | +0.2 | 0.00 | +0.00 |
| GFS_MOS | 11/18Z | +3.1 | 4.3 | 62 (+2) pending | 33 (+5) | +2.0 | — | — |
| NBM | 11/18Z | +5.5 | 6.0 | 65 (+5) pending | 35 (+7) | -0.6 | — | — |
| USL | 11/22Z | +2.1 | 2.7 | 63 (+3) pending | 32 (+4) | +1.7 | 0.00 | +0.00 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- NWS Area Forecast Discussion (SEW): https://forecast.weather.gov/product.php?site=SEW&issuedby=SEW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
