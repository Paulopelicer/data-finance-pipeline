from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_project_name_is_standardized():
    assert "stf_pss_ms_data_finance_pipeline" in (ROOT / "README.md").read_text(encoding="utf-8")
    assert "stf_pss_ms_data_finance_pipeline" in (ROOT / "pyproject.toml").read_text(encoding="utf-8")


def test_no_frontend_folder():
    assert not (ROOT / "c_frontend").exists()


def test_domain_pipelines_exist():
    assert (ROOT / "a_backend" / "a_code" / "pipelines" / "b3" / "run_pipeline.py").exists()
    assert (ROOT / "a_backend" / "a_code" / "pipelines" / "pix" / "run_pipeline.py").exists()


def test_orchestration_exists():
    assert (ROOT / "run_pipeline.py").exists()
    assert (ROOT / "a_backend" / "a_code" / "orchestration" / "validate_pipeline.py").exists()
