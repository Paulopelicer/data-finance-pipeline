from pathlib import Path
from a_configs.utils import remove_path


def test_remove_path_file(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("x", encoding="utf-8")
    remove_path(path)
    assert not path.exists()
