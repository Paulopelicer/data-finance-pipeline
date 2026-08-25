# Padrões PySpark

## SparkSession

Use `.master("local[*]")`, timezone explícita e log level `WARN` em projetos locais.

## Transformações

- `withColumn` para colunas derivadas.
- `groupBy().agg()` para Gold.
- `lag().over(Window.orderBy(...))` para crescimento temporal.
- `when(...).otherwise(...)` para regras com nulos ou divisão por zero.

## Escrita

Parquet para camadas processadas. CSV somente para amostras ou consumo analítico pequeno.
