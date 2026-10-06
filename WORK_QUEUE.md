# Work Queue

The queue is ordered by dependency and risk. Codex should always choose the highest-priority unblocked task.

Status values: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`.

| ID | Status | Task | Depends on |
|---|---|---|---|
| ARCH-00 | BLOCKED | Direct dataset inspection, license verification, canonical schema freeze, SOH reference rule | — |
| FOUND-01 | DONE | Repository/package/config/test/CI foundation | — (architecture-independent; ARCH-00 research preserved) |
| INGEST-01 | BLOCKED | HUST immutable ingestion + provenance | FOUND-01, ARCH-00 PASS |
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

## ARCH-00 disposition (2026-10-02)

ARCH-00 is **BLOCKED**, not DONE. Exact HUST/Aurora archives and a subset of their internal metadata/schema are verified, but the HUST per-cycle `dq` semantics, Aurora BDF capacity fields, source reference windows, and exact Aurora LFP subset are unresolved. Candidate record licenses and the SINTEF/DLR fixture catalog were verified. See [docs/evidence/ARCH-00.md](docs/evidence/ARCH-00.md) and the four ADR research records under `docs/adr/`.

No downstream task is unblocked. Re-open ARCH-00 only after the exact HUST files and both sources' capacity/cycle semantics can be directly inspected, or after an explicit architecture decision changes scope.

FOUND-01 is proceeding independently on `chore/FOUND-01-repository-foundation`. Its completion does not change ARCH-00 status or authorize source ingestion.

FOUND-01 implementation and all local/CI acceptance checks pass (`docs/evidence/FOUND-01.md`). PR #3 has passing CI but must be rebased onto updated `main` and rechecked before squash merge. No downstream task is unblocked because ARCH-00 remains BLOCKED.

## Queue rules

- Do not skip ARCH-00.
- Do not mark a task DONE because code exists. Acceptance criteria, tests, and evidence must pass.
- When a task completes, unblock only tasks whose dependencies are all DONE.
- Architecture ambiguity means BLOCKED, not improvised scope.
- Each implementation task should have a dedicated card under `docs/task-cards/` before coding begins.
