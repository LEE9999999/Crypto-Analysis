#!/bin/bash
#
# Crypto-Analysis (crypto-project-evaluator) 更新脚本
#
# 使用方法:
#   bash push-to-github.sh "your commit message"
#   如果不带参数, 使用时间戳作为默认提交信息
#

set -e
cd "$(dirname "$0")"

echo "========================================="
echo "  Crypto-Analysis -> GitHub Update"
echo "========================================="
echo ""

# Git config
git config user.name "LEE9999999" 2>/dev/null
git config user.email "LEE9999999@users.noreply.github.com" 2>/dev/null

# Commit message
MSG="${1:-Update: $(date '+%Y-%m-%d %H:%M')}"

# Show what changed
echo "=== Current status ==="
git status --short
echo ""

if [ -z "$(git status --short)" ]; then
    echo "No changes to commit. Working tree is clean."
    exit 0
fi

# Add all files
git add -A
echo "=== Staged files ==="
git diff --cached --stat
echo ""

# Commit
git commit -m "$MSG"
echo ""

# Push
git push origin main
echo ""

echo "========================================="
echo "  Push complete!"
echo "  Repo: https://github.com/LEE9999999/Crypto-Analysis"
echo "========================================="
