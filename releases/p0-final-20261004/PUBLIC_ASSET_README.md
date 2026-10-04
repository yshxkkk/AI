# Public v8 release asset: no-raw-data variant

This archive is the public, no-raw-data variant of the frozen v8 submission package. It preserves code, manuscript material, aggregate audit evidence, derived result summaries, and release metadata needed to inspect the claims. It excludes source observations and source-like event tables or subject-level provenance, including raw VIIRS/FIRMS samples, raw EEG arrays, selector raw tables and split indices, Kepler raw/row-level pilot tables, LHC event feature archives, compressed event feature tables, per-observation source metadata, Solar event-provenance and row-index sidecars, STEAD holdout assignment rows, storm/event indices, and all NumPy binary state files.

The original frozen v8 archive remains a private working artifact because the explicit publication authorization also prohibits uploading raw data. This variant is the asset eligible for public distribution. Derived prediction tables are retained only where they are outputs of the released analyses rather than source observations; they are not a substitute for the excluded raw inputs.

The package manifest was rebuilt after these exclusions. Run `release_audit/check_formal_release.py` and `release_audit/verify_claim_ledger.py` from `p0_release` to verify release structure and claim-ledger consistency.
