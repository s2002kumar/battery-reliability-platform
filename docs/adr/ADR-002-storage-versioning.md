# ADR-002: Immutable Raw Storage and Analytical Versioning

- **Status:** Proposed for architecture review; implementation deferred
- **Date:** 2026-10-06
- **Scope:** V1 persistence and deterministic replay lineage

## Context

V1 requires immutable source bytes, provenance, deterministic replay, idempotence, and reproducible targets/features. The selected HUST and Aurora archives are respectively 1.19 GB and 2.51 GB. They were downloaded and inspected outside Git; no source bytes are in the repository. The candidate SINTEF/DLR fixture files range from about 3 MB to 63 MB.

## Decision

1. Keep every retrieved artifact immutable and address it by source record/version, exact file key, locally computed SHA-256, and byte size.
2. Keep a manifest adjacent to each stored artifact with source URI/version, retrieval time UTC, exact file key, hash, size, parser/adapter version, and explicit license/attribution/usage notes.
3. Store canonical and curated output as Parquet with explicit schema/version and deterministic partition/manifest rules. Rebuild derived data from immutable raw artifacts.
4. Version target/features by source manifest, code, schema/ontology snapshot, and configuration; reruns of the same logical inputs must be idempotent.
5. Keep full datasets outside Git. Any future fixture-in-Git choice needs verified per-file rights, attribution, and a separate size/storage decision.
6. Do not add Delta or table transaction machinery without a demonstrated concurrency, mutation, or time-travel requirement. S3 remains a later deployment profile, not an implementation approval here.

## Consequences and evidence

The exact archive sizes/checksums support keeping source files outside Git. Manifests plus deterministic Parquet outputs provide a minimal architecture boundary for replay without new runtime infrastructure. The BDF datastore is a reference, not an approval to copy its storage layout. No directory layout, cloud storage, or pipeline implementation is frozen by this ADR.

- [HUST Mendeley v2 artifact](https://data.mendeley.com/datasets/nsc7hnsg4s/2): local SHA-256 recorded in [ARCH-01 evidence](../evidence/ARCH-01.md).
- [Aurora Zenodo v1 artifact](https://zenodo.org/records/15481956): archive MD5 matches record; local SHA-256 recorded in [ARCH-01 evidence](../evidence/ARCH-01.md).
- [BDA/SINTEF/DLR fixture catalog](https://zenodo.org/records/21337233): catalog provides exact file sizes/MD5 and per-file licenses; candidate fixture bytes remain unfetched.

This storage/versioning direction is for review. It does not unblock ARCH-00 or ARCH-01 and does not authorize ingestion.
