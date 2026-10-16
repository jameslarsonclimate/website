# WxChallenge forecast brief: Olympia, WA (KOLM)

- Station: **KOLM**
- Target day: **2026-10-17**, scored over 2026-10-17T06Z to 2026-10-18T06Z (UTC, 06Z to 06Z)
- Submission deadline: 2026-10-17T00Z (forecasts for a day are due at 00Z that day)
- Generated: 2026-10-16T01:04:56+00:00 (refreshed several times an hour while the forecast job runs)
- Units: temperature °F, wind kt (max sustained), precipitation inches (liquid)

## How to use this brief (for AI assistants)

1. Start from the **CONSENSUS** row. It is already bias-corrected and skill-weighted using this period's verification (method below).
2. Check the track-record table: a model with a large, consistent bias (|bias| close to its MAE) is reliably off in that direction. The consensus already removes most of that bias; lean further only if the last few days (daily verification tables) show the bias growing.
3. Use the ensemble percentiles for uncertainty. For **precip**, enter roughly the ensemble **median**, not the mean: points are charged per 0.01" of error, and charged most heavily near zero, so the median minimizes expected points. Check the chance-of-rain table: when the calibrated chances (NBM, NBM QMD, MOS) are low, 0.00 is often the best entry.
4. Use "Today so far" (the day currently in progress, not the target day) to see which models are handling the current pattern; persistent errors there often carry into tomorrow.
5. Check the clouds section: when a model's low or high misses line up with its cloud misses (too clear at night -> low too cold, too cloudy at night -> low too warm; too clear by day -> high too warm, too cloudy by day -> high too cool), ask whether its cloud forecast for the target day has the same problem before trusting its temperatures.
6. Read the latest AFD for the forecaster's view of the pattern; it often explains when a model bias learned earlier in the period won't apply.
7. Give whole °F for high/low, whole kt for wind, and precip to 0.01". State the reasoning for any departure from the consensus.

## Scoring (error points; lower is better)

- High and low temperature: 1 point per °F of error.
- Max sustained wind: 0.5 point per kt of error.
- Precipitation: per 0.01" between forecast and observed: 0.4 pt for amounts 0.00 to 0.10", 0.3 for 0.11 to 0.25", 0.2 for 0.26 to 0.50", 0.1 above 0.50". A trace counts as 0.00.
- Forecasts are rounded as submitted (whole °F and kt, 0.01") before scoring.

## Guidance for the target day

Run = day/hour (UTC) of the model initialization.

| Model | Run | High °F | Low °F | Wind kt | Precip in |
| --- | --- | --: | --: | --: | --: |
| HRRR | 15/18Z | 59.3 | 52.6 | 7.9 | 0.01 |
| RRFS | 15/18Z | 64.1 | 48.1 | 8.4 | 0.02 |
| IFS | 15/12Z | 62.3 | 49.0 | 7.0 | 0.06 |
| GFS | 15/18Z | 63.6 | 44.0 | 7.5 | 0.04 |
| AIFS | 15/18Z | 62.1 | 46.6 | 8.0 | 0.07 |
| GFS_MOS | 15/18Z | 64.0 | 43.0 | 9.0 | 0.10 |
| NBM | 15/18Z | 65.0 | 43.0 | 9.0 | 0.01 |
| USL | — | — | — | — | — |
| ENS | 15/12Z | 63.2 | 49.3 | 7.7 | 0.08 |
| AIFS_ENS | 15/12Z | 62.0 | 48.0 | 8.5 | 0.06 |
| GEFS | 15/18Z | 64.3 | 44.4 | 7.2 | 0.05 |
| HRRRCAST (precip only) | — | — | — | — | — |
| REFS (precip only) | 15/18Z | — | — | — | 0.03 |
| NBM_QMD (precip only) | 15/12Z | — | — | — | 0.02 |
| **CONSENSUS** |  | **63.2** | **43.0** | **11.0** | **0.05** |

Notes:
- HRRR: 18Z HRRR stops at f48: window truncated
- AIFS: 6-hourly output: high/low likely underdone
- GFS_MOS: MOS Q06 categories [1, 1, 0, 0] -> midpoints
- NBM: NBS Q06 amounts
- USL: failed this run (no USL run for 2026-10-17 available at 2026-10-16 01Z)
- ENS: ensemble mean of 51 members (Open-Meteo)
- AIFS_ENS: ensemble mean of 51 members (Open-Meteo)
- GEFS: ensemble mean of 31 members (Open-Meteo); not in the consensus
- HRRRCAST: failed this run (no complete 00/06/12/18Z HRRRCast cycle covering the day yet)
- REFS: median of 7 members, 18Z + 12Z runs (RRFS para)
- NBM_QMD: calibrated PoP and percentiles (NBM QMD); precip = 50% level

GEFS is shown but not used in the consensus. Precip-only ensembles (REFS, HRRRCAST) and NBM QMD are not in the consensus either; they inform the precip choice.

## Consensus method

- High, Wind, Precip: bias-corrected (n_eff/(n_eff+3) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Low: bias-corrected (n_eff/(n_eff+1) of each model's decay-weighted mean error), 1/(MAE+0.5) weighted.
- Precip is weighted but not bias-corrected.

- High °F weights: NBM 0.18, AIFS_ENS 0.15, HRRR 0.11, AIFS 0.11, RRFS 0.10, GFS_MOS 0.10, IFS 0.09, ENS 0.09, GFS 0.08 (using parent's track record: ENS from IFS)
- Low °F weights: GFS_MOS 0.18, NBM 0.15, AIFS_ENS 0.11, HRRR 0.11, GFS 0.10, AIFS 0.10, IFS 0.08, ENS 0.08, RRFS 0.08 (using parent's track record: ENS from IFS)
- Wind kt weights: RRFS 0.15, HRRR 0.13, AIFS_ENS 0.12, GFS_MOS 0.12, NBM 0.11, IFS 0.10, ENS 0.10, GFS 0.09, AIFS 0.09 (using parent's track record: ENS from IFS)
- Precip in weights: GFS 0.11, GFS_MOS 0.11, HRRR 0.11, RRFS 0.11, AIFS 0.11, NBM 0.11, AIFS_ENS 0.11, IFS 0.11, ENS 0.11 (using parent's track record: ENS from IFS)

## Ensemble spread (target day)

| Ensemble | Members | Variable | p10 | p25 | Median | p75 | p90 | Mean |
| --- | --- | --- | --: | --: | --: | --: | --: | --: |
| ENS | 51 | High °F | 62.4 | 62.7 | 63.2 | 63.7 | 64.2 | 63.2 |
| ENS | 51 | Low °F | 47.2 | 48.5 | 49.7 | 50.6 | 51.1 | 49.3 |
| ENS | 51 | Wind kt | 6.7 | 7.0 | 7.6 | 8.3 | 8.8 | 7.7 |
| ENS | 51 | Precip in | 0.04 | 0.05 | 0.07 | 0.11 | 0.16 | 0.08 |
| AIFS_ENS | 51 | High °F | 60.6 | 61.2 | 62.1 | 63.0 | 63.3 | 62.0 |
| AIFS_ENS | 51 | Low °F | 45.0 | 46.4 | 48.0 | 49.6 | 51.1 | 48.0 |
| AIFS_ENS | 51 | Wind kt | 6.8 | 7.2 | 8.3 | 9.3 | 10.8 | 8.5 |
| AIFS_ENS | 51 | Precip in | 0.02 | 0.02 | 0.05 | 0.10 | 0.12 | 0.06 |
| GEFS | 31 | High °F | 62.3 | 63.3 | 64.4 | 65.3 | 66.2 | 64.3 |
| GEFS | 31 | Low °F | 43.0 | 43.5 | 44.4 | 45.1 | 45.8 | 44.4 |
| GEFS | 31 | Wind kt | 5.8 | 6.5 | 7.4 | 7.8 | 8.0 | 7.2 |
| GEFS | 31 | Precip in | 0.01 | 0.02 | 0.04 | 0.06 | 0.07 | 0.05 |
| REFS | 7 | Precip in | 0.02 | 0.02 | 0.03 | 0.04 | 0.05 | 0.03 |

Share of members reaching each 24-h precip amount:

| Ensemble | ≥0.01" | ≥0.10" | ≥0.25" | ≥0.50" |
| --- | --: | --: | --: | --: |
| ENS | 100% | 29% | 0% | 0% |
| AIFS_ENS | 96% | 14% | 0% | 0% |
| GEFS | 100% | 6% | 0% | 0% |
| REFS | 100% | 0% | 0% | 0% |

NBM QMD calibrated 24-h precip percentiles: p10 0.00", p25 0.00", p50 0.02", p75 0.06", p90 0.15"

## Chance of measurable precip (≥0.01") on the target day

6-hour blocks in UTC. Brier 6h = this period's Brier score of the 6-hour chances (lower is better; number of blocks verified in brackets).

| Source | Basis | 06-12 | 12-18 | 18-00 | 00-06 | 24 h | Brier 6h (n) |
| --- | --- | --: | --: | --: | --: | --: | --: |
| GFS_MOS | GFS MOS P06 | 54% | 51% | 19% | 2% | 54% to 82% | 0.01 (8) |
| NBM | NBS P06 | 43% | 35% | 2% | 0% | 43% to 64% | 0.01 (8) |
| ENS | member fraction | 100% | 88% | 0% | 0% | 100% | 0.02 (8) |
| AIFS_ENS | member fraction | 82% | 45% | 2% | 4% | 96% | 0.02 (8) |
| GEFS | member fraction | 87% | 61% | 3% | 0% | 100% | 0.01 (8) |
| REFS | member fraction | — | — | — | — | 100% | — |
| NBM_QMD | NBM QMD | 53% | 28% | 1% | 0% | 70% | 0.00 (8) |

For reference, always forecasting the period's observed frequency (0% of 6-h blocks wet) scores Brier 0.00.

## Hourly guidance through the target day

Each model's values at each valid time (UTC; local time alongside). HRRR, RRFS, USL and the ensembles are hourly, IFS, GFS, GFS_MOS and NBM 3-hourly, AIFS 6-hourly; ENS, AIFS_ENS and GEFS are ensemble means. Blank = no value at that hour. Hourly temperatures can miss the true high/low between output times; the guidance table's daily values (which also use interval max/min fields where available) are what get scored.

Cloud cover (context, not scored): total cloud cover from each model's own output; GFS_MOS gives categories (clear 0, few 19, scattered 44, broken 75, overcast 100) and the ensembles none. * = averaged over the preceding interval rather than instantaneous. Clouds overnight hold the low up; clouds by day hold the high down.

Temperature (°F):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 54.0 | 52.8 | 53.5 | 52.8 | 52.9 | 54.0 | 52.0 | 54.1 | 54.8 | 52.9 |
| 10-17 07Z | Sat 00:00 | 55.8 | 51.9 |  |  |  |  |  | 54.0 | 53.9 | 53.1 |
| 10-17 08Z | Sat 01:00 | 55.7 | 51.9 |  |  |  |  |  | 54.3 | 53.8 | 53.9 |
| 10-17 09Z | Sat 02:00 | 55.3 | 52.5 | 53.9 | 55.0 |  | 53.0 | 52.0 | 54.5 | 54.3 | 54.5 |
| 10-17 10Z | Sat 03:00 | 55.5 | 54.1 |  |  |  |  |  | 54.9 | 55.0 | 54.7 |
| 10-17 11Z | Sat 04:00 | 55.1 | 54.3 |  |  |  |  |  | 55.2 | 55.8 | 54.8 |
| 10-17 12Z | Sat 05:00 | 53.7 | 54.5 | 54.3 | 54.7 | 55.3 | 52.0 | 54.0 | 55.4 | 56.4 | 54.6 |
| 10-17 13Z | Sat 06:00 | 52.8 | 54.6 |  |  |  |  |  | 55.0 | 56.8 | 53.8 |
| 10-17 14Z | Sat 07:00 | 52.6 | 55.4 |  |  |  |  |  | 54.3 | 57.4 | 52.7 |
| 10-17 15Z | Sat 08:00 | 52.8 | 55.4 | 53.5 | 52.8 |  | 54.0 | 54.0 | 54.3 | 57.9 | 52.5 |
| 10-17 16Z | Sat 09:00 | 55.1 | 57.2 |  |  |  |  |  | 55.3 | 58.5 | 53.9 |
| 10-17 17Z | Sat 10:00 | 57.7 | 58.8 |  |  |  |  |  | 57.0 | 59.1 | 56.1 |
| 10-17 18Z | Sat 11:00 | 59.3 | 60.7 | 57.6 | 57.7 | 59.0 | 58.0 | 57.0 | 58.6 | 59.5 | 58.3 |
| 10-17 19Z | Sat 12:00 |  | 61.5 |  |  |  |  |  | 60.3 | 60.1 | 60.5 |
| 10-17 20Z | Sat 13:00 |  | 62.6 |  |  |  |  |  | 62.1 | 60.8 | 62.7 |
| 10-17 21Z | Sat 14:00 |  | 63.5 | 62.1 | 63.5 |  | 62.0 | 62.0 | 63.1 | 61.5 | 64.1 |
| 10-17 22Z | Sat 15:00 |  | 64.0 |  |  |  |  |  | 63.1 | 61.9 | 64.2 |
| 10-17 23Z | Sat 16:00 |  | 63.7 |  |  |  |  |  | 62.4 | 61.9 | 63.5 |
| 10-18 00Z | Sat 17:00 |  | 62.5 | 60.2 | 60.8 | 62.1 | 61.0 | 63.0 | 60.9 | 61.4 | 61.7 |
| 10-18 01Z | Sat 18:00 |  | 59.3 |  |  |  |  |  | 58.2 | 59.9 | 58.0 |
| 10-18 02Z | Sat 19:00 |  | 55.8 |  |  |  |  |  | 54.7 | 57.8 | 53.3 |
| 10-18 03Z | Sat 20:00 |  | 53.2 | 51.2 | 47.4 |  | 51.0 | 49.0 | 51.9 | 55.2 | 49.3 |
| 10-18 04Z | Sat 21:00 |  | 51.3 |  |  |  |  |  | 50.5 | 52.5 | 47.0 |
| 10-18 05Z | Sat 22:00 |  | 49.6 |  |  |  |  |  | 50.0 | 50.0 | 45.5 |
| 10-18 06Z | Sat 23:00 |  | 48.1 | 49.3 | 44.7 | 46.6 | 43.0 | 43.0 | 49.4 | 48.0 | 44.4 |

Wind speed (kt) at the hour:

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 7.3 | 3.6 | 6.3 | 4.2 | 6.4 | 3.0 | 6.0 | 5.6 | 6.5 | 4.3 |
| 10-17 07Z | Sat 00:00 | 7.4 | 6.4 |  |  |  |  |  | 5.7 | 6.7 | 4.6 |
| 10-17 08Z | Sat 01:00 | 7.3 | 8.4 |  |  |  |  |  | 6.0 | 6.8 | 4.8 |
| 10-17 09Z | Sat 02:00 | 7.1 | 7.2 | 6.3 | 4.7 |  | 4.0 | 7.0 | 6.3 | 6.9 | 5.1 |
| 10-17 10Z | Sat 03:00 | 6.9 | 7.7 |  |  |  |  |  | 6.4 | 6.9 | 5.3 |
| 10-17 11Z | Sat 04:00 | 6.5 | 8.0 |  |  |  |  |  | 6.5 | 6.9 | 5.4 |
| 10-17 12Z | Sat 05:00 | 5.7 | 6.5 | 5.8 | 4.8 | 8.0 | 6.0 | 8.0 | 6.4 | 6.9 | 5.5 |
| 10-17 13Z | Sat 06:00 | 5.6 | 5.4 |  |  |  |  |  | 6.1 | 6.8 | 5.3 |
| 10-17 14Z | Sat 07:00 | 6.1 | 5.3 |  |  |  |  |  | 5.7 | 6.8 | 5.1 |
| 10-17 15Z | Sat 08:00 | 6.6 | 4.1 | 5.8 | 4.3 |  | 6.0 | 8.0 | 5.6 | 6.9 | 5.0 |
| 10-17 16Z | Sat 09:00 | 6.6 | 5.4 |  |  |  |  |  | 5.8 | 7.2 | 5.1 |
| 10-17 17Z | Sat 10:00 | 7.1 | 6.8 |  |  |  |  |  | 6.2 | 7.4 | 5.4 |
| 10-17 18Z | Sat 11:00 | 7.9 | 6.7 | 7.0 | 7.1 | 7.2 | 6.0 | 9.0 | 6.7 | 7.4 | 5.9 |
| 10-17 19Z | Sat 12:00 |  | 7.6 |  |  |  |  |  | 6.8 | 7.2 | 6.2 |
| 10-17 20Z | Sat 13:00 |  | 7.3 |  |  |  |  |  | 6.8 | 6.7 | 6.5 |
| 10-17 21Z | Sat 14:00 |  | 7.5 | 6.8 | 7.5 |  | 8.0 | 8.0 | 6.7 | 6.2 | 6.6 |
| 10-17 22Z | Sat 15:00 |  | 6.5 |  |  |  |  |  | 6.2 | 5.7 | 6.6 |
| 10-17 23Z | Sat 16:00 |  | 5.9 |  |  |  |  |  | 5.5 | 5.3 | 6.4 |
| 10-18 00Z | Sat 17:00 |  | 6.6 | 3.8 | 6.0 | 5.5 | 9.0 | 6.0 | 4.8 | 5.1 | 6.0 |
| 10-18 01Z | Sat 18:00 |  | 6.6 |  |  |  |  |  | 4.2 | 4.8 | 5.0 |
| 10-18 02Z | Sat 19:00 |  | 3.6 |  |  |  |  |  | 3.6 | 4.4 | 3.8 |
| 10-18 03Z | Sat 20:00 |  | 3.5 | 1.9 | 3.2 |  | 4.0 | 0.0 | 3.3 | 4.0 | 3.0 |
| 10-18 04Z | Sat 21:00 |  | 2.1 |  |  |  |  |  | 2.8 | 3.7 | 2.3 |
| 10-18 05Z | Sat 22:00 |  | 3.3 |  |  |  |  |  | 3.0 | 3.6 | 1.8 |
| 10-18 06Z | Sat 23:00 |  | 2.8 | 3.6 | 1.5 | 2.4 | 2.0 | 0.0 | 3.4 | 3.5 | 1.4 |

Precipitation (in), accumulated since the start of the day (06Z):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | ENS | AIFS_ENS | GEFS |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10-17 07Z | Sat 00:00 | 0.00 | 0.00 |  |  |  | 0.00 | 0.01 | 0.01 |
| 10-17 08Z | Sat 01:00 | 0.01 | 0.00 |  |  |  | 0.01 | 0.01 | 0.01 |
| 10-17 09Z | Sat 02:00 | 0.01 | 0.00 | 0.00 | 0.01 |  | 0.01 | 0.02 | 0.01 |
| 10-17 10Z | Sat 03:00 | 0.01 | 0.00 |  |  |  | 0.03 | 0.03 | 0.02 |
| 10-17 11Z | Sat 04:00 | 0.01 | 0.01 |  |  |  | 0.05 | 0.04 | 0.03 |
| 10-17 12Z | Sat 05:00 | 0.01 | 0.01 | 0.04 | 0.04 | 0.06 | 0.07 | 0.04 | 0.03 |
| 10-17 13Z | Sat 06:00 | 0.01 | 0.03 |  |  |  | 0.07 | 0.05 | 0.04 |
| 10-17 14Z | Sat 07:00 | 0.01 | 0.03 |  |  |  | 0.08 | 0.05 | 0.04 |
| 10-17 15Z | Sat 08:00 | 0.01 | 0.03 | 0.06 | 0.04 |  | 0.08 | 0.05 | 0.04 |
| 10-17 16Z | Sat 09:00 | 0.01 | 0.03 |  |  |  | 0.08 | 0.06 | 0.04 |
| 10-17 17Z | Sat 10:00 | 0.01 | 0.03 |  |  |  | 0.08 | 0.06 | 0.04 |
| 10-17 18Z | Sat 11:00 | 0.01 | 0.03 | 0.06 | 0.04 | 0.07 | 0.09 | 0.06 | 0.04 |
| 10-17 19Z | Sat 12:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-17 20Z | Sat 13:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-17 21Z | Sat 14:00 |  | 0.03 | 0.06 | 0.04 |  | 0.09 | 0.06 | 0.04 |
| 10-17 22Z | Sat 15:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-17 23Z | Sat 16:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-18 00Z | Sat 17:00 |  | 0.03 | 0.06 | 0.04 | 0.07 | 0.09 | 0.06 | 0.04 |
| 10-18 01Z | Sat 18:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-18 02Z | Sat 19:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-18 03Z | Sat 20:00 |  | 0.03 | 0.06 | 0.04 |  | 0.09 | 0.06 | 0.04 |
| 10-18 04Z | Sat 21:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-18 05Z | Sat 22:00 |  | 0.03 |  |  |  | 0.09 | 0.06 | 0.04 |
| 10-18 06Z | Sat 23:00 |  | 0.03 | 0.06 | 0.04 | 0.07 | 0.09 | 0.06 | 0.04 |

Total cloud cover (%):

| UTC | Local (PDT) | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| 10-17 06Z | Fri 23:00 | 100 | 45 | 91 | 100 | 95 | 100 | 30 |
| 10-17 07Z | Sat 00:00 | 100 | 51 |  |  |  |  |  |
| 10-17 08Z | Sat 01:00 | 100 | 100 |  |  |  |  |  |
| 10-17 09Z | Sat 02:00 | 100 | 98 | 100 | 100 |  | 100 | 81 |
| 10-17 10Z | Sat 03:00 | 100 | 100 |  |  |  |  |  |
| 10-17 11Z | Sat 04:00 | 98 | 100 |  |  |  |  |  |
| 10-17 12Z | Sat 05:00 | 100 | 100 | 100 | 100 | 97 | 100 | 99 |
| 10-17 13Z | Sat 06:00 | 100 | 100 |  |  |  |  |  |
| 10-17 14Z | Sat 07:00 | 100 | 100 |  |  |  |  |  |
| 10-17 15Z | Sat 08:00 | 100 | 99 | 57 | 100 |  | 100 | 92 |
| 10-17 16Z | Sat 09:00 | 90 | 93 |  |  |  |  |  |
| 10-17 17Z | Sat 10:00 | 100 | 61 |  |  |  |  |  |
| 10-17 18Z | Sat 11:00 | 39 | 12 | 5 | 98 | 26 | 100 | 38 |
| 10-17 19Z | Sat 12:00 |  | 15 |  |  |  |  |  |
| 10-17 20Z | Sat 13:00 |  | 93 |  |  |  |  |  |
| 10-17 21Z | Sat 14:00 |  | 8 | 10 | 2 |  | 44 | 22 |
| 10-17 22Z | Sat 15:00 |  | 13 |  |  |  |  |  |
| 10-17 23Z | Sat 16:00 |  | 17 |  |  |  |  |  |
| 10-18 00Z | Sat 17:00 |  | 75 | 71 | 13 | 56 | 19 | 24 |
| 10-18 01Z | Sat 18:00 |  | 100 |  |  |  |  |  |
| 10-18 02Z | Sat 19:00 |  | 69 |  |  |  |  |  |
| 10-18 03Z | Sat 20:00 |  | 0 | 35 | 2 |  | 19 | 29 |
| 10-18 04Z | Sat 21:00 |  | 0 |  |  |  |  |  |
| 10-18 05Z | Sat 22:00 |  | 1 |  |  |  |  |  |
| 10-18 06Z | Sat 23:00 |  | 0 | 2 | 30 | 15 | 44 | 17 |

## Track record this period

Since 2026-09-28 at KOLM (forecast - observed, so negative bias = too cold / too light / too dry). Bias and MAE are decay-weighted toward recent days (half-lives: High °F 9 d, Low °F 9 d, Wind kt 18 d, Precip in 12 d). Days before 2026-10-13 are hindcasts (model runs from 23Z the evening before, as they would have been submitted). Sorted best first by mean error points per day.

| Model | Days | Pts/day | Bias high | Bias low | Bias wind | Bias precip | MAE high | MAE low | MAE wind | MAE precip |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| CONSENSUS | 17 | 5.3 | -0.2 | +1.5 | -0.9 | +0.01 | 1.1 | 2.9 | 2.2 | 0.01 |
| NBM | 17 | 6.2 | +0.5 | +1.8 | -3.3 | +0.00 | 0.8 | 3.3 | 3.8 | 0.01 |
| GFS_MOS | 17 | 6.4 | +0.3 | +1.4 | -3.4 | +0.01 | 1.9 | 2.7 | 3.6 | 0.01 |
| USL | 4 | 6.4 | -1.9 | +2.9 | -0.3 | +0.00 | 1.9 | 3.9 | 1.3 | 0.00 |
| AIFS_ENS | 2 | 7.7 | -1.0 | +4.6 | -3.5 | +0.01 | 1.0 | 4.6 | 3.5 | 0.01 |
| HRRR | 17 | 8.3 | +0.8 | +4.0 | -2.7 | -0.01 | 1.6 | 4.7 | 3.0 | 0.01 |
| ENS | 1 | 9.4 | +0.0 | +7.0 | -4.0 | +0.01 | 0.0 | 7.0 | 4.0 | 0.01 |
| RRFS | 17 | 9.6 | -0.1 | +6.4 | -2.6 | +0.01 | 1.7 | 6.5 | 2.7 | 0.01 |
| AIFS | 17 | 9.6 | -1.3 | +4.9 | -4.8 | +0.01 | 1.6 | 5.4 | 5.1 | 0.01 |
| GFS | 17 | 9.9 | +0.5 | +4.3 | -4.5 | +0.01 | 2.4 | 5.0 | 4.7 | 0.01 |
| GEFS | 2 | 10.4 | -1.9 | +5.0 | -4.5 | +0.01 | 2.9 | 5.0 | 4.5 | 0.01 |
| IFS | 17 | 10.6 | -1.9 | +6.1 | -4.1 | +0.01 | 2.0 | 6.3 | 4.2 | 0.01 |

## Daily verification (all 17 days this period)

One row per day; "h" = hindcast day (before the first forecast day for this city). On hindcast days the CONSENSUS is reconstructed: what the current method would have submitted using only the earlier days' track record.

Error points (lower is better):

| Date | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS | Best |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 12.0 | 11.5 | 14.0 | 10.0 | 12.0 | 5.5 | 8.5 | — | — | — | — | 9.0 | GFS_MOS |
| 09-29 h | 11.5 | 10.0 | 11.1 | 13.4 | 5.6 | 4.8 | 10.8 | — | — | — | — | 6.3 | GFS_MOS |
| 09-30 h | 7.5 | 6.0 | 6.0 | 5.5 | 7.0 | 6.0 | 5.5 | — | — | — | — | 4.0 | CONSENSUS |
| 10-01 h | 6.0 | 7.0 | 8.0 | 5.5 | 8.0 | 1.5 | 2.0 | — | — | — | — | 1.0 | CONSENSUS |
| 10-02 h | 9.0 | 10.0 | 11.5 | 8.5 | 10.0 | 6.5 | 3.5 | — | — | — | — | 5.0 | NBM |
| 10-03 h | 10.5 | 10.5 | 10.0 | 13.5 | 10.5 | 9.5 | 8.0 | — | — | — | — | 7.5 | CONSENSUS |
| 10-04 h | 11.0 | 12.5 | 10.0 | 15.0 | 8.0 | 4.0 | 8.5 | — | — | — | — | 5.0 | GFS_MOS |
| 10-05 h | 2.5 | 10.0 | 11.5 | 6.5 | 7.5 | 1.0 | 4.0 | — | — | — | — | 2.0 | GFS_MOS |
| 10-06 h | 3.5 | 8.5 | 8.5 | 9.0 | 4.5 | 5.0 | 4.5 | — | — | — | — | 3.0 | CONSENSUS |
| 10-07 h | 10.5 | 7.0 | 6.0 | 14.0 | 8.5 | 16.0 | 10.0 | — | — | — | — | 10.5 | IFS |
| 10-08 h | 4.5 | 4.5 | 8.5 | 9.5 | 7.0 | 3.5 | 2.0 | — | — | — | — | 4.5 | NBM |
| 10-09 h | 12.7 | 11.9 | 16.0 | 10.5 | 19.2 | 12.0 | 8.3 | — | — | — | — | 9.1 | NBM |
| 10-10 h | 7.5 | 10.0 | 9.4 | 7.8 | 12.8 | 9.0 | 2.5 | — | — | — | — | 4.4 | NBM |
| 10-11 h | 12.0 | 12.0 | 16.0 | 11.5 | 16.0 | 8.5 | 10.0 | 6.5 | — | — | — | 6.5 | USL |
| 10-12 h | 11.0 | 12.0 | 16.5 | 9.0 | 12.5 | 7.5 | 10.5 | 5.5 | — | — | — | 7.0 | USL |
| 10-13 | 2.0 | 7.4 | 7.0 | 10.5 | 5.0 | 3.5 | 3.5 | 5.5 | — | 5.5 | 10.5 | 4.5 | HRRR |
| 10-14 | 7.0 | 11.5 | 9.9 | 8.5 | 8.8 | 4.5 | 4.0 | 8.0 | 9.4 | 9.8 | 10.4 | 0.9 | CONSENSUS |

High °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 67 | -1 | +0 | -2 | +1 | -3 | +1 | +1 | — | — | — | — | +0 |
| 09-29 h | 61 | +0 | -3 | -2 | -4 | +0 | +2 | +0 | — | — | — | — | -1 |
| 09-30 h | 66 | -4 | -2 | -2 | -2 | -2 | -1 | -1 | — | — | — | — | -2 |
| 10-01 h | 71 | +1 | +1 | -4 | +0 | -3 | +1 | -1 | — | — | — | — | +0 |
| 10-02 h | 73 | -4 | -3 | -4 | -2 | -3 | -2 | -1 | — | — | — | — | -2 |
| 10-03 h | 70 | +3 | +1 | -1 | +5 | +1 | +5 | +2 | — | — | — | — | +3 |
| 10-04 h | 72 | +6 | +3 | +1 | +6 | +1 | +2 | +3 | — | — | — | — | +3 |
| 10-05 h | 70 | +1 | -2 | -4 | +2 | -3 | +0 | +1 | — | — | — | — | -1 |
| 10-06 h | 68 | -1 | +1 | -3 | +4 | +0 | +2 | +1 | — | — | — | — | +1 |
| 10-07 h | 68 | +4 | +1 | -1 | +6 | +1 | +4 | +2 | — | — | — | — | +2 |
| 10-08 h | 73 | +1 | +0 | -2 | +4 | -2 | -3 | +0 | — | — | — | — | -1 |
| 10-09 h | 62 | +0 | -1 | -3 | -1 | -4 | +2 | +0 | — | — | — | — | -1 |
| 10-10 h | 59 | +1 | +1 | -2 | +0 | -1 | +1 | +0 | — | — | — | — | +0 |
| 10-11 h | 62 | +2 | +1 | -1 | +0 | -1 | +0 | +1 | +0 | — | — | — | +0 |
| 10-12 h | 64 | +1 | -1 | -2 | +0 | -2 | -2 | +1 | -1 | — | — | — | -1 |
| 10-13 | 63 | +1 | -4 | -3 | -5 | -2 | -3 | +0 | -3 | — | -2 | -5 | -2 |
| 10-14 | 66 | +0 | +3 | +0 | -1 | +0 | +1 | +0 | -3 | +0 | +0 | +1 | +0 |

Low °F: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 34 | +9 | +9 | +10 | +7 | +6 | +3 | +5 | — | — | — | — | +7 |
| 09-29 h | 55 | -4 | -2 | -3 | -5 | -2 | +0 | -5 | — | — | — | — | -3 |
| 09-30 h | 47 | -1 | +2 | +1 | +0 | +2 | +2 | -2 | — | — | — | — | +0 |
| 10-01 h | 43 | +4 | +5 | +3 | +4 | +4 | +0 | +0 | — | — | — | — | +1 |
| 10-02 h | 46 | +4 | +6 | +5 | +4 | +4 | +2 | +0 | — | — | — | — | +2 |
| 10-03 h | 46 | +5 | +7 | +6 | +5 | +6 | +1 | +4 | — | — | — | — | +3 |
| 10-04 h | 43 | +4 | +8 | +7 | +7 | +5 | +1 | +4 | — | — | — | — | +2 |
| 10-05 h | 46 | +1 | +8 | +6 | +4 | +3 | -1 | +2 | — | — | — | — | +0 |
| 10-06 h | 48 | +1 | +6 | +3 | +2 | +2 | -1 | +1 | — | — | — | — | -1 |
| 10-07 h | 50 | -3 | +3 | +1 | -3 | -3 | -8 | -5 | — | — | — | — | -6 |
| 10-08 h | 43 | +2 | +4 | +6 | +5 | +4 | +0 | +0 | — | — | — | — | +1 |
| 10-09 h | 40 | +8 | +8 | +8 | +4 | +8 | +5 | +5 | — | — | — | — | +5 |
| 10-10 h | 36 | +5 | +8 | +6 | +5 | +9 | +6 | +2 | — | — | — | — | +4 |
| 10-11 h | 30 | +9 | +10 | +12 | +8 | +11 | +6 | +7 | +6 | — | — | — | +6 |
| 10-12 h | 28 | +10 | +11 | +14 | +9 | +9 | +5 | +7 | +4 | — | — | — | +5 |
| 10-13 | 39 | +0 | +2 | +2 | +4 | +1 | +0 | -2 | -2 | — | +2 | +4 | -2 |
| 10-14 | 44 | +6 | +7 | +7 | +5 | +6 | -1 | +2 | +4 | +7 | +7 | +6 | +0 |

Wind kt: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 12 | -4 | -5 | -4 | -4 | -6 | -3 | -5 | — | — | — | — | -4 |
| 09-29 h | 15 | -3 | -3 | -4 | -7 | -6 | -3 | -2 | — | — | — | — | -4 |
| 09-30 h | 11 | -5 | -4 | -6 | -7 | -6 | -6 | -5 | — | — | — | — | -4 |
| 10-01 h | 6 | -2 | -2 | -2 | -3 | -2 | -1 | -2 | — | — | — | — | +0 |
| 10-02 h | 10 | -2 | -2 | -5 | -5 | -6 | -5 | -5 | — | — | — | — | -2 |
| 10-03 h | 12 | -5 | -5 | -6 | -7 | -7 | -7 | -4 | — | — | — | — | -3 |
| 10-04 h | 7 | -2 | -3 | -4 | -4 | -4 | -2 | -3 | — | — | — | — | +0 |
| 10-05 h | 5 | -1 | +0 | -3 | -1 | -3 | +0 | -2 | — | — | — | — | +2 |
| 10-06 h | 10 | -3 | -3 | -5 | -6 | -5 | -4 | -5 | — | — | — | — | -2 |
| 10-07 h | 14 | -7 | -6 | -8 | -10 | -9 | -8 | -6 | — | — | — | — | -5 |
| 10-08 h | 4 | +3 | +1 | +1 | +1 | +2 | +1 | +4 | — | — | — | — | +5 |
| 10-09 h | 19 | -7 | -5 | -6 | -7 | -8 | -6 | -5 | — | — | — | — | -3 |
| 10-10 h | 10 | -3 | -2 | -2 | -4 | -4 | -4 | -1 | — | — | — | — | +0 |
| 10-11 h | 12 | -2 | -2 | -6 | -7 | -8 | -5 | -4 | -1 | — | — | — | -1 |
| 10-12 h | 5 | +0 | +0 | -1 | +0 | -3 | +1 | -5 | +1 | — | — | — | +2 |
| 10-13 | 7 | -2 | -2 | -4 | -3 | -4 | -1 | -3 | +1 | — | -3 | -3 | +1 |
| 10-14 | 9 | -2 | -3 | -5 | -5 | -4 | -5 | -4 | -2 | -4 | -4 | -6 | -1 |

Precip in: observed (~ = still preliminary) and each model's error (forecast - observed, as submitted):

| Date | Obs | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL | ENS | AIFS_ENS | GEFS | CONSENSUS |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 09-29 h | 0.22 | -0.18 | +0.16 | +0.19 | +0.03 | -0.02 | +0.05 | -0.15 | — | — | — | — | +0.01 |
| 09-30 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-01 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-02 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-03 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-04 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-05 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-06 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-07 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-08 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | — | +0.00 |
| 10-09 h | 0.00 | +0.03 | +0.01 | +0.05 | +0.05 | +0.08 | +0.05 | +0.02 | — | — | — | — | +0.04 |
| 10-10 h | 0.00 | +0.00 | +0.00 | +0.01 | +0.02 | +0.02 | +0.00 | +0.00 | — | — | — | — | +0.01 |
| 10-11 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-12 h | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | — | — | +0.00 |
| 10-13 | 0.00 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | — | +0.00 | +0.00 | +0.00 |
| 10-14 | 0.00 | +0.00 | +0.00 | +0.01 | +0.00 | +0.02 | +0.00 | +0.00 | +0.00 | +0.01 | +0.02 | +0.01 | +0.01 |

## Clouds (context only, not scored)

Each scored run's total cloud cover vs the observed cloud cover, in percentage points (forecast - observed: negative = too clear, positive = too cloudy). Night = the dark hours from 06Z to sunrise, which drive the low; day = sun up, which drives the high. Observed = METAR sky cover (highest layer: FEW 19%, SCT 44%, BKN 75%, OVC 100%); automated stations see clouds only up to 12,000 ft. GOES = the satellite's cloud fraction within 15 km over the same hours (GOES Clear Sky Mask), shown for comparison; the errors are against the METAR value. At night the satellite mask relies on infrared and often misses low stratus and fog. — = no data (e.g. a station outage, or a model without a cloud forecast). Bias / MAE are decay-weighted like the low (night) and high (day).

| Model | Days | Night bias | Night MAE | Day bias | Day MAE |
| --- | --: | --: | --: | --: | --: |
| HRRR | 17 | +1 | 22 | +11 | 30 |
| RRFS | 17 | -7 | 25 | +6 | 29 |
| IFS | 17 | -1 | 21 | +3 | 21 |
| GFS | 17 | -2 | 32 | +1 | 24 |
| AIFS | 17 | +3 | 20 | +3 | 28 |
| GFS_MOS | 17 | -1 | 30 | +4 | 27 |
| NBM | 17 | -8 | 25 | -3 | 19 |
| USL | 4 | -15 | 15 | -9 | 9 |

Night clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 0% | — | +49 | +38 | +49 | +68 | +62 | +11 | +30 | — |
| 09-29 h | 100% | — | +0 | -1 | +0 | +0 | -1 | +0 | -17 | — |
| 09-30 h | 88% | — | -38 | -47 | -45 | -39 | -12 | +12 | -23 | — |
| 10-01 h | 0% | — | +99 | +99 | +89 | +100 | +100 | +88 | +80 | — |
| 10-02 h | 47% | — | -24 | -10 | -6 | +31 | +14 | +33 | -23 | — |
| 10-03 h | 19% | — | +81 | +76 | +74 | +72 | +68 | +27 | +46 | — |
| 10-04 h | 49% | — | -11 | -19 | -37 | -30 | -17 | -47 | -23 | — |
| 10-05 h | 80% | — | +1 | -22 | +5 | -55 | -7 | -50 | -32 | — |
| 10-06 h | 89% | — | -24 | -20 | -6 | -25 | -17 | -34 | -30 | — |
| 10-07 h | 69% | — | +20 | +5 | +10 | -51 | -26 | -69 | -23 | — |
| 10-08 h | 56% | — | +11 | -14 | -48 | +32 | -10 | -54 | -21 | — |
| 10-09 h | — | — | — | — | — | — | — | — | — | — |
| 10-10 h | 14% | — | -14 | -13 | -8 | +28 | +12 | +86 | +17 | — |
| 10-11 h | 13% | — | -10 | -10 | -9 | -12 | +0 | -5 | -1 | -6 |
| 10-12 h | 0% | 3% | +0 | +0 | +0 | +0 | +10 | +2 | +7 | +0 |
| 10-13 | 89% | 84% | -40 | -51 | -18 | -41 | -27 | -1 | -50 | -43 |
| 10-14 | 97% | 100% | +1 | -24 | +3 | -10 | -8 | +3 | -11 | -8 |

Day clouds: observed and each model's error (forecast - observed, percentage points):

| Date | Obs | GOES | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 09-28 h | 34% | — | +20 | +32 | +41 | +52 | +50 | +46 | +16 | — |
| 09-29 h | 100% | — | +0 | -1 | +0 | -4 | -6 | +0 | -17 | — |
| 09-30 h | 19% | — | +67 | +50 | +60 | +77 | +62 | +59 | +25 | — |
| 10-01 h | 2% | — | +98 | +98 | +93 | +98 | +93 | +69 | +66 | — |
| 10-02 h | 70% | — | -6 | -38 | -11 | -4 | -4 | +29 | -22 | — |
| 10-03 h | 54% | — | -18 | -11 | -15 | -45 | -31 | -24 | -14 | — |
| 10-04 h | 56% | — | +36 | -2 | -38 | -36 | -33 | -53 | -19 | — |
| 10-05 h | 56% | — | +44 | +42 | +21 | +16 | +18 | +15 | +14 | — |
| 10-06 h | 50% | — | +46 | +46 | +33 | +11 | +33 | -11 | -1 | — |
| 10-07 h | 52% | — | -17 | -14 | -1 | -48 | -40 | -52 | -17 | — |
| 10-08 h | 36% | — | +55 | +53 | +18 | +6 | +39 | -22 | +15 | — |
| 10-09 h | 22% | — | +39 | +31 | +6 | +36 | +36 | +48 | +23 | — |
| 10-10 h | 52% | — | -41 | -30 | -31 | +4 | -15 | +32 | -9 | — |
| 10-11 h | 18% | — | -15 | -14 | -10 | -18 | -12 | -10 | -5 | -17 |
| 10-12 h | 0% | 0% | +0 | +10 | +1 | +1 | +5 | +10 | +8 | +1 |
| 10-13 | 90% | 94% | +10 | -5 | +9 | +0 | +0 | +10 | -28 | -8 |
| 10-14 | 100% | 87% | -30 | -48 | -29 | -31 | -48 | -23 | -30 | -11 |

## Daily verification of precip chances

Chance (%) of ≥0.01" in each 6-hour block, 06-12/12-18/18-00/00-06 UTC, against the observed precip and which blocks were wet.

| Date | Observed | GFS_MOS | NBM | ENS | AIFS_ENS | GEFS | HRRRCAST | REFS | NBM_QMD |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-13 | 0.00" (dry) | 2/7/9/3 | 7/9/6/3 | 0/2/2/16 | 2/0/0/2 | 0/0/0/10 | 24h 22% | 24h 7% | 0/0/0/0 |
| 10-14 | 0.00" (dry) | 9/20/1/2 | 10/11/3/0 | 6/39/8/0 | 33/26/2/0 | 3/29/0/0 | 24h 0% | 24h 7% | 0/9/0/0 |

## Today so far (2026-10-15, through 2026-10-16T00:54Z)

This is the day in progress (not the target day), scored against the runs submitted before its deadline. Observed so far: high 66.9 °F, low 39.9 °F, max wind 7 kt, precip 0.00" (19 hourly obs).

Temp bias/MAE are over the hourly obs so far. High/low columns show the model's daily value and (in brackets) its difference from the observed extreme so far; "pending" means the model's expected time of that extreme hasn't passed, so the observed value can still change.

| Model | Run | Temp bias | Temp MAE | High (err) | Low (err) | Wind bias | Precip so far | Precip err |
| --- | --- | --: | --: | --: | --: | --: | --: | --: |
| HRRR | 14/18Z | +4.9 | 7.7 | 78 (+11) | 44 (+4) | -0.7 | 0.00 | +0.00 |
| RRFS | 14/18Z | +4.3 | 5.3 | 74 (+7) | 48 (+8) | -0.5 | 0.00 | +0.00 |
| IFS | 14/12Z | +2.3 | 3.5 | 69 (+2) pending | 47 (+7) | +0.1 | 0.00 | +0.00 |
| GFS | 14/18Z | +3.8 | 5.6 | 74 (+7) | 46 (+6) | -0.1 | 0.00 | +0.00 |
| AIFS | 14/12Z | +2.6 | 3.5 | 70 (+4) pending | 46 (+6) | +0.8 | 0.00 | +0.00 |
| GFS_MOS | 14/18Z | +0.3 | 4.2 | 71 (+4) pending | 41 (+1) | -1.9 | — | — |
| NBM | 14/18Z | +1.4 | 3.9 | 70 (+3) pending | 44 (+4) | +0.7 | — | — |
| USL | 14/22Z | +1.0 | 3.8 | 69 (+2) | 45 (+5) | +1.6 | 0.00 | +0.00 |
| ENS | 14/06Z | +4.0 | 4.8 | 70 (+3) | 48 (+8) | +0.4 | 0.00 | +0.00 |
| AIFS_ENS | 14/12Z | +3.5 | 4.2 | 71 (+4) pending | 47 (+8) | +0.8 | 0.00 | +0.00 |
| GEFS | 14/18Z | +3.9 | 5.5 | 72 (+5) | 47 (+7) | +0.0 | 0.00 | +0.00 |

## Clouds so far today (2026-10-15, observed vs forecast)

Cloud cover (%) each hour of the day in progress. GOES = satellite cloud fraction within 15 km of the station (GOES-18 Clear Sky Mask, the scan nearest the top of the hour); at night it relies on infrared and often misses low stratus and fog, so trust METAR then. METAR = the station's sky cover (highest layer: FEW 19, SCT 44, BKN 75, OVC 100; automated stations see only up to 12,000 ft), from the report nearest the hour. Model columns are the runs submitted for today (* = averaged over the preceding interval). Context only, not scored.

| UTC | Local (PDT) | GOES | METAR | HRRR | RRFS | IFS | GFS | AIFS | GFS_MOS | NBM | USL |
| --- | --- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| 10-15 06Z | Wed 23:00 | 0 | 0 | 0 | 0 | 0 | 5 | 2 | 0 | 4 | 49 |
| 10-15 07Z | Thu 00:00 | 0 | 0 | 1 | 5 |  |  |  |  |  | 46 |
| 10-15 08Z | Thu 01:00 | 0 | 100 | 7 | 13 |  |  |  |  |  | 41 |
| 10-15 09Z | Thu 02:00 | 20 | 100 | 19 | 28 | 2 | 5 |  | 0 | 20 | 40 |
| 10-15 10Z | Thu 03:00 | 12 | 100 | 100 | 43 |  |  |  |  |  | 42 |
| 10-15 11Z | Thu 04:00 | 78 | 100 | 100 | 61 |  |  |  |  |  | 44 |
| 10-15 12Z | Thu 05:00 | 94 | 100 | 100 | 68 | 72 | 10 | 57 | 0 | 55 | 47 |
| 10-15 13Z | Thu 06:00 | 95 | 100 | 100 | 71 |  |  |  |  |  | 51 |
| 10-15 14Z | Thu 07:00 | 99 | 100 | 100 | 79 |  |  |  |  |  | 56 |
| 10-15 15Z | Thu 08:00 | 6 | 100 | 100 | 86 | 100 | 21 |  | 44 | 66 | 60 |
| 10-15 16Z | Thu 09:00 | 99 | 100 | 100 | 85 |  |  |  |  |  | 54 |
| 10-15 17Z | Thu 10:00 | 99 | 100 | 88 | 58 |  |  |  |  |  | 39 |
| 10-15 18Z | Thu 11:00 | 100 | 100 | 38 | 18 | 44 | 5 | 22 | 0 | 41 | 27 |
| 10-15 19Z | Thu 12:00 | 97 | 100 | 6 | 6 |  |  |  |  |  | 21 |
| 10-15 20Z | Thu 13:00 | 86 | 100 | 90 | 32 |  |  |  |  |  | 18 |
| 10-15 21Z | Thu 14:00 | 0 | 0 | 45 | 0 | 4 | 73 |  | 0 | 6 | 17 |
| 10-15 22Z | Thu 15:00 | 0 | 0 | 0 | 0 |  |  |  |  |  | 17 |
| 10-15 23Z | Thu 16:00 | 0 | 0 | 0 | 0 |  |  |  |  |  | 15 |
| 10-16 00Z | Thu 17:00 | 0 | 0 | 2 | 0 | 8 | 100 | 2 | 0 | 5 | 16 |
| 10-16 01Z | Thu 18:00 | 0 | 0 | 34 | 0 |  |  |  |  |  | 24 |

## Raw data

- Forecast (all models, ensemble members, consensus weights): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/forecast.json
- Verification (every day, every model, observations, PoP calibration): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/verification.json
- Today so far: https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/today.json
- Cloud forecast vs observed per scored run (not scored): https://jameslarsonclimate.github.io/website/weather-forecasts/data/wxchallenge/cloud_context.json
- NWS Area Forecast Discussion (SEW): https://forecast.weather.gov/product.php?site=SEW&issuedby=SEW&product=AFD&format=txt&version=1&glossary=0
- Human page: https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/
