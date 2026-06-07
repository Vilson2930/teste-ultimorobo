import numpy as np

from src.backtest_auditor import run_backtest_auditor


def fake_equity_curve():
    np.random.seed(42)

    returns = np.random.normal(
        loc=0.0005,
        scale=0.01,
        size=252
    )

    equity = [100000]

    for r in returns:
        equity.append(
            equity[-1] * (1 + r)
        )

    return equity


def test_backtest_auditor_gera_saida():

    result = run_backtest_auditor(
        fake_equity_curve()
    )

    assert result is not None


def test_backtest_score_existe():

    result = run_backtest_auditor(
        fake_equity_curve()
    )

    summary = result["backtest_summary"]

    assert "backtest_score" in summary.columns


def test_backtest_level_valido():

    result = run_backtest_auditor(
        fake_equity_curve()
    )

    level = result["backtest_summary"].iloc[0][
        "backtest_level"
    ]

    assert level in [
        "ROBUSTO",
        "ACEITAVEL",
        "ACEITAVEL_COM_RESSALVAS",
        "FRAGIL",
    ]


def test_cagr_existe():

    result = run_backtest_auditor(
        fake_equity_curve()
    )

    summary = result["backtest_summary"]

    assert "cagr_pct" in summary.columns


def test_max_drawdown_existe():

    result = run_backtest_auditor(
        fake_equity_curve()
    )

    summary = result["backtest_summary"]

    assert "max_drawdown_pct" in summary.columns
