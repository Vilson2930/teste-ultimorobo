import pandas as pd

from src.counterparty_engine import run_counterparty_engine


def make_rebalance():
    return pd.DataFrame(
        {
            "valor_atual": [
                40000,
                10000,
                15000,
                20000,
                10000,
                3000,
                2000,
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
    return run_counterparty_engine(
        rebalance=make_rebalance(),
    )


def test_counterparty_engine_gera_saida():
    result = run_engine()

    assert "counterparty_audit" in result
    assert "counterparty_summary" in result


def test_counterparty_score_existe():
    result = run_engine()

    score = result["counterparty_summary"].iloc[0]["counterparty_score"]

    assert score > 0


def test_counterparty_level_valido():
    result = run_engine()

    level = result["counterparty_summary"].iloc[0]["counterparty_level"]

    assert level in [
        "ROBUSTO",
        "ACEITAVEL",
        "CONCENTRADO",
        "CRITICO",
    ]


def test_largest_counterparty_existe():
    result = run_engine()

    largest = result["counterparty_summary"].iloc[0]["largest_counterparty"]

    assert largest in [
        "SELF_CUSTODY",
        "TETHER",
        "BLACKROCK",
        "STATE_STREET",
        "GLOBAL_X",
        "OUTROS",
    ]


def test_concentration_level_valido():
    result = run_engine()

    level = result["counterparty_summary"].iloc[0]["concentration_level"]

    assert level in [
        "ROBUSTA",
        "ACEITAVEL",
        "CONCENTRADA",
        "CRITICA",
    ]
