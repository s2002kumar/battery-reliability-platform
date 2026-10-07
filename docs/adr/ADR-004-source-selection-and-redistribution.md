# ADR-004: Dataset Selection and Redistribution

- **Status:** Accepted for ARCH-00/ARCH-01 source selection and record-level rights
- **Date:** 2026-10-07
- **Scope:** V1 public data, legal terms, and robustness fixtures

## Selected candidate records

1. **HUST supervised-data selection:** Mendeley v2, DOI `10.17632/nsc7hnsg4s.2`, exact `our_data.zip` artifact. Record declares CC BY 4.0. Archive has 77 pickle members; all 77 ordered data/label key structures and early reference-window labels were audited. Seven representative/edge payloads, including the smallest and largest members, received row-level inspection; `dq` matches per-cycle discharge capacity in all 13,517 inspected cycles.
2. **Empa Aurora BDF/second-source selection:** Zenodo v1, DOI `10.5281/zenodo.15481956`, exact `Dataset-rocrate.zip`. Record declares CC BY 4.0. Archive includes 199 cells: 135 NMC622, 32 LFP, and 32 whose metadata formula is `Ni0.83Mn0.06Co0.11O2`. The last formula differs from the original paper's stated NMC811 composition; do not relabel it absent clarification. The SOH subset is the 32 metadata-verified LFP cells; their JSON-LD protocols and current/time traces support a separately derived discharge-event ordinal and capacity.
3. **BDA/SINTEF/DLR pipeline fixture candidate:** Zenodo v0.8.0, DOI `10.5281/zenodo.21337233`. The official record declares CC BY 4.0 and its metadata catalog gives per-file SPDX CC-BY-4.0. Six exact fixture candidates and bug descriptions are in [DATA_SOURCES.md](../../DATA_SOURCES.md). The bytes have not been fetched, so catalog provenance is not yet a test-result claim.

## Terms and redistribution decision

- The exact HUST Mendeley v2 record displays [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en). That license grants reproduction/sharing and adaptation of licensed material, subject to attribution, license/link retention, and change indication. Its scope is limited to rights the licensor can grant; the record warns that additional permission may be needed for content identified as third-party. The exact archive contains 77 data pickle members and no per-member rights manifest or identified third-party component. Record-level redistribution is therefore permitted under CC BY 4.0 for the licensed dataset material; this does not assert rights in separately identified third-party content or the RSC article. Preserve attribution and provenance. No source bytes are committed to this repository.
- Aurora Zenodo v1 declares CC BY 4.0. Attribute record creators, cite/version the artifact, include the license and modifications. Do not treat per-cell rated-capacity metadata as measured data or make broader rights claims than the record license.
- The fixture catalog declares each listed item CC-BY-4.0. Preserve source citations and metadata if later retrieved; do not commit the large files without a separate storage choice.
- Paper/article licenses do not replace the dataset record licenses. No rights are inferred from public accessibility.

## Consequences and evidence

Keep exact source records pinned, retrieve immutable source artifacts outside Git, and retain locally computed SHA-256 plus provenance/attribution metadata. Do not claim absolute capacity comparability. The approved normalized SOH target and bounded combined-shift HUST-to-Aurora LFP evaluation are defined in ADR-003 and the evaluation plan. The six clean/bad pipeline files are licensed catalog candidates, but their actual bytes must be verified before treating their issue classifications as local parser test results.

Direct artifact identities, source checksums, exact Aurora chemistry IDs/schema, selected fixture classes, and coverage limitations appear in [ARCH-01 evidence](../evidence/ARCH-01.md) and [DATA_SOURCES.md](../../DATA_SOURCES.md). Ingestion still requires architecture review and its scoped task card.
