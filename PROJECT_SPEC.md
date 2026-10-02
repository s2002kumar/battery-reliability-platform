# Project Specification — Locked V1

## Product

**Battery Reliability & Degradation Intelligence Platform**

Do not call V1 a fleet platform unless real field telemetry is integrated.

## Purpose

Build a production-inspired Data Engineering + Data Science/ML system that converts heterogeneous battery cycling/test data into trustworthy, reproducible analytical and ML artifacts.

The project must prove more than model training. It must demonstrate data contracts, provenance, quality, replay/backfills, reproducible features, rigorous ML evaluation, lineage, testing, and evidence.

## V1 product flow

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
cross-source/domain-shift evaluation
      ↓
ML lineage + evidence artifacts
      ↓
small read-only Battery Intelligence Console
```

## V1 data strategy

Primary source candidate:
- HUST personalized-discharge battery dataset.

Second source / standards + domain-shift candidate:
- Empa Aurora open battery dataset.

Robustness/conformance fixtures:
- BDA / SINTEF / DLR workflow-automation datasets with explicit usable licenses.

MATR is optional only after original terms are directly verified.

No source bytes are redistributed without verified rights.

## V1 ML target

Primary task: capacity-based State of Health estimation.

Conceptually:

`SOH(t) = available_discharge_capacity(t) / reference_capacity(cell)`

The exact reference-capacity rule must be frozen by ARCH-00 after direct source inspection. Codex must not invent this rule.

Primary evaluation:
- grouped by physical cell identity;
- no random row-level splitting across repeated observations from the same cell;
- separate cross-source/domain-shift stress evaluation.

V1 model ladder:
- naive/reference baseline;
- Ridge or ElasticNet;
- boosted-tree model;
- one uncertainty-aware method such as GPR only if computationally appropriate.

Deep learning is deferred until evidence justifies it.

## Technology baseline

Approved direction:
- Python + SQL
- Polars / PyArrow / DuckDB for local processing
- Parquet for analytical storage
- Delta-style table versioning only where concrete requirements justify it
- MLflow for experiment/model lineage
- Airflow only after stable replayable stages exist
- AWS S3 deployment profile after local correctness
- Docker + GitHub Actions

Deferred:
- Kafka
- Kubernetes
- Spark / Databricks
- dbt
- online inference
- automatic retraining
- deep neural networks

## V1 recruiter-ready definition

V1 is not recruiter-ready until QUALITY_GATES.md passes in full and AUDIT-01 approves every public claim.

## Later roadmap

### V2 — deeper ML
- degradation forecasting / RUL;
- anomaly detection;
- richer curve features;
- domain adaptation / cross-chemistry work where valid;
- stronger uncertainty/calibration;
- PyTorch models only if baselines and data justify them.

### V3 — MLE
- model registry/promotion;
- scheduled batch inference;
- drift monitoring;
- feature/data drift;
- automated evaluation gates;
- shadow-model comparisons;
- retraining decision logic.

### V4 — scale / online systems
- real or realistically sourced telemetry;
- streaming only if justified;
- Spark/Databricks benchmark;
- distributed feature computation;
- potential online inference.

Later phases may not weaken V1 truth/evidence requirements.
