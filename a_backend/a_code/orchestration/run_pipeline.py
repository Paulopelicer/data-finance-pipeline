"""CLI unica para executar os pipelines B3 e Pix."""

from __future__ import annotations

import argparse

from a_backend.a_code.common.paths import create_project_directories
from a_backend.a_code.pipelines.b3 import runner as b3_runner
from a_backend.a_code.pipelines.pix import runner as pix_runner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Executa pipelines financeiros B3 e Pix.")
    parser.add_argument("--pipeline", choices=["all", "b3", "pix"], default="all")
    parser.add_argument("--pix-mode", choices=["all", "few"], default="all")
    parser.add_argument("--pix-rows", type=int, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    create_project_directories()

    results: list[tuple[str, int]] = []
    if args.pipeline in {"all", "b3"}:
        results.append(("b3", b3_runner.run()))
    if args.pipeline in {"all", "pix"}:
        results.append(("pix", pix_runner.run(mode=args.pix_mode, rows=args.pix_rows)))

    failed = [(name, code) for name, code in results if code != 0]
    if failed:
        for name, code in failed:
            print(f"Pipeline {name} falhou com codigo {code}.")
        return 1

    for name, _code in results:
        print(f"Pipeline {name} executado com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
