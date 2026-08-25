# Checklist de Validação

## Estrutura

- `README.md` existe.
- `requirements.txt` existe.
- `.gitignore` existe.
- `run_pipeline.py` existe.
- `src/` contém módulos esperados.
- `scripts/` contém limpeza, execução e validação.
- `notebooks/` contém cinco notebooks sequenciais.
- `docs/` contém PRD funcional e PRD técnico.
- `data/input/README_input.md` existe.

## Execução

Executar:

```bash
python -m compileall src scripts
python run_pipeline.py
python scripts/validate_pipeline.py
```

## Dados

- Bronze possui registros.
- Silver possui registros.
- Gold indicadores possui registros.
- Tabelas de estimativa possuem registros.
- Parquets são legíveis pelo Spark.

## Outputs

- Cinco gráficos existem em `reports/figures`.
- Gráficos têm nomes padronizados.
- Exports CSV pequenos existem apenas quando previstos.

## Documentação

- README explica instalação, execução e validação.
- PRDs explicam contexto funcional e técnico.
- Fonte pública está documentada.
- Premissas de economia estão documentadas.
- Limitações estão explícitas.

## Qualidade de Código

- Não há hardcode de caminhos locais.
- Não há emojis.
- Não há dados simulados como execução padrão.
- `SPARK_HOME` inválido é tratado.
- `.gitignore` ignora caches, outputs e artefatos Spark.

## Git

- `git status` não deve mostrar artefatos inesperados.
- Não fazer commit nem push sem autorização explícita.
