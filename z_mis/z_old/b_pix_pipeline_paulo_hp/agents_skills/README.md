# Agents e Skills

Esta pasta existe no projeto para demonstracao ao gestor e para permitir curadoria tecnica das skills usadas no contexto de Data, Analytics, BI, Ciencia de Dados e Engenharia de Dados.

## Conceito

Agents/skills sao guias especializados que orientam o Codex em tarefas especificas. Eles nao substituem o pipeline nem executam automaticamente o projeto; eles padronizam raciocinio, criterios de aceite, validacoes e respostas.

## Skills Agnosticas

As skills agnosticas podem ser usadas em outros projetos de dados:

- data-ingestion
- data-treatment
- exploratory-data-analysis
- feature-engineering
- feature-selection
- regression-modeling
- classification-modeling
- metrics-evaluation
- data-visualization
- data-quality
- documentation-prd
- run-all-pipeline
- bi-analytics
- data-engineering
- pyspark-pipeline

## Skill Especifica

- pix-pipeline-generator: especifica para projetos baseados em dados publicos do Pix.

## Como Usar No Codex

Solicite explicitamente a skill no prompt, por exemplo:

```text
Use a skill data-visualization para revisar os graficos do projeto.
```

## Como Sincronizar

```bash
python scripts/sync_agents_skills_to_codex.py
```

O script copia apenas `SKILL.md`, `agents/` e `references/` para `~/.codex/skills`.

## Como Validar

```bash
python scripts/validate_agents_skills.py
```

## Relacao Com A Lista Do Gestor

As skills cobrem ingestion, treatment, EDA, feature engineering, feature selection, regressao, classificacao, metricas, plots, qualidade, documentacao e execucao ponta a ponta.

## Observacao

As skills existem para demonstracao e reuso. Elas nao fazem parte da execucao obrigatoria do pipeline de dados.
