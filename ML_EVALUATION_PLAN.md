# ML Evaluation Plan — ARCH-00/ARCH-01 Architecture Gate

**SOH target and evaluation contract are approved for the selected HUST and Aurora LFP subsets.** This approves target design only; it does not authorize model implementation before the dependent ingestion and feature tasks are complete. Source-specific coverage and the known Aurora event-quality exclusions are documented below and in [ARCH-01 evidence](docs/evidence/ARCH-01.md).

## Target and reference capacity

Conceptual target:

`SOH(cell, cycle) = available_discharge_capacity(cell, cycle) / reference_capacity(cell)`

The target is a within-cell normalized trajectory under an identified sustained discharge protocol. It is not an absolute-capacity comparison across different cell designs or test rates.

**Deterministic reference rule:** for each cell, take the median of the first three complete discharge-capacity observations in its sustained aging protocol. Exclude the baseline observations from scored targets; score only subsequent aging cycles.

- **HUST:** `available_discharge_capacity = dq` in mAh. Use the first three ordered recorded discharge labels, keys 1–3; the selected dataset does not identify an earlier separate formation phase. `reference_capacity = median(dq[1], dq[2], dq[3])`. Exclude cycles 1–3 from scored targets. The 77-file audit confirms `data`, `dq`, and `rul` key sets and order agree, begin at 1, and remain monotonic. The three-cycle window range is at most 0.724% of its median (median across cells 0.154%). Frame-level `dq = max(Capacity (mAh)) - final Capacity (mAh)` is directly verified across all cycles in seven representative/edge payloads; see coverage limits in the evidence.
- **Aurora LFP:** derive capacity as trapezoidal integration of absolute discharge current over elapsed time for each protocol-aligned substantive discharge event. Direct JSON-LD metadata specifies three 0.1 mA cm⁻² formation/conditioning iterations followed by a 1,000-iteration 1.0 mA cm⁻² aging loop. Each of 32 LFP traces has 1,003 substantive discharge events. The first three sustained-aging events (after the first three conditioning events) form the reference median; do not use rated-capacity metadata as measured capacity. Exclude both the three conditioning events and three baseline events from scored targets. Preserve raw `cycle_dimensionless` reset values and use a separately recorded derived event ordinal.

Across the 32 Aurora cells, the first three aging-event capacity ranges are 0.386%–1.374% of each cell's median (median 0.669%). The observed capacity gap separates zero-duration current artifacts (largest 0.00428 mAh) from substantive events (smallest 0.2757 mAh); the audit's 0.1 mAh cut lies between these populations and identifies exactly 1,003 events per cell, matching the metadata loop count. Twenty-nine cells have all substantive events ending within 0.08 V of the specified 2.5 V cutoff; three cells each have one event outside this diagnostic. Those events require explicit quality disposition/quarantine; the baseline events themselves align with the lower cutoff.

HUST's first-three recorded cycles are operational reference observations, not a claim that the source calls them formation or a standardized capacity test. Do not use HUST's author-code omission of nine labels as a formation rule. Do not substitute a first-cycle value, nominal/rated capacity, full-life maximum, or future-derived statistic.

## Split identity and leakage controls

Group all rows/tests/cycles for a physical cell by `(source_name, source_record_version, source_native_cell_id)`. HUST uses its nested key (for example, `1-1`); Aurora uses `ccid000XXX`; namespace identifiers by source. Split by cell before fitting or preprocessing. Never randomly split cycle rows.

Before features are approved, declare a prediction cutoff and exclude or prove time-safe:

1. Target-cycle capacity and all aliases/aggregations, including HUST `dq` and Aurora integrated event capacity.
2. `SOH`, `reference_capacity`, `rul`, end-of-life, health grades, and labels based on present/future capacity trajectories.
3. Future-cycle samples, windows crossing the cutoff, and full-life statistics.
4. Cumulative capacity/energy with unknown event/reset semantics.
5. Cell IDs, filenames, source, protocol, batch, chemistry, and product metadata as predictors unless a later deployment decision explicitly approves use; retain them for grouping and error analysis.
6. Cycle count, elapsed age, throughput, and other age proxies unless they are available at inference time and independently reviewed.

Record seed, split assignments, source manifests, target/reference rule version, feature lineage, and exact code/config/environment versions. No feature is leakage-safe solely because its name differs from the target.

## Cross-source/domain-shift design

**Approve an exploratory, zero-shot HUST→Aurora LFP stress evaluation after the data quality and ingestion gates pass.** Select HUST's 77 A123 LFP/graphite cylindrical cells and Aurora's exact 32 LFP/graphite coin-cell records (`ccid000217`–`ccid000247` excluding `ccid000248`, plus `ccid000249`). The shared chemistry and source-specific within-cell reference rule make normalized SOH trajectories interpretable for a bounded stress test.

This is a **combined domain shift**, not an isolated source or chemistry effect: it simultaneously changes laboratory/source, cylindrical A123 versus CR2032 coin-cell design, electrode batch/construction, temperature (30 °C versus 25 °C), and discharge protocol (personalized HUST profiles versus Aurora's fixed 1.0 mA cm⁻² aging loop). Train on grouped HUST cells and evaluate Aurora cells zero-shot; report the result as exploratory, with the listed covariates and per-source metrics. Do not pool the different Aurora chemistries, compare absolute capacities, or call this a like-for-like benchmark.

Within HUST, also reserve complete personalized discharge-protocol families for a grouped held-out-protocol analysis. Keep all cells and cycles for each physical cell together. Report this separately from grouped within-protocol held-out-cell metrics; protocol-family identity must be validated before split construction.

## Evaluation after architecture review unblocks modeling

- Naive/reference, linear, boosted-tree, and uncertainty-aware baselines when scale justifies it.
- Deterministic physical-cell grouped train/validation/test splits and the separate zero-shot Aurora LFP evaluation above.
- Metrics and error analysis by source, chemistry, cell design, protocol, temperature, and batch.
- Versioned source manifests, target/reference definition, feature lineage, split manifest, model/config, and environment.
- Reproducible results and leakage audit under `docs/evidence/` before any public performance claim.
