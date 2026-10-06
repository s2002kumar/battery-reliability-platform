# FOUND-01 — Architecture-Independent Python Repository Foundation

## Objective

Create a reproducible, typed Python 3.12+ repository foundation and local/CI quality gates without implementing battery-domain behavior.

## Context

ARCH-00 is BLOCKED on scientific and source-contract questions. Those blockers do not prevent setting up packaging, developer tooling, generic configuration/logging, and test infrastructure. All interfaces in this task must avoid assumptions about battery schemas, source adapters, BDF mappings, or SOH semantics.

## Depends on

- ARCH-00 research state is recorded and preserved; its scientific gate remains BLOCKED.

## Scope

- Configure a modern `pyproject.toml` and `uv` project for Python 3.12+.
- Establish a `src/` package layout and `tests/`.
- Configure Ruff lint and formatting, strict Mypy for `src/`, and pytest.
- Add a small typed settings/configuration foundation and structured logging setup.
- Define a small typed filesystem/URI boundary that can represent local paths and generic URIs without implementing S3 or storage behavior beyond the stated interface.
- Set deterministic test configuration and explicit seeds anywhere a randomized test fixture is used.
- Add GitHub Actions CI for the same lint, format, type, and test commands developers run locally.
- Add a development/test Dockerfile and document standard developer commands.
- Add `.env.example` only if the chosen settings require environment configuration; it must contain placeholders only.
- Write `docs/evidence/FOUND-01.md` with versions, commands/results, CI and Docker results, introduced files, and limitations.
- Update `STATUS.md` and `WORK_QUEUE.md` when acceptance criteria pass.

## Allowed architectural changes

- Repository layout, packaging, developer tooling, generic settings/logging, generic storage-interface types, CI, and development/test container setup only.
- No battery-domain interfaces or semantics may be introduced in the name of future extensibility.

## Acceptance criteria

- [ ] A fresh clone can create the environment deterministically using documented `uv` commands and a committed lockfile.
- [ ] The package imports through the `src/` layout.
- [ ] The repository is package-first; no notebook-first structure is introduced.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run ruff format --check .` passes.
- [ ] `uv run mypy src` passes with strict, documented settings appropriate to production code.
- [ ] `uv run pytest` passes without network access.
- [ ] GitHub Actions runs equivalent checks on supported pushes and pull requests.
- [ ] The development/test Docker image builds successfully from a fresh checkout context.
- [ ] No secrets or real dataset bytes are committed.
- [ ] Generic interfaces contain no guessed battery, BDF, source, capacity, or SOH semantics.
- [ ] `docs/evidence/FOUND-01.md`, `STATUS.md`, and `WORK_QUEUE.md` accurately record results; FOUND-01 is DONE only if every gate passes.

## Required tests

- Local import/package smoke test through the installed `src/` package.
- Unit tests for any settings validation, structured logging setup, or generic URI/path value types that are implemented.
- All four project quality-gate commands above.
- Docker build command recorded in evidence.
- Confirm the test suite succeeds with network access disabled or document a direct equivalent proving no test makes network calls.

## Required evidence

Write `docs/evidence/FOUND-01.md` containing:

- exact Python, uv, Ruff, Mypy, pytest, and Docker versions;
- exact environment/setup and quality-gate commands and results;
- package import result and test count/result;
- Docker build command/result;
- CI workflow path and checks;
- files introduced or changed;
- confirmation that no dataset bytes/secrets were added;
- known limitations and any unavailable validation.

## Documentation updates

- Document environment creation, sync, lint, format, type-check, test, and Docker commands in a concise developer guide or README section.
- Update `STATUS.md` with the task result, evidence path, commit, and remaining ARCH-00 blocker state.
- Update `WORK_QUEUE.md` to mark FOUND-01 DONE only when all acceptance criteria pass; ARCH-00 remains BLOCKED until separately resolved.

## Explicitly excluded

- HUST parsing or ingestion.
- Empa Aurora parsing or ingestion.
- BDF mapping implementation.
- SOH or reference-capacity logic.
- Feature engineering, ML, or model evaluation.
- Airflow, MLflow, AWS SDK/S3 implementation, Spark, Kafka, dbt, Kubernetes, frontend/UI.
- Production pipeline code or assumptions about unresolved source schemas.

## Stop conditions

- Stop and document a blocker if a requested foundation feature requires an unresolved product or scientific decision.
- Stop if any proposed generic abstraction requires invented battery semantics.
- Do not weaken lint, typing, tests, or CI to make a failing check pass; correct the implementation within scope or document the blocker.

## Definition of done

All acceptance criteria, checks, evidence, and documentation updates pass; changes are committed on a scoped branch with `chore(repo): establish typed Python project foundation`. Push the branch and open a PR. Squash-merge only after required review and CI pass. Do not start ARCH-01 or any ingestion task as part of FOUND-01.
