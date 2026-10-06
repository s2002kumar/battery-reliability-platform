# Work Queue

The queue is ordered by dependency and risk. Codex should always choose the highest-priority unblocked task.

Status values: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`.

| ID | Status | Task | Depends on |
|---|---|---|---|
| ARCH-00 | BLOCKED | Direct dataset inspection, license verification, canonical schema freeze, SOH reference rule | — |
| ARCH-01 | BLOCKED | Directly inspect source artifacts and resolve ARCH-00 blockers | ARCH-00 research recorded, FOUND-01 |
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

## ARCH-00 / ARCH-01 disposition (2026-10-06)

ARCH-00 and ARCH-01 are **BLOCKED**, not DONE. Direct inspection verified both exact archive checksums, HUST `dq` semantics for five complete payloads, the Aurora chemistry inventory and common six-column schema for all 199 files, four CSV/Parquet pairs, and Aurora null statistics. Blockers remain: uninspected 72 HUST payloads and its unresolved third-party permission caveat; Aurora has no capacity/step/status field and LFP/32 Ni-rich NMC metadata cells have repeated cycle-count resets; the 32 metadata formulas `Ni0.83Mn0.06Co0.11O2` differ from the paper's stated NMC811 formula; no defensible common SOH reference-capacity rule is supported. Quantitative HUST-to-Aurora SOH evaluation is not approved. See [docs/evidence/ARCH-01.md](docs/evidence/ARCH-01.md), [docs/evidence/ARCH-00.md](docs/evidence/ARCH-00.md), the source contract, and ADR-001 through ADR-004.

No downstream task is unblocked. Stop for architecture/source-owner review before reopening the data gate. INGEST-01 remains blocked until ARCH-00 and ARCH-01 both pass and architecture review authorizes it.

FOUND-01 is DONE and merged in PR #3. ARCH-00 research is merged in PR #4 and remains BLOCKED. ARCH-01 is research-only and adds no ingestion authority.

## Queue rules

- Do not skip ARCH-00.
- Do not mark a task DONE because code exists. Acceptance criteria, tests, and evidence must pass.
- When a task completes, unblock only tasks whose dependencies are all DONE.
- Architecture ambiguity means BLOCKED, not improvised scope.
- Each implementation task should have a dedicated card under `docs/task-cards/` before coding begins.
