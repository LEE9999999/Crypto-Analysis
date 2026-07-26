# Crypto 项目综合评估插件 (v1.6)

AI 驱动的 Crypto/Web3 项目多维度评估插件。5 阶段流水线，7 维度加权评分，可插拔数据层（5 个 MCP Server + WebFetch 降级），跨维度关联规则，安全一票否决。

## 核心能力

- **7 维度加权评分**：基本面(5%) + 安全(25%, 一票否决) + 流量(10%) + 链上(20%) + 叙事(15%) + 资金(15%) + 市场(10%)
- **5 阶段流水线**：信息收集 → 信息萃取 → 多维度并行分析 → 全局洞察 → 报告渲染
- **6 条跨维度关联规则**：安全否决传导、安全-链上风险共振、叙事-流量背离、资金-Smart Money 背离、融资-安全缺口、流量-链上健康共振
- **可插拔数据层**：5 个 MCP Server 优先，自动降级到 WebFetch + WebSearch
- **统一数据对象 UDO**：每个数据点标注来源、置信度、交叉验证状态、降级记录
- **影响力层级定义**：KOL 四级 + Web2 跨界领袖 + VC 五级 + 做市商三级
- **Web2 叙事传播检测**：搜索引擎热度 + 主流媒体 + AI 讨论 + 内容平台 + 视频/播客
- **资金流入 6 维测量**：交易所净流入 + 量比趋势 + 价格 alpha + 稳定币占比 + 合约 OI + Smart Money 净持仓

## 评级体系

| 评级 | 分数 | 投资建议 | 含义 |
|------|------|---------|------|
| S | ≥ 8.0 | strong_buy | 顶级项目，强烈关注 |
| A | ≥ 6.5 | buy | 优秀项目，值得关注 |
| B | ≥ 5.0 | watch | 中等项目，持续观察 |
| C | ≥ 3.5 | caution | 一般项目，谨慎对待 |
| D | ≥ 2.0 | avoid | 较弱项目，高风险 |
| F | < 2.0 | avoid | 否决或极高风险，建议回避 |

## 快速开始

### 1. 安装 Skill

将 `crypto-project-evaluator/` 目录复制到 WorkBuddy 的 skills 目录：
- 用户级（跨项目）：`~/.workbuddy/skills/crypto-project-evaluator/`
- 项目级（仅当前项目）：`.workbuddy/skills/crypto-project-evaluator/`

### 2. 配置 MCP Server（可选但推荐）

MCP Server 可大幅提升数据质量和评估深度。不配置也能用（自动降级到 WebFetch + WebSearch）。

**步骤：**

1. 打开 `mcp-config-template.json`，按需填入 API Key
2. 将 `mcpServers` 内容合并到 `~/.workbuddy/mcp.json`
3. **RootData MCP 需要额外步骤**：
   ```bash
   git clone https://github.com/jincai/rootdata-mcp-server ~/mcp-servers/rootdata-mcp-server
   ```
   然后将 mcp.json 中 rootdata 的 `--directory` 路径改为你实际的 clone 路径
4. 重启 WorkBuddy
5. 在 WorkBuddy 右上角「连接器管理」页面，对每个 MCP Server 点击「信任」

### 3. MCP Server 一览

| MCP | 类型 | 费用 | 覆盖维度 | 注册地址 |
|-----|------|------|---------|---------|
| CMC | 远程 HTTP | 免费 Basic (10K credits/月) | D1/D3/D5/D6/D7 | https://pro.coinmarketcap.com/signup |
| CoinGecko | 本地 npx | Demo 免费 / Pro 付费 | D1/D3 | https://www.coingecko.com/en/api/pricing |
| RootData | 本地 Python (uv) | 需申请 | D1/D6 | https://www.rootdata.com/Api |
| Dune | 远程 HTTP | 免费 (2500 points/月) | D4 链上 | https://dune.com/settings/api |
| CoinGlass | 远程 HTTP | $29/月起 | D6/D7 衍生品 | https://www.coinglass.com/pricing |

> **最低配置**：只配 CMC（免费）即可覆盖大部分维度。Dune（免费）补充链上数据。两者搭配零成本即可获得较好的评估质量。

### 4. 使用

在 WorkBuddy 对话中输入：
- 项目名称：`评估 kiteAI`
- 代币符号：`评估 KITE`
- 合约地址：`评估 0x9045...16be`

插件会自动执行 5 阶段流水线，输出完整评估报告。

## 文件结构

```
crypto-project-evaluator/
├── SKILL.md                          # 主入口 — 5阶段流水线 + 数据层架构 + 降级策略
├── README.md                         # 本文件
├── mcp-config-template.json          # MCP Server 配置模板（填Key后合并到 ~/.workbuddy/mcp.json）
├── schemas/
│   └── crypto_project.json           # 7维度数据结构定义 + 数据处理策略
├── rules/
│   ├── cross_dimension_rules.json    # 6条跨维度关联规则 (R001-R006)
│   ├── scoring_anchors.json          # 7维度1-10分打分锚点 + 评级转换
│   └── source_credibility.json       # 8层来源可信度表 + 降级链 + Twitter获取指南
├── config/
│   └── connectors.json               # 可插拔连接器注册表（8组, 含MCP/WebFetch/WebSearch/API）
├── references/
│   ├── influence_tiers.json          # KOL四级 + Web2跨界 + VC五级 + 做市商三级 + 检测方法
│   └── data_acquisition_guide.json   # Twitter/API/资金流入6维/Web2传播/做市商检测方法论
└── templates/
    └── report_template.md            # 评估报告模板（10章节 + MACHINE块JSON）
```

## 架构设计

### 数据层（可插拔）

Agent 不直接调 API，通过数据层 facade 按 `connectors.json` 配置自动选择连接器：

```
MCP Server (priority=1, confidence=0.95)
    ↓ 失败时降级
WebFetch 公开页面 (confidence=0.75)
    ↓ 失败时降级
WebSearch 搜索结果 (confidence=0.5)
    ↓ 全部失败
标注 🚫 无法获取，该指标不参与评分
```

8 组连接器：market_data / funding_data / social_data / onchain_data / derivatives_data / narrative_data / market_maker_data / security_data

### 评分体系

```
final_score = D1×0.05 + D2×0.25 + D3×0.10 + D4×0.20 + D5×0.15 + D6×0.15 + D7×0.10
```

- D2 安全有**一票否决权**：触发时总分上限 2.0，评级强制 F
- D5 叙事力 = crypto_native×0.6 + web2_propagation×0.4
- D6 资金力 = 6维资金流入信号均值（已TGE）/ 融资机构层级（未TGE）
- 评分受可信度约束：单一来源(❓)≤5，待验证(⚠️)≤7

## 免责声明

本插件由 AI 系统自动执行评估，基于公开信息分析，不构成投资建议。加密市场高风险，投资需谨慎。所有评分基于评估时点的可用信息，可能随时间变化。请始终进行自己的研究（DYOR）。
