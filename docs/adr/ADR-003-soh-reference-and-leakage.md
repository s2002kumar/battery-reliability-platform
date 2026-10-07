# ADR-003: SOH Reference Capacity and Leakage Policy

- **Status:** Accepted for the selected HUST and Aurora LFP subsets; ARCH-01 evidence applies
- **Date:** 2026-10-07
- **Scope:** Capacity-based SOH target definition and cell-safe evaluation

## Context

The product target is `SOH = available_discharge_capacity / reference_capacity(cell)`. The reference must be measurable from data available before each scored cycle. Nominal rating, a future-life maximum, and arbitrary source-index windows are not valid substitutes.

Direct archive inspection established: (1) HUST contains 77 ordered, cycle-keyed `dq` label series; their keys align with `data` and `rul`, start at key 1, and are monotonic in insertion order. A complete first-three-cycle reference window varies by at most 0.724% of its median over 77 cells (median range 0.154%). In seven representative/edge payloads, 13,517 frame-level comparisons show `dq = max(Capacity (mAh)) - final Capacity (mAh)` within 2.28e-13 mAh. (2) Aurora's exact LFP metadata explicitly defines three low-rate cycles followed by a 1,000-iteration aging protocol. Its 32 LFP BDF traces each contain 1,003 substantive discharge events aligned to those protocol loops. Trapezoidal current/time integration has a clean observed separation between zero-duration artifacts (maximum 0.00428 mAh) and discharge events (minimum 0.2757 mAh). The first three aging-event capacities vary by at most 1.374% of their median (median range 0.669%).

Evidence locations: [ARCH-01 evidence](../evidence/ARCH-01.md), [HUST all-77 label audit](../../research/ARCH-01/hust_all77_reference_window_audit.json), and [Aurora LFP protocol/capacity audit](../../research/ARCH-01/aurora_lfp_protocol_alignment.json).

## Decision

Use a source-aware **median of the first three complete discharge-capacity observations in the cell's sustained aging protocol** as `reference_capacity`. Score only later sustained-aging cycles. This is an operational per-cell baseline, not a manufacturer-rated or universal initial capacity.

- **HUST:** use `dq` for the first three ordered recorded discharge cycles (keys 1–3). The source does not label a separate formation stage in this dataset; do not invent one or apply the author's first-nine-label preprocessing convention. The denominator is `median(dq[1], dq[2], dq[3])`. Exclude keys 1–3 from scored targets.
- **Aurora LFP:** use current/time-integrated capacity from the first three substantive discharge events after the metadata-declared three-cycle low-rate phase. These are the first three discharge events in the 1,000-iteration, 1.0 mA cm⁻² aging loop. Exclude the initial three low-rate events and these three reference events from scored targets. Map logical cycle ordinal from protocol-aligned ordered discharge events; preserve the source `cycle_dimensionless` values unchanged. Flag/quarantine discharge events outside the protocol cutoff quality tolerance rather than silently accepting them.
- Do not compare absolute capacity across the two sources. The normalized within-cell trajectory is the target; chemistry, cell design, test protocol, temperature, and source remain distinct strata.

This rule is deterministic, causal for scored cycles, and directly grounded in each selected source's measurements/protocol. It must be versioned in derived dataset metadata. If source versions or protocol structures change, rerun the audit before reuse.

## Leakage and grouping policy

- Group all rows/tests/cycles from one physical cell by `(source_name, source_record_version, source_native_cell_id)` before splitting.
- Never randomly split repeated cycle rows.
- Exclude the target capacity and aliases, denominator, HUST `dq`/`rul` target labels, precomputed SOH/EOL/RUL, future cycles, full-life statistics, and cumulative values with unverified resets from predictors.
- Do not score reference-window cycles. Features must be available at the declared prediction cutoff; cell/source/protocol identifiers remain metadata for grouping and analysis unless a later decision approves a deployment use.
- Version the source manifests, capacity derivation, reference observations, target rule, feature lineage, and split manifest.

## Evidence and limits

- HUST exact record and observed data: [Mendeley v2](https://data.mendeley.com/datasets/nsc7hnsg4s/2), [Ma et al. (2022)](https://pubs.rsc.org/en/content/articlehtml/2022/ee/d2ee01676a), and [ARCH-01 evidence](../evidence/ARCH-01.md).
- Aurora exact record and metadata: [Zenodo v1](https://zenodo.org/records/15481956), [Svaluto-Ferro et al. (2025)](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/batt.202500155), and [ARCH-01 evidence](../evidence/ARCH-01.md).
- Source mappings and unavailable fields are in [DATA_CONTRACT.md](../../DATA_CONTRACT.md); evaluation restrictions are in [ML_EVALUATION_PLAN.md](../../ML_EVALUATION_PLAN.md).

Remaining limits include seven-cell row-level HUST schema/capacity comparisons (with the full 77-member key/label window audit), integrated rather than source-reported Aurora capacity, three Aurora cells with one event each outside the 0.08 V cutoff diagnostic, and no absolute cross-source capacity comparability. These are explicit provenance/quality limits; the operational SOH rule does not silently include suspect cycles.
