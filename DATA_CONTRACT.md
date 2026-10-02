# Data Contract — Draft Gate

This file defines the project-owned contract. BDF alignment informs battery measurement semantics but does not replace provenance, identity, quality, or feature-lineage requirements.

## Canonical measurement minimum

Required when present in a compatible source:

- source_name
- source_artifact_id
- cell_id
- test_id
- test_time_s
- voltage_v
- current_a

Optional normalized measurements include:

- cycle_index
- step_index
- temperature_c
- charge_capacity_ah
- discharge_capacity_ah
- charge_energy_wh
- discharge_energy_wh

## Contract rules

- Normalized units are explicit in field names.
- Source-native values remain traceable through provenance.
- Missing is not zero.
- Source IDs are never assumed globally unique.
- Validation never silently invents missing cycle/step labels.
- Derived cycle boundaries must carry a method/version identifier.
- Any source-specific coercion must be documented and tested.
- Ambiguous values are quarantined or explicitly flagged, not guessed.

## Not yet frozen

Exact nullable constraints, cycle derivation semantics, canonical metadata fields, and source-specific mappings remain ARCH-00 decisions.
