import pandas as pd

from src.report_engine import generate_report


def fake_market():
    return {
        "market_status": "INSTITUCIONAL",
        "market_score": 85
    }


def fake_macro():
    return {
        "regime": "EXPANSAO_NORMAL",
        "signal": "RISCO_ON_VALIDADO",
        "macro_conviction": 70
    }


def fake_portfolio():
    return {
        "allocation_score": 88
    }


def fake_survival():
    return {
        "runway_months": 24,
        "ruin_risk": "BAIXO"
    }


def fake_stress():
    return {
        "stress_score": 82,
        "stress_level": "ROBUSTO"
    }


def fake_risk_budget():
    return {
        "risk_budget_score": 80,
        "risk_budget_level": "ACEITAVEL"
    }


def fake_liquidity():
    return {
        "liquidity_score": 85,
        "liquidity_level": "ROBUSTO"
    }


def fake_counterparty():
    return {
        "counterparty_score": 90,
        "counterparty_level": "ROBUSTO"
    }


def fake_governance():
    return {
        "final_verdict": "APROVADO",
        "governance_score": 90
    }


def fake_ai():
    return {
        "ai_audit_status": "COERENTE",
        "ai_audit_score": 100
    }


def test_report_engine_gera_saida():

    report = generate_report(
        fake_market(),
        fake_macro(),
        fake_portfolio(),
        fake_survival(),
        fake_stress(),
        fake_risk_budget(),
        fake_liquidity(),
        fake_counterparty(),
        fake_governance(),
        fake_ai(),
    )

    assert report is not None


def test_report_tem_veredito():

    report = generate_report(
        fake_market(),
        fake_macro(),
        fake_portfolio(),
        fake_survival(),
        fake_stress(),
        fake_risk_budget(),
        fake_liquidity(),
        fake_counterparty(),
        fake_governance(),
        fake_ai(),
    )

    assert "APROVADO" in str(report)


def test_report_tem_regime():

    report = generate_report(
        fake_market(),
        fake_macro(),
        fake_portfolio(),
        fake_survival(),
        fake_stress(),
        fake_risk_budget(),
        fake_liquidity(),
        fake_counterparty(),
        fake_governance(),
        fake_ai(),
    )

    assert "EXPANSAO_NORMAL" in str(report)


def test_report_tem_market_score():

    report = generate_report(
        fake_market(),
        fake_macro(),
        fake_portfolio(),
        fake_survival(),
        fake_stress(),
        fake_risk_budget(),
        fake_liquidity(),
        fake_counterparty(),
        fake_governance(),
        fake_ai(),
    )

    assert "85" in str(report)


def test_report_tem_ai_score():

    report = generate_report(
        fake_market(),
        fake_macro(),
        fake_portfolio(),
        fake_survival(),
        fake_stress(),
        fake_risk_budget(),
        fake_liquidity(),
        fake_counterparty(),
        fake_governance(),
        fake_ai(),
    )

    assert "100" in str(report)
