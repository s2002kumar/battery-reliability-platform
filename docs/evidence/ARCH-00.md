# ARCH-00 Evidence — Dataset Inspection and Architecture Gate

> **Snapshot note:** The original findings below record the 2026-10-02 ARCH-00 audit. The 2026-10-06 ARCH-01 direct archive reinspection supersedes its “not yet inspected” statements. See the dated ARCH-01 audit appended at the end; ARCH-00 remains **BLOCKED**, and no source bytes are in Git.

- **Disposition:** BLOCKED
- **Inspection date:** 2026-10-02
- **Branch:** `docs/ARCH-00-data-architecture`
- **Repository state before document edits:** clean `main`, origin `https://github.com/s2002kumar/battery-reliability-platform.git`; branch created before edits.
- **Data bytes in repository:** none added.
- **Scope:** ARCH-00 only. No ingestion, feature, model, orchestration, cloud, or UI code was added.

## Findings and primary evidence

### HUST personalized-discharge dataset

**Verified record and archive:** [Mendeley Data v2, DOI 10.17632/nsc7hnsg4s.2](https://data.mendeley.com/datasets/nsc7hnsg4s/2), published 2022-05-24. The record itself states CC BY 4.0 and describes 77 LFP/graphite cells, nominal 1.1 Ah / 3.3 V, the same charge protocol, different multistage discharge protocols, and constant 30 °C. Its public dataset metadata identifies `our_data.zip`, file ID `5ca0ac3e-d598-4d07-8dcb-879aa047e98b`, 1,188,136,932 bytes, SHA-256 `071d24617153693b0d29059568525e620f6af6512acc9d00c98c7adcf15125db`. The record's license description warns that further permission may be required for any content identified as third-party. The [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) permits sharing/adaptation subject to attribution, license link, change indication, and no extra restrictions, only for rights the licensor can grant.

**Original study:** [Ma et al., Energy & Environmental Science, DOI 10.1039/D2EE01676A](https://doi.org/10.1039/D2EE01676A). It names A123 APR18650M1A cells, 77 discharge protocols, >140,000 charge-discharge cycles, and uses capacity estimation as a health output. Its data availability section points to the same Mendeley record.

The ZIP central directory was read by HTTP byte range; no complete archive was downloaded. It contains exactly 78 entries: one directory `our_data/` and 77 pickle members. Exact member stems are `1-{1..8}`, `2-{2..8}`, `3-{1..8}`, `4-{1..8}`, `5-{1..7}`, `6-{1..6,8}`, `7-{1..8}`, `8-{1..8}`, `9-{1..8}`, and `10-{1..8}`; append `.pkl` under `our_data/`.

One compressed member, `our_data/1-1.pkl` (17,309,189 compressed / 53,553,885 uncompressed bytes; pickle protocol 4), was range-read and its serialization strings inspected. The DataFrame fields are `Status`, `Cycle number`, `Current (mA)`, `Voltage (V)`, `Capacity (mAh)`, and `Time (s)`. Observed statuses include `Constant current charge`, `Constant current-constant voltage charge`, and `Constant current discharge_0` through `_3`. The authors' original [preprocessing code](https://raw.githubusercontent.com/HAIRLAB/Health_status_prediction/main/common.py) expects the per-cell object to contain `rul`, `dq`, and `data`; it uses `dq[cycle]` as a capacity label, `rul[cycle]` as an RUL label, and charge-only rows from the DataFrame to create voltage/capacity features. This establishes a measured capacity-target candidate and explicit leakage fields, but the code does not define the project's SOH denominator. Its HUST path starts from the tenth `dq` key and does not document this as a formation/reference rule.

**Still not verified:** whether `dq` is complete-cycle discharge capacity with what units/reset semantics across all 77 files; exact cycle-key-to-DataFrame mapping; current sign; data nulls; formation/test-reference protocols; and any third-party-content notices inside the archive. The public Mendeley API's file endpoints also returned HTTP 401 without OAuth, but the public record metadata provided the exact archive and file SHA-256 without credentials. No complete archive was downloaded and no alternative mirror/processed derivative was substituted.

### Empa Aurora dataset

**Verified record:** [Zenodo v1, DOI 10.5281/zenodo.15481956](https://zenodo.org/records/15481956). The [authoritative record API JSON](https://zenodo.org/api/records/15481956) declares `cc-by-4.0` and identifies one archive, `Dataset-rocrate.zip`, 2,507,129,091 bytes, MD5 `eaec9549b74b59d998e5138dab965b5d`. Apply the [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en), including attribution, license link, and change indication.

The record description identifies 199 coin cells with NMC//graphite or LFP//graphite and cycling to 1,000 cycles. Per-cell package paths are documented as `empa__ccid000XXX.metadata.json` (JSON-LD), `empa__ccid000XXX.bdf.csv`, and `empa__ccid000XXX.bdf.parquet`; it says the CSV and Parquet data are identical and use BDF time-series format.

**Original study:** [Svaluto-Ferro et al., Batteries & Supercaps, DOI 10.1002/batt.202500155](https://doi.org/10.1002/batt.202500155). The publisher-hosted paper describes CR2032 coin cells, graphite anodes, LFP/NMC622/NMC811 cathodes, testing at 25 °C, and a protocol with three formation cycles at 0.1 mA cm-2 followed by long-term cycling at 1.0 mA cm-2. That protocol evidence does not reveal BDF cycle indices or confirm a common capacity-reference window.

The archive ZIP central directory was read by HTTP range. It has 797 entries: 199 cell directories, each containing the expected JSON-LD metadata, BDF CSV, and BDF Parquet, plus `ro-crate-metadata.json`. `ccid` IDs span a non-contiguous namespace from 000001 through 000249. One actual file, `empa__ccid000001.metadata.json` (55,780 uncompressed bytes), was range-read and parsed. It is JSON-LD (`@context`, `@graph`) containing cell identity/product IDs, date/creator/manufacturer, positive/negative electrode composition and measured properties, rated-capacity values, and an explicit generated test procedure. This cell is NMC622//graphite (positive formula `LiNi0.6Co0.2Mn0.2O2`, negative Graphite). Its actual per-cell chemistry does not establish chemistry counts across the archive.

**Not verified from time-series bytes:** chemistry-specific cell counts/IDs, BDF CSV/Parquet headers and values, native cycle index mapping, null behavior, and which BDF capacity field is a complete cycle discharge in each file. The exact archive and all member patterns are identified, but source-specific capacity mapping and the LFP evaluation subset remain blocked.

### BDA/SINTEF/DLR pipeline-robustness fixtures

**Verified record:** [SINTEF Battery Lab Zenodo v0.8.0, DOI 10.5281/zenodo.21337233](https://zenodo.org/records/21337233). Its [record API JSON](https://zenodo.org/api/records/21337233) declares CC BY 4.0. The record's [metadata.json catalog](https://zenodo.org/api/records/21337233/files/metadata.json/content) contains per-fixture SPDX `CC-BY-4.0`, source file URL, type, size, parser-schema identifier, and source/citation metadata. The [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) requires attribution, license link, and change indication when sharing. The record README states intentional bugs are included for data-pipeline robustness tests.

Selected files (record MD5s retained as source identifiers; SHA-256 still must be computed on retrieval):

| Selected use | Exact artifact | Bytes | MD5 | Source-catalog facts |
|---|---|---:|---|---|
| Clean parser fixture | `DLR__LiGrHydra0b__20221114__GITT__25degC__Basytec.txt` | 62,380,666 | `26eb1804d891c87bff7af244927be602` | Li-graphite half-cell, GITT; no listed bug; CC-BY-4.0 |
| Clean parser fixture | `DLR__LiGrHydra0b__20230131__POCV__25degC__Basytec.txt` | 9,257,892 | `9e5b47be4a13c71a66d20714d3e016b6` | Li-graphite half-cell, POCV; no listed bug; CC-BY-4.0 |
| Clean chemistry fixture | `DLR__LiLNMOHydra0b__20221125__POCV__25degC__Basytec.txt` | 4,060,881 | `5e6bd90f2f01b777fe871e7f867d3ee0` | Li-LNMO half-cell, POCV; no listed bug; CC-BY-4.0 |
| Clean chemistry fixture | `DLR__LiLNMOHydra0b__20221130__GITT__25degC__Basytec.txt` | 63,013,852 | `4c72b750dead3747e9bfe82413ecc9cd` | Li-LNMO half-cell, GITT; no listed bug; CC-BY-4.0 |
| Intentional rejection/repair fixture | `SINTEF__NaCR32140-MP10-04__20250825__CCCV-0p02C__25degC__BioLogic__OutlierBug.mpt` | 53,617,142 | `627f276281d2de9ad3ffe9494c7b115d` | Na-ion full-cell; voltage/current outlier spikes and corrupted vendor energy accumulators; CC-BY-4.0 |
| Intentional rejection fixture | `SINTEF__SLPBA842124HV__20241023__Rate__25degC__Neware__TimeBug.csv` | 3,151,396 | `e2075f6ffd08ea0d9f1e686cebbf2d1e` | Li-ion full-cell rate test; non-monotonic total time; CC-BY-4.0 |

These fixtures are approved as *candidate* parser/validation tests from license/catalog evidence. Their bytes were not fetched, so no local SHA-256, row-level schema check, or fixture test has occurred. The FZJ Digatron fixture also has a documented seconds-header/milliseconds-data defect in the record README, but it is not included in this initial six-file subset.

## Canonical BDF mapping findings

The [BDF specification](https://github.com/battery-data-alliance/battery-data-format) identifies one cell per time-series file; required test time, voltage, current; positive current as charging and negative as discharging; recommended cycle count, step count, ambient temperature, and timestamp; and optional separate cycle-, step-, and test-cumulative charge/discharge capacity and energy fields. BDF capacity fields are not interchangeable. The project contract therefore rejects an unqualified `discharge_capacity_ah` and requires source-specific mapping proof before using cycle discharge capacity as a target.

| Source | Verified source-to-contract mapping | Unresolved mapping |
|---|---|---|
| HUST | Record-level cell/protocol facts only; no exact columns mapped | All source headers, normalized units/sign, identifiers, cycle/step semantics, capacity fields, nullability |
| Aurora | Record describes per-cell BDF CSV/Parquet plus JSON-LD metadata; BDF required concepts provide expected vocabulary | Exact columns/data/metadata values, cell IDs, cycle and capacity mapping, nullability |
| SINTEF/DLR fixtures | Catalog identifies source file types, lab/test/chemistry, and selected defects/license | No raw bytes parsed; parser behavior and per-row mappings not tested |

No source field was silently coerced. Proposed nullability and required/optional/derived/unavailable/source-specific classes are in [DATA_CONTRACT.md](../../DATA_CONTRACT.md), explicitly marked not frozen for adapters.

## SOH, reference, leakage, grouping, and cross-source decision

- Capacity-based SOH is a candidate supported at publication level for HUST and by Aurora's cycling/BDF description. Exact compatible numerator field and its complete-cycle semantics are not verified for either selected archive.
- **No exact denominator rule is frozen.** A first cycle is rejected as an assumption. Aurora publication describes three formation cycles; HUST formation/reference measurement semantics remain unknown. The candidate of a median over repeated post-formation standardized reference measurements can only be considered if source metadata/files prove the window and the protocols are sufficiently comparable.
- Leakage-safe group key: `(source_name, source_record_version, source_native_cell_id)`; all repeated rows/files/tests for a physical cell stay in one fold.
- Target, same-cycle discharge capacity aliases, SOH/EOL/RUL labels, reference denominator, future-cycle data, full-life summaries, and cumulative measurements with unknown reset semantics are leakage risks. Cell/source/protocol IDs remain split/stratification metadata by default, not predictors. See [ML_EVALUATION_PLAN.md](../../ML_EVALUATION_PLAN.md).
- No cross-source SOH metrics are approved yet. A potential external stress set is LFP/graphite in both HUST and Aurora only. This is a combined source/cell-design/protocol shift (including cylindrical commercial vs CR2032 coin-cell design, differing test temperatures/protocols), not isolated source effect or chemistry transfer. Require aligned per-cell reference semantics and explicit metadata before running or reporting it.

## Acceptance-criteria audit

| ARCH-00 criterion | Result | Evidence / reason |
|---|---|---|
| Authoritative license/terms for each selected record/fixture | **PASS at record/catalog level** | HUST Mendeley v2 CC BY 4.0; Aurora Zenodo API CC BY 4.0; fixture record and selected catalog entries SPDX CC-BY-4.0. |
| No inferred redistribution claim | **PASS** | Claims derive from source record/API license metadata; source bytes remain uncommitted. |
| Exact source files needed for V1 identified | **PARTIAL / BLOCKED** | HUST archive and all 77 member names verified; Aurora archive and all per-cell file patterns/199 IDs verified; exact Aurora LFP subset and fixture raw-byte ingestion selection remain unresolved. |
| Canonical field mapping covers selected sources | **BLOCKED** | HUST sampled frame fields and author `dq`/`rul` usage known but capacity/cycle semantics unresolved; Aurora metadata sample read but BDF time-series rows not parsed; fixture bytes not parsed. |
| Nullable/optional behavior explicit | **PARTIAL** | Contract defines project policy; source-specific nullability cannot be frozen before file inspection. |
| Deterministic, source-aware numerator/reference | **BLOCKED** | HUST `dq` role is a capacity label but exact physical capacity semantics need validation; Aurora BDF capacity rows unparsed; reference windows unverified; no denominator rule selected. |
| Leakage risks documented | **PASS as policy** | Target, future data, capacity aliases, denominator, cycle-age proxies, IDs, and accumulators documented. |
| Group key unambiguous | **PASS as contract** | Source + record version + source-native physical cell ID; actual source-native ID values still need checking. |
| Cross-source comparison meaningful or narrowed | **BLOCKED / narrowed candidate** | Only same-chemistry LFP candidate; still combined source/design/protocol shift and target comparability unresolved. |
| Required ADRs created | **PASS as research state** | ADR-001 through ADR-004 created; ADR-001/003/004 explicitly retain BLOCKED/proposed state where evidence is incomplete. |
| No production code added | **PASS** | Documentation only. |

## Validation and work record

- Read all required repository policy/spec/architecture/status/queue/quality/source/contract/evaluation/task-card documents before edits.
- Confirmed clean `main` and correct `origin`; created `docs/ARCH-00-data-architecture` before editing.
- Inspected authoritative pages/API metadata and original publications linked above. Mendeley unauthenticated file listing returned 401; no credentials were requested or used.
- No local dataset bytes or source-derived files were created.
- No project markdown lint/format command is configured in the inspected repository file list. Documentation validation performed after edits: `git diff --check` and manual cross-document/acceptance-criteria review.
- Because the exit criteria are not met, task status is **BLOCKED** and no downstream task is unblocked.

## ARCH-01 resolution audit (2026-10-06)

The exact selected HUST and Aurora archives were subsequently downloaded outside the repository, checked against the source record identity, and audited with the isolated reproducible scripts under `research/ARCH-01/`. HUST's `dq` capacity relation is verified for all cycles in five selected payloads (9,453 cycles), not all 77 cell files. HUST's archive-level CC BY 4.0 is explicit, but the Mendeley third-party-content permission caveat cannot be resolved from any in-archive notice; no bytes may be redistributed until that scope is clarified.

Aurora's exact v1 archive was fully inspected: 199 cells, 135 NMC622, 32 LFP, and 32 metadata formulas `Ni0.83Mn0.06Co0.11O2`; these last 32 differ from the original paper's NMC811 formula `LiNi0.83Mn0.10Co0.07O2` and are not relabeled pending clarification. One six-column Parquet schema; no explicit capacity/status/step/energy field; all source Parquet fields have zero nulls per available statistics. Four selected CSV and Parquet pairs matched exactly. The 32 LFP cell IDs are listed in [DATA_SOURCES.md](../../DATA_SOURCES.md). `cycle_dimensionless` is not safe to normalize: all 32 LFP cells have repeated resets to zero (16,240 returns in total); the 32 Ni-rich NMC metadata records also have 13,349 returns; NMC622 contains 91 decreases (59 returns to zero). No non-guessed mapping from these values to the article's formation/aging cycle phases or complete discharge capacity has been verified.

The exact HUST source labels, Aurora fields, direct mapping candidates, nullability, license scope, early-cycle statistics, cell-group key, leakage rules, and cross-source decision are now detailed in [DATA_CONTRACT.md](../../DATA_CONTRACT.md), [DATA_SOURCES.md](../../DATA_SOURCES.md), [ML_EVALUATION_PLAN.md](../../ML_EVALUATION_PLAN.md), ADR-001–004, and [ARCH-01 evidence](ARCH-01.md).

### Updated ARCH-00 acceptance audit

| Criterion | 2026-10-06 result | Evidence / blocker |
|---|---|---|
| Authoritative source records, files, checksums, and terms | **PARTIAL** | Exact archives/checksums and record CC BY licenses verified. HUST's generic third-party permission caveat remains unresolved for redistribution. |
| HUST file schema, capacity units/meaning, cycle and current semantics | **PARTIAL** | Directly demonstrated in five full cell payloads; other 72 payloads and source-wide null/order audit remain. |
| Aurora exact population/schema/nulls/CSV-Parquet consistency | **PASS for inspected archive** | 199-cell chemistry inventory, all schemas/statistics, and four full-pair equality comparisons recorded. |
| Aurora capacity/cycle mapping | **BLOCKED** | No capacity/step/status field; repeat cycle-index resets; no verified integration segmentation. |
| Source-aware SOH numerator and deterministic reference | **BLOCKED** | HUST `dq` supported in five cells; Aurora complete-discharge capacity and common reference rule unverified. No denominator selected. |
| Formation/early unstable cycles | **PARTIAL / BLOCKED** | Aurora paper's 3 formation cycles describe NMC622, not established for LFP; archive index mapping ambiguous. HUST first 10 variation measured; first 9 exclusion in author code is not labeled formation. |
| Leakage and physical-cell group policy | **PASS as policy** | Documented and source ID formats directly checked; SOH target remains unavailable. |
| Cross-source evaluation | **BLOCKED** | Only same-chemistry LFP candidate (77 HUST vs 32 Aurora), but combined source/design/protocol/temperature shift and target incompatibility block SOH metrics. |
| Required canonical mapping and nullability contract | **PARTIAL** | Direct field mappings and absent/unverified fields documented. No ambiguous cycle/capacity field is guessed. |
| No implementation scope expansion | **PASS** | Research-only scripts/dependencies, evidence, and architecture documents; no ingestion/model code. |

Therefore ARCH-00 did not pass. ARCH-01 is **BLOCKED** pending source/architecture review. `INGEST-01` and every dependent task stay BLOCKED.
