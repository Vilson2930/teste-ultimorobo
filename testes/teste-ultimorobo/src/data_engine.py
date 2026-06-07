import pandas as pd

from src.data_engine import run_data_engine


def fake_fred_data():
    index = pd.date_range("2024-01-01", periods=5)

    return pd.DataFrame(
        {
            "real_yield_10y": [1.5, 1.6, 1.7, 1.8, 1.9],
            "financial_conditions": [0.1, 0.1, 0.2, 0.2, 0.3],
            "high_yield_spread": [4.0, 4.1, 4.2, 4.1, 4.0],
            "core_pce": [125, 126, 127, 128, 129],
            "inflation_5y5y": [2.2, 2.3, 2.4, 2.3, 2.2],
            "treasury_10y": [4.0, 4.1, 4.2, 4.1, 4.0],
            "fed_funds": [5.0, 5.0, 5.0, 5.0, 5.0],
            "fed_assets": [7000000, 7000000, 7000000, 7000000, 7000000],
            "yield_curve": [-1.0, -0.9, -0.8, -0.9, -1.0],
        },
        index=index,
    )


def fake_market_data():
    index = pd.date_range("2024-01-01", periods=5)

    market_data = pd.DataFrame(
        {
            "btc": [90000, 91000, 92000, 93000, 94000],
            "gld": [280, 281, 282, 283, 284],
            "voo": [500, 501, 502, 503, 504],
            "tlt": [90, 91, 92, 93, 94],
            "botz": [30, 31, 32, 33, 34],
            "inda": [50, 51, 52, 53, 54],
            "dxy": [100, 101, 102, 101, 100],
            "vix": [15, 16, 17, 16, 15],
        },
        index=index,
    )

    latest_market = market_data.iloc[-1]

    market_audit = pd.DataFrame([{
        "market_data_score": 100,
        "market_data_status": "INSTITUCIONAL",
        "market_quality_score": 100,
        "market_quality_status": "ALTA",
        "freshness_status": "ATUALIZADO",
        "coverage_status": "COMPLETO",
    }])

    return market_data, latest_market, market_audit


def test_data_engine_gera_saida(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "src.data_engine.load_fred_data",
        lambda: (fake_fred_data(), pd.DataFrame(), []),
    )

    monkeypatch.setattr(
        "src.data_engine.load_market_data",
        fake_market_data,
    )

    result = run_data_engine()

    assert "fred_data" in result
    assert "market_data" in result
    assert "latest_market" in result
    assert "market_audit" in result
    assert "data_snapshot" in result


def test_market_data_score_existe(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "src.data_engine.load_fred_data",
        lambda: (fake_fred_data(), pd.DataFrame(), []),
    )

    monkeypatch.setattr(
        "src.data_engine.load_market_data",
        fake_market_data,
    )

    result = run_data_engine()

    score = result["market_audit"].iloc[0]["market_data_score"]

    assert score > 0


def test_market_data_status_valido(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "src.data_engine.load_fred_data",
        lambda: (fake_fred_data(), pd.DataFrame(), []),
    )

    monkeypatch.setattr(
        "src.data_engine.load_market_data",
        fake_market_data,
    )

    result = run_data_engine()

    status = result["market_audit"].iloc[0]["market_data_status"]

    assert status in [
        "INSTITUCIONAL",
        "ACEITAVEL",
        "FRAGIL",
        "CRITICO",
    ]


def test_data_snapshot_gerado(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "src.data_engine.load_fred_data",
        lambda: (fake_fred_data(), pd.DataFrame(), []),
    )

    monkeypatch.setattr(
        "src.data_engine.load_market_data",
        fake_market_data,
    )

    result = run_data_engine()

    snapshot = result["data_snapshot"]

    assert not snapshot.empty


def test_data_snapshot_tem_btc_e_vix(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "src.data_engine.load_fred_data",
        lambda: (fake_fred_data(), pd.DataFrame(), []),
    )

    monkeypatch.setattr(
        "src.data_engine.load_market_data",
        fake_market_data,
    )

    result = run_data_engine()

    snapshot = result["data_snapshot"]

    assert "btc" in snapshot.columns
    assert "vix" in snapshot.columns
