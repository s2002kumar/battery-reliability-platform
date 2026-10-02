# ADR-001: Canonical Schema Boundary and BDF Alignment

- **Status:** Proposed; source mapping not approved (ARCH-00 BLOCKED)
- **Date:** 2026-10-02
- **Scope:** Canonical measurement vocabulary boundary before any source adapter is implemented

## Context

V1 needs a stable representation across vendor exports without erasing source semantics. BDF defines common cycler quantities, units, required/recommended/optional conformance, and distinctions among step, cycle, and test cumulative capacities. The draft contract previously used an unqualified `discharge_capacity_ah`, which cannot distinguish these quantities.

## Proposed decision

1. Align canonical time-series measurement meanings and normalized SI units with the pinned Battery Data Alliance BDF ontology/specification.
2. Keep project provenance, source-scoped cell/test identity, quality, and feature lineage as project-owned fields outside the BDF measurement vocabulary.
3. Keep separate fields for cycle, step, and test-cumulative charge/discharge capacity. Do not map an ambiguous capacity label to a canonical field.
4. Preserve BDF current sign (positive charge, negative discharge), source cycle counts, pauses, and source-native IDs. Never silently renumber, reset, or coerce.
5. Missing optional values remain null/absent. Ambiguous semantics quarantine the affected data with machine-readable reason.
6. Pin the exact BDF release/ontology snapshot at implementation time; do not depend on mutable `main`.

## Field boundary

`test_time_s`, `voltage_v`, and `current_a` are the canonical measurement minimum. `cycle_index`, `step_count`, `step_id`, `step_time_s`, temperature channels, absolute timestamp, and cycle/step/test capacity/energy are optional and nullable only when absent from the source. Derived step/cycle boundaries must include method and version. Full details and nullability are in [DATA_CONTRACT.md](../../DATA_CONTRACT.md).

## Evidence and unresolved condition

- [BDF specification repository](https://github.com/battery-data-alliance/battery-data-format) states one cell per time-series file, required time/voltage/current, current sign, and optional cycle/step/capacity fields.
- [BDF specification README](https://github.com/battery-data-alliance/battery-data-format/blob/main/README.md) distinguishes cumulative test capacities from per-cycle capacities and says source IDs/metadata belong in companion metadata.
- The inspected HUST `our_data/1-1.pkl` DataFrame exposes `Time (s)`, `Voltage (V)`, `Current (mA)`, `Cycle number`, `Status`, and `Capacity (mAh)`. Unit names do not establish sign, aggregation, cycle, or capacity semantics; no adapter mapping is approved.
- The Aurora archive inventory and `empa__ccid000001.metadata.json` were inspected, but its `.bdf.csv`/`.bdf.parquet` time-series rows were not parsed. Record-level BDF description is not evidence of the actual capacity fields or null behavior in each member.

The vocabulary boundary is proposed, but mapping coverage for selected sources has not been demonstrated. Revisit this ADR after exact source artifacts and headers are inspected. No source adapter is authorized by this ADR.
