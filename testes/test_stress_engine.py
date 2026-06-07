import pandas as pd

from src.stress_engine import run_stress_engine


def make_rebalance():
    return pd.DataFrame(
        {
            "valor_atual": [
                40000,
                10000,
                15000,
                20000,
                15000,
                5000,
                5000,
            ],
            "peso_atual": [
                0.40,
                0.10,
                0.15,
                0.20,
                0.15,
                0.05,
                0.05,
            ],
        },
        index=[
            "BTC-USD",
            "USDT-USD",
            "GLD",
            "VOO",
            "TLT",
            "BOTZ",
            "INDA",
        ],
    )


def run_engine():
    return run_stress_engine(
        rebalance=make_rebalance(),
        monthly_expense_usd=2000,
    )


def test_stress_engine_gera_saida():
    result = run_engine()

    assert "stress_results" in result
    assert "stress_summary" in result


def test_stress_tem_cenarios():
    result = run_engine()

    stress_results = result["stress_results"]

    assert len(stress_results) >= 6


def test_stress_summary_tem_score():
    result = run_engine()

    score = result["stress_summary"].iloc[0]["stress_score"]

    assert score > 0


def test_stress_level_valido():
    result = run_engine()

    level = result["stress_summary"].iloc[0]["stress_level"]

    assert level in [
        "ROBUSTO",
        "ACEITAVEL_COM_RESSALVAS",
        "FRAGIL_COM_RESSALVAS",
        "FRAGIL",
        "CRITICO",
    ]


def test_drawdown_maximo_existe():
    result = run_engine()

    max_drawdown = result["stress_summary"].iloc[0]["max_drawdown_pct"]

    assert max_drawdown >= 0


def test_forced_selling_booleano():
    result = run_engine()

    forced = result["stress_summary"].iloc[0]["forced_selling_any"]

    assert forced in [True, False]
