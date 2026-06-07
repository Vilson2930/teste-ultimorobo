import pandas as pd

from src.governance_engine import run_governance_engine


def make_latest():
    return pd.Series({
        "regime": "EXPANSAO_NORMAL",
        "sinal_operacional": "RISCO_ON_VALIDADO",
        "macro_conviction": 75,
        "confidence_score": 80,
        "macro_momentum": 5,
        "macro_score": 72,
    })


def make_market_audit():
    return pd.DataFrame([{
        "market_data_score": 100,
        "market_quality_score": 100,
    }])


def make_rebalance():
    return pd.DataFrame(
        {
            "valor_atual": [40000, 10000, 15000, 20000, 15000],
            "peso_atual": [0.40, 0.10, 0.15, 0.20, 0.15],
        },
        index=["BTC-USD", "USDT-USD", "GLD", "VOO", "TLT"],
    )


def make_survival_audit(kill_switch=False, ruin_risk="BAIXO", survival_score=90):
    return pd.DataFrame([{
        "runway_months": 36,
        "bucket_trilhos": 3,
        "bucket_entidades": 3,
        "bucket_jurisdicoes_validas": 3,
        "max_bucket_concentration": 0.40,
        "survival_kill_switch": kill_switch,
        "survival_score": survival_score,
        "survival_status": "ROBUSTO",
        "ruin_risk": ruin_risk,
    }])


def make_deterioration_audit():
    return pd.DataFrame([{
        "deterioration_score": 90,
        "early_warning": False,
    }])


def make_liquidity_forecast():
    return pd.DataFrame([{
        "future_liquidity_score": 80,
        "future_regime": "EXPANSAO",
    }])


def run_engine(tmp_path, survival_audit=None):
    if survival_audit is None:
        survival_audit = make_survival_audit()

    return run_governance_engine(
        latest=make_latest(),
        macro_engine_audit=pd.DataFrame([make_latest()]),
        market_audit=make_market_audit(),
        rebalance=make_rebalance(),
        orders=pd.DataFrame(),
        total_value=100000,
        gross_turnover_final=0.10,
        turnover_status="GIRO_DENTRO_DO_LIMITE",
        kill_switch=False,
        survival_audit=survival_audit,
        deterioration_audit=make_deterioration_audit(),
        liquidity_forecast=make_liquidity_forecast(),
    )


def test_governance_engine_gera_saida(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = run_engine(tmp_path)

    assert "committee_audit" in result
    assert "risk_committee_integrated" in result
    assert "final_opinion" in result
    assert "executive_dashboard" in result


def test_governance_final_verdict_existe(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = run_engine(tmp_path)

    verdict = result["risk_committee_integrated"].iloc[0]["final_verdict"]

    assert verdict in [
        "APROVADO",
        "APROVADO_COM_RESSALVAS",
        "APROVADO_COM_RESSALVAS_CRITICAS",
        "REPROVADO",
        "REPROVADO_OPERACIONALMENTE",
    ]


def test_governance_score_integrado_existe(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = run_engine(tmp_path)

    score = result["risk_committee_integrated"].iloc[0]["integrated_risk_score"]

    assert score > 0


def test_governance_detecta_survival_kill_switch(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    survival = make_survival_audit(
        kill_switch=True,
        ruin_risk="ALTO",
        survival_score=30,
    )

    result = run_engine(tmp_path, survival_audit=survival)

    verdict = result["risk_committee_integrated"].iloc[0]["final_verdict"]

    assert verdict == "REPROVADO_OPERACIONALMENTE"


def test_executive_dashboard_gera_veredito(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = run_engine(tmp_path)

    dashboard = result["executive_dashboard"]

    assert "final_verdict" in dashboard.columns
    assert "committee_action" in dashboard.columns
