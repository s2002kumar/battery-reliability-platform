# Work Queue

The queue is ordered by dependency and risk. Codex should always choose the highest-priority unblocked task.

Status values: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`.

| ID | Status | Task | Depends on |
|---|---|---|---|
| ARCH-00 | DONE | Direct dataset inspection, license verification, canonical schema freeze, SOH reference rule | — |
| ARCH-01 | DONE | Directly inspect source artifacts and resolve ARCH-00 blockers | ARCH-00 research recorded, FOUND-01 |
| FOUND-01 | DONE | Repository/package/config/test/CI foundation | — (architecture-independent; ARCH-00 research preserved) |
| INGEST-01 | BLOCKED | HUST immutable ingestion + provenance | FOUND-01, ARCH-00 PASS, ARCH-01 PASS, architecture review |
| INGEST-02 | BLOCKED | Empa/BDF source integration | INGEST-01 |
| QUAL-01 | BLOCKED | Validation, quarantine, known-bad fixtures | INGEST-02 |
| MODEL-01 | BLOCKED | Curated cell/test/cycle analytical model | QUAL-01 |
| REPLAY-01 | BLOCKED | Deterministic replay/backfill semantics | MODEL-01 |
| FEAT-01 | BLOCKED | Versioned leakage-safe feature dataset | MODEL-01, REPLAY-01 |
| ML-01 | BLOCKED | Naive + linear + boosted-tree baselines | FEAT-01 |
| ML-02 | BLOCKED | Held-out-cell evaluation | ML-01 |
| ML-03 | BLOCKED | Cross-source/domain-shift + uncertainty evaluation | ML-02 |
| MLOPS-01 | BLOCKED | MLflow experiment/model lineage | ML-03 |
| ORCH-01 | BLOCKED | Airflow orchestration and backfill controls | REPLAY-01, MLOPS-01 |
| CLOUD-01 | BLOCKED | AWS S3 execution/storage profile | ORCH-01 |
| PERF-01 | BLOCKED | Reproducible processing/query/feature/ML benchmarks | CLOUD-01 |
| SHOW-01 | BLOCKED | Read-only Battery Intelligence Console | PERF-01 |
| DEFENSE-01 | BLOCKED | Project defense + runbook/documentation pass | SHOW-01 |
| AUDIT-01 | BLOCKED | Claims/evidence audit and V1 release gate | DEFENSE-01 |

## ARCH-00 / ARCH-01 disposition (2026-10-07)

ARCH-00 and ARCH-01 are **DONE / PASS** for the documented source selection, BDF-aligned data boundary, source-aware SOH reference definition, and evaluation design. Direct inspection verified both exact archive checksums and authoritative CC BY 4.0 record terms; HUST's all-77 ordered label/key structures and first-window statistics, plus row-level schemas/capacity relation in seven named representative/edge cells; all 199 Aurora metadata/schema records; and LFP-specific protocol/event/capacity mappings for all 32 selected cells. HUST reference capacity is median `dq` over keys 1–3. Aurora LFP reference capacity is the median of the first three 1.0 mA cm⁻² aging discharge events after three metadata-defined conditioning events. Exclude reference windows from scored targets and group by `(source_name, source_record_version, source_native_cell_id)`. An exploratory HUST→Aurora LFP zero-shot combined-domain-shift evaluation is approved, with cell-design, temperature, batch, source/lab, and protocol differences stated explicitly. The exact 32 non-LFP metadata formulas `Ni0.83Mn0.06Co0.11O2` remain unreclassified and outside this SOH subset. Three Aurora cells each have one out-of-diagnostic-cutoff event requiring quarantine. HUST frame-level schema validation covers seven payloads; future ingestion must validate all members. These limitations are documented, not silently generalized.

INGEST-01 remains **BLOCKED** until architecture review and a scoped implementation task card authorize it. BDA/SINTEF/DLR fixtures are licensed catalog selections, but their bytes still need local verification in the future quality-fixture task. See [docs/evidence/ARCH-01.md](docs/evidence/ARCH-01.md), [docs/evidence/ARCH-00.md](docs/evidence/ARCH-00.md), [DATA_CONTRACT.md](DATA_CONTRACT.md), [ML_EVALUATION_PLAN.md](ML_EVALUATION_PLAN.md), and ADR-001 through ADR-004.

FOUND-01 is DONE and merged in PR #3. ARCH-00 research is merged in PR #4. ARCH-01 blocker-resolution research is recorded separately on `docs/ARCH-01-blocker-resolution`.

## Queue rules

- Do not skip ARCH-00.
- Do not mark a task DONE because code exists. Acceptance criteria, tests, and evidence must pass.
- When a task completes, unblock only tasks whose dependencies are all DONE.
- Architecture ambiguity means BLOCKED, not improvised scope.
- Each implementation task should have a dedicated card under `docs/task-cards/` before coding begins.
