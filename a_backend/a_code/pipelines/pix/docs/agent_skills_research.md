# Pesquisa e Organização de Agents/Skills

## Objetivo

Documentar as skills criadas para apoiar projetos de Data & Analytics, Engenharia de Dados, BI, qualidade, modelagem e visualização.

## Skills Agnósticas

As skills agnósticas em `agents_skills/` foram criadas para uso em diferentes domínios, como dados públicos, vendas, crédito, cartões, operações, governo e pipelines PySpark ou pandas.

## Skill Específica Pix

A skill `pix-pipeline-generator` é específica para o projeto Pix e atua como orquestradora do caso de uso aplicado.

## Relação com o Projeto

As skills representam padrões extraídos do projeto Pix, mas não são necessárias para executar o pipeline. Elas apoiam documentação, apresentação e reutilização futura.

## Status

Implementado para apresentação local. MCP não foi implementado nesta versão.

## Curadoria Final Para MCP CSV

Repositorios considerados como referencia conceitual de curadoria:

- https://github.com/Paulopelicer/stf_pss_da_agent
- https://github.com/GMiraaa/stf_pss_de_agent
- https://github.com/DanielgSantos6/stf_pss_ds_agent

O que foi aproveitado:

- Separacao de responsabilidades por dominio de dados.
- Organizacao de skills agnosticas para Data Analytics, Data Engineering e Data Science.
- Necessidade de validacao automatizada e linguagem adequada para apresentacao.

Nesta versao, nao foi copiado repositorio inteiro nem foram trazidos artefatos externos para dentro do projeto. A implementacao do MCP CSV foi feita localmente, com foco em leitura segura de CSVs analiticos em `reports/`.

Classificacao:

- Skills agnosticas: reutilizaveis em projetos de dados, analytics, BI e ciencia de dados.
- Skill `pix-pipeline-generator`: especifica para dados publicos do Pix.
- MCP CSV: especifico para consulta read-only dos CSVs analiticos deste projeto, mas o padrao pode ser reutilizado em outros projetos com reports CSV.
