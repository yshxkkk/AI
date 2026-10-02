# 2026-10-02 估计量对齐修订说明

本版本以 `from-point-scores-to-certified-regional-probabilities-v1.2026-10-02` 为权威发布包，正文 11 页，Supplementary Information 68 页。


## P0–P5 折衷执行状态

- **P0 发布闭环**：本地 manifest、源文件副本、PDF、ZIP 和一致性审计可重放；GitHub 连接已验证，并已确认目标仓库 `yshxkkk/AI` 具有管理员/写入权限。DOI 仍未生成。
- **P1 Solar 外部 transport**：由于当前会话没有原始 FITS/GOES/HEK 输入，保留 fail-closed handoff 和 `pending_data`，不生成外部预测指标。
- **P2 分组稳健性**：新增 STEAD station-hash、EEG subject 和 Solar action/support 分组审计；这些是声明单位下的描述性区间，不是分布无关覆盖或普遍资源收益。
- **P3 STEAD 原生 allocator**：新增真实 HDF5 依赖的 fail-closed runner；缺少 `test.hdf5/test_noise.hdf5` 时只输出 `pending_missing_input`，不从旧的 `cell_id` 或点概率重建原生特征。
- **P4 LHC 轻量审计**：新增 support/radius/transfer-factor 四分位 closure、delta-method 区间与 assigned-event 分解；仍不声称 background-only closure、detector systematics、下游拟合或 discovery。
- **P5 head gate**：只复核 registry、零半径闭包和 fallback 编码，未搜索或晋级新 head；四个扩展 head 继续为 `SI_or_protocol_only`。

## 主张与模型冻结

本版本的主张、证据等级、禁止外推、canonical computational head、控制 head、protocol-only 扩展和晋级门已冻结在 `evidence/CLAIM_LEDGER_V1.md` 与 `evidence/CLAIM_LEDGER_V1.json`。任何未达到独立验证和 fail-closed 晋级条件的结构，只保留为协议或失败边界；更改 headline claim 必须创建新的 release identifier 并重新生成 manifest。

## 叙事主线的重新定位

本版本把核心对象从“逐点分数附加审计元数据”改写为“以区域分辨率为索引的概率统计对象”。区域概率对象携带明确的 estimand、有效支持、几何范围、局部不确定性、复用条件、行动状态和失败状态；Granular Ball 是本文实现该统计抽象的可审计几何单元。它保留 point surface，不把球内样本替换成没有条件结构的常数概率。 对象身份由 estimand、allocation fingerprint、support/geometry certificate、head、deployment/action contract 和 fallback state 共同确定；任一版本变化都会使旧证书失效。

运行语义被固定为

`区域概率对象 → 证书通过 → 条件性复用/对象压缩/扰动稳定性 → 证书失效时细化、重新认证、回退 point 或拒答`。

因此，复用、压缩和抗扰动都是由支持、同质性、边界、校准、部署测度与漂移证书限定的条件性属性。singleton/identity 零半径分支恢复 point Logistic 的完整预测、目标函数、校准、决策、证书状态和回退语义；零局部项本身只恢复 point surface/objective，gate 拒绝时才按 fail-closed 恢复 point action/certificate；GB-Logistic-S 是 canonical computational head，GB-Logistic-H 是硬支持/边界/审计/回退控制。

概率头 registry 将区域对象契约与具体计算头分离但绑定：每个头都必须登记保留的 point surface、局部耦合方式、零半径闭包、支持/边界/校准/部署字段、资源与 assigned-event 负担、失败原因和 exact point fallback。PP、Beta--Binomial-S、cloglog/Hazard-S 与 Dirichlet-S 用来检验这一接口的可扩展性；当前没有一个扩展头同时通过主文晋级门，因此不把接口筛选写成普遍精度结论。

## 本版本新增三类结果

主文新增“现有方法—本文对象”对照维度，按区域 estimand、有效支持、几何边界、区域不确定性、细化、action contract、point-compatible reduction、证书门控、失败回退、对象压缩和扰动稳定性进行并列说明。该表不声称其他方法不具备某一单项模块，而是明确本文的差异在于把这些性质组合成同一个可审计概率对象和运行协议。 head registry 则把这一对象协议扩展到不同局部概率头，并统一点兼容闭包协议、证书字段、资源负担和 fail-closed 回退；因此 registry 是协议扩展层，不是未经验证的模型排行榜。

- **退化定理**：SI 定理明确把零半径定义为 singleton/identity allocation，并分别证明预测、Logistic 目标函数、Dirac 区域目标、proper-score/calibration functional 与确定性行动恢复 point Logistic；仅把已有多点球的数值半径记为 0 不构成闭包。
- **证书充分性定理**：在冻结表示/分配/有限候选菜单、独立验证、支持下界、球内同质性、边界转移、TV 漂移和联合 surface--measure 证书下给出有限样本区域目标界、Brier 界和选择性非劣界；若结构证书事件的失败概率为 `gamma`，总保证为 `1-gamma-delta`，否则标为 model-assisted conditional。
- **条件收益**：单 seed 的球内异质场景仅作为 illustrative diagnostic（通过 2/16 球、整体 Brier 约改善 `-0.000402`、对象复用代理减少约 `12.08%`）；边界场景改善约 `-0.000021`，污染场景全部回退。20-seed 汇总是正文口径：平均对象复用代理减少约 `4.30%`，route--point Brier 差的区间跨零，因此不宣称普遍精度收益。Solar 历史外层回放 24/48 h 分别通过 7/32、4/32 球，严格 fail-closed 组合 Brier 为 `0.016905/0.025611`，point 为 `0.016629/0.024519`，同时给出正向条件模拟和实际应用中的拒绝边界。

- **本轮严格性补充**：证书定理改为 independent-block 条件，补充 signed-loss 的 TV/边界常数、$2^\alpha$ 同质性因子、联合 `gamma+delta` 预算、部署测度漂移和 model-assisted 标记；零半径 verifier 分离真实 Dirac target 与估计量，并新增排序、top-k、拒答和 utility 检查。
- **多种子条件收益**：新增每场景 20 个固定种子、assignment-change/re-certification/fallback 诊断；球内异质场景平均对象代理减少约 4.30%，固定噪声下约 20.4% 行发生重新归属，保守路由触发重新认证并回退 point。结果为描述性机制证据，不构成定理覆盖保证。

- **证书定理覆盖率网格**：新增已知合成条件分布下的平衡网格（48 配置、每配置 80 次），交叉 `n_eff`、`K`、`h`、`b/pi`、`Delta`、`Delta_mu` 与 `M`。within-bound 层区间覆盖率均值为 1.000，选择性风险违约为 0；将真实结构包络设为声明值 2.5 倍后，覆盖率均值为 0.955，最高 noisy-diagnostic false-pass 为 10.6%，有限菜单 U 门仍通过回退保持选择性风险违约为 0。该结果是 proof-contract 经验审计，不是分布自由或外部数据覆盖保证。

- **GB-Logistic-S 扰动压力审计**：新增 20 个固定种子的 clean、0.25/0.50 倍 assignment margin、boundary crossing 和 large-noise 场景。干净 route--point Brier 差为 `-0.003084`；匹配认证子集上中等扰动时缓存 S 的 Brier 退化为 0，而 point 退化为约 `+0.000072`，0.50 倍 margin 时 point 退化约 `+0.000543`；paired slope 差为 `-0.000600`，bootstrap 区间 `[-0.000957,-0.000228]`。跨界时约 38.3% 分配改变且 100% 回退，large-noise 回退约 99.9%。这些结果是 synthetic/model-assisted 条件证据，不是定理覆盖或新鲜 Solar 外部确认。

## 本轮折衷执行结果

- **GB-native allocator**：使用发布包中的递归坐标中位数 Granular Ball 生成器，在 structure/calibration/test 三角色上完成 12 个固定种子的端到端审计。清洁数据中 8.3% 终端球、9.5% 查询通过证书，GB-native-S Brier 为 0.19740，point Logistic 为 0.19829；仅 1.3% 终端球和 1.5% 查询通过，20% structure-role 标签翻转时 98.5% 查询回退 point。该结果证明接口可以由原生 Granular Ball 执行，但不是外部泛化或普遍精度增益。
- **STEAD matched-recall**：在 12,000 条 checksum-verified 子样本和 2,381 条 station-hash holdout 上，目标召回率 0.80 时 point 使用 815 条波形输入，区域队列选择 23 个区域但分配 839 条波形；目标召回率 0.70/0.90/0.95 时区域分配 736/974/1,068 条，均不支持普遍调用节省。
- **LHC 轻量 closure**：64 个冻结相空间单元的 signal-subtracted sideband-transfer closure 中位数为 0.9934，5--95% 区间为 0.9044--1.0993，加权比为 0.9909；特征、分配和压力审计耗时 2.9--27.2 秒。该结果不等同于 background-only closure，也不包含 detector systematics、look-elsewhere 或下游物理拟合。
- **Solar transport handoff**：新增 raw-FITS/provider-feature/GOES--HEK 的 fail-closed 接口，但当前未提供原始 manifest、重算特征和事件连接，因此状态保持 pending，不生成外部预测指标。

## 本轮正文改动

- 分开样本条件概率面 `q_A(x)` 与部署行动估计量 `theta_{A,D}`；后者在区域内归一化部署测度上积分，不回填为每个状态的点预测。
- Solar 行动评分按去重的 `HARPNUM–UTC day` 单位定义固定预算 M+ recall、固定 recall 的窗口负担、active-region-day false alarms 和 cost per captured positive；状态行不作为独立耀斑事件。M+ 为主终点，X+ 仅作稀疏描述性诊断。
- 固定 `K=32, n_init=1` 的 action/interface 审计加入球内异质性、支持、后验宽度和部署测度失败门控；失败时回退到 point/parent。2019–2024 外部 HMI/SHARP 端点仍是 protocol-only；另附小规模 raw-FITS/GOES/HEK transport handoff runner，当前无原始输入时显式保持 pending，不产生预测性外部指标。
- 已验证的正向证据仅保留为物理表示对 point anchor 的历史修复（严格重接审计：24/48 h Brier 差异约 `-0.000334/-0.000468`）；不将其写成区域精度、成本或外部确认增益。
- 区域积分、rare-event/class-balanced specialization、增大粒球数量或 `n_init` 的结果均保留为失败边界或稳定性审计，不构成正文增益主张。
- 新增冻结分配下的嵌套 GB-Logistic 审计：区域系数置零时严格退化为 point Logistic；canonical M4 相对 M3 的 soft-versus-hard 条件性 Brier 改善进入正文，但 M4 相对 point 的区间仍跨零。
- **概率头登记与主线冻结**：将 GB-Logistic-S 明确为 canonical computational head，将 GB-Logistic-H 定义为 hard support/audit/fallback control，point Logistic 为严格嵌套基线；登记 GB-Logistic-PP、GB-Beta-Binomial-S、GB-cloglog/GB-Hazard-S 和 GB-Dirichlet-S 四类扩展。主文最多保留一个经独立验证的扩展头；本版本四类扩展均未通过全部晋级门，因此只作为可扩展接口、协议和失败边界，不新增精度主张。
- **四类 head 的固定几何合成审计**：20-seed、三角色、独立 synthetic test 下，S/PP clean Brier 分别相对 point 改善 `-0.001783/-0.001786`，Beta-S/Hazard-S 为 `-0.002090/-0.002095`；20% label noise 下四者区间仍为负，40% 时 Beta/Hazard 区间跨零，S/PP 仅略低于零；认证路由约 9–14%，其余 fallback point。Dirichlet-S clean Brier 变差约 `+0.00225`，仅证明接口闭包。上述均为 synthetic/model-assisted evidence，不能替代 Solar/STEAD 外部确认，也不构成新增 headline gain。
- 按用户命名复核 `GB-Logistic-H_hybrid` 与 `GB-Logistic-S_soft`：S 相对 H 的 Brier 改善为约 `-0.000655/-0.000606`（24/48 h，HARPNUM paired CI 不跨零），但两者相对 point Logistic 均未通过确认性增益门；因此只写作 hard-block failure boundary，不宣称区域或计算优势。
- H/S 使用固定 `K=32, n_init=1`、固定中心/半径/cell ID/Wendland 权重；未增加粒球数量或 `n_init`，未改变支持、边界、失败、回退和行动接口。相关脚本、系数、几何、预测、bootstrap 与协议索引均随包提供。
- 新增中心、半径和 Logistic 边界联合优化审计：Wendland 交替 probe 相对 point 的名义 Brier 为 `-0.000263/-0.000277`，但相对 canonical M4 区间跨零；late support/risk gate 安全 cell 为 0、可部署路线 100% 回退 point。可微 trust-region probe 未通过优化收敛门，严格 fail-closed 后为 point。该结果只进入 SI/证据包，不进入正文精度主张。
- 将残差式、部分池化 GB-Logistic 明确写成下一阶段模型：局部截距/低秩斜率由公共收缩先验估计，支持、球内异质性、后验宽度和边界余量共同决定局部权重；局部项为零时精确退化为 point Logistic。当前 OOF 结果仍未通过全局 Brier 门，因此只保留为可审计协议和失败边界。
- 将联合中心--半径--Logistic 更新改写为有限候选菜单，预先固定中心扰动、半径比例、`C`、信任域、最大候选数和角色顺序；任何几何变化均重建支持、Voronoi/radial/logit/action 证书和 fingerprint，失败时 fail-closed 回退同角色 point。
- 新增独立行动 estimand 协议，要求固定部署测度、HARPNUM/时间交叉拟合、可观测行动与成本日志，并把 sample-level Brier/log loss 与区域行动 utility 分开报告；当前仍为 protocol-only。
- 按“物理 point 表示→时间结构→选择性残差头→有限几何菜单→部署行动估计量”的五阶段顺序重排晋级门：只有同时通过 immediate-parent 机制门和 strongest-point headline 门才进入正文；严格 point-only hazard 与物理交互 probe 均未超过 canonical point，作为 SI 失败边界归档。
- 新增 `GB-Logistic-S_sel` 选择性局部头：固定物理 point 表示和 `K=32,n_init=1` 分配，仅在支持、异质性、后验宽度、边界余量与 OOF 遗憾门允许的少数粒球上启用软残差，其他粒球精确回退 point；稀有事件正例数收缩和严格 finite-menu 屏幕已归档。相对匹配 point/M4 的区间均跨零，故该方向只作为 SI 机制与失败边界，不进入正文精度收益。

`PACKAGE_MANIFEST.json`、`PACKAGE_MANIFEST.sha256` 与 canonical PDF 哈希已同步更新；`audit_consistency.py` 返回 `OK`。

