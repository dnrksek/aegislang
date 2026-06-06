import argparse
from pathlib import Path


def cmd_check(args: argparse.Namespace) -> int:
    path = Path(args.file)

    if not path.exists():
        print(f"error: file not found: {path}")
        return 1

    source = path.read_text(encoding="utf-8")

    print(f"Checking {path}")
    print(source)
    print("OK")

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="aegis")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("file")
    check_parser.set_defaults(func=cmd_check)

    args = parser.parse_args()
    raise SystemExit(args.func(args))
