#!/usr/bin/env python3
"""
Unit tests for technical_analysis.py (v2.0.3)

覆盖：
1. 上涨/下跌趋势数据的 SuperTrend 方向与评分方向
2. 中性信号处理（v2.0.3 修复的核心 bug：
   1 bullish + 6 neutral 不应被判为"强烈看空"）
3. 全部中性 → 中性分 5.5 附近
4. 无成交量数据 → OBV/VWAP 跳过，评分仍自适应
5. 数据不足 30 根 → 报错退出

运行：python scripts/test_technical_analysis.py
依赖：pip install ta pandas numpy
"""

import json
import math
import random
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "technical_analysis.py"

sys.path.insert(0, str(Path(__file__).parent))
from technical_analysis import (  # noqa: E402
    calculate_indicators,
    calculate_supertrend,
    calculate_technical_score,
)
import pandas as pd  # noqa: E402

PASS, FAIL = 0, 0


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name}  {detail}")


def make_ohlcv(closes, volumes=None):
    """从收盘价序列构造最小 OHLCV DataFrame。"""
    n = len(closes)
    data = {
        "open": [c * 0.99 for c in closes],
        "high": [c * 1.02 for c in closes],
        "low": [c * 0.98 for c in closes],
        "close": closes,
    }
    if volumes is not None:
        data["volume"] = volumes
    return pd.DataFrame(data)


def trend_closes(start, pct_per_day, n=60, vol=0.02, seed=42):
    """带噪声的随机漫步序列（固定 seed 保证可复现）。
    纯平滑趋势会让 RSI/KDJ 等震荡指标钉在极端值（持续阴跌=超卖=bullish），
    加噪声后才接近真实行情。"""
    rng = random.Random(seed)
    prices = [start]
    for _ in range(n - 1):
        change = pct_per_day + rng.gauss(0, vol)
        prices.append(prices[-1] * (1 + change))
    return prices


print("== 1. SuperTrend 方向 ==")
up_df = make_ohlcv(trend_closes(100, 0.012))
_, up_dir = calculate_supertrend(up_df)
check("上涨趋势 → direction=1", up_dir == 1, f"got {up_dir}")

down_df = make_ohlcv(trend_closes(100, -0.012))
_, down_dir = calculate_supertrend(down_df)
check("下跌趋势 → direction=-1", down_dir == -1, f"got {down_dir}")

print("== 2. 评分方向 ==")
# 注意：RSI/KDJ/BB 是均值回归指标，下跌末端超卖会投 bullish（"潜在反弹"），
# 与趋势指标（EMA/SuperTrend/MACD）分歧是设计内行为。
# 因此本测试断言相对关系和边界，而非绝对极端分。
up_ind = calculate_indicators(up_df)
up_score, _ = calculate_technical_score(up_ind)
check("上涨趋势评分 > 5.5", up_score > 5.5, f"got {up_score}")

down_ind = calculate_indicators(down_df)
down_score, _ = calculate_technical_score(down_ind)
check("下跌趋势评分 < 上涨趋势评分", down_score < up_score, f"down={down_score} up={up_score}")
check("下跌趋势评分不进入看多区间 (<7.0)", down_score < 7.0, f"got {down_score}")

print("== 3. 中性信号处理（v2.0.3 核心修复）==")
# 旧 bug：1 bullish + 6 neutral → bull_ratio=1/7≈0.167 → 1-3 分"强烈看空"
fake = {"atr": {"volatility_level": "moderate_volatility"}}
fake["rsi"] = {"value": 50, "signal": "bullish"}
for k in ["macd", "ema", "bollinger", "supertrend", "kdj", "obv"]:
    fake[k] = {"value": 1, "signal": "neutral"}
score, info = calculate_technical_score(fake)
check(
    "1 bullish + 6 neutral → 中性偏上 (5.5-7.0)，不再误判强烈看空",
    5.5 <= score <= 7.0,
    f"got {score}",
)

fake_all_neutral = {"atr": {"volatility_level": "moderate_volatility"}}
for k in ["rsi", "macd", "ema", "bollinger", "supertrend", "kdj", "obv"]:
    fake_all_neutral[k] = {"value": 1, "signal": "neutral"}
score2, _ = calculate_technical_score(fake_all_neutral)
check("全部中性 → 5.5 附近 (5.0-6.0)", 5.0 <= score2 <= 6.0, f"got {score2}")

fake_bear = {"atr": {"volatility_level": "moderate_volatility"}}
fake_bear["rsi"] = {"value": 50, "signal": "bullish"}
for k in ["macd", "ema", "bollinger", "supertrend", "kdj", "obv"]:
    fake_bear[k] = {"value": 1, "signal": "bearish"}
score3, _ = calculate_technical_score(fake_bear)
check("1 bullish + 6 bearish → 强烈看空 (<3.0)", score3 < 3.0, f"got {score3}")

print("== 4. 无成交量降级 ==")
novol_df = make_ohlcv(trend_closes(100, 0.01))  # 无 volume 列
novol_ind = calculate_indicators(novol_df)
check("无 volume → OBV 标记 unavailable", novol_ind["obv"]["value"] is None)
novol_score, novol_info = calculate_technical_score(novol_ind)
check("无 volume 评分仍在 0-10", 0 <= novol_score <= 10, f"got {novol_score}")

print("== 5. 数据不足 30 根 → 报错 ==")
short = {
    "symbol": "TEST",
    "interval": "daily",
    "candles": [
        {"timestamp": i, "open": 1, "high": 1.1, "low": 0.9, "close": 1.05, "volume": 100}
        for i in range(20)
    ],
}
tmp = Path(__file__).parent / "_test_short.json"
tmp.write_text(json.dumps(short))
r = subprocess.run(
    [sys.executable, str(SCRIPT), "--input", str(tmp)],
    capture_output=True, text=True,
)
tmp.unlink()
check("退出码非 0", r.returncode != 0, f"got {r.returncode}")
check("输出含 error 字段", '"error"' in r.stdout, r.stdout[:120])

print(f"\n结果: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
