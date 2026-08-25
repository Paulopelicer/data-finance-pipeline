# Matriz De Aderencia Aos Requisitos

| Categoria | Item | Status | Artefato | Observacao | Nota sugerida de 0 a 4 |
|---|---|---|---|---|---|
| Domain | MCP CSV | Implementado | `mcp/csv_mcp_server.py`, `mcp/tools/csv_tools.py`, `mcp/README.md`, `mcp/CODEX_MCP_SETUP.md` | MCP read-only nativo via stdio e CLI para CSVs de `reports/` | 4 |
| Domain | MCP Spark | Evolucao futura | `mcp/README.md` | Nao implementado nesta versao por decisao de escopo | 0 |
| Domain | MCP PowerBI | Evolucao futura | `mcp/README.md` | Nao implementado nesta versao por decisao de escopo | 0 |
| Domain | MCP DeltaLake | Evolucao futura | `mcp/README.md` | Nao implementado nesta versao por decisao de escopo | 0 |
| Domain | MCP Brain | Evolucao futura | `mcp/README.md` | Nao implementado nesta versao | 0 |
| Domain | Agent | Implementado | `agents_skills/` | Skills com metadados `agents/openai.yaml` | 4 |
| Domain | Skill | Implementado | `agents_skills/*/SKILL.md` | Skills agnosticas e skill especifica Pix | 4 |
| Domain | Brain | Implementado como base documental | `docs/knowledge_base/` | Markdown compatível com curadoria documental; sem MCP Brain | 3 |
| SPC | Functional | Implementado | `docs/PRD_Functional.md` | Escopo funcional atualizado | 4 |
| SPC | Technical | Implementado | `docs/PRD_Technical.md` | Arquitetura tecnica atualizada | 4 |
| Guardrail | Doc | Implementado | `docs/guardrails.md` | Regras de linguagem, fonte e limitacoes | 4 |
| Guardrail | Code | Implementado | `docs/code_guardrails.md` | Regras de codigo, paths, dados e MCP CSV | 4 |
| Test | Unit | Implementado | `tests/` | Testes PyTest incluindo MCP CSV | 4 |
| Test | System | Implementado | `run_pipeline.py`, `scripts/validate_pipeline.py`, `scripts/test_few.py` | Test Few, Test All e validacao | 4 |
| Analytics | Ingestion | Implementado | `notebooks/01_bronze_ingestion_pix.ipynb` | Ingestao de dados publicos reais | 4 |
| Analytics | Treatment | Implementado | `notebooks/02_silver_transform_pix.ipynb` | Tratamento Silver | 4 |
| Analytics | EDA | Implementado | `notebooks/03_eda_pix.ipynb` | Analise exploratoria | 4 |
| Analytics | New Feature | Implementado | `notebooks/06_feature_engineering_pix.ipynb` | Features analiticas | 4 |
| Analytics | Feature Selection | Implementado | `notebooks/07_feature_selection_pix.ipynb` | Selecao de variaveis | 4 |
| Analytics | Prediction Regression | Implementado | `notebooks/08_prediction_regression_pix.ipynb` | Modelo educacional de regressao | 4 |
| Analytics | Prediction Classification | Implementado | `notebooks/09_prediction_classification_pix.ipynb` | Modelo educacional de classificacao | 4 |
| Analytics | Metrics | Implementado | `notebooks/10_metrics_pix.ipynb`, `reports/*.csv` | RMSE, MAE, R2, accuracy, precision, recall e f1-score quando aplicavel | 4 |
| Analytics | Plots | Implementado | `reports/figures/*.png` | Graficos formatados para apresentacao | 4 |
| Analytics | Test Few | Implementado | `scripts/test_few.py` | Amostra proxima de 500 linhas | 4 |
| Analytics | Test All | Implementado | `run_pipeline.py` | Execucao completa | 4 |
| Analytics | Run All Notebook | Implementado | `notebooks/00_run_all.ipynb` | Orquestracao via notebook | 4 |
| Other | GitHub | Parcial | Repositorio local | Alteracoes locais; commit e push nao executados por regra do prompt | 3 |
| Other | Planilha | Nao aplicavel | Nao disponivel | Nao ha acesso a planilha da equipe neste ambiente | 0 |
| Other | Agnostic | Implementado | `agents_skills/` | Skills majoritariamente reutilizaveis | 4 |
| Other | Explanation | Implementado | `README.md`, `docs/agents_inventory.md`, `mcp/README.md` | Material de apoio para apresentacao | 4 |
