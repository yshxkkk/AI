# Region-native v2 / P0 freeze claim ledger (2026-10-04)

This ledger is the release authority for the frozen regional-probability routes. The older `CLAIM_LEDGER_V1.*` files remain historical archives. H/S code remains available for reproducibility, but H/S are not canonical routes or headline claims.

## Unified auditable value chain and route roles

The release treats auditability, conditional stability, query workload and proper-score behavior as linked but separate endpoints of one regional probability contract; it does not claim universal joint dominance across these dimensions. The auditable value chain is:

`regional allocation -> regional probability/support/geometry -> heterogeneity/support/boundary certificate -> reuse, selective local refinement, borrow, abstain or fail-closed fallback -> query workload and downstream-action audit`.

The route roles are deliberately separated. `P0-canonical-local-all` is the fixed-topology accuracy and mechanism reference: it retains the complete local surface and makes zero query-time Point Logistic calls, but evaluates that local surface for every query row. `P0-LOCO-PPC-selective-residual` is a fixed-topology, scalar-first query-workload candidate: an independently gated residual surface is read only for eligible regions; the release does not claim dynamic query-time splitting or an end-to-end human-cost reduction. The Solar audit is a strict chronological/HARPNUM-disjoint temporal-transport failure boundary: all 12,659 outer-time anchors rejected regional cells and used the explicit Point Logistic fallback. STEAD and LHC provide task-specific object-compression and assigned-downstream-burden audits, including their coverage or burden trade-offs, rather than universal efficiency or robustness evidence.

**Contract invariant.** Under the same frozen allocation, frozen support records and unchanged certificate eligibility, the region identifier, recorded support and regional action eligibility are invariant to a query perturbation. The numerical local surface and row-level threshold actions are not required to be invariant. Boundary crossing, support loss or temporal-transport failure invalidates the reuse certificate and requires re-certification, refinement, borrowing, abstention or explicit Point Logistic fallback.

## Frozen route registry

| Route | Role | Release status | Evidence boundary |
|---|---|---|---|
| `RegionNativeProbabilityModel` | canonical positive-radius regional head | canonical | Regional probability, support, geometry, uncertainty and failure state; no universal accuracy/cost claim |
| `P0-canonical-local-all` | accuracy and mechanism reference | headline reference | Stored local surface, zero query-time Point Logistic calls; still evaluates a local surface per query row |
| `P0-LOCO-PPC-selective-residual` | scalar-first deployment candidate | conditional SI/deployment candidate | Scalar posterior by default; local residual only after independent gate; Digits remains below fixed-topology P0 |
| `P0-exact-residual-identity` | strict precision-lossless boundary | SI only | Algebraically identical to P0 but requires 100% local-surface evaluation |
| `P0-K32-UCB-microball` | workload--precision frontier | exploratory SI only | Surface reduction is measured; group-ESS, simultaneous, PPC and outer-time promotion gates remain incomplete |
| `point-logistic` | comparator and zero-radius closure | promoted control | Strict singleton/identity comparator; not a positive-radius requirement |

## H/S policy

`GB-Logistic-H` and `GB-Logistic-S` are **historical head ablations / legacy controls**. They are retained in the Supplementary Information and compatibility code only. They are absent from the canonical head, primary route list and main configuration; no independent H/S headline conclusion is claimed.

## Claims

| Claim | Evidence | Status | Boundary |
|---|---|---|---|
| A Granular Ball can be an estimand-bearing regional probability object with support, geometry, uncertainty, action and failure state. | `evidence/region_native/region_native_probability.py`; synthetic/Digits runners | Implemented and contract-audited | Fresh pure-Solar fit is not claimed because raw inputs are absent. |
| Frozen allocation and region-first query routing are path-consistent and fail closed. | region-native contract tests and provenance tables | Contract-audited | Intervals are conditional plug-in/model-assisted. |
| P0 canonical local-all is the highest-tested fixed-topology regional surface reference and is point-free at query time. | `evidence/next_upgrade/native_bayes_surface/precision_lossless/` | Headline reference | Local surface is still evaluated for each query row; zero point calls do not prove wall-clock or human savings. |
| LOCO--PPC selective residual gives a scalar-first deployment candidate. | `calibration/results_same_topology_hierarchical_20261004/` and PPC companion | Conditional deployment candidate | Synthetic is near P0; Digits remains below fixed-topology P0; full simultaneous/group-ESS/PPC/outer-time promotion gates remain required. |
| An early empirical-Bayes regional pilot had worse proper scores than the point comparator. | `evidence/region_native/pre_repair_20261003/region_native_metrics.csv`; `evidence/region_native/pre_repair_20261003/digits_region_native_metrics.csv` | Historical negative boundary | This applies only to that early pilot and must not be used to characterize the current P0 canonical local-all route, which is governed by the fixed-topology audit below. |
| P0 surface can conditionally outperform matched Point Logistic under the fixed-topology audit. | `evidence/next_upgrade/native_bayes_surface/precision_lossless/`; `evidence/next_upgrade/p0_direct_stress/`; six-seed P0 audit | Conditional mechanism evidence | The explanation is regional anchor detail filtering, local heterogeneity recovery and parent/global shrinkage; direct P0 stress supports conditional stability only; no universal superiority or noise-immunity claim. The separate `gblogistic_s_perturbation_stress_metrics.csv` table is a historical GB-Logistic-S compatibility-control stress audit. |
| Regional reuse may reduce selected object-level calls under a declared threshold. | regional cost audits | Conditional diagnostic | No matched-recall downstream saving is established. |
| H/S are useful only as reproducibility controls. | SI legacy-control section and historical compatibility evidence | SI-only legacy | No independent H/S accuracy, robustness or efficiency conclusion; historical S perturbation results are not promoted as P0 robustness evidence. |
| The Solar outer-time audit is a temporal-transport failure-boundary case. | Released SWAN--SF outer audit and Solar transport protocol | Completed fail-closed boundary / protocol-only raw-input extension | All 12,659 chronological/HARPNUM-disjoint anchors rejected regional cells and used the explicit Point Logistic fallback; 2019--2024 raw-FITS/SHARP and independent GOES/HEK inputs remain protocol-only, so no positive Solar external/deployment metric is claimed. The auxiliary M4 selective-risk probe is reported in the main text as a bounded exploratory endpoint; its complete grid remains in the SI. |
| A frozen Solar M4 route shows a conditional equal-action-budget selective-risk signal on the released outer test. | `evidence/next_upgrade/ball_surface_ablation/solar_m4_matched_risk_budget.csv` and paired HARPNUM bootstrap | Main-text conditional exploratory endpoint | Action units are HARPNUM x UTC day and budgets are fixed before test scoring; this is selective Brier at equal review budget, not matched-recall saving, human cost, total compute, 2019--2024 external transport or a canonical P0 promotion. The 50% budget is the representative point used in the main-text exposition; the full eight-point-by-two-horizon grid is retained for multiplicity-aware interpretation and is not a claim of simultaneous significance. An action-unit sensitivity audit compares persistent HARPNUM and daily HARPNUM x UTC-day estimands; the difference in risk magnitude and fallback fraction is itself an audit result, not a universal advantage. A HARPNUM-cluster bootstrap sensitivity leaves the persistent-unit contrasts below zero but places the 24-h daily upper endpoint at zero, so dependence-aware uncertainty is reported without promotion. |
| The regional contract links support, geometry, probability, certificate state, action state and failure state into one auditable query path. | `evidence/region_native/`; contract tests and provenance tables | Contract-audited | This is an operational/statistical-geometric auditability claim, not a semantic, causal or neuroscience explanation; the four performance dimensions are not claimed to improve jointly on every task. |
| Unified independent calibration role is executable for the P0 selective route. | `evidence/next_upgrade/native_bayes_surface/calibration/results_unified_20261004/` | Conditional calibration audit complete | Synthetic/Digits benchmark-group evidence; Solar HARPNUM ESS and external time-block PPC remain protocol-only. |
| LOCO--PPC query workload is auditable under frozen predictions. | `evidence/next_upgrade/native_bayes_surface/workload_audit/`, including `loco_true_query_timing_summary.csv` and `loco_scaling/` | Query-workload audit complete | Large-batch fixed-thread timing confirms 62.63%/75.97% surface fractions but the legacy route is slower than P0 by 21.4%/14.3%; an exact-parity Boolean-vector dispatch audit reduces legacy wall time by 28.65%/22.97% and is 15.15%/11.13% faster than P0 in the measured in-memory batches. Fit, file I/O, downstream calls, independent RSS and human review remain excluded, so no universal end-to-end saving is claimed. |

## Explicit non-claims

The release does not claim universal regional accuracy, speed, cost, energy, robustness, matched-recall saving, distribution-free/posterior-predictive coverage, external Solar transport validity, or absolute P0 losslessness under reduced surface evaluation. It does not claim that auditability, robustness, query workload and proper score jointly improve on every task.

The release also does not claim that H/S are current competing methods. They are historical controls only.

## New task endpoints and explicit promotion boundaries

- **LHC strict raw-HDF5 audit (`RN19`)**: all 64 regional fits, sidebands, region order and Point scores were frozen before masterkey access. At observed FPR cap 0.05, the regional prefix has lower observed FPR and 13,669 rather than 14,997 assigned events, with 3 selected whole regions after scoring all 64. The paired recall interval crosses zero; higher FPR caps favour Point. A separate development-calibrated protocol-repair replication freezes the cap before audit-label access and reduces assigned events from 15,104 to 13,669, but was run after inspection of the original audit and is not an independent confirmatory result. A fresh 600k/100k/300k role split gives 11,324 versus 15,363 assigned events, recall difference +0.14068 [+0.07806,+0.20240] and FPR difference -0.01360 [-0.01449,-0.01261]; it remains post-inspection and has no downstream fit timing. This is a conditional candidate-object/assigned-event proxy, not a downstream physics-fit or analyst-time result. The fresh role split also has descriptive cross-role sideband closure and derived-feature systematics-surrogate audits, but no detector-response package, calibrated null/look-elsewhere distribution or physics likelihood fit.
- **Kepler/KOI/TCE pilot (`RN20`)**: system-held-out pilot under a predeclared release protocol (no external registry timestamp claimed). At system recall 0.80, regional TCE call proxies increase 21.4% and Brier worsens by +0.01275 [0.00204, 0.02329]. It is an SI failure boundary; the call proxy is not measured human time and the quarter metadata does not provide unseen-time validation.
- **FIRMS/VIIRS feasibility (`RN21`)**: protocol and provenance only. Earthdata authentication, partial derived event coverage, missing independent perimeter labels and missing downstream timing block promotion. No positive wildfire claim is made.

## Latest targeted upgrade audits

- Canonical P0 direct stress preserves region IDs within the measured margin and triggers re-routing or fallback at boundary crossing; this is conditional stability evidence.
- The Solar M4 same-selector decomposition shows a local-surface calibration signal at the representative 50% budget, while the 16-endpoint simultaneous intervals cross zero.
- STEAD repeated PhaseNet timing, once complete, remains a negative matched-recall downstream boundary rather than a positive cost claim.

- **Solar action-unit sensitivity:** `evidence/next_upgrade/solar_action_unit_sensitivity/` provides an image-first comparison of persistent HARPNUM and daily HARPNUM x UTC-day estimands; both have full recall at the 50% prefix, but their selective-risk magnitudes and fallback fractions differ.
- **LOCO large-batch and dispatch audits:** `evidence/next_upgrade/native_bayes_surface/workload_audit/loco_scaling/` confirms stable surface-object reduction above 10^5 rows, exposes the legacy dispatch penalty, and records an exact-parity Boolean-vector engineering repair. The repair is SI-only and does not establish downstream or human-workload saving.
