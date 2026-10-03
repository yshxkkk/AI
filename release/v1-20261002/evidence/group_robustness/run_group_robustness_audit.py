#!/usr/bin/env python3
"""Aggregate grouped robustness evidence already bundled with the release.

This runner deliberately performs no download and no model refit.  It reads the
frozen STEAD station bootstrap, EEG subject bootstrap and Solar action-budget
exports and writes a common audit table.  Solar HARPNUM rows are a descriptive
support/action audit because the released row-level predictions do not expose a
HARPNUM key for an independent group bootstrap.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd


def add(rows, domain, unit, method, metric, estimate, lo, hi, n_groups, scope, status, note=""):
    rows.append({"domain":domain,"group_unit":unit,"method":method,"metric":metric,
                 "estimate":float(estimate) if pd.notna(estimate) else np.nan,
                 "q025":float(lo) if pd.notna(lo) else np.nan,
                 "q975":float(hi) if pd.notna(hi) else np.nan,
                 "n_groups":int(n_groups) if pd.notna(n_groups) else np.nan,
                 "scope":scope,"claim_status":status,"note":note})


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args=ap.parse_args(); root=args.root
    out=root/"evidence"/"group_robustness"; out.mkdir(parents=True, exist_ok=True)
    rows=[]; sources={}

    # STEAD: station-hash clustered bootstrap of frozen holdout predictions.
    f=root/"evidence"/"stead"/"stead_station_bootstrap_summary.csv"
    raw=root/"evidence"/"stead"/"stead_station_bootstrap_raw.csv"
    d=pd.read_csv(f); n=int(pd.read_json(root/"evidence"/"stead"/"stead_station_bootstrap_metadata.json", typ="series")["n_station_keys"])
    sources["stead_summary"]=str(f.relative_to(root)); sources["stead_raw"]=str(raw.relative_to(root))
    for metric in ["point_brier","region_brier","brier_diff_region_minus_point",
                   "point_logloss","region_logloss","logloss_diff_region_minus_point",
                   "point_calls80","region_calls80","calls_diff_region_minus_point",
                   "point_recall80","region_recall80","recall_diff_region_minus_point"]:
        r=d.loc[d.metric.eq(metric)].iloc[0]
        add(rows,"STEAD","station-hash bootstrap",metric.split("_")[0] if metric.startswith(("point_","region_")) else "point-vs-region",
            metric,float(r["median"]),float(r["q025"]),float(r["q975"]),n,
            "frozen holdout descriptive clustered bootstrap","measured; no external rerun",
            "5000 station-key resamples; queue-input metric is not a PhaseNet accuracy guarantee")

    # EEG: subject-level bootstrap, already generated from unseen query subjects.
    f=root/"v6"/"evidence"/"flagship_external_eeg_91subjects"/"subject_bootstrap_summary.csv"
    raw=root/"v6"/"evidence"/"flagship_external_eeg_91subjects"/"subject_bootstrap_raw.csv"
    eeg=pd.read_csv(f); sources["eeg_summary"]=str(f.relative_to(root)); sources["eeg_raw"]=str(raw.relative_to(root))
    n_eeg=int(eeg.n_subjects.iloc[0])
    # Cross-check the declared subject count against the raw bootstrap rows.
    # This guards against accidentally carrying over the STEAD station count
    # when the grouped table is regenerated.
    eeg_raw=pd.read_csv(raw)
    n_eeg_raw=int(eeg_raw["subject"].nunique())
    if n_eeg_raw != n_eeg:
        raise ValueError(f"EEG subject-count mismatch: summary={n_eeg}, raw={n_eeg_raw}")
    # Keep all methods to make the comparison auditable; selected methods are
    # highlighted by the note rather than promoted to a universal claim.
    for _,r in eeg.iterrows():
        m=str(r.method)
        for metric,mean_col,lo,hi in [
            ("subject_brier","subject_brier_mean","subject_brier_bootstrap_lo","subject_brier_bootstrap_hi"),
            ("subject_log_loss","subject_log_loss_mean","subject_log_loss_bootstrap_lo","subject_log_loss_bootstrap_hi"),
            ("subject_ece","subject_ece_mean","subject_ece_bootstrap_lo","subject_ece_bootstrap_hi"),
            ("subject_interval_coverage","subject_interval_coverage_mean",None,None),
        ]:
            if metric=="subject_interval_coverage":
                est=float(r[mean_col]); qlo=np.nan; qhi=np.nan
            else:
                est=float(r[mean_col]); qlo=float(r[lo]); qhi=float(r[hi])
            # Use the declared number of unseen query subjects.  The previous
            # release accidentally reused the STEAD station count here,
            # causing EEG rows to report n_groups=236 despite the source
            # summary declaring 19 query subjects.
            add(rows,"EEG","unseen subject",m,metric,est,qlo,qhi,n_eeg,
                "19 unseen query subjects; subject bootstrap","measured; no clinical claim",
                "subject-level interval for Brier/log-loss/ECE; coverage is empirical over declared subjects")

    # Solar: available export has HARPNUM counts but no row-level HARPNUM key
    # for an independent bootstrap.  Report support/action burden only.
    f=root/"evidence"/"solar"/"solar_state_inverse_budget.csv"
    solar=pd.read_csv(f); sources["solar_state_inverse_budget"]=str(f.relative_to(root))
    for (h,t),g in solar.groupby(["horizon_h","target_recall"], sort=True):
        for _,r in g.iterrows():
            m=str(r.method)
            add(rows,"Solar", "HARPNUM/action support", m, f"n_unique_HARPNUM@recall{t:g}h{h:g}",
                r.n_unique_HARPNUM,np.nan,np.nan,np.nan,
                "frozen historical action-budget export","descriptive; no HARPNUM bootstrap",
                "row-level HARPNUM IDs are not present in the released prediction table; do not infer group risk CI")
            add(rows,"Solar", "HARPNUM/action support", m, f"state_windows@recall{t:g}h{h:g}",
                r.state_windows,np.nan,np.nan,np.nan,
                "frozen historical action-budget export","descriptive; no HARPNUM bootstrap",
                "positive-state proxy; not raw HMI image reread")
    summary=pd.DataFrame(rows)
    summary.to_csv(out/"group_robustness_summary.csv", index=False)
    # Domain status is intentionally explicit so downstream text cannot treat
    # all rows as comparable inferential intervals.
    status=pd.DataFrame([
      {"domain":"STEAD","unit":"station-hash","status":"complete_descriptive_cluster_bootstrap","n_groups":n,"source":"evidence/stead/stead_station_bootstrap_*","limitation":"frozen prediction bootstrap; no new waveform or PhaseNet accuracy rerun"},
      {"domain":"EEG","unit":"subject","status":"complete_subject_bootstrap","n_groups":n_eeg,"source":"v6/evidence/flagship_external_eeg_91subjects/subject_bootstrap_*","limitation":"19 unseen query subjects; empirical group coverage, not clinical validity"},
      {"domain":"Solar","unit":"HARPNUM","status":"support_action_only","n_groups":"not exposed","source":"evidence/solar/solar_state_inverse_budget.csv","limitation":"no released row-level HARPNUM IDs; no group-risk interval or transport claim"},
    ])
    status.to_csv(out/"group_robustness_domain_status.csv", index=False)
    meta={"version":"group_robustness_audit_v1","scope":"existing bundled outputs only; no downloads or refits",
          "sources":sources,"group_counts":{"STEAD_station_keys":int(n),"EEG_query_subjects_summary":int(n_eeg),"EEG_query_subjects_raw":int(n_eeg_raw)},
          "n_summary_rows":int(len(summary)),"status":"measured_with_explicit_solar_limitations",
          "notes":["Bootstrap intervals are descriptive under the declared grouping units.","Solar HARPNUM rows report action/support burden only because row-level group keys are absent.","No universal accuracy, robustness or resource claim is made."]}
    (out/"group_robustness_meta.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"outdir":str(out),"summary_rows":len(summary),"status_rows":len(status)},ensure_ascii=False))

if __name__=="__main__": main()
