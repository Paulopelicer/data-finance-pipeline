"""Sincroniza skills locais do projeto para o diretorio operacional do Codex."""

from __future__ import annotations

import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_DIR / "agents_skills"
TARGET_DIR = Path.home() / ".codex" / "skills"
ALLOWED_NAMES = {"SKILL.md", "agents", "references"}


def copy_skill(skill_dir: Path) -> str:
    target_skill = TARGET_DIR / skill_dir.name
    if target_skill.exists():
        shutil.rmtree(target_skill)
    target_skill.mkdir(parents=True, exist_ok=True)
    for item in skill_dir.iterdir():
        if item.name not in ALLOWED_NAMES:
            continue
        target = target_skill / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        elif item.is_file():
            shutil.copy2(item, target)
    return skill_dir.name


def main() -> int:
    if not SOURCE_DIR.exists():
        print("Pasta agents_skills nao encontrada.")
        return 1
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    copied = [copy_skill(path) for path in sorted(SOURCE_DIR.iterdir()) if path.is_dir()]
    print("Sincronizacao concluida.")
    print(f"Origem: {SOURCE_DIR.relative_to(PROJECT_DIR)}")
    print("Destino: ~/.codex/skills")
    print(f"Skills copiadas: {len(copied)}")
    for name in copied:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

