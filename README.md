# Crypto Project Evaluator

**AI 驱动的 Crypto/Web3 项目多维度评估插件（v2.0）**

8 维度加权评分 · 5 阶段流水线 · 5 个 MCP Server 数据层 · 8 个 Tier 1 技术指标本地计算 · 跨维度关联洞察 · 安全一票否决

---

## 概览

本插件为 [WorkBuddy](https://www.codebuddy.cn/)（AI 助手平台）设计，对任意 Crypto/Web3 项目执行结构化深度评估。通过 5 个官方 MCP Server 获取多源数据，经 5 阶段流水线处理后，输出 8 维度加权评分报告，含跨维度战略洞察与风险预警。

### 核心能力

| 能力 | 说明 |
|------|------|
| **8 维度加权评分** | 基本面(5%) + 安全(25%,否决) + 流量(10%) + 链上(15%) + 叙事(15%) + 资金(10%) + 市场(10%) + 技术面(10%) |
| **D8 技术面分析** | RSI / MACD / EMA / Bollinger / SuperTrend / KDJ / ATR / OBV-VWAP — 本地 Python `ta` 库计算 |
| **5 阶段流水线** | 定向信息收集 → 信息萃取 → 多维度并行分析 → 全局洞察 → 报告渲染 |
| **5 个 MCP Server** | CoinMarketCap / CoinGecko / RootData / Dune / CoinGlass — 可插拔，自动降级 |
| **8 条跨维度规则** | 安全否决传导、技术-资金背离、技术-市场共振等战略级关联分析 |
| **可插拔数据层** | 9 组连接器，MCP 优先 → WebFetch → WebSearch，带置信度标注与降级记录 |
| **影响力层级** | KOL 四级 + Web2 跨界领袖 + VC 五级 + 做市商三级 |
| **Web2 叙事检测** | 搜索引擎热度 + 主流媒体 + AI 讨论 + 内容平台 + 视频播客 |
| **资金流入 6 维** | 交易所净流入 + 量比趋势 + 价格 alpha + 稳定币占比 + 合约 OI + Smart Money |

---

## 评分体系

### 8 维度加权评分卡

```
总分 = D1×5% + D2×25% + D3×10% + D4×15% + D5×15% + D6×10% + D7×10% + D8×10% = 100%
```

| 维度 | 名称 | 权重 | 分析者 | 核心指标 |
|------|------|------|--------|---------|
| D1 | 项目基本面 | 5% | 信息萃取 | 团队/赛道/TGE状态/代币经济 |
| D2 | 安全性 | 25% | Agent3A | 合约审计/蜜罐检测/持仓集中度/权限控制 |
| D3 | 流量热度 | 10% | Agent3B | 社媒粉丝/活跃度/Web流量/Twitter互动 |
| D4 | 链上健康度 | 15% | Agent3D | 持仓分布/Smart Money/流动性/链上交易 |
| D5 | 叙事力 | 15% | Agent3E-E1 | Crypto native热度 + Web2传播6维 |
| D6 | 资金力 | 10% | Agent3E-E2 | 6维资金流入信号 / 融资机构层级 |
| D7 | 市场表现 | 10% | Agent3E-E3 | 价格走势/市值排名/交易量/波动率 |
| D8 | 技术面 | 10% | Agent3E-E4 | 8个Tier 1技术指标多空信号 + ATR波动率修正 |

> **D2 安全一票否决**：触发否决条件时，总分上限 2.0，评级强制 F。

### 评级标准

| 评级 | 分数 | 建议 | 含义 |
|------|------|------|------|
| S | >= 8.0 | strong_buy | 顶级项目，强烈关注 |
| A | >= 6.5 | buy | 优秀项目，值得关注 |
| B | >= 5.0 | watch | 中等项目，持续观察 |
| C | >= 3.5 | caution | 一般项目，谨慎对待 |
| D | >= 2.0 | avoid | 较弱项目，高风险 |
| F | < 2.0 | avoid | 否决或极高风险，回避 |

---

## D8 技术面分析（v2.0 新增）

### 数据流

```
CoinGecko MCP (OHLCV K线)  →  Python ta 库本地计算  →  8个技术指标  →  评分
                                    ↓                        ↓
                              CMC MCP 交叉验证         7方向性看多/看空计数
                              (覆盖4/8指标)            + ATR波动率修正
```

### 8 个 Tier 1 核心指标

| 指标 | 参数 | 类型 | 信号 |
|------|------|------|------|
| RSI | (14) | 方向性 | >70 超买看跌 / <30 超卖看涨 / 30-70 中性 |
| MACD | (12,26,9) | 方向性 | 金叉看涨 / 死叉看跌 / 柱状图趋势 |
| EMA | (5,20) | 方向性 | EMA5>EMA20 看涨 / EMA5<EMA20 看跌 |
| Bollinger Bands | (20,2) | 方向性 | 触上轨看涨 / 触下轨看跌 / 收口待变 |
| SuperTrend | (10,3) | 方向性 | 价格在线上方看涨 / 下方看跌 |
| KDJ | (9,3,3) | 方向性 | 金叉看涨 / 死叉看跌 / 超买超卖 |
| ATR | (14) | 波动率 | 高波动修正-0.5 / 低波动修正+0.2 |
| OBV/VWAP | - | 方向性 | OBV上升+VWAP上方看涨 / 反之看跌 |

### 评分逻辑

```
看多比例 = 看多指标数 / 方向性指标总数(7 或 6)

>=85%  → 9-10 分 (强烈看多)
60-85% → 7-9 分  (偏多)
40-60% → 5-7 分  (中性)
20-40% → 3-5 分  (偏空)
<20%   → 1-3 分  (强烈看空)

ATR 修正: 高波动 -0.5 / 低波动 +0.2
```

> **无成交量降级**：当 OHLCV 数据中 Volume 缺失时，OBV/VWAP 自动排除，方向性指标从 7 降为 6，评分逻辑自适应。

### 跨维度关联规则（新增 R007/R008）

| 规则 | 重要性 | 触发条件 | 效果 |
|------|--------|---------|------|
| R007 | HIGH | D8>=7 且 D6<4 | 技术-资金背离，价格可能被操纵，触发风险预警 |
| R008 | MEDIUM | D8>=7 且 D7>=7 | 技术-市场共振，趋势可信度增强，总分+0.3 |

---

## 安装

### 前置要求

- [WorkBuddy](https://www.codebuddy.cn/) 桌面客户端
- Python 3.10+（D8 技术面计算需要）
- pip install ta pandas（D8 技术面计算依赖）

### 第 1 步：安装 Skill

将 `crypto-project-evaluator/` 目录复制到 WorkBuddy 的 skills 目录：

```bash
# 用户级（跨项目可用，推荐）
cp -r crypto-project-evaluator/ ~/.workbuddy/skills/crypto-project-evaluator/

# 或项目级（仅当前项目）
cp -r crypto-project-evaluator/ .workbuddy/skills/crypto-project-evaluator/
```

### 第 2 步：配置 MCP Server（可选但推荐）

MCP Server 可大幅提升数据质量和评估深度。不配置也能用（自动降级到 WebFetch + WebSearch）。

**2a. 安装 D8 计算依赖：**

```bash
pip install ta pandas
```

**2b. 配置 MCP Server：**

1. 打开 `mcp-config-template.json`，将所有 `YOUR_*_KEY` 替换为真实 API Key
2. 将 `mcpServers` 内容合并到 `~/.workbuddy/mcp.json`
3. **RootData MCP 需要额外步骤**：
   ```bash
   git clone https://github.com/jincai/rootdata-mcp-server ~/mcp-servers/rootdata-mcp-server
   ```
   然后将 mcp.json 中 rootdata 的 `--directory` 路径改为你实际的 clone 路径
4. 重启 WorkBuddy
5. 在 WorkBuddy 右上角「连接器管理」页面，对每个 MCP Server 点击「信任」

### MCP Server 一览

| MCP | 类型 | 费用 | 覆盖维度 | 注册地址 |
|-----|------|------|---------|---------|
| CoinMarketCap | 远程 HTTP | 免费 Basic (10K credits/月) | D1/D3/D5/D6/D7/D8 | https://pro.coinmarketcap.com/signup |
| CoinGecko | 本地 npx | Demo 免费 / Pro 付费 | D1/D3/D8(OHLCV) | https://www.coingecko.com/en/api/pricing |
| RootData | 本地 Python (uv) | 需申请 | D1/D6 | https://www.rootdata.com/Api |
| Dune | 远程 HTTP | 免费 (2500 points/月) | D4 链上 | https://dune.com/settings/api |
| CoinGlass | 远程 HTTP | $29/月起 | D6/D7 衍生品 | https://www.coinglass.com/pricing |

> **最低配置**：只配 CoinMarketCap（免费）即可覆盖大部分维度。Dune（免费）补充链上数据。两者搭配零成本即可获得较好的评估质量。

---

## 使用

在 WorkBuddy 对话中输入：

```
评估 kiteAI
评估 KITE
评估 0x9045...16be
```

插件会自动执行 5 阶段流水线，输出完整评估报告（Markdown 格式），包含：

- 8 维度加权评分卡
- 各维度详细分析（数据来源 + 置信度标注）
- 跨维度关联洞察（风险预警 / 趋势增强信号）
- 连接器使用报告（数据来源 + 降级记录）
- 竞品对比表
- 投资建议与风险提示

---

## 架构

### 5 阶段流水线

```
阶段一: 定向信息收集
  ├── 读取 connectors.json → 选择连接器 → 获取原始数据
  └── 输出: 统一数据对象 UDO (含来源/置信度/交叉验证状态)

阶段二: 信息萃取
  ├── 从 UDO 提取结构化项目信息
  └── 输出: D1 基本面数据 + 阻断检查(缺关键字段则停止)

阶段三: 多维度并行分析
  ├── Agent3A → D2 安全性 (25%, 有否决权)
  ├── Agent3B → D3 流量热度 (10%)
  ├── Agent3D → D4 链上健康度 (15%)
  ├── Agent3E-E1 → D5 叙事力 (15%)
  ├── Agent3E-E2 → D6 资金力 (10%)
  ├── Agent3E-E3 → D7 市场表现 (10%)
  └── Agent3E-E4 → D8 技术面 (10%)  ← v2.0 新增
  └── 输出: 5 个 MACHINE 块 (各维度评分 + 风险标记)

阶段四: 全局洞察
  ├── 执行 8 条跨维度关联规则 (按 importance 降序)
  ├── 安全否决检查 (D2 veto → 总分上限 2.0, 评级 F)
  └── 输出: 最终加权总分 + 评级 + 战略洞察

阶段五: 报告渲染
  └── 按 report_template.md 输出结构化 Markdown 报告
```

### 可插拔数据层

```
Agent 声明需要的 data_type
        ↓
数据层 facade 读取 config/connectors.json
        ↓
选择 priority 最高的可用连接器
        ↓
MCP Server (priority=1, confidence=0.95)
    ↓ 失败时降级
WebFetch 公开页面 (confidence=0.75)
    ↓ 失败时降级
WebSearch 搜索结果 (confidence=0.5)
    ↓ 全部失败
标注 🚫 无法获取，该指标不参与评分
```

**9 组连接器**：market_data / funding_data / social_data / onchain_data / derivatives_data / narrative_data / market_maker_data / security_data / technical_data

---

## 文件结构

```
crypto-project-evaluator/
├── SKILL.md                              # 主入口 — 5阶段流水线 + 数据层架构 + 降级策略
├── README.md                             # 本文件
├── mcp-config-template.json              # MCP Server 配置模板（填Key后合并到 ~/.workbuddy/mcp.json）
├── push-to-github.sh                     # 一键推送到 GitHub 脚本
├── schemas/
│   └── crypto_project.json               # 8维度数据结构定义 + 数据处理策略
├── rules/
│   ├── cross_dimension_rules.json        # 8条跨维度关联规则 (R001-R008)
│   ├── scoring_anchors.json              # 8维度1-10分打分锚点 + 评级转换
│   └── source_credibility.json           # 来源可信度表 + 降级链 + Twitter获取指南
├── config/
│   └── connectors.json                   # 可插拔连接器注册表（9组, 含MCP/WebFetch/WebSearch/API）
├── references/
│   ├── influence_tiers.json              # KOL四级 + Web2跨界 + VC五级 + 做市商三级
│   ├── data_acquisition_guide.json       # Twitter/API/资金流入6维/Web2传播/做市商检测方法论
│   └── technical_indicators_guide.json  # D8技术指标解读 + 数据获取 + 评分方法
├── scripts/
│   └── technical_analysis.py             # D8本地计算引擎（8个Tier 1指标, ta库）
└── templates/
    └── report_template.md                # 评估报告模板（8维度评分卡 + D8技术面段落 + 连接器报告）
```

---

## 安全与隐私

- **API Key 永不泄露**：所有 API Key 写在 `~/.workbuddy/mcp.json`（用户目录，不在项目仓库内），`mcp-config-template.json` 中仅含 `YOUR_*_KEY` 占位符
- **无硬编码凭据**：`connectors.json` 只记录连接器配置和认证方式（env 变量名 / header 名），不存储实际 Key 值
- **报告不含敏感信息**：评估报告中所有数据来源标注为类型（MCP / WebFetch / WebSearch），不暴露 Key
- **`.gitignore` 已配置**：`*.env`、`mcp.json`、`secrets.json` 等敏感文件不会被提交

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 运行平台 | WorkBuddy AI 助手 |
| MCP 协议 | Model Context Protocol (远程 HTTP + 本地 npx/uv) |
| D8 计算 | Python 3.10+ / `ta` 库 v0.11.0 / pandas |
| 数据格式 | JSON Schema (数据结构) + Markdown (报告) |
| 语言 | 中文 (zh-CN) |

---

## 免责声明

本插件由 AI 系统自动执行评估，基于公开信息分析，不构成投资建议。加密市场高风险，投资需谨慎。所有评分基于评估时点的可用信息，可能随时间变化。请始终进行自己的研究（DYOR - Do Your Own Research）。

## License

MIT
