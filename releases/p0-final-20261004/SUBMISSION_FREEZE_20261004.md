# Final submission freeze (2026-10-04)

The targeted closure work is complete and no further experiments are promoted in this release.

## LHC downstream-fit decision

The official BlackBox1 HDF5 and masterkey are present and the fresh 600k/100k/300k candidate-object audit is complete. The current account does not contain an official downstream physics likelihood or shape-fit workflow, detector-response/pileup/smearing calibration, a background-only pseudo-experiment ensemble, a validated look-elsewhere distribution, or fit/analyst timing. Existing sideband closure, derived-feature systematics and screening proxies remain audit evidence only. The manuscript therefore retains the fixed-risk candidate-object endpoint and explicitly does not claim a downstream physics-fit or analyst-time benefit.

## Frozen scientific scope

- Canonical head: `RegionNativeProbabilityModel`.
- Main routes: `P0-canonical-local-all` and `P0-LOCO-PPC-selective-residual`.
- `GB-Logistic-H` and `GB-Logistic-S` remain SI-only historical controls.
- Claim ledger: 21 claims; no universal accuracy, robustness, cost, speed, human-workload, external Solar transport or lossless-workload claim.
- New experiments are stopped after the LHC closure, Solar action-unit bootstrap and LOCO exact-parity dispatch audit.

## Repository and DOI state

The public target repository `https://github.com/yshxkkk/AI` is write-accessible and its review branch snapshot is recorded in `evidence/github/GITHUB_RELEASE_HANDOFF_CN.md`. The complete local release package is the authoritative artifact; the remote branch is a review subset rather than a byte-complete mirror. A DOI has not been minted. Repository deposit, archival DOI minting and the final editorial upload are external publication steps and are not fabricated in this release.

The canonical PDFs, cover letter, claim ledger, manifest, hashes and reproducibility records are frozen locally. Any later manuscript change must increment the release revision and rerun the clean build, visual QA and formal release audit.
