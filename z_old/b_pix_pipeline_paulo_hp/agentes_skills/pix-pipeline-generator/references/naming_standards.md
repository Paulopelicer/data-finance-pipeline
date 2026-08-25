# Padrões de Nomeação

## Arquivos

Usar nomes minúsculos, descritivos e sequenciais para notebooks e gráficos. Evitar espaços e caracteres especiais em nomes de arquivos.

## Colunas Técnicas

Usar `snake_case` e sem acentos em nomes técnicos:

```text
ano_mes
quantidade_transacoes
valor_total
ticket_medio
crescimento_qtd_mes_anterior
crescimento_valor_mes_anterior
```

## Títulos e Textos Visuais

Usar acentuação correta em títulos, eixos, legendas, README e PRDs.

## Caminhos

Usar `pathlib.Path`, caminhos relativos e constantes centralizadas em `src/config.py`. Não usar caminhos locais absolutos.

## Padronização de Colunas

Implementar função para normalizar nomes de colunas de origem, removendo acentos, convertendo para minúsculas e substituindo separadores por `_`.
