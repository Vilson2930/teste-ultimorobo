import pandas as pd

from src.operational_risk import run_operational_risk
from src.risk_budget_engine import run_risk_budget_engine
from src.liquidity_engine import run_liquidity_engine
from src.counterparty_engine import run_counterparty_engine
from src.stress_engine import run_stress_engine
from src.governance_engine import run_governance_engine
from src.ai_auditor import run_ai_auditor


def make_rebalance():
    return pd.DataFrame(
        {
            "valor_atual": [40000, 10000, 15000, 20000, 10000, 3000, 2000],
            "peso_atual": [0.40, 0.10, 0.15, 0.20, 0.10, 0.03, 0.02],
            "peso_alvo": [0.35, 0.10, 0.15, 0.22, 0.12, 0.04, 0.02],
            "valor_alvo": [35000, 10000, 15000, 22000, 12000, 4000, 2000],
            "desvio_peso": [-0.05, 0.00, 0.00, 0.02, 0.02, 0.01, 0.00],
            "ajuste_usd": [-5000, 0, 0, 2000, 2000, 1000, 0],
            "acao": ["VENDER", "MANTER", "MANTER", "MANTER", "COMPRAR", "MANTER", "MANTER"],
            "motivo_execucao": ["TESTE"] * 7,
        },
        index=["BTC-USD", "USDT-USD", "GLD", "VOO", "TLT", "BOTZ", "INDA"],
    )


def make_access_map(tmp_path):
    df = pd.DataFrame({
        "ativo": ["BTC-USD", "USDT-USD", "GLD", "VOO", "TLT", "BOTZ", "INDA"],
        "trilho": ["SELF_CUSTODY", "EXCHANGE", "ETF", "ETF", "ETF", "ETF", "ETF"],
        "entidade": ["SELF_CUSTODY", "TETHER", "STATE_STREET", "BLACKROCK", "BLACKROCK", "GLOBAL_X", "BLACKROCK"],
        "jurisdicao": ["GLOBAL", "GLOBAL", "USA", "USA", "USA", "USA", "USA"],
        "status": ["ATIVO"] * 7,
        "criticidade": ["MEDIA", "MEDIA", "BAIXA", "BAIXA", "BAIXA", "MEDIA", "MEDIA"],
        "bucket_sobrevivencia": [True, True, True, False, True, False, False],
        "jurisdicao_valida": [True] * 7,
    })

    path = tmp_path / "access_map.csv"
    df.to_csv(path, index=False)
    return str(path)


def make_latest():
    return pd.Series({
        "regime": "EXPANSAO_NORMAL",
        "sinal_operacional": "RISCO_ON_VALIDADO",
        "macro_conviction": 75,
        "confidence_score": 80,
        "macro_momentum": 5,
        "macro_score": 72,
    })


def make_macro_engine_audit():
    return pd.DataFrame([make_latest()])


def make_market_audit():
    return pd.DataFrame([{
        "market_data_score": 100,
        "market_data_status": "INSTITUCIONAL",
        "market_quality_score": 100,
        "market_quality_status": "ALTA",
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


def run_full_integration(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    rebalance = make_rebalance()
    access_map_path = make_access_map(tmp_path)

    survival_context = run_operational_risk(
        rebalance=rebalance,
        access_map_path=access_map_path,
        monthly_expense_usd=2000,
    )

    stress_context = run_stress_engine(
        rebalance=rebalance,
        monthly_expense_usd=2000,
    )

    risk_budget_context = run_risk_budget_engine(
        rebalance=rebalance,
        market_data=None,
    )

    liquidity_context = run_liquidity_engine(
        rebalance=rebalance,
        access_map_path=access_map_path,
    )

    counterparty_context = run_counterparty_engine(
        rebalance=rebalance,
    )

    governance_context = run_governance_engine(
        latest=make_latest(),
        macro_engine_audit=make_macro_engine_audit(),
        market_audit=make_market_audit(),
        rebalance=rebalance,
        orders=pd.DataFrame(),
        total_value=float(rebalance["valor_atual"].sum()),
        gross_turnover_final=0.10,
        turnover_status="GIRO_DENTRO_DO_LIMITE",
        kill_switch=False,
        survival_audit=survival_context["survival_audit"],
        deterioration_audit=make_deterioration_audit(),
        liquidity_forecast=make_liquidity_forecast(),
        stress_summary_override=stress_context["stress_summary"],
        risk_budget_summary=risk_budget_context["risk_budget_summary"],
        liquidity_summary=liquidity_context["liquidity_summary"],
        counterparty_summary=counterparty_context["counterparty_summary"],
    )

    ai_context = run_ai_auditor()

    return {
        "survival": survival_context,
        "stress": stress_context,
        "risk_budget": risk_budget_context,
        "liquidity": liquidity_context,
        "counterparty": counterparty_context,
        "governance": governance_context,
        "ai_audit": ai_context,
    }


def test_integration_gera_todos_contextos(tmp_path, monkeypatch):
    result = run_full_integration(tmp_path, monkeypatch)

    assert "survival" in result
    assert "stress" in result
    assert "risk_budget" in result
    assert "liquidity" in result
    assert "counterparty" in result
    assert "governance" in result
    assert "ai_audit" in result


def test_integration_governance_tem_veredito(tmp_path, monkeypatch):
    result = run_full_integration(tmp_path, monkeypatch)

    verdict = result["governance"]["risk_committee_integrated"].iloc[0]["final_verdict"]

    assert verdict in [
        "APROVADO",
        "APROVADO_COM_RESSALVAS",
        "APROVADO_COM_RESSALVAS_CRITICAS",
        "REPROVADO",
        "REPROVADO_OPERACIONALMENTE",
    ]


def test_integration_ai_auditor_coerente_ou_falha_controlada(tmp_path, monkeypatch):
    result = run_full_integration(tmp_path, monkeypatch)

    status = result["ai_audit"]["ai_audit_summary"].iloc[0]["ai_audit_status"]

    assert status in [
        "COERENTE",
        "FALHA_DE_COHERENCIA",
    ]


def test_integration_risco_liquidez_stress_existentes(tmp_path, monkeypatch):
    result = run_full_integration(tmp_path, monkeypatch)

    assert result["risk_budget"]["risk_budget_summary"].iloc[0]["risk_budget_score"] > 0
    assert result["liquidity"]["liquidity_summary"].iloc[0]["liquidity_score"] > 0
    assert result["stress"]["stress_summary"].iloc[0]["stress_score"] > 0


def test_integration_survival_e_counterparty_existentes(tmp_path, monkeypatch):
    result = run_full_integration(tmp_path, monkeypatch)

    assert result["survival"]["survival_audit"].iloc[0]["survival_score"] > 0
    assert result["counterparty"]["counterparty_summary"].iloc[0]["counterparty_score"] > 0
