# Fontes de Dados

## Fonte Preferencial

Usar dados públicos reais do Banco Central do Brasil relacionados ao Pix, preferencialmente via API OData ou arquivos públicos oficiais.

Exemplo de referência pública aceitável:

```text
https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/
```

## Regras de Ingestão

- Tentar ingestão automática pela fonte pública.
- Validar resposta, registros e colunas mínimas.
- Registrar origem usada, URL ou arquivo manual e quantidade de registros.
- Documentar fonte no README e PRDs.

## Fallback Manual

Se a ingestão automática falhar, procurar CSV público real em `data/input`. O arquivo deve ser baixado manualmente de fonte pública e documentada.

## Proibições

- Não usar dados simulados como execução padrão.
- Não substituir silenciosamente fonte real por massa fictícia.
- Não usar credenciais, tokens, dados internos ou dados sensíveis.

## Falha Esperada

Se não houver fonte pública automática disponível nem CSV público manual, o pipeline deve falhar com mensagem clara orientando o usuário a fornecer dado público real.
