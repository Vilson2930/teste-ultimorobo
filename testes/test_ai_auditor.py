import pandas as pd

from src.ai_auditor import run_ai_auditor


def criar_outputs_base(tmp_path):
    outputs = tmp_path / "outputs"
    outputs.mkdir()

    pd.DataFrame([{
        "runway_months": 24,
        "ruin_risk": "BAIXO",
        "survival_kill_switch": False,
    }]).to_csv(outputs / "survival_audit.csv", index=False)

    pd.DataFrame([{
        "stress_score": 80,
        "stress_level": "ACEITAVEL",
        "forced_selling_any": False,
    }]).to_csv(outputs / "stress_summary_v2.csv", index=False)

    pd.DataFrame([{
        "risk_budget_score": 85,
        "risk_budget_level": "ROBUSTO",
        "top_risk_asset": "BTC-USD",
        "max_risk_contribution_pct": 35,
    }]).to_csv(outputs / "risk_budget_summary.csv", index=False)

    pd.DataFrame([{
        "liquidity_score": 80,
        "liquidity_level": "ACEITAVEL",
    }]).to_csv(outputs / "liquidity_summary.csv", index=False)

    pd.DataFrame([{
        "counterparty_score": 80,
        "counterparty_level": "ACEITAVEL",
    }]).to_csv(outputs / "counterparty_summary.csv", index=False)

    pd.DataFrame([{
        "final_verdict": "APROVADO",
        "committee_action": "MANTER_APROVADO",
    }]).to_csv(outputs / "risk_committee_integrated.csv", index=False)


def test_ai_auditor_gera_saida(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_outputs_base(tmp_path)

    result = run_ai_auditor()

    assert "ai_audit_summary" in result
    assert "ai_audit_details" in result


def test_ai_auditor_status_coerente(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_outputs_base(tmp_path)

    result = run_ai_auditor()
    summary = result["ai_audit_summary"]

    assert summary.iloc[0]["ai_audit_status"] == "COERENTE"


def test_ai_auditor_score_100(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_outputs_base(tmp_path)

    result = run_ai_auditor()
    summary = result["ai_audit_summary"]

    assert summary.iloc[0]["ai_audit_score"] == 100


def test_ai_auditor_detecta_survival_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_outputs_base(tmp_path)

    pd.DataFrame([{
        "runway_months": 6,
        "ruin_risk": "ALTO",
        "survival_kill_switch": True,
    }]).to_csv("outputs/survival_audit.csv", index=False)

    result = run_ai_auditor()
    summary = result["ai_audit_summary"]

    assert summary.iloc[0]["root_cause"] == "RISCO_OPERACIONAL_DE_SOBREVIVENCIA"


def test_ai_auditor_detecta_forced_selling(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    criar_outputs_base(tmp_path)

    pd.DataFrame([{
        "stress_score": 40,
        "stress_level": "CRITICO",
        "forced_selling_any": True,
    }]).to_csv("outputs/stress_summary_v2.csv", index=False)

    result = run_ai_auditor()
    summary = result["ai_audit_summary"]

    assert summary.iloc[0]["root_cause"] == "FORCED_SELLING"
