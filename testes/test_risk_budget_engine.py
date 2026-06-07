import pandas as pd

from src.risk_budget_engine import run_risk_budget_engine


def make_rebalance():
    return pd.DataFrame({
        "ativo": [
            "BTC-USD",
            "USDT-USD",
            "GLD",
            "VOO",
            "TLT",
            "BOTZ",
            "INDA",
        ],
        "valor_atual": [
            40000,
            7000,
            16000,
            17000,
            7000,
            7000,
            6000,
        ],
        "peso_atual": [
            0.40,
            0.07,
            0.16,
            0.17,
            0.07,
            0.07,
            0.06,
        ],
    })


def test_risk_budget_gera_saida():
    result = run_risk_budget_engine(
        rebalance=make_rebalance(),
        market_data=None,
    )

    assert "risk_budget" in result
    assert "risk_budget_summary" in result


def test_risk_budget_tem_score():
    result = run_risk_budget_engine(
        rebalance=make_rebalance(),
        market_data=None,
    )

    summary = result["risk_budget_summary"]

    assert summary.iloc[0]["risk_budget_score"] > 0


def test_risk_budget_tem_nivel():
    result = run_risk_budget_engine(
        rebalance=make_rebalance(),
        market_data=None,
    )

    level = result["risk_budget_summary"].iloc[0]["risk_budget_level"]

    assert level in [
        "EXCELENTE",
        "ROBUSTO",
        "ACEITAVEL",
        "CONCENTRADO",
        "CRITICO",
    ]


def test_top_risk_asset_existe():
    result = run_risk_budget_engine(
        rebalance=make_rebalance(),
        market_data=None,
    )

    top_asset = result["risk_budget_summary"].iloc[0]["top_risk_asset"]

    assert top_asset is not None


def test_contribuicoes_somam():
    result = run_risk_budget_engine(
        rebalance=make_rebalance(),
        market_data=None,
    )

    rb = result["risk_budget"]

    total = rb["risk_contribution_abs_pct"].sum()

    assert 0.99 <= total <= 1.01
