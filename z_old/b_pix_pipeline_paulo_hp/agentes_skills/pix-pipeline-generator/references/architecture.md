# Arquitetura do Pipeline Pix

## Visão Geral

O projeto deve implementar uma arquitetura local de Engenharia de Dados em camadas, com ingestão de dados públicos reais do Pix, processamento com PySpark e geração de indicadores para consumo analítico.

## Fluxo Principal

```text
Fonte pública Banco Central
        |
        v
Ingestão
        |
        v
Bronze Parquet
        |
        v
Silver Parquet
        |
        v
Gold Parquet
        |
        v
Reports e visualizações
```

## Camada Bronze

A Bronze deve preservar os dados próximos da origem, sem transformações complexas. O objetivo é rastreabilidade e reprocessamento.

## Camada Silver

A Silver deve conter dados limpos, padronizados e com tipos adequados. Deve resolver nomes de colunas, datas, valores numéricos, nulos e registros inválidos.

## Camada Gold

A Gold deve conter dados orientados ao consumo, com indicadores mensais, estimativas de economia e exports analíticos pequenos quando necessário.

## Uso de PySpark

Usar PySpark para leitura principal, transformação, agregação, cálculo de indicadores e escrita em Parquet. Usar pandas apenas quando o dataset já for pequeno ou para visualização.

## Relação com BI

A camada Gold deve responder perguntas de negócio, apoiar visualizações e oferecer métricas com fórmulas documentadas.
