# AGENTS.md — Codex Engineering Contract

This repository is a flagship Data Engineering + Data Science/ML project. Codex is an implementation engineer, not the product architect.

## 1. Non-negotiable architecture rules

1. Do not change the locked product direction without an explicit task card.
2. Raw source artifacts are immutable. Never rewrite source bytes in place.
3. Every ingestion must preserve provenance: source, source version, checksum, adapter version, ingestion timestamp, and license/usage metadata.
4. Canonical battery time-series semantics must align with stable Battery Data Format (BDF) concepts where applicable.
5. Bad or ambiguous data must fail validation or enter quarantine with a machine-readable reason. Never silently coerce questionable records.
6. All transformations must be deterministic and replayable from raw data.
7. Re-running the same logical input must be idempotent.
8. ML feature datasets must be versioned and reproducible from raw/canonical data plus code/config versions.
9. Never use random cycle-row train/test splits when multiple rows originate from the same physical cell. Primary evaluation is grouped by cell identity.
10. Never include a feature that directly or indirectly leaks the SOH target or future information.
11. Cross-source/domain-shift evaluation is a required V1 capability.
12. Metrics and performance claims must be reproducible and recorded under `docs/evidence/` before they appear in README or résumé-facing docs.

## 2. V1 scope

V1 must eventually include:

- at least two independent battery data sources;
- immutable ingestion + manifests/checksums;
- BDF-aligned canonical representation;
- validation/quarantine/data-quality reporting;
- curated cell/test/cycle analytical tables;
- replay/backfill support;
- versioned leakage-safe features;
- SOH estimation with naive, linear, boosted-tree, and one uncertainty-aware baseline when computationally justified;
- held-out-cell evaluation;
- cross-source/domain-shift evaluation;
- MLflow lineage;
- orchestration only after stable independent jobs exist;
- S3 deployment profile;
- tests, CI, benchmarks, evidence, PROJECT_DEFENSE, and CLAIMS_LEDGER;
- small read-only evidence console after the underlying system is real.

## 3. Explicitly deferred unless a task card justifies them

Do not introduce these merely for résumé keywords:

- Kafka
- Kubernetes
- Spark / Databricks
- dbt
- online serving
- automatic retraining
- deep neural networks

## 4. Coding standards

- Python 3.12+.
- Strict typing for project code; no untyped dictionaries crossing module boundaries.
- Prefer small typed modules with explicit interfaces over notebooks or monolithic scripts.
- Public functions/classes require docstrings when behavior is non-obvious.
- Use `pathlib.Path` or URI-aware abstractions; do not hardcode OS-specific paths.
- Keep IO, parsing, domain transforms, and orchestration separate.
- Use dataclasses/Pydantic models for contracts.
- No bare `except:`; never swallow exceptions.
- Error messages must contain actionable context but never credentials/secrets.
- Logging must include source, artifact/run id, stage, and failure reason where applicable.
- Avoid global mutable state.
- Randomized work must use an explicit seed.
- Numerical/ML code must document units and target definitions.
- Keep dependencies minimal. New infrastructure dependencies require a task-card justification.

## 5. Required quality gates

Before reporting implementation work complete, run the project-standard checks once those commands exist:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

Normal unit tests must not require network access.

## 6. Queue-driven workflow

Before editing code:

1. Read `PROJECT_SPEC.md`.
2. Read `ARCHITECTURE.md`.
3. Read `STATUS.md`.
4. Read `WORK_QUEUE.md`.
5. Select the highest-priority unblocked task.
6. Read its task card under `docs/task-cards/`.
7. Inspect existing interfaces before writing code.

For every task:

1. Restate the objective and files/interfaces expected to change.
2. Do not expand scope without an explicit architecture decision.
3. Implement the smallest coherent change.
4. Add tests.
5. Run required quality gates.
6. Write or refresh the requested evidence artifact.
7. Update STATUS and queue state.
8. Commit only after acceptance criteria pass.

Never report only "done". Report exact files changed, commands run, test results, evidence written, and remaining limitations.

## 7. Stop conditions

Stop and mark the task BLOCKED rather than improvising if:

- a source license/usage right is unclear;
- the canonical schema needs a new architectural decision;
- an ML target definition is ambiguous;
- an implementation would violate leakage or provenance rules;
- credentials/secrets are required and unavailable;
- a requested technology is not approved by the current architecture;
- tests show a locked product assumption is invalid.

## 8. Documentation truth rules

- `CLAIMS_LEDGER.md` is the only source for résumé-ready claims.
- Do not put unverified scale, accuracy, throughput, production, or user claims in README.
- Synthetic, simulated, and public laboratory data must be labeled accurately.
- Implemented behavior and future production design must be clearly separated.
