# GitHub 发布与权限交接说明

当前会话已验证目标仓库 `yshxkkk/AI` 可写：仓库为公开仓库，连接账户对该仓库返回 `admin`，并具备 Contents: write 与 Pull requests: write 权限。已创建独立发布分支 `release/v1-20261002`；默认分支 `main` 未直接修改。

截至 2026-10-03，本地连接器对该分支观察到 **26 个 UTF-8 文件（含根目录 README）**，远端分支头为 `bc625f6a26c8e96b7c7d3e3faa0f7dad5db2dc61`。本地 `GITHUB_SUBSET_MANIFEST.json` 描述的是 307 项候选审阅子集；该候选子集尚未全部上传，因此不能把当前分支称为完整发布包。

## 发布边界

- 分支用于审阅已上传的源文件与可重放的审计入口；完整正式包（含全部证据、PDF 与校验清单）仍以本地正式 ZIP/后续 GitHub Release asset 或外部存档为准。
- 大型原始数据不随包伪造或打包；Solar 2019–2024 transport、完整 STEAD、完整 LHC systematics/下游拟合和 Weather 多传感器仍按 fail-closed 协议待原始输入。
- DOI 尚未 mint；在存档完成前不填写未生成的 DOI。

## 当前远端状态

- 仓库：`https://github.com/yshxkkk/AI`
- 发布分支：`https://github.com/yshxkkk/AI/tree/release/v1-20261002`
- 权限：已验证 `admin`（包含内容写入与 Pull Request 写入）
- 默认分支：`main` 保持不变
- 远端分支头：`bc625f6a26c8e96b7c7d3e3faa0f7dad5db2dc61`
- 远端已观察 UTF-8 文件数：`26`（含根目录 README）
- 本地候选子集清单：`307` 项（尚未全部上传）
- 审阅策略：优先创建 draft Pull Request；不自动合并。
