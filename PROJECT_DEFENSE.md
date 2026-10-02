# PROJECT_DEFENSE

Interview-defense document. Expand only from implemented behavior and verified evidence.

## Questions V1 must eventually answer

- Why is this a data platform rather than a battery-prediction notebook?
- What does BDF standardize and what remains project-specific?
- How is immutable raw data represented?
- How does idempotent ingestion work?
- What is quarantined versus rejected?
- How are cycles represented when sources disagree?
- What is the precise SOH target?
- Why is random cycle-row splitting invalid?
- How are features prevented from leaking target/future information?
- What happened during cross-source evaluation and why?
- How can any prediction be traced back to source artifacts and code/config versions?
- How are reruns/backfills performed?
- Why were Spark/Kafka/dbt/Kubernetes omitted from V1?
- What measured condition would justify each of them later?
- What remains imperfect?

## Debugging stories

Populate after real failures occur. Never invent debugging stories retroactively.
