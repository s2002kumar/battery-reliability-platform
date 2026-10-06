# ARCH-01 Evidence — Direct Source and SOH Blocker Audit

- **Disposition:** BLOCKED; no source ingestion or ML work is authorized.
- **Research date:** 2026-10-06.
- **Branch:** `docs/ARCH-01-blocker-resolution`.
- **Purpose:** Resolve the source-level uncertainties in ARCH-00 using the exact archives and authoritative records, without committing dataset bytes.

## Primary records, selected artifacts, and rights

### HUST

- Record: [Mendeley Data v2, DOI 10.17632/nsc7hnsg4s.2](https://data.mendeley.com/datasets/nsc7hnsg4s/2); source metadata [API](https://data.mendeley.com/public-api/datasets/nsc7hnsg4s).
- Exact file: `our_data.zip`; file id `5ca0ac3e-d598-4d07-8dcb-879aa047e98b`; 1,188,136,932 bytes; expected and locally verified SHA-256 `071d24617153693b0d29059568525e620f6af6512acc9d00c98c7adcf15125db`.
- Primary article: Ma et al., [Energy & Environmental Science (2022), DOI 10.1039/D2EE01676A](https://pubs.rsc.org/en/content/articlehtml/2022/ee/d2ee01676a). The article describes 77 A123 APR18650M1A LFP/graphite cylindrical cells, nominal 1.1 Ah/3.3 V, 30 °C, common fast charging, and personalized multistage discharges; it treats capacity as a health output.
- The dataset record declares CC BY 4.0; see the [legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en). Attribution, license link, and change indication apply. Mendeley also warns that additional permission may be required for content identified as third-party. ZIP inventory has no embedded README or rights manifest. This research cannot identify any third-party-marked member or prove their absence. **No redistribution of HUST bytes is approved pending clarification of any applicable third-party rights.** The RSC article license is separate.

### Empa Aurora

- Record: [Zenodo v1, DOI 10.5281/zenodo.15481956](https://zenodo.org/records/15481956); authoritative [record API](https://zenodo.org/api/records/15481956).
- Exact file: `Dataset-rocrate.zip`; 2,507,129,091 bytes; record/local MD5 `eaec9549b74b59d998e5138dab965b5d`; local SHA-256 `61f66d309462c5bcbb00ddfef0d141ad836f811f2b78d07457aadc4a3e7baff7`.
- Zenodo API declares CC BY 4.0; apply its attribution, license-link, and modification notice requirements. Primary study: Svaluto-Ferro et al., [Batteries & Supercaps (2025), DOI 10.1002/batt.202500155](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/batt.202500155). It describes the protocol/chemistry/cell design evidence below.

### Pipeline fixtures

- [SINTEF Battery Lab Zenodo v0.8.0, DOI 10.5281/zenodo.21337233](https://zenodo.org/records/21337233), [record API](https://zenodo.org/api/records/21337233), and official [metadata catalog](https://zenodo.org/api/records/21337233/files/metadata.json/content) declare record CC BY 4.0 and per-file SPDX `CC-BY-4.0` for selected entries. The six exact clean/bad candidates and catalog MD5/size/bug labels are listed in [DATA_SOURCES.md](../../DATA_SOURCES.md). These fixture bytes were not retrieved or parsed; their classification is catalog evidence only, not a local parser test result.

## Inspection environment and reproducible commands

Archives were saved outside the repository under `%TEMP%` on 2026-10-06. The isolated research environment is `research/ARCH-01/pyproject.toml` and `uv.lock`: Python 3.12.13, pandas 2.3.3, NumPy 2.5.3, PyArrow 21.0.0, uv 0.12.1, and Ruff 0.16.10 for script checks. `uv --cache-dir "$env:TEMP\brip-uv-cache" lock --check --project research/ARCH-01` resolved eight locked packages. Research outputs contain source metadata/statistics only; no battery source bytes were written under the repository.

```powershell
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/inspect_hust_archive.py "$env:TEMP\ARCH01-our_data.zip" research/ARCH-01/hust_archive_inventory.json
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/inspect_hust_payloads.py "$env:TEMP\ARCH01-our_data.zip" research/ARCH-01/hust_payload_inspection.json
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/inspect_aurora_archive.py "$env:TEMP\ARCH01-Dataset-rocrate.zip" --output research/ARCH-01/aurora_archive_inventory.json
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/inspect_aurora_lfp_cycles.py "$env:TEMP\ARCH01-Dataset-rocrate.zip" --output research/ARCH-01/aurora_lfp_cycle_profiles.json
```

`inspect_hust_archive.py` validates the pinned archive hash, exact 77 member paths and representative static pickle globals without executing payloads. `inspect_hust_payloads.py` validates that same hash and only unpickles with a strict allowlist for the observed NumPy/pandas globals. `inspect_aurora_archive.py` validates source size/MD5, exact archive member set/count, all per-cell metadata, all Parquet schemas/row counts/statistical nulls, and CSV/Parquet equality for selected chemistry representatives. `inspect_aurora_lfp_cycles.py` validates the same archive identity and summarizes the first seven cycle values, current/voltage ranges and cycle/time counter transitions for two exact LFP members without writing source rows. Each script asserts expected archive identity/structure and writes deterministic JSON.

## Direct HUST findings

The archive has exactly 77 `.pkl` member paths under `our_data/`, matching the full enumerated inventory in `research/ARCH-01/hust_archive_inventory.json`. Static opcode inspection found pickle protocol 4 and the allowlisted standard NumPy/pandas classes used by the selected payloads. The five deserialized payloads are boundary/representative cells `1-1`, `2-2`, `5-7`, `6-8`, and `10-8`.

| Member / payload key | Cycle entries | Rows | `dq` ↔ capacity comparison |
|---|---:|---:|---|
| `our_data/1-1.pkl` / `1-1` | 1,504 | 1,163,166 | all 1,504; max abs error `2.28e-13 mAh` |
| `our_data/2-2.pkl` / `2-2` | 2,651 | 1,563,012 | all 2,651; max abs error `2.28e-13 mAh` |
| `our_data/5-7.pkl` / `5-7` | 1,448 | 828,946 | all 1,448; max abs error `2.28e-13 mAh` |
| `our_data/6-8.pkl` / `6-8` | 2,450 | 1,358,891 | all 2,450; max abs error `2.28e-13 mAh` |
| `our_data/10-8.pkl` / `10-8` | 1,400 | 1,022,531 | all 1,400; max abs error `2.28e-13 mAh` |

All 9,453 inspected cycle frames had the same six-column schema: `Status`, `Cycle number`, `Current (mA)`, `Voltage (V)`, `Capacity (mAh)`, `Time (s)`. All six fields have zero nulls in the five inspected payloads. `data` is cycle-keyed; frame `Cycle number` equals its containing key in these samples. The six observed status values are CC charge, CC-CV charge, and CC discharge steps `_0` through `_3`. Current sign agrees with charge/discharge status. `dq[cycle]` matches `max(Capacity (mAh)) - final Capacity (mAh)`, establishing an empirical complete-cycle discharge-capacity relation and mAh scale for these five payloads. It does not justify mapping the row-level `Capacity (mAh)` itself to cycle capacity.

For each of the five cells, first-cycle `dq` is 0.233–0.283% greater than the median of cycles 1–10; observed values decline across those first ten. The original author code at [HAIRLAB/Health_status_prediction](https://github.com/HAIRLAB/Health_status_prediction/blob/main/common.py), pinned to inspected commit `8e9073edbc54c2620b5356e601a5d48abf70573d`, uses `dq` as capacity labels, `rul` as an RUL label, and slices away the first nine ordered keys. It does not identify those nine cycles as formation or a standardized capacity-reference test. The paper's 10th-cycle baseline applies to charge-curve features, not the SOH denominator. Remaining blockers: the 72 uninspected payloads, source-wide null/order semantics, and the Mendeley third-party caveat.

## Direct Aurora findings

The full archive has 797 ZIP entries: 199 cell directories × (`.metadata.json`, `.bdf.csv`, `.bdf.parquet`) plus `ro-crate-metadata.json`. All per-cell JSON-LD metadata records were parsed. The positive-electrode formulas and negative electrode metadata produce this exact archive inventory:

| Chemistry / negative electrode | Cells |
|---|---:|
| NMC622 / graphite (`LiNi0.6Co0.2Mn0.2O2`) | 135 |
| Ni-rich NMC / graphite (metadata `Ni0.83Mn0.06Co0.11O2`) | 32 |
| LFP / graphite (`LiFePO4`) | 32 |

Aurora LFP IDs: `ccid000217`–`ccid000247` except `ccid000248`, and `ccid000249`. The paper discusses a 36-cell LFP batch; the selected v1 archive includes 32 LFP records. Do not silently substitute the article population for the exact archive population. The paper identifies NMC811 as `LiNi0.83Mn0.10Co0.07O2`, while 32 archive JSON-LD records state positive formula `Ni0.83Mn0.06Co0.11O2`; retain the exact metadata formula and do not relabel these records as NMC811 until the discrepancy is clarified.

All 199 Parquet files have the same fields: `test_time_millisecond` int64, `current_ampere` float64, `voltage_volt` float64, `cycle_dimensionless` int64, `date_time_millisecond` int64, and `ambient_temperature_celsius` float64. Total row count is 99,715,350. Parquet statistics report zero nulls for all six fields in all 199 files. There is no explicit capacity, energy, status, or step field. CSV and Parquet field schemas and all values matched for `ccid000001`, `ccid000037`, `ccid000210`, and `ccid000249`. All 199 files show positive and negative current values; all temperature min/max statistics equal 25.0 °C. Cell IDs and batch/product IDs appear in JSON-LD metadata, alongside electrode materials/properties, rated-capacity values, and generated per-cell protocol structures. Rated capacity is metadata, not a measured cycle output.

All records include `cycle_dimensionless` starting at zero; the exact maximum varies. Across LFP records, the field returns to zero 16,240 times; across the 32 Ni-rich NMC metadata records it returns 13,349 times; across NMC622, 59 returns are recorded (91 total decreases). In LFP `ccid000217`, it returns to zero 506 times after having increased; `ccid000249` has 500 such returns. The sequences interleave zeros, for example `0,1,2,3,0,3,4,0,4`. Neither file has step/status/capacity fields resolving these resets. The Aurora paper's three formation cycles at 0.1 mA cm-2 followed by long-term cycling at 1.0 mA cm-2 describe its NMC622 case; do not generalize that phase count to LFP. The LFP discussion gives a 3.65 V upper cutoff. In both sampled LFP records, cycles 1–3 have currents around -0.154 to +0.154 mA; cycle 4 onward is around -1.54 to +1.54 mA. This confirms a current-level change but not the reason/phase mapping. A current-integrated complete-cycle capacity is therefore not approved.

## SOH, formation, leakage, grouping, and cross-source decision

- **Numerator:** HUST `dq` is a supported per-cycle discharge-capacity candidate in five files. Aurora has no source-reported capacity value; current/time integration needs an unambiguous complete-discharge grouping that is not established from its LFP BDF rows.
- **Reference capacity:** none selected. Do not use nominal/rated capacity, one first cycle, full-life maximum, or an arbitrary post-formation window. HUST has no verified formation/reference-cycle declaration; Aurora's three literature-described formation cycles apply to its NMC622 case, not by assumption to LFP. Candidate early-window statistics do not establish stable-reference capacity semantics.
- **Early cycles:** HUST first vs cycles 1–10 median results are shown above. The Aurora NMC622 formation sequence is not assigned to LFP; the LFP row samples show a current-level change across cycle values 1–3 and 4 onward, but unresolved reset semantics prevent an approved phase mapping.
- **Leakage:** exclude the target and aliases (`dq`, current target capacity), denominator, `rul`, precomputed SOH/EOL, future-cycle measurements, full-life summaries, and cumulative values with unknown reset semantics. Keep identifiers/source/protocol/batch and age proxies out of predictors absent a defined prediction cutoff and independent review.
- **Physical-cell grouping key:** `(source_name, source_record_version, source_native_cell_id)`. HUST key is the nested cell identifier such as `1-1`; Aurora uses the source-namespaced `ccid000XXX` cell ID. Do not join IDs across sources.
- **Cross-source:** quantitative HUST→Aurora SOH comparison is **not approved**. A possible stress subset is LFP/graphite only (77 HUST cylindrical A123 cells vs 32 Aurora CR2032 coin cells). It also shifts lab/source, temperature (30 vs 25 °C), electrode batch/design, formation and discharge protocol. If target/reference becomes valid, report HUST in-domain and Aurora zero-shot separately as exploratory combined domain shift; never call it isolated source/chemistry transfer or a like-for-like benchmark. Without a common target, omit SOH metrics.

## Canonical field disposition

The BDF specification's required concepts are elapsed time, voltage, and current; current is positive on charge and negative on discharge. Candidate Aurora mappings are `test_time_millisecond / 1000 → test_time_s`, `current_ampere → current_a`, `voltage_volt → voltage_v`, `date_time_millisecond / 1000 → unix_time_s` (retain original and confirm epoch/UTC interpretation), and `ambient_temperature_celsius → ambient_temperature_c`. Preserve `cycle_dimensionless` source-specifically; do not normalize its resets to a canonical cycle index. HUST candidates are `Time (s) → test_time_s`, `Current (mA) / 1000 → current_a`, `Voltage (V) → voltage_v`; candidate `dq / 1000 → cycle_discharging_capacity_ah` only within inspected samples and not yet adapter-approved source-wide. Retain `Status`, native IDs, and raw capacity fields source-specifically. Required/optional/nullable/derived/unavailable mappings and non-coercion rules are in [DATA_CONTRACT.md](../../DATA_CONTRACT.md).

## ARCH-00 / ARCH-01 acceptance audit

| Criterion | Result | Exact disposition |
|---|---|---|
| Exact selected source artifacts, members, checksums, record licenses | **PARTIAL** | Both archive identities/checksums verified. HUST record says CC BY 4.0 but third-party applicability/rights are not resolvable from archive. |
| HUST schema, `dq`, units, cycle/step/current semantics | **PARTIAL** | Direct and exact for five full cell payloads; other 72 and source-wide null/order audit remain. |
| Aurora 199-cell chemistry inventory, schemas, nulls, formats | **PASS for inspected v1 archive** | Exact 135/32/32 inventory, common six-field schema, no reported nulls, 4 direct CSV/Parquet value comparisons. |
| Aurora cycle/capacity fields and semantics | **BLOCKED** | No capacity/step/status field; LFP cycle counter resets; no evidenced non-guessed complete-discharge roll-up. |
| SOH numerator/reference definition | **BLOCKED** | HUST candidate supported in five files; no Aurora numerator mapping and no defensible common deterministic reference rule. |
| Formation/reference window | **BLOCKED** | Aurora paper's first-three formation cycles describe NMC622, not established for LFP; archive cycle indexes ambiguous. HUST has no source-declared formation/reference window. |
| Leakage/grouping | **PASS as evaluation policy** | Risks and source-namespaced physical-cell group key documented; target itself remains unavailable. |
| Cross-source evaluation | **BLOCKED / constrained candidate** | No SOH metrics approved. Only future same-chemistry LFP exploratory combined-shift design can be reconsidered after target alignment. |
| Source-specific required/optional/nullable/derived/unavailable contract | **PARTIAL** | Direct measured fields and unknowns recorded; ambiguous mappings explicitly stay source-specific. |
| No production pipeline/ML work | **PASS** | Research scripts, dependency lock, documentation, and audit outputs only. |

Because blockers remain, **ARCH-00 and ARCH-01 are BLOCKED**. No downstream task is unblocked. Continue only with an architecture/source-owner review of the third-party notice, remaining HUST payloads, and Aurora cycle/capacity semantics. Do not begin INGEST-01.

## Validation and output integrity

Research output JSON SHA-256 values were identical on repeat runs of each script:

| Output | SHA-256 |
|---|---|
| `research/ARCH-01/hust_archive_inventory.json` | `59c89f2fc2dfe37a78d72a537a38d397de0e4ef788c69f68a4245c95af6a0c7` |
| `research/ARCH-01/hust_payload_inspection.json` | `b64c8ca35ca0374f21b8ae914e27df57e80128eacdffa65e8a256902bd00ccf2` |
| `research/ARCH-01/aurora_archive_inventory.json` | `2df94438ebc1f5a4ce8c2efe5f7ded934f99225ee5a2132bbd958f6618b43d62` |
| `research/ARCH-01/aurora_lfp_cycle_profiles.json` | `1e289b6080c2073d4f15cf1e1111e799579dcd03efd3bb19f464d29925958908` |

Validation completed: `uv --cache-dir "$env:TEMP\brip-uv-cache" lock --check --project research/ARCH-01`; all four research scripts ran with `uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked ...`; Ruff check and format check pass for `research/ARCH-01`; a relative-link audit checked 12 edited Markdown files and found zero broken local links; `git diff --check` and final manual acceptance/cross-document review are recorded in the commit log. A project Markdown lint command is not configured. Audit scripts contain archive identity/member/schema/equality assertions; no production test suite was needed or changed. No ingestion, feature/model, or application code was added.
