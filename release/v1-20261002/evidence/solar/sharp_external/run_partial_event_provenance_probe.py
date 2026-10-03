#!/usr/bin/env python3
"""Fetch a tiny public GOES/HEK event sample for provenance-only auditing.

This script intentionally does not download HMI/SHARP FITS, reconstruct features,
or compute prediction metrics.  It records public source bytes, normalizes the
GOES and HEK event tables, and performs a time-nearest descriptive comparison.
The output status is always ``pending_raw_fits`` because event provenance alone
cannot satisfy the Solar transport audit contract.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

GOES_BASE = "https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/multi/l2/data/xrsf-l2-flrpt_science/csv"
HEK_BASE = "https://www.lmsal.com/hek/her"

def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "regional-probability-transport-audit/1.0"})
    with urlopen(req, timeout=90) as r:
        return r.read()

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def normalize_goes(raw: bytes, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    from io import BytesIO
    d = pd.read_csv(BytesIO(raw), comment="#")
    d["time"] = pd.to_datetime(d["time"], utc=True, errors="coerce")
    d = d[d["time"].between(start, end, inclusive="left")].copy()
    out = pd.DataFrame({
        "event_id": d["flare_id"].astype(str),
        "peak_time_utc": d["time"].dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "goes_class": d["flare_class"].astype(str).str.upper().str.replace(" ", "", regex=False),
        "noaa_ar": pd.to_numeric(d.get("active_region"), errors="coerce"),
        "source": "NOAA_NCEI_GOES_XRS_FLARE_REPORT",
        "source_url": GOES_BASE,
    })
    return out

def normalize_hek(raw: bytes, frm_name: str | None) -> pd.DataFrame:
    payload = json.loads(raw.decode("utf-8"))
    d = pd.DataFrame(payload.get("result", []))
    if frm_name is not None and "frm_name" in d:
        d = d[d["frm_name"].astype(str).eq(frm_name)].copy()
    out = pd.DataFrame({
        "event_id": d.get("kb_archivid", pd.Series(dtype=str)).astype(str),
        "peak_time_utc": pd.to_datetime(d.get("event_peaktime"), utc=True, errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "goes_class": d.get("fl_goescls", pd.Series(dtype=str)).fillna("").astype(str).str.upper().str.replace(" ", "", regex=False),
        "noaa_ar": pd.to_numeric(d.get("ar_noaanum"), errors="coerce"),
        "source": "HEK_" + (frm_name or "ALL").replace(" ", "_"),
        "source_url": HEK_BASE,
    })
    return out.dropna(subset=["peak_time_utc"]).reset_index(drop=True)

def nearest_summary(goes: pd.DataFrame, hek: pd.DataFrame, tol_h: float) -> dict:
    g = goes.copy(); h = hek.copy()
    for d in (g, h):
        d["t"] = pd.to_datetime(d["peak_time_utc"], utc=True, errors="coerce")
        d["letter"] = d["goes_class"].str[:1]
    g = g.sort_values("t"); h = h.sort_values("t")
    # Use an explicit nearest-time loop so both source timestamps remain in the
    # receipt table; this avoids hiding source-time differences in merge_asof.
    # Build a compact, auditable matched table.
    rows = []
    ht = h["t"].tolist()
    for _, r in g.iterrows():
        if not ht: continue
        j = min(range(len(ht)), key=lambda k: abs((ht[k] - r.t).total_seconds()))
        delta = abs((ht[j] - r.t).total_seconds()) / 3600.0
        if delta <= tol_h:
            rr = h.iloc[j]
            rows.append({"goes_event_id": r.event_id, "hek_event_id": rr.event_id, "peak_delta_h": delta, "goes_class": r.goes_class, "hek_class": rr.goes_class, "class_letter_match": bool(r.letter == rr.letter)})
    mm = pd.DataFrame(rows)
    mplus_g = g[g.letter.isin(["M","X"])]
    mplus_h = h[h.letter.isin(["M","X"])]
    return {
        "goes_events": int(len(g)), "hek_events": int(len(h)),
        "goes_mplus_events": int(len(mplus_g)), "hek_mplus_events": int(len(mplus_h)),
        "nearest_matches_within_tolerance": int(len(mm)),
        "nearest_class_letter_agreement_fraction": float(mm.class_letter_match.mean()) if len(mm) else None,
        "mplus_nearest_matches_within_tolerance": int(mm[mm.goes_class.str[:1].isin(["M","X"])].shape[0]) if len(mm) else 0,
        "mplus_class_letter_agreement_fraction": float(mm.loc[mm.goes_class.str[:1].isin(["M","X"]), "class_letter_match"].mean()) if len(mm) and (mm.goes_class.str[:1].isin(["M","X"])).any() else None,
        "time_tolerance_h": tol_h,
        "interpretation": "descriptive event-source comparison only; not a raw-FITS transport or predictive-validation result",
    }, mm

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="2019-05-06")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "partial_event_provenance_20190506")
    ap.add_argument("--time-tolerance-h", type=float, default=1.0)
    args = ap.parse_args()
    day = pd.Timestamp(args.date, tz="UTC"); end = day + pd.Timedelta(days=1)
    args.out.mkdir(parents=True, exist_ok=True)
    year = day.year
    goes_url = f"{GOES_BASE}/sci_xrsf-l2-flrpt_geo_y{year}_v1-0-1.csv"
    hek_params = {"cosec":"2", "cmd":"search", "type":"column", "event_type":"fl", "event_starttime":day.strftime("%Y-%m-%dT%H:%M:%S"), "event_endtime":end.strftime("%Y-%m-%dT%H:%M:%S"), "event_coordsys":"helioprojective", "x1":"-1200", "x2":"1200", "y1":"-1200", "y2":"1200"}
    hek_url = HEK_BASE + "?" + urlencode(hek_params)
    goes_raw = fetch(goes_url); hek_raw = fetch(hek_url)
    (args.out / "goes_source.csv").write_bytes(goes_raw)
    (args.out / "hek_source.json").write_bytes(hek_raw)
    goes = normalize_goes(goes_raw, day, end)
    hek_all = normalize_hek(hek_raw, None)
    hek_swpc = normalize_hek(hek_raw, "SWPC")
    hek_ssw = normalize_hek(hek_raw, "SSW Latest Events")
    goes.to_csv(args.out / "goes_events.csv", index=False)
    hek_all.to_csv(args.out / "hek_events_all.csv", index=False)
    hek_swpc.to_csv(args.out / "hek_events_swpc.csv", index=False)
    hek_ssw.to_csv(args.out / "hek_events_ssw.csv", index=False)
    summaries = {}
    for name, h in [("all", hek_all), ("swpc", hek_swpc), ("ssw", hek_ssw)]:
        summary, matches = nearest_summary(goes, h, args.time_tolerance_h)
        matches.to_csv(args.out / f"event_matches_{name}.csv", index=False)
        summaries[name] = summary
    meta = {
        "status": "pending_raw_fits",
        "transport_audit_complete": False,
        "predictive_metrics_generated": False,
        "date_utc": args.date,
        "requested_components": {"raw_fits_manifest": False, "provider_summary": False, "raw_reconstructed_features": False, "goes_events": True, "hek_events": True},
        "blocker": "No HMI/SHARP raw-FITS segments, provider summary, or independently reconstructed 24-feature table are available; event-only parity cannot satisfy transport contract.",
        "goes_url": goes_url, "goes_sha256": sha256_bytes(goes_raw), "goes_bytes": len(goes_raw),
        "hek_url": hek_url, "hek_sha256": sha256_bytes(hek_raw), "hek_bytes": len(hek_raw),
        "event_counts": {"goes_normalized": int(len(goes)), "hek_all": int(len(hek_all)), "hek_swpc": int(len(hek_swpc)), "hek_ssw": int(len(hek_ssw))},
        "event_source_comparison": summaries,
        "claim_scope": ["public GOES/HEK event retrieval and descriptive timestamp/class comparison", "no raw-data provenance claim", "no external predictive metric", "no transport completion"],
    }
    (args.out / "partial_event_provenance_summary.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
