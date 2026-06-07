import pandas as pd
from src.portfolio_engine import run_rebalance


def make_latest(
    macro_conviction,
    macro_score,
    macro_momentum,
    confidence_score,
    liquidez,
    stress,
):
    return pd.Series({
        "macro_conviction": macro_conviction,
        "macro_score": macro_score,
        "macro_momentum": macro_momentum,
        "confidence_score": confidence_score,
        "liquidez": liquidez,
        "stress": stress,
    })


def make_market():
    return {
        "btc": 100000,
        "gld": 300,
        "voo": 500,
        "tlt": 100,
        "botz": 30,
        "inda": 50,
    }


def test_rebalance_macro_favoravel_nao_vende_btc(monkeypatch):
    portfolio_fake = {
        "BTC-USD": 0.40,
        "USDT-USD": 20000,
        "GLD": 20,
        "VOO": 20,
        "TLT": 100,
        "BOTZ": 100,
        "INDA": 100,
    }

    monkeypatch.setattr(
        "src.portfolio_engine.load_live_portfolio",
        lambda required_assets=None: portfolio_fake,
    )

    latest = make_latest(85, 80, 5, 80, 70, 80)
    market = make_market()

    target = {
        "BTC-USD": 0.25,
        "USDT-USD": 0.10,
        "GLD": 0.10,
        "VOO": 0.25,
        "TLT": 0.15,
        "BOTZ": 0.08,
        "INDA": 0.07,
    }

    result = run_rebalance(latest, market, target)
    rebalance = result["rebalance"]

    btc_action = rebalance.loc["BTC-USD", "acao"]

    assert btc_action == "MANTER"


def test_rebalance_macro_defensivo_compra_tlt(monkeypatch):
    portfolio_fake = {
        "BTC-USD": 0.20,
        "USDT-USD": 5000,
        "GLD": 10,
        "VOO": 40,
        "TLT": 20,
        "BOTZ": 200,
        "INDA": 200,
    }

    monkeypatch.setattr(
        "src.portfolio_engine.load_live_portfolio",
        lambda required_assets=None: portfolio_fake,
    )

    latest = make_latest(30, 35, -5, 80, 30, 50)
    market = make_market()

    target = {
        "BTC-USD": 0.08,
        "USDT-USD": 0.32,
        "GLD": 0.22,
        "VOO": 0.05,
        "TLT": 0.33,
        "BOTZ": 0.00,
        "INDA": 0.00,
    }

    result = run_rebalance(latest, market, target)
    rebalance = result["rebalance"]

    assert rebalance.loc["TLT", "acao"] in ["COMPRAR", "MANTER"]
    assert rebalance.loc["BTC-USD", "acao"] in ["VENDER", "MANTER"]


def test_rebalance_preserva_usdt_em_macro_defensivo(monkeypatch):
    portfolio_fake = {
        "BTC-USD": 0.10,
        "USDT-USD": 30000,
        "GLD": 10,
        "VOO": 20,
        "TLT": 50,
        "BOTZ": 100,
        "INDA": 100,
    }

    monkeypatch.setattr(
        "src.portfolio_engine.load_live_portfolio",
        lambda required_assets=None: portfolio_fake,
    )

    latest = make_latest(30, 35, -5, 80, 30, 50)
    market = make_market()

    target = {
        "BTC-USD": 0.08,
        "USDT-USD": 0.05,
        "GLD": 0.22,
        "VOO": 0.05,
        "TLT": 0.33,
        "BOTZ": 0.00,
        "INDA": 0.00,
    }

    result = run_rebalance(latest, market, target)
    rebalance = result["rebalance"]

    assert rebalance.loc["USDT-USD", "acao"] == "MANTER"
    assert rebalance.loc["USDT-USD", "motivo_execucao"] == "USDT_PRESERVADO_MACRO_DEFENSIVO"


def test_rebalance_limite_de_giro(monkeypatch):
    portfolio_fake = {
        "BTC-USD": 0.80,
        "USDT-USD": 1000,
        "GLD": 1,
        "VOO": 1,
        "TLT": 1,
        "BOTZ": 1,
        "INDA": 1,
    }

    monkeypatch.setattr(
        "src.portfolio_engine.load_live_portfolio",
        lambda required_assets=None: portfolio_fake,
    )

    latest = make_latest(30, 35, -5, 80, 30, 50)
    market = make_market()

    target = {
        "BTC-USD": 0.08,
        "USDT-USD": 0.32,
        "GLD": 0.22,
        "VOO": 0.05,
        "TLT": 0.33,
        "BOTZ": 0.00,
        "INDA": 0.00,
    }

    result = run_rebalance(latest, market, target)

    assert result["gross_turnover_final"] <= 0.25
