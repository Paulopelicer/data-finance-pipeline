from pathlib import Path

import pytest

from h_mcp.tools.csv_tools import (
    csv_describe_file,
    csv_list_reports,
    csv_preview_file,
    csv_validate_columns,
)


def test_csv_list_reports_returns_structure():
    result = csv_list_reports()
    assert "csv_files" in result
    assert isinstance(result["csv_files"], list)


def test_csv_preview_blocks_path_traversal():
    with pytest.raises(ValueError):
        csv_preview_file("../README.md")


def test_csv_preview_blocks_absolute_path():
    with pytest.raises(ValueError):
        csv_preview_file(str(Path.cwd() / "reports" / "regression_metrics.csv"))


def test_csv_describe_and_validate_columns_when_report_exists():
    reports = csv_list_reports()["csv_files"]
    if not reports:
        pytest.skip("Nenhum CSV em reports para validar.")
    file_name = reports[0]["path"]
    description = csv_describe_file(file_name)
    assert description["row_count"] >= 0
    columns = description["columns"]
    result = csv_validate_columns(file_name, columns[:1])
    assert result["valid"] is True
