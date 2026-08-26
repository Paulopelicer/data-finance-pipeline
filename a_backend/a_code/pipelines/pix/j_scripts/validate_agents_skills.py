"""Valida agents/skills locais usados para apresentacao e reuso."""

from __future__ import annotations

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SKILLS_DIR = BASE_DIR / "k_agents_skills"
REQUIRED_SECTIONS = [
    "Purpose",
    "Scope",
    "When to Use",
    "Inputs",
    "Outputs",
    "Required Steps",
    "Standards",
    "Constraints",
    "Validation",
    "Acceptance Criteria",
    "Example Prompts",
]
REQUIRED_SKILLS = [
    "data-ingestion",
    "data-treatment",
    "exploratory-data-analysis",
    "feature-engineering",
    "feature-selection",
    "regression-modeling",
    "classification-modeling",
    "metrics-evaluation",
    "data-visualization",
    "data-quality",
    "documentation-prd",
    "run-all-pipeline",
    "bi-analytics",
    "data-engineering",
    "pyspark-pipeline",
    "pix-pipeline-generator",
]
EMOJI_RE = re.compile(
    "[" "\U0001f300-\U0001faff" "\U00002700-\U000027bf" "\U00002600-\U000026ff" "]"
)
LOCAL_PATH_RE = re.compile(
    r"/home/|/mnt/" + "c/Users/" + r"|[A-Za-z]:" + r"\\", re.IGNORECASE
)


def validate_skill(skill_name: str, errors: list[str]) -> None:
    skill_dir = SKILLS_DIR / skill_name
    skill_md = skill_dir / "SKILL.md"
    yaml_path = skill_dir / "agents" / "openai.yaml"
    refs_dir = skill_dir / "references"
    if not skill_dir.exists():
        errors.append(f"skill ausente: {skill_name}")
        return
    for path in [skill_md, yaml_path, refs_dir]:
        if not path.exists():
            errors.append(
                f"artefato ausente em {skill_name}: {path.relative_to(skill_dir)}"
            )
    checklist = refs_dir / "checklist.md"
    if refs_dir.exists() and not checklist.exists():
        errors.append(f"checklist ausente em {skill_name}: references/checklist.md")
    if not skill_md.exists():
        return
    text = skill_md.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"secao ausente em {skill_name}: {section}")
    for path in skill_dir.rglob("*"):
        if path.is_file():
            content = path.read_text(encoding="utf-8", errors="ignore")
            if EMOJI_RE.search(content):
                errors.append(f"emoji encontrado em {path.relative_to(SKILLS_DIR)}")
            if LOCAL_PATH_RE.search(content):
                errors.append(
                    f"caminho local encontrado em {path.relative_to(SKILLS_DIR)}"
                )
    if skill_name != "pix-pipeline-generator" and "Pix" in text:
        errors.append(
            f"skill agnostica contem dependencia textual de Pix: {skill_name}"
        )
    if skill_name != "pix-pipeline-generator" and "Tipo: Agnóstica" not in text:
        errors.append(f"skill agnostica sem classificacao obrigatoria: {skill_name}")
    if skill_name == "pix-pipeline-generator" and "específica" not in text.lower():
        errors.append("skill pix-pipeline-generator nao esta marcada como especifica")


def main() -> int:
    errors: list[str] = []
    for skill in REQUIRED_SKILLS:
        validate_skill(skill, errors)
    if errors:
        print("Validacao de agents/skills concluida com falhas.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validacao de agents/skills concluida com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
