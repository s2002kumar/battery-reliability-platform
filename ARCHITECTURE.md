# Architecture — V1 Baseline

## Product boundary

The Battery Reliability & Degradation Intelligence Platform converts heterogeneous public battery cycling/test data into trustworthy, reproducible analytical and ML artifacts.

V1 is batch-first. Streaming is out of scope until real continuously arriving telemetry creates a justified requirement.

## Layers

1. **Source registry / immutable raw** — source metadata, license/usage notes, checksums, original bytes.
2. **Source adapters** — parse source-native formats and map units/semantics.
3. **Validation + quarantine** — structural and semantic failures are explicit.
4. **Canonical time series** — BDF-aligned field semantics plus project-owned provenance/identity fields.
5. **Curated analytical model** — cells, tests/protocols, cycles, measurements, derived cycle metrics, quality events.
6. **Versioned features** — leakage-safe feature datasets with a manifest tying data/code/config versions together.
7. **ML** — SOH target construction, baselines, grouped-cell evaluation, cross-source stress evaluation, uncertainty.
8. **Lineage/evidence** — MLflow for runs/models and immutable evidence artifacts for benchmark/recruiter claims.
9. **Showcase** — read-only evidence console consuming generated artifacts; never a source of truth.

## Technology baseline

- Python + SQL
- Polars / PyArrow / DuckDB for local processing
- Parquet for analytical storage; Delta-style table versioning only where concrete requirements justify it
- MLflow for experiment/model lineage
- Airflow only after independent replayable stages exist
- AWS S3 deployment profile after local correctness
- Docker + GitHub Actions

## Deferred

Kafka, Kubernetes, Spark/Databricks, dbt, online inference, deep learning, automatic retraining.

## Required ADRs before source implementation

- ADR-001 canonical schema boundary and BDF mapping
- ADR-002 storage/versioning strategy
- ADR-003 SOH reference-capacity rule and leakage policy
- ADR-004 dataset/source selection and redistribution policy
