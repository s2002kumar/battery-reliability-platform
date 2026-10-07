# ARCH-01 — Resolve ARCH-00 Dataset and SOH Evidence Blockers

**Execution disposition (updated 2026-10-07): PASS.** Direct inspection of all 77 HUST label structures, seven representative/edge HUST payloads, every Aurora metadata/schema record, and all 32 Aurora LFP protocols/traces supports the canonical source mappings, source-aware SOH rule, and bounded combined-shift evaluation. HUST frame-level schema/capacity comparisons cover seven cells; future ingestion must validate every row/member. Three Aurora cells have one out-of-diagnostic-cutoff event each and those events must be quarantined. See [docs/evidence/ARCH-01.md](../evidence/ARCH-01.md). INGEST-01 remains blocked pending architecture review and a scoped implementation task card.

## Objective

Resolve the specific source, license, canonical-field, SOH-reference, and cross-source blockers recorded by ARCH-00 through direct inspection of the exact selected files and authoritative evidence.

## Context

ARCH-00 was initially BLOCKED. This task resolves the blockers for the selected V1 sources through direct archive and authoritative record inspection. HUST source-row evidence has stated sample coverage; Aurora target mapping applies only to the exact 32-cell LFP subset. FOUND-01 is complete and merged; neither task authorizes ingestion. This task is research and architecture evidence only.

## Depends on

- ARCH-00 research record and blockers are documented.
- FOUND-01 repository foundation is DONE.

## Scope

### HUST

- Retrieve the exact Mendeley v2 artifact `our_data.zip` selected by ARCH-00; record retrieval date, size, and locally computed SHA-256; do not add source bytes to Git.
- Enumerate and verify all 77 pickle member paths against the ARCH-00 inventory.
- Safely inspect representative and edge-case cells programmatically, including smallest and largest archive members; record inspected payload keys, cycle/label counts, schemas, nulls, cycle semantics, and capacity comparisons. Enumerate all 77 members; label the remaining uninspected payload count explicitly.
- Establish `dq` meaning, units, cycle association, and calculation source from the original publication, authors' code, archive contents, and value-level comparisons. Distinguish evidence from inference.
- Establish native cycle and step semantics, current sign, capacity-column accumulation/reset behavior, nulls, and early-cycle/formation behavior from actual data.
- Inspect archive members, file metadata, and authoritative record terms for license/third-party notices. State exactly which redistribution rights are explicit and which remain unclear.

### Empa Aurora

- Retrieve the exact Zenodo v1 `Dataset-rocrate.zip`; record retrieval date, size, and locally computed SHA-256; do not add source bytes to Git.
- Enumerate all 199 cell folders and verify all metadata, BDF CSV, and BDF Parquet paths.
- Programmatically inventory all 199 per-cell metadata records to determine chemistry, physical-cell identifiers, and protocol/test metadata; list exact LFP/graphite cell IDs if present.
- Inspect BDF CSV and Parquet schemas, nulls, cycle-index values, capacity fields, units, and selected rows from each relevant chemistry/protocol. Verify CSV/Parquet consistency using actual values.
- Determine from source metadata/paper and file data how capacity fields are produced, when reference/capacity-check tests occur, and which cycles are formation/conditioning.

### SOH target and cross-source evaluation

- Extract per-cell capacity series only after validating source meanings; keep raw capacity distinct from SOH.
- Quantify early-cycle variation and compare first valid cycle with documented candidate stable-window references using transparent per-cell statistics and exact exclusions.
- Select one deterministic source-aware reference-capacity rule only if the observed protocols and measurements support it scientifically without future-data leakage. Otherwise preserve BLOCKED and describe the exact unsupported assumption.
- Compare each sampled cell's first valid capacity with candidate 3/5/10/30-cycle robust-window medians; quantify the variation and direction across cells. Treat these as candidate sensitivities, not a formation rule unless source evidence establishes that interpretation.
- Record target leakage hazards, prediction-time availability, and the physical-cell grouping key. Do not use future-derived labels or full-life summaries as predictors.
- Separate chemistry, cell format/design, protocol, temperature, and source/lab shift. Approve a quantitative cross-source SOH design only if target semantics and relevant test subsets align; otherwise reject it and state a defensible V1 domain-shift alternative.

### Reproducible research

- Keep every exploratory script under `research/ARCH-01/` or `docs/research/ARCH-01/`, outside the production package.
- Scripts must accept input/output locations as arguments or environment configuration, validate expected archive identity/checksum, be deterministic, and emit machine-readable inventory/statistics plus human-readable summaries.
- Do not add source data, credentials, or private data to the repository. Keep downloaded archives and extracted files outside Git.
- Any research-only dependencies must be explicitly pinned and isolated from production runtime dependencies.

## Required outputs

- Update `DATA_SOURCES.md`, `DATA_CONTRACT.md`, and `ML_EVALUATION_PLAN.md` with only verified mappings and conclusions.
- Revisit ADR-001 through ADR-004; preserve BLOCKED status where any gate remains unresolved.
- Update `docs/evidence/ARCH-00.md` with the resolution audit; do not mark ARCH-00 PASS unless every original acceptance criterion is met.
- Create `docs/evidence/ARCH-01.md` with exact source checksums, commands, script versions, observations, quantitative summaries, decisions, and blockers.
- Add reproducible audit scripts and outputs under `research/ARCH-01/` or `docs/research/ARCH-01/` as appropriate; never commit source data bytes.
- Update `STATUS.md` and `WORK_QUEUE.md`.

## Allowed architectural changes

- Clarify or freeze canonical mappings, license/redistribution scope, SOH reference definition, and cross-source evaluation only where direct evidence supports the decision.
- Add research-only inspection scripts and isolated dependencies.
- No implementation architecture or production data pipeline changes.

## Acceptance criteria

- [x] Exact selected HUST and Aurora archive identities, members, checksums, and authoritative terms are recorded.
- [x] HUST `dq`, capacity units, cycle/step meaning, current sign, and early-cycle behavior are supported by direct data inspection. Seven-payload row-level coverage is stated separately from the all-77 label/key audit.
- [x] HUST third-party/redistribution terms are directly checked and not inferred.
- [x] All 199 Aurora cells have an exact chemistry inventory; the exact LFP subset and identifiers are recorded.
- [x] Aurora CSV/Parquet schemas, BDF measurement/capacity fields, cycle semantics, null behavior, and metadata mappings are directly evidenced.
- [x] Capacity target numerator and deterministic reference denominator are source-aware, leakage-safe, and supported by direct observed behavior.
- [x] Early-cycle variability, first-cycle versus candidate stable-window comparisons, exclusions, leakage risks, and cell-group key are recorded with reproducible calculations.
- [x] Cross-source decision separates chemistry, cell design, protocol, temperature, and lab/source effects and labels the evaluation as a combined shift.
- [x] Source-specific required/optional/nullable/derived/unavailable fields in `DATA_CONTRACT.md` match inspected evidence; ambiguous fields remain source-specific.
- [x] Research scripts and derived audit outputs are reproducible, versioned, and contain no dataset bytes or secrets.
- [x] ARCH-00 and ARCH-01 are marked PASS for the documented selection and target; row-validation and event-quarantine limits are explicit.
- [x] No ingestion, production adapter, feature pipeline, model, or downstream FOUND/INGEST scope is added.

## Required tests and validation

- Verify downloaded archive SHA-256 against the source record when available and independently record the observed digest.
- Run research scripts from a clean research environment against the exact archived inputs and verify deterministic output hashes on repeat runs.
- Validate member counts, chemistry inventory totals, CSV/Parquet schema comparisons, and capacity-series summaries with assertions that fail on unexpected source structure.
- Run relevant documentation and script checks; do not alter source bytes.

## Required evidence

`docs/evidence/ARCH-01.md` must include:

- authoritative source URLs, record versions, selected filenames, sizes, and source/local checksums;
- exact license text/metadata and any third-party/redistribution limits;
- inspection environment and pinned tool/dependency versions;
- all commands and script invocations;
- archive/member/schema/chemistry/capacity findings with counts and representative row locators;
- reference-capacity comparison method, population, exclusions, and results;
- leakage and grouping decisions;
- cross-source validity analysis;
- all required document changes and test/check results;
- known limitations, open questions, task/architecture disposition, and commit reference.

## Documentation updates

- Keep `STATUS.md` and `WORK_QUEUE.md` truthful. No ingestion task is unblocked unless ARCH-00 passes.
- Update the evidence and ADR decisions in the same scoped branch.
- If blocked, preserve useful verified research and stop at the architecture gate.

## Explicitly excluded

- INGEST-01 or INGEST-02 implementation.
- Production parsing/adapters, canonical transforms, or storage pipelines.
- Feature engineering, SOH model implementation/training/evaluation, or MLflow.
- Airflow, cloud deployment, S3 implementation, Spark, Kafka, dbt, Kubernetes, or application/UI work.
- Redistribution of HUST/Aurora source bytes in the repository.

## Stop conditions

- Stop and mark ARCH-01 BLOCKED if required source bytes cannot be obtained or verified, license/third-party rights remain unclear, capacity semantics cannot be resolved, the reference target is scientifically indefensible, or cross-source results would mislead.
- Do not guess missing schemas or silently coerce values.
- Do not continue to INGEST-01, even if all gates pass; stop for architecture review.

## Definition of done

All acceptance criteria pass with evidence. Commit the research state separately with a professional `docs(arch): resolve battery source and SOH evidence` message. Stop before INGEST-01; architecture review and an explicit scoped task card are still required before implementation.
