# Project Status

## Current milestone

**Architecture/Data Gate**

## Current task

**ARCH-00 — dataset inspection and architecture freeze**

## Product state

- Project direction: LOCKED
- V1 product boundary: LOCKED
- ML required in V1: YES
- Coding implementation: NOT STARTED
- Resume claims approved: NONE

## Current blockers

ARCH-00 must verify directly:
1. exact HUST source files/schema/license/redistribution terms;
2. exact Empa source files/schema/license/redistribution terms;
3. fixture licenses and known-bad cases;
4. BDF field mapping;
5. source-compatible SOH target availability;
6. deterministic reference-capacity rule;
7. cross-source evaluation compatibility.

## Last decision

Do not implement production code before ARCH-00 exits successfully.

## Update protocol

Every completed task must append:
- task ID;
- date;
- commit/PR;
- tests run;
- evidence path;
- known limitations;
- newly unblocked task(s).
