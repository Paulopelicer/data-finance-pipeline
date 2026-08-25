---
name: data-engineering
description: Especialização em Engenharia de Dados, arquitetura de pipelines, data lakehouse, camadas Bronze/Silver/Gold, ingestão batch ou streaming, orquestração, modelagem analítica, governança e documentação. Use quando Codex precisar planejar, revisar, implementar ou explicar soluções de dados, pipelines ETL/ELT, data products, modern data stack ou projetos educacionais de dados.
---

# Data Engineering

## Fluxo de Trabalho

1. Entender o objetivo de negócio, a fonte, a frequência, o volume e os consumidores do dado.
2. Mapear a arquitetura de dados existente antes de propor mudanças.
3. Separar responsabilidades por camadas: ingestão, Bronze, Silver, Gold e consumo.
4. Priorizar simplicidade operacional quando o projeto for educacional ou local.
5. Documentar premissas, limitações, qualidade esperada e modo de execução.
6. Validar outputs com contagem de registros, schema, nulos, ranges e arquivos esperados.

## Padrões Recomendados

- Usar caminhos relativos e `pathlib.Path`.
- Centralizar configurações em módulo dedicado.
- Evitar credenciais, dados privados e caminhos absolutos.
- Usar Parquet nas camadas processadas.
- Manter CSV apenas para entrada manual, exportação analítica pequena ou conferência.
- Escrever scripts idempotentes para limpeza, execução e validação.
- Tratar falhas de fonte externa com fallback documentado e erro claro.

## Decisões de Arquitetura

- Para projetos iniciantes, preferir notebooks sequenciais e scripts simples de execução.
- Para pipelines recorrentes, considerar Airflow, Dagster ou Prefect.
- Para versionamento de tabelas, considerar Delta Lake ou Iceberg quando o ambiente justificar.
- Para consumo de negócio, materializar camada Gold com nomes estáveis e documentação funcional.

## Checklist

- Fonte pública ou autorizada identificada.
- Bronze preserva dado bruto.
- Silver padroniza nomes, tipos e qualidade mínima.
- Gold responde perguntas de negócio.
- Validações automatizadas existem.
- README explica instalação, execução, dados e limitações.
- `.gitignore` exclui outputs pesados e artefatos temporários.

## Referências

Leia `references/patterns.md` quando precisar de checklist mais detalhado para arquitetura, execução e revisão.
