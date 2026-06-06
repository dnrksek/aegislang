# Task 001 — Bootstrap AegisLang v0.1 Project

Read AGENTS.md first and follow it strictly.

## Goal

Create the initial Python project structure for AegisLang v0.1.

This task is only for scaffolding. Do not implement the full language yet.

## Required Files

Create these files:

```text
README.md
pyproject.toml
aegis/__init__.py
aegis/__main__.py
aegis/cli.py
aegis/token.py
aegis/lexer.py
aegis/ast_nodes.py
aegis/parser.py
aegis/type_checker.py
aegis/interpreter.py
aegis/errors.py
examples/hello.aegis
tests/test_lexer.py
tests/test_parser.py
tests/test_type_checker.py
tests/test_interpreter.py
tests/test_cli.py
scripts/verify.sh
```

## pyproject.toml

Use pytest as the test dependency.

## CLI

Implement a placeholder CLI with these commands:

```bash
python -m aegis check examples/hello.aegis
python -m aegis run examples/hello.aegis
```

For this task only:

- `check` may print `OK`
- `run` may print placeholder output
- tests should verify the commands are wired correctly

## Example Program

Create `examples/hello.aegis`:

```aegis
let name: String = "Aegis"
let score: Int = 85

if score >= 80 {
    print("pass")
} else {
    print("fail")
}
```

## Verification Script

Create `scripts/verify.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

python -m pytest
python -m aegis check examples/hello.aegis
python -m aegis run examples/hello.aegis
```

## Constraints

- Do not implement the full lexer.
- Do not implement the full parser.
- Do not implement the full type checker.
- Do not implement the full interpreter.
- Keep the implementation minimal and clean.
- Add TODO comments for future implementation points.
