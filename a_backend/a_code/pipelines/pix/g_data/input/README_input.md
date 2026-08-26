# Entrada manual de dados publicos do Pix

Esta pasta e usada apenas como fallback quando a ingestao automatica pela fonte publica do Banco Central nao estiver disponivel.

O arquivo manual deve ser um CSV publico, baixado de fonte aberta, contendo no minimo as colunas:

```text
AnoMes
VALOR
QUANTIDADE
```

Fonte publica preferencial do projeto:

```text
Banco Central do Brasil - Servico OData Pix_DadosAbertos - EstatisticasTransacoesPix
```

A execucao padrao nao usa dados simulados. Se a fonte automatica falhar e nao houver CSV publico nesta pasta, o pipeline encerra com erro claro.
