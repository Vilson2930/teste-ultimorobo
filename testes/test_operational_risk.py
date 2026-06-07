import pandas as pd

from src.operational_risk import run_operational_risk


def make_rebalance():
    return pd.DataFrame(
        {
            "valor_atual": [
                40000,
                10000,
                15000,
                20000,
                10000,
            ],
            "peso_atual": [
                0.40,
                0.10,
                0.15,
                0.20,
                0.10,
            ],
        },
        index=[
            "BTC-USD",
            "USDT-USD",
            "GLD",
            "VOO",
            "TLT",
        ],
    )


def make_access_map(tmp_path):

    df = pd.DataFrame({
        "ativo": [
            "BTC-USD",
            "USDT-USD",
            "GLD",
            "VOO",
            "TLT",
        ],
        "trilho": [
            "SELF_CUSTODY",
            "EXCHANGE",
            "ETF",
            "ETF",
            "ETF",
        ],
        "entidade": [
            "SELF_CUSTODY",
            "TETHER",
            "STATE_STREET",
            "BLACKROCK",
            "BLACKROCK",
        ],
        "jurisdicao": [
            "GLOBAL",
            "GLOBAL",
            "USA",
            "USA",
            "USA",
        ],
        "status": [
            "ATIVO",
            "ATIVO",
            "ATIVO",
            "ATIVO",
            "ATIVO",
        ],
        "criticidade": [
            "MEDIA",
            "MEDIA",
            "BAIXA",
            "BAIXA",
            "BAIXA",
        ],
        "bucket_sobrevivencia": [
            True,
            True,
            True,
            False,
            True,
        ],
        "jurisdicao_valida": [
            True,
            True,
            True,
            True,
            True,
        ],
    })

    file_path = tmp_path / "access_map.csv"

    df.to_csv(file_path, index=False)

    return str(file_path)


def run_engine(tmp_path):

    return run_operational_risk(
        rebalance=make_rebalance(),
        access_map_path=make_access_map(tmp_path),
        monthly_expense_usd=2000,
    )


def test_survival_gera_saida(tmp_path):

    result = run_engine(tmp_path)

    assert "survival_audit" in result


def test_runway_existe(tmp_path):

    result = run_engine(tmp_path)

    runway = result["survival_audit"].iloc[0]["runway_months"]

    assert runway > 0


def test_survival_score_existe(tmp_path):

    result = run_engine(tmp_path)

    score = result["survival_audit"].iloc[0]["survival_score"]

    assert score > 0


def test_ruin_risk_valido(tmp_path):

    result = run_engine(tmp_path)

    risk = result["survival_audit"].iloc[0]["ruin_risk"]

    assert risk in [
        "BAIXO",
        "MEDIO",
        "ALTO",
    ]


def test_kill_switch_booleano(tmp_path):

    result = run_engine(tmp_path)

    ks = result["survival_audit"].iloc[0]["survival_kill_switch"]

    assert ks in [True, False]
