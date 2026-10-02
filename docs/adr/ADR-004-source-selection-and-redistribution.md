# ADR-004: Candidate Dataset Selection and Redistribution Policy

- **Status:** Candidate records verified; exact V1 file subset blocked for HUST/Aurora
- **Date:** 2026-10-02
- **Scope:** Public dataset selection, fixture scope, and redistribution

## Candidate records

1. **HUST:** Mendeley dataset version 2, DOI `10.17632/nsc7hnsg4s.2`, CC BY 4.0 per the [authoritative record](https://data.mendeley.com/datasets/nsc7hnsg4s/2). Candidate supervised source. Record describes 77 LFP/graphite cells and varying multistage discharge protocols. The `our_data.zip` archive and all 77 member names were inventoried; one pickle member's DataFrame field names and the authors' `dq`/`rul` preprocessing use were inspected. Complete `dq`, cycle, capacity, protocol, and third-party-notice semantics remain unresolved, so selection is not final.
2. **Empa Aurora:** Zenodo v1, DOI `10.5281/zenodo.15481956`, CC BY 4.0 per [Zenodo record metadata](https://zenodo.org/api/records/15481956). Exact archive `Dataset-rocrate.zip`, 2,507,129,091 bytes, MD5 `eaec9549b74b59d998e5138dab965b5d`; its 199 per-cell metadata/BDF file trios were inventoried and one NMC622 metadata file inspected. Exact chemistry subset, time-series rows, and capacity schema remain unverified.
3. **Robustness fixtures:** SINTEF Battery Lab Zenodo v0.8.0, DOI `10.5281/zenodo.21337233`, record-level CC BY 4.0 and per-dataset `CC-BY-4.0` in its [machine-readable catalog](https://zenodo.org/api/records/21337233/files/metadata.json/content). Initial proposed subset is four clean DLR Basytec fixtures and two intentionally bad SINTEF fixtures listed in [DATA_SOURCES.md](../../DATA_SOURCES.md). They are not ML-training data.

## Redistribution decision

The three source records' CC BY 4.0 metadata is verified. The [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) permits sharing and adaptation, including commercially, subject to attribution, license link, change indication, and no additional restrictions; retain supplied creator, copyright, and disclaimer notices. It licenses only rights the licensor can grant and does not itself clear other rights. Preserve separate attribution and provenance for each artifact. Do not describe the publisher's general “open” status as license permission. Do not commit full datasets: keep raw downloads external to Git; reconsider only a minimal, approved robustness fixture set with attribution and source checksums.

## Source-selection limits

- HUST and Aurora are not yet approved as a joint SOH benchmark: exact artifact fields, capacity methods, reference windows, and cell-level subsets remain to be inspected.
- The only candidate comparison is LFP/graphite against LFP//graphite, reported as a combined source/cell-design/protocol stress test, not isolated source or chemistry transfer. Do not make the comparison if target definitions cannot be aligned.
- BDA/SINTEF/DLR fixtures are approved for parser/validation testing only after retrieving exact versioned files and preserving their file-level license metadata. The initial named subset has verified catalog classifications; bytes have not been downloaded or hashed locally.

## Evidence

- HUST: [Mendeley record v2](https://data.mendeley.com/datasets/nsc7hnsg4s/2); [original paper DOI](https://doi.org/10.1039/D2EE01676A).
- Empa Aurora: [Zenodo record v1](https://doi.org/10.5281/zenodo.15481956); [record API JSON/license/file metadata](https://zenodo.org/api/records/15481956); [original paper DOI](https://doi.org/10.1002/batt.202500155).
- Fixtures: [Zenodo record v0.8.0](https://doi.org/10.5281/zenodo.21337233); [record API JSON](https://zenodo.org/api/records/21337233); [per-file catalog](https://zenodo.org/api/records/21337233/files/metadata.json/content); [README](https://zenodo.org/records/21337233).
- Canonical terms: [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en).
