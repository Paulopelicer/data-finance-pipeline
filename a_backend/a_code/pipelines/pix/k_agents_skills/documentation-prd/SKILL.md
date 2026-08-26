---
name: documentation-prd
description: Skill agnostica para orientar tarefas de Documentation PRD em projetos de dados, analytics, BI, ciencia de dados e engenharia de dados.
---

# Documentation PRD

## Purpose

Orientar a execucao de tarefas de Documentation PRD com padrao tecnico reutilizavel, validavel e independente de dominio.

## Scope

Tipo: Agnóstica
Aplicação: Qualquer projeto de Engenharia de Dados, Analytics, BI ou Ciência de Dados.

## When to Use

Use quando o usuario solicitar criacao, revisao, melhoria, validacao ou explicacao relacionada a documentacao funcional, tecnica, PRDs e matriz de aderencia.

## Inputs

- Objetivo da analise ou pipeline.
- Fonte ou dataset disponivel.
- Regras tecnicas e de negocio.
- Criterios de aceite.

## Outputs

- Artefatos tecnicos coerentes com a tarefa.
- Documentacao objetiva.
- Validacao aplicavel.
- Resumo final com limitacoes.

## Required Steps

1. Entender contexto, dados disponiveis e objetivo de negocio.
2. Preservar a logica existente quando houver projeto em andamento.
3. Implementar ou revisar a solucao com simplicidade e rastreabilidade.
4. Documentar premissas, limitacoes e comandos.
5. Validar outputs e informar resultados.

## Standards

- Usar linguagem formal e tecnica.
- Usar nomes claros e `snake_case` quando aplicavel.
- Preferir caminhos relativos e configuracao centralizada.
- Separar dados brutos, tratados e analiticos quando houver pipeline.
- Manter os artefatos adequados para execucao local em WSL quando aplicavel.

## Constraints

- Nao usar emojis.
- Nao hardcodar caminhos locais.
- Nao usar credenciais, tokens ou dados sensiveis.
- Nao fazer commit nem push sem autorizacao explicita.
- Nao afirmar causalidade, economia real ou previsao oficial sem base tecnica.

## Validation

Validar arquivos, dados, metricas, graficos ou documentacao conforme a tarefa. Reportar falhas de forma objetiva e acionavel.

## Acceptance Criteria

A tarefa deve estar concluida quando os artefatos esperados existirem, as validacoes passarem e as limitacoes estiverem documentadas.

## Example Prompts

- Use a skill documentation-prd para revisar uma etapa de documentacao funcional, tecnica, PRDs e matriz de aderencia.
- Use a skill documentation-prd para criar artefatos tecnicos reutilizaveis em um projeto de dados.
- Use a skill documentation-prd para validar criterios de aceite e documentar pendencias.

## Final Response Format

Informar alteracoes, arquivos criados, validacoes executadas, resultado e pendencias.
