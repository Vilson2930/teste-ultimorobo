from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("outputs")


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def ensure_outputs():
    OUTPUT_DIR.mkdir(exist_ok=True)


def calculate_cagr(equity_curve):
    equity_curve = pd.Series(equity_curve).dropna()

    if len(equity_curve) < 2:
        return 0.0

    start = float(equity_curve.iloc[0])
    end = float(equity_curve.iloc[-1])

    if start <= 0 or end <= 0:
        return 0.0

    years = len(equity_curve) / 252

    if years <= 0:
        return 0.0

    return (end / start) ** (1 / years) - 1


def calculate_drawdown(equity_curve):
    equity_curve = pd.Series(equity_curve).dropna()

    if equity_curve.empty:
        return pd.Series(dtype=float)

    peak = equity_curve.cummax()
    drawdown = equity_curve / peak - 1

    return drawdown


def calculate_sharpe(returns, risk_free=0.0):
    returns = pd.Series(returns).dropna()

    if returns.empty or returns.std() == 0:
        return 0.0

    excess = returns - risk_free / 252

    return float(np.sqrt(252) * excess.mean() / returns.std())


def calculate_sortino(returns, risk_free=0.0):
    returns = pd.Series(returns).dropna()

    if returns.empty:
        return 0.0

    downside = returns[returns < 0]

    if downside.empty or downside.std() == 0:
        return 0.0

    excess = returns - risk_free / 252

    return float(np.sqrt(252) * excess.mean() / downside.std())


def classify_backtest(cagr, max_drawdown, sharpe):
    if max_drawdown <= -0.50:
        return 40, "FRAGIL"

    if sharpe >= 1.0 and max_drawdown > -0.30 and cagr > 0:
        return 90, "ROBUSTO"

    if sharpe >= 0.5 and max_drawdown > -0.40 and cagr > 0:
        return 75, "ACEITAVEL"

    if cagr > 0:
        return 60, "ACEITAVEL_COM_RESSALVAS"

    return 40, "FRAGIL"


def run_backtest_auditor(equity_curve):
    ensure_outputs()

    equity_curve = pd.Series(equity_curve).dropna().astype(float)

    if equity_curve.empty:
        raise ValueError("Equity curve vazia para Backtest Auditor.")

    returns = equity_curve.pct_change().dropna()
    drawdown = calculate_drawdown(equity_curve)

    cagr = calculate_cagr(equity_curve)
    max_drawdown = float(drawdown.min()) if not drawdown.empty else 0.0
    volatility = float(returns.std() * np.sqrt(252)) if not returns.empty else 0.0
    sharpe = calculate_sharpe(returns)
    sortino = calculate_sortino(returns)

    calmar = cagr / abs(max_drawdown) if max_drawdown < 0 else 0.0

    backtest_score, backtest_level = classify_backtest(
        cagr=cagr,
        max_drawdown=max_drawdown,
        sharpe=sharpe,
    )

    summary = pd.DataFrame([{
        "timestamp_utc": utc_now(),
        "initial_value": float(equity_curve.iloc[0]),
        "final_value": float(equity_curve.iloc[-1]),
        "cagr_pct": round(cagr * 100, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "volatility_pct": round(volatility * 100, 2),
        "sharpe": round(sharpe, 2),
        "sortino": round(sortino, 2),
        "calmar": round(calmar, 2),
        "backtest_score": backtest_score,
        "backtest_level": backtest_level,
    }])

    audit = pd.DataFrame({
        "equity": equity_curve.values,
        "returns": equity_curve.pct_change().fillna(0).values,
        "drawdown": drawdown.values,
    })

    summary.to_csv(OUTPUT_DIR / "backtest_summary.csv", index=False)
    audit.to_csv(OUTPUT_DIR / "backtest_audit.csv", index=False)

    print("====================================================")
    print("BACKTEST AUDITOR")
    print("====================================================")
    print(f"CAGR:              {cagr * 100:.2f}%")
    print(f"Max Drawdown:      {max_drawdown * 100:.2f}%")
    print(f"Volatilidade:      {volatility * 100:.2f}%")
    print(f"Sharpe:            {sharpe:.2f}")
    print(f"Sortino:           {sortino:.2f}")
    print(f"Calmar:            {calmar:.2f}")
    print(f"Backtest Score:    {backtest_score}")
    print(f"Backtest Level:    {backtest_level}")
    print("====================================================")

    return {
        "backtest_summary": summary,
        "backtest_audit": audit,
    }
