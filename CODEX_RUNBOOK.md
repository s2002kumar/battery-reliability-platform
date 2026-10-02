# Codex Runbook

This repository is designed for long-running, queue-driven Codex execution with human architecture gates.

## Start-of-run command

Use a persistent Codex Goal or equivalent long-running task with this instruction:

> Complete recruiter-ready V1 of the Battery Reliability & Degradation Intelligence Platform according to PROJECT_SPEC.md and WORK_QUEUE.md. Treat AGENTS.md as mandatory operating policy. Work through tasks in dependency order. Before each task, read its task card. Inspect first, implement only approved scope, run required verification, generate evidence, update STATUS.md and WORK_QUEUE.md, and commit the completed change before moving to the next task. Never alter locked product architecture, ML evaluation rules, dataset licenses, or technology gates without stopping and recording an architecture blocker. V1 is complete only when QUALITY_GATES.md passes in full.

## Autonomous loop

For each cycle:

1. Read `AGENTS.md`.
2. Read `PROJECT_SPEC.md`.
3. Read `ARCHITECTURE.md`.
4. Read `STATUS.md`.
5. Read `WORK_QUEUE.md`.
6. Find the first `TODO` item whose dependencies are all `DONE`.
7. Read `docs/task-cards/<TASK_ID>.md`.
8. Inspect existing files/interfaces before coding.
9. Mark task `IN_PROGRESS` in queue/status.
10. Implement the smallest coherent change.
11. Add/modify tests.
12. Run required checks.
13. Produce/update `docs/evidence/<TASK_ID>.md`.
14. Audit acceptance criteria.
15. If PASS:
    - mark task `DONE`;
    - unblock newly available tasks;
    - update `STATUS.md`;
    - commit with a scoped Conventional Commit message.
16. If FAIL:
    - diagnose;
    - fix within task scope;
    - rerun verification.
17. If architecture/data-license/target ambiguity is encountered:
    - mark `BLOCKED`;
    - write the blocker to `STATUS.md`;
    - stop rather than redesigning the system.
18. Continue with the next unblocked task.

## Commit policy

Prefer one reviewable commit per completed task.

Commit style examples:

- `docs(arch): freeze HUST and Empa source contracts`
- `chore(repo): add typed Python project foundation`
- `feat(ingest): add immutable HUST artifact registry`
- `test(quality): cover duplicate and malformed source fixtures`
- `feat(ml): add grouped-cell SOH baselines`

Do not use meaningless messages such as `updates`, `fix stuff`, or `wip final`.

## Branch policy

- `main` should stay releasable/documented.
- Work from task-scoped branches such as `feat/INGEST-01-hust-ingestion`.
- One task card per branch/PR unless a card explicitly groups work.
- Do not mix refactors with feature work unless required by the task.

## Human architecture gates

Stop for review at minimum after:

1. ARCH-00 — source/schema/SOH freeze.
2. INGEST-02 + QUAL-01 — both real sources and failure behavior are proven.
3. FEAT-01 — before training/evaluation begins.
4. ML-03 — before platform/cloud/showcase work.
5. AUDIT-01 — before recruiter-ready release.

Everything between gates can be highly autonomous.

## Evidence standard

A task is not complete because tests pass. Evidence must include:

- exact commands run;
- test/check summaries;
- fixture/data version;
- benchmark/model config when relevant;
- artifact paths;
- limitations/failures;
- references to commits.

Never manually fabricate benchmark/model output in evidence files.

## Long-running safety

If a task takes too long:
- split implementation internally only if the task card permits it;
- preserve task acceptance criteria;
- do not skip tests to move the queue forward;
- do not silently substitute a different library/architecture.

If usage/session limits stop work, the repository files must make the next session resumable without chat history.
