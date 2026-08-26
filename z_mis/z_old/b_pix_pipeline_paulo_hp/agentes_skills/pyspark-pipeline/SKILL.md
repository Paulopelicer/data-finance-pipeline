---
name: pyspark-pipeline
description: Especialização em PySpark para pipelines locais ou educacionais, SparkSession, leitura e escrita Parquet, transformação Silver, agregação Gold, Window Functions, tratamento de tipos, performance básica e execução em WSL. Use quando Codex precisar criar, corrigir, revisar ou otimizar código PySpark, notebooks Spark ou scripts de pipeline com Spark.
---

# PySpark Pipeline

## Fluxo de Trabalho

1. Confirmar ambiente: Python, Java, PySpark, WSL e `SPARK_HOME`.
2. Centralizar criação de `SparkSession` em função reutilizável.
3. Sanitizar `SPARK_HOME` se apontar para diretório inválido.
4. Ler dados principais com Spark quando possível.
5. Gravar Bronze, Silver e Gold em Parquet.
6. Usar pandas apenas para datasets pequenos e visualização.
7. Encerrar SparkSession ao final de notebooks e scripts.

## Padrões de Código

- Usar `mode("overwrite")` em pipelines reexecutáveis locais.
- Usar `Window.orderBy` para crescimento mês contra mês.
- Tratar divisão por zero com `F.when`.
- Converter números textuais com vírgula antes de cast.
- Evitar `collect()` em dados grandes.
- Usar `count()` apenas em validações conscientes.

## Validação

- Confirmar `_SUCCESS` e contagem maior que zero para Parquets principais.
- Validar schema antes de cálculos Gold.
- Confirmar que outputs esperados foram gerados.
- Executar `python run_pipeline.py` e `python scripts/validate_pipeline.py` quando existirem.

## Referências

Leia `references/pyspark_patterns.md` para padrões de transformação e agregação.
