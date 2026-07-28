# GitHub 上传指南

## 前置安全确认

以下检查已全部通过：

- [x] 无真实 API Key（全部使用 `YOUR_*_KEY` 占位符）
- [x] 无用户路径（`/Users/ken/...` 已替换为 `~/...` 或 `python3`）
- [x] 无个人邮箱或用户名泄露
- [x] `.gitignore` 已配置（排除 `*.env`、`mcp.json`、`secrets.json`）
- [x] `mcp-config-template.json` 仅含占位符，无真实凭据

## 上传步骤

### 方法一：一键脚本（推荐）

```bash
cd crypto-project-evaluator
bash push-to-github.sh
```

按提示输入：
1. GitHub 仓库地址（如 `https://github.com/yourname/crypto-project-evaluator.git`）
2. 你的 GitHub 用户名
3. 你的 GitHub 邮箱

如果提示输入密码，使用 GitHub Personal Access Token (PAT) 作为密码：
- 生成地址：https://github.com/settings/tokens/new?scopes=repo

### 方法二：手动 Git 命令

```bash
# 1. 进入分发目录
cd crypto-project-evaluator

# 2. 初始化 git（如果 .git 已存在则跳过）
git init

# 3. 配置你的 GitHub 身份（首次需要）
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub邮箱"

# 4. 添加所有文件
git add -A

# 5. 提交
git commit -m "v2.0: Crypto Project Evaluator - 8-dimension analysis

- 8-dimension weighted scoring (D1-D8) for Crypto/Web3 projects
- D8 technical analysis: 8 Tier 1 indicators (RSI/MACD/EMA/Bollinger/SuperTrend/KDJ/ATR/OBV-VWAP)
- Local Python calculation engine using ta library
- 5-phase pipeline: collection -> extraction -> analysis -> insight -> report
- 5 MCP server integrations (CMC/CoinGecko/RootData/Dune/CoinGlass)
- 9 connector groups with pluggable architecture + graceful degradation
- 8 cross-dimension correlation rules with safety veto"

# 6. 添加远程仓库（替换为你的地址）
git remote add origin https://github.com/yourname/crypto-project-evaluator.git

# 7. 推送
git push -u origin main
```

### 方法三：GitHub Desktop

1. 打开 GitHub Desktop
2. File → Add Local Repository → 选择 `crypto-project-evaluator/` 目录
3. 填写 commit message → Commit
4. Publish repository → 选择 GitHub 账号 → Publish

## 如果是更新已有仓库

```bash
cd crypto-project-evaluator

# 如果之前已经推过，remote origin 已存在
git add -A
git commit -m "v2.0: add D8 technical analysis dimension"
git push origin main
```

## 上传后验证

1. 打开你的 GitHub 仓库页面
2. 确认以下文件都在：
   - `SKILL.md`（主入口）
   - `README.md`（项目说明）
   - `mcp-config-template.json`（MCP 配置模板）
   - `schemas/crypto_project.json`
   - `rules/` 下 3 个 JSON
   - `config/connectors.json`
   - `references/` 下 3 个 JSON
   - `scripts/technical_analysis.py`
   - `templates/report_template.md`
3. 点击 `mcp-config-template.json` 确认只含 `YOUR_*_KEY` 占位符
4. 确认无 `/Users/` 开头的路径

## 安全注意事项

- **永远不要**在仓库中提交 `~/.workbuddy/mcp.json`（含真实 API Key）
- **永远不要**在代码中硬编码 API Key
- 如果误提交了 Key，立即在 GitHub 删除该 commit 或 force push 覆盖，然后去对应平台 revoke 并重新生成 Key
- 建议在 GitHub 仓库 Settings → Security → Secret scanning 开启
