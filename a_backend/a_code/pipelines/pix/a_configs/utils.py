"""Utilitarios compartilhados do projeto."""

from pathlib import Path
import shutil


def remove_path(path: Path) -> None:
    """Remove arquivo ou diretorio se existir."""
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def clear_directory_contents(directory: Path) -> None:
    """Remove todo o conteudo de um diretorio mantendo a pasta."""
    directory.mkdir(parents=True, exist_ok=True)
    for child in directory.iterdir():
        remove_path(child)
