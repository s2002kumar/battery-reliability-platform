# ADR-003: SOH Reference Capacity and Leakage Policy

- **Status:** BLOCKED — no reference-capacity rule approved
- **Date:** 2026-10-06
- **Scope:** Capacity-based SOH target and cell-safe evaluation

## Context

The product target is `SOH = available_discharge_capacity / reference_capacity(cell)`. The denominator must use a physically interpretable, deterministic capacity measurement and must not depend on future outcomes. An arbitrary first cycle or nominal rating does not establish a reference measurement.

## Decision

**No deterministic reference-capacity rule is frozen.** Five HUST payloads show `dq` equals max-minus-final `Capacity (mAh)` for every inspected cycle; the first value is 0.233–0.283% above the first-ten median in these selected cells. The author pipeline drops the first nine ordered labels but does not call them formation cycles. The paper describes a 10th-cycle charge-curve feature baseline, not a capacity denominator. Aurora's original paper reports three formation cycles and subsequent aging for its NMC622 case; do not generalize this to LFP. The v1 archive has no explicit capacity field and the observed LFP cycle-count sequence repeatedly returns to zero. These facts do not establish a common, stable, complete-discharge reference window.

Reject nominal/rated capacity, single first-cycle capacity, maximum full-life capacity, and an arbitrary post-formation window. Do not use a proposed median window until primary source/file evidence establishes exact source cycle boundaries, the reference protocol, and repeatability in both sources. If no comparable rule fits both sources, the target or source scope requires an explicit architecture decision.

## Leakage and grouping policy

- Group all files/tests/cycles for one physical cell by `(source_name, source_record_version, source_native_cell_id)` before splitting.
- Never randomly split repeated cycle rows.
- Exclude target capacity and aliases, the denominator, HUST `dq`/`rul` labels, precomputed SOH/EOL/RUL, future cycles, full-life statistics, and accumulators with unknown reset semantics from predictors.
- Keep cell/source/protocol IDs, filenames, batch, chemistry, cycle age, and throughput as grouping/analysis metadata by default. A future prediction task must establish inference-time availability and perform a separate leakage audit.
- Version the target rule, reference measurements/window, feature lineage, source manifests, and split manifest.

## Evidence and blocker

- HUST exact source and inspection: [Mendeley v2](https://data.mendeley.com/datasets/nsc7hnsg4s/2), author paper [Ma et al. (2022)](https://pubs.rsc.org/en/content/articlehtml/2022/ee/d2ee01676a), and [ARCH-01 evidence](../evidence/ARCH-01.md).
- Aurora exact source and metadata: [Zenodo v1](https://zenodo.org/records/15481956), original [Aurora paper](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/batt.202500155), and [ARCH-01 evidence](../evidence/ARCH-01.md).
- Source mappings/nullability are recorded in [DATA_CONTRACT.md](../../DATA_CONTRACT.md); evaluation restrictions are in [ML_EVALUATION_PLAN.md](../../ML_EVALUATION_PLAN.md).

Until the Aurora event boundaries and capacity integration rule and the comparable reference-window semantics are directly verified, no SOH target or cross-source metric is approved. This is an architecture blocker, not an implementation choice.
