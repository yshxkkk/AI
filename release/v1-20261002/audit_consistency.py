#!/usr/bin/env python3
"""Fast source-table to manuscript consistency checks for the review bundle."""
from pathlib import Path
import json, pandas as pd, math
ROOT=Path(__file__).resolve().parent
# Solar external endpoint gate: the released package currently carries only
# the schema fixture and protocol.  This prevents a stale manuscript sentence
# from silently promoting an absent 2019--2024 audit.
sharp_status=json.loads((ROOT/'evidence/solar/sharp_external/sharp_external_status.json').read_text())
assert sharp_status['external_period_present'] is False and sharp_status['headline_metrics'] is False and sharp_status['fixture_only'] is True
solar_manifest=json.loads((ROOT/'evidence/solar/solar_manifest.json').read_text())
assert solar_manifest['status']=='protocol_only_external_validation'
assert all((ROOT/'evidence/solar'/rec['path']).is_file() for rec in solar_manifest['files'])
cover_source = ROOT/'cover_letter_final.tex' if (ROOT/'cover_letter_final.tex').exists() else ROOT/'submission/cover_letter_final.tex'
for manuscript_source in [ROOT/'nature_main_en.tex', ROOT/'supplementary_information.tex', cover_source, ROOT/'DATA_CODE_AVAILABILITY_FINAL_EN.md']:
    txt=manuscript_source.read_text(errors='ignore')
    assert '14,035' not in txt and '196,490' not in txt and '21 of 24' not in txt, manuscript_source
    assert 'author confirmation required' not in txt.lower() and 'nature submission' not in txt.lower(), manuscript_source
# Release additions: corrected whole-cell STEAD endpoint, auditable intervals and
# a contract-level reuse replay must be present and internally consistent.
unc = ROOT/'evidence/uncertainty'
assert (unc/'UNCERTAINTY_AND_REUSE_MANIFEST.json').is_file()
assert (unc/'stead_station_cluster_ci.csv').is_file()
assert (unc/'reuse_amortization_sensitivity.csv').is_file()
bud = pd.read_csv(ROOT/'evidence/stead/stead_raw_budget_curve.csv')
assert int(bud.query("method=='region' and target_recall==0.8").assigned_trace_count.iloc[0]) == 839
assert 'provable under declared assumptions' in (ROOT/'nature_main_en.tex').read_text().lower()
assert 'assignment-preserving' in (ROOT/'supplementary_information.tex').read_text()
# Initialization sensitivity is a registered descriptive diagnostic.  It must
# remain separate from the frozen headline tables, while the optional helper
# exposes a fail-closed support contract.
init_dir = ROOT/'evidence/initialization'
assert (init_dir/'quick_kmeans_init_diagnostic.py').is_file()
assert (init_dir/'quick_kmeans_init_raw.csv').is_file()
assert (init_dir/'quick_kmeans_init_summary.csv').is_file()
init_meta = json.loads((init_dir/'initialization_diagnostic_manifest.json').read_text())
assert init_meta['status'] == 'descriptive_sensitivity_only'
qi = pd.read_csv(init_dir/'quick_kmeans_init_summary.csv')
assert len(qi) == 12 and set(qi.estimator) == {'KMeans','MiniBatchKMeans'}
kp1 = qi[(qi.estimator=='KMeans')&(qi.init=='k-means++')&(qi.n_init==1)].iloc[0]
kp10 = qi[(qi.estimator=='KMeans')&(qi.init=='k-means++')&(qi.n_init==10)].iloc[0]
assert float(kp10.brier_mean) < float(kp1.brier_mean)
assert (ROOT/'source_archive/gbpe_experiments/init_policy.py').is_file()
# Solar metrics
s=pd.read_csv(ROOT/'evidence/solar/solar_metrics.csv')
checks={
 ('regional_entropy',24,'brier'):0.020135,
 ('regional_entropy',48,'brier'):0.030070,
 ('point_logistic',24,'brier'):0.016000,
 ('point_logistic',48,'brier'):0.024082,
}
for (method,h,m),v in checks.items():
 r=s[(s.method==method)&(s.horizon_h==h)].iloc[0]
 assert math.isclose(float(r[m]),v,rel_tol=0,abs_tol=2e-5),(method,h,m,r[m],v)
# LHC clean event-level rerun
raw_manifest=json.loads((ROOT/'evidence/lhco/raw_features/lhco_raw_feature_manifest.json').read_text())
assert raw_manifest['n_events']==1_000_000 and raw_manifest['n_audit']==300_000 and raw_manifest['n_signal_audit']==263
b=pd.read_csv(ROOT/'evidence/lhco/raw_features/audit_results/lhco_budget_curves.csv')
q=b[(b.method=='point_isolation_forest') & (b.target_recall==0.5)].iloc[0]
g=b[(b.method=='granular_region') & (b.target_recall==0.5)].iloc[0]
assert int(q.n_events_reviewed)==74951 and int(g.n_human_review_objects)==28
assert int(g.n_events_reviewed)==137656
split=json.loads((ROOT/'evidence/lhco/lhco_split_index.json').read_text())
assert split['phase_space']==['log1p(leading_jet_mass)','log1p(leading_jet_pt)','log1p(all_particle_mass)']
assert split['region_menu']['K']==64 and split['look_elsewhere']['bonferroni_trials']==378
m_lhco=json.loads((ROOT/'evidence/lhco/lhco_budget_noise_manifest.json').read_text())
assert m_lhco['status']=='measured_clean_and_noise_event_level_rerun' and m_lhco['noise_reps']==10
noise=pd.read_csv(ROOT/'evidence/lhco/raw_features/audit_results_reps10/lhco_noise_stability.csv')
assert len(noise)==240 and noise.mechanism.nunique()==6 and noise.eta.nunique()==4
# EEG fixed-batch sensitivity plus corrected 91-subject expansion
q=pd.read_csv(ROOT/'v6/evidence/flagship_external_eeg/flagship_eeg_summary.csv')
r=q[q.method=='granular_region'].iloc[0]
for col,v,tol in [('brier_mean',0.242152,2e-5),('log_loss_mean',0.678288,2e-5),('ece_mean',0.040074,2e-5),('group_interval_width_mean',0.186608,2e-5)]:
 assert math.isclose(float(r[col]),v,rel_tol=0,abs_tol=tol),(col,r[col],v)
cv=pd.read_csv(ROOT/'v6/evidence/flagship_external_eeg_91subjects/flagship_eeg_summary.csv')
r=cv[cv.method=='granular_region'].iloc[0]
for col,v,tol in [('brier_mean',0.24768072,2e-6),('log_loss_mean',0.68878467,2e-6),('ece_mean',0.04081878,2e-6),('group_interval_width_mean',0.10286664,2e-6)]:
 assert math.isclose(float(r[col]),v,rel_tol=0,abs_tol=tol),(col,r[col],v)
assert math.isclose(float(r.group_interval_coverage_mean),0.51578947,abs_tol=2e-6)
assert json.loads((ROOT/'v6/evidence/flagship_external_eeg_91subjects/run_metadata.json').read_text())['seeds']==[0,1,2,3,4]
# Grouped robustness audit: preserve the declared independent units. This
# catches accidental reuse of the 236-station STEAD count for EEG's 19 query
# subjects when the common summary table is regenerated.
gr = ROOT/'evidence/group_robustness'
gs = pd.read_csv(gr/'group_robustness_summary.csv')
assert set(gs.loc[gs.domain.eq('STEAD'),'n_groups'].dropna().astype(int)) == {236}
assert set(gs.loc[gs.domain.eq('EEG'),'n_groups'].dropna().astype(int)) == {19}
gstatus = pd.read_csv(gr/'group_robustness_domain_status.csv')
assert int(gstatus.loc[gstatus.domain.eq('STEAD'),'n_groups'].iloc[0]) == 236
assert int(gstatus.loc[gstatus.domain.eq('EEG'),'n_groups'].iloc[0]) == 19
gmeta = json.loads((gr/'group_robustness_meta.json').read_text())
assert gmeta['group_counts']['STEAD_station_keys'] == 236
assert gmeta['group_counts']['EEG_query_subjects_summary'] == 19
assert gmeta['group_counts']['EEG_query_subjects_raw'] == 19
# STEAD raw-waveform matched-FPR audit. Region review objects must be cells
# from the frozen K=64 table; a previous export accidentally sorted event rows
# and reported impossible counts (>64), so this is an explicit regression check.
st=pd.read_csv(ROOT/'evidence/stead/stead_raw_matched_fpr.csv')
sr=st[st.method=='region']
assert int(sr.selected_object_count.max()) <= 64, sr.selected_object_count.max()
row=sr[sr.fpr_cap==0.20].iloc[0]
assert int(row.selected_object_count)==36 and int(row.assigned_trace_count)==1242
assert math.isclose(float(row.achieved_recall),0.9673267,abs_tol=2e-6)
assert int(pd.read_csv(ROOT/'evidence/stead/stead_raw_budget_curve.csv').query("method=='region'").selected_cell_count.max()) <= 64
# Selector-alignment v6: the figure is generated from this six-repeat summary,
# while the raw and regional tables retain the full audit fields.
sel_dir = ROOT/'evidence/selector_alignment'
sel_raw = pd.read_csv(sel_dir/'selector_alignment_v6_raw.csv')
sel_sum = pd.read_csv(sel_dir/'selector_alignment_v6_summary.csv')
assert len(sel_raw)==48 and set(sel_raw.selector)=={'entropy','lepski_local'}
assert sorted(sel_raw.n_per_role.unique().tolist())==[400,800,1600,3200]
e=sel_sum[(sel_sum.selector=='entropy')&(sel_sum.n_per_role==800)].iloc[0]
l=sel_sum[(sel_sum.selector=='lepski_local')&(sel_sum.n_per_role==800)].iloc[0]
for col,v in [('mse_mean',0.0158552846),('selected_depth_mean',1.166666667),('regional_width_mean',0.167662660)]:
    assert math.isclose(float(e[col]),v,rel_tol=0,abs_tol=2e-8),(col,e[col],v)
for col,v in [('mse_mean',0.0467233014),('selected_depth_mean',0.0),('regional_width_mean',0.118566803)]:
    assert math.isclose(float(l[col]),v,rel_tol=0,abs_tol=2e-8),(col,l[col],v)
assert json.loads((sel_dir/'selector_alignment_v6_replay_check.json').read_text())['metrics_match_excluding_wall_clock_columns'] is True
print('OK: solar, LHC, EEG, STEAD and selector-alignment source-table checks passed')
