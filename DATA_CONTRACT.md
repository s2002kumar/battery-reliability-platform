# Data Contract — ARCH-00 Proposed Boundary

**ARCH-00 status: BLOCKED; this contract is not frozen for source ingestion.** The BDF-aligned vocabulary and null-handling policy below are proposed project constraints. A sampled HUST payload and one Aurora metadata member were inspected, but exact source mappings, nullability, cycle roll-up, and SOH capacity semantics remain open. No adapter may infer those mappings.

## Identity and provenance

| Field | Status | Contract |
|---|---|---|
| `source_name` | Required | Stable registered source identifier, e.g. `hust_mendeley_v2`, `empa_aurora_zenodo_v1`; never inferred from a cell ID alone. |
| `source_record_uri` | Required | DOI/record URI plus immutable source version. |
| `source_artifact_id` | Required | Project artifact-manifest ID for the exact immutable source file. |
| `source_file_name` | Required | Exact upstream file key, retained byte-for-byte as metadata. |
| `source_sha256` | Required | SHA-256 of original bytes after retrieval; source record MD5 may be retained separately but is not a substitute. |
| `adapter_name`, `adapter_version` | Required on derived rows | Exact parser/adapter build that emitted the row. |
| `ingested_at_utc` | Required on manifest | UTC timestamp; do not copy this as a cell observation time. |
| `license_id`, `attribution`, `usage_notes` | Required on manifest | Exact source-record/file terms and applicable attribution, not a guessed repository-wide default. |
| `cell_id` | Required for cell/cycle analytics | Source-native physical cell identity, namespaced by source and version. If absent or ambiguous, quarantine from cell-level ML; never use row order or filename guesses. |
| `test_id` | Required for test/cycle analytics | Source-native test/run ID or a deterministic artifact-scoped ID only when one file is confirmed to contain one test. If test boundaries are ambiguous, quarantine the analytic partition. |

The physical-cell split/group key is the tuple `(source_name, source_record_version, source_native_cell_id)`. This is stable across files for one cell and prevents identifiers reused by different sources from joining. A test ID is not a cell identity.

## Canonical BDF-aligned measurements

Canonical units are encoded in field names. BDF's required measurements are current, elapsed test time, and terminal voltage. BDF positive current means charge; negative current means discharge. Preserve native signs and cumulative measures; do not reverse signs or reset values to force a preferred convention.

| Canonical field | Status / nullability | BDF concept or rule |
|---|---|---|
| `test_time_s` | Required measurement; nullable only when source row has a documented non-measurement record, otherwise reject/quarantine | BDF `Test Time / s`; elapsed test time, non-decreasing within a test; preserve source pause behavior. |
| `voltage_v` | Required measurement; null is invalid for a measurement row | BDF `Voltage / V`. |
| `current_a` | Required measurement; null is invalid for a measurement row | BDF `Current / A`; positive charges, negative discharges. |
| `cycle_index` | Optional, nullable only when source does not supply or unambiguously define a cycle count | Preserve source BDF `Cycle Count / 1` verbatim; starting value is instrument-defined; non-negative and non-decreasing. Do not renumber. |
| `step_count` | Optional, nullable | BDF `Step Count / 1` is the monotonically increasing step-execution count. Preserve the source value; do not renumber. |
| `step_id` | Optional, source-specific, nullable | Preserve instrument/test-program ID. Do not map a column merely named “Step Index” here without checking its documented semantics. |
| `step_record_index` | Optional, derived only under a versioned derivation | BDF within-step point position; it is not the instrument program's `Step ID`. |
| `step_time_s` | Optional, nullable | BDF step elapsed time; resets at step transitions. |
| `ambient_temperature_c` | Optional, nullable | BDF ambient temperature. Surface/auxiliary sensor channels remain separate fields and are not synonyms. |
| `unix_time_s` | Optional, nullable | Absolute UTC Unix time only if supplied as such; do not derive from local timestamps without timezone evidence. |
| `cycle_charging_capacity_ah`, `cycle_discharging_capacity_ah` | Optional, nullable, distinct measures | BDF cycle capacities: non-negative within current cycle and reset at cycle transition. `cycle_discharging_capacity_ah` is the candidate SOH numerator only after source-specific validation. |
| `charging_capacity_ah`, `discharging_capacity_ah` | Optional, nullable, distinct cumulative test measures | BDF charge/discharge capacity since test start; do not confuse these with cycle capacity or a single step's capacity. |
| `step_charging_capacity_ah`, `step_discharging_capacity_ah` | Optional, nullable, distinct measures | BDF step-specific capacities; valid only for the named step execution. |
| Energy fields | Optional, nullable, separate charge/discharge/cumulative/cycle/step concepts | Preserve the BDF ontology distinction and units; do not substitute energy for capacity. |
| `record_index` | Optional, derived only if source ordering is preserved and method/version is recorded | BDF ordinal record order, not physical time. |

`discharge_capacity_ah` is rejected as an unqualified canonical name: it does not distinguish a step quantity, cycle capacity, or test-cumulative discharge capacity. A source column called “Step Index” is not automatically `step_count` or `step_record_index`; inspect its behavior and source documentation first. No source-specific column is mapped to any capacity field until the column definition and reset/accumulation behavior are verified from the exact file and protocol metadata.

## Cell, test, cycle, and protocol metadata

| Field group | Status |
|---|---|
| Cell chemistry/electrodes, format, manufacturer/model, nominal capacity/voltage | Optional source metadata; nullable when not reported; preserve source terms and original units/strings. No chemistry inferred from a filename token alone. |
| Test protocol, charge/discharge stages, rates, cutoffs, temperature control, instrument/cycler | Optional source metadata; required for source-comparability decisions; unknown stays unknown. |
| Native cell/test/cycle/step identifiers | Preserve as source-specific strings/numbers; null only when absent; never repair or renumber without a documented deterministic mapping. |
| Cycle boundaries | Optional derived entity only with method/version and evidence. Do not derive from current sign alone when source protocol semantics are unavailable. |
| Quality flags / quarantine reason | Optional for accepted records, required for rejected/quarantined records; machine-readable reason and source row/artifact locator. |
| SOH target and reference capacity | Derived, versioned, and currently unavailable/unfrozen. Never store as if it were a source measurement. |

## Source mapping inventory (observed, not adapter approval)

| Source/artifact | Observed upstream field or metadata | Canonical disposition | Status / reason |
|---|---|---|---|
| HUST `our_data/1-1.pkl`, nested `data` DataFrame | `Time (s)`, `Voltage (V)`, `Current (mA)` | Candidate `test_time_s`, `voltage_v`, `current_a` after unit, sign, ordering, and row-semantics validation | Names and units observed in one member; sign, nulls, and time semantics not verified across files. No mapping approved. |
| HUST nested `data` DataFrame | `Cycle number`, `Status`, `Capacity (mAh)` | Preserve as source-specific raw columns pending semantics; do not map to canonical `cycle_index`, step fields, or capacity measures yet | One sampled member only; cycle/step values and `Capacity (mAh)` reset/accumulation meaning unknown. |
| HUST serialized object / author preprocessing interface | `dq`, `rul`, `data` | Preserve `dq` and `rul` as source-specific labels; exclude both and aliases from predictors | Author code uses `dq[cycle]` as capacity label and `rul[cycle]` as RUL label. `dq` unit and complete-cycle meaning are unresolved. |
| Aurora per-cell metadata JSON-LD, sampled `ccid000001` | Cell/product IDs, date, creator/manufacturer, electrode composition/properties, rated-capacity metadata, generated protocol | Candidate source-specific cell/test metadata; map only fields whose definitions and units are confirmed in each record | One NMC622//graphite cell was inspected; population and exact metadata keys/units have not been fully inventoried. |
| Aurora `.bdf.csv` / `.bdf.parquet` | Record says these are per-cell BDF time series; actual rows not inspected | Expected BDF concepts are in the vocabulary table above; no source field mapped | Headers, cycle index values, capacity fields, null behavior, and CSV/Parquet equality have not been directly checked. |
| SINTEF/DLR selected fixtures | Catalog filename, lab, chemistry/test description, file type, license and listed defect | Fixture provenance/quality metadata only; no canonical measurement mapping | Fixture bytes and row schemas were not parsed; they are not SOH observations. |

## Missing, unavailable, and invalid values

- Missing is null or a manifest-level unavailable declaration, never zero.
- A field unavailable in a source remains absent/null; adapters do not synthesize it.
- An optional field that exists but has an ambiguous meaning is not nullable-clean data: quarantine the affected source partition with the ambiguity reason.
- A measurement row lacking required current, time, or voltage is invalid unless the source format explicitly identifies a non-measurement row.
- Only the single-member HUST observations and one Aurora metadata sample above are verified. Exact HUST capacity semantics, all native identifiers/cycle semantics, Aurora BDF columns, and per-source null behavior remain **unverified**. The mapping inventory is evidence, not adapter approval.

## BDF reference

Use the [Battery Data Alliance BDF specification](https://github.com/battery-data-alliance/battery-data-format) and its [machine-readable ontology](https://github.com/battery-data-alliance/battery-data-format-ontology) as the semantic authority for BDF-aligned fields. Pin a released specification/ontology snapshot in implementation; a mutable `main` branch is not a reproducible schema version.
