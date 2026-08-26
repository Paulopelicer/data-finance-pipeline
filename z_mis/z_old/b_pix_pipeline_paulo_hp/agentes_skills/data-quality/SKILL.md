---
name: data-quality
description: Especialização em qualidade de dados, validação de pipelines, checks de schema, nulos, duplicidade, ranges, contagem de registros, integridade de outputs, critérios de aceite e documentação de falhas. Use quando Codex precisar criar, revisar ou executar validações em pipelines, tabelas, notebooks ou outputs analíticos.
---

# Data Quality

## Fluxo de Trabalho

1. Definir o que precisa existir: arquivos, tabelas, colunas e gráficos.
2. Validar se datasets não estão vazios.
3. Confirmar schema mínimo antes de transformação ou agregação.
4. Verificar nulos em colunas críticas.
5. Verificar valores negativos indevidos e ranges esperados.
6. Validar outputs finais após execução.
7. Gerar mensagens de erro acionáveis.

## Checks Essenciais

- Existência de diretórios e arquivos obrigatórios.
- JSON válido para notebooks.
- Imports e sintaxe válidos.
- Tabelas Parquet legíveis.
- Contagem de registros maior que zero.
- Colunas obrigatórias presentes.
- Ausência de caminhos absolutos locais em código versionado.
- Ausência de dados fictícios em execução padrão quando o requisito exigir dado real.

## Boas Práticas

- Separar validação estrutural, validação de dados e validação de apresentação.
- Falhar rápido quando uma etapa crítica estiver ausente.
- Reportar todos os erros encontrados ao final quando possível.
- Não mascarar falhas de fonte externa com dados fictícios.

## Referências

Leia `references/checklists.md` para checklists prontos de validação.
