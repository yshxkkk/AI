# Frozen claim ledger — From Point Scores to Certified Regional Probabilities v1

**Release:** `from-point-scores-to-certified-regional-probabilities-v1.2026-10-02`  
**Status:** frozen for the current submission package  
**Purpose:** this ledger is the authority for what the manuscript claims, what evidence supports each statement, and where the statement must stop. It is a release-control document, not an additional scientific result.

## Claim levels

| Level | Meaning | Permitted wording | Prohibited extrapolation |
|---|---|---|---|
| T1 — formal | Algebraic or theorem result under stated assumptions | “equals”, “recovers”, or “is bounded under the stated assumptions” | Distribution-free, assumption-free or external-data guarantee |
| T2 — measured audit | Replayed data or real downstream call with a declared split and denominator | “in this audit”, “on this held-out role”, or “for this subsample” | Universal accuracy, robustness, cost or operational utility |
| T3 — descriptive/model-assisted | Synthetic, historical, single-seed or model-assisted diagnostic | “conditional signal”, “descriptive diagnostic” or “protocol evidence” | Confirmatory external validation or theorem coverage |
| T4 — protocol-only | Specified but not completed with the required independent data or labels | “protocol retained”, “pending”, or “not claimed” | Any numerical empirical conclusion |
| T5 — rejected/superseded | Failed gate, obsolete branch or exploratory result | “failure boundary” or “superseded audit” | Reusing the result as a headline gain |

## Headline claims frozen in v1

| ID | Frozen statement | Level | Evidence anchor | Boundary that must be retained |
|---|---|---|---|---|
| C01 | A regional probability object binds an estimand to effective support, Granular Ball geometry, uncertainty, refinement, action state and failure state; Granular Ball is the auditable geometric implementation of the statistical abstraction. | T1/interface definition | `nature_main_en.tex` Introduction/Discussion; `evidence/head_registry/` | This is not a new probability axiom and does not claim that every individual field is unique to this work. |
| C02 | The runtime protocol is object → certificate → conditional reuse/compression/stability → refine, re-certify, point fallback or abstain. | T1/protocol | Main text operating chain; SI implementation contract | Reuse, compression and stability are conditional properties, not universal consequences of forming regions. |
| C03 | Under singleton/identity allocation, (r=0) restores point Logistic prediction, objective, calibration, decision, certificate state and fallback semantics. | T1/formal | SI zero-radius theorem; `evidence/conditional_benefits/verify_zero_radius_closure.py` | A multi-point cell labelled with numerical radius zero is not sufficient; zero local coefficients alone give only point-surface/objective closure. |
| C04 | The certificate-sufficiency bound is finite-sample and selective only under independent validation, frozen finite menus, support, homogeneity, boundary, transport and deployment-measure assumptions. | T1/conditional theorem | SI theorem; `evidence/theorem_coverage/` | The known-law grid is a proof-contract audit, not distribution-free or external coverage. |
| C05 | GB-Logistic-S is the canonical computational head; GB-Logistic-H is the hard support/boundary/audit/fallback control; point Logistic is the strict nested baseline. | T1/interface + T2 release status | `evidence/head_registry/HEAD_REGISTRY.{json,csv}` | Head status is not a model leaderboard and does not imply pointwise dominance. |
| C06 | GB-Logistic-S is clean-data non-inferior to point Logistic in the declared synthetic/model-assisted screen and has a conditional moderate-perturbation stability signal. | T3 | `evidence/conditional_benefits/gblogistic_s_perturbation_stress_*` | This is not a Solar/STEAD external confirmation, theorem coverage or universal robustness claim. |
| C07 | Boundary crossing or large perturbation triggers assignment invalidation and point fallback in the declared S stress audit. | T2/T3 | S perturbation stress certificates and fallback records | The trigger is valid only for the declared representation, metric, perturbation and gate. |
| C08 | Solar 2010–2018 is a historical model/evaluation audit. The regional action route is retained as an explicit rejection/fallback boundary because the passed-subset action risk is not lower than its matched point risk. | T2 | `evidence/solar/`; `evidence/conditional_benefits/solar_conditional_benefit_*` | The 2019–2024 raw-FITS/GOES/HEK endpoint is protocol-only; no external Solar transport metric is claimed. |
| C09 | STEAD real PhaseNet calls document a 64.8% fixed-threshold input reduction on the checksum-verified 12,000-window subsample, while matched-recall analysis shows no universal call saving and regional proper scores are worse in that split. | T2 | `evidence/stead/stead_phasenet_wallclock_receipt.json`; STEAD audit tables | The count is a coverage–call trade-off, not operational warning utility, full-release accuracy or matched-recall superiority. |
| C10 | LHC regional candidate objects can be fewer while assigned-event burden is higher; no uniform matched-operating-point saving is claimed. | T2 | `evidence/lhco/` raw-event audit | Candidate counts are not downstream fit time, analyst time or discovery-level significance. |
| C11 | The head registry demonstrates a common extensibility and fail-closed interface; PP, Beta–Binomial-S, cloglog/Hazard-S and Dirichlet-S are not promoted as additional headline accuracy results in v1. | T2/T3 | `evidence/head_registry/`; `evidence/next_upgrade/probability_heads/` | No fourth head enters the main text without all promotion gates, independent validation and a zero-radius/interface check. |
| C12 | The release is reproducible at the level of supplied tables, scripts, manifests and declared public-input branches. | T2/release | `REPRODUCE_NATURE_REVISION.sh`; release audit reports | Missing raw branches remain pending and are never interpreted as zero results or completed external validation. |
| C13 | The GB-native recursive allocator provides an end-to-end Granular Ball identity audit: on the fixed synthetic screen, GB-native-S gives Brier 0.19740 versus 0.19829 for point Logistic (mean change −0.00089); under 20% structure-label flipping only 1.5% of queries pass and 98.5% return to point Logistic. | T3 | `evidence/gb_native/gb_native_allocator_{metrics,summary,meta}.*` | This is a fixed synthetic allocator/failure-boundary audit; it is not external transport, a universal native-allocator advantage or a new headline accuracy claim. |
| C14 | Grouped robustness is auditable only at the declared unit: STEAD station-hash bootstrap reports higher regional proper scores and positive assigned-trace burden; EEG subject bootstrap reports heterogeneous coverage; Solar HARPNUM exports provide support/action counts but no row-level group-risk interval. | T2/T3 | `evidence/group_robustness/group_robustness_summary.csv`; `group_robustness_domain_status.csv` | These are descriptive grouped audits. They do not establish universal group robustness, clinical validity, Solar transport validity or matched-recall resource savings. |
| C15 | The P5 release-integrity audit rechecks the frozen head registry, zero-radius semantic closure, released fallback encodings and boundary fail-closed records; no extension head is promoted by this audit. | T2/release audit | `evidence/head_registry/P5_HEAD_GATE_AUDIT_{SUMMARY,META}.json`; `evidence/head_registry/P5_HEAD_GATE_AUDIT_README_CN.md` | This is a deterministic consistency check over released records; it adds no precision, robustness, resource or external-validation result. |

## Frozen model list and promotion rule

The v1 computational list is fixed as follows:

1. **point Logistic** — strict singleton/identity zero-radius baseline and point fallback.
2. **GB-Logistic-H** — hard support, boundary, audit and fallback control; not the canonical row-level surface.
3. **GB-Logistic-S** — canonical strongly coupled head with a continuous point surface and gated local residual.
4. **GB-Logistic-PP**, **GB-Beta-Binomial-S**, **GB-cloglog/GB-Hazard-S** and **GB-Dirichlet-S** — registered extensions only; protocol/SI status in this release.

No new head or geometry branch may be promoted into a headline accuracy or efficiency statement unless it simultaneously satisfies: clean non-inferiority to the strongest point head; independent certified-subset gain or non-inferiority; no increase in false-pass; expected boundary-triggered fallback; measured incremental computation and assigned work; and exact zero-radius or zero-local-term closure. Any change to representation, centres, radii, metric, tie rule, local head, deployment measure or assignment fingerprint creates a new object version and invalidates prior certificates and reuse records.

## Claims explicitly frozen out of v1

- no universal regional accuracy gain, robustness gain, speed gain or energy saving;
- no constant-ball probability replacement for the point surface;
- no external 2019–2024 Solar transport validation;
- no claim that KMeans-backed regional allocations are a GB-native optimizer or dominate point gates;
- no claim that the fixed synthetic GB-native allocator universally dominates KMeans-backed or point allocations;
- no claim of particle discovery, solar-flare mechanism, clinical validity or operational earthquake-warning utility;
- no distribution-free pointwise or external coverage claim;
- no promotion of Weather, full STEAD, full LHC closure or additional head searches as completed evidence.

The main text, Supplementary Information, cover letter and reporting summary must use the frozen statements above. Historical exploratory files remain available only as explicitly labelled audit evidence and cannot alter the v1 headline claims without a new release identifier.

