#!/usr/bin/env python3
"""Audit the formal release without changing manuscript or evidence files.

The audit checks four independent contracts:

* every file hash/size recorded in PACKAGE_MANIFEST.json;
* duplicate manuscript/source copies and canonical PDF page counts;
* page-count statements in the authority and summary records;
* a clean five-pass LaTeX rebuild of the two source documents, including
  extracted-text equality against the bundled canonical PDFs.

The final check is deliberately run in a temporary directory.  It does not
rewrite the release tree.  The report is deterministic apart from the
optional compiler diagnostics and is intended to be run before packaging.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "formal_release_consistency_report.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


def pdf_pages(path: Path) -> int | None:
    p = run(["pdfinfo", str(path)])
    if p.returncode:
        return None
    m = re.search(r"^Pages:\s*(\d+)\s*$", p.stdout, re.M)
    return int(m.group(1)) if m else None


def pdf_text(path: Path) -> str | None:
    p = run(["pdftotext", "-layout", str(path), "-"])
    return p.stdout if p.returncode == 0 else None


def compile_clean(src: Path, outdir: Path) -> dict[str, Any]:
    work = outdir / "latex"
    work.mkdir(parents=True, exist_ok=True)
    for name in ("nature_main_en.tex", "supplementary_information.tex"):
        shutil.copy2(src / name, work / name)
    shutil.copytree(src / "figures", work / "figures")
    result: dict[str, Any] = {"commands": [], "returncodes": {}}
    for stem in ("nature_main_en", "supplementary_information"):
        logs: list[str] = []
        for _ in range(5):
            p = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                     f"{stem}.tex"], cwd=work)
            result["commands"].append(["pdflatex", stem])
            result["returncodes"][stem] = p.returncode
            logs.append(p.stdout[-1000:])
            if p.returncode:
                break
        result.setdefault("tail", {})[stem] = logs[-1] if logs else ""
        pdf = work / f"{stem}.pdf"
        result.setdefault("pdf", {})[stem] = {
            "exists": pdf.exists(),
            "pages": pdf_pages(pdf) if pdf.exists() else None,
            "sha256": sha256(pdf) if pdf.exists() else None,
            "text_sha256": hashlib.sha256((pdf_text(pdf) or "").encode()).hexdigest()
            if pdf.exists() else None,
        }
    return result


def main() -> int:
    manifest_path = ROOT / "PACKAGE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_errors: list[dict[str, Any]] = []
    for entry in manifest.get("files", []):
        path = ROOT / entry["path"]
        if not path.exists():
            manifest_errors.append({"type": "missing", "path": entry["path"]})
            continue
        got = {"bytes": path.stat().st_size, "sha256": sha256(path)}
        want = {"bytes": entry.get("bytes"), "sha256": entry.get("sha256")}
        if got != want:
            manifest_errors.append({"type": "hash_or_size_mismatch",
                                    "path": entry["path"], "expected": want,
                                    "actual": got})

    pdf_paths = {
        "main": ROOT / "manuscript/nature_main_en.pdf",
        "supplement": ROOT / "manuscript/supplementary_information.pdf",
        "cover": ROOT / "manuscript/NATURE_COVER_LETTER_FINAL_EN.pdf",
    }
    pdf_info: dict[str, Any] = {}
    for name, path in pdf_paths.items():
        pdf_info[name] = {"path": str(path.relative_to(ROOT)),
                          "exists": path.exists(),
                          "pages": pdf_pages(path) if path.exists() else None,
                          "bytes": path.stat().st_size if path.exists() else None,
                          "sha256": sha256(path) if path.exists() else None}

    duplicate_groups = [
        ["nature_main_en.tex", "manuscript/nature_main_en.tex", "submission/nature_main_en.tex"],
        ["supplementary_information.tex", "manuscript/supplementary_information.tex",
         "submission/supplementary_information.tex"],
        ["manuscript/nature_main_en.pdf", "submission/nature_main_en.pdf", "nature_main_en.pdf"],
        ["manuscript/supplementary_information.pdf", "submission/supplementary_information.pdf",
         "supplementary_information.pdf"],
        ["manuscript/NATURE_COVER_LETTER_FINAL_EN.pdf", "submission/NATURE_COVER_LETTER_FINAL_EN.pdf"],
    ]
    duplicates: list[dict[str, Any]] = []
    for group in duplicate_groups:
        items = [{"path": p, "exists": (ROOT / p).exists(),
                  "sha256": sha256(ROOT / p) if (ROOT / p).exists() else None}
                 for p in group]
        hashes = {x["sha256"] for x in items if x["exists"]}
        duplicates.append({"paths": items,
                           "all_equal": len(hashes) == 1 and len(items) == len(group)})

    claims: dict[str, Any] = {}
    authority = (ROOT / "CURRENT_AUTHORITY.md").read_text(encoding="utf-8")
    summary = (ROOT / "FINAL_RELEASE_SUMMARY_CN.md").read_text(encoding="utf-8")
    claims["authority_mentions_stale_pages"] = bool(re.search(r"11-page.*57-page|12-page.*62-page|正文\s*12\s*页", authority))
    claims["summary_mentions_stale_pages"] = bool(re.search(r"正文\s*12\s*页.*(?:58|62)\s*页", summary))
    claims["actual_main_pages"] = pdf_info["main"]["pages"]
    claims["actual_supplement_pages"] = pdf_info["supplement"]["pages"]

    with tempfile.TemporaryDirectory(prefix="formal_release_audit_") as td:
        build = compile_clean(ROOT, Path(td))
        built = build.get("pdf", {})
        for name, key in (("main", "nature_main_en"), ("supplement", "supplementary_information")):
            canonical = pdf_paths[name]
            can_text = pdf_text(canonical) if canonical.exists() else None
            build.setdefault("pdf", {}).setdefault(key, {})["text_equal_to_canonical"] = (
                can_text is not None and can_text == pdf_text(Path(td) / "latex" / f"{key}.pdf")
            ) if (Path(td) / "latex" / f"{key}.pdf").exists() else False

    report = {
        "release_root": str(ROOT),
        "release_id": manifest.get("release_id"),
        "manifest": {"entry_count": len(manifest.get("files", [])),
                     "errors": manifest_errors},
        "canonical_pdfs": pdf_info,
        "duplicate_copy_checks": duplicates,
        "page_claim_checks": claims,
        "clean_rebuild": build,
        "status": "PASS" if (
            not manifest_errors
            and all(d["all_equal"] for d in duplicates)
            and claims["actual_main_pages"] == 11
            and claims["actual_supplement_pages"] == 68
            and not claims["authority_mentions_stale_pages"]
            and all(build.get("returncodes", {}).get(k) == 0 for k in ("nature_main_en", "supplementary_information"))
            and build.get("pdf", {}).get("nature_main_en", {}).get("text_equal_to_canonical")
            and build.get("pdf", {}).get("supplementary_information", {}).get("text_equal_to_canonical")
        ) else "FAIL",
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(OUT),
                      "manifest_errors": len(manifest_errors),
                      "main_pages": pdf_info["main"]["pages"],
                      "supplement_pages": pdf_info["supplement"]["pages"],
                      "clean_rebuild_main_pages": build.get("pdf", {}).get("nature_main_en", {}).get("pages"),
                      "clean_rebuild_supplement_pages": build.get("pdf", {}).get("supplementary_information", {}).get("pages")},
                     ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

