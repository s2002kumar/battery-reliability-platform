# Battery Reliability & Degradation Intelligence Platform

Production-inspired **Data Engineering + Data Science/ML** platform for trustworthy battery degradation intelligence.

## V1 goal

Ingest heterogeneous public battery cycling/test datasets, preserve provenance, normalize them into a BDF-aligned canonical model, quarantine bad or ambiguous data, build reproducible cycle-level features, and train/evaluate state-of-health models using held-out-cell and cross-source evaluation.

## Current status

**Architecture/Data Gate — ARCH-00**

Implementation is intentionally blocked until exact source files, licenses, schema mappings, and the SOH reference-capacity rule are directly verified.

No résumé claims are approved yet.

## How this repository is run

This repository is designed for queue-driven Codex execution:

- `AGENTS.md` — engineering contract and non-negotiable rules
- `PROJECT_SPEC.md` — locked product/V1 boundary
- `ARCHITECTURE.md` — architecture baseline
- `WORK_QUEUE.md` — dependency-aware task queue
- `STATUS.md` — current task/blockers
- `QUALITY_GATES.md` — recruiter-ready release criteria
- `CODEX_RUNBOOK.md` — autonomous execution loop
- `docs/task-cards/` — exact task scopes and acceptance criteria
- `docs/evidence/` — reproducible proof for technical/ML claims

## Engineering principles

- Evidence before claims.
- Raw source data is immutable.
- No silent repair of questionable data.
- No random row-level train/test split across repeated observations from the same battery.
- Every derived artifact must be traceable to source data, code, and configuration.
- Technologies earn their place from requirements and benchmarks.
- Codex implements; architecture changes require an explicit decision/task card.

## V1

V1 must include real Data Engineering **and** real ML:
- multiple heterogeneous battery sources;
- provenance, data quality, quarantine, replay/backfills;
- curated analytical model;
- versioned leakage-safe features;
- SOH baselines/models;
- held-out-cell evaluation;
- cross-source/domain-shift evaluation;
- uncertainty when computationally appropriate;
- ML lineage;
- CI/testing/benchmarks;
- a small read-only Battery Intelligence evidence console;
- PROJECT_DEFENSE and CLAIMS_LEDGER.

See `PROJECT_SPEC.md` for the locked scope.
