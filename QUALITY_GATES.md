# V1 Quality Gates

V1 is recruiter-ready only when every required gate below is PASS.

## Data sources
- [ ] At least two independent real battery sources integrated.
- [ ] License/usage/redistribution terms documented for every source/fixture.
- [ ] Source provenance includes URI/version/retrieval time/checksum/size/adapter version.
- [ ] No unapproved source bytes committed.

## Data engineering
- [ ] Raw artifacts are immutable.
- [ ] Re-ingesting identical logical input is idempotent.
- [ ] Canonical representation is BDF-aligned where applicable.
- [ ] Validation/quarantine has machine-readable reasons.
- [ ] Curated cell/test/cycle analytical model exists.
- [ ] Replay from raw to curated is deterministic.
- [ ] Historical backfill path is tested.
- [ ] Schema/adapter versions are explicit.

## ML data
- [ ] Feature datasets are versioned and reproducible.
- [ ] Split manifests are deterministic.
- [ ] Physical-cell grouping prevents row-level leakage.
- [ ] Target construction is versioned and documented.
- [ ] Leakage audit passes.
- [ ] Feature lineage points back to source artifacts and code/config.

## ML
- [ ] Naive/reference baseline evaluated.
- [ ] Linear baseline evaluated.
- [ ] Boosted-tree model evaluated.
- [ ] Held-out-cell test results recorded.
- [ ] Cross-source/domain-shift results recorded separately.
- [ ] Error analysis exists.
- [ ] Uncertainty/calibration is implemented or explicitly waived with evidence-based rationale.
- [ ] Model metrics are reproducible.

## MLOps / orchestration / cloud
- [ ] MLflow or equivalent lineage ties dataset/features/code/run/model/metrics.
- [ ] Stable pipeline stages are independently rerunnable.
- [ ] Airflow is introduced only after stage stability and has tested retry/backfill behavior.
- [ ] S3 profile runs without a separate code path.
- [ ] Secrets are never committed.

## Software quality
- [ ] Ruff passes.
- [ ] Formatting check passes.
- [ ] Mypy passes under project settings.
- [ ] Unit tests pass.
- [ ] Integration tests pass.
- [ ] Data-quality tests pass.
- [ ] Critical bug fixes have regression tests.
- [ ] CI runs the normal quality suite.

## Evidence / presentation
- [ ] BENCHMARKS evidence is reproducible.
- [ ] Battery Intelligence Console reads generated evidence artifacts only.
- [ ] README distinguishes implemented behavior from future roadmap.
- [ ] PROJECT_DEFENSE is based on actual implementation/debugging.
- [ ] CLAIMS_LEDGER maps every public/résumé claim to evidence.
- [ ] AUDIT-01 confirms no inflated production/scale/user claims.

## Release condition

All required boxes checked and AUDIT-01 marked PASS.
