# ARCH-01 Evidence — Direct Source and SOH Blocker Audit

- **Disposition:** PASS for the documented source selection, canonical data boundary, SOH target, and evaluation design; ingestion/model implementation still require architecture review and their task cards.
- **Research date:** 2026-10-06 to 2026-10-07 (supplemental HUST/license audit).
- **Branch:** `docs/ARCH-01-blocker-resolution`.
- **Commit reference:** the dedicated ARCH-01 research commit on this branch (reported with its SHA in the completion summary).
- **Purpose:** Resolve the source-level uncertainties in ARCH-00 using the exact archives and authoritative records, without committing dataset bytes. Earlier audit observations below are preserved; the supplemental all-cell LFP and HUST label audits supersede their provisional blocker conclusions.

## Primary records, selected artifacts, and rights

### HUST

- Record: [Mendeley Data v2, DOI 10.17632/nsc7hnsg4s.2](https://data.mendeley.com/datasets/nsc7hnsg4s/2); source metadata [API](https://data.mendeley.com/public-api/datasets/nsc7hnsg4s).
- Exact file: `our_data.zip`; file id `5ca0ac3e-d598-4d07-8dcb-879aa047e98b`; 1,188,136,932 bytes; expected and locally verified SHA-256 `071d24617153693b0d29059568525e620f6af6512acc9d00c98c7adcf15125db`.
- Primary article: Ma et al., [Energy & Environmental Science (2022), DOI 10.1039/D2EE01676A](https://pubs.rsc.org/en/content/articlehtml/2022/ee/d2ee01676a). The article describes 77 A123 APR18650M1A LFP/graphite cylindrical cells, nominal 1.1 Ah/3.3 V, 30 °C, common fast charging, and personalized multistage discharges; it treats capacity as a health output.
- The dataset record declares CC BY 4.0; see the [legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en). Attribution, license link, and change indication apply. Mendeley notes that further permission may be required for content identified as third-party. The supplemental 2026-10-07 archive review found only the 77 data pickle members and no identified third-party component or per-member carve-out. Record-level redistribution is permitted under CC BY 4.0 for the licensed dataset material; the license cannot grant rights to any separately identified third-party content. The RSC article license is separate.

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
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/inspect_hust_payloads.py "$env:TEMP\ARCH01-our_data.zip" research/ARCH-01/hust_seven_payload_audit.json --members our_data/1-1.pkl our_data/2-2.pkl our_data/5-7.pkl our_data/6-8.pkl our_data/10-8.pkl our_data/2-5.pkl our_data/1-2.pkl
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/summarize_hust_reference_sensitivity.py research/ARCH-01/hust_reference_sensitivity.json research/ARCH-01/hust_seven_payload_audit.json
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/inspect_aurora_archive.py "$env:TEMP\ARCH01-Dataset-rocrate.zip" --output research/ARCH-01/aurora_archive_inventory.json
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/inspect_aurora_lfp_cycles.py "$env:TEMP\ARCH01-Dataset-rocrate.zip" --output research/ARCH-01/aurora_lfp_cycle_profiles.json
```

`inspect_hust_archive.py` validates the pinned archive hash, exact 77 member paths and representative static pickle globals without executing payloads. `inspect_hust_payloads.py` validates that same hash and only unpickles with a strict allowlist for the observed NumPy/pandas globals. `inspect_aurora_archive.py` validates source size/MD5, exact archive member set/count, all per-cell metadata, all Parquet schemas/row counts/statistical nulls, and CSV/Parquet equality for selected chemistry representatives. `inspect_aurora_lfp_cycles.py` validates the same archive identity and summarizes the first seven cycle values, current/voltage ranges and cycle/time counter transitions for two exact LFP members without writing source rows. Each script asserts expected archive identity/structure and writes deterministic JSON.

## Initial direct HUST findings (five-payload audit phase; expanded below)

The archive has exactly 77 `.pkl` member paths under `our_data/`, matching the full enumerated inventory in `research/ARCH-01/hust_archive_inventory.json`. Static opcode inspection found pickle protocol 4 and the allowlisted standard NumPy/pandas classes used by the selected payloads. The initial five deserialized payloads were representative cells `1-1`, `2-2`, `5-7`, `6-8`, and `10-8`; minimum/maximum-size members were later inspected as described below.

| Member / payload key | Cycle entries | Rows | `dq` ↔ capacity comparison |
|---|---:|---:|---|
| `our_data/1-1.pkl` / `1-1` | 1,504 | 1,163,166 | all 1,504; max abs error `2.28e-13 mAh` |
| `our_data/2-2.pkl` / `2-2` | 2,651 | 1,563,012 | all 2,651; max abs error `2.28e-13 mAh` |
| `our_data/5-7.pkl` / `5-7` | 1,448 | 828,946 | all 1,448; max abs error `2.28e-13 mAh` |
| `our_data/6-8.pkl` / `6-8` | 2,450 | 1,358,891 | all 2,450; max abs error `2.28e-13 mAh` |
| `our_data/10-8.pkl` / `10-8` | 1,400 | 1,022,531 | all 1,400; max abs error `2.28e-13 mAh` |

All 9,453 inspected cycle frames had the same six-column schema: `Status`, `Cycle number`, `Current (mA)`, `Voltage (V)`, `Capacity (mAh)`, `Time (s)`. All six fields have zero nulls in the five inspected payloads. `data` is cycle-keyed; frame `Cycle number` equals its containing key in these samples. The six observed status values are CC charge, CC-CV charge, and CC discharge steps `_0` through `_3`. Current sign agrees with charge/discharge status. `dq[cycle]` matches `max(Capacity (mAh)) - final Capacity (mAh)`, establishing an empirical complete-cycle discharge-capacity relation and mAh scale for these five payloads. It does not justify mapping the row-level `Capacity (mAh)` itself to cycle capacity.

For each of the initial five cells, first-cycle `dq` is 0.233–0.283% greater than the median of cycles 1–10; observed values decline across those first ten. The original author code at [HAIRLAB/Health_status_prediction](https://github.com/HAIRLAB/Health_status_prediction/blob/main/common.py), pinned to inspected commit `8e9073edbc54c2620b5356e601a5d48abf70573d`, uses `dq` as capacity labels, `rul` as an RUL label, and slices away the first nine ordered keys. It does not identify those nine cycles as formation or a standardized capacity-reference test. The paper's 10th-cycle baseline applies to charge-curve features, not the SOH denominator. Supplemental seven-cell comparisons are below; 70 payloads remain un-deserialized and source-wide null/order semantics are not established.

## Supplemental HUST sample and rights audit (2026-10-07; seven row-inspected payloads)

The initial five-cell audit was expanded to seven payloads chosen to cover the initial representative set plus the smallest and largest uncompressed ZIP members: `our_data/2-5.pkl` (36,734,361 uncompressed bytes) and `our_data/1-2.pkl` (88,277,079 bytes). The source inventory still enumerates all 77 exact `.pkl` members; the other 70 payloads have not been deserialized. All pickle loads use the inspector's strict NumPy/pandas/builtins allowlist.

| Payload | Cycle frames and matched `dq` labels | Rows | Cycle key == frame number | Maximum `dq` relation error |
|---|---:|---:|---:|---:|
| `1-1` | 1,504 | 1,163,166 | 1,504 / 1,504 | `2.28e-13 mAh` |
| `2-2` | 2,651 | 1,563,012 | 2,651 / 2,651 | `2.28e-13 mAh` |
| `5-7` | 1,448 | 828,946 | 1,448 / 1,448 | `2.28e-13 mAh` |
| `6-8` | 2,450 | 1,358,891 | 2,450 / 2,450 | `2.28e-13 mAh` |
| `10-8` | 1,400 | 1,022,531 | 1,400 / 1,400 | `2.28e-13 mAh` |
| `2-5` (smallest member) | 1,386 | 791,546 | 1,386 / 1,386 | `2.28e-13 mAh` |
| `1-2` (largest member) | 2,678 | 1,913,792 | 2,678 / 2,678 | `2.28e-13 mAh` |
| **Total** | **13,517** | **8,641,884** | **13,517 / 13,517** | **maximum** `2.28e-13 mAh` |

Every frame in the seven payloads has the same six columns and zero nulls in those columns. Each frame's `Cycle number` equals its containing `data` map key, and the `dq` key count matches the cycle-frame count. `dq` matches `max(Capacity (mAh)) - final Capacity (mAh)` for every matched cycle. This strengthens, but does not establish, source-wide behavior for the 70 uninspected payloads.

Early-window comparison was computed from ordered numeric `dq` labels. First valid cycle is key 1 for all seven samples. Across seven cells, first-cycle deviation from the median over the first 3 cycles ranges 0.000% to +0.103%; for first 5, −0.059% to +0.200%; first 10, −0.403% to +0.283%; first 30, −1.330% to +0.554%. The smallest payload (`2-5`) changes direction relative to the other six as windows widen. Window ranges also increase: maximum within-window range is 0.200%, 0.373%, 0.894%, and 1.822% of that window's median for windows 3, 5, 10, and 30 respectively. These data do not establish a common formation phase or stable reference rule. The author code's omission of nine early labels remains a preprocessing convention, not a source-declared formation test.

The exact [Mendeley v2 page](https://data.mendeley.com/datasets/nsc7hnsg4s/2) displays CC BY 4.0. The [license legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) explicitly grants reproduction and sharing of the licensed material (including database contents) subject to attribution, license reference, and modification notice. It grants only rights the licensor can grant; Mendeley notes that further permission can be required for content identified as third-party. The archive comprises the 77 data pickle members and has no per-member rights manifest or third-party item identified. Therefore record-level redistribution is permitted under CC BY 4.0 for the licensed dataset material; no conclusion is made about separately identified third-party material or the separately licensed paper. The Mendeley FAQ notes CC BY 4.0 is the interface default but can be changed; this record specifically displays CC BY 4.0. No source bytes are committed here.

## Initial direct Aurora findings (before the all-32 LFP audit below)

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

- **Numerator:** HUST `dq` is supported as a per-cycle discharge-capacity value in seven inspected files. Aurora has no source-reported capacity value; current/time integration needs an unambiguous complete-discharge grouping that is not established from its LFP BDF rows.
- **Reference capacity:** none selected. Do not use nominal/rated capacity, one first cycle, full-life maximum, or an arbitrary post-formation window. HUST has no verified formation/reference-cycle declaration; Aurora's three literature-described formation cycles apply to its NMC622 case, not by assumption to LFP. Candidate early-window statistics do not establish stable-reference capacity semantics.
- **Early cycles:** HUST first vs cycles 1–10 median results are shown above. The Aurora NMC622 formation sequence is not assigned to LFP; the LFP row samples show a current-level change across cycle values 1–3 and 4 onward, but unresolved reset semantics prevent an approved phase mapping.
- **Leakage:** exclude the target and aliases (`dq`, current target capacity), denominator, `rul`, precomputed SOH/EOL, future-cycle measurements, full-life summaries, and cumulative values with unknown reset semantics. Keep identifiers/source/protocol/batch and age proxies out of predictors absent a defined prediction cutoff and independent review.
- **Physical-cell grouping key:** `(source_name, source_record_version, source_native_cell_id)`. HUST key is the nested cell identifier such as `1-1`; Aurora uses the source-namespaced `ccid000XXX` cell ID. Do not join IDs across sources.
- **Cross-source:** quantitative HUST→Aurora SOH comparison is **not approved**. A possible stress subset is LFP/graphite only (77 HUST cylindrical A123 cells vs 32 Aurora CR2032 coin cells). It also shifts lab/source, temperature (30 vs 25 °C), electrode batch/design, formation and discharge protocol. If target/reference becomes valid, report HUST in-domain and Aurora zero-shot separately as exploratory combined domain shift; never call it isolated source/chemistry transfer or a like-for-like benchmark. Without a common target, omit SOH metrics.

## Canonical field disposition

The BDF specification's required concepts are elapsed time, voltage, and current; current is positive on charge and negative on discharge. Candidate Aurora mappings are `test_time_millisecond / 1000 → test_time_s`, `current_ampere → current_a`, `voltage_volt → voltage_v`, `date_time_millisecond / 1000 → unix_time_s` (retain original and confirm epoch/UTC interpretation), and `ambient_temperature_celsius → ambient_temperature_c`. Preserve `cycle_dimensionless` source-specifically; do not normalize its resets to a canonical cycle index. HUST candidates are `Time (s) → test_time_s`, `Current (mA) / 1000 → current_a`, `Voltage (V) → voltage_v`; candidate `dq / 1000 → cycle_discharging_capacity_ah` only within inspected samples and not yet adapter-approved source-wide. Retain `Status`, native IDs, and raw capacity fields source-specifically. Required/optional/nullable/derived/unavailable mappings and non-coercion rules are in [DATA_CONTRACT.md](../../DATA_CONTRACT.md).

## Supplemental all-member HUST and all-LFP Aurora audit (2026-10-07)

The following audits supersede provisional target/cycle blockers in the earlier evidence sections. Earlier source observations remain valid where they describe coverage limits; in particular, HUST row-level frame inspection covers seven payloads, while the new all-77 audit covers label/key structure and early-window statistics.

### HUST all-77 label audit

`audit_hust_reference_windows_all.py` safely deserialized each of the exact 77 allowlisted payloads after checking the pinned archive SHA-256 and exact ZIP member inventory. For all 77: the nested cell key matches the filename; `data`, `dq`, and `rul` key sets and insertion order match; the first cycle key is 1; and `dq` keys are strictly increasing. It computes first-1/3/5/10/30 label-window summaries for every cell. This does not inspect every frame/schema: seven representative/edge payloads remain the complete row-level inspection sample (13,517 cycles, 8,641,884 rows), with zero nulls and `dq = max(Capacity (mAh)) - final Capacity (mAh)` within 2.28e-13 mAh.

Across the 77 cell-level label series, the first-three-cycle window has a minimum/median/maximum within-window range of 0.054% / 0.154% / 0.724% of the window median. First-cycle deviation from the first-three median is −0.314% / +0.101% / +0.619% (min/median/max). For 5/10/30-cycle windows, maximum within-window ranges are 0.830% / 1.289% / 1.961%. This supports a stable, causal operational baseline but does not make HUST's first cycles a source-declared formation test. Do not interpret the author's omission of nine labels as formation.

### Aurora LFP protocol and discharge-capacity audit

`audit_aurora_lfp_protocol_alignment.py` inspected all 32 selected LFP metadata records and their Parquet time series. All 32 metadata protocols have one identical signature: three iterations at 0.1 mA cm⁻² followed by a 1,000-iteration 1.0 mA cm⁻² aging loop. The protocol includes charge to 3.65 V, CV hold to 0.05 mA cm⁻², discharge to 2.5 V, and an initial six-hour rest. This directly establishes an LFP-specific conditioning/aging phase split; it does not rely on generalizing the paper's NMC622 paragraph.

Capacity is not a source column. The reproducible derivation integrates `abs(current_ampere)` by trapezoid over `test_time_millisecond` for ordered contiguous negative-current runs. Zero-duration/singleton artifacts are strongly separated: the largest run below 0.1 mAh is 0.004278 mAh; the smallest run at/above 0.1 mAh is 0.275733 mAh, a factor of 64.46. The 0.1 mAh cut is interior to this observed gap and returns exactly 1,003 events in every LFP cell, matching the 3 + 1,000 protocol iteration counts. Preserve the source `cycle_dimensionless` reset values; the derived event ordinal is separate, auditable, and versioned.

The first three 0.1 mA cm⁻² discharge capacities vary by 2.026% / 3.082% / 6.749% (minimum/median/maximum range as a percent of the three-value median). These conditioning capacities are rate-distinct and are not the aging reference. The first aging event is 2.331%–5.171% below the median conditioning capacity. Among the first three 1.0 mA cm⁻² aging capacities, the range is 0.386% / 0.669% / 1.374% of the median (min/median/max); the first aging capacity differs from its first-three median by 0.123% / 0.342% / 0.916%. All 192 reference events (three conditioning + three aging events across 32 cells) end within 0.08 V of the protocol's 2.5 V cutoff. In 29/32 cells, all 1,003 substantial events fall within that cutoff diagnostic; each of `ccid000217`, `ccid000231`, and `ccid000247` has one other aging event outside it. Quarantine those three individual events and retain the otherwise quality-passing capacity observations.

### Final SOH reference, leakage, and cross-source decision

ADR-003 freezes this source-aware deterministic operational rule: `reference_capacity(cell) = median(first three complete discharge-capacity observations in the sustained-aging protocol)`. HUST uses `dq` keys 1–3; Aurora LFP skips its metadata-defined three low-rate conditioning events and uses the next three 1.0 mA cm⁻² discharge events. Do not score baseline observations. This reference is available before every scored target and does not use future or full-life information. HUST's early cycles are not labeled formation; its inclusion is an operational baseline choice supported by the all-77 stability audit. The SOH is a normalized within-cell trajectory, not absolute cross-source capacity.

Approve exploratory zero-shot HUST→Aurora evaluation on LFP/graphite only: 77 A123 cylindrical cells vs the exact 32 Aurora CR2032 coin cells, using each source's verified within-cell reference rule. Describe it as a **combined** source/lab, cell-design, batch/construction, temperature (30 vs 25 °C), and discharge-protocol shift; do not attribute the result to an isolated source or chemistry effect. Also reserve whole HUST personalized-protocol families for a grouped within-source domain-shift evaluation. Use physical-cell group key `(source_name, source_record_version, source_native_cell_id)`. Exclude target capacity/aliases, reference denominator, `dq`/`rul`, future cycles, full-life statistics, uncertain accumulators, and unapproved IDs/protocol/age proxies from model features.

### Reproducible commands and output hashes

```powershell
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/audit_hust_reference_windows_all.py "$env:TEMP\ARCH01-our_data.zip" research/ARCH-01/hust_all77_reference_window_audit.json
uv --cache-dir "$env:TEMP\brip-uv-cache" run --offline --project research/ARCH-01 --locked python research/ARCH-01/audit_aurora_lfp_protocol_alignment.py "$env:TEMP\ARCH01-Dataset-rocrate.zip" research/ARCH-01/aurora_lfp_protocol_alignment.json
```

- `hust_all77_reference_window_audit.json` SHA-256: `060455e2e6f73bbea9f6130455c46e4827b49978e41857c576d597ff76e5e403`.
- `aurora_lfp_protocol_alignment.json` SHA-256: `f807203e507db629587fbf3badf5e12242b4d314302dfc156321e1471833f603`.
- Re-running both scripts against the same exact archives produced byte-identical JSON hashes. Research scripts are outside the production package and source bytes remain outside Git.

## ARCH-00 / ARCH-01 acceptance audit

| Criterion | Result | Exact disposition |
|---|---|---|
| Exact selected source artifacts, members, checksums, record licenses | **PASS** | Both archive identities/checksums and CC BY 4.0 records verified. HUST record-level sharing applies to licensed material; no third-party component is identified in the exact archive. |
| HUST schema, `dq`, units, cycle/step/current semantics | **PASS with stated row coverage** | All 77 payload label/key structures and window summaries verified; seven full payloads (13,517 cycles) have frame schema, null, current/status, and `dq` formula comparison. Ingestion must validate every member. |
| Aurora 199-cell chemistry inventory, schemas, nulls, formats | **PASS** | Exact 135/32/32 inventory, common six-field schema, no reported nulls, and four direct CSV/Parquet value comparisons. |
| Aurora selected LFP cycle/capacity fields and semantics | **PASS with event quarantine** | Exact LFP-specific protocol metadata and 1,003 integrated discharge events per cell verified for all 32 cells; preserve native resets and quarantine three cutoff-diagnostic outlier events. |
| SOH numerator/reference definition | **PASS for selected subsets** | HUST `dq` in row-inspected payloads and Aurora protocol-aligned integrated capacity; first-three sustained-protocol median is source-aware and causal. |
| Formation/reference window | **PASS with source distinction** | Aurora's LFP metadata declares three low-rate conditioning events; HUST has no labeled formation phase and uses keys 1–3 as an operational reference. |
| Leakage/grouping | **PASS** | Target/feature exclusions and source-namespaced physical-cell group key are explicit. |
| Cross-source evaluation | **PASS as bounded combined-shift stress test** | Same-chemistry LFP only; explicitly reports simultaneous source/lab, design, batch, temperature, and protocol shifts. |
| Source-specific required/optional/nullable/derived/unavailable contract | **PASS for selected V1 scope** | Direct, derived, source-specific, and unavailable fields are distinguished; ambiguous fields remain raw/nullable. |
| No production pipeline/ML work | **PASS** | Research scripts, dependency lock, documentation, and audit outputs only. |

**ARCH-00 and ARCH-01 are PASS** for the documented data selection and target design. This resolves the research gate but does not authorize implementation: stop for architecture review, then create/approve a scoped INGEST-01 task card. No ingestion, features, or ML code is included in this commit. Remaining limitations—seven HUST row-inspected payloads, three quarantined Aurora outlier events, four CSV/Parquet pair comparisons, catalog-only fixture verification, and the unreconciled non-LFP formula—are listed in scope and must remain visible during implementation.

## Validation and output integrity

Research output JSON SHA-256 values were identical on repeat runs of each script:

| Output | SHA-256 |
|---|---|
| `research/ARCH-01/hust_archive_inventory.json` | `59c89f2fc2dfe37a78d72a537a38d397de0e4ef788c69f68a4245c95af6a0c7` |
| `research/ARCH-01/hust_payload_inspection.json` | `b64c8ca35ca0374f21b8ae914e27df57e80128eacdffa65e8a256902bd00ccf2` |
| `research/ARCH-01/aurora_archive_inventory.json` | `2df94438ebc1f5a4ce8c2efe5f7ded934f99225ee5a2132bbd958f6618b43d62` |
| `research/ARCH-01/aurora_lfp_cycle_profiles.json` | `1e289b6080c2073d4f15cf1e1111e799579dcd03efd3bb19f464d29925958908` |
| `research/ARCH-01/hust_seven_payload_audit.json` | `24f8c9ea747c5de08d36009449a1a8eec96a166ca1be02695630153015edbba4` |
| `research/ARCH-01/hust_reference_sensitivity.json` | `0b642e2eef93c2825cc5c35a9bb0da0d125b3721079521012af332a9d55f3361` |

Validation completed: `uv --cache-dir "$env:TEMP\brip-uv-cache" lock --check --project research/ARCH-01`; archive/member, selected payload, all-77 HUST label/reference, all-199 Aurora inventory, representative Aurora cycle, and all-32 Aurora LFP protocol/capacity audit scripts ran with the locked offline research environment; Ruff check and format check pass for `research/ARCH-01`; a relative-link audit checked all 11 changed Markdown files and found zero broken local links; `git diff --check` and final manual acceptance/cross-document review are recorded in the commit log. The two final audit outputs were repeated byte-identically (hashes above). A project Markdown lint command is not configured. No production test suite was needed or changed. No ingestion, feature/model, or application code was added.
