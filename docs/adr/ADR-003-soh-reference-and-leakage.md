# ADR-003: SOH Reference Capacity and Leakage Policy

- **Status:** BLOCKED; no reference-capacity rule frozen
- **Date:** 2026-10-02
- **Scope:** Capacity-based state-of-health target and cell-safe evaluation

## Context

The locked target is `SOH = available_discharge_capacity / reference_capacity(cell)`. A physically meaningful denominator must be deterministic, comparable to the numerator, and available without using future observations. A first-cycle denominator can be biased by formation/early-cycle instability.

## Decision

No denominator rule is approved. Do not use nominal capacity, a single first cycle, maximum observed capacity across the full life, or an arbitrary initial window as a substitute. The HUST native files and capacity protocol have not been verified. The Aurora publication describes three formation cycles; its per-cell BDF cycle indices and exact capacity fields have not been verified from the archive.

The only candidate to evaluate after source inspection is a median over an explicitly documented post-formation reference window of repeated standardized discharge-capacity measurements, if and only if both selected sources contain such measurements under comparable protocols. Otherwise the denominator and possibly the cross-source target require architecture review. This candidate is not a frozen rule.

## Leakage and grouping policy

- Group every row/file/test from one physical cell using `(source_name, source_record_version, source_native_cell_id)` before splitting.
- Never random-split repeated cycle rows.
- Exclude the target capacity, its aliases/derived labels, the reference denominator, precomputed SOH/EOL/RUL, future cycles, full-life statistics, and any cumulative values with unknown reset/future semantics from predictors.
- Treat cycle count, elapsed age, throughput, source, test protocol, filenames, and cell IDs as metadata by default. A future task may justify an inference-available field only with a defined prediction cutoff and separate leakage review.
- Version the target definition, reference window, feature set, split manifest, and source manifests.

## Evidence and blocker

- [HUST Mendeley version 2 record](https://data.mendeley.com/datasets/nsc7hnsg4s/2): 77 LFP/graphite cells, same charge protocol, personalized multistage discharge protocols, 30 °C; exact files and reference-check semantics unavailable in current inspection.
- [Ma et al. (2022)](https://doi.org/10.1039/D2EE01676A): original study describes capacity as a health output and the 77-cell HUST dataset.
- [Empa Aurora Zenodo v1](https://zenodo.org/records/15481956) and [original publication](https://doi.org/10.1002/batt.202500155): 199 coin cells, LFP//graphite or NMC//graphite; publication describes three formation cycles and subsequent long-term cycling.
- [BDF ontology/specification](https://github.com/battery-data-alliance/battery-data-format) distinguishes per-cycle discharge capacity from test-cumulative discharge capacity.

Exact source columns, capacity roll-up, formation indices, stable-reference observations, and target comparability are not established. ARCH-00 remains BLOCKED until directly verified or explicitly redesigned by the project owner.
