"""Valida a estrutura, a seguranca e os modos CLI/stdio do MCP CSV."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
MCP_DIR = PROJECT_DIR / "mcp"
REQUIRED_FILES = [
    "mcp/README.md",
    "mcp/CODEX_MCP_SETUP.md",
    "mcp/csv_mcp_server.py",
    "mcp/mcp_config.example.json",
    "mcp/tools/__init__.py",
    "mcp/tools/csv_tools.py",
]
EXPECTED_TOOLS = [
    "csv_compare_metrics_files",
    "csv_describe_file",
    "csv_get_metrics_summary",
    "csv_list_reports",
    "csv_preview_file",
    "csv_search_value",
    "csv_validate_columns",
]
EMOJI_RE = re.compile("[" "\\U0001F300-\\U0001FAFF" "\\U00002700-\\U000027BF" "\\U00002600-\\U000026FF" "]")
LOCAL_PATH_RE = re.compile(r"/home/|/mnt/" + "c/Users/" + r"|[A-Za-z]:\\", re.IGNORECASE)


def run_command(args: list[str], input_text: str | None = None, timeout: int = 30) -> tuple[int, str, str]:
    result = subprocess.run(
        args,
        cwd=PROJECT_DIR,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def fail(errors: list[str], message: str) -> None:
    errors.append(message)
    print(f"FALHA: {message}")


def ok(message: str) -> None:
    print(f"OK: {message}")


def validate_structure(errors: list[str]) -> None:
    for item in REQUIRED_FILES:
        path = PROJECT_DIR / item
        ok(f"arquivo encontrado: {item}") if path.exists() else fail(errors, f"arquivo ausente: {item}")
    forbidden = ["spark", "powerbi", "delta", "brain"]
    if MCP_DIR.exists():
        for path in MCP_DIR.rglob("*"):
            if "__pycache__" in path.parts:
                continue
            if path.is_file() and path.name != "README.md" and any(term in str(path).lower() for term in forbidden):
                fail(errors, f"MCP proibido encontrado: {path.relative_to(PROJECT_DIR)}")


def validate_text(errors: list[str]) -> None:
    if not MCP_DIR.exists():
        return
    for path in MCP_DIR.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(PROJECT_DIR)
        if EMOJI_RE.search(text):
            fail(errors, f"emoji encontrado em {relative}")
        if LOCAL_PATH_RE.search(text):
            fail(errors, f"caminho local encontrado em {relative}")


def validate_cli(errors: list[str]) -> None:
    commands = [
        [sys.executable, "mcp/csv_mcp_server.py", "--list-tools"],
        [sys.executable, "mcp/csv_mcp_server.py", "--tool", "csv_list_reports"],
        [sys.executable, "mcp/csv_mcp_server.py", "--tool", "csv_get_metrics_summary"],
    ]
    for command in commands:
        code, stdout, stderr = run_command(command)
        if code != 0:
            fail(errors, f"comando falhou: {' '.join(command)} | {stderr.strip()}")
            continue
        try:
            payload = json.loads(stdout)
            ok(f"CLI valida: {' '.join(command[1:])}")
        except json.JSONDecodeError as exc:
            fail(errors, f"saida JSON invalida em {' '.join(command)}: {exc}")
            continue
        if "--list-tools" in command:
            tools = payload.get("tools", [])
            missing = sorted(set(EXPECTED_TOOLS) - set(tools))
            if missing:
                fail(errors, f"ferramentas ausentes no CLI: {missing}")
            else:
                ok("todas as ferramentas esperadas aparecem no CLI")

    reports = PROJECT_DIR / "reports"
    csv_files = sorted(reports.glob("*.csv")) if reports.exists() else []
    if csv_files:
        target = f"reports/{csv_files[0].name}"
        code, _stdout, stderr = run_command([sys.executable, "mcp/csv_mcp_server.py", "--tool", "csv_preview_file", "--file", target])
        ok(f"preview valido: {target}") if code == 0 else fail(errors, f"preview falhou: {stderr.strip()}")


def validate_native_mcp_stdio(errors: list[str]) -> None:
    messages = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "validator", "version": "1.0"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "csv_list_reports", "arguments": {}}},
    ]
    payload = "\n".join(json.dumps(message) for message in messages) + "\n"
    code, stdout, stderr = run_command([sys.executable, "mcp/csv_mcp_server.py", "--mcp-stdio"], input_text=payload, timeout=20)
    if code != 0:
        fail(errors, f"MCP stdio falhou: {stderr.strip()}")
        return
    try:
        responses = [json.loads(line) for line in stdout.splitlines() if line.strip()]
    except json.JSONDecodeError as exc:
        fail(errors, f"saida MCP stdio invalida: {exc}")
        return
    by_id = {response.get("id"): response for response in responses}
    for expected_id in [1, 2, 3]:
        if expected_id not in by_id:
            fail(errors, f"resposta MCP stdio ausente para id {expected_id}")
    if 2 in by_id:
        tools = [tool.get("name") for tool in by_id[2].get("result", {}).get("tools", [])]
        missing = sorted(set(EXPECTED_TOOLS) - set(tools))
        if missing:
            fail(errors, f"ferramentas ausentes no MCP stdio: {missing}")
        else:
            ok("todas as ferramentas esperadas aparecem no MCP stdio")
    if 3 in by_id and "content" in by_id[3].get("result", {}):
        ok("tools/call valido no MCP stdio")
    else:
        fail(errors, "tools/call do MCP stdio nao retornou content")


def validate_import(errors: list[str]) -> None:
    code, stdout, stderr = run_command([sys.executable, "-c", "from mcp.csv_mcp_server import handle_mcp_message, tool_list_payload; print(len(tool_list_payload()))"])
    if code != 0:
        fail(errors, f"import do servidor MCP falhou: {stderr.strip()}")
        return
    try:
        count = int(stdout.strip())
    except ValueError:
        fail(errors, f"import retornou saida inesperada: {stdout.strip()}")
        return
    ok("import do servidor MCP valido") if count == len(EXPECTED_TOOLS) else fail(errors, "quantidade inesperada de ferramentas no import")


def validate_security(errors: list[str]) -> None:
    unsafe_commands = [
        [sys.executable, "mcp/csv_mcp_server.py", "--tool", "csv_preview_file", "--file", "../README.md"],
        [sys.executable, "mcp/csv_mcp_server.py", "--tool", "csv_preview_file", "--file", "README.md"],
    ]
    for command in unsafe_commands:
        code, _stdout, _stderr = run_command(command)
        ok(f"bloqueio de caminho inseguro validado: {command[-1]}") if code != 0 else fail(errors, f"caminho inseguro aceito: {command[-1]}")


def main() -> int:
    errors: list[str] = []
    validate_structure(errors)
    validate_text(errors)
    validate_import(errors)
    validate_cli(errors)
    validate_native_mcp_stdio(errors)
    validate_security(errors)
    if errors:
        print("Validacao do MCP CSV concluida com falhas.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validacao do MCP CSV concluida com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
