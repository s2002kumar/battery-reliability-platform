# ML Evaluation Plan — ARCH-00 Gate State

**Status: BLOCKED.** The project target is capacity-based SOH, but there is no approved denominator or cross-source target contract yet. Do not construct targets, feature tables, or model splits until the data gate resolves the evidence gaps below.

## Target definition and reference capacity

Conceptual target:

`SOH(cell, cycle) = available_discharge_capacity(cell, cycle) / reference_capacity(cell)`

The numerator must ultimately be a source-validated complete-cycle discharge capacity in Ah, not a partial step capacity, test-cumulative accumulator, charge capacity, nominal rating, or energy. A source-native capacity label can be used only after its exact field, reset semantics, measurement protocol, and row-to-cycle association are verified.

**No deterministic `reference_capacity` rule is frozen.** The tempting rule “first cycle capacity” is not accepted: the Empa Aurora paper describes three formation cycles, and the HUST record does not yet establish the formation sequence or the presence of a standardized capacity check. A median over a post-formation reference window would be preferable to one unstable measurement only if both selected sources expose repeated measurements under a documented, comparable reference protocol. That condition has not been verified. Do not choose the window length or BDF cycle numbers by assumption.

The next evidence needed is the exact HUST file/readme inventory and the exact Aurora archive subset/metadata. Verify whether each source has a common capacity-check protocol distinct from its aging cycles, how the capacity was computed, which cycles are formation/conditioning, and how cycle counts are encoded. If HUST has no defensible reference window comparable to Aurora, stop and request an architecture decision on target/source scope rather than normalize by nominal capacity or an arbitrary early cycle.

## Dataset and split identity

- Primary development candidate: HUST Mendeley dataset version 2, restricted to physical LFP/graphite cells after file-level verification.
- Potential external source candidate: Empa Aurora Zenodo v1, initially restricted to its LFP//graphite subset if an adequate cell count and target protocol are confirmed.
- Group key: `(source_name, source_record_version, source_native_cell_id)`. All cycles/tests/files for one physical cell belong to a single split. If source-native IDs cannot identify a physical cell unambiguously, that source is excluded from cell-level evaluation pending a documented identity decision.
- Record stable group IDs only in split manifests; do not emit row-level target values or raw source identifiers into public manifests.
- Seed and split configuration must be explicit and recorded. Never randomly split cycle rows.

## Leakage audit

Candidate feature construction must exclude or prove time-safe all of the following:

1. The numerator field `cycle_discharging_capacity_ah`, any duplicate/alias/derived capacity summary for the target cycle, and any target-cycle capacity used in the denominator.
2. Any precomputed SOH/capacity-retention label, health grade, end-of-life flag, remaining-life label, or preprocessing column computed from the target/future capacity trajectory.
3. Any later-cycle measurement, statistic, rolling window that crosses the prediction cutoff, or full-test normalization/summary calculated using future cycles.
4. Reference capacity as a model predictor when it is used to construct the target; it is target-construction metadata, not a feature.
5. Cell IDs, filenames, protocol labels, source names, or acquisition batch as predictors unless a separately specified deployment question justifies them. They can reveal split/source identity or encode outcomes; keep them as grouping/stratification metadata by default.
6. Cycle number, elapsed aging time, or throughput as potential age proxies. They may be included only for a clearly defined prediction-time use case and must be available at inference time without target/future-derived computation.
7. Any capacity/energy accumulator that is cumulative across future parts of a cycle/test or whose reset semantics are unknown.

The leakage review must operate on the exact feature lineage and a declared prediction cutoff. A feature merely having a different column name does not establish independence from SOH.

## Cross-source/domain-shift decision

**Not approved as a V1 quantitative comparison yet.** HUST provides LFP/graphite A123 cylindrical cells and personalized multistage discharge protocols at 30 °C. Aurora has LFP/graphite and NMC/graphite CR2032 coin-cell data with cell-specific assembly/protocol metadata and 25 °C experiments; its paper describes formation cycles. A pooled all-chemistry comparison would conflate source, chemistry, cell format/design, temperature, and protocol.

The only scientifically defensible candidate is a separately reported zero-shot stress test restricted to verified LFP/graphite cells in both sources, using source-validated capacity measurements and the same defensible per-cell reference-capacity definition. Even then, it is a **combined source/cell-design/protocol shift**, not an isolated source effect. Report HUST in-domain cell-grouped results and Aurora external results separately, stratify by available protocol/temperature metadata, and label the external result as exploratory domain-shift evidence. Do not describe it as chemistry transfer or fair like-for-like model comparison. If common capacity semantics/reference tests cannot be established, omit cross-source SOH metrics and mark this product requirement BLOCKED for architecture review.

## Required evaluation once unblocked

- Deterministic train/validation/test splits grouped by physical cell; no shared cell across partitions.
- Naive/reference, linear (Ridge or ElasticNet), and boosted-tree baselines; uncertainty-aware baseline only if justified by scale and evidence.
- Target/feature/split version and configuration, source manifests, metrics, error analysis, per-source/condition breakdown, and leakage audit under `docs/evidence/`.
- Cross-source metrics kept separate from in-domain metrics; no benchmark claim without reproducible evidence.
