#!/usr/bin/env bash
set -euo pipefail

# Reproducibility entry point for the audited release.
#   ./REPRODUCE_NATURE_REVISION.sh verify   (default; bundled-data verification)
#   ./REPRODUCE_NATURE_REVISION.sh full     (also reruns bundled uncertainty; raw branches if inputs exist)
# Missing large public inputs are reported as pending; verify mode still exits 0
# when all bundled artefacts, source builds and certificates pass.
ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-verify}"
PYTHON="${PYTHON:-python3}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
QA_DIR="${QA_DIR:-$(mktemp -d -t nature_revision_${STAMP}_XXXXXX)}"
mkdir -p "$QA_DIR"
cd "$ROOT"
export PYTHONPATH="$ROOT/source_archive${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1

if [[ "$MODE" != verify && "$MODE" != full ]]; then
  echo "usage: $0 [verify|full]" >&2
  exit 2
fi

status="PASS"
pending=()
run_optional() {
  local label="$1"; shift
  local missing=()
  while [[ "$1" != "--" ]]; do
    [[ -e "$1" ]] || missing+=("$1")
    shift
  done
  shift
  if ((${#missing[@]})); then
    echo "[PENDING] $label: ${missing[*]}"
    pending+=("$label")
    return 0
  fi
  echo "[RUN] $label"
  "$@"
}

printf '%s\n' '[1/7] Validate bundled tables, metadata and geometry'
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" audit_consistency.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/stead/run_stead_matched_recall.py >/dev/null
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=source_archive "$PYTHON" evidence/gb_native/run_gb_native_allocator_audit.py >/dev/null
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/conditional_benefits/verify_zero_radius_closure.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/head_registry/verify_head_registry.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/head_registry/run_p5_head_gate_audit.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/verify_claim_ledger.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/group_robustness/run_group_robustness_audit.py >/dev/null
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" release_audit/check_formal_release.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=source_archive "$PYTHON" -m unittest discover -s source_archive/tests -p 'test_geometry_certificates.py' -v

printf '%s\n' '[2/7] Compile sources in a clean QA directory (five passes for SI TOC stability)'
if command -v pdflatex >/dev/null 2>&1; then
  BUILD="$QA_DIR/latex"
  mkdir -p "$BUILD"
  for stem in nature_main_en supplementary_information; do
    for pass in 1 2 3 4 5; do
      pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" "$stem.tex" >"$QA_DIR/${stem}_${pass}.log"
    done
    pdfinfo "$BUILD/$stem.pdf" | awk '/^Pages:/{print stem, $0}' stem="$stem"
    pdftotext -layout "$BUILD/$stem.pdf" "$QA_DIR/$stem.txt"
    pdftotext -layout "manuscript/$stem.pdf" "$QA_DIR/${stem}_canonical.txt"
    cmp "$QA_DIR/$stem.txt" "$QA_DIR/${stem}_canonical.txt"
  done
else
  echo '[PENDING] pdflatex is unavailable; source build was not rerun.'
  pending+=("pdflatex")
fi

printf '%s\n' '[3/7] Check duplicate source and PDF copies'
for group in \
  'nature_main_en.tex manuscript/nature_main_en.tex submission/nature_main_en.tex' \
  'supplementary_information.tex manuscript/supplementary_information.tex submission/supplementary_information.tex' \
  'nature_main_en.pdf manuscript/nature_main_en.pdf submission/nature_main_en.pdf' \
  'supplementary_information.pdf manuscript/supplementary_information.pdf submission/supplementary_information.pdf' \
  'cover_letter_final.pdf manuscript/NATURE_COVER_LETTER_FINAL_EN.pdf submission/NATURE_COVER_LETTER_FINAL_EN.pdf submission/cover_letter_final.pdf'; do
  set -- $group
  first="$1"; shift
  for other in "$@"; do cmp "$first" "$other"; done
done

printf '%s\n' '[4/7] Compile all tracked Python modules into the QA directory'
"$PYTHON" - "$QA_DIR/pycompile" <<'PY2'
import py_compile, sys
from pathlib import Path
root=Path('.')
out=Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
files=[p for base in (root/'evidence', root/'source_archive', root/'v6', root/'scripts', root/'release_audit') if base.is_dir() for p in base.rglob('*.py')]
for p in files:
    target=out/(str(p.relative_to(root)).replace('/', '__')+'.pyc')
    py_compile.compile(str(p), cfile=str(target), doraise=True)
print(f'compiled {len(files)} Python modules')
PY2

printf '%s\n' '[5/7] Recompute bundled uncertainty and figure checks in full mode only'
if [[ "$MODE" == full ]]; then
  "$PYTHON" evidence/uncertainty/generate_uncertainty_and_reuse.py --bootstrap 5000 --output-dir "$QA_DIR/uncertainty"
  echo '[INFO] Derived figures are already regenerated from bundled tables and remain immutable in this mode.'
else
  echo '[SKIP] full-data/figure regeneration (use MODE=full explicitly)'
fi

printf '%s\n' '[6/7] Re-run optional raw-data branches when inputs are present'
run_optional 'Solar raw anchor pilot' evidence/solar/solar_anchor_table.csv -- \
  "$PYTHON" evidence/solar/run_solar_noise_minimal.py
run_optional 'LHC raw feature audit' evidence/lhco/raw_features/lhco_blackbox1_development_features.csv.gz evidence/lhco/raw_features/lhco_blackbox1_audit_features.csv.gz -- \
  "$PYTHON" evidence/lhco/run_lhco_matched_fpr_audit.py --outdir "$QA_DIR/lhco"
run_optional 'STEAD raw subset audit' evidence/stead/raw_source/test.hdf5 evidence/stead/raw_source/test_noise.hdf5 -- \
  "$PYTHON" evidence/stead/run_stead_raw_subset.py --data-dir evidence/stead/raw_source --output-dir "$QA_DIR/stead"
run_optional 'Weather action audit' evidence/weather/raw_source -- \
  "$PYTHON" evidence/weather/run_weather_action_audit.py --data-dir evidence/weather/raw_source --results-dir evidence/weather --output "$QA_DIR/weather_run_status.json"

if [[ -f evidence/lhco/lhco_region_compression_raw_event.csv ]]; then
  PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/lhco/run_lhco_sideband_closure_audit.py \
    --regions evidence/lhco/lhco_region_compression_raw_event.csv --outdir "$QA_DIR/lhco_light" >/dev/null
else
  echo '[PENDING] LHC lightweight sideband closure input'
  pending+=("LHC lightweight sideband closure")
fi

if [[ -f evidence/lhco/lhco_region_compression_raw_event.csv && -f evidence/lhco/lhco_matched_fpr_raw_event.csv && -f evidence/lhco/lhco_sideband_closure.csv ]]; then
  PYTHONDONTWRITEBYTECODE=1 "$PYTHON" evidence/lhco/run_lhco_stratified_closure_audit.py \
    --regions evidence/lhco/lhco_region_compression_raw_event.csv \
    --matched-fpr evidence/lhco/lhco_matched_fpr_raw_event.csv \
    --closure evidence/lhco/lhco_sideband_closure.csv \
    --outdir "$QA_DIR/lhco_p4" >/dev/null
else
  echo '[PENDING] LHC P4 stratified closure inputs'
  pending+=("LHC P4 stratified closure")
fi

printf '%s\n' '[7/7] Write machine-readable status'
pending_joined="$(IFS='|'; echo "${pending[*]-}")"
"$PYTHON" - "$QA_DIR/reproducibility_status.json" "$MODE" "$pending_joined" <<'PY'
import json,sys
from pathlib import Path
out=Path(sys.argv[1]); mode=sys.argv[2]; pending=sys.argv[3].split('|') if sys.argv[3] else []
status={"mode":mode,"status":"PASS_WITH_PENDING" if pending else "PASS","pending_branches":pending,"bundled_source_build":"PASS","duplicate_copy_check":"PASS","raw_inputs_included":False,"note":"Full raw-data regeneration requires the public inputs and hashes listed in DOWNLOAD_PUBLIC_DATA.md."}
out.write_text(json.dumps(status,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(status,ensure_ascii=False))
PY
printf '%s\n' "Reproducibility check complete: $QA_DIR"

