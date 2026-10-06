# ADR-004: Dataset Selection and Redistribution

- **Status:** Candidate record selection verified; source ingestion/redistribution scope BLOCKED
- **Date:** 2026-10-06
- **Scope:** V1 public data, legal terms, and robustness fixtures

## Selected candidate records

1. **HUST supervised-data candidate:** Mendeley v2, DOI `10.17632/nsc7hnsg4s.2`, exact `our_data.zip` artifact. Record declares CC BY 4.0. Archive has 77 pickle members; five complete payloads were inspected. HUST `dq` is supported as per-cycle discharge capacity in those five files, but the remaining files and third-party-rights notice have not been cleared for full-source ingestion/redistribution.
2. **Empa Aurora BDF/second-source candidate:** Zenodo v1, DOI `10.5281/zenodo.15481956`, exact `Dataset-rocrate.zip`. Record declares CC BY 4.0. Archive includes 199 cells: 135 NMC622, 32 LFP, and 32 whose metadata formula is `Ni0.83Mn0.06Co0.11O2`. The last formula differs from the original paper's stated NMC811 composition; do not relabel it absent clarification. The six-column time series has no capacity field; LFP cycle-count resets block cycle/capacity mapping and SOH target approval.
3. **BDA/SINTEF/DLR pipeline fixture candidate:** Zenodo v0.8.0, DOI `10.5281/zenodo.21337233`. The official record declares CC BY 4.0 and its metadata catalog gives per-file SPDX CC-BY-4.0. Six exact fixture candidates and bug descriptions are in [DATA_SOURCES.md](../../DATA_SOURCES.md). The bytes have not been fetched, so catalog provenance is not yet a test-result claim.

## Terms and redistribution decision

- The HUST Mendeley v2 record declares [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en), which requires attribution, license link, and change indication for sharing/adaptation. The authoritative record/API carries a generic notice that additional permission may be necessary for content identified as third-party. The archive contains no per-file rights/attribution manifest. Dataset-level license evidence is recorded, but no claim is made that every embedded item is free of third-party restrictions. Keep raw bytes outside Git and do not redistribute them until any applicable third-party rights are clarified.
- Aurora Zenodo v1 declares CC BY 4.0. Attribute record creators, cite/version the artifact, include the license and modifications. Do not treat per-cell rated-capacity metadata as measured data or make broader rights claims than the record license.
- The fixture catalog declares each listed item CC-BY-4.0. Preserve source citations and metadata if later retrieved; do not commit the large files without a separate storage choice.
- Paper/article licenses do not replace the dataset record licenses. No rights are inferred from public accessibility.

## Consequences and evidence

Keep exact source records pinned, retrieve immutable source artifacts outside Git, and retain locally computed SHA-256 plus provenance/attribution metadata. Do not claim model-data comparability or SOH target support merely because both records are openly licensed or use a BDF-labeled format.

Direct artifact identities, source checksums, exact Aurora chemistry IDs/schema, selected fixture classes, and limitations appear in [ARCH-01 evidence](../evidence/ARCH-01.md) and [DATA_SOURCES.md](../../DATA_SOURCES.md). No production ingestion is authorized by this ADR.
