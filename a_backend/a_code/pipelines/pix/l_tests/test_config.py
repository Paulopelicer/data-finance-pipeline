from a_configs.config import BASE_DIR, DATA_DIR, create_project_directories


def test_base_dir_exists():
    assert BASE_DIR.exists()


def test_create_project_directories():
    create_project_directories(False)
    assert DATA_DIR.exists()
