#!/bin/bash
#
# 一键推送 crypto-project-evaluator 到 GitHub
#
# 使用方法:
#   1. 在 GitHub 创建一个空仓库 (不要勾选 README/.gitignore/license)
#   2. 复制仓库地址, 例如: https://github.com/yourname/crypto-project-evaluator.git
#   3. 运行: bash push-to-github.sh
#   4. 按提示粘贴仓库地址, 输入你的 GitHub 用户名和邮箱
#
# 如果提示需要密码, 使用 GitHub Personal Access Token (PAT) 作为密码:
#   生成地址: https://github.com/settings/tokens/new?scopes=repo
#

set -e

echo "========================================="
echo "  Crypto Project Evaluator v2.0 -> GitHub"
echo "========================================="
echo ""

# 1. 收集信息
read -p "GitHub 仓库地址 (https://github.com/xxx/xxx.git): " REPO_URL
read -p "你的 GitHub 用户名: " GIT_USER
read -p "你的 GitHub 邮箱: " GIT_EMAIL

# 2. 配置 git
git config user.name "$GIT_USER"
git config user.email "$GIT_EMAIL"

# 3. 添加文件并提交
git add -A
git commit -m "v2.0: Crypto Project Evaluator - 8-dimension analysis

- 8-dimension weighted scoring (D1-D8) for Crypto/Web3 projects
- D8 technical analysis: 8 Tier 1 indicators (RSI/MACD/EMA/Bollinger/SuperTrend/KDJ/ATR/OBV-VWAP)
- Local Python calculation engine using ta library
- 5-phase pipeline: collection -> extraction -> analysis -> insight -> report
- 5 MCP server integrations (CMC/CoinGecko/RootData/Dune/CoinGlass)
- 9 connector groups with pluggable architecture + graceful degradation
- 8 cross-dimension correlation rules with safety veto
- KOL/VC/MarketMaker influence tier definitions
- D5 Web2 narrative propagation detection
- D6 6-dimensional capital inflow measurement"

echo ""
echo "Commit created. Now pushing to GitHub..."
echo "(如果提示输入密码, 请使用 GitHub Personal Access Token)"
echo "生成 Token: https://github.com/settings/tokens/new?scopes=repo"
echo ""

# 4. 推送
# 如果已有 origin 则更新地址，否则添加
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi
git push -u origin main

echo ""
echo "========================================="
echo "  Push 成功!"
echo "  仓库地址: $REPO_URL"
echo "========================================="
