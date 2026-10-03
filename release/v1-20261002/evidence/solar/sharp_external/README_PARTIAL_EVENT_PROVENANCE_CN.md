# 小规模 GOES/HEK 事件 provenance probe（非 transport 完成）

本目录中的 `partial_event_provenance_20190506/` 是在当前工作空间能够独立重放的**事件源辅助审计**。脚本从 NOAA/NCEI 的 2019 GOES XRS 年度事件表和 LMSAL HEK 查询接口取得 2019-05-06 的少量事件，记录原始响应的 URL、字节数和 SHA-256，并将 GOES 与 HEK 事件归一化后做 1 小时内的最近时间与 GOES class 字母比较。

该 probe 的状态固定为 `pending_raw_fits`，原因是当前包没有 HMI/SHARP raw-FITS segment、provider SHARP summary 或由 FITS 独立重算的 24 个特征。事件表本身不能替代 raw-FITS provenance、特征 parity 或模型外部验证，因此不产生 Brier、log loss、ECE、区域覆盖或任何预测指标，也不把结果标成 `transport_audit_complete`。

运行：

```bash
python run_partial_event_provenance_probe.py \
  --date 2019-05-06 \
  --out partial_event_provenance_20190506
```

输入源：

- NOAA/NCEI GOES XRS flare report：`sci_xrsf-l2-flrpt_geo_y2019_v1-0-1.csv`；
- LMSAL Heliophysics Events Knowledgebase（HEK）`cmd=search&type=column&event_type=fl`，时间窗口为 2019-05-06 00:00–2019-05-07 00:00 UTC；输出同时保留全部记录、`SWPC` 记录和 `SSW Latest Events` 记录。

当前样本的事件源比较仅用于发现交接风险：不同 HEK 归档器可能有重复记录或 GOES class/活动区标识差异。它不支持将任一来源写成绝对真值。完整 Solar transport audit 仍需按 `README_SOLAR_TRANSPORT_AUDIT_CN.md` 提供 raw-FITS manifest、provider summary、独立 24 特征重建、GOES 事件表和 HEK 事件表。
