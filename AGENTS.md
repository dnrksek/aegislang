# AegisLang Agent Instructions

## Project Goal

AegisLang is a small statically typed programming language designed for human-AI collaborative programming.

The language should prioritize:

- explicit syntax
- static type checking
- no implicit type conversion
- immutable variables by default
- clear diagnostics with line and column
- simple architecture
- testability
- future support for intent, contracts, effects, and security automation

## Implementation Language

Use Python.

## Current Target

Build AegisLang v0.1 as an interpreter.

v0.1 includes:

- let immutable variable declarations
- mut mutable variable declarations
- Int, String, Bool types
- arithmetic expressions
- comparison expressions
- equality expressions
- if / else
- print()
- assignment only to mut variables
- static type checking before execution
- CLI commands:
  - python -m aegis check examples/hello.aegis
  - python -m aegis run examples/hello.aegis

v0.1 does not include:

- functions
- structs
- enums
- arrays
- loops
- Result / Option
- contracts
- effects
- modules
- package manager
- compiler backend

## Coding Rules

- Use Python standard library only unless explicitly requested.
- Use dataclasses for AST nodes.
- Use a recursive descent parser.
- Keep modules small and readable.
- Do not add advanced features early.
- Add tests for every implemented feature.
- Prefer clear errors over clever code.
- Do not silently change the language syntax without updating docs.

## Required Project Structure

```text
aegis/
  __init__.py
  __main__.py
  cli.py
  token.py
  lexer.py
  ast_nodes.py
  parser.py
  type_checker.py
  interpreter.py
  errors.py

examples/
  hello.aegis

tests/
  test_lexer.py
  test_parser.py
  test_type_checker.py
  test_interpreter.py
  test_cli.py

scripts/
  verify.sh
