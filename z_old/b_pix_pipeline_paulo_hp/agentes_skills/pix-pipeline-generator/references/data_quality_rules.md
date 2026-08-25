# Regras de Qualidade de Dados

## Schema

Validar colunas obrigatórias antes de cada etapa crítica. Quando a fonte puder variar, localizar colunas candidatas por palavras-chave e reportar ausência com mensagem clara.

## Contagem de Registros

Cada camada principal deve possuir registros. Falhar se Bronze, Silver ou Gold estiver vazia.

## Nulos

Remover registros totalmente nulos. Tratar nulos críticos com regra simples e documentada. Evitar preencher valores sem justificativa.

## Tipos

Converter datas, referência mensal, quantidades e valores financeiros para tipos adequados. Tratar valores monetários em texto e vírgula decimal.

## Ranges

Filtrar ou sinalizar valores negativos indevidos em quantidade e valor financeiro.

## Divisão por Zero

Usar regra explícita para retornar nulo quando divisor for zero ou nulo.

## Duplicidade

Avaliar duplicidades conforme granularidade da fonte. Não remover automaticamente sem entender a composição das dimensões.

## Validação Automatizada

Criar `scripts/validate_pipeline.py` para verificar arquivos, notebooks, outputs, Parquets, gráficos, ausência de emojis, ausência de hardcode e ausência de dados fictícios na execução padrão.
