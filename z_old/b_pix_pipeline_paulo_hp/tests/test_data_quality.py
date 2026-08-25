import pytest
from src.data_quality import ensure_columns


class DummyDf:
    columns = ["a", "b"]


def test_ensure_columns_success():
    ensure_columns(DummyDf(), ["a"], "dummy")


def test_ensure_columns_failure():
    with pytest.raises(ValueError):
        ensure_columns(DummyDf(), ["c"], "dummy")
