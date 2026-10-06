# Project Status

## Current milestone

**FOUND-01 DONE; Architecture/Data Gate BLOCKED**

## Current task

**ARCH-01 — resolve ARCH-00 evidence blockers before any ingestion**

## Product state

- Project direction: LOCKED
- V1 product boundary: LOCKED
- ML required in V1: YES
- Coding implementation: FOUNDATION COMPLETE; source/domain implementation NOT STARTED
- Resume claims approved: NONE

## Current blockers

1. **HUST semantics blocker:** exact Mendeley v2 archive (`our_data.zip`), SHA-256, all 77 pickle member names, and one cell's serialized DataFrame schema were verified. The exact `dq` meaning/units and mapping to complete discharge cycles across all payloads, current sign, formation/early-cycle semantics, and source third-party notices remain unverified.
2. **Aurora data blocker:** Zenodo v1 record/license/archive checksum, 199 cell folders and each file-pattern trio, plus one JSON-LD cell metadata file were verified. The chemistry-specific cell IDs/counts, BDF CSV/Parquet row fields, cycle-index values, and capacity-field semantics have not been extracted from time-series members.
3. **Target blocker:** no common deterministic reference-capacity rule can be selected until exact source capacity fields and post-formation/reference-test semantics are verified. The first cycle is specifically not accepted as a denominator by assumption.
4. **Cross-source blocker:** only an LFP/graphite subset comparison is a candidate. It would combine source, format/design, temperature, and protocol shifts. The exact Aurora LFP subset and comparable capacity target have not been established.

## Last decision

On 2026-10-06, ARCH-00 PR [#4](https://github.com/s2002kumar/battery-reliability-platform/pull/4) was squash-merged into `main` at `60937a8dd9d2b13491a3c2a7826f3c618dab7c42`; its research disposition remains BLOCKED. FOUND-01 is implemented on `chore/FOUND-01-repository-foundation`; local gates and GitHub Actions runs [37508586503](https://github.com/s2002kumar/battery-reliability-platform/actions/runs/37508586503) and [37511473205](https://github.com/s2002kumar/battery-reliability-platform/actions/runs/37511473205) pass. FOUND-01 PR [#3](https://github.com/s2002kumar/battery-reliability-platform/pull/3) was created after green CI; its branch must be rebased onto updated `main` and CI rerun before squash merge. No ingestion or ML work is authorized while ARCH-00 remains BLOCKED. See [docs/evidence/ARCH-00.md](docs/evidence/ARCH-00.md) and [docs/evidence/FOUND-01.md](docs/evidence/FOUND-01.md).

## Update protocol

Every completed task must append:
- task ID;
- date;
- commit/PR;
- tests run;
- evidence path;
- known limitations;
- newly unblocked task(s).
