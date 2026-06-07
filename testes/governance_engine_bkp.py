from src.governance_engine import evaluate_governance


def test_governanca_aprovada():
    result = evaluate_governance(
        macro_status="OK",
        portfolio_status="OK",
        rebalance_status="OK",
        risk_status="OK"
    )

    assert result["decision"] == "APROVADO"


def test_governanca_com_ressalvas():
    result = evaluate_governance(
        macro_status="OK",
        portfolio_status="OK",
        rebalance_status="ATENCAO",
        risk_status="OK"
    )

    assert result["decision"] in [
        "APROVADO_COM_RESSALVAS",
        "ATENCAO"
    ]


def test_governanca_reprovada_por_macro():
    result = evaluate_governance(
        macro_status="FALHA",
        portfolio_status="OK",
        rebalance_status="OK",
        risk_status="OK"
    )

    assert result["decision"] == "REPROVADO"


def test_governanca_reprovada_por_risco():
    result = evaluate_governance(
        macro_status="OK",
        portfolio_status="OK",
        rebalance_status="OK",
        risk_status="FALHA"
    )

    assert result["decision"] == "REPROVADO"


def test_governanca_todas_falhas():
    result = evaluate_governance(
        macro_status="FALHA",
        portfolio_status="FALHA",
        rebalance_status="FALHA",
        risk_status="FALHA"
    )

    assert result["decision"] == "REPROVADO"
