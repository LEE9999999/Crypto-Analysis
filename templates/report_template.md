# {{project_name}} ({{ticker}}) — 项目综合评估报告

> 评估时间：{{evaluated_at}}
> 评估版本：v1.3
> 数据完整度：{{data_completeness}} ({{completeness_label}})
> TGE 状态：{{tge_status}}

---

## 一、执行摘要

{{executive_summary}}

### 综合评级

| 指标 | 结果 |
|------|------|
| **综合评分** | **{{final_score}} / 10** |
| **综合评级** | **{{rating}}** — {{rating_label}} |
| **投资建议** | {{recommendation}} |
| **安全否决** | {{veto_status}} |

---

## 二、8维度加权评分卡

| # | 维度 | 评分 | 权重 | 加权分 | 来源Agent | 可信度 |
|---|------|------|------|--------|----------|--------|
| D1 | 项目基本面 | {{D1_score}} | 5% | {{D1_weighted}} | 信息萃取 | {{D1_confidence}} |
| D2 | 安全性 | {{D2_score}} | 25% | {{D2_weighted}} | Agent3A | {{D2_confidence}} |
| D3 | 流量热度 | {{D3_score}} | 10% | {{D3_weighted}} | Agent3B | {{D3_confidence}} |
| D4 | 链上健康度 | {{D4_score}} | 15% | {{D4_weighted}} | Agent3D | {{D4_confidence}} |
| D5 | 叙事力 | {{D5_score}} | 15% | {{D5_weighted}} | Agent3E-E1 | {{D5_confidence}} |
| D6 | 资金力 | {{D6_score}} | 10% | {{D6_weighted}} | Agent3E-E2 | {{D6_confidence}} |
| D7 | 市场表现 | {{D7_score}} | 10% | {{D7_weighted}} | Agent3E-E3 | {{D7_confidence}} |
| D8 | 技术面分析 | {{D8_score}} | 10% | {{D8_weighted}} | Agent3E-E4 | {{D8_confidence}} |
| — | **加权总分** | — | 100% | **{{final_score}}** | — | — |

> 评分锚点参照 `rules/scoring_anchors.json`，所有评分基于统一坐标系。

### 评分雷达图（文字版）

```
           D2安全 ({{D2_score}})
               |
    D1基本面    |    D3流量
   ({{D1_score}})  |  ({{D3_score}})
      \         |         /
       \        |        /
        \       |       /
         \      |      /
          \     |     /
           \    |    /
            \   |   /
             \  |  /
              \ | /
---------------+--------------- D4链上 ({{D4_score}})
              / | \
             /  |  \
            /   |   \
           /    |    \
          /     |     \
         /      |      \
        /       |       \
       /        |        \
      /         |         \
  D7市场        |        D5叙事
 ({{D7_score}})  |  ({{D5_score}})
               |
            D6资金
           ({{D6_score}})
```

---

## 三、各维度详细分析

### D1 — 项目基本面 ({{D1_score}}/10)

**融资情况**
- 融资金额：{{funding_total}} {{funding_confidence}}
- 领投方：{{lead_investor}} {{investor_confidence}}
- 投资机构层级：{{investor_tier}}

**团队背景**
- 核心团队：{{team_info}} {{team_confidence}}
- 团队可验证性：{{team_verifiability}}

**赛道定位**
- 所属赛道：{{track}}
- 赛道竞争格局：{{track_competition}}
- 项目定位：{{project_positioning}}

**关键依据**
{{D1_evidence}}

---

### D2 — 安全性 ({{D2_score}}/10) {{veto_flag}}

| 子维度 | 评分 | 关键发现 |
|--------|------|----------|
| 背景 | {{D2_bg_score}}/10 | {{D2_bg_finding}} |
| 代码 | {{D2_code_score}}/10 | {{D2_code_finding}} |
| 合规 | {{D2_compliance_score}}/10 | {{D2_compliance_finding}} |
| 社媒 | {{D2_social_score}}/10 | {{D2_social_finding}} |

**安全否决状态**：{{veto_detail}}
**风险标记**：{{risk_flags}}
**审计情况**：{{audit_status}}

---

### D3 — 流量热度 ({{D3_score}}/10, 评级: {{D3_rating}})

| 指标 | 数值 | 来源 |
|------|------|------|
| 24h成交额 | {{volume_24h}} | {{volume_source}} |
| CMC排名 | {{cmc_rank}} | CMC |
| 官网流量 | {{web_traffic}} | Similarweb |
| RootData评分 | {{rd_score}} | RootData |
| 推特阅读量 | {{tweet_views}} | Twitter |
| KOL影响 | {{kol_impact}} | 综合评估 |

**有效参评指标数**：{{valid_indicators}}/6

---

### D4 — 链上健康度 ({{D4_score}}/10, 风险等级: {{D4_risk_level}})

| 指标 | 数值/状态 | 评估 |
|------|-----------|------|
| Top10持仓占比 | {{holder_concentration}} | {{holder_assessment}} |
| Smart Money信号 | {{smart_money_signal}} | {{smart_money_assessment}} |
| 流动性深度 | {{liquidity_depth}} | {{liquidity_assessment}} |
| 合约风险 | {{contract_risk}} | {{contract_assessment}} |

**交易行为分析**：{{trading_behavior}}
**风险信号汇总**：{{D4_risk_signals}}

---

### D5 — 叙事力 ({{D5_score}}/10, 权重15%)

**核心叙事**：{{core_narrative}}
**传播广度**：{{spread_breadth}}
**绑定强度**：{{binding_strength}}（KOL层级参照 influence_tiers.json）
**生命周期**：{{lifecycle_stage}}
**近期催化**：{{catalyst_events}}

**Web2 传播分析**（评分公式: crypto_native×0.6 + web2×0.4）
| 渠道 | 信号 | 数据 |
|------|------|------|
| 搜索引擎热度 | {{search_trends_signal}} | {{search_trends_data}} |
| 主流媒体报道 | {{mainstream_media_signal}} | {{mainstream_media_count}}家 |
| AI/Agent讨论 | {{ai_discussion_signal}} | {{ai_discussion_data}} |
| 机器人活动(反向) | {{bot_activity_signal}} | {{bot_activity_score}} |
| 内容平台 | {{content_platform_signal}} | {{content_platform_count}}篇 |
| 视频/播客 | {{video_podcast_signal}} | {{video_podcast_count}}个 |

---

### D6 — 资金力 ({{D6_score}}/10, 权重15%)

{{#if tge}}
**已TGE项目 — 资金流入6维分析**（参照 data_acquisition_guide.json）
| 维度 | 信号 | 数据 | 来源 |
|------|------|------|------|
| 交易所净流入/出 | {{d1_signal}} | {{d1_data}} | {{d1_source}} |
| 交易量趋势(7d/30d) | {{d2_signal}} | {{d2_data}} | {{d2_source}} |
| 价格vs基准(BTC/ETH) | {{d3_signal}} | alpha={{d3_alpha}} | {{d3_source}} |
| 稳定币交易对占比 | {{d4_signal}} | {{d4_data}} | {{d4_source}} |
| 合约未平仓量(OI) | {{d5_signal}} | {{d5_data}} | {{d5_source}} |
| Smart Money净持仓 | {{d6_signal}} | {{d6_data}} | {{d6_source}} |

- **资金流入综合分**：{{capital_inflow_score}}/10（{{capital_inflow_dims_available}}/6维有数据）
- **做市商**：{{market_maker_name}}（{{market_maker_tier}}，参照 influence_tiers.json）
{{else}}
**未TGE项目**
- 投资机构层级：{{investor_tier}}（参照 influence_tiers.json vc_institution_tiers）
- 融资规模：{{funding_scale}}
- 做市商情况：{{market_maker_name}}（{{market_maker_tier}}）
{{/if}}

---

### D7 — 市场表现 ({{D7_score}}/10, 权重10%)

{{#if meme}}
**Meme类项目 — 链上数据健康度**
- Holder分散度：{{holder_distribution}}
- 交易自然度：{{trading_naturalness}}
- 链上综合健康度：{{onchain_health_summary}}
{{else}}
**非Meme类项目 — 产品+用户+合作**
- 产品状态：{{product_status}}
- 用户指标：{{user_metrics}}
- 重要合作：{{partnerships}}
{{/if}}

---

### D8 — 技术面分析 ({{D8_score}}/10, 权重10%)

**数据来源**：{{D8_data_source}} ({{D8_data_points}}根K线)
**交叉验证**：{{D8_cross_validation}}

**8个Tier 1核心指标**
| # | 指标 | 数值 | 信号 | 解读 |
|---|------|------|------|------|
| 1 | RSI(14) | {{rsi_value}} | {{rsi_signal}} | {{rsi_interpretation}} |
| 2 | MACD(12,26,9) | DIF={{macd_line}} DEA={{signal_line}} Hist={{histogram}} | {{macd_signal}} | {{macd_interpretation}} |
| 3 | EMA(5,20) | EMA5={{ema5}} EMA20={{ema20}} | {{ema_signal}} | {{ema_interpretation}} |
| 4 | Bollinger(20,2) | U={{bb_upper}} M={{bb_middle}} L={{bb_lower}} W={{bb_width}}% | {{bb_signal}} | {{bb_interpretation}} |
| 5 | SuperTrend(10,3) | {{st_value}} | {{st_direction}} | {{st_interpretation}} |
| 6 | KDJ(9,3,3) | K={{kdj_k}} D={{kdj_d}} J={{kdj_j}} | {{kdj_signal}} | {{kdj_interpretation}} |
| 7 | ATR(14) | {{atr_value}} ({{atr_pct}}%) | {{atr_level}} | {{atr_interpretation}} |
| 8 | OBV/VWAP | OBV={{obv_value}} ({{obv_trend}}) VWAP={{vwap_value}} | {{obv_signal}} | {{obv_interpretation}} |

**多空信号汇总**：{{bull_count}}看涨 / {{bear_count}}看跌 / {{neutral_count}}中性 (共{{total_directional}}个方向性指标)
**技术评分推理**：{{D8_score_reasoning}}
{{#if D8_volume_missing}}
> ⚠️ Volume数据不可用，OBV/VWAP未参与计算，方向性指标从8个降为{{total_directional}}个
{{/if}}

---

## 四、跨维度战略洞察

{{cross_dimension_insights}}

> 以下洞察基于 `rules/cross_dimension_rules.json` 中的关联规则自动触发。

### 触发的关联规则

{{#each triggered_rules}}
#### {{this.id}} — {{this.name}} [{{this.importance}}]
- **触发条件**：{{this.trigger_condition}}
- **分析结论**：{{this.conclusion}}
- **影响评估**：{{this.impact}}
{{/each}}

{{#if no_rules_triggered}}
本轮评估未触发跨维度关联规则。
{{/if}}

---

## 五、SWOT 综合分析

### Strengths（优势）
{{#each swot.strengths}}
- {{this}}
{{/each}}

### Weaknesses（劣势）
{{#each swot.weaknesses}}
- {{this}}
{{/each}}

### Opportunities（机会）
{{#each swot.opportunities}}
- {{this}}
{{/each}}

### Threats（威胁）
{{#each swot.threats}}
- {{this}}
{{/each}}

---

## 六、风险矩阵

| 风险类别 | 风险等级 | 概率 | 影响 | 缓解措施 |
|----------|---------|------|------|----------|
| 安全风险 | {{security_risk_level}} | {{security_probability}} | {{security_impact}} | {{security_mitigation}} |
| 链上风险 | {{onchain_risk_level}} | {{onchain_probability}} | {{onchain_impact}} | {{onchain_mitigation}} |
| 流动性风险 | {{liquidity_risk_level}} | {{liquidity_probability}} | {{liquidity_impact}} | {{liquidity_mitigation}} |
| 叙事风险 | {{narrative_risk_level}} | {{narrative_probability}} | {{narrative_impact}} | {{narrative_mitigation}} |
| 合规风险 | {{compliance_risk_level}} | {{compliance_probability}} | {{compliance_impact}} | {{compliance_mitigation}} |

---

## 七、竞品对比

| 维度 | {{project_name}} | {{competitor_1}} | {{competitor_2}} | {{competitor_3}} |
|------|-----------------|------------------|------------------|------------------|
| 综合评分 | {{final_score}} | {{comp1_score}} | {{comp2_score}} | {{comp3_score}} |
| 安全性 | {{D2_score}} | {{comp1_D2}} | {{comp2_D2}} | {{comp3_D2}} |
| 流量热度 | {{D3_score}} | {{comp1_D3}} | {{comp2_D3}} | {{comp3_D3}} |
| 链上健康 | {{D4_score}} | {{comp1_D4}} | {{comp2_D4}} | {{comp3_D4}} |
| 叙事力 | {{D5_score}} | {{comp1_D5}} | {{comp2_D5}} | {{comp3_D5}} |
| 资金力 | {{D6_score}} | {{comp1_D6}} | {{comp2_D6}} | {{comp3_D6}} |
| 市场表现 | {{D7_score}} | {{comp1_D7}} | {{comp2_D7}} | {{comp3_D7}} |
| 技术面 | {{D8_score}} | {{comp1_D8}} | {{comp2_D8}} | {{comp3_D8}} |

**竞争优势**：{{competitive_advantage}}
**竞争劣势**：{{competitive_disadvantage}}

---

## 八、投资建议

### 建议评级：{{recommendation}}

{{recommendation_detail}}

### 建议逻辑

| 信号方向 | 具体内容 |
|----------|----------|
| 看多信号 | {{bull_signals}} |
| 看空信号 | {{bear_signals}} |
| 中性信号 | {{neutral_signals}} |

### 关注节点
{{#each watch_points}}
- {{this}}
{{/each}}

---

## 九、信息缺口与数据质量

### 数据完整度

| 维度 | 完整度 | 缺失字段 |
|------|--------|----------|
| D1 基本面 | {{D1_completeness}} | {{D1_missing}} |
| D2 安全 | {{D2_completeness}} | {{D2_missing}} |
| D3 流量 | {{D3_completeness}} | {{D3_missing}} |
| D4 链上 | {{D4_completeness}} | {{D4_missing}} |
| D5 叙事 | {{D5_completeness}} | {{D5_missing}} |
| D6 资金 | {{D6_completeness}} | {{D6_missing}} |
| D7 市场 | {{D7_completeness}} | {{D7_missing}} |
| D8 技术面 | {{D8_completeness}} | {{D8_missing}} |

### 信息缺口清单
{{#each data_gaps}}
- **{{this.dimension}}**：{{this.gap_description}} → 影响：{{this.impact_on_scoring}}
{{/each}}

### 可信度分布
- ✅ 已确认：{{confirmed_count}} 个数据点
- ⚠️ 待验证：{{partial_count}} 个数据点
- ❓ 单一来源：{{single_count}} 个数据点
- 🚫 无法获取：{{unavailable_count}} 个数据点

### 数据源与连接器使用报告

| 数据组 | 主源 | 实际使用源 | 降级? | 置信度变化 |
|--------|------|-----------|-------|-----------|
| Market data | {{market_primary}} | {{market_actual}} | {{market_fallback}} | {{market_confidence_change}} |
| Funding data | {{funding_primary}} | {{funding_actual}} | {{funding_fallback}} | {{funding_confidence_change}} |
| Social data | {{social_primary}} | {{social_actual}} | {{social_fallback}} | {{social_confidence_change}} |
| Onchain data | {{onchain_primary}} | {{onchain_actual}} | {{onchain_fallback}} | {{onchain_confidence_change}} |
| Security data | {{security_primary}} | {{security_actual}} | {{security_fallback}} | {{security_confidence_change}} |
| Narrative data | {{narrative_primary}} | {{narrative_actual}} | {{narrative_fallback}} | {{narrative_confidence_change}} |
| MM data | {{mm_primary}} | {{mm_actual}} | {{mm_fallback}} | {{mm_confidence_change}} |
| Technical data | {{tech_primary}} | {{tech_actual}} | {{tech_fallback}} | {{tech_confidence_change}} |

> 连接器配置参照 `config/connectors.json`，数据获取方法参照 `references/data_acquisition_guide.json`

---

## 十、事实/分析/建议分离标注

{{#each conclusions}}
### {{this.title}}
- **类型**：{{this.type}} (事实/分析/建议)
- **内容**：{{this.content}}
- **来源**：{{this.source}}
- **可信度**：{{this.confidence}}
{{/each}}

---

## MACHINE 块（报告最末尾，严格 JSON）

```json
{
  "dim": "TOTAL",
  "project_name": "{{project_name}}",
  "ticker": "{{ticker}}",
  "final_score": {{final_score_raw}},
  "rating": "{{rating}}",
  "dimension_scores": {
    "D1_fundamentals": {{D1_raw}},
    "D2_security": {{D2_raw}},
    "D3_traffic": {{D3_raw}},
    "D4_onchain": {{D4_raw}},
    "D5_narrative": {{D5_raw}},
    "D6_capital": {{D6_raw}},
    "D7_market": {{D7_raw}},
    "D8_technical": {{D8_raw}}
  },
  "weights": {
    "D1_fundamentals": 0.05,
    "D2_security": 0.25,
    "D3_traffic": 0.10,
    "D4_onchain": 0.15,
    "D5_narrative": 0.15,
    "D6_capital": 0.10,
    "D7_market": 0.10,
    "D8_technical": 0.10
  },
  "veto_triggered": {{veto_triggered}},
  "veto_source": "{{veto_source}}",
  "cross_dimension_insights": {{cross_dimension_insights_raw}},
  "swot": {
    "strengths": {{swot_strengths_raw}},
    "weaknesses": {{swot_weaknesses_raw}},
    "opportunities": {{swot_opportunities_raw}},
    "threats": {{swot_threats_raw}}
  },
  "recommendation": "{{recommendation_code}}",
  "data_completeness": {{data_completeness_raw}},
  "one_line": "≤100字总结结论，含评级、关键风险、核心建议"
}
```

---

> **免责声明**：本报告由AI系统自动生成，基于公开信息分析，不构成投资建议。加密市场高风险，投资需谨慎。所有评分基于评估时点的可用信息，可能随时间变化。请始终进行自己的研究（DYOR）。
