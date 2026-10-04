# Formal release audit

**Release ID:** `region-native-probabilistic-inference-with-auditable-granular-balls-v2`

**Release tag:** `region-native-probabilistic-inference-with-auditable-granular-balls-v2.2026-10-03`

**Audit scope:** release-layer consistency, source/PDF binding, declaration metadata, manifest integrity, package hygiene and clean-build verification. This report does not promote a scientific result beyond the evidence and claims stated in the manuscript and Supplementary Information.

## Canonical package state

The v2 package changes the manuscript axis to **Region-native probabilistic inference with auditable Granular Balls**. Main-text tables and process diagrams are delivered as checked image assets (600-dpi PNG with vector PDF source), while captions and cross-references remain in LaTeX. A positive-radius Granular Ball is the statistical unit: a query is allocated once, reads or estimates its region probability, receives interval/support/boundary fields, and is routed to reuse, refinement, partial pooling, interval output or abstention. P0 canonical local-all is the accuracy/mechanism reference and LOCO--PPC selective residual is the conditional deployment candidate. The H and S point-nested routes are retained only as disabled-by-default SI legacy controls and compatibility code.

The current canonical PDFs are:

- `manuscript/nature_main_en.pdf`: 16 pages; SHA-256 `abaca2c153beae5944897ee7af9d21858cb016310227a765f8b61e33839a8adb`.
- `manuscript/supplementary_information.pdf`: 87 pages; SHA-256 `d68569b4a11f0931af5e00eb2977376aec6897d30e71544fe7f9c0592fcfa674`.
- `manuscript/NATURE_COVER_LETTER_FINAL_EN.pdf`: 2 pages; SHA-256 `3d6ca42c2d4e9c523d556f3da1201306b39fdfc392b2092a0479047608f4412b`.

The release manifest currently contains 1,831 entries; its detached SHA-256 is recorded in `PACKAGE_MANIFEST.sha256` and checked by `check_formal_release.py`. The page-count gate is read from `RELEASE_METADATA.json`, so a later editorial source change must update the metadata and rerun the clean build rather than silently accepting stale v1 counts.

## Scientific evidence boundary

The new implementation and result profile live under `evidence/region_native/`. The bundled synthetic and Digits audits demonstrate the model contract, certificates, perturbation routing and conditional object accounting; their current row-level proper scores remain worse than the point comparator. They therefore support a transparent failure boundary and an auditable coarse-to-fine protocol, not a universal accuracy, robustness or cost improvement. The strict Solar outer route remains a fail-closed temporal-transport boundary: its 2014--2018 regional cells are rejected and routed to Point, while 2019--2024 raw-FITS/GOES/HEK parity remains pending. A frozen M4 region-first route provides a narrow conditional equal-action-budget selective-risk probe on the historical outer block; it is reported in the main text and SI, but is not an external deployment or human-time claim. The strict raw LHC replay is a measured risk-capped candidate-object/assigned-event endpoint after label-after-freeze freezing; its recall interval crosses zero and it has no downstream physics-fit or analyst-time measurement. The Kepler/TCE pilot is an SI-only matched-recall failure boundary, and FIRMS is a blocked feasibility/provenance boundary.

## Recheck sequence

```bash
python3 release_audit/rebuild_manifest.py
python3 release_audit/check_formal_release.py
python3 audit_consistency.py
python3 evidence/region_native/audit_region_native_artifacts.py --root evidence/region_native
```

The generated `release_audit/FORMAL_RELEASE_AUDIT_RESULT.json` is a validator output and is intentionally excluded from `PACKAGE_MANIFEST.json`. Rerun the checker after any source, PDF, metadata or evidence change.
