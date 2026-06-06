# AegisLang

AegisLang is a small statically typed programming language designed for human-AI collaborative programming.

This repository currently contains the bootstrap scaffolding for the AegisLang v0.1 interpreter. The lexer, parser, type checker, and interpreter are placeholders for future tasks.

## Requirements

- Python 3.11 or newer
- pytest (for tests)

Install the test dependency with:

```bash
python -m pip install -e '.[test]'
```

## Placeholder CLI

Check the example program:

```bash
python -m aegis check examples/hello.aegis
```

Run the example program with the placeholder interpreter:

```bash
python -m aegis run examples/hello.aegis
```

## Verification

```bash
scripts/verify.sh
```
