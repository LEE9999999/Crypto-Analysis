#!/usr/bin/env python3
"""
D8 Technical Analysis Script
Calculates 8 Tier 1 technical indicators from OHLCV data.

Tier 1 indicators:
1. RSI (14) - momentum
2. MACD (12,26,9) - trend + momentum
3. EMA (5,20) - trend direction
4. Bollinger Bands (20,2) - volatility
5. SuperTrend (10,3) - trend + buy/sell signal
6. KDJ (9,3,3) - stochastic oscillator
7. ATR (14) - volatility measure
8. OBV / VWAP - volume confirmation

Usage:
    python technical_analysis.py --input ohlcv.json
    python technical_analysis.py --stdin < ohlcv.json
    cat ohlcv.json | python technical_analysis.py --stdin

Input format (JSON):
{
    "symbol": "BTC",
    "interval": "daily",
    "candles": [
        {"timestamp": 1234567890, "open": 50000, "high": 51000, "low": 49000, "close": 50500, "volume": 1000000},
        ...
    ]
}

Output format (JSON):
{
    "symbol": "BTC",
    "indicators": { ... },
    "signal_summary": { ... },
    "technical_score": 6.5,
    "tier1_indicators": [...]
}
"""

import argparse
import json
import sys

import pandas as pd
import ta


def calculate_supertrend(df, period=10, multiplier=3):
    """Calculate SuperTrend indicator (ta library does not have it built-in).

    Returns: (supertrend_value, direction) where direction=1 is bullish, -1 is bearish.
    """
    high = df["high"]
    low = df["low"]
    close = df["close"]

    atr_obj = ta.volatility.AverageTrueRange(high, low, close, window=period)
    atr_vals = atr_obj.average_true_range()

    hl2 = (high + low) / 2
    upper_basic = hl2 + multiplier * atr_vals
    lower_basic = hl2 - multiplier * atr_vals

    upper_band = upper_basic.copy()
    lower_band = lower_basic.copy()

    for i in range(1, len(close)):
        if (upper_basic.iloc[i] < upper_band.iloc[i - 1]) or (
            close.iloc[i - 1] > upper_band.iloc[i - 1]
        ):
            upper_band.iloc[i] = upper_basic.iloc[i]
        else:
            upper_band.iloc[i] = upper_band.iloc[i - 1]

        if (lower_basic.iloc[i] > lower_band.iloc[i - 1]) or (
            close.iloc[i - 1] < lower_band.iloc[i - 1]
        ):
            lower_band.iloc[i] = lower_basic.iloc[i]
        else:
            lower_band.iloc[i] = lower_band.iloc[i - 1]

    supertrend = pd.Series(index=close.index, dtype=float)
    direction = pd.Series(index=close.index, dtype=int)

    supertrend.iloc[0] = upper_band.iloc[0]
    direction.iloc[0] = 1

    for i in range(1, len(close)):
        if supertrend.iloc[i - 1] == upper_band.iloc[i - 1]:
            if close.iloc[i] <= upper_band.iloc[i]:
                direction.iloc[i] = -1
                supertrend.iloc[i] = upper_band.iloc[i]
            else:
                direction.iloc[i] = 1
                supertrend.iloc[i] = lower_band.iloc[i]
        else:
            if close.iloc[i] >= lower_band.iloc[i]:
                direction.iloc[i] = 1
                supertrend.iloc[i] = lower_band.iloc[i]
            else:
                direction.iloc[i] = -1
                supertrend.iloc[i] = upper_band.iloc[i]

    return supertrend.iloc[-1], direction.iloc[-1]


def calculate_indicators(df):
    """Calculate all 8 Tier 1 indicators from OHLCV DataFrame.

    Returns dict of indicator results.
    """
    results = {}
    current_price = float(df["close"].iloc[-1])

    # --- 1. RSI (14) ---
    rsi = ta.momentum.RSIIndicator(df["close"], window=14)
    rsi_val = float(rsi.rsi().iloc[-1])
    if rsi_val < 30:
        rsi_signal = "bullish"
        rsi_interp = f"RSI {rsi_val:.1f} - oversold, potential rebound"
    elif rsi_val > 70:
        rsi_signal = "bearish"
        rsi_interp = f"RSI {rsi_val:.1f} - overbought, potential correction"
    else:
        rsi_signal = "neutral"
        rsi_interp = f"RSI {rsi_val:.1f} - neutral zone"
    results["rsi"] = {
        "value": round(rsi_val, 2),
        "signal": rsi_signal,
        "interpretation": rsi_interp,
    }

    # --- 2. MACD (12, 26, 9) ---
    macd = ta.trend.MACD(
        df["close"], window_slow=26, window_fast=12, window_sign=9
    )
    macd_line = float(macd.macd().iloc[-1])
    signal_line = float(macd.macd_signal().iloc[-1])
    histogram = float(macd.macd_diff().iloc[-1])
    if macd_line > signal_line:
        macd_signal = "bullish"
        macd_interp = "MACD above signal line, bullish momentum"
    else:
        macd_signal = "bearish"
        macd_interp = "MACD below signal line, bearish momentum"
    results["macd"] = {
        "macd_line": round(macd_line, 4),
        "signal_line": round(signal_line, 4),
        "histogram": round(histogram, 4),
        "signal": macd_signal,
        "interpretation": macd_interp,
    }

    # --- 3. EMA (5, 20) ---
    ema5 = float(
        ta.trend.EMAIndicator(df["close"], window=5).ema_indicator().iloc[-1]
    )
    ema20 = float(
        ta.trend.EMAIndicator(df["close"], window=20).ema_indicator().iloc[-1]
    )
    if ema5 > ema20 and current_price > ema20:
        ema_signal = "bullish"
        ema_interp = "EMA5 > EMA20, price above EMA20, uptrend"
    elif ema5 < ema20 and current_price < ema20:
        ema_signal = "bearish"
        ema_interp = "EMA5 < EMA20, price below EMA20, downtrend"
    else:
        ema_signal = "neutral"
        ema_interp = "EMA5 and EMA20 mixed, trend unclear"
    results["ema"] = {
        "ema5": round(ema5, 4),
        "ema20": round(ema20, 4),
        "current_price": round(current_price, 4),
        "signal": ema_signal,
        "interpretation": ema_interp,
    }

    # --- 4. Bollinger Bands (20, 2) ---
    bb = ta.volatility.BollingerBands(df["close"], window=20, window_dev=2)
    bb_upper = float(bb.bollinger_hband().iloc[-1])
    bb_middle = float(bb.bollinger_mavg().iloc[-1])
    bb_lower = float(bb.bollinger_lband().iloc[-1])
    bb_width = float(bb.bollinger_wband().iloc[-1])
    if current_price <= bb_lower:
        bb_signal = "bullish"
        bb_interp = "Price near lower Bollinger Band, oversold"
    elif current_price >= bb_upper:
        bb_signal = "bearish"
        bb_interp = "Price near upper Bollinger Band, overbought"
    else:
        bb_signal = "neutral"
        bb_interp = "Price within Bollinger Bands, normal range"
    results["bollinger"] = {
        "upper": round(bb_upper, 4),
        "middle": round(bb_middle, 4),
        "lower": round(bb_lower, 4),
        "width_pct": round(bb_width, 2),
        "signal": bb_signal,
        "interpretation": bb_interp,
    }

    # --- 5. SuperTrend (10, 3) ---
    st_val, st_dir = calculate_supertrend(df, period=10, multiplier=3)
    if st_dir == 1:
        st_signal = "bullish"
        st_interp = "SuperTrend bullish, price above trend line"
    else:
        st_signal = "bearish"
        st_interp = "SuperTrend bearish, price below trend line"
    results["supertrend"] = {
        "value": round(float(st_val), 4),
        "direction": "buy" if st_dir == 1 else "sell",
        "signal": st_signal,
        "interpretation": st_interp,
    }

    # --- 6. KDJ (9, 3, 3) ---
    stoch = ta.momentum.StochasticOscillator(
        df["high"], df["low"], df["close"], window=9, smooth_window=3
    )
    k_val = float(stoch.stoch().iloc[-1])
    d_val = float(stoch.stoch_signal().iloc[-1])
    j_val = 3 * k_val - 2 * d_val
    if j_val > 100:
        kdj_signal = "bearish"
        kdj_interp = f"KDJ J={j_val:.1f} - overbought"
    elif j_val < 0:
        kdj_signal = "bullish"
        kdj_interp = f"KDJ J={j_val:.1f} - oversold"
    elif k_val > d_val:
        kdj_signal = "bullish"
        kdj_interp = f"KDJ K={k_val:.1f} > D={d_val:.1f}, bullish cross"
    else:
        kdj_signal = "bearish"
        kdj_interp = f"KDJ K={k_val:.1f} < D={d_val:.1f}, bearish cross"
    results["kdj"] = {
        "k": round(k_val, 2),
        "d": round(d_val, 2),
        "j": round(j_val, 2),
        "signal": kdj_signal,
        "interpretation": kdj_interp,
    }

    # --- 7. ATR (14) ---
    atr = ta.volatility.AverageTrueRange(
        df["high"], df["low"], df["close"], window=14
    )
    atr_val = float(atr.average_true_range().iloc[-1])
    atr_pct = (atr_val / current_price) * 100 if current_price > 0 else 0
    if atr_pct > 5:
        atr_level = "high_volatility"
        atr_interp = (
            f"ATR {atr_val:.4f} ({atr_pct:.1f}% of price) - high volatility"
        )
    elif atr_pct > 2:
        atr_level = "moderate_volatility"
        atr_interp = (
            f"ATR {atr_val:.4f} ({atr_pct:.1f}% of price) - moderate volatility"
        )
    else:
        atr_level = "low_volatility"
        atr_interp = (
            f"ATR {atr_val:.4f} ({atr_pct:.1f}% of price) - low volatility"
        )
    results["atr"] = {
        "value": round(atr_val, 4),
        "pct_of_price": round(atr_pct, 2),
        "volatility_level": atr_level,
        "signal": "neutral",
        "interpretation": atr_interp,
    }

    # --- 8. OBV / VWAP ---
    has_volume = "volume" in df.columns and df["volume"].notna().any()
    if has_volume:
        obv = ta.volume.OnBalanceVolumeIndicator(df["close"], df["volume"])
        obv_val = float(obv.on_balance_volume().iloc[-1])
        obv_series = obv.on_balance_volume()
        lookback = min(5, len(obv_series) - 1)
        obv_prev = float(obv_series.iloc[-(lookback + 1)])
        obv_trend = "rising" if obv_val > obv_prev else "falling"
        obv_signal = "bullish" if obv_trend == "rising" else "bearish"
        obv_interp = (
            "OBV rising, accumulation phase"
            if obv_trend == "rising"
            else "OBV falling, distribution phase"
        )
        results["obv"] = {
            "value": round(obv_val, 2),
            "trend": obv_trend,
            "signal": obv_signal,
            "interpretation": obv_interp,
        }

        vwap = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()
        vwap_val = float(vwap.iloc[-1])
        vwap_signal = "bullish" if current_price > vwap_val else "bearish"
        vwap_interp = (
            "Price above VWAP, buyer dominance"
            if current_price > vwap_val
            else "Price below VWAP, seller dominance"
        )
        results["vwap"] = {
            "value": round(vwap_val, 4),
            "signal": vwap_signal,
            "interpretation": vwap_interp,
        }
    else:
        results["obv"] = {
            "value": None,
            "signal": "neutral",
            "interpretation": "Volume data not available, OBV skipped",
        }
        results["vwap"] = {
            "value": None,
            "signal": "neutral",
            "interpretation": "Volume data not available, VWAP skipped",
        }

    return results


def calculate_technical_score(indicators):
    """Calculate overall technical score (0-10) from indicator signals.

    Directional indicators (7): RSI, MACD, EMA, Bollinger, SuperTrend, KDJ, OBV/VWAP
    Non-directional (1): ATR (volatility risk modifier)

    Returns: (score, signal_info)
    """
    directional = [
        "rsi",
        "macd",
        "ema",
        "bollinger",
        "supertrend",
        "kdj",
        "obv",
        "vwap",
    ]
    bullish = 0
    bearish = 0
    neutral = 0
    total_directional = 0
    signal_list = []

    for name in directional:
        if name not in indicators:
            continue
        ind = indicators[name]
        signal = ind.get("signal", "neutral")
        # Skip indicators with explicit value=None (e.g., OBV/VWAP when volume is missing)
        if "value" in ind and ind["value"] is None:
            signal_list.append(f"{name.upper()}: unavailable (no data)")
            continue
        total_directional += 1
        if signal == "bullish":
            bullish += 1
            signal_list.append(f"{name.upper()}: bullish")
        elif signal == "bearish":
            bearish += 1
            signal_list.append(f"{name.upper()}: bearish")
        else:
            neutral += 1
            signal_list.append(f"{name.upper()}: neutral")

    if total_directional == 0:
        score = 5.0
    else:
        bull_ratio = bullish / total_directional
        bear_ratio = bearish / total_directional

        if bull_ratio >= 0.85:
            score = 9.0 + (bull_ratio - 0.85) * 10
        elif bull_ratio >= 0.6:
            score = 7.0 + (bull_ratio - 0.6) * 20
        elif bull_ratio >= 0.4:
            score = 5.0 + (bull_ratio - 0.4) * 20
        elif bull_ratio >= 0.2:
            score = 3.0 + (bull_ratio - 0.2) * 20
        else:
            score = 1.0 + bull_ratio * 10

    # ATR volatility risk modifier
    atr = indicators.get("atr", {})
    if atr.get("volatility_level") == "high_volatility":
        score -= 0.5
        signal_list.append("ATR: high_volatility (risk penalty -0.5)")
    elif atr.get("volatility_level") == "low_volatility":
        score += 0.2
        signal_list.append("ATR: low_volatility (stability bonus +0.2)")

    score = max(0.0, min(10.0, score))

    return round(score, 1), {
        "bullish_count": bullish,
        "bearish_count": bearish,
        "neutral_count": neutral,
        "total_directional": total_directional,
        "bull_ratio": round(bull_ratio, 2) if total_directional > 0 else 0,
        "bear_ratio": round(bear_ratio, 2) if total_directional > 0 else 0,
        "signals": signal_list,
        "score_reasoning": (
            f"{bullish}/{total_directional} bullish, "
            f"{bearish}/{total_directional} bearish, "
            f"{neutral}/{total_directional} neutral"
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Calculate 8 Tier 1 technical indicators from OHLCV data"
    )
    parser.add_argument("--input", "-i", help="Input JSON file with OHLCV data")
    parser.add_argument(
        "--stdin", action="store_true", help="Read from stdin"
    )
    parser.add_argument(
        "--cmc-data",
        help="CMC MCP technical analysis JSON for cross-validation (optional)",
    )
    args = parser.parse_args()

    if args.stdin:
        data = json.load(sys.stdin)
    elif args.input:
        with open(args.input) as f:
            data = json.load(f)
    else:
        print(
            json.dumps(
                {"error": "No input provided. Use --input <file> or --stdin."}
            )
        )
        sys.exit(1)

    candles = data.get("candles", [])
    if not candles:
        print(json.dumps({"error": "No candles data found in input."}))
        sys.exit(1)

    df = pd.DataFrame(candles)
    required = ["open", "high", "low", "close"]
    for col in required:
        if col not in df.columns:
            print(json.dumps({"error": f"Missing required column: {col}"}))
            sys.exit(1)

    if len(df) < 30:
        print(
            json.dumps(
                {
                    "error": f"Insufficient data: {len(df)} candles. "
                    f"Need at least 30 for reliable indicator calculation."
                }
            )
        )
        sys.exit(1)

    indicators = calculate_indicators(df)
    score, signal_info = calculate_technical_score(indicators)

    cross_validation = None
    if args.cmc_data:
        with open(args.cmc_data) as f:
            cmc_data = json.load(f)
        cross_validation = {
            "cmc_rsi_14": cmc_data.get("rsi", {}).get("rsi14"),
            "cmc_macd": cmc_data.get("macd", {}),
            "cmc_ema_7d": cmc_data.get("moving_averages", {}).get(
                "exponential_moving_average_7_day"
            ),
            "local_rsi": indicators.get("rsi", {}).get("value"),
            "local_macd_line": indicators.get("macd", {}).get("macd_line"),
            "local_ema5": indicators.get("ema", {}).get("ema5"),
            "note": "CMC MCP values used for cross-validation. Small differences expected due to different calculation windows.",
        }

    output = {
        "symbol": data.get("symbol", "UNKNOWN"),
        "interval": data.get("interval", "daily"),
        "data_points": len(candles),
        "indicators": indicators,
        "signal_summary": signal_info,
        "technical_score": score,
        "cross_validation": cross_validation,
        "tier1_indicators": [
            "RSI(14)",
            "MACD(12,26,9)",
            "EMA(5,20)",
            "BollingerBands(20,2)",
            "SuperTrend(10,3)",
            "KDJ(9,3,3)",
            "ATR(14)",
            "OBV/VWAP",
        ],
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
