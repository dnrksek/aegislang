"""Command-line interface for the AegisLang bootstrap."""

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build the placeholder AegisLang command-line parser."""
    parser = argparse.ArgumentParser(prog="aegis")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("check", "run"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("source")

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Run a placeholder AegisLang command."""
    args = build_parser().parse_args(argv)

    if args.command == "check":
        print("OK")
    else:
        # TODO: Execute the source program once the interpreter is implemented.
        print("AegisLang run placeholder")
