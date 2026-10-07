# Data Contract — Verified BDF-Aligned Boundary, ARCH-00/ARCH-01 PASS

This document records the canonical boundary and source mappings verified for the selected HUST archive and Aurora LFP subset. **SOH architecture is approved; production ingestion still requires architecture review and its own task card.** Aurora lacks a source-reported capacity field and its native cycle counter resets, but direct LFP metadata and traces support a protocol-aligned derived discharge event/capacity. HUST's 77 payload key/label structures and first-window statistics were audited; seven representative/edge payloads (13,517 cycles) received full frame-level schema and `dq` comparisons. The Mendeley record grants CC BY 4.0 rights for licensed material, subject to any separately identified third-party content. Preserve native fields and quarantine ambiguous or out-of-protocol rows; do not silently coerce them.

## Identity and provenance

| Field | Contract status | Rule |
|---|---|---|
| `source_name`, `source_record_uri`, `source_record_version` | Required | Stable registered source, canonical record/DOI, immutable version. |
| `source_artifact_id`, `source_file_name`, `source_sha256`, `source_size_bytes` | Required | Exact immutable artifact and source member; hash original bytes locally with SHA-256. Keep source MD5 only as upstream metadata. |
| `retrieved_at_utc`, `license_id`, `attribution`, `usage_notes` | Required on artifact manifest | Record exact record/file terms and source notices; no inferred license. |
| `adapter_name`, `adapter_version` | Required on derived rows | Exact parser build that emitted canonical data. |
| `cell_id` | Required for cell/cycle analytics | Source-native physical cell identity, namespaced by source and version. If identity is missing/ambiguous, exclude from cell-level ML. |
| `test_id` | Required for test analytics | Source test/run identifier, or deterministic artifact-scoped ID only when one file is verified to contain one test. |
| Split group key | Required | `(source_name, source_record_version, source_native_cell_id)`. Keep all tests/files/cycles for that physical cell in one partition. |

HUST's nested payload key (e.g. `1-1`) and Aurora's `ccid000XXX` product/file identifier are directly observed physical-cell identifiers in the inspected artifacts. They remain source-specific strings; never join across sources on their textual value. Aurora `schema:productID` contains both a batch/assembly identifier and the `empa__ccid...` dataset identifier; preserve both metadata values without treating the batch value as another cell.

## Canonical BDF-aligned measurement vocabulary

Keep time, current, and voltage distinct and unit-normalized. BDF's current convention is positive for charge and negative for discharge. Preserve source timestamps, current signs, native index values, and raw values; record every unit conversion as a deterministic derivation.

| Canonical field | Status | Contract meaning |
|---|---|---|
| `test_time_s` | Required for accepted measurement rows | Elapsed test time in seconds. Convert only where exact source unit is explicit; preserve order and pause behavior. |
| `voltage_v` | Required for measurement rows | Terminal voltage in volts. |
| `current_a` | Required for measurement rows | Current in amperes; positive charges, negative discharges. |
| `unix_time_s` | Optional, nullable | UTC Unix time in seconds only where source epoch/unit/timezone are documented. |
| `ambient_temperature_c` | Optional, nullable | Ambient temperature; do not substitute surface or internal sensor channels. |
| `cycle_index` | Optional, nullable, derived | Emit only for a source field with validated cycle semantics or a separately documented, versioned event derivation. Preserve the raw source index even when a derived logical cycle ordinal is available. |
| `step_count`, `step_id`, `step_record_index`, `step_time_s` | Optional, nullable/derived | Distinct meanings. A source field named `step` or a cycle-count reset is not automatically one of these. Derived indexes need method/version. |
| `cycle_charging_capacity_ah`, `cycle_discharging_capacity_ah` | Optional, nullable, source-validated or derived | Complete per-cycle capacity in Ah; never substitute test-cumulative or step capacity. Aurora LFP discharge capacity is a versioned current/time integration; HUST discharge capacity is the source `dq` measurement. |
| `charging_capacity_ah`, `discharging_capacity_ah` | Optional, nullable, source-validated | Test-cumulative capacities, distinct from per-cycle and per-step values. |
| Step charge/discharge capacity and energy | Optional, nullable, source-validated | Preserve step-specific quantities separately; energy is never a capacity substitute. |
| `record_index` | Derived, optional | Stable source row order only; retain derivation method/version. |
| SOH and `reference_capacity_ah` | Derived, approved definition | Use ADR-003's source-aware median of the first three complete discharge capacities in the sustained aging protocol. Preserve capacity lineage; denominator is target metadata, never a predictor. |

Missing optional values remain null/absent, never zero. If a required measurement is null or an optional field's meaning is ambiguous, reject/quarantine with a machine-readable reason and source locator. Do not coerce suspect data.

## Exact inspected source mappings

### HUST Mendeley v2

| Source field | Canonical disposition | Evidence and boundary |
|---|---|---|
| `Time (s)` | Candidate direct `test_time_s` | Present in all cycles of seven safely inspected cell payloads; source unit is explicit in field name. Full 77-file null/order audit remains outstanding. |
| `Current (mA)` | Candidate `current_a = value / 1000` | Positive charge and negative discharge observed by `Status` in seven cells. Do not erase the original field. |
| `Voltage (V)` | Candidate direct `voltage_v` | Exact name/unit in seven cells; source-wide null audit outstanding. |
| `Cycle number` | Preserve source value; map to `cycle_index` | Equals the containing `data` map key in all 13,517 frames across seven representative/edge payloads. Across all 77 payloads, `data`, `dq`, and `rul` key sets/order match and start at key 1; frame-level validation coverage is seven payloads. |
| `Status` | Source-specific step/protocol label | Six observed CC/CV/numbered discharge values; no mapping to canonical `step_count` or `step_id` is established. |
| `Capacity (mAh)` | Preserve as raw source-specific signal | Value rises through charge and falls during discharge; not itself complete discharge capacity. |
| `dq` | `cycle_discharging_capacity_ah = dq / 1000` | In all 13,517 cycles in seven representative/edge payloads, `dq` matches `max(Capacity) - final Capacity` within `2.28e-13 mAh`. All 77 payload label maps align with cycle maps. Treat `dq` as target-only; never a predictor. |
| `rul` | Source target/derived label; forbidden as predictor | Author preprocessing code uses it as RUL label. |

Seven sampled cell payloads have the same six-column schema across every cycle; all observed fields are non-null in these seven. The other 70 payloads were deserialized for key/label-order and early-window audit but their DataFrame rows were not individually inspected; adapter validation must enforce the six-column sample schema and quarantine deviations. Across all 77 cells, first-three `dq` windows have a maximum range of 0.724% of the median and median range of 0.154%, supporting the operational baseline defined in ADR-003. No cycle is designated “formation” by the inspected payload or author code. The author code dropping its first nine ordered `dq` keys is evidence of preprocessing choice, not proof those cycles are formation.

### Empa Aurora Zenodo v1

| Exact Parquet/CSV field | Canonical disposition | Directly observed meaning / limitation |
|---|---|---|
| `test_time_millisecond` (int64) | `test_time_s = value / 1000` | Explicit millisecond unit; preserve source row order. Monotonicity has not been audited across every source row. All 199 Parquet statistics report no nulls. |
| `current_ampere` (float64) | `current_a` | Ampere explicit; both signs occur in all 199 records. Sign meaning follows BDF (positive charge, negative discharge). |
| `voltage_volt` (float64) | `voltage_v` | Volt explicit; all 199 Parquet stats available with no reported nulls. |
| `date_time_millisecond` (int64) | `unix_time_s = value / 1000` | Millisecond Unix timestamps are observed; preserve original integer too. Validate UTC epoch semantics before emitting the canonical timestamp. |
| `ambient_temperature_celsius` (float64) | `ambient_temperature_c` | Celsius explicit; all 199 files' statistics report 25.0, no nulls. |
| `cycle_dimensionless` (int64) | Preserve source-specific; do not map directly | Values start at zero and reset; in `ccid000217` it returns to zero 506 times after increasing. Preserve exact native values. A separate logical cycle ordinal is derived from ordered substantive discharge events and exact per-cell protocol metadata; record derivation/version and source locator. |
| No capacity or energy field | Derived discharge capacity, source-validated | Integrate absolute `current_ampere` over `test_time_millisecond` by trapezoid for each substantive negative-current discharge event. A fixed 0.1 mAh cut falls in the observed >64× gap between zero-duration artifacts (max 0.00428 mAh) and discharge events (min 0.2757 mAh); all 32 LFP files yield 1,003 events, matching three conditioning plus 1,000 aging iterations. Record the derived Ah value separately from rated-capacity metadata. Quarantine event quality failures; three cells each have one event outside the 0.08 V cutoff diagnostic. |

All 199 Parquet files expose the same six-field schema and report zero nulls in the inspected Parquet statistics. Exact CSV/Parquet schema and values matched for four records across the observed chemistries. The BDF specification uses a distinct ontology for cycle, step, cumulative, capacity, and energy quantities; a source name containing “cycle” alone does not prove the event boundary.

## Source metadata

Chemistry/electrode formula, cell format, manufacturer, rated capacity, assembly, electrolyte, protocol tasks, current density, voltage cutoffs, and dates are optional source metadata and remain nullable if not reported. Keep source term, unit, and raw JSON-LD path. Aurora JSON-LD confirms NMC622, LFP, and 32 positive-electrode formulas `Ni0.83Mn0.06Co0.11O2`. The last formula differs from the primary paper's stated NMC811 composition `LiNi0.83Mn0.10Co0.07O2`; keep the formula exact and classification unresolved pending clarification. Do not convert areal or gravimetric rated-capacity metadata into Ah/cycle capacity. HUST paper-level chemistry and nominal capacity are documented metadata, not measured per-cycle target fields.

## SOH target and leakage state

`SOH = available_discharge_capacity / reference_capacity` is approved as a source-aware, within-cell target. In both sources, reference capacity is the median of the first three complete discharge capacities in the sustained aging protocol: HUST keys 1–3; Aurora LFP the first three events after its metadata-defined three-event low-rate phase. Exclude baseline observations from scored targets. HUST capacity is `dq`; Aurora capacity is a reproducible integrated derivation. See [ADR-003](docs/adr/ADR-003-soh-reference-and-leakage.md) and the complete [evaluation plan](ML_EVALUATION_PLAN.md). This normalized target does not make absolute capacities comparable across sources.

Always exclude the current target capacity and aliases, SOH/EOL/RUL labels, denominator, future cycles, full-life summaries, and unknown-reset cumulative measures from predictors. Keep cell/source/file/test/protocol IDs as grouping/stratification metadata, not model inputs by default. Cycle number, elapsed age, and throughput need a declared prediction-time cutoff and a separate leakage review before feature approval.

## BDF reference

Use the [Battery Data Alliance BDF specification](https://github.com/battery-data-alliance/battery-data-format) and [ontology](https://github.com/battery-data-alliance/battery-data-format-ontology) as the semantic authority. Their current repository is mutable; pin a release/commit before implementation. The observed Aurora column names are the dataset's exact columns; preserve them alongside any unit conversion and do not make undocumented broad “BDF-compliant” claims.
