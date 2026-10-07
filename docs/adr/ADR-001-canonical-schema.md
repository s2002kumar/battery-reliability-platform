# ADR-001: Canonical Schema Boundary and BDF Alignment

- **Status:** Accepted for source selection and canonical field boundary; production adapter details remain subject to ARCH-REVIEW
- **Date:** 2026-10-07
- **Scope:** Canonical measurement vocabulary before adapters exist

## Context

V1 needs common battery measurements without erasing source semantics. The BDF format distinguishes required time/voltage/current from optional cycle, step, cumulative, cycle-capacity, step-capacity, and energy quantities. Source fields named “capacity” or “cycle” do not alone establish these meanings.

## Decision boundary

1. Align canonical measurement meaning and SI units to a pinned Battery Data Alliance BDF specification/ontology snapshot before implementation.
2. Preserve raw source names, values, source IDs, order, and sign. Keep project provenance, cell/test identity, quality, and lineage outside the BDF measurement vocabulary.
3. Use separate canonical fields for test-cumulative, per-cycle, and per-step charge/discharge capacity/energy. No unqualified `discharge_capacity_ah` field.
4. BDF current is positive for charge and negative for discharge. Preserve that convention; do not reverse signs or reset source counters.
5. Missing optional source fields remain null/absent. Ambiguous required semantics fail or quarantine with a machine-readable reason.
6. Source-native and derived values must remain distinguishable in lineage. Mappings below define architecture contracts; actual ingestion must still validate each artifact and quarantine records that fail them.

## Verified source mapping candidates

- HUST seven row-inspected payloads share `Status`, `Cycle number`, `Current (mA)`, `Voltage (V)`, `Capacity (mAh)`, `Time (s)` in every cycle frame. Map time to seconds, current mA to A, voltage to V, and `dq` mAh to cycle discharge capacity Ah. In all 13,517 inspected cycle records, `dq` matches max-minus-final `Capacity (mAh)` within 2.28e-13 mAh. The all-77 audit confirms filename/nested-cell identity and matching ordered `data`/`dq`/`rul` keys beginning at 1; row-level schema/null validation covers the seven stated payloads. `Status` remains source-specific, not a normalized step ID. See [DATA_CONTRACT.md](../../DATA_CONTRACT.md).
- Aurora all 199 Parquet files share six columns: `test_time_millisecond`, `current_ampere`, `voltage_volt`, `cycle_dimensionless`, `date_time_millisecond`, `ambient_temperature_celsius`. Time/current/voltage/temperature have explicit unit-bearing names. There is no source-reported capacity, energy, step, or status column. For the selected 32 LFP cells, direct JSON-LD protocol metadata and current/time traces support a separate derived event ordinal and trapezoid-integrated discharge capacity; preserve raw `cycle_dimensionless` resets. The derived event threshold yields exactly 1,003 events per LFP trace, matching the three conditioning plus 1,000 aging iterations.
- Aurora CSV/Parquet values matched for four sampled members. Parquet metadata reports no nulls in the common schema for all 199 cells.

## Evidence and limits

- [BDF specification](https://github.com/battery-data-alliance/battery-data-format) and [ontology](https://github.com/battery-data-alliance/battery-data-format-ontology); pin a release or commit before implementation.
- [HUST Mendeley v2](https://data.mendeley.com/datasets/nsc7hnsg4s/2), exact archive checksum and direct payload audit in [ARCH-01 evidence](../evidence/ARCH-01.md).
- [Aurora Zenodo v1](https://zenodo.org/records/15481956) and [original paper](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/batt.202500155); full inventory/schema/cycle audit in [ARCH-01 evidence](../evidence/ARCH-01.md).

The BDF-aligned measurement vocabulary and the source-specific HUST/Aurora LFP mapping decisions are approved for implementation planning. Pin the BDF specification/ontology revision and implement source-level validation/quarantine before declaring an adapter complete. This ADR does not authorize ingestion code by itself; INGEST tasks remain gated on architecture review and their task cards.
