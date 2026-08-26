"""Servidor MCP CSV do projeto Pix com modo nativo stdio e modo CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from h_mcp.tools.csv_tools import TOOLS

PROTOCOL_VERSION = "2024-11-05"

TOOL_DEFINITIONS: dict[str, dict[str, Any]] = {
    "csv_list_reports": {
        "description": "Lista arquivos CSV disponiveis em reports/.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    "csv_preview_file": {
        "description": "Retorna as primeiras linhas de um CSV seguro em reports/.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "Arquivo CSV relativo em reports/.",
                },
                "rows": {
                    "type": "integer",
                    "description": "Quantidade de linhas, limitada pelo servidor.",
                    "default": 5,
                },
            },
            "required": ["file"],
            "additionalProperties": False,
        },
    },
    "csv_describe_file": {
        "description": "Descreve colunas, tipos e estatisticas basicas de um CSV.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "Arquivo CSV relativo em reports/.",
                }
            },
            "required": ["file"],
            "additionalProperties": False,
        },
    },
    "csv_validate_columns": {
        "description": "Valida se um CSV possui colunas esperadas.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "Arquivo CSV relativo em reports/.",
                },
                "columns": {
                    "description": "Colunas esperadas como lista ou texto separado por virgula.",
                    "oneOf": [
                        {"type": "array", "items": {"type": "string"}},
                        {"type": "string"},
                    ],
                },
            },
            "required": ["file", "columns"],
            "additionalProperties": False,
        },
    },
    "csv_get_metrics_summary": {
        "description": "Resume os principais CSVs de metricas em reports/.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    "csv_search_value": {
        "description": "Busca termo textual simples nos CSVs de reports/.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Termo de busca."},
                "max_results": {
                    "type": "integer",
                    "description": "Limite de resultados.",
                    "default": 20,
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    "csv_compare_metrics_files": {
        "description": "Compara arquivos de metricas e consolida dimensoes basicas.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MCP CSV read-only para arquivos analiticos em reports."
    )
    parser.add_argument(
        "--mcp-stdio",
        action="store_true",
        help="Inicia explicitamente o servidor MCP stdio.",
    )
    parser.add_argument(
        "--list-tools", action="store_true", help="Lista ferramentas disponiveis."
    )
    parser.add_argument("--tool", choices=sorted(TOOLS), help="Ferramenta a executar.")
    parser.add_argument("--file", help="Arquivo CSV relativo em reports.")
    parser.add_argument("--columns", help="Colunas esperadas separadas por virgula.")
    parser.add_argument("--query", help="Termo para busca textual.")
    parser.add_argument(
        "--rows", type=int, default=5, help="Quantidade de linhas para preview."
    )
    return parser


def _tool_arguments(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if tool_name in {
        "csv_list_reports",
        "csv_get_metrics_summary",
        "csv_compare_metrics_files",
    }:
        return {}
    if tool_name == "csv_preview_file":
        return {"file_name": arguments["file"], "rows": arguments.get("rows", 5)}
    if tool_name == "csv_describe_file":
        return {"file_name": arguments["file"]}
    if tool_name == "csv_validate_columns":
        return {"file_name": arguments["file"], "columns": arguments["columns"]}
    if tool_name == "csv_search_value":
        return {
            "query": arguments["query"],
            "max_results": arguments.get("max_results", 20),
        }
    raise ValueError(f"Ferramenta desconhecida: {tool_name}")


def call_tool(
    tool_name: str, arguments: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Executa uma ferramenta do MCP CSV de forma reutilizavel por CLI e stdio."""
    if tool_name not in TOOLS:
        raise ValueError(f"Ferramenta desconhecida: {tool_name}")
    kwargs = _tool_arguments(tool_name, arguments or {})
    return TOOLS[tool_name](**kwargs)


def run_tool(args: argparse.Namespace) -> dict:
    if args.tool == "csv_list_reports":
        return call_tool(args.tool)
    if args.tool == "csv_get_metrics_summary":
        return call_tool(args.tool)
    if args.tool == "csv_compare_metrics_files":
        return call_tool(args.tool)
    if args.tool == "csv_preview_file":
        if not args.file:
            raise ValueError("--file e obrigatorio para csv_preview_file.")
        return call_tool(args.tool, {"file": args.file, "rows": args.rows})
    if args.tool == "csv_describe_file":
        if not args.file:
            raise ValueError("--file e obrigatorio para csv_describe_file.")
        return call_tool(args.tool, {"file": args.file})
    if args.tool == "csv_validate_columns":
        if not args.file or not args.columns:
            raise ValueError(
                "--file e --columns sao obrigatorios para csv_validate_columns."
            )
        return call_tool(args.tool, {"file": args.file, "columns": args.columns})
    if args.tool == "csv_search_value":
        if not args.query:
            raise ValueError("--query e obrigatorio para csv_search_value.")
        return call_tool(args.tool, {"query": args.query})
    raise ValueError("Ferramenta invalida.")


def tool_list_payload() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "description": TOOL_DEFINITIONS[name]["description"],
            "inputSchema": TOOL_DEFINITIONS[name]["inputSchema"],
        }
        for name in sorted(TOOLS)
    ]


def _jsonrpc_result(message_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def _jsonrpc_error(message_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": message_id,
        "error": {"code": code, "message": message},
    }


def handle_mcp_message(message: dict[str, Any]) -> dict[str, Any] | None:
    """Processa uma mensagem JSON-RPC MCP no transporte stdio."""
    method = message.get("method")
    message_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        return _jsonrpc_result(
            message_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "pix-csv-mcp", "version": "1.0.0"},
            },
        )
    if method == "tools/list":
        return _jsonrpc_result(message_id, {"tools": tool_list_payload()})
    if method == "tools/call":
        try:
            tool_name = params.get("name")
            arguments = params.get("arguments") or {}
            payload = call_tool(tool_name, arguments)
            return _jsonrpc_result(
                message_id,
                {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                payload, ensure_ascii=False, indent=2, default=str
                            ),
                        }
                    ],
                    "isError": False,
                },
            )
        except Exception as exc:
            return _jsonrpc_result(
                message_id,
                {"content": [{"type": "text", "text": str(exc)}], "isError": True},
            )
    if method == "ping":
        return _jsonrpc_result(message_id, {})
    if method and method.startswith("notifications/"):
        return None
    return _jsonrpc_error(message_id, -32601, f"Metodo nao suportado: {method}")


def run_mcp_stdio() -> int:
    """Inicia servidor MCP nativo via stdio com mensagens JSON-RPC por linha."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = handle_mcp_message(message)
        except Exception as exc:
            response = _jsonrpc_error(None, -32700, f"Mensagem invalida: {exc}")
        if response is not None:
            print(json.dumps(response, ensure_ascii=False, default=str), flush=True)
    return 0


def run_cli(args: argparse.Namespace) -> int:
    try:
        if args.list_tools:
            payload = {"tools": sorted(TOOLS)}
        elif args.tool:
            payload = run_tool(args)
        else:
            parser.print_help()
            return 0
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return 0
    except Exception as exc:
        print(
            json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2),
            file=sys.stderr,
        )
        return 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.mcp_stdio or not any([args.list_tools, args.tool]):
        return run_mcp_stdio()
    return run_cli(args)


if __name__ == "__main__":
    raise SystemExit(main())
