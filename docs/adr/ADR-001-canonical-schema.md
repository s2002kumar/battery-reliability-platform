# ADR-001: Canonical Schema Boundary and BDF Alignment

- **Status:** Proposed; ARCH-00/ARCH-01 BLOCKED, source mappings are only partially verified
- **Date:** 2026-10-06
- **Scope:** Canonical measurement vocabulary before adapters exist

## Context

V1 needs common battery measurements without erasing source semantics. The BDF format distinguishes required time/voltage/current from optional cycle, step, cumulative, cycle-capacity, step-capacity, and energy quantities. Source fields named “capacity” or “cycle” do not alone establish these meanings.

## Decision boundary

1. Align canonical measurement meaning and SI units to a pinned Battery Data Alliance BDF specification/ontology snapshot before implementation.
2. Preserve raw source names, values, source IDs, order, and sign. Keep project provenance, cell/test identity, quality, and lineage outside the BDF measurement vocabulary.
3. Use separate canonical fields for test-cumulative, per-cycle, and per-step charge/discharge capacity/energy. No unqualified `discharge_capacity_ah` field.
4. BDF current is positive for charge and negative for discharge. Preserve that convention; do not reverse signs or reset source counters.
5. Missing optional source fields remain null/absent. Ambiguous required semantics fail or quarantine with a machine-readable reason.
6. No adapter is approved by this ADR. Exact HUST/Aurora mappings below are evidence-based candidates only.

## Verified source mapping candidates

- HUST five inspected complete payloads share `Status`, `Cycle number`, `Current (mA)`, `Voltage (V)`, `Capacity (mAh)`, `Time (s)` in every cycle frame. Candidate unit mappings are time→seconds, current mA→A, voltage→V. `dq` matches max-minus-final `Capacity (mAh)` in all 9,453 inspected cycle records; it may be converted mAh→Ah only after the remaining files are audited. `Status` is source-specific and not an approved step ID. See [DATA_CONTRACT.md](../../DATA_CONTRACT.md).
- Aurora all 199 Parquet files share six columns: `test_time_millisecond`, `current_ampere`, `voltage_volt`, `cycle_dimensionless`, `date_time_millisecond`, `ambient_temperature_celsius`. Time/current/voltage/temperature have explicit unit-bearing names. There is no capacity, energy, step, or status column. Aurora LFP cell `ccid000217` contains 506 returns of `cycle_dimensionless` to zero after increasing; preserve it as source-specific and do not normalize to a canonical cycle index pending authoritative boundary semantics.
- Aurora CSV/Parquet values matched for four sampled members. Parquet metadata reports no nulls in the common schema for all 199 cells.

## Evidence and limits

- [BDF specification](https://github.com/battery-data-alliance/battery-data-format) and [ontology](https://github.com/battery-data-alliance/battery-data-format-ontology); pin a release or commit before implementation.
- [HUST Mendeley v2](https://data.mendeley.com/datasets/nsc7hnsg4s/2), exact archive checksum and direct payload audit in [ARCH-01 evidence](../evidence/ARCH-01.md).
- [Aurora Zenodo v1](https://zenodo.org/records/15481956) and [original paper](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/batt.202500155); full inventory/schema/cycle audit in [ARCH-01 evidence](../evidence/ARCH-01.md).

The BDF-aligned vocabulary is a proposed architecture boundary, not a completed canonical schema contract. HUST source-wide verification and Aurora cycle/capacity semantics block adapter approval. No production code is authorized.
