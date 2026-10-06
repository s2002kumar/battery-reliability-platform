# Project Status

## Current milestone

**Repository Foundation in Progress; Architecture/Data Gate BLOCKED**

## Current task

**FOUND-01 — architecture-independent repository foundation**

## Product state

- Project direction: LOCKED
- V1 product boundary: LOCKED
- ML required in V1: YES
- Coding implementation: FOUNDATION ONLY; source/domain implementation NOT STARTED
- Resume claims approved: NONE

## Current blockers

1. **HUST semantics blocker:** exact Mendeley v2 archive (`our_data.zip`), SHA-256, all 77 pickle member names, and one cell's serialized DataFrame schema were verified. The exact `dq` meaning/units and mapping to complete discharge cycles across all payloads, current sign, formation/early-cycle semantics, and source third-party notices remain unverified.
2. **Aurora data blocker:** Zenodo v1 record/license/archive checksum, 199 cell folders and each file-pattern trio, plus one JSON-LD cell metadata file were verified. The chemistry-specific cell IDs/counts, BDF CSV/Parquet row fields, cycle-index values, and capacity-field semantics have not been extracted from time-series members.
3. **Target blocker:** no common deterministic reference-capacity rule can be selected until exact source capacity fields and post-formation/reference-test semantics are verified. The first cycle is specifically not accepted as a denominator by assumption.
4. **Cross-source blocker:** only an LFP/graphite subset comparison is a candidate. It would combine source, format/design, temperature, and protocol shifts. The exact Aurora LFP subset and comparable capacity target have not been established.

## Last decision

On 2026-10-06, ARCH-00 commit `162ad0e963d23e7a65bb2dba718a37f53b674515` was pushed on `docs/ARCH-00-data-architecture` and fast-forwarded into local `main` because remote `main` was its ancestor. GitHub CLI authentication is invalid, so a PR could not be created; the pushed branch remains available for PR creation. ARCH-00 remains BLOCKED. FOUND-01 is in progress on `chore/FOUND-01-repository-foundation`; this foundation work does not authorize ingestion or ML work. See [docs/evidence/ARCH-00.md](docs/evidence/ARCH-00.md).

## Update protocol

Every completed task must append:
- task ID;
- date;
- commit/PR;
- tests run;
- evidence path;
- known limitations;
- newly unblocked task(s).
