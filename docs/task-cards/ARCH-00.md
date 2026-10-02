# ARCH-00 — Dataset Inspection and Architecture Freeze

## Objective

Verify the exact V1 data sources and freeze the canonical schema, redistribution policy, and SOH target/reference-capacity rule before implementation begins.

## Context

The product direction is locked, but implementation depends on direct inspection of real source files and authoritative license/terms metadata.

## Scope

1. Inspect the exact HUST dataset record/files.
2. Inspect the exact Empa Aurora dataset record/files.
3. Inspect BDA/SINTEF/DLR robustness fixtures that may be used in tests.
4. Record exact source URLs, versions, file names, sizes, hashes when available, schema summaries, and licenses/terms.
5. Confirm which source bytes may or may not be redistributed.
6. Map source fields to the draft BDF-aligned canonical contract.
7. Determine whether each source contains a defensible capacity signal for SOH.
8. Freeze the reference-capacity rule.
9. Decide which source is primary supervised-ML data and which is cross-source/domain-shift data.
10. Write required ADRs.

## Required outputs

- updated `DATA_SOURCES.md`
- frozen `DATA_CONTRACT.md`
- frozen `ML_EVALUATION_PLAN.md`
- `docs/adr/ADR-001-canonical-schema.md`
- `docs/adr/ADR-002-storage-versioning.md`
- `docs/adr/ADR-003-soh-reference-and-leakage.md`
- `docs/adr/ADR-004-source-selection-and-redistribution.md`
- `docs/evidence/ARCH-00.md`

## Acceptance criteria

- authoritative license/terms source exists for every selected dataset/fixture;
- no redistribution claim is inferred from a secondary source;
- exact source files needed for V1 are identified;
- canonical field mapping covers the selected sources without silent semantic coercion;
- nullable/optional behavior is explicit;
- SOH numerator and reference-capacity denominator are deterministic and source-aware;
- target leakage risks are documented;
- grouped-cell split key is unambiguous;
- cross-source evaluation is technically meaningful or explicitly narrowed with rationale;
- no production code is added.

## Stop conditions

Mark BLOCKED and stop if:
- a required source license cannot be verified;
- target construction cannot be made comparable/defensible;
- BDF/source semantics conflict in a way requiring product redesign;
- cross-source comparison would be scientifically misleading.

## Excluded work

- ingestion implementation
- pipeline code
- model training
- Airflow
- cloud deployment
- UI
