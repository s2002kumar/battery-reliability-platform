# ML Evaluation Plan — ARCH-01 BLOCKED

**No SOH target, denominator, or HUST→Aurora SOH metric is approved.** HUST `dq` is supported as a cycle discharge-capacity label in five inspected cells; Aurora contains current/time/voltage but no capacity field, and its LFP `cycle_dimensionless` stream resets to zero repeatedly. A deterministic complete-discharge grouping and common reference-capacity rule cannot currently be established without guessing. Do not build target/feature tables or train models.

## Target and reference capacity

Conceptual target:

`SOH(cell, cycle) = available_discharge_capacity(cell, cycle) / reference_capacity(cell)`

The numerator must be a complete-cycle discharge capacity, in a source-verified unit and under an identified protocol. HUST's source label `dq` matched `max(Capacity (mAh)) - final Capacity (mAh)` for all cycles in five inspected cells, within `2.28e-13 mAh`; that is strong source-specific evidence but not yet a 77-file audit. Aurora has no explicit capacity field; numerically integrating its negative current over time could estimate capacity only after complete discharge segments and cycle boundaries are unambiguously identified. Its observed LFP cycle count resets repeatedly to zero, and the BDF schema has no step/status/capacity column to distinguish those segments.

**Final ARCH-01 reference decision: no deterministic `reference_capacity` rule is frozen.** Do not use nominal/rated capacity, a single first cycle, maximum over full life, or a guessed first-N/post-formation window. Five HUST samples show the first `dq` is 0.233–0.283% above the median of cycles 1–10 and each selected series declines during those first ten cycles. HUST author preprocessing omits the first nine ordered `dq` labels without documenting that as formation. The Aurora paper's three formation cycles at 0.1 mA cm⁻² followed by aging at 1.0 mA cm⁻² are documented for its NMC622 case; do not generalize that phase count to LFP. The paper's LFP discussion gives a 3.65 V upper cutoff. Direct LFP sample rows show a current change between cycles 1–3 and 4 onward, but do not resolve the archive's repeated BDF cycle-index resets or create an explicit capacity field. A robust reference window is not selected because neither a matching HUST reference test/window nor an Aurora unambiguous archive cycle/capacity mapping has been verified.

This is an explicit target blocker, not a deferred modeling detail. Reopen only with source-owner clarification or direct evidence that establishes both sources' complete-cycle capacity measurements, formation/cycle mapping, and a reproducible comparable reference rule. A source-aware denominator may be reconsidered only if its meaning still matches the locked product definition.

## Split identity

Group all rows, tests, and files for a physical cell by `(source_name, source_record_version, source_native_cell_id)`. HUST's nested cell key (e.g., `1-1`) and Aurora's `ccid000XXX` IDs are namespaced separately; never join them. Split by cell before fitting or preprocessing. A source-native ID missing or ambiguous for a partition excludes that partition from cell-level evaluation.

Record seed, split assignments, source manifests, and exact target/feature/config versions. Do not randomly split cycle rows. Preserve source, chemistry, cell design, protocol, temperature, and batch as metadata for grouped stratification/error analysis rather than predictors by default.

## Leakage controls

Before any feature set is approved, declare the prediction cutoff and exclude or prove time-safe:

1. The target-cycle discharge capacity and all aliases/aggregations of it.
2. SOH, RUL, end-of-life, health grade, or labels computed from present/future capacity trajectories.
3. Future-cycle samples, windows that cross the cutoff, and full-life statistics.
4. `reference_capacity` when used to construct the target; it is target metadata, never a feature.
5. `rul` and `dq` target/label aliases in HUST payloads.
6. Cumulative capacity/energy whose reset or measurement window is unknown.
7. Cell IDs, filenames, source, protocol, batch, or chemistry as inputs unless a separate deployment question explicitly justifies them; retain them for grouping and analysis.
8. Cycle count, time, throughput, and any age proxy unless available at the defined inference time and independently checked for target/future derivation.

No column is leakage-safe solely because its name differs from the target. Feature lineage must trace to raw/canonical records and a prediction-time cutoff.

## Cross-source evaluation decision

**HUST→Aurora quantitative SOH evaluation is blocked.** Both contain LFP/graphite candidates, but no comparable normalized target is currently established. Aurora's exact archive LFP subset is 32 cells: `ccid000217`–`ccid000247` excluding `ccid000248`, plus `ccid000249`. Its paper reports an LFP batch of 36; the archive contains 32 records in that chemistry. HUST is 77 commercial cylindrical A123 LFP/graphite cells at 30 °C with per-cell personalized multistage discharges. Aurora uses CR2032 coin cells and 25 °C. The Aurora paper's three formation cycles followed by aging at 1.0 mA cm⁻² describe its NMC622 case; do not assign that exact protocol to LFP. The LFP paper discussion specifies a 3.65 V upper cutoff; archived LFP JSON-LD has per-cell protocols and row samples show a current-level change between cycle values 1–3 and 4 onward, while the cycle field resets remain unresolved. A future aligned LFP experiment would be a combined source/lab, cell-design, temperature, electrode-batch, and protocol shift, not an isolated source or chemistry effect. Do not pool all chemistries or call it a like-for-like benchmark.

After target blockers are resolved, a potential design is HUST cell-grouped in-domain evaluation plus a separately reported zero-shot Aurora LFP stress test, stratified by verified protocol/temperature and labeled exploratory. If target semantics/reference windows remain incompatible, omit cross-source SOH metrics; only parser/data-quality robustness can be compared across those data, not model accuracy.

## Evaluation after architecture review unblocks modeling

- Deterministic physical-cell grouped train/validation/test splits; no cell may cross partitions.
- Naive/reference, linear, boosted-tree and, when scale justifies, uncertainty-aware baselines.
- Metrics and error analysis by source, chemistry, cell design, protocol, temperature, and relevant batch.
- Versioned source manifests, target rule, reference window, feature lineage, split manifest, model/config, and environment.
- Reproducible results and leakage audit under `docs/evidence/` before any public performance claim.
