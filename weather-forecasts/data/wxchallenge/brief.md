# WxChallenge forecast brief: Tampa, FL (KTPA)

- Station: **KTPA**
- Target day: **2026-10-12**, scored over 2026-10-12T06Z to 2026-10-13T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-12T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-11T23:54:43+00:00 (refreshed several times an hour while the forecast job runs)
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
| HRRR | 11/18Z | 80.4 | 67.8 | 7.3 | 0.00 |
| RRFS | 11/18Z | 78.7 | 67.4 | 7.3 | 0.00 |
| IFS | 11/12Z | 85.5 | 71.2 | 6.7 | 0.00 |
| GFS | 11/18Z | 87.6 | 71.3 | 9.3 | 0.00 |
| AIFS | 11/12Z | 85.1 | 70.3 | 6.9 | 0.00 |
| GFS_MOS | 11/18Z | 89.0 | 71.0 | 8.0 | 0.00 |
| NBM | 11/18Z | 85.0 | 70.0 | 9.0 | 0.00 |
| USL | — | — | — | — | — |
| ENS | 10/18Z | 85.9 | 70.3 | 6.4 | 0.00 |
| AIFS_ENS | 10/18Z | 85.4 | 69.6 | 7.5 | 0.00 |
| GEFS | 11/18Z | 87.2 | 74.7 | 9.8 | 0.00 |
| HRRRCAST (precip only) | 11/12Z | — | — | — | 0.01 |
| REFS (precip only) | 11/18Z | — | — | — | 0.00 |
| NBM_QMD (precip only) | 11/12Z | — | — | — | 0.00 |
| **CONSENSUS** |  | **85.6** | **71.1** | **16.3** | **0.00** |

Notes:
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [0, 0, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- USL: failed this run (no USL run for 2026-10-12 available at 2026-10-11 23Z)
- ENS: ensemble mean of 51 members (Open-Meteo)
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- HRRRCAST: median of 18 members (experimental AI model)
- REFS: median of 14 members, 18Z + 12Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS is shown but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted. Precip is weighted but not bias-corrected.

- High °F weights: AIFS_ENS 0.14, NBM 0.14, AIFS 0.13, GFS 0.11, GFS_MOS 0.11, IFS 0.10, ENS 0.10, HRRR 0.10, RRFS 0.07
- Low °F weights: AIFS 0.17, GFS_MOS 0.16, NBM 0.12, AIFS_ENS 0.11, GFS 0.11, IFS 0.10, ENS 0.09, HRRR 0.07, RRFS 0.07
- Wind kt weights: GFS 0.13, HRRR 0.13, RRFS 0.12, GFS_MOS 0.12, NBM 0.12, IFS 0.11, AIFS 0.11, AIFS_ENS 0.09, ENS 0.08
- Precip in weights: AIFS 0.12, NBM 0.12, GFS 0.12, AIFS_ENS 0.12, IFS 0.11, HRRR 0.11, ENS 0.10, GFS_MOS 0.10, RRFS 0.09

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 84.0 | 84.8 | 86.2 | 87.0 | 87.6 | 85.9 |
| ENS | 51 | Low °F | 68.6 | 69.6 | 70.5 | 71.3 | 71.5 | 70.3 |
| ENS | 51 | Wind kt | 5.3 | 5.8 | 6.3 | 7.0 | 7.8 | 6.4 |
| ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| AIFS_ENS | 51 | High °F | 83.5 | 84.2 | 85.4 | 86.6 | 87.3 | 85.4 |
| AIFS_ENS | 51 | Low °F | 67.6 | 68.8 | 69.7 | 70.5 | 71.2 | 69.6 |
| AIFS_ENS | 51 | Wind kt | 6.2 | 6.7 | 7.5 | 8.1 | 8.8 | 7.5 |
| AIFS_ENS | 51 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| GEFS | 31 | High °F | 86.2 | 86.7 | 87.4 | 87.8 | 88.8 | 87.2 |
| GEFS | 31 | Low °F | 73.9 | 74.3 | 74.5 | 75.2 | 75.6 | 74.7 |
| GEFS | 31 | Wind kt | 9.0 | 9.4 | 9.9 | 10.2 | 10.8 | 9.8 |
| GEFS | 31 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HRRRCAST | 18 | Precip in | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 |
| REFS | 14 | Precip in | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 0% | 0% | 0% | 0% |
| AIFS_ENS | 2% | 0% | 0% | 0% |
| GEFS | 0% | 0% | 0% | 0% |
| HRRRCAST | 11% | 0% | 0% | 0% |
| REFS | 0% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.00", p75 0.00", p90 0.00"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 3% | 5% | 0% | 0% | 5% to 8% | 0.20 (32) |
| NBM | NBS P06 | 0% | 0% | 0% | 0% | 0% to 0% | 0.14 (32) |
| ENS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.30 (32) |
| AIFS_ENS | member fraction | 2% | 0% | 0% | 0% | 2% | 0.26 (32) |
| GEFS | member fraction | 0% | 0% | 0% | 0% | 0% | 0.31 (32) |
| HRRRCAST | member fraction | — | — | — | — | 11% | 0.17 (24) |
| REFS | member fraction | — | — | — | — | 0% | — |
| NBM_QMD | NBM QMD | 0% | 0% | 0% | 0% | 0% | 0.13 (32) |

For reference, always forecasting the period's observed frequency (34% of 6-h blocks wet) scores Brier 0.23.

## Track record this period

Since 2026-09-16 at KTPA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-09-29 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 25 | 10.8 | -0.3 | -0.4 | -6.0 | +0.07 | 1.9 | 1.1 | 7.7 | 0.28 |
| NBM | 25 | 11.5 | +0.0 | -1.1 | -9.8 | -0.09 | 1.8 | 1.6 | 9.8 | 0.26 |
| USL | 14 | 12.0 | +0.9 | -0.4 | -9.4 | +0.11 | 2.0 | 0.9 | 9.9 | 0.27 |
| GFS | 25 | 12.4 | +0.4 | -0.3 | -7.4 | +0.05 | 2.3 | 1.8 | 8.6 | 0.27 |
| AIFS | 25 | 12.6 | -1.2 | -0.7 | -10.8 | +0.10 | 1.9 | 1.0 | 10.8 | 0.25 |
| GFS_MOS | 25 | 14.0 | +2.0 | +0.5 | -9.7 | +0.33 | 2.3 | 1.1 | 9.8 | 0.45 |
| HRRR | 25 | 14.1 | -2.2 | -2.9 | -7.6 | +0.19 | 2.6 | 2.9 | 8.9 | 0.37 |
| IFS | 25 | 14.4 | -0.4 | -1.7 | -10.7 | -0.10 | 2.4 | 2.0 | 10.7 | 0.33 |
| AIFS_ENS | 11 | 15.4 | -0.5 | -1.6 | -13.0 | +0.07 | 1.7 | 1.8 | 13.0 | 0.31 |
| GEFS | 8 | 17.3 | +0.1 | +0.7 | -12.4 | -0.06 | 2.6 | 0.7 | 15.1 | 0.38 |
| RRFS | 25 | 17.9 | -3.3 | -3.2 | -9.6 | +0.21 | 3.8 | 3.2 | 9.7 | 0.56 |
| ENS | 11 | 18.1 | -1.8 | -2.2 | -13.8 | +0.00 | 2.5 | 2.4 | 13.8 | 0.41 |

## Daily verification (all 25 days this period)

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
| 10-09 | 11.8 | 12.2 | 12.7 | 11.2 | 13.0 | 11.0 | 12.1 | 11.2 | 15.5 | 10.2 | 7.2 | 8.8 | GEFS |
| 10-10 | 68.7 | 57.3 | 61.9 | 56.2 | 56.1 | 53.9 | 51.3 | 49.8 | 62.5 | 55.3 | 48.5 | 55.2 | GEFS |

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
| 10-09 | 90 | -6 | -5 | -3 | +0 | -3 | -1 | -3 | -1 | -4 | -2 | -1 | -3 |
| 10-10 | 89 | -6 | -5 | -4 | -1 | -3 | +1 | -2 | -1 | -5 | -3 | +1 | -3 |

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
| 10-09 | 75 | -3 | -2 | -2 | -2 | -1 | +1 | -2 | +0 | -2 | -2 | +1 | +0 |
| 10-10 | 80 | -3 | -2 | -3 | -2 | -1 | +0 | -2 | -1 | -3 | -2 | +0 | -1 |

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
| 10-09 | 15 | -4 | -4 | -5 | -2 | -4 | -4 | -5 | -4 | -5 | -2 | +0 | +0 |
| 10-10 | 98 | -87 | -86 | -90 | -85 | -86 | -86 | -86 | -84 | -88 | -86 | -84 | -83 |

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
| 10-09 | 0.00 | +0.02 | +0.08 | +0.14 | +0.24 | +0.20 | +0.20 | +0.12 | +0.24 | +0.20 | +0.14 | +0.14 | +0.16 |
| 10-10 | 0.00 | +0.77 | +0.21 | +0.32 | +0.36 | +0.28 | +0.32 | +0.11 | +0.16 | +0.35 | +0.21 | +0.15 | +0.31 |

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
| 10-09 | 0.00" (dry) | 34/48/45/41 | 8/17/63/14 | 20/92/96/18 | 28/45/61/41 | 68/74/84/13 | 24h 72% | 24h 100% | 5/14/66/6 |
| 10-10 | 0.00" (dry) | 53/39/43/57 | 26/37/56/40 | 61/100/100/71 | 57/84/78/59 | 71/36/36/77 | 24h 61% | 24h 100% | 30/50/62/34 |

## Today so far (2026-10-11, through 2026-10-11T22:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 84.0 °F, low 77.0 °F, max wind 15 kt, precip 0.34" (17 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 10/18Z | -1.5 | 1.9 | 81 (-3) | 70 (-7) pending | +1.3 | 0.91 | +0.57 |
| RRFS | 10/18Z | -0.4 | 2.6 | 84 (+0) | 69 (-8) pending | +1.0 | 0.03 | -0.31 |
| IFS | 10/12Z | -0.5 | 2.0 | 84 (+0) | 73 (-4) pending | +0.0 | 0.45 | +0.11 |
| GFS | 10/18Z | +1.7 | 1.9 | 84 (+0) | 75 (-2) pending | +1.0 | 0.32 | -0.02 |
| AIFS | 10/12Z | +0.1 | 1.7 | 83 (-1) | 71 (-6) pending | -0.4 | 0.38 | +0.04 |
| GFS_MOS | 10/18Z | +2.7 | 2.7 | 88 (+4) | 75 (-2) pending | +0.9 | — | — |
| NBM | 10/18Z | +0.6 | 1.7 | 85 (+1) | 74 (-3) pending | +1.0 | — | — |
| ENS | 10/06Z | -0.2 | 1.8 | 83 (-1) | 74 (-3) pending | -0.5 | 0.37 | +0.03 |
| AIFS_ENS | 10/12Z | +0.3 | 1.7 | 83 (-1) | 73 (-4) pending | +0.0 | 0.27 | -0.07 |
| GEFS | 10/18Z | +3.5 | 3.5 | 86 (+2) | 78 (+1) | +1.3 | 0.19 | -0.15 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- NWS Area Forecast Discussion (TBW): https://forecast.weather.gov/product.php?site=TBW&issuedby=TBW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
