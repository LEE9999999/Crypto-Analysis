---
name: crypto-project-evaluator
version: "1.6.0"
description: "AI驱动的Crypto/Web3项目多维度评估插件。5阶段流水线(信息收集→萃取→并行分析→全局洞察→报告渲染)，7维度加权评分(基本面/安全/流量/链上/叙事/资金/市场)，可插拔数据层(5个MCP Server+WebFetch降级)，跨维度关联规则，安全一票否决。用户输入项目名/Ticker/合约地址即可生成完整评估报告。"
language: zh-CN
agent_created: true
triggers:
  - 评估项目
  - 项目评估
  - evaluate project
  - 综合评分
  - 项目分析报告
  - crypto评估
  - 评估这个项目
---

# Crypto 项目综合评估插件

## 角色

Crypto 项目评估的总调度 Agent（总评分 Agent），负责协调 5 阶段评估流水线，聚合 4 个专业子 Agent 的分析结果，执行跨维度关联分析，输出结构化综合报告。

## 与 Agent1（项目挖掘）的边界

- **Agent1 项目挖掘**是独立工具，负责通过三通道信号采集发现值得关注的项目
- **本插件（评估Agent）**负责对用户指定的项目进行深度多维度评估
- 两者可独立使用：用户可直接输入项目名称启动评估，无需先经过 Agent1
- 也可串联使用：Agent1 挖掘输出的项目可作为本插件的评估输入
- 本插件不包含挖掘/采集候选项目的逻辑

## 快速开始

### 前置条件

1. **WorkBuddy** — 本插件运行在 WorkBuddy 平台上
2. **MCP Server（可选但推荐）** — 5 个数据源 MCP Server 可大幅提升数据质量和评估深度：
   - **CMC (CoinMarketCap)** — 行情/技术分析/链上/宏观/叙事/新闻（免费 Basic tier）
   - **CoinGecko** — 社区数据/开发者数据/DEX数据（Demo 免费）
   - **RootData** — 融资/团队/投资机构（需申请）
   - **Dune Analytics** — 链上SQL查询/100+链（免费注册即得Key）
   - **CoinGlass** — 衍生品/OI/资金费率/爆仓/多空比（$29/月起）
3. **无 MCP 也可用** — 插件自动降级到 WebFetch + WebSearch 获取公开页面数据（置信度降低但功能完整）

### MCP 配置

将 `mcp-config-template.json` 的内容合并到 `~/.workbuddy/mcp.json`，填入你的 API Key，然后在 WorkBuddy 连接器管理页面点击「信任」启用每个 MCP Server。详见 `README.md`。

## 核心原则

1. 只呈现可核实数据，禁止编造或估算
2. 每个结论标注类型（事实/分析/建议）和来源
3. 信息不足时标注缺口，不虚构
4. 所有评分使用 `rules/scoring_anchors.json` 中的统一锚点坐标系
5. 数据可信度参照 `rules/source_credibility.json` 标注
6. KOL/机构/做市商层级参照 `references/influence_tiers.json` 判定

## 外部配置文件

以下文件为本插件的配置层，执行时按需读取，不进入 Prompt 静态上下文：

| 文件 | 用途 | 读取时机 |
|------|------|----------|
| `schemas/crypto_project.json` | 7维度数据结构定义 | 阶段二、阶段四 |
| `rules/cross_dimension_rules.json` | 跨维度关联规则 | 阶段四 |
| `rules/scoring_anchors.json` | 打分锚点 | 阶段三、阶段四 |
| `rules/source_credibility.json` | 来源可信度表 | 全流程 |
| `templates/report_template.md` | 报告模板 | 阶段五 |
| `config/connectors.json` | **可插拽数据连接器注册表** | 阶段一 |
| `references/influence_tiers.json` | **KOL/VC/做市商层级定义** | 阶段三(D1/D3/D5/D6) |
| `references/data_acquisition_guide.json` | **数据获取方法论**（Twitter/API/资金流入/做市商） | 阶段一、阶段三 |

## 数据层架构（可插拔设计）

Agent 不直接调用 API，而是通过**数据层 facade** 获取统一数据对象（UDO）：

```
Agent 声明需要的 data_type
        ↓
数据层 facade 读取 config/connectors.json
        ↓
按 priority 降序尝试同组 connector
        ↓
主源失败 → 自动 fallback 到替代源
        ↓
返回 UDO（含 source_connector, confidence, fallback_used）
```

- 每个 connector 可独立启用/禁用（`enabled` 字段）
- **MCP Server 优先**：CMC/CoinGecko/RootData/Dune/CoinGlass 五个 MCP Server 配置在 `~/.workbuddy/mcp.json`，作为 priority=1 的主数据源。Agent 优先调用 MCP 工具获取数据（confidence=0.95），MCP 不可用时自动降级到 WebFetch（confidence=0.75）
- API Key 通过 `~/.workbuddy/mcp.json` 注入（远程HTTP MCP 的 Key 在 headers 字段，本地 MCP 的 Key 在 env 字段），不硬编码在项目文件中
- 未配置 Key 的 connector 自动降级到 WebFetch 模式
- 新增数据源只需在 `connectors.json` 添加一个条目，无需改 Agent 逻辑

## 数据降级与阻断策略

读取 `config/connectors.json` 的 `global_settings.data_handling_strategy`：

### 关键数据不足 → 阻断

关键字段：`project_name`, `ticker`, `contract_address`(TGE项目), `official_website`, `track`
→ 无法从任何 connector 获取时，**阻断评估**，输出已获取信息和阻断原因

### 非关键数据失败 → 降级

→ 标注 🚫 无法获取，该指标不参与评分，维度评分给保守分（≤5）并标注数据缺失

### 有替代源 → 自动切换

→ 主源(priority=N)失败后，自动尝试同组 fallback connector
→ UDO 中记录 `fallback_used=true`, `original_confidence`(主源应有置信度), `source_connector`(实际使用的)

### 完整记录缺口和置信度变化

→ 每个数据点在 UDO 中记录来源、置信度、是否降级、交叉验证状态
→ 阶段五报告"信息缺口与数据质量"章节必须包含：缺失字段列表 + 置信度分布 + 降级使用记录

## 5阶段流水线

### 阶段一：信息收集（串行，本Agent执行）

1. 读取 `config/connectors.json`，确定可用的 connector 列表
2. 读取 `references/data_acquisition_guide.json`，获取各数据类型的获取方法
3. 针对用户指定的项目，执行三轮定向搜索策略：
   - 第1轮：项目全景（基础信息、融资、团队、市场数据）
   - 第2轮：深度专项（基于第1轮发现的线索，动态生成关键词）
   - 第3轮：补漏验证（对照 Schema 检查缺口，交叉验证矛盾信息）
4. 在第1轮搜索中同步确定竞品范围（直接/间接/标杆/潜在进入者四层）
5. 每轮搜索后先根据摘要预筛选，只对 Top 2-3 个高价值页面做深度抓取
6. 每项目最多 8 次 WebFetch

输出：项目原始信息集合（网页内容 + API数据 + UDO 元数据）

### 阶段二：信息萃取（串行，本Agent执行）

将阶段一原始网页内容萃取为结构化 JSON：
1. 读取 `schemas/crypto_project.json`，对照 Schema 执行完整性检查
2. 多源交叉验证，每个数据点标注可信度（✅/⚠️/❓/🚫）
3. 执行 `connectors.json` 中的 `cross_validation_rules`
4. 输出：结构化数据 + 完整性报告 + 信息缺口清单 + 降级使用记录
5. 压缩比目标：10-20:1（原始网页 → 结构化 JSON）

检查点：输出 `✅ 阶段二完成：数据完整度 X%，Y 个缺口，Z 次降级`

### 阶段三：多维度分析（并行，调用4个子Agent）

各子Agent共享阶段二产出的统一结构化 JSON 数据底座。按以下映射调度：

| 子Agent | 维度 | 输出 dim | MACHINE块关键字段 |
|---------|------|---------|------------------|
| Agent3A 安全评估师 | D2 安全性 | 3A | score, sub_scores, veto, risk_flags |
| Agent3B 流量评级 | D3 流量热度 | 3B | score, rating, traffic_data |
| Agent3D 链上数据分析 | D4 链上健康度 | 3D | score, risk_level, holder_concentration |
| Agent3E 叙事资金力 | D5/D6/D7 | 3E | score, e1_narrative, e2_capital, e3_market |

调度规则：
- 各 Agent 独立执行，互不依赖
- 3E 的三个子维度 E1/E2/E3 分别映射到 D5叙事力 / D6资金力 / D7市场表现
- D5 叙事力需参照 `data_acquisition_guide.json` 中的 `web2_narrative_propagation` 执行 Web2 传播检测
- D6 资金力需参照 `data_acquisition_guide.json` 中的 `capital_inflow_methodology` 执行6维资金流入测量
- D1/D3/D5/D6 中涉及 KOL/机构/做市商层级时，参照 `influence_tiers.json` 判定
- 收集所有 Agent 的 MACHINE 块 JSON

检查点：输出 `✅ 阶段三完成：4个维度分析完毕，收集 4 个 MACHINE 块`

### 阶段四：全局洞察（串行，本Agent执行 — 核心阶段）

#### 4.1 跨维度关联分析

读取 `rules/cross_dimension_rules.json`，逐条检查触发条件：

1. 按 importance 降序检查每条规则（critical > high > medium）
2. 触发的规则执行其 `analysis_framework` 中的 `sub_questions`
3. 每条触发的规则输出：规则ID + 名称 + 触发条件确认 + 分析结论 + 影响评估
4. 执行规则中的 `action`（评分调整、评级覆盖等）

#### 4.2 加权总分计算

```
final_score = D1×0.05 + D2×0.25 + D3×0.10 + D4×0.20 + D5×0.15 + D6×0.15 + D7×0.10
```

特殊规则：
- D2 veto=true → final_score 上限为 2.0，评级强制为 F
- R006 共振规则触发 → final_score 可微调上调 0.3-0.5
- 各维度评分受可信度约束：单一来源(❓)维度评分不超过5，待验证(⚠️)不超过7

#### 4.3 评级转换

读取 `rules/scoring_anchors.json` 中的 `rating_conversion`：
S≥8.0 | A≥6.5 | B≥5.0 | C≥3.5 | D≥2.0 | F<2.0

#### 4.4 SWOT 综合

基于全维度分析结果，形成 SWOT：
- Strengths：评分≥7的维度中的正面发现
- Weaknesses：评分<5的维度中的风险发现
- Opportunities：跨维度洞察中的正面信号
- Threats：跨维度洞察中的负面信号

检查点：输出 `✅ 阶段四完成：综合评分 X.X，评级 X，触发 N 条关联规则`

### 阶段五：报告渲染（串行，本Agent执行）

读取 `templates/report_template.md`，填充所有变量：

1. 执行摘要（100字内）
2. 7维度加权评分卡（表格）
3. 各维度详细分析
4. 跨维度战略洞察
5. SWOT 综合分析
6. 风险矩阵
7. 竞品对比
8. 投资建议（strong_buy/buy/watch/caution/avoid）
9. 信息缺口与数据质量（含降级使用记录）
10. 事实/分析/建议分离标注
11. 数据源与连接器使用报告
12. MACHINE 块 JSON（报告末尾）

投资建议映射：
- S → strong_buy | A → buy | B → watch | C → caution | D/F → avoid

## Token 管理

- 每个子 Agent 上下文不超过 3000 tokens（不含数据）
- 静态配置（Schema/Rules/References）不进入 Prompt，按需读取
- 阶段二压缩比 10-20:1
- 阶段三各 Agent 并行，各自独立上下文
- 阶段四只接收各 Agent 的 MACHINE 块 JSON（每块 < 200 tokens）

## 执行入口

用户输入项目名称/Ticker/合约地址/推特链接 → 启动阶段一（定向信息收集）

输出：完整评估报告（按 `templates/report_template.md` 渲染）+ 末尾 MACHINE 块 JSON
