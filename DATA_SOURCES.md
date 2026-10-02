# Data Sources

No dataset bytes are committed unless redistribution rights are explicitly verified.

## V1 candidates

### HUST personalized discharge dataset

Role: primary supervised-ML source candidate.

Research expectation to verify directly in ARCH-00:
- LFP/graphite cells;
- heterogeneous discharge protocols;
- explicit open license;
- enough cycle/capacity information for SOH target construction.

### Empa Aurora battery dataset

Role: standards-aligned second source and cross-source/domain-shift stress evaluation candidate.

Research expectation to verify directly in ARCH-00:
- BDF-compatible exports;
- rich metadata;
- multiple chemistries / materially different domain;
- compatible capacity/SOH information.

### BDA / SINTEF / DLR robustness fixtures

Role: parser, validation, and robustness tests across cycler formats and known-bad examples.

Only files with explicit compatible licensing may be stored as repository fixtures.

## Source registration requirements

Each registered artifact must record:

- source_name
- source_uri
- source_version
- retrieved_at
- license_or_terms
- sha256
- byte_size
- adapter_name
- adapter_version

## ARCH-00 exit condition

This document is frozen only after exact source records/files, license terms, target availability, field mappings, and redistribution policy are directly verified and recorded with citations/links.
