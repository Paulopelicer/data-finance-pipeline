from a_backend.a_code.orchestration.validate_pipeline import main


def test_validate_pipeline_structure():
    assert main() == 0
