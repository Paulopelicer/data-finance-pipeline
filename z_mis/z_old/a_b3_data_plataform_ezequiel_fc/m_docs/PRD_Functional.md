# PRD Funcional - B3 Data Platform

| Campo     | Valor                                     |
| --------- | ----------------------------------------- |
| Produto   | B3 Data Platform (Plataforma de Dados B3) |
| Documento | Product Requirements Document (Funcional) |
| Versao    | 1.0                                       |
| Data      | 2026-07-15                                |
| Status    | Aprovado para desenvolvimento             |
| Autor     | Ezequiel FC                               |

---

## 1. Visao Geral

### 1.1 Resumo Executivo

A B3 Data Platform e uma plataforma de dados financeiros para acoes da B3
(Bolsa de Valores brasileira). Ela coleta, limpa, valida e agrega dados diarios
de precos de acoes, gerando metricas analiticas e relatorios em PDF de forma
automatizada.

### 1.2 Visao do Produto

Oferecer uma base de dados confiavel e governada de precos historicos da B3,
com metricas analiticas prontas para consumo e relatorios periodicos que apoiem
o acompanhamento de desempenho e risco de uma carteira de acoes.

### 1.3 Problema

Acompanhar o mercado acionario brasileiro exige coletar, padronizar e validar
precos de multiplas fontes, calcular metricas de risco e retorno e consolidar
tudo em relatorios. Fazer isso manualmente e propenso a erros, dificil de
reproduzir e nao escala.

### 1.4 Solucao

Um fluxo automatizado ponta a ponta que:

- Coleta dados diarios de precos de fontes de mercado.
- Aplica limpeza, deduplicacao e validacao de qualidade.
- Calcula metricas analiticas (retornos, volatilidade, retorno acumulado).
- Gera relatorios em PDF com graficos.
- Executa todo o fluxo automaticamente em dias uteis.

---

## 2. Objetivos e Metas

### 2.1 Objetivos de Produto

1. Automatizar a coleta diaria de precos de acoes da B3.
2. Garantir qualidade e consistencia dos dados por meio de validacoes.
3. Disponibilizar metricas analiticas prontas para consumo.
4. Produzir relatorios periodicos de desempenho e risco.
5. Assegurar reprodutibilidade e rastreabilidade dos dados.

### 2.2 Metricas de Sucesso (KPIs)

| Metrica                             | Meta                |
| ----------------------------------- | ------------------- |
| Acoes acompanhadas por padrao       | 12 acoes da B3      |
| Cobertura historica inicial         | 365 dias            |
| Frequencia de execucao              | Diaria (dias uteis) |
| Etapas de processamento             | 4                   |
| Checagens de qualidade na validacao | >= 4                |
| Relatorio PDF gerado por execucao   | 1                   |

### 2.3 Fora de Escopo

- Execucao de ordens (trading).
- Recomendacoes de investimento.
- Dados intradiarios (foco em fechamento diario).
- Cobertura de outras bolsas alem da B3.

---

## 3. Personas

| Persona                       | Descricao                  | Necessidade principal                       |
| ----------------------------- | -------------------------- | ------------------------------------------- |
| Analista de dados financeiros | Estuda desempenho de acoes | Metricas confiaveis e relatorios prontos    |
| Engenheiro(a) de dados        | Mantem e evolui os fluxos  | Fluxos modulares e observaveis              |
| Gestor(a) de carteira         | Acompanha risco e retorno  | Resumo de portfolio e relatorios periodicos |
| Cientista de dados            | Explora e modela dados     | Acesso a dados limpos e metricas analiticas |

---

## 4. Requisitos Funcionais

### 4.1 Coleta de Dados

**RF-01** O sistema deve coletar precos diarios de acoes (abertura, maxima,
minima, fechamento, fechamento ajustado e volume) de uma lista configuravel
de acoes.

**RF-02** O sistema deve suportar pelo menos duas fontes de dados de mercado,
sendo uma primaria e outra alternativa.

**RF-03** O sistema deve armazenar os dados brutos de forma imutavel,
registrando a origem e o momento da coleta.

**RF-04** O sistema deve tolerar falhas por acao individual, registrando o erro
e prosseguindo com as demais.

### 4.2 Limpeza e Validacao

**RF-05** O sistema deve padronizar e normalizar os dados coletados.

**RF-06** O sistema deve remover registros com valores ausentes em campos
essenciais (acao, data, preco de fechamento, volume).

**RF-07** O sistema deve remover registros com precos invalidos (zero ou
negativos).

**RF-08** O sistema deve eliminar duplicidades, mantendo o registro de maior
valor ajustado por combinacao de acao e data.

**RF-09** O sistema deve calcular o retorno diario percentual por acao.

**RF-10** O sistema deve executar checagens de qualidade que impedem a promocao
de dados invalidos, verificando: campos essenciais preenchidos, precos positivos,
ausencia de duplicidade e datas coerentes.

### 4.3 Metricas Analiticas

**RF-11** O sistema deve gerar metricas diarias por acao: preco de fechamento,
retorno diario, media movel de volume (20 dias), volatilidade anualizada
(20 dias) e retorno acumulado.

**RF-12** O sistema deve gerar um resumo por acao do periodo analisado: retorno
total, volume medio, volatilidade media, preco maximo e preco minimo.

**RF-13** O sistema deve gerar agregacoes mensais por acao: precos de abertura
e fechamento do mes, preco maximo e minimo, volume total e retorno mensal.

### 4.4 Relatorio

**RF-14** O sistema deve gerar um relatorio em PDF por execucao com graficos de:
retorno acumulado, volatilidade, risco versus retorno e distribuicao de retornos
mensais.

**RF-15** O sistema deve nomear e armazenar o relatorio com identificacao de
data e hora da geracao.

### 4.5 Orquestracao

**RF-16** O sistema deve executar as etapas em sequencia (Coleta, Limpeza,
Agregacao, Relatorio) de forma automatizada em dias uteis.

**RF-17** Cada etapa deve depender da conclusao bem-sucedida da etapa anterior.

**RF-18** O sistema deve reaplicar tentativas automaticas em caso de falha.

---

## 5. Fluxos de Uso

### 5.1 Fluxo Diario Automatizado

1. Ao final do pregao, o sistema coleta os precos do dia e armazena os dados
   brutos.
2. Os dados sao limpos, validados e enriquecidos com o retorno diario.
3. As metricas analiticas sao calculadas e consolidadas.
4. O relatorio PDF e gerado e disponibilizado.

### 5.2 Fluxo de Exploracao Interativa

1. O analista acessa o ambiente de exploracao de dados.
2. Consulta os dados limpos ou as metricas analiticas.
3. Realiza analises e gera visualizacoes sob demanda.

---

## 6. Escopo de Entrega

### 6.1 Dentro do Escopo (MVP)

- Coleta diaria de 12 acoes da B3.
- Processamento em quatro etapas (Coleta, Limpeza, Agregacao, Relatorio).
- Validacoes de qualidade antes da promocao de dados.
- Relatorio PDF automatizado.
- Orquestracao automatizada com agendamento diario.

### 6.2 Fora do Escopo (MVP)

- Dados intradiarios e streaming em tempo real.
- Dashboards interativos web.
- Alertas e notificacoes automatizadas.
- Modelos preditivos de precos.

---

## 7. Premissas e Restricoes

### 7.1 Premissas

- As fontes de dados de mercado estao disponiveis e retornam dados consistentes.
- O ambiente de execucao esta provisionado e operacional.

### 7.2 Restricoes

- Foco em dados diarios de fechamento.
- Dependencia de disponibilidade das fontes externas de dados.

---

## 8. Roadmap

| Fase   | Entrega                                                 |
| ------ | ------------------------------------------------------- |
| Fase 1 | Fluxo completo com relatorio PDF (concluido)            |
| Fase 2 | Expansao de acoes acompanhadas e indicadores adicionais |
| Fase 3 | Dashboards interativos e distribuicao de relatorios     |
| Fase 4 | Alertas de risco e deteccao de anomalias                |

---

## 9. Criterios de Aceite

- O fluxo executa ponta a ponta em dias uteis sem intervencao manual.
- As checagens de qualidade impedem a promocao de dados invalidos.
- As metricas analiticas refletem corretamente as definicoes.
- O relatorio PDF e gerado com os quatro graficos especificados.
