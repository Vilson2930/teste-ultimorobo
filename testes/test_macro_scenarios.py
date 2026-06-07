import pandas as pd
from src.macro_engine import classify_regime, operational_signal


def make_row(macro_conviction, macro_momentum, confidence_score):
    return pd.Series({
        "macro_conviction": macro_conviction,
        "macro_momentum": macro_momentum,
        "confidence_score": confidence_score,
    })


def test_expansao_forte():
    row = make_row(85, 5, 80)

    assert classify_regime(row["macro_conviction"]) == "EXPANSAO_FORTE"
    assert operational_signal(row) == "RISCO_ON_VALIDADO"


def test_expansao_normal():
    row = make_row(65, 3, 75)

    assert classify_regime(row["macro_conviction"]) == "EXPANSAO_NORMAL"
    assert operational_signal(row) == "RISCO_ON_VALIDADO"


def test_neutro():
    row = make_row(50, 0, 70)

    assert classify_regime(row["macro_conviction"]) == "NEUTRO"
    assert operational_signal(row) == "NEUTRO"


def test_contracao():
    row = make_row(30, -3, 70)

    assert classify_regime(row["macro_conviction"]) == "CONTRACAO"
    assert operational_signal(row) == "DEFENSIVO_VALIDADO"


def test_stress_sistemico():
    row = make_row(10, -8, 80)

    assert classify_regime(row["macro_conviction"]) == "STRESS_SISTEMICO"
    assert operational_signal(row) == "DEFENSIVO_VALIDADO"


def test_sinal_fraco_por_baixa_confianca():
    row = make_row(70, 5, 40)

    assert classify_regime(row["macro_conviction"]) == "EXPANSAO_NORMAL"
    assert operational_signal(row) == "SINAL_FRACO"


def test_risco_on_com_cautela():
    row = make_row(65, -2, 75)

    assert classify_regime(row["macro_conviction"]) == "EXPANSAO_NORMAL"
    assert operational_signal(row) == "RISCO_ON_COM_CAUTELA"
