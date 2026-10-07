# Project Status

## Current milestone

**ARCH-00 / ARCH-01 data and ML architecture gate: PASS; architecture review required before ingestion.**

## Current task

**ARCH-01 — direct source inspection and blocker-resolution decision completed.** Research and architecture documents only; no ingestion, feature, or model implementation was started.

## Product state

- Project direction: LOCKED
- V1 product boundary: LOCKED
- ML required in V1: YES
- Coding implementation: FOUNDATION COMPLETE; source/domain implementation NOT STARTED
- Resume claims approved: NONE

## Verified decisions and limitations

1. **HUST:** exact Mendeley v2 archive has 77 pickle members. All 77 payloads were safely deserialized for filename/cell identity, `data`/`dq`/`rul` key-set/order alignment, and early-window label stability. Seven named representative/edge payloads received full frame-level inspection across 13,517 cycles and 8,641,884 rows; `dq` matches max-minus-final `Capacity (mAh)` within 2.28e-13 mAh. Across 77 cells, first-three `dq` windows have a maximum range of 0.724% of the median (median 0.154%). Frame-level schema/null coverage remains seven payloads; ingestion must validate every member and quarantine deviations.
2. **Aurora:** all 199 metadata records and Parquet schemas are inventoried; the exact SOH subset is 32 LFP/graphite cells. Their metadata directly specifies three low-rate cycles followed by 1,000 aging cycles. All 32 time series yield 1,003 substantive current-integrated discharge events aligned to that protocol. Preserve the raw resetting `cycle_dimensionless`; derive an auditable event ordinal and capacity. Three cells have one event each outside the 0.08 V cutoff diagnostic; quarantine those events. The separate 32 formula records `Ni0.83Mn0.06Co0.11O2` still differ from the paper's stated NMC811 formula; they are outside the selected SOH subset and remain unreclassified.
3. **SOH:** use the median capacity of the first three complete discharges in each cell's sustained aging protocol. HUST uses `dq` keys 1–3; Aurora LFP uses the first three aging events after its metadata-declared three-cycle low-rate phase. Exclude reference cycles from scored targets. This is a within-cell normalized target, not absolute cross-source capacity.
4. **Evaluation:** approve grouped held-out-cell evaluation and a bounded exploratory zero-shot HUST→Aurora LFP combined-domain-shift test after ingestion/evaluation tasks pass. This simultaneously shifts lab/source, cylindrical vs coin-cell design, temperature, batch, and protocol; it does not isolate any one cause. Also retain HUST unseen-protocol holdout. Full leakage and grouping policy is in `ML_EVALUATION_PLAN.md`.
5. **Rights/fixtures:** HUST Mendeley v2 and Aurora Zenodo v1 explicitly declare CC BY 4.0. HUST's exact archive has no identified third-party component; record-level redistribution is permitted for licensed material with attribution, license link, and change notice. SINTEF/DLR fixture candidates have record/catalog-level CC BY terms and exact bug classifications; local fixture bytes remain to be verified before making parser test claims.

## Last decision

ARCH-00 and ARCH-01 pass their research/architecture gates based on the exact archive checksums, primary terms, direct data inspection, reproducible audit scripts, and documented limitations. See [ARCH-00 evidence](docs/evidence/ARCH-00.md), [ARCH-01 evidence](docs/evidence/ARCH-01.md), ADR-001 through ADR-004, and the source/contract/evaluation documents. This does not itself authorize INGEST-01: the required architecture review and scoped implementation task card remain prerequisites.

FOUND-01 is DONE and merged to `main` in PR [#3](https://github.com/s2002kumar/battery-reliability-platform/pull/3) at `4784bd6fc54b87fff73f825b2ab946e2c7774657`. ARCH-00 research is merged in PR [#4](https://github.com/s2002kumar/battery-reliability-platform/pull/4) at `60937a8dd9d2b13491a3c2a7826f3c618dab7c42`. ARCH-01 research is isolated on `docs/ARCH-01-blocker-resolution` and recorded in its task commit.

## Update protocol

Every completed or blocked task must record its task ID, date, commit/PR, checks, evidence path, limitations, and newly unblocked task(s). A blocked task unblocks nothing.
