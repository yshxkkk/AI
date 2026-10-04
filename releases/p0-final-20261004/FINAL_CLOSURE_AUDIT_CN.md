# P0 收尾闭环审计（2026-10-04）

本次收尾冻结两条主路线：`P0-canonical-local-all` 是精度与机制参考，`P0-LOCO-PPC-selective-residual` 是条件部署候选。`P0-exact-residual-identity`、`P0-K32-UCB-microball`、pure scalar 与 grouped-native 仅保留在补充材料。H/S 只作为 `historical head ablations / legacy controls` 保留在补充材料和兼容代码中，主接口、主配置、摘要和 headline 结果不再突出它们。

## 已完成的四项收尾工作

1. **统一独立校准角色。** Synthetic 与 Digits 各完成六个固定 seed 的统一 replay。child--parent Brier/log-loss、ECE、class-balanced ESS、分组 Kish ESS、Westfall--Young simultaneous correction 与 posterior-predictive coverage 已放在同一协议中。保守 gate 的 local-surface fraction 为 26.18%/18.19%，PPC coverage 为 0.917/0.693；Brier 为 0.214812/0.059319，而同轮 P0 为 0.214372/0.046271。Digits 的分组 ESS 中位数为 0，gate 因此 fail closed 并回退 P0；该结果是安全边界审计，不是选择性路线的精度晋级。
2. **LOCO--PPC 工作负载审计。** 冻结预测上的 replay 记录了零 query-time Point Logistic calls、active local-surface fraction、unique regions/actions、RSS、算术 replay wall time 与 retrospective matched-recall envelope。Digits 的 active fraction 为 0.7597、Synthetic 为 0.6263；arithmetical replay 的 wall time 约为 0.0035/0.0094 ms，峰值 RSS 约为 54.4/58.2 MB。该 wall time 不含拟合、路由、I/O 或下游调用，matched-recall 结果只用于审计，不构成端到端速度或人工审核节省声明。
3. **Solar 时间块边界。** 已完成 released SWAN--SF 表上的严格 chronological/HARPNUM-disjoint outer-time audit（2014--2018 测试块共 12,659 anchors，24/48 h）。固定风险 gate 在两个 horizon 均拒绝全部 regional cells，最终 100% 回退 Point Logistic；这是完成的 fail-closed 时间迁移边界，不是正向外部部署结果。正文保留冻结 M4 的等 action-budget selective-risk 探针，SI 另存完整预算网格，不把它解释为 matched-recall、人时或总计算节省。2019--2024 raw-FITS/SHARP、GOES/HEK 独立标签和重建 feature table 仍未提供，因此外部端点保持 protocol-only，不报告外部预测指标。
4. **新增四项 targeted upgrade。** P0 direct stress 支持证书内复用与跨界回退；LOCO 真实查询路径确认表面调用减少但未形成普遍 wall-clock 优势；Solar M4 同 selector 分解显示主要是局部概率面校准信号且 16-endpoint 联合区间跨零；STEAD 六次 PhaseNet 重复计时可复现，但 matched recall 下区域仍多 24 条 assigned traces，保持负向边界。

5. **版本与可审计性冻结。** claim ledger、head registry、release metadata、canonical configuration、source index、代码复现说明、manifest/hash 与 formal release audit 已同步。主文和 SI 的 canonical 副本逐字节一致；最终同步目标为主文 16 页、SI 87 页、cover 2 页。严格原始 LHC 审计、Kepler/TCE pilot 和 FIRMS feasibility boundary 已写入证据索引；Kepler 与 FIRMS 未通过晋级门，不进入主文正向性能结论。formal checker 已在最终 PDF 同步后运行，结果为 0 errors；manifest 含 1,831 entries。

## 正文采用的机制解释

P0 在已测 Synthetic/Digits 协议上优于同角色 Point Logistic 的原因写成三个互补机制：regional anchor 过滤 assignment-preserving 的无关细节扰动；local residual surface 保留粒球内可识别的条件异质性；parent/global shrinkage 在稀疏球中借助更大尺度支持控制局部方差。因而它可以减少单一全局 slope 的失配，同时避免完全独立 local fit 的方差代价。该解释是冻结表示、分配和证书门控下的条件机制证据，不是对任意噪声或任意外部分布的不变性声明。

## 训练点与查询点的结论

训练阶段减少 point 的主要价值是理论上的表示和计算扩展性，只有在频繁重训或超大规模数据下才直接转化为成本收益。当前稿件把应用侧重点放在查询阶段：区域对象复用、local-surface evaluation、unique region/action 与 matched-recall downstream workload。因而 P0 local-all 作为高精度 reference，LOCO--PPC 作为 scalar-first、可审计但需 fail-closed 的 deployment candidate；统一协议是否能够在特定域中替代 P0，必须由 ESS、同时校正、PPC、外部时间块和端到端 workload gates 决定。

## 新增真实任务端点与晋级结论

- **LHC BlackBox1**：官方 HDF5/masterkey 已恢复；development/audit、64 区域、sideband、region order 与 Point score 在读取 masterkey 前冻结。cap=0.05 下区域候选对象为 3、assigned events 为 13,669，相比 Point 的 14,997 减少 8.85%；FPR 差异区间低于零，但 recall 差异区间跨零。因此主文只保留风险封顶下的候选对象/assigned-event 代理，不宣称召回、物理拟合或人工时间优势。
- **Kepler/TCE**：预注册 system-level pilot 在 recall=0.80 时增加 21.4% call proxy 且 Brier 变差，保留为 SI failure boundary。
- **FIRMS/VIIRS**：官方归档认证、完整事件表、独立 perimeter label 和真实 downstream timing 尚未闭合，保留为 protocol/provenance boundary。

最终跨任务结论使用 task-conditional region utility frontier：同一契约可在明确的匹配风险或匹配召回点减少候选负担，也会在覆盖、校准、下游 burden 或时间迁移失败时显式回退。该结论不外推为普遍人工成本下降或所有任务上的综合性能优势。

## 本轮新增实验结论

- LHC 全新 600k development / 100k calibration / 300k audit：区域 assigned events 11,324，对 Point 的 15,363 减少 26.29%；recall 差异 +0.14068 [ +0.07806, +0.20240 ]，FPR 差异 -0.01360 [ -0.01449, -0.01261 ]。这是 post-inspection protocol-repair replication，可强化固定风险候选压缩证据，不构成真实物理拟合或人工时间收益。
- Solar action-unit sensitivity：HARPNUM 与 HARPNUM×UTC-day 分别代表持续活动区复核和日级监测行动；50% budget 下两者都达到 route recall=1.0，但 selective-risk 幅度和 fallback fraction 不同。该图进入 SI，说明行动单位必须作为区域契约的一部分显式声明。
- LOCO large-batch scaling：超过 (10^5) 行时 local-surface fraction 仍为 62.63%/75.97%，但当前实现 wall-clock 比 P0 高 21.4%/14.3%。这强化 workload frontier 和失败边界叙事，不支持普遍加速。

- LHC fresh downstream closure：对 64 个冻结区域完成跨角色 sideband-transfer closure；development→calibration / development→audit 加权 on ratio 为 1.01129 / 0.99943，且完成 derived-feature systematics surrogate 与 64-region screening proxy。由于缺少官方 detector response、background-only null、真实 physics likelihood fit 和 analyst timing，该结果只进入 SI 作为闭环与失败边界。
- Solar HARPNUM-cluster bootstrap：按 1,205 个 HARPNUM 对日级 action units 做聚类重采样；24 h daily 50% 区间上界为 +0.000002，故保留为 dependence-aware SI sensitivity。
- LOCO exact-parity dispatch：六 seed、固定线程下，bool-vector dispatch 与 legacy 输出及 SHA256 完全一致；Synthetic/Digits 分别比 legacy wall time 减少 28.65%/22.97%，比 P0 快 15.15%/11.13%，但只属于内存查询端点工程审计。
