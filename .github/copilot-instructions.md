# Copilot Instructions for Data Finance

## Objetivo
Este projeto integra pipeline financeiro B3, qualidade de dados, orquestração e relatórios. O agente deve pensar em arquitetura, qualidade e governança antes de implementar mudanças.

## Diretrizes principais
- Preservar a arquitetura atual do pipeline e a estrutura de camadas.
- Priorizar dados financeiros reais, contratos de schema e validação.
- Manter consistência entre Bronze, Silver, Gold e relatórios.
- Documentar premissas, riscos e pendências quando houver limitação.
- Usar skills especializadas do Data Finance para tarefas de ingestão, qualidade, orquestração e relatórios.

## Agentes recomendados
- Finance Pipeline Architect
- B3 Market Data Engineer
- Data Quality & Contracts
- Silver/Gold Transformation Lead
- Airflow & Orchestration Specialist
- Reports & BI Analyst
- Debug & Reliability Responder
- Test & Validation Engineer
- Documentation & Governance Lead

## Fluxo operacional
1. Especificar escopo
2. Planejar impacto e arquivos
3. Implementar com critério de aceite
4. Validar qualidade, testes e saída
5. Revisar documentação e riscos

## Restrições
- Sem hardcoded paths locais
- Sem credenciais ou secrets em código
- Sem emojis em artefatos de instrução
- Sem assumir qualidade sem validação
