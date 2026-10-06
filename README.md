# Battery Reliability & Degradation Intelligence Platform

A production-inspired **Data Engineering + Data Science/ML** system for trustworthy battery degradation and state-of-health intelligence.

## Problem

Battery testing data is fragmented across laboratories, cyclers, schemas, units, protocols, and metadata conventions. Reliable analytics and machine learning depend on preserving provenance, normalizing semantics, detecting data-quality failures, and reproducing historical feature datasets before a model is trained.

This project is designed around that full lifecycle rather than a standalone prediction notebook.

## V1

The first release will:

- ingest multiple independent public battery cycling/test datasets;
- preserve immutable raw artifacts, source metadata, versions, and checksums;
- map heterogeneous measurements into a BDF-aligned canonical model;
- validate and quarantine malformed or semantically ambiguous records;
- build curated cell, experiment, cycle, and measurement datasets;
- support deterministic replay and historical backfills;
- generate versioned, leakage-safe ML feature datasets;
- estimate capacity-based state of health (SOH);
- evaluate models on held-out physical cells;
- measure cross-source/domain-shift behavior separately from in-domain performance;
- preserve experiment/model/data lineage;
- expose reproducible technical evidence through a small read-only intelligence console.

## Current status

**Architecture/data gate: BLOCKED.** ARCH-00 research is preserved on `docs/ARCH-00-data-architecture`; its unresolved source, schema, license-notice, and SOH reference blockers still prohibit ingestion and ML work. FOUND-01 establishes only architecture-independent repository tooling.

See [STATUS.md](STATUS.md) and [docs/evidence/ARCH-00.md](docs/evidence/ARCH-00.md) for the exact evidence and blockers.

## Architecture

```text
public battery sources
        ↓
immutable raw artifacts + provenance
        ↓
source adapters
        ↓
validation / quarantine
        ↓
BDF-aligned canonical time series
        ↓
curated cell / test / cycle model
        ↓
versioned leakage-safe features
        ↓
SOH model training + evaluation
        ↓
cross-source/domain-shift analysis
        ↓
model + data lineage
        ↓
evidence console
```

See [ARCHITECTURE.md](ARCHITECTURE.md), [DATA_CONTRACT.md](DATA_CONTRACT.md), and [ML_EVALUATION_PLAN.md](ML_EVALUATION_PLAN.md).

## Engineering principles

- Evidence before claims.
- Raw source data is immutable.
- Questionable records are never silently repaired.
- Repeated observations from one physical cell never leak across primary train/test partitions.
- Derived artifacts remain traceable to source data, code, and configuration.
- Technologies are introduced only when requirements or measurements justify them.
- Implemented behavior is kept separate from future scaling designs.

## Planned technical foundation

Python and SQL are the core implementation languages. Local analytical processing is expected to use Polars/PyArrow and DuckDB with Parquet-based storage. ML experiment lineage, recoverable orchestration, cloud object storage, and additional scale technologies are added only after the underlying data contracts and pipeline behavior are proven.

## Documentation

- [PROJECT_SPEC.md](PROJECT_SPEC.md) — product and release boundary
- [ARCHITECTURE.md](ARCHITECTURE.md) — architecture baseline
- [DATA_SOURCES.md](DATA_SOURCES.md) — source provenance and licensing
- [DATA_CONTRACT.md](DATA_CONTRACT.md) — canonical data contract
- [ML_EVALUATION_PLAN.md](ML_EVALUATION_PLAN.md) — target and evaluation rules
- [QUALITY_GATES.md](QUALITY_GATES.md) — V1 release criteria
- [PROJECT_DEFENSE.md](PROJECT_DEFENSE.md) — architecture/tradeoff explanations
- [CLAIMS_LEDGER.md](CLAIMS_LEDGER.md) — evidence-backed public claims

## Developer setup

Install [uv](https://docs.astral.sh/uv/). The committed `.python-version` pins the interpreter. From the repository root:

```bash
uv python install
uv sync --locked --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
docker build --tag battery-reliability-platform:dev .
```

`uv.lock` pins the resolved dependency graph. Run project commands through `uv run` so they use the locked environment. The Docker image is for development and tests; its default command runs pytest. No `.env` file is required. Optional runtime settings are `BRIP_ENV` (`development`, `test`, or `production`) and `BRIP_LOG_LEVEL` (a standard Python logging level).
