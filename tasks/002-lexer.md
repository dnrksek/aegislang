# Task 002 — Implement AegisLang Lexer

Read AGENTS.md first and follow it strictly.

## Goal

Implement the lexer for AegisLang v0.1.

The lexer converts AegisLang source code into a sequence of tokens with line and column information.

## Scope

This task implements only lexical analysis.

Do not implement the parser, type checker, or interpreter beyond what is necessary to keep existing tests passing.

## Token Requirements

Support the following token categories.

### Keywords

- let
- mut
- if
- else
- true
- false
- print

### Type Names

- Int
- String
- Bool

### Identifiers

Identifiers must start with an ASCII letter or underscore.

Identifiers may contain ASCII letters, digits, or underscores.

Examples:

```text
score
user_name
_private
x1
```

### Literals

Support:

- integer literals
- string literals
- boolean literals through `true` and `false`

Integer examples:

```text
0
1
85
12345
```

String examples:

```text
"hello"
"Aegis"
"pass"
```

For this task:

- Support simple double-quoted strings.
- Do not implement escape sequences yet.
- Unterminated strings must raise `AegisSyntaxError`.

### Operators

Support:

```text
+
-
*
/
=
==
!=
<
<=
>
>=
!
```

### Punctuation

Support:

```text
:
(
)
{
}
```

### Comments

Support `//` line comments.

Example:

```aegis
let x: Int = 1 // this is a comment
```

The comment should be ignored by the lexer.

### Whitespace

Ignore:

- spaces
- tabs
- carriage returns
- newlines

But line and column tracking must remain correct.

## EOF

The lexer must always append an EOF token at the end.

## Error Handling

Raise `AegisSyntaxError` for:

- invalid characters
- unterminated strings

Errors must include line and column information.

Example error message style:

```text
SyntaxError at line 1, column 5: unexpected character '@'
```

The exact wording may differ, but it must be clear and tested.

## Implementation Requirements

- Keep token definitions simple and explicit.
- Track token kind, lexeme, literal value if applicable, line, and column.
- Existing placeholder CLI tests must continue to pass.
- Add lexer unit tests.

## Required Tests

Add or update tests in `tests/test_lexer.py`.

Test at least:

1. Lexes `let score: Int = 85`
2. Lexes string literals
3. Lexes boolean literals
4. Lexes if/else block tokens
5. Lexes comparison operators
6. Ignores whitespace
7. Ignores `//` comments
8. Raises `AegisSyntaxError` for invalid characters
9. Raises `AegisSyntaxError` for unterminated strings
10. Appends EOF token

## Example Input

```aegis
let score: Int = 85

if score >= 80 {
    print("pass")
} else {
    print("fail")
}
```

The lexer should produce a token sequence representing all keywords, identifiers, literals, operators, punctuation, and EOF.

## Verification

After implementation, this must pass:

```bash
./scripts/verify.sh
```

Also run:

```bash
python -m pytest tests/test_lexer.py
```

## Constraints

- Do not implement full parsing in this task.
- Do not implement type checking in this task.
- Do not implement runtime execution in this task.
- Do not add functions, structs, enums, loops, arrays, Result, Option, contracts, or effects.
- Do not change the AegisLang syntax without updating this task and AGENTS.md.
