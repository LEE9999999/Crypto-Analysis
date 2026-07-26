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
echo "  Crypto Project Evaluator -> GitHub"
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
git commit -m "Initial release: Crypto Project Evaluator v1.6

- 7-dimension weighted scoring (D1-D7) for Crypto/Web3 projects
- 5-phase pipeline: collection -> extraction -> analysis -> insight -> report
- 5 MCP server integrations (CMC/CoinGecko/RootData/Dune/CoinGlass)
- 8 connector groups with pluggable architecture + graceful degradation
- 6 cross-dimension correlation rules with safety veto
- KOL/VC/MarketMaker influence tier definitions
- Tested with real evaluation (Kite AI, rating B 5.38/10)"

echo ""
echo "Commit created. Now pushing to GitHub..."
echo "(如果提示输入密码, 请使用 GitHub Personal Access Token)"
echo "生成 Token: https://github.com/settings/tokens/new?scopes=repo"
echo ""

# 4. 推送
git remote add origin "$REPO_URL"
git push -u origin main

echo ""
echo "========================================="
echo "  Push 成功!"
echo "  仓库地址: $REPO_URL"
echo "========================================="
