import pandas as pd

from src.liquidity_engine import run_liquidity_engine


def make_rebalance():
    return pd.DataFrame(
        {
            "ativo": [
                "BTC-USD",
                "USDT-USD",
                "GLD",
                "VOO",
                "TLT",
            ],
            "valor_atual": [
                40000,
                10000,
                15000,
                20000,
                15000,
            ],
            "peso_atual": [
                0.40,
                0.10,
                0.15,
                0.20,
                0.15,
            ],
        }
    )


def make_access_map(tmp_path):
    df = pd.DataFrame(
        {
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
                True,
                True,
            ],
            "jurisdicao_valida": [
                True,
                True,
                True,
                True,
                True,
            ],
        }
    )

    file_path = tmp_path / "access_map.csv"

    df.to_csv(file_path, index=False)

    return str(file_path)


def test_liquidity_engine_gera_saida(tmp_path):
    rebalance = make_rebalance()
    access_map = make_access_map(tmp_path)

    result = run_liquidity_engine(
        rebalance,
        access_map,
    )

    assert "liquidity_summary" in result
    assert "liquidity_audit" in result


def test_liquidity_score_existe(tmp_path):
    rebalance = make_rebalance()
    access_map = make_access_map(tmp_path)

    result = run_liquidity_engine(
        rebalance,
        access_map,
    )

    score = result["liquidity_summary"].iloc[0]["liquidity_score"]

    assert score > 0


def test_liquidity_level_existe(tmp_path):
    rebalance = make_rebalance()
    access_map = make_access_map(tmp_path)

    result = run_liquidity_engine(
        rebalance,
        access_map,
    )

    level = result["liquidity_summary"].iloc[0]["liquidity_level"]

    assert level in [
        "ROBUSTO",
        "ACEITAVEL",
        "FRAGIL",
        "CRITICO",
    ]


def test_haircut_agregado_existe(tmp_path):
    rebalance = make_rebalance()
    access_map = make_access_map(tmp_path)

    result = run_liquidity_engine(
        rebalance,
        access_map,
    )

    haircut = result["liquidity_summary"].iloc[0][
        "aggregate_haircut_pct"
    ]

    assert haircut >= 0


def test_valor_liquido_menor_ou_igual_ao_bruto(tmp_path):
    rebalance = make_rebalance()
    access_map = make_access_map(tmp_path)

    result = run_liquidity_engine(
        rebalance,
        access_map,
    )

    bruto = result["liquidity_summary"].iloc[0]["gross_value"]

    liquido = result["liquidity_summary"].iloc[0]["liquid_value"]

    assert liquido <= bruto
