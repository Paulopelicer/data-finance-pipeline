# Guardrails de Código

## Regras

- Não usar hardcode de caminhos locais.
- Usar `pathlib.Path` para manipulação de caminhos.
- Centralizar caminhos em `src/config.py`.
- Usar PySpark nas transformações principais.
- Usar pandas apenas para visualização, métricas pequenas e datasets agregados.
- Não usar dados simulados como execução padrão.
- Tratar `SPARK_HOME` inválido.
- Validar outputs após execução.
- Não versionar caches, `.crc`, `_SUCCESS`, `.pipeline_runs` e dados processados reproduzíveis.
- Manter funções reutilizáveis em `src/` quando houver lógica compartilhada.

## Guardrail Code Final

- Nao hardcodar caminhos absolutos.
- Usar `pathlib.Path` para caminhos.
- Nao usar dados simulados como execucao padrao.
- Tratar ambiente Spark local e WSL.
- Validar outputs obrigatorios.
- Usar PySpark nas etapas principais do pipeline.
- Usar pandas apenas para dados agregados, reports e graficos.
- Proteger leitura de arquivos no MCP CSV.
- Manter o MCP CSV read-only.
- Nao fazer commit nem push automatico.
- Nao expor credenciais, tokens ou chaves.
