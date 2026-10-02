# ADR-002: Immutable Raw Storage and Analytical Versioning

- **Status:** Proposed for architecture review; implementation deferred
- **Date:** 2026-10-02
- **Scope:** V1 data persistence and replay lineage

## Context

The product requires immutable source bytes, provenance, deterministic replay, idempotence, and reproducible features. Candidate datasets include multi-gigabyte archives. No source bytes are currently present in the repository.

## Decision

1. Keep each retrieved source artifact immutable and address it by source record/version plus exact file key and SHA-256. Never rewrite or normalize raw bytes in place.
2. Store a manifest beside raw artifacts with source URI, source version, retrieval timestamp, exact file name, SHA-256, byte size, adapter/version, and explicit license/attribution/usage notes.
3. Write canonical and curated outputs as Parquet with explicit schema/version and deterministic partition/manifest rules. Rebuild derived data from immutable raw artifacts.
4. Version feature and target outputs by source manifest, code version, schema/ontology snapshot, and configuration. A rerun of the same logical inputs must be idempotent.
5. Do not adopt Delta/table transaction machinery until a concrete concurrency, mutation, or time-travel requirement is demonstrated. Local Parquet plus immutable manifests is the V1 default.
6. Keep datasets outside Git by default. Any future small fixture commit requires verified redistribution terms, attribution, and a deliberate size/storage decision.

## Consequences

This direction supports replay and lineage without adding infrastructure dependencies. It places responsibility on manifests and deterministic writers for snapshot identity. Object-store/S3 behavior remains a later deployment profile; this ADR does not approve cloud implementation.

## Evidence and limits

- [PROJECT_SPEC.md](../../PROJECT_SPEC.md) and [ARCHITECTURE.md](../../ARCHITECTURE.md) already establish immutable raw, replay, Parquet, and deferred S3 direction.
- [BDF datastore conventions](https://github.com/battery-data-alliance/bdf-datastore) distinguish raw and processed files and companion metadata.
- The reviewed Aurora archive is 2,507,129,091 bytes; the fixture collection contains files from 22.6 kB through 258 MB. This supports keeping full public data out of Git but does not itself choose a local storage location.

This ADR freezes only storage/versioning direction. Directory layout, cloud storage, and pipeline implementation remain deferred.
