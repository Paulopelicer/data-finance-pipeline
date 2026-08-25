# Padrões de Engenharia de Dados

## Arquitetura em Camadas

Bronze deve manter dados próximos da origem. Silver deve padronizar estrutura, tipos e qualidade. Gold deve entregar métricas de negócio prontas para consumo.

## Validação Mínima

- Arquivos e diretórios esperados existem.
- Tabelas principais possuem registros.
- Schemas têm colunas obrigatórias.
- Datas e valores numéricos foram convertidos corretamente.
- Não há fallback silencioso para dados fictícios em execução padrão.

## Documentação

Documentar fonte, arquitetura, notebooks, scripts, premissas, limitações, comandos de execução e troubleshooting.
