# Configuracao Do MCP CSV No Codex

Este documento explica como conectar o MCP CSV ao Codex no VSCode ou Codex CLI em ambiente WSL.

## Objetivo

Depois da configuracao, o Codex pode chamar as ferramentas do MCP CSV pelo chat, sem que o usuario precise executar manualmente os comandos CLI.

Exemplos de pedidos no chat:

```text
Use o MCP CSV para listar os reports disponiveis.
```

```text
Use o MCP CSV para resumir as metricas principais do projeto Pix.
```

```text
Use a skill bi-analytics com o MCP CSV para criar uma narrativa executiva dos resultados.
```

## Modos Disponiveis

O arquivo `mcp/csv_mcp_server.py` suporta dois modos:

- MCP nativo via `stdio`: `python mcp/csv_mcp_server.py`
- CLI demonstravel: `python mcp/csv_mcp_server.py --tool csv_get_metrics_summary`

## Configuracao Em ``config.toml` do Codex`

Use um caminho absoluto Linux valido dentro do WSL. Nao use formato de caminho nativo do Windows.

Modelo recomendado:

```toml
[mcp_servers.pix-csv-mcp]
command = "python"
args = ["/CAMINHO/ABSOLUTO/DO/PROJETO/mcp/csv_mcp_server.py"]
```

Modelo alternativo, caso a sua versao do Codex use lista de servidores:

```toml
[[mcp_servers]]
name = "pix-csv-mcp"
command = "python"
args = ["/CAMINHO/ABSOLUTO/DO/PROJETO/mcp/csv_mcp_server.py"]
```

No WSL, o caminho geralmente segue o padrao `/mnt/c/...`. Use `pwd` dentro da pasta do projeto para obter o caminho correto.

## Passo A Passo

1. Abra o terminal WSL.
2. Entre na pasta do projeto.
3. Execute `pwd`.
4. Copie o caminho retornado.
5. Edite ``config.toml` do Codex`.
6. Adicione um dos blocos TOML acima, substituindo o placeholder.
7. Reinicie o Codex ou o VSCode.
8. Teste pelo chat do Codex.

## Validacao Local

Antes de configurar no Codex, valide o servidor:

```bash
python scripts/validate_mcp_csv.py
```

Teste a CLI:

```bash
python mcp/csv_mcp_server.py --list-tools
python mcp/csv_mcp_server.py --tool csv_get_metrics_summary
```

## Seguranca

O MCP CSV e read-only. Ele:

- le apenas arquivos `.csv`;
- restringe leitura a `reports/`;
- bloqueia caminhos absolutos em argumentos;
- bloqueia `..`;
- limita linhas retornadas;
- nao altera dados;
- nao executa commit ou push.

## Pontos De Atencao

- O servidor MCP depende dos CSVs gerados em `reports/`.
- Se `reports/` estiver vazio, execute `python run_pipeline.py`.
- O formato exato de `config.toml` pode variar conforme a versao do Codex instalada.
- Esta versao nao implementa MCP Spark, PowerBI, DeltaLake ou Brain.
