Padrões de Projeto¶
Esta seção define as convenções e padrões adotados nos projetos da Stefanini (STF). O objetivo é garantir consistência, clareza e rastreabilidade em todos os repositórios.

Nomenclatura de Repositórios¶
Todo repositório segue o padrão:

stf_pss_<tipo>_<nome>
Tipo  Descrição  Exemplo
ms  Microserviço  stf_pss_ms_graph
ap  Aplicação  stf_pss_ap_sat
cd  Cross-domain (infra, segurança, mock)  stf_pss_cd_cloud
O prefixo stf_pss identifica que o repositório pertence ao ecossistema Stefanini PSS. O tipo (ms, ap, cd) indica a natureza do projeto.

Estrutura de Pastas¶
Cada projeto segue a estrutura abaixo, com prefixos alfabéticos garantindo ordenação consistente no sistema de arquivos:

stf_pss_ms_<nome>/
├── a_backend/           # Código do backend
│   ├── a_code/          # Código-fonte principal
│   └── d_doc/           # DDL e documentação técnica
├── b_middleware/        # Camada intermediária (quando aplicável)
├── c_frontend/          # Código do frontend
│   ├── a_code/          # Código-fonte
│   └── d_doc/           # Documentação técnica do frontend
├── d_test/              # Suites de teste
│   ├── a_data_dictionary/
│   ├── b_test_unit/
│   ├── c_test_integration/
│   ├── c_test_system/
│   ├── d_test_load/
│   ├── e_test_capacity/
│   ├── f_test_performance/
│   └── g_test_security/
├── e_doc/               # Documentação geral
│   ├── 0_Context/       # Contexto e planejamento
│   ├── 1_SPC/           # Especificação funcional e técnica
│   ├── 2_BPM/           # Fluxos de processo
│   ├── 3_MER/           # Modelo de dados (ERD)
│   └── 4_Class/         # Diagrama de classes
├── f_infra/             # Infraestrutura
│   ├── a_docker/        # Docker e Docker Compose
│   └── b_terraform/     # Terraform (IaC)
└── z_mis/               # Miscelânea / rascunhos
As pastas usam letras (a_, b_, c_, ..., z_) para garantir ordenação consistente em qualquer ambiente.

Nomenclatura de Arquivos¶
Os artefatos de documentação seguem o padrão:

stf_pss_<tipo>_<nome>_<papel>_<tópico>_<timestamp>.<ext>
Exemplo de artefatos por fase:

Fase  Arquivos
1_SPC  a_CHAT_functional.md · b_SPC_functional.md · c_CHAT_technical.md · d_SPC_technical.md
2_BPM  bpm_a_CHAT_<Op>.md · bpm_b_PRD_<Op>.md · bpm_c_BPM_<Op>.drawio
3_MER  mer_a_CHAT.md · mer_b_PRD.md · mer_c_MER.mermaid
4_Class  class_a_CHAT.md · class_b_PRD.md · class_c_Class.mermaid
Timestamp: formato yymmdd_hhMM — calculado uma vez por execução e idêntico em todos os arquivos do mesmo conjunto.

Convenções de Banco de Dados¶
Tabelas¶
Padrão  Uso
{{TAG}}_TP_*  Tabelas de tipo / enum
{{TAG}}_TB_*  Tabelas de entidade de negócio
{{TAG}}_TB_*_CHANGE  Tabelas de change tracking (auditoria)
Exemplo: Para o microserviço de testes com tag SAT:

SAT_TP_TEST_STATUS      -- Tipos de status de teste
SAT_TB_TEST_CASE        -- Tabela principal de casos de teste
SAT_TB_TEST_CASE_CHANGE -- Histórico de alterações
Prefixos de Coluna¶
Prefixo  Tipo
u_  UUID
i_  Integer / Smallint
s_  String / Varchar
n_  Numeric (valores monetários)
ts_  Timestamp
b_  Boolean
Exemplo:

u_test_case_id  UUID PRIMARY KEY
i_status_id     SMALLINT
s_description   VARCHAR(255)
n_duration_ms   NUMERIC(18,2)
ts_executed_at  TIMESTAMPTZ
b_active        BOOLEAN
Padrão de Branches¶
O nome da branch segue o padrão:

<status>_<nome>_<ss>
Prefixo  Descrição
u_  Membro veterano da equipe
v_  Membro novo na equipe
Formato do nome: primeira letra do primeiro nome + primeira letra do sobrenome (ou duas primeiras letras do sobrenome se necessário).

Exemplos:

Nome Completo  Branch
Ezequiel Ferreira Cardoso  u_ezequiel_fc
Ana Paula Silva  v_ana_ps
João Victor Mendes  u_joao_vm
Padrão de Commits¶
Os commits seguem o padrão:

OK: <Tipo>: <Descrição>
NOK: <Tipo>: <Descrição>
OK vs NOK¶
Prefixo  Quando usar
OK  Completo, funcional e revisado
NOK  Trabalho em progresso, incompleto
Tipos de Commit¶
Tipo  Uso
Feat  Nova funcionalidade
Fix  Correção de bug
Doc  Documentação
Infra  Infraestrutura (Docker, Terraform, scripts)
Config  Configurações (gitignore, variáveis de ambiente)
Chore  Reorganização de pastas, renomeação, limpeza
Deploy  Scripts e automações de deploy
Test  Adição ou correção de testes
Style  Formatação, identação, espaçamento
Merge  Merge de branches
Exemplos¶
OK: Feat: Adicionar endpoint de execução de testes
OK: Fix: Corrigir falha no parser de relatório
OK: Doc: Criar SPC funcional do módulo de agendamento
OK: Infra: Configurar Docker Compose para ambiente local
OK: Chore: Reorganizar pastas do backend
OK: Test: Adicionar testes de integração

NOK: Feat: Início da implementação do dashboard
NOK: Fix: Tentativa de correção no timeout
Regras¶
Sempre iniciar com OK: ou NOK:
Descrição objetiva: o que foi feito
Para detalhes adicionais, usar o segundo -m do commit:
git commit -m "OK: Feat: Adicionar endpoint de execução" -m "Implementado o handler, validações e testes unitários"
Um commit = uma unidade lógica de trabalho