# Regras de Estimativa de Economia

## Conceito Obrigatório

A análise de economia potencial é baseada em cenários hipotéticos. Os dados públicos não identificam qual meio de pagamento cada transação Pix substituiu. Por isso, os valores calculados não representam economia real comprovada, mas sim uma simulação analítica para fins educacionais.

## Cenários de Cartão

Cenários mínimos:

```text
Conservador - débito: 10% do valor Pix substituiu cartão de débito.
Moderado - débito: 20% do valor Pix substituiu cartão de débito.
Conservador - crédito: 10% do valor Pix substituiu cartão de crédito.
Moderado - crédito: 20% do valor Pix substituiu cartão de crédito.
```

Taxas de referência didáticas:

```text
MDR débito: 1,08%
MDR crédito: 2,26%
```

Fórmula:

```text
economia_estimada_cartao = valor_total_pix * percentual_substituicao * taxa_mdr
```

## Cenários de Transferência

Cenários mínimos:

```text
Conservador - transferência: 5% das transações Pix substituíram transferências tradicionais.
Moderado - transferência: 10% das transações Pix substituíram transferências tradicionais.
Agressivo - transferência: 20% das transações Pix substituíram transferências tradicionais.
```

Tarifas hipotéticas:

```text
tarifa_baixa = 5.00
tarifa_media = 10.00
tarifa_alta = 15.00
```

Fórmula:

```text
economia_estimada_transferencia = quantidade_transacoes_pix * percentual_substituicao * tarifa_referencia
```

## Linguagem Correta

Usar sempre termos como `estimativa hipotética`, `cenário`, `potencial estimado` e `fins educacionais`. Não afirmar economia real comprovada.
