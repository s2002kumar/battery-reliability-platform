# Project Status

## Current milestone

**Architecture/Data Gate — BLOCKED**

## Current task

**ARCH-00 — dataset inspection and architecture freeze**

## Product state

- Project direction: LOCKED
- V1 product boundary: LOCKED
- ML required in V1: YES
- Coding implementation: NOT STARTED
- Resume claims approved: NONE

## Current blockers

1. **HUST semantics blocker:** exact Mendeley v2 archive (`our_data.zip`), SHA-256, all 77 pickle member names, and one cell's serialized DataFrame schema were verified. The exact `dq` meaning/units and mapping to complete discharge cycles across all payloads, current sign, formation/early-cycle semantics, and source third-party notices remain unverified.
2. **Aurora data blocker:** Zenodo v1 record/license/archive checksum, 199 cell folders and each file-pattern trio, plus one JSON-LD cell metadata file were verified. The chemistry-specific cell IDs/counts, BDF CSV/Parquet row fields, cycle-index values, and capacity-field semantics have not been extracted from time-series members.
3. **Target blocker:** no common deterministic reference-capacity rule can be selected until exact source capacity fields and post-formation/reference-test semantics are verified. The first cycle is specifically not accepted as a denominator by assumption.
4. **Cross-source blocker:** only an LFP/graphite subset comparison is a candidate. It would combine source, format/design, temperature, and protocol shifts. The exact Aurora LFP subset and comparable capacity target have not been established.

## Last decision

On 2026-10-02, ARCH-00 research was documented as a blocked evidence state on branch `docs/ARCH-00-data-architecture`. Dataset records and licenses are recorded, but no exact raw files were retrieved into this repository, no canonical source mapping or SOH target is frozen, and no ingestion/model work is authorized. The commit is the current branch head. See [docs/evidence/ARCH-00.md](docs/evidence/ARCH-00.md).

## Update protocol

Every completed task must append:
- task ID;
- date;
- commit/PR;
- tests run;
- evidence path;
- known limitations;
- newly unblocked task(s).
