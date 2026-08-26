from src.feature_engineering import calculate_rmse


def test_rmse():
    assert calculate_rmse(9) == 3
