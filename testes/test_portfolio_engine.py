from src.portfolio_engine import build_target_allocation


def test_expansao_forte():

    latest = {
        "macro_conviction": 85,
        "confidence_score": 80,
        "macro_momentum": 5
    }

    allocation = build_target_allocation(latest)

    assert allocation["BTC-USD"] >= 0.25
    assert allocation["VOO"] >= 0.25
    assert allocation["BOTZ"] >= 0.08

    assert allocation["USDT-USD"] <= 0.10
    assert allocation["TLT"] <= 0.15


def test_expansao_normal():

    latest = {
        "macro_conviction": 65,
        "confidence_score": 80,
        "macro_momentum": 3
    }

    allocation = build_target_allocation(latest)

    assert allocation["BTC-USD"] > allocation["USDT-USD"]
    assert allocation["VOO"] > allocation["TLT"]


def test_neutro():

    latest = {
        "macro_conviction": 50,
        "confidence_score": 80,
        "macro_momentum": 0
    }

    allocation = build_target_allocation(latest)

    assert allocation["USDT-USD"] > 0.10
    assert allocation["TLT"] > 0.10


def test_stress_sistemico():

    latest = {
        "macro_conviction": 10,
        "confidence_score": 80,
        "macro_momentum": -5
    }

    allocation = build_target_allocation(latest)

    assert allocation["USDT-USD"] > allocation["BTC-USD"]
    assert allocation["TLT"] > allocation["VOO"]
    assert allocation["GLD"] > allocation["BOTZ"]


def test_baixa_confianca_reduz_risco():

    latest = {
        "macro_conviction": 85,
        "confidence_score": 40,
        "macro_momentum": 5
    }

    allocation = build_target_allocation(latest)

    risco = (
        allocation["BTC-USD"]
        + allocation["VOO"]
        + allocation["BOTZ"]
        + allocation["INDA"]
    )

    defesa = (
        allocation["USDT-USD"]
        + allocation["GLD"]
        + allocation["TLT"]
    )

    assert defesa > 0.30


def test_momentum_negativo_reduz_risco():

    latest = {
        "macro_conviction": 85,
        "confidence_score": 80,
        "macro_momentum": -10
    }

    allocation = build_target_allocation(latest)

    defesa = (
        allocation["USDT-USD"]
        + allocation["GLD"]
        + allocation["TLT"]
    )

    assert defesa > 0.25
