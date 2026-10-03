# 分组稳健性与证书审计（仅使用已发布证据）

本目录把当前正式包中已有的分组结果整理为统一的、可重放的审计表，**不下载新数据、不重新拟合模型，也不把描述性 bootstrap 提升为分布无关保证**。审计覆盖三个不同的数据角色：

1. **STEAD station-hash holdout**：读取冻结的 `stead_station_bootstrap_raw/summary.csv`，以 236 个 station-hash 为聚类单位，报告 point 与 regional 的 Brier、log loss、80% recall 队列大小及其差值的 2.5--97.5% bootstrap 区间。该结果是冻结预测的分组不确定性审计，不能替代新的波形推理或 PhaseNet 准确率实验。
2. **EEG unseen subjects**：读取 19 个未见 query subject 的 subject bootstrap，报告各已发布方法的 subject-level Brier、log loss、ECE 区间和经验 interval coverage。该 coverage 是声明的 19 个受试者上的经验覆盖，不能解释为临床或总体人群有效性。
3. **Solar HARPNUM**：读取 `solar_state_inverse_budget.csv` 中的 HARPNUM 数量和状态窗口。当前发布的 Solar 行级预测表没有 HARPNUM 主键，因而不能重建独立 HARPNUM bootstrap；这里仅报告 action/support 负担，并明确标记为 `support_action_only`，不报告组风险或传输覆盖区间。

运行：

```bash
python3 evidence/group_robustness/run_group_robustness_audit.py
```

输出：

- `group_robustness_summary.csv`：统一的指标、分组单位、区间和主张状态；
- `group_robustness_domain_status.csv`：每个任务的可审计范围与限制；
- `group_robustness_meta.json`：源文件、版本和不使用外部数据的记录。

## 当前可引用的边界

STEAD 的 station bootstrap 显示区域路由的 Brier 和 log loss 高于 point，且在 80% 召回队列上平均多分配 34 条 trace；这支持 matched-recall 下没有普遍调用节省的结论。EEG 的 `granular_region` 在 19 个未见 subject 上有较低的 subject-level Brier/log loss/ECE 点估计，但 interval coverage 只有 0.516，不能写成无条件优越性。Solar 的 HARPNUM action/support 表显示区域路线使用更多 state windows 和 HARPNUM 单元，因而不支持对象压缩的普遍结论。

这些结果的作用是把“按组审计、条件性复用和失效回退”落实为可检查的分组单位，同时显式显示哪些数据条件尚不足以给出组级不确定性结论。
