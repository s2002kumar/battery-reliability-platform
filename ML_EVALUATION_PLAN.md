# ML Evaluation Plan — V1 Gate

## Primary task

Capacity-based state-of-health (SOH) estimation.

Conceptually:

`SOH(t) = available_discharge_capacity(t) / reference_capacity(cell)`

The exact rule for `reference_capacity` is not frozen. ARCH-00 must inspect source protocols and choose a deterministic, physically defensible rule that prevents target leakage.

## Evaluation hierarchy

1. Development diagnostics may inspect within-cell behavior.
2. Primary train/validation/test partitions must be grouped by physical cell identity.
3. A separate cross-source/domain-shift stress evaluation is required.
4. Cross-chemistry evaluation is optional unless source compatibility makes it meaningful.

## V1 model ladder

- naive/reference baseline;
- Ridge or ElasticNet;
- boosted-tree model;
- uncertainty-aware method (for example GPR) only if computationally appropriate.

Deep learning is explicitly deferred until baselines, data volume, and failure analysis justify it.

## Required evidence

- split manifest containing stable IDs only;
- deterministic random seed/config;
- target construction version;
- feature-set version;
- MAE/RMSE and suitable error summaries;
- per-source/per-condition error analysis where metadata allows;
- cross-source results reported separately from in-domain results;
- uncertainty/calibration evidence if an uncertainty-aware model is used;
- explicit leakage audit.
