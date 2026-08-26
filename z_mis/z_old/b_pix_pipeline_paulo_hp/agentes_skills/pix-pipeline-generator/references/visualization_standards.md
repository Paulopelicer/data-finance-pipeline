# Padrões de Visualização

## Regras Gerais

Todos os gráficos devem ter título, eixo X, eixo Y, legenda quando aplicável, grid discreto, fonte dos dados e boa resolução.

## Escalas

- Exibir transações em milhões ou bilhões.
- Exibir valores financeiros e economias em R$ bilhões ou R$ trilhões.
- Exibir ticket médio em reais.
- Remover notação científica dos eixos.

## Eixo X

Reduzir poluição visual usando seleção de ticks. Evitar rotação excessiva quando houver muitos meses.

## Anotações

Destacar o maior valor de cada gráfico com anotação curta. Não anotar todos os pontos.

## Fonte e Observação

Inserir rodapé:

```text
Fonte: dados públicos do Banco Central do Brasil
```

Nos gráficos de economia, inserir também:

```text
Estimativa hipotética baseada em cenários
```

## Arquivos Obrigatórios

```text
01_pix_monthly_transactions.png
02_pix_monthly_value.png
03_pix_average_ticket.png
04_pix_estimated_card_fee_savings.png
05_pix_estimated_transfer_fee_savings.png
```
