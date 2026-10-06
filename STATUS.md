# Project Status

## Current milestone

**ARCH-00 / ARCH-01 architecture and data gate: BLOCKED**

## Current task

**ARCH-01 — direct source inspection completed to a blocked research disposition; stop for architecture/source-owner review.**

## Product state

- Project direction: LOCKED
- V1 product boundary: LOCKED
- ML required in V1: YES
- Coding implementation: FOUNDATION COMPLETE; source/domain implementation NOT STARTED
- Resume claims approved: NONE

## Current blockers

1. **HUST source-wide evidence/rights:** `dq` matches the measured discharge relation in all cycles of five complete payloads, but 72 of 77 payloads have not been deserialized/audited. The authoritative Mendeley record's CC BY 4.0 is explicit, but its third-party permission warning cannot be resolved from the archive's lack of an in-archive rights manifest. Do not redistribute until applicable third-party content is clarified.
2. **Aurora cycle/capacity/chemistry mapping:** all 199 cells and schemas are inventoried; no capacity, step, status, or energy field exists. `cycle_dimensionless` repeatedly returns to zero in LFP and 32 Ni-rich NMC metadata records. Those records' `Ni0.83Mn0.06Co0.11O2` formula differs from the primary paper's stated NMC811 `LiNi0.83Mn0.10Co0.07O2`; retain the discrepancy unresolved. The source does not supply enough step/status data to map cycle resets to complete discharges without a non-verified rule.
3. **SOH reference rule:** no deterministic reference capacity is approved. HUST has no source-declared formation/reference window. Aurora's paper describes three formation cycles for its NMC622 case; do not generalize this phase count to LFP. Aurora's LFP cycle mapping is unresolved. Rated/nominal capacity, single first cycle, full-life maximum, and arbitrary early windows are rejected.
4. **Cross-source evaluation:** quantitative HUST→Aurora SOH metrics are blocked. Same-chemistry LFP is a future candidate, but combines source/lab, cylindrical vs coin-cell design, temperature, electrode batch, formation, and protocol shifts; target/reference semantics do not align yet.

## Last decision

On 2026-10-06, the ARCH-01 audit verified the exact HUST Mendeley v2 archive and Aurora Zenodo v1 archive outside Git and recorded locally computed checksums, all 199 Aurora metadata/schema records, and five full HUST payloads. The gate remains BLOCKED because source-wide HUST evidence/third-party rights, Aurora cycle/capacity grouping, and a defensible common reference rule are unresolved. ARCH-01 work is isolated on `docs/ARCH-01-blocker-resolution`; no ingestion, feature, or model work is authorized. See [docs/evidence/ARCH-01.md](docs/evidence/ARCH-01.md) and the updated [ARCH-00 audit](docs/evidence/ARCH-00.md).

FOUND-01 is DONE and merged to `main` in PR [#3](https://github.com/s2002kumar/battery-reliability-platform/pull/3) at `4784bd6fc54b87fff73f825b2ab946e2c7774657`. ARCH-00 research is merged in PR [#4](https://github.com/s2002kumar/battery-reliability-platform/pull/4) at `60937a8dd9d2b13491a3c2a7826f3c618dab7c42` and remains BLOCKED.

## Update protocol

Every completed or blocked task must append its task ID, date, commit/PR, checks, evidence path, limitations, and newly unblocked task(s). A BLOCKED task unblocks nothing.
