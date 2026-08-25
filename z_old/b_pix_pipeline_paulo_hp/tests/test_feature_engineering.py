from src.feature_engineering import calculate_card_savings, calculate_growth_percent, calculate_ticket_medio, calculate_transfer_savings


def test_ticket_medio():
    assert calculate_ticket_medio(100, 4) == 25
    assert calculate_ticket_medio(100, 0) is None


def test_growth_percent():
    assert calculate_growth_percent(120, 100) == 20
    assert calculate_growth_percent(120, 0) is None


def test_savings():
    assert calculate_card_savings(1000, 0.1, 0.02) == 2
    assert calculate_transfer_savings(100, 0.1, 5) == 50
