# Agentes e Skills do Projeto Pix

Esta pasta foi criada apenas para apresentação. Ela contém uma cópia das skills pessoais do Codex relacionadas ao projeto Pix e a temas de Data, Analytics, Engenharia de Dados, BI, qualidade e visualização.

As skills originais continuam em `~/.codex/skills`. Esta cópia não é necessária para a execução do pipeline Pix e não deve ser versionada no Git.

## Skills Copiadas

| Skill | Finalidade |
| --- | --- |
| `pix-pipeline-generator` | Gerar, revisar e validar projetos completos de Engenharia de Dados do Pix com PySpark, Bronze, Silver, Gold, documentação, PRDs, gráficos e validação final. |
| `data-engineering` | Orientar arquitetura de pipelines, Data Lake, camadas Bronze/Silver/Gold, ingestão, transformação, governança e documentação. |
| `pyspark-pipeline` | Orientar implementação e revisão de pipelines PySpark, SparkSession, Parquet, transformações, agregações e execução local em WSL. |
| `data-quality` | Orientar validações de estrutura, schema, contagem de registros, nulos, ranges, outputs e critérios de aceite. |
| `bi-analytics` | Orientar KPIs, camada Gold, métricas de negócio, leitura executiva, PRDs funcionais e storytelling analítico. |
| `data-visualization` | Orientar criação e melhoria de gráficos, escalas, eixos, legendas, fonte dos dados, formatação monetária e apresentação. |

## Como Demonstrar ao Gestor

1. Abrir esta pasta no VSCode.
2. Mostrar que cada skill possui `SKILL.md`, `agents/openai.yaml` e, quando aplicável, arquivos em `references/`.
3. Explicar que `SKILL.md` contém as regras principais que orientam o Codex.
4. Explicar que `references/` contém instruções complementares carregadas conforme a necessidade da tarefa.
5. Demonstrar o uso com um prompt como:

```text
Use $pix-pipeline-generator para criar um projeto completo de Engenharia de Dados com PySpark sobre dados públicos do Pix, contendo Bronze/Silver/Gold, README, PRD funcional, PRD técnico, notebooks, scripts, gráficos e validação final.
```

## Observação

Esta pasta é apenas uma cópia para apresentação. Para uso real no Codex, as skills devem permanecer em `~/.codex/skills`.
