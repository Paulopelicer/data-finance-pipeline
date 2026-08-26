---
name: pix-pipeline-generator
description: Skill especifica para criar, revisar e validar o pipeline Pix com PySpark, dados publicos do Banco Central, Bronze, Silver, Gold, Analytics, ML educacional, reports, agents, skills, MCP CSV, testes e documentacao.
---

# Pix Pipeline Generator

## Purpose

Orientar a criacao, revisao e validacao do projeto Pix Data Pipeline com PySpark, dados publicos reais, arquitetura em camadas, analytics, visualizacao, testes, documentacao, agents/skills e MCP CSV.

## Scope

Tipo: Específica de domínio
Aplicação: Projetos baseados em dados públicos do Pix.
Observação: Usa padrões agnósticos das demais skills.

## When to Use

Use quando a tarefa envolver o projeto Pix, dados publicos do Banco Central, pipeline Bronze/Silver/Gold, indicadores Pix, estimativas hipoteticas de economia, notebooks, scripts, validacoes, reports ou apresentacao do projeto.

## Inputs

- Diretorio do projeto Pix.
- Requisitos de negocio e criterios de aceite.
- Fonte publica ou CSV manual em `data/input`.
- Restricoes de execucao local em VSCode e WSL.

## Outputs

- Pipeline funcional e validado.
- Notebooks sequenciais.
- Camadas Bronze, Silver e Gold.
- Reports, metricas e graficos.
- Documentacao funcional e tecnica.
- Agents/skills organizados.
- MCP CSV read-only demonstravel por CLI.

## Required Steps

1. Inspecionar estrutura atual antes de alterar arquivos.
2. Preservar regra de negocio e execucao com dados publicos reais.
3. Manter PySpark nas transformacoes principais.
4. Garantir outputs analiticos e graficos esperados.
5. Validar agents/skills e MCP CSV.
6. Executar testes unitarios e validacoes de sistema.
7. Documentar limitacoes e evolucoes futuras.

## Standards

- Usar `pathlib.Path` e caminhos relativos.
- Usar Parquet nas camadas Bronze, Silver e Gold.
- Usar CSV apenas para entrada manual ou reports analiticos pequenos.
- Usar linguagem formal, tecnica e objetiva.
- Explicitar que economias sao estimativas hipoteticas.

## Constraints

- Nao usar dados simulados como execucao padrao.
- Nao usar credenciais, tokens ou dados sensiveis.
- Nao implementar MCP Spark, PowerBI, DeltaLake ou Brain nesta versao.
- Nao fazer commit nem push sem autorizacao explicita.
- Nao usar emojis.

## Validation

Executar validacoes de sintaxe, unit tests, Test Few, pipeline completo, validacao de pipeline, validacao de agents/skills e validacao do MCP CSV.

## Acceptance Criteria

A entrega e aceita quando o pipeline funciona, os outputs existem, as skills estao organizadas, o MCP CSV e demonstravel por CLI, os guardrails estao documentados e as validacoes passam.

## Example Prompts

- Use a skill pix-pipeline-generator para revisar o projeto Pix completo.
- Use a skill pix-pipeline-generator para validar se o pipeline Pix atende aos criterios do gestor.
- Use a skill pix-pipeline-generator para explicar o projeto Pix em linguagem executiva.

## Final Response Format

Informar status do pipeline, agents/skills, MCP CSV, Brain, testes, documentacao, matriz de aderencia, arquivos alterados, comandos executados e recomendacao para Git.
