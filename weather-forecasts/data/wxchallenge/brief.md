# WxChallenge forecast brief: Tampa, FL (KTPA)

- Station: **KTPA**
- Target day: **2026-10-07**, scored over 2026-10-07T06Z to 2026-10-08T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-07T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-06T22:24:09+00:00 (refreshed several times an hour while the forecast job runs)
- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)

## How to use this brief (for AI assistants)

1. Start from the **CONSENSUS** row. It is already bias-corrected and skill-weighted using this period's verification (method below).
2. Check the track-record table: a model with a large, consistent bias (|bias| close to its MAE) is reliably off in that direction. The consensus already removes most of that bias; lean further only if the last few days (recent-errors table) show the bias growing.
3. Use the ensemble percentiles for uncertainty. For **precip**, enter roughly the ensemble **median**, not the mean: points are charged per 0.01" of error, and charged most heavily near zero, so the median minimizes expected points. Check the chance-of-rain table: when the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.
4. Use "Today so far" (the day currently in progress, not the target day) to see which models are handling the current pattern; persistent errors there often carry into tomorrow.
5. Give whole °F for high/low, whole kt for wind, and precip to 0.01". State the reasoning for any departure from the consensus.

## Scoring (error points; lower is better)

- High and low temperature: 1 point per °F of error.
- Max sustained wind: 0.5 point per kt of error.
- Precipitation: per 0.01" between forecast and observed: 0.4 pt for amounts 0.00 to 0.10", 0.3 for 0.11 to 0.25", 0.2 for 0.26 to 0.50", 0.1 above 0.50". A trace counts as 0.00.
- Forecasts are rounded as submitted (whole °F and kt, 0.01") before scoring.

## Guidance for the target day

Run = day/hour (UTC) of the model initialization.

| Model | Run | High °F | Low °F | Wind kt | Precip in |
| --- | --- | --: | --: | --: | --: |
| HRRR | 06/18Z | 81.1 | 71.9 | 10.1 | 1.39 |
| RRFS | 06/18Z | 78.5 | 71.4 | 9.0 | 1.46 |
| IFS | 06/12Z | 83.3 | 74.3 | 7.8 | 0.58 |
| GFS | 06/12Z | 79.8 | 72.1 | 10.6 | 1.61 |
| AIFS | 06/12Z | 80.0 | 75.4 | 5.0 | 1.83 |
| GFS_MOS | 06/12Z | 84.0 | 74.0 | 7.0 | 3.42 |
| NBM | 06/18Z | 81.0 | 74.0 | 8.0 | 1.04 |
| USL | 06/12Z | 83.0 | 76.0 | 11.0 | 0.62 |
| ENS | 06/06Z | 81.2 | 73.9 | 7.8 | 0.82 |
| AIFS_ENS | 06/12Z | 80.3 | 74.3 | 7.8 | 1.66 |
| GEFS | 06/12Z | 78.8 | 74.7 | 12.1 | 1.15 |
| HRRRCAST (precip only) | 06/12Z | — | — | — | 2.35 |
| REFS (precip only) | 06/18Z | — | — | — | 1.44 |
| NBM_QMD (precip only) | 06/12Z | — | — | — | 2.37 |
| **CONSENSUS** |  | **81.5** | **75.0** | **11.7** | **1.40** |

Notes:
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [2, 4, 5, 5] -> midpoints
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

- High °F weights: AIFS_ENS 0.17, NBM 0.13, USL 0.11, AIFS 0.11, GFS 0.09, ENS 0.09, GFS_MOS 0.09, HRRR 0.08, IFS 0.08, RRFS 0.05
- Low °F weights: AIFS 0.15, USL 0.14, GFS_MOS 0.14, NBM 0.11, GFS 0.10, IFS 0.09, AIFS_ENS 0.09, ENS 0.07, HRRR 0.06, RRFS 0.06
- Wind kt weights: USL 0.24, GFS 0.11, HRRR 0.10, AIFS_ENS 0.09, ENS 0.09, NBM 0.08, GFS_MOS 0.08, RRFS 0.07, IFS 0.07, AIFS 0.07
- Precip in weights: RRFS 0.11, NBM 0.11, USL 0.10, HRRR 0.10, IFS 0.10, ENS 0.10, AIFS_ENS 0.10, AIFS 0.10, GFS 0.10, GFS_MOS 0.08

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 78.5 | 79.7 | 80.9 | 83.0 | 84.7 | 81.2 |
| ENS | 51 | Low °F | 73.0 | 73.3 | 73.8 | 74.5 | 75.2 | 73.9 |
| ENS | 51 | Wind kt | 5.8 | 6.1 | 7.3 | 9.1 | 10.7 | 7.8 |
| ENS | 51 | Precip in | 0.16 | 0.40 | 0.85 | 1.02 | 1.51 | 0.82 |
| AIFS_ENS | 51 | High °F | 78.3 | 79.3 | 80.2 | 81.2 | 82.8 | 80.3 |
| AIFS_ENS | 51 | Low °F | 73.2 | 73.8 | 74.3 | 74.9 | 75.3 | 74.3 |
| AIFS_ENS | 51 | Wind kt | 5.3 | 6.8 | 7.7 | 8.7 | 10.3 | 7.8 |
| AIFS_ENS | 51 | Precip in | 0.79 | 1.00 | 1.46 | 2.22 | 2.83 | 1.66 |
| GEFS | 31 | High °F | 76.5 | 77.0 | 77.7 | 80.2 | 81.9 | 78.8 |
| GEFS | 31 | Low °F | 73.2 | 73.9 | 75.0 | 75.7 | 75.9 | 74.7 |
| GEFS | 31 | Wind kt | 9.3 | 10.7 | 11.9 | 13.3 | 14.4 | 12.1 |
| GEFS | 31 | Precip in | 0.54 | 0.73 | 1.08 | 1.51 | 1.88 | 1.15 |
| HRRRCAST | 18 | Precip in | 1.60 | 1.85 | 2.35 | 3.17 | 4.29 | 2.67 |
| REFS | 14 | Precip in | 0.89 | 1.00 | 1.44 | 2.29 | 3.21 | 1.79 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 94% | 86% | 71% |
| AIFS_ENS | 100% | 100% | 100% | 96% |
| GEFS | 100% | 100% | 100% | 90% |
| HRRRCAST | 100% | 100% | 100% | 100% |
| REFS | 100% | 100% | 100% | 93% |

NBM QMD calibrated 24-h precip percentiles: p10 0.23", p25 1.08", p50 2.37", p75 2.94", p90 3.56"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 60% | 84% | 87% | 93% | 93% to 100% | 0.28 (12) |
| NBM | NBS P06 | 73% | 79% | 74% | 42% | 79% to 99% | 0.12 (12) |
| ENS | member fraction | 90% | 96% | 92% | 76% | 100% | 0.32 (12) |
| AIFS_ENS | member fraction | 98% | 100% | 98% | 88% | 100% | 0.36 (12) |
| GEFS | member fraction | 84% | 100% | 100% | 87% | 100% | 0.40 (12) |
| HRRRCAST | member fraction | 100% | 100% | 100% | 100% | 100% | 0.24 (12) |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 61% | 81% | 91% | 55% | 98% | 0.10 (12) |

For reference, always forecasting the period's observed frequency (8% of 6-h blocks wet) scores Brier 0.08.

## Track record this period

Since 2026-09-16 at KTPA (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-09-29 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| USL | 9 | 7.6 | +0.7 | -0.8 | -1.1 | +0.17 | 1.5 | 1.2 | 1.1 | 0.17 |
| CONSENSUS | 20 | 8.3 | -0.2 | -0.7 | -1.0 | +0.04 | 1.3 | 1.2 | 2.3 | 0.19 |
| NBM | 20 | 8.9 | +0.1 | -1.0 | -4.5 | +0.00 | 1.2 | 1.6 | 4.5 | 0.16 |
| GFS | 20 | 10.1 | +0.1 | +0.6 | -3.0 | +0.04 | 1.9 | 1.9 | 3.2 | 0.24 |
| AIFS | 20 | 10.7 | -1.1 | -0.9 | -5.6 | +0.06 | 1.6 | 1.0 | 5.6 | 0.22 |
| HRRR | 20 | 11.1 | -1.9 | -3.1 | -2.3 | +0.06 | 2.1 | 3.1 | 3.4 | 0.18 |
| AIFS_ENS | 6 | 11.4 | +0.1 | -2.2 | -3.8 | +0.06 | 0.8 | 2.2 | 3.8 | 0.21 |
| GFS_MOS | 20 | 11.6 | +2.0 | +0.5 | -4.6 | +0.19 | 2.1 | 1.2 | 4.6 | 0.35 |
| IFS | 20 | 11.8 | -0.4 | -1.9 | -5.2 | +0.00 | 2.2 | 2.2 | 5.2 | 0.19 |
| GEFS | 3 | 12.5 | -1.9 | +0.7 | +0.3 | +0.26 | 2.6 | 0.7 | 1.7 | 0.26 |
| ENS | 6 | 12.6 | -1.9 | -2.9 | -3.9 | +0.11 | 1.9 | 2.9 | 3.9 | 0.19 |
| RRFS | 20 | 14.1 | -3.9 | -3.5 | -4.8 | -0.03 | 3.9 | 3.5 | 4.8 | 0.15 |

## Recent days (last 8 verified)

Observed (~ = still preliminary):

| Date | High °F | Low °F | Wind kt | Precip in |
| --- | --: | --: | --: | --: |
| 2026-09-28 (hindcast) | 85 | 70 | 10 | 0.00 |
| 2026-09-29 | 87 | 74 | 10 | 0.00 |
| 2026-09-30 | 88 | 75 | 14 | 0.42 |
| 2026-10-01 | 88 | 74 | 14 | 0.28 |
| 2026-10-02 | 87 | 77 | 10 | 0.00 |
| 2026-10-03 | 90 | 80 | 11 | 0.00 |
| 2026-10-04 | 89 | 79 | 9 | 0.01 |
| 2026-10-05 | 88 | 78 | 11 | 0.00 |

Errors as forecast - observed, high/low/wind/precip:

| Model | 09-28 | 09-29 | 09-30 | 10-01 | 10-02 | 10-03 | 10-04 | 10-05 |
| --- | --: | --: | --: | --: | --: | --: | --: | --: |
| HRRR | +1/-1/-4/+0.00 | -1/-5/+0/+0.00 | +0/-3/-3/+0.25 | -3/-2/-4/+0.41 | -4/-5/+0/+0.04 | -1/-4/+2/+0.12 | -2/-4/-1/+0.00 | +0/-3/+1/+0.11 |
| RRFS | -2/-3/-4/+0.00 | -2/-4/-5/+0.00 | -3/-3/-7/-0.18 | -7/-2/-4/-0.15 | -2/-4/-2/+0.15 | -6/-8/-1/+0.30 | -2/-5/-2/+0.00 | -3/-4/-6/+0.13 |
| IFS | +7/+3/-4/+0.00 | +3/-2/-1/+0.21 | -1/-4/-6/-0.41 | +0/+0/-5/+0.18 | +0/-2/-1/+0.51 | -5/-4/-4/+0.09 | -1/-4/-2/+0.10 | -1/-4/-6/+0.07 |
| GFS | +0/+4/-3/+0.00 | -1/+2/-2/+0.00 | -2/-2/-5/-0.38 | +2/+2/-1/-0.08 | +4/-1/+1/+0.37 | -5/-3/-2/+0.36 | +1/-1/+0/+0.19 | -3/-1/-4/+0.76 |
| AIFS | +2/+0/-5/+0.01 | -4/-1/-5/+0.18 | -1/-1/-7/-0.30 | +0/+0/-5/-0.01 | +0/-1/-2/+0.39 | -3/-3/-4/+0.45 | +1/-2/-2/+0.16 | -1/-2/-6/+0.39 |
| GFS_MOS | +3/-1/-2/+0.00 | +1/-1/-1/+0.00 | +2/-1/-7/-0.20 | +2/+1/-6/+0.52 | +4/+1/-2/+1.22 | -1/-2/-3/+0.44 | +2/+0/-1/+0.33 | +1/+0/-5/+1.02 |
| NBM | +3/+0/-3/+0.00 | +1/-2/-3/+0.02 | +0/-3/-7/-0.24 | +0/+1/-3/-0.15 | +1/-1/-1/+0.36 | -3/-4/-3/+0.23 | +0/-3/-2/+0.08 | -1/-2/-5/+0.13 |
| USL | +3/+0/+0/+0.00 | +0/-1/+0/+0.00 | +1/-1/-4/+0.07 | +1/+1/-2/+0.06 | +2/+0/-1/+0.10 | -2/-3/-2/+0.41 | +1/-2/+0/+0.48 | -1/-1/-1/+0.25 |
| ENS | — | — | -2/-3/-8/-0.23 | +0/+0/-4/-0.06 | -1/-2/-2/+0.33 | -4/-5/-3/+0.32 | -2/-4/-2/+0.15 | -2/-3/-5/+0.09 |
| AIFS_ENS | — | — | +0/-3/-7/-0.36 | +1/+0/-5/-0.13 | +1/-1/-1/+0.19 | -2/-4/-3/+0.21 | +1/-3/-2/+0.07 | +0/-2/-5/+0.29 |
| GEFS | — | — | — | — | — | -5/+0/+1/+0.30 | +1/+1/+2/+0.16 | -2/+1/-2/+0.31 |
| CONSENSUS | +3/+1/+1/+0.00 | -1/-2/+1/+0.05 | -1/-2/-3/-0.20 | +0/+0/-2/+0.06 | +1/-1/+1/+0.36 | -3/-3/+1/+0.30 | +0/-2/+2/+0.16 | -1/-1/-1/+0.32 |

Error points per day:

| Model | 09-28 | 09-29 | 09-30 | 10-01 | 10-02 | 10-03 | 10-04 | 10-05 |
| --- | --: | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 4.0 | 6.0 | 7.8 | 13.3 | 10.6 | 10.6 | 6.5 | 7.8 |
| RRFS | 7.0 | 8.5 | 13.2 | 15.2 | 12.5 | 24.0 | 8.0 | 14.9 |
| IFS | 12.0 | 12.8 | 19.5 | 6.1 | 16.1 | 14.6 | 9.9 | 10.8 |
| GFS | 5.5 | 4.0 | 16.8 | 6.6 | 16.4 | 19.7 | 8.6 | 22.1 |
| AIFS | 4.9 | 13.9 | 12.8 | 2.7 | 13.3 | 20.5 | 9.7 | 17.3 |
| GFS_MOS | 5.0 | 2.5 | 10.8 | 13.4 | 26.7 | 16.8 | 12.4 | 22.2 |
| NBM | 4.5 | 5.3 | 12.0 | 6.7 | 13.2 | 16.4 | 7.2 | 10.4 |
| USL | 3.0 | 1.0 | 5.4 | 4.2 | 6.5 | 17.7 | 15.9 | 11.0 |
| ENS | — | — | 14.2 | 3.5 | 14.1 | 20.4 | 12.4 | 11.1 |
| AIFS_ENS | — | — | 16.0 | 7.1 | 9.2 | 14.8 | 7.8 | 13.8 |
| GEFS | — | — | — | — | — | 15.0 | 8.7 | 13.7 |
| CONSENSUS | 4.5 | 5.5 | 8.8 | 2.2 | 13.2 | 16.0 | 8.7 | 12.4 |

## Today so far (2026-10-06, through 2026-10-06T21:53Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 79.0 °F, low 75.9 °F, max wind 5 kt, precip 0.92" (16 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 05/18Z | -0.5 | 1.4 | 81 (+2) | 73 (-3) pending | +1.4 | 0.99 | +0.07 |
| RRFS | 05/18Z | +0.8 | 2.5 | 82 (+3) | 74 (-2) pending | -0.2 | 0.07 | -0.85 |
| IFS | 05/12Z | +1.1 | 2.5 | 84 (+4) | 75 (-1) | -0.8 | 0.10 | -0.82 |
| GFS | 05/18Z | +3.0 | 3.0 | 87 (+8) | 75 (-1) pending | -0.2 | 0.46 | -0.46 |
| AIFS | 05/12Z | +0.7 | 1.3 | 82 (+2) | 76 (+0) pending | -0.6 | 0.60 | -0.32 |
| GFS_MOS | 05/18Z | +2.8 | 2.8 | 86 (+7) | 77 (+1) | +0.5 | — | — |
| NBM | 05/18Z | +1.2 | 1.9 | 84 (+5) | 75 (-1) pending | +1.3 | — | — |
| ENS | 04/18Z | +0.6 | 2.1 | 82 (+4) | 74 (-2) | +0.0 | 0.32 | -0.60 |
| AIFS_ENS | 05/00Z | +1.1 | 1.6 | 82 (+3) | 75 (-1) pending | +0.5 | 0.55 | -0.37 |
| GEFS | 05/18Z | +4.3 | 4.3 | 86 (+7) | 77 (+1) | +1.8 | 0.50 | -0.42 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
