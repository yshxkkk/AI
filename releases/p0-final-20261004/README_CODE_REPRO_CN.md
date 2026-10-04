# 代码复现包

## 研究对象与主线

本包实现的是以正半径粒球为统计单元的区域原生概率模型。canonical head 将区域 Logistic 的几何均值、父球多尺度先验和区域 Binomial 计数统一成 empirical-Bayes plug-in 层级模型，并显式携带 estimand、支持、几何边界、条件区间、复用条件、行动状态和失败状态。Granular Ball 提供中心、半径、冻结树路径、分配指纹、边界余量和递归 split--refit 状态；point Logistic 只作为严格比较器与零半径闭包。当前区间不是完整联合 Bayesian posterior，也不是分布自由覆盖。

运行语义沿一条可重放的链条组织：冻结结构树并保持训练/查询路径一致，拟合区域头，有限轮次执行不可靠叶的局部 split--refit，再输出概率、条件区间、支持、source region、细化步数、边界和 OOD 状态。证书失效时 deployment 返回 abstain/NaN；`raw` 仅为诊断。复用、压缩和抗扰动都是证书条件下的属性，不是对所有粒球的无条件承诺。

point Logistic 仅用于 singleton/identity 零半径闭包与比较；正半径区域的失败路径是父区/邻区借力、递归细化、区间输出或 abstain。RegionNativeProbabilityModel 是 canonical computational head；P0 canonical local-all 是精度/机制参考，P0 LOCO--PPC selective residual 是条件部署候选；H/S 仅作为 SI legacy controls，兼容代码保留但默认不启用。区域原生实现把 Binomial 计数、区域 Logistic、父子多尺度传递、邻域平滑、有限递归细化和稳定性证书放进同一个可审计接口。

统一可核验价值链为“区域分配 → 区域概率/支持/几何 → 异质性/支持/边界证书 → 复用、选择性局部细化、借力、abstain 或 fail-closed 回退 → 查询工作量与下游 action 审计”。可审计性、条件稳定性、查询工作量和 proper score 是分开的结果端点，不宣称四者在所有任务上共同占优。契约不变量仅适用于相同冻结分配、冻结支持记录和不变的 certificate eligibility：region ID、记录支持和区域 action eligibility 保持不变；local numerical surface 与逐行 threshold action 可以变化。边界穿越、支持损失或时间迁移失败时必须重新认证或显式回退。

P0 local-all 是精度/机制参考；LOCO--PPC 是固定拓扑的查询工作量候选，不宣称动态 query split 或端到端人工成本下降；Solar 12,659 个 outer anchors 的失败闭环是时间迁移边界，不是正向外部部署结果；SI 另存一个冻结 M4 的等 action-budget selective-risk 探针，但不把它解释为 matched-recall、人时或总计算节省；STEAD/LHC 的对象压缩需要同时报告覆盖或 assigned downstream burden。`gblogistic_s_perturbation_stress_metrics.csv` 仅为历史 GB-Logistic-S 兼容性 stress，不直接证明 P0 鲁棒性。

根目录的 `nature_main_en.tex`、`supplementary_information.tex` 与 `manuscript/` PDF 是当前权威源。运行 `REPRODUCE_NATURE_REVISION.sh` 前先执行 `audit_consistency.py`，再按各任务 manifest 下载并校验公开输入。代码包不重复发布大型 SWAN、LHC 或天气原始数据；STEAD 的 12,000 条 HDF5 子集也是外部可下载输入，正文所用 PhaseNet 墙钟结果由 `stead_phasenet_wallclock_receipt.json` 和对应脚本记录。

区域对象的复用只在冻结分配契约内成立；assignment-preserving 与 reassignment-aware 扰动结果不能混写。`pending`、`protocol-only` 和失败状态不会被当作实证结果。

`evidence/uncertainty/` 保存按实际统计单位生成的描述性区间、Solar重复行去重表、LHC记录行范围、冻结分配等价性检查、失效指纹和复用摊销敏感性。区间不是全体总体保证；复用结果是行/单元访问次数模拟，不是硬件功耗或端到端下游时间。

LHC 轻量折衷审计见 `evidence/lhco/README_LHCO_LIGHTWEIGHT_CLOSURE_CN.md`。新增的 `run_lhco_strict_raw_audit.py` 使用官方 HDF5 与 masterkey，在读取审计标签前冻结 700k/300k development/audit 分区、64 个区域、sideband、region order 和 Point score，并输出 `raw_features/strict_raw_audit/` 下的 event-level vectors、paired event bootstrap、freeze certificate、资源收据和 image-first summary。cap=0.05 的 recall bootstrap 跨零，因此主文只宣称风险封顶下的候选对象压缩与 assigned-event 工作量代理，不宣称召回优势、下游物理拟合节省或人工时间下降。旧的 `run_lhco_sideband_closure_audit.py`、`run_lhco_stratified_closure_audit.py` 和 `lhco_noise_stability_summary.csv` 仍用于补充材料中的 closure、压力和失败边界。

Kepler/KOI/TCE 的小规模预注册 pilot 位于 `evidence/kepler/`。它按 KIC system 做 SHA-256 60/20/20 分割，排除 disposition 等标签泄漏，报告 system-level matched recall、Brier/ECE、TCE call proxy 和 system bootstrap；区域路线在 recall=0.80 下增加 21.4% call proxy 且 Brier 变差，因此为 SI-only failure boundary。FIRMS/VIIRS 位于 `evidence/firms/`，当前受 Earthdata archive authentication、部分 derived event coverage、独立 perimeter labels 和 downstream timing 缺失限制，状态为 `blocked_exploratory_only`，不进入主文。

`evidence/initialization/` 保存 digits 上的 KMeans/MiniBatchKMeans 初始化敏感性诊断。它比较 `k-means++`/`random` 与显式 `n_init`，不用于选择或替换 STEAD、Solar、LHC 的冻结主结果。`source_archive/gbpe_experiments/init_policy.py` 提供可选的初始化契约、最小支持度 fail-closed 检查和 assignment fingerprint；这保障可复现与低支持失败可见，不承诺普遍预测精度提升。

主文的“现有方法—本文对象”对照表说明区域原生统计接口；`evidence/head_registry/` 保存冻结版 head registry、P0 路线和晋级记录；旧 v1 ledger 仅作历史档案。v2 canonical head 是 `RegionNativeProbabilityModel`；P0 路线配置见 `evidence/region_native/region_native_release_config.json` 和 `evidence/next_upgrade/native_bayes_surface/`。point Logistic 仅为严格比较器/零半径闭包，H/S 仅在 SI 作为 disabled-by-default legacy controls。

v1 的 `evidence/CLAIM_LEDGER_V1.md/json` 保留为历史审计档案；v2 的 headline evidence 在 `evidence/region_native/`，主张由 `evidence/CLAIM_LEDGER_REGION_NATIVE_V2.md/json` 管理，必须随 release freeze 重新生成。早期 empirical-Bayes pilot 的 synthetic/Digits proper-score 结果仅用于展示历史失败边界与证书行为；当前 P0 local-all 与 LOCO--PPC 按各自固定拓扑角色报告，不宣称普遍精度、鲁棒性或成本收益；纯 Solar 区域原生重算等待 raw-FITS 与独立 GOES/HEK 输入。
`evidence/verify_claim_ledger.py` 会检查账本与 `HEAD_REGISTRY.json` 的 canonical/control/extension 列表、晋级失败状态和主张编号是否一致。

`evidence/next_upgrade/probability_heads/` 是本轮四类强耦合概率头的固定几何、20-seed synthetic/model-assisted registry screen；包含 point surface、legacy head ablations/PP、GB-Beta-Binomial-S、GB-cloglog/Hazard-S 和多类 GB-Dirichlet-S 的证书、扰动和回退记录。该 screen 的结果支持接口闭包和条件性方向，但不是 Solar/STEAD 外部确认，且四类扩展均未通过全部主文晋级门。运行入口为 `run_probability_head_registry.py`。

P5 的确定性 release-integrity 复核入口为 `evidence/head_registry/run_p5_head_gate_audit.py`，输出 `P5_HEAD_GATE_AUDIT_SUMMARY.json` 与 `P5_HEAD_GATE_AUDIT_META.json`。它只读取已释放的 registry screen、零半径检查和 fail-closed fallback 记录，确认账本/metadata 对齐；不搜索新结构、不重算新的精度或资源结果。由于独立外部验证、false-pass 和 assigned-work 门尚未完成，v1 扩展 head 继续保持 `SI_or_protocol_only`；v2 区域原生 head 的结果仍按实际 proper-score 与成本失败边界报告。协议和边界说明见 `evidence/head_registry/P5_HEAD_GATE_AUDIT_README_CN.md`。

原生 Granular Ball allocator 的合成端到端审计位于 `evidence/gb_native/`；真实 STEAD 12k 子样本的同一 allocator/fail-closed 审计结果位于 `evidence/stead/stead_gb_native_*`，原始 HDF5 仅作外部输入并不随包分发。运行
`python evidence/gb_native/run_gb_native_allocator_audit.py`

该脚本会自动加载发布包内的 `source_archive`；显式设置 `PYTHONPATH=source_archive`
仍然兼容。
可重放 structure/calibration/test 三角色实验；递归 Granular Ball 分配、
该历史审计固定原生 allocator、支持/边界/Brier 证书；它不代表 v2 区域原生主头的逐点回退路线。
这是实现身份和 fail-closed 接口审计，不是外部数据或普遍精度结论。

`evidence/next_upgrade/solar_accuracy_upgrade/README_SUPPORT_ADAPTIVE_PARTIAL_POOLING_CN.md` 记录支持自适应的部分池化 GB-Logistic 协议。它以 point Logistic 为全局偏置，只在 OOF 异质性、有效支持、后验宽度和边界余量同时通过时开放少数局部残差；当前结果未通过确认性精度门，因此不能当作已验证增益。

`evidence/next_upgrade/joint_geometry_probe/FINITE_MENU_JOINT_GEOMETRY_PROTOCOL_CN.md` 与 `finite_menu_joint_geometry_protocol.json` 记录中心、半径和 Logistic 边界的有限候选菜单、角色顺序、同时置信界、fingerprint 失效和 fail-closed 回退。`evidence/next_upgrade/action_estimand/README_ACTION_ESTIMAND_SEPARATION_CN.md` 单独规定部署测度下行动效用的评估；行动结果不回写为样本级 Brier 精度结论。


冻结分配的几何审计由 `source_archive/gbpe_experiments/geometry_certificates.py` 实现：分别输出经验支持相对尺度、公共度量下的精确 Voronoi 分配余量和余量/扰动预算比。它不会修改 cell ID 或自动修复不一致分配；每区域独立度量需要另一种 score-gap 审计。运行检查：`PYTHONPATH=source_archive python -m unittest discover -s source_archive/tests -p 'test_geometry_certificates.py' -v`。

联合中心--半径--Logistic 探针位于 `evidence/next_upgrade/solar_accuracy_upgrade/joint_center_radius/`，可微软几何证书位于 `evidence/next_upgrade/joint_geometry_probe/`；两者均固定 `K=32,n_init=1`，并将未通过支持、边界或优化门的候选 fail-closed 回退到 point Logistic。

`evidence/solar/SOLAR_BASELINE_RUN_REGISTRY.csv` 与 `README_SOLAR_BASELINE_RUN_REGISTRY_CN.md` 固定 Solar 的 baseline/run ID、角色、split、estimand、K/n_init 和比较边界；clean K=64 point benchmark、严格 outer-time point fallback、K=32 conditional action gate、GB-Logistic head probe 与历史 cached-noise diagnostic 不再混称。

`evidence/conditional_benefits/` 是本版本新增的三类结果复现入口：`verify_zero_radius_closure.py` 检查零半径的真实 Dirac target 与估计量分离、预测、目标函数、proper score、ECE、区间、排序/top-k、阈值/拒答行动和 utility 等价；`run_solar_conditional_audit.py` 复现严格 fail-closed 的 Solar 历史独立时间块回放；`run_simulated_conditional_benefit.py` 复现固定三角色模拟；`run_simulated_conditional_benefit_multiseed.py` 复现每场景 20 个固定种子的分布、描述性 bootstrap 区间和 assignment-change/re-certification 诊断；`run_gblogistic_s_perturbation_stress.py` 专门复现嵌套 GB-Logistic-S 的 clean、margin-relative moderate、half-margin、boundary-crossing 和 large-noise stress；paired-slope 文件对同一认证子集比较退化斜率。对应 CSV/JSON 记录证书通过率、测试行覆盖率、回退率、通过子集风险、point 基线风险、组合路由风险、匹配子集退化和回退原因。模拟结果不构成定理覆盖保证，Solar 结果才使用 HARPNUM grouped bootstrap。

## 正式复现入口与状态边界

正文版式约定：面向审稿人展示的复杂表格和流程图统一作为独立图片资产插入正文，使用可编辑的生成脚本同时输出 600 dpi PNG 和矢量 PDF；LaTeX 只负责图片位置、caption、label 和交叉引用。当前 `figures/table1_object_comparison.png`、`figures/claim_evidence_scope.png` 与 `figures/regional_contract_flow.png` 遵循这一约定。新增或修改表格/流程图时，必须同步生成图片、更新四份 TeX/PDF 副本、执行清洁编译和逐页视觉检查；机器可读 CSV/JSON 仍作为数据审计源，不替代正文图片。

`REPRODUCE_NATURE_REVISION.sh verify` 是默认的清洁环境核验：它运行表格/元数据审计、五遍 LaTeX 构建（SI 的目录页码需要第五遍稳定）、4 项几何证书单元测试、canonical 副本逐字节比较、Python 编译检查和可选原始数据分支的输入预检。它不会把缺失的公开原始输入当作零结果，也不会把 protocol-only 分支写成外部指标。

`REPRODUCE_NATURE_REVISION.sh full` 还会重放随包表格可重放的描述性区间和图形；Solar、LHC、STEAD 和天气的完整原始数据重放只有在 `DOWNLOAD_PUBLIC_DATA.md` 所列文件已下载并通过 manifest 校验后才会运行。每次运行把机器可读状态写入时间戳目录；`pending` 只表示输入尚未提供，不表示通过了实证精度门。

Solar 2019--2024 transport audit 的轻量入口是 `evidence/solar/run_solar_transport_audit.py`。它只核验 sampled raw-FITS receipts、provider summary 与 raw 重建特征的 parity，以及独立 GOES/HEK 事件关联；不下载数据、不重新拟合、不生成 predictive metrics。当前包缺少 raw-FITS、provider summary 和 raw 重建特征，但包含一个 event-only GOES/HEK provenance sidecar，运行无参数命令会输出 `status=pending_raw_fits` 并附 blocker、输入计数和 claim scope；没有 sidecar 时则输出 `pending_data`。manifest 还要求每一行 FITS 本地存在、SHA-256 匹配并落在预注册年份范围内。因此 pending transport 不能被解释为外部验证已完成。

正式包的来源权威关系是：根目录 TeX → 根目录五遍编译 PDF → `manuscript/` 与 `submission/` 的逐字节副本；`PACKAGE_MANIFEST.json` 和 detached SHA-256 在最终清理后重建。论文/cover letter 中的日期服从当前投稿稿件；3 October 2026 是本次 v2 审计发布日期。

证书充分性定理的经验覆盖率网格位于 `evidence/theorem_coverage/`。`run_theorem_coverage_grid.py` 使用固定种子和已知合成条件分布，交叉有效支持、K、球内异质性、边界比例、响应/部署测度漂移和有限菜单 M，并输出区间覆盖率、选择性风险违约、false-pass、回退和理论界 slack。该网格是 proof-contract 的经验审计，不替代真实 Solar/STEAD 外部验证。

STEAD downstream call replay: `evidence/stead/run_stead_phasenet_wallclock.py` loads the checksum-verified 12,000-waveform-window Zenodo subsample and executes SeisBench PhaseNet original v2 on the all-input, canonical station-hash holdout and frozen whole-cell regional queue. `stead_phasenet_wallclock_receipt.json` records model/config URLs and hashes, package versions, raw I/O, frozen feature extraction, model-load, gate and PhaseNet wall times, RSS and limitations. `run_stead_matched_recall.py` additionally recomputes the frozen target-recall prefixes and cross-matched assigned-trace counts; at 0.80 recall, point uses 815 traces while the regional prefix assigns 839 traces across 23 cells. The 15 W number is a wall-time proxy; this audit does not claim full-release seismic accuracy or operational alert utility.

## 当前区域原生修复边界

`evidence/region_native/tests_region_native_contract.py` 当前 14/14 通过。headline synthetic/Digits metadata 的 `refinement_rounds=0` 表示该次 headline fit 未接受额外局部 split；递归机制本身已实现，并在独立 six-seed refinement audit 中跨 head、粒度和图权重测试。早期 empirical-Bayes pilot 的 synthetic/Digits proper-score 负边界仅适用于该历史 pilot；当前 P0 local-all 以固定拓扑结果作为精度/机制参考，LOCO--PPC 以查询工作量候选报告。Solar raw-FITS + GOES/HEK transport 仍需外部输入。
