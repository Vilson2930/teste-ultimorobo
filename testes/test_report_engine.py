import pandas as pd

from src.report_engine import build_institutional_report


def criar_csvs_base(tmp_path):
    outputs = tmp_path / "outputs"
    outputs.mkdir()

    pd.DataFrame([{
        "regime": "EXPANSAO_NORMAL",
        "sinal_operacional": "RISCO_ON_VALIDADO",
        "macro_conviction": 75,
        "macro_score": 72,
        "confidence_score": 80,
    }]).to_csv(outputs / "macro_engine_audit.csv", index=False)

    pd.DataFrame([{
        "market_data_score": 100,
        "market_data_status": "INSTITUCIONAL",
    }]).to_csv(outputs / "market_data_audit.csv", index=False)

    pd.DataFrame([{
        "final_verdict": "APROVADO",
        "committee_action": "MANTER_APROVADO",
        "integrated_risk_level": "BAIXO",
    }]).to_csv(outputs / "risk_committee_integrated.csv", index=False)

    pd.DataFrame([{
        "runway_months": 24,
        "survival_score": 90,
        "survival_status": "APROVADO",
        "ruin_risk": "BAIXO",
        "survival_kill_switch": False,
    }]).to_csv(outputs / "survival_audit.csv", index=False)

    pd.DataFrame([{
        "stress_score": 80,
        "stress_level": "ROBUSTO",
        "max_drawdown_pct": 20,
        "forced_selling_any": False,
    }]).to_csv(outputs / "stress_summary_v2.csv", index=False)

    pd.DataFrame([{
        "risk_budget_score": 85,
        "risk_budget_level": "ROBUSTO",
        "top_risk_asset": "BTC-USD",
        "max_risk_contribution_pct": 35,
    }]).to_csv(outputs / "risk_budget_summary.csv", index=False)

    pd.DataFrame([{
        "liquidity_score": 85,
        "liquidity_level": "ROBUSTO",
        "aggregate_haircut_pct": 5,
        "liquid_value": 95000,
    }]).to_csv(outputs / "liquidity_summary.csv", index=False)

    pd.DataFrame([{
        "counterparty_score": 90,
        "counterparty_level": "ROBUSTO",
        "largest_counterparty": "BLACKROCK",
    }]).to_csv(outputs / "counterparty_summary.csv", index=False)

    pd.DataFrame([{
        "early_warning": False,
    }]).to_csv(outputs / "deterioration_audit.csv", index=False)

    pd.DataFrame([{
        "ai_audit_status": "COERENTE",
        "ai_audit_score": 100,
    }]).to_csv(outputs / "ai_audit_summary.csv", index=False)

    pd.DataFrame([{
        "allocation_alignment_score": 88,
        "allocation_alignment_level": "ALINHADO_AO_MODELO",
        "total_model_drift_pct": 5,
        "turnover_recommended_pct": 10,
        "top_gap_asset": "BTC-USD",
        "top_gap_abs_pct": 5,
    }]).to_csv(outputs / "allocation_advisor_summary.csv", index=False)

    pd.DataFrame([{
        "ativo": "BTC-USD",
        "peso_atual_pct": 40,
        "peso_alvo_pct": 35,
        "desvio_pct": -5,
        "acao_modelo": "REDUZIR",
        "prioridade_modelo": "MEDIA",
    }]).to_csv(outputs / "allocation_advisor.csv", index=False)

    pd.DataFrame([{
        "real_yield_10y": 1.5,
        "financial_conditions": 0.1,
        "high_yield_spread": 4.0,
        "yield_curve": 0.5,
        "dxy_proxy": 100,
        "vix": 15,
        "fed_assets": 7000000,
    }]).to_csv(outputs / "fred_macro_cache.csv", index=False)


def test_report_engine_gera_html(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_csvs_base(tmp_path)

    html = build_institutional_report()

    assert html is not None
    assert "<html>" in html


def test_report_tem_veredito(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_csvs_base(tmp_path)

    html = build_institutional_report()

    assert "APROVADO" in html


def test_report_tem_regime_macro(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_csvs_base(tmp_path)

    html = build_institutional_report()

    assert "EXPANSAO_NORMAL" in html


def test_report_tem_ai_auditor(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_csvs_base(tmp_path)

    html = build_institutional_report()

    assert "COERENTE" in html


def test_report_tem_allocation_advisor(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_csvs_base(tmp_path)

    html = build_institutional_report()

    assert "ALINHADO_AO_MODELO" in html
