# WxChallenge forecast brief: Tampa, FL (KTPA)

- Station: **KTPA**
- Target day: **2026-10-10**, scored over 2026-10-10T06Z to 2026-10-11T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-10T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-09T23:19:06+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 09/18Z | 82.6 | 76.5 | 11.4 | 0.77 |
| RRFS | 09/18Z | 84.0 | 77.6 | 11.9 | 0.21 |
| IFS | 09/12Z | 84.6 | 76.7 | 8.3 | 0.32 |
| GFS | 09/12Z | 87.9 | 77.7 | 11.8 | 0.21 |
| AIFS | 09/12Z | 86.2 | 79.3 | 11.8 | 0.28 |
| GFS_MOS | 09/18Z | 90.0 | 80.0 | 12.0 | 0.32 |
| NBM | 09/18Z | 87.0 | 78.0 | 12.0 | 0.11 |
| USL | 09/22Z | 88.0 | 79.0 | 14.0 | 0.16 |
| ENS | 09/06Z | 83.8 | 76.6 | 10.2 | 0.37 |
| AIFS_ENS | 09/12Z | 86.1 | 77.9 | 12.2 | 0.21 |
| GEFS | 09/12Z | 89.8 | 79.8 | 13.1 | 0.09 |
| HRRRCAST (precip only) | 09/12Z | — | — | — | 0.01 |
| REFS (precip only) | 09/18Z | — | — | — | 0.30 |
| NBM_QMD (precip only) | 09/12Z | — | — | — | 0.33 |
| **CONSENSUS** |  | **86.0** | **79.0** | **15.0** | **0.29** |

Notes:
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [1, 1, 1, 2] -> midpoints
- NBM: NBS Q06 amounts
- ENS: ensemble mean of 51 members (Open-Meteo)
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- HRRRCAST: median of 18 members (experimental AI model)
- REFS: median of 14 members, 18Z + 12Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS is shown but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted. Precip is weighted but not bias-corrected.

- High °F weights: AIFS_ENS 0.13, NBM 0.12, AIFS 0.12, ENS 0.11, HRRR 0.11, USL 0.10, IFS 0.09, GFS_MOS 0.08, GFS 0.08, RRFS 0.06
- Low °F weights: USL 0.14, AIFS 0.14, GFS_MOS 0.12, NBM 0.11, AIFS_ENS 0.10, GFS 0.10, IFS 0.09, ENS 0.07, HRRR 0.07, RRFS 0.06
- Wind kt weights: USL 0.17, GFS 0.11, HRRR 0.11, AIFS_ENS 0.10, ENS 0.09, RRFS 0.09, NBM 0.09, GFS_MOS 0.09, IFS 0.08, AIFS 0.07
- Precip in weights: AIFS 0.11, GFS 0.11, NBM 0.11, USL 0.11, IFS 0.10, AIFS_ENS 0.10, HRRR 0.10, ENS 0.09, GFS_MOS 0.09, RRFS 0.08

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 81.8 | 82.9 | 84.0 | 84.8 | 85.9 | 83.8 |
| ENS | 51 | Low °F | 75.6 | 76.0 | 76.7 | 77.3 | 77.6 | 76.6 |
| ENS | 51 | Wind kt | 8.8 | 9.2 | 10.1 | 11.0 | 11.5 | 10.2 |
| ENS | 51 | Precip in | 0.16 | 0.27 | 0.36 | 0.47 | 0.55 | 0.37 |
| AIFS_ENS | 51 | High °F | 82.8 | 84.3 | 85.7 | 88.2 | 89.5 | 86.1 |
| AIFS_ENS | 51 | Low °F | 76.8 | 77.4 | 77.8 | 78.4 | 79.1 | 77.9 |
| AIFS_ENS | 51 | Wind kt | 10.9 | 11.3 | 12.1 | 12.9 | 13.9 | 12.2 |
| AIFS_ENS | 51 | Precip in | 0.05 | 0.07 | 0.14 | 0.27 | 0.52 | 0.21 |
| GEFS | 31 | High °F | 88.9 | 89.5 | 89.8 | 90.3 | 90.8 | 89.8 |
| GEFS | 31 | Low °F | 79.5 | 79.6 | 79.8 | 80.0 | 80.4 | 79.8 |
| GEFS | 31 | Wind kt | 11.6 | 12.5 | 12.9 | 13.7 | 14.5 | 13.1 |
| GEFS | 31 | Precip in | 0.00 | 0.02 | 0.05 | 0.13 | 0.18 | 0.09 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.01 | 0.01 | 0.02 | 0.14 | 0.04 |
| REFS | 14 | Precip in | 0.10 | 0.17 | 0.30 | 0.43 | 0.68 | 0.34 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 96% | 76% | 14% |
| AIFS_ENS | 96% | 65% | 28% | 12% |
| GEFS | 84% | 42% | 3% | 0% |
| HRRRCAST | 61% | 17% | 0% | 0% |
| REFS | 100% | 86% | 57% | 14% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.07", p50 0.33", p75 0.81", p90 1.18"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 53% | 39% | 43% | 57% | 57% to 93% | 0.20 (24) |
| NBM | NBS P06 | 26% | 37% | 56% | 40% | 56% to 88% | 0.13 (24) |
| ENS | member fraction | 51% | 100% | 96% | 69% | 100% | 0.20 (24) |
| AIFS_ENS | member fraction | 57% | 84% | 78% | 59% | 96% | 0.23 (24) |
| GEFS | member fraction | 48% | 16% | 55% | 61% | 84% | 0.29 (24) |
| HRRRCAST | member fraction | — | — | — | — | 61% | 0.17 (24) |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 30% | 50% | 62% | 34% | 84% | 0.12 (24) |

For reference, always forecasting the period's observed frequency (46% of 6-h blocks wet) scores Brier 0.25.

## Track record this period

Since 2026-09-16 at KTPA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-09-29 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 23 | 9.0 | +0.3 | -0.4 | -1.1 | +0.05 | 1.7 | 1.2 | 3.0 | 0.29 |
| USL | 12 | 9.0 | +1.5 | -0.3 | -1.8 | +0.09 | 2.2 | 1.0 | 2.4 | 0.29 |
| NBM | 23 | 9.7 | +0.5 | -0.9 | -4.8 | -0.12 | 1.6 | 1.6 | 4.8 | 0.29 |
| GFS | 23 | 10.5 | +0.6 | +0.1 | -2.3 | +0.01 | 2.6 | 1.7 | 3.8 | 0.27 |
| AIFS | 23 | 10.7 | -0.8 | -0.6 | -6.0 | +0.07 | 1.7 | 1.0 | 6.0 | 0.26 |
| AIFS_ENS | 9 | 11.5 | +0.2 | -1.4 | -4.4 | +0.03 | 1.4 | 1.7 | 4.4 | 0.35 |
| HRRR | 23 | 11.8 | -1.5 | -2.9 | -2.4 | +0.15 | 1.9 | 2.9 | 3.9 | 0.36 |
| IFS | 23 | 12.4 | +0.2 | -1.5 | -5.6 | -0.16 | 2.2 | 1.9 | 5.6 | 0.34 |
| GFS_MOS | 23 | 12.4 | +2.5 | +0.5 | -4.8 | +0.34 | 2.6 | 1.2 | 4.9 | 0.48 |
| ENS | 9 | 13.4 | -0.9 | -2.1 | -4.7 | -0.08 | 1.9 | 2.4 | 4.7 | 0.45 |
| GEFS | 6 | 13.7 | +0.2 | +0.8 | -0.6 | -0.15 | 3.3 | 0.8 | 4.3 | 0.47 |
| RRFS | 23 | 16.4 | -3.0 | -3.5 | -4.7 | +0.22 | 3.6 | 3.5 | 4.8 | 0.62 |

## Daily verification (all 23 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-16 h | 13.5 | 17.0 | 7.8 | 4.6 | 8.9 | 4.0 | 4.5 | — | — | — | — | 9.1 | GFS_MOS |
| 09-17 h | 10.0 | 12.0 | 11.3 | 1.0 | 5.0 | 5.5 | 5.5 | — | — | — | — | 5.5 | GFS |
| 09-18 h | 5.5 | 11.0 | 11.2 | 5.9 | 9.6 | 6.5 | 5.9 | — | — | — | — | 4.0 | CONSENSUS |
| 09-19 h | 18.4 | 32.4 | 25.5 | 24.7 | 20.1 | 27.1 | 22.4 | — | — | — | — | 20.3 | HRRR |
| 09-20 h | 11.1 | 12.1 | 12.2 | 11.6 | 13.8 | 11.5 | 10.4 | — | — | — | — | 6.9 | CONSENSUS |
| 09-21 h | 24.2 | 12.0 | 9.7 | 8.0 | 8.1 | 9.3 | 13.0 | — | — | — | — | 11.0 | GFS |
| 09-22 h | 32.3 | 30.9 | 27.3 | 18.2 | 20.1 | 19.3 | 17.1 | — | — | — | — | 18.8 | NBM |
| 09-23 h | 12.0 | 19.6 | 10.7 | 9.5 | 12.1 | 10.0 | 4.9 | — | — | — | — | 9.6 | NBM |
| 09-24 h | 6.5 | 7.0 | 4.8 | 2.5 | 4.2 | 9.0 | 5.0 | — | — | — | — | 2.9 | GFS |
| 09-25 h | 11.0 | 11.5 | 5.0 | 3.0 | 7.3 | 6.5 | 3.0 | — | — | — | — | 2.0 | CONSENSUS |
| 09-26 h | 6.0 | 7.5 | 2.0 | 5.0 | 5.0 | 7.0 | 3.5 | — | — | — | — | 1.5 | CONSENSUS |
| 09-27 h | 5.0 | 5.0 | 6.5 | 8.5 | 4.0 | 6.5 | 7.0 | 4.0 | — | — | — | 4.0 | AIFS |
| 09-28 h | 4.0 | 7.0 | 12.0 | 5.5 | 4.9 | 5.0 | 4.5 | 3.0 | — | — | — | 4.5 | USL |
| 09-29 | 6.0 | 8.5 | 12.8 | 4.0 | 13.9 | 2.5 | 5.3 | 1.0 | — | — | — | 5.5 | USL |
| 09-30 | 7.8 | 13.2 | 19.5 | 16.8 | 12.8 | 10.8 | 12.0 | 5.4 | 14.2 | 16.0 | — | 8.8 | USL |
| 10-01 | 13.3 | 15.2 | 6.1 | 6.6 | 2.7 | 13.4 | 6.7 | 4.2 | 3.5 | 7.1 | — | 2.2 | CONSENSUS |
| 10-02 | 10.6 | 12.5 | 16.1 | 16.4 | 13.3 | 26.7 | 13.2 | 6.5 | 14.1 | 9.2 | — | 13.2 | USL |
| 10-03 | 10.6 | 24.0 | 14.6 | 19.7 | 20.5 | 16.8 | 16.4 | 17.7 | 20.4 | 14.8 | 15.0 | 16.0 | HRRR |
| 10-04 | 6.5 | 8.0 | 9.9 | 8.6 | 9.7 | 12.4 | 7.2 | 15.9 | 12.4 | 7.8 | 8.7 | 8.7 | HRRR |
| 10-05 | 7.8 | 14.9 | 10.8 | 22.1 | 17.3 | 22.2 | 10.4 | 11.0 | 11.1 | 13.8 | 13.7 | 12.4 | HRRR |
| 10-06 | 22.5 | 20.1 | 17.5 | 18.4 | 5.9 | 10.0 | 16.4 | 18.0 | 15.4 | 8.6 | 17.3 | 10.7 | AIFS |
| 10-07 | 17.2 | 20.0 | 24.3 | 11.5 | 17.3 | 22.4 | 21.7 | 16.1 | 20.3 | 16.5 | 20.9 | 13.9 | GFS |
| 10-08 | 10.1 | 56.4 | 7.2 | 10.2 | 9.0 | 21.3 | 7.0 | 4.8 | 9.5 | 10.0 | 6.8 | 14.6 | USL |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-16 h | 92 | -7 | -6 | -2 | -1 | -2 | +0 | -2 | — | — | — | — | -3 |
| 09-17 h | 92 | -6 | -7 | -5 | +0 | -3 | +2 | -3 | — | — | — | — | -3 |
| 09-18 h | 92 | -2 | -5 | -5 | +1 | -3 | +2 | -1 | — | — | — | — | +0 |
| 09-19 h | 89 | -3 | -4 | +0 | +1 | -1 | +2 | +1 | — | — | — | — | +1 |
| 09-20 h | 88 | -1 | -3 | +1 | +3 | -1 | +4 | +1 | — | — | — | — | +2 |
| 09-21 h | 89 | -1 | -5 | -3 | +2 | -1 | +3 | +0 | — | — | — | — | +0 |
| 09-22 h | 90 | -6 | -6 | -3 | +0 | -1 | +1 | -1 | — | — | — | — | -1 |
| 09-23 h | 90 | -3 | -6 | -4 | +1 | -2 | +1 | -1 | — | — | — | — | -1 |
| 09-24 h | 86 | -1 | -3 | +1 | +2 | +1 | +5 | +3 | — | — | — | — | +2 |
| 09-25 h | 86 | -5 | -6 | -1 | +0 | -4 | +1 | +0 | — | — | — | — | -1 |
| 09-26 h | 84 | -3 | -5 | +0 | +1 | -3 | +2 | +1 | — | — | — | — | +0 |
| 09-27 h | 83 | +1 | -2 | +5 | +2 | +0 | +4 | +3 | +3 | — | — | — | +3 |
| 09-28 h | 85 | +1 | -2 | +7 | +0 | +2 | +3 | +3 | +3 | — | — | — | +3 |
| 09-29 | 87 | -1 | -2 | +3 | -1 | -4 | +1 | +1 | +0 | — | — | — | -1 |
| 09-30 | 88 | +0 | -3 | -1 | -2 | -1 | +2 | +0 | +1 | -2 | +0 | — | -1 |
| 10-01 | 88 | -3 | -7 | +0 | +2 | +0 | +2 | +0 | +1 | +0 | +1 | — | +0 |
| 10-02 | 87 | -4 | -2 | +0 | +4 | +0 | +4 | +1 | +2 | -1 | +1 | — | +1 |
| 10-03 | 90 | -1 | -6 | -5 | -5 | -3 | -1 | -3 | -2 | -4 | -2 | -5 | -3 |
| 10-04 | 89 | -2 | -2 | -1 | +1 | +1 | +2 | +0 | +1 | -2 | +1 | +1 | +0 |
| 10-05 | 88 | +0 | -3 | -1 | -3 | -1 | +1 | -1 | -1 | -2 | +0 | -2 | -1 |
| 10-06 | 79 | +2 | +3 | +5 | +8 | +3 | +7 | +5 | +6 | +4 | +3 | +7 | +5 |
| 10-07 | 83 | -2 | -4 | +0 | -4 | -3 | +1 | -2 | -1 | -2 | -3 | -3 | -2 |
| 10-08 | 79 | +0 | +1 | +2 | +3 | +0 | +4 | +2 | +4 | +0 | +1 | +2 | +2 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-16 h | 78 | -6 | -4 | -3 | -1 | -2 | -1 | -1 | — | — | — | — | -3 |
| 09-17 h | 76 | -4 | -3 | -3 | +0 | +0 | +1 | -1 | — | — | — | — | -1 |
| 09-18 h | 75 | -2 | -2 | -1 | +1 | +0 | +2 | -1 | — | — | — | — | +1 |
| 09-19 h | 75 | -3 | -3 | -2 | +1 | +0 | +2 | -1 | — | — | — | — | +0 |
| 09-20 h | 75 | -3 | -3 | -2 | +2 | -1 | +0 | -1 | — | — | — | — | +0 |
| 09-21 h | 73 | -1 | -2 | +0 | +4 | +1 | +3 | +1 | — | — | — | — | +2 |
| 09-22 h | 76 | -4 | -4 | -3 | +1 | -1 | +0 | -1 | — | — | — | — | -1 |
| 09-23 h | 76 | -3 | -2 | -1 | +1 | +1 | +1 | +0 | — | — | — | — | +0 |
| 09-24 h | 74 | -3 | -3 | +0 | +0 | +0 | +2 | +0 | — | — | — | — | +0 |
| 09-25 h | 70 | -3 | -3 | -1 | +2 | +0 | +3 | +1 | — | — | — | — | +1 |
| 09-26 h | 66 | -1 | -1 | +0 | +3 | +0 | +4 | +1 | — | — | — | — | +1 |
| 09-27 h | 65 | -2 | -1 | +0 | +4 | -1 | +1 | +2 | +1 | — | — | — | +1 |
| 09-28 h | 70 | -1 | -3 | +3 | +4 | +0 | -1 | +0 | +0 | — | — | — | +1 |
| 09-29 | 74 | -5 | -4 | -2 | +2 | -1 | -1 | -2 | -1 | — | — | — | -2 |
| 09-30 | 75 | -3 | -3 | -4 | -2 | -1 | -1 | -3 | -1 | -3 | -3 | — | -2 |
| 10-01 | 74 | -2 | -2 | +0 | +2 | +0 | +1 | +1 | +1 | +0 | +0 | — | +0 |
| 10-02 | 77 | -5 | -4 | -2 | -1 | -1 | +1 | -1 | +0 | -2 | -1 | — | -1 |
| 10-03 | 80 | -4 | -8 | -4 | -3 | -3 | -2 | -4 | -3 | -5 | -4 | +0 | -3 |
| 10-04 | 79 | -4 | -5 | -4 | -1 | -2 | +0 | -3 | -2 | -4 | -3 | +1 | -2 |
| 10-05 | 78 | -3 | -4 | -4 | -1 | -2 | +0 | -2 | -1 | -3 | -2 | +1 | -1 |
| 10-06 | 76 | -3 | -2 | -1 | -1 | +0 | +1 | -1 | +0 | -2 | -1 | +1 | +0 |
| 10-07 | 73 | -1 | -2 | +1 | -1 | +2 | +2 | +1 | +2 | +1 | +1 | +2 | +2 |
| 10-08 | 75 | -2 | -6 | -1 | -2 | -1 | -1 | -2 | +0 | -2 | -1 | +0 | -1 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-16 h | 15 | -1 | -3 | -4 | -2 | -5 | -6 | -3 | — | — | — | — | -3 |
| 09-17 h | 15 | +0 | -4 | -5 | -2 | -4 | -5 | -3 | — | — | — | — | -3 |
| 09-18 h | 13 | -3 | -4 | -4 | -3 | -4 | -5 | -3 | — | — | — | — | -2 |
| 09-19 h | 17 | -5 | -10 | -11 | -7 | -12 | -11 | -11 | — | — | — | — | -7 |
| 09-20 h | 17 | -7 | -11 | -13 | -10 | -13 | -11 | -12 | — | — | — | — | -8 |
| 09-21 h | 11 | -2 | -6 | -7 | -4 | -7 | -5 | -5 | — | — | — | — | -1 |
| 09-22 h | 18 | -12 | -14 | -14 | -11 | -14 | -12 | -14 | — | — | — | — | -9 |
| 09-23 h | 9 | +8 | -3 | -5 | +1 | -3 | -2 | -3 | — | — | — | — | +5 |
| 09-24 h | 14 | -5 | -2 | -6 | -1 | -4 | -4 | -4 | — | — | — | — | +1 |
| 09-25 h | 13 | -6 | -5 | -6 | -2 | -5 | -5 | -4 | — | — | — | — | +0 |
| 09-26 h | 10 | -4 | -3 | -4 | -2 | -4 | -2 | -3 | — | — | — | — | +1 |
| 09-27 h | 10 | -4 | -4 | -3 | -5 | -6 | -3 | -4 | +0 | — | — | — | +0 |
| 09-28 h | 10 | -4 | -4 | -4 | -3 | -5 | -2 | -3 | +0 | — | — | — | +1 |
| 09-29 | 10 | +0 | -5 | -1 | -2 | -5 | -1 | -3 | +0 | — | — | — | +1 |
| 09-30 | 14 | -3 | -7 | -6 | -5 | -7 | -7 | -7 | -4 | -8 | -7 | — | -3 |
| 10-01 | 14 | -4 | -4 | -5 | -1 | -5 | -6 | -3 | -2 | -4 | -5 | — | -2 |
| 10-02 | 10 | +0 | -2 | -1 | +1 | -2 | -2 | -1 | -1 | -2 | -1 | — | +1 |
| 10-03 | 11 | +2 | -1 | -4 | -2 | -4 | -3 | -3 | -2 | -3 | -3 | +1 | +1 |
| 10-04 | 9 | -1 | -2 | -2 | +0 | -2 | -1 | -2 | +0 | -2 | -2 | +2 | +2 |
| 10-05 | 11 | +1 | -6 | -6 | -4 | -6 | -5 | -5 | -1 | -5 | -5 | -2 | -1 |
| 10-06 | 8 | +4 | +0 | -3 | +3 | -4 | -2 | -2 | +2 | -2 | -1 | +3 | +3 |
| 10-07 | 23 | -13 | -14 | -15 | -9 | -18 | -16 | -15 | -13 | -14 | -15 | -12 | -11 |
| 10-08 | 9 | +1 | +1 | -4 | +7 | -2 | +1 | -1 | +1 | -2 | +0 | +5 | +3 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-16 h | 0.00 | +0.00 | +0.15 | +0.02 | +0.04 | +0.06 | +0.00 | +0.00 | — | — | — | — | +0.04 |
| 09-17 h | 0.00 | +0.00 | +0.00 | +0.02 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 09-18 h | 0.00 | +0.00 | +0.05 | +0.08 | +0.06 | +0.12 | +0.00 | +0.06 | — | — | — | — | +0.05 |
| 09-19 h | 1.31 | -0.90 | -1.28 | -1.22 | -1.25 | -1.06 | -1.21 | -1.12 | — | — | — | — | -1.15 |
| 09-20 h | 0.10 | -0.09 | +0.02 | +0.09 | -0.04 | +0.19 | -0.05 | +0.08 | — | — | — | — | +0.03 |
| 09-21 h | 0.08 | +1.51 | +0.06 | +0.10 | +0.00 | +0.08 | +0.02 | +0.38 | — | — | — | — | +0.33 |
| 09-22 h | 0.78 | -0.78 | -0.72 | -0.73 | -0.66 | -0.64 | -0.68 | -0.54 | — | — | — | — | -0.68 |
| 09-23 h | 0.00 | +0.05 | +0.33 | +0.08 | +0.20 | +0.22 | +0.20 | +0.06 | — | — | — | — | +0.17 |
| 09-24 h | 0.00 | +0.00 | +0.00 | +0.02 | +0.00 | +0.03 | +0.00 | +0.00 | — | — | — | — | +0.01 |
| 09-25 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.02 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 09-26 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 09-27 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 09-28 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 09-29 | 0.00 | +0.00 | +0.00 | +0.21 | +0.00 | +0.18 | +0.00 | +0.02 | +0.00 | — | — | — | +0.05 |
| 09-30 | 0.42 | +0.25 | -0.18 | -0.41 | -0.38 | -0.30 | -0.20 | -0.24 | +0.07 | -0.23 | -0.36 | — | -0.20 |
| 10-01 | 0.28 | +0.41 | -0.15 | +0.18 | -0.08 | -0.01 | +0.52 | -0.15 | +0.06 | -0.06 | -0.13 | — | +0.06 |
| 10-02 | 0.00 | +0.04 | +0.15 | +0.51 | +0.37 | +0.39 | +1.22 | +0.36 | +0.10 | +0.33 | +0.19 | — | +0.36 |
| 10-03 | 0.00 | +0.12 | +0.30 | +0.09 | +0.36 | +0.45 | +0.44 | +0.23 | +0.41 | +0.32 | +0.21 | +0.30 | +0.30 |
| 10-04 | 0.01 | +0.00 | +0.00 | +0.10 | +0.19 | +0.16 | +0.33 | +0.08 | +0.48 | +0.15 | +0.07 | +0.16 | +0.16 |
| 10-05 | 0.00 | +0.11 | +0.13 | +0.07 | +0.76 | +0.39 | +1.02 | +0.13 | +0.25 | +0.09 | +0.29 | +0.31 | +0.32 |
| 10-06 | 1.36 | +1.55 | -1.16 | -0.93 | -0.79 | -0.09 | -0.10 | -0.90 | -0.98 | -0.84 | -0.41 | -0.78 | -0.42 |
| 10-07 | 2.16 | -0.77 | -0.70 | -1.58 | +0.20 | -0.33 | +1.14 | -1.12 | +0.66 | -1.03 | -0.50 | -0.99 | -0.44 |
| 10-08 | 0.66 | +0.76 | +4.89 | +0.22 | +0.17 | +0.70 | +1.58 | +0.25 | +0.03 | +0.65 | +0.80 | +0.23 | +1.01 |

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-03 | 0.00" (dry) | 67/48/59/52 | 17/14/66/42 | 45/61/100/53 | 57/53/84/61 | 90/58/77/48 | 33/0/72/33 | 24h 100% | 12/8/65/38 |
| 10-04 | 0.01" (wet: 00-06) | 25/22/62/62 | 7/6/37/50 | 18/43/90/53 | 12/18/65/49 | 13/0/84/81 | 0/0/22/67 | 24h 93% | 7/0/28/50 |
| 10-05 | 0.00" (dry) | 47/46/76/60 | 8/15/49/34 | 4/24/80/24 | 10/49/92/88 | 48/77/84/71 | 22/61/83/94 | 24h 100% | 3/6/46/33 |
| 10-06 | 1.36" (wet: 12-18, 18-00, 00-06) | 55/65/78/61 | 17/45/63/68 | 31/84/96/86 | 61/98/100/94 | 94/97/100/42 | 33/100/100/100 | 24h 100% | 16/46/86/61 |
| 10-07 | 2.16" (wet: 06-12, 12-18, 18-00, 00-06) | 52/92/87/86 | 73/79/74/42 | 96/98/100/78 | 98/100/98/88 | 90/100/100/94 | 100/100/100/100 | 24h 100% | 61/81/91/55 |
| 10-08 | 0.66" (wet: 12-18, 18-00, 00-06) | 74/82/82/90 | 49/58/90/52 | 90/98/100/80 | 92/98/96/94 | 94/97/100/94 | 100/100/100/100 | 24h 100% | 44/66/82/44 |

## Today so far (2026-10-09, through 2026-10-09T22:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 89.1 °F, low 75.0 °F, max wind 12 kt, precip 0.00" (17 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 08/18Z | -3.1 | 3.1 | 84 (-5) | 72 (-3) | +0.5 | 0.00 | +0.00 |
| RRFS | 08/18Z | -2.8 | 2.8 | 85 (-4) | 73 (-2) | +0.9 | 0.02 | +0.02 |
| IFS | 08/12Z | -2.4 | 2.4 | 87 (-2) | 73 (-2) | -0.5 | 0.14 | +0.14 |
| GFS | 08/12Z | -0.4 | 1.1 | 90 (+1) | 73 (-2) | +3.4 | 0.20 | +0.20 |
| AIFS | 08/12Z | -1.3 | 1.4 | 87 (-2) | 74 (-1) | +1.7 | 0.16 | +0.16 |
| GFS_MOS | 08/18Z | -0.3 | 1.2 | 89 (+0) | 76 (+1) | +1.9 | — | — |
| NBM | 08/18Z | -2.9 | 2.9 | 87 (-2) | 73 (-2) | +1.5 | — | — |
| USL | 08/22Z | -0.2 | 0.8 | 89 (+0) | 75 (+0) | -1.1 | 0.13 | +0.13 |
| ENS | 08/12Z | -2.5 | 2.5 | 86 (-3) | 73 (-2) | -0.2 | 0.17 | +0.17 |
| AIFS_ENS | 08/12Z | -1.1 | 1.3 | 88 (-1) | 73 (-2) | +2.4 | 0.10 | +0.10 |
| GEFS | 08/18Z | +1.3 | 1.4 | 89 (+0) | 76 (+1) | +4.5 | 0.13 | +0.13 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- NWS Area Forecast Discussion (TBW): https://forecast.weather.gov/product.php?site=TBW&issuedby=TBW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
