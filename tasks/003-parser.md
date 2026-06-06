# Task 003 — Implement AegisLang Parser and AST

Read AGENTS.md first and follow it strictly.

## Goal

Implement the AegisLang v0.1 parser and AST.

The parser converts tokens from the lexer into an abstract syntax tree.

This task implements parsing only. Do not implement static type checking or real interpretation yet.

## Scope

Implement:

- AST node definitions
- recursive descent parser
- syntax error reporting
- parser unit tests

Do not implement:

- functions
- structs
- enums
- arrays
- loops
- Result / Option
- contracts
- effects
- runtime execution
- static type checking rules

## Grammar

Implement this grammar:

```text
program     -> statement* EOF

statement   -> letDecl
             | mutDecl
             | assignStmt
             | printStmt
             | ifStmt
             | block

letDecl     -> "let" IDENT ":" type "=" expression
mutDecl     -> "mut" IDENT ":" type "=" expression
assignStmt  -> IDENT "=" expression

printStmt   -> "print" "(" expression ")"

ifStmt      -> "if" expression block ("else" block)?
block       -> "{" statement* "}"

expression  -> equality
equality    -> comparison (("==" | "!=") comparison)*
comparison  -> term ((">" | ">=" | "<" | "<=") term)*
term        -> factor (("+" | "-") factor)*
factor      -> unary (("*" | "/") unary)*
unary       -> ("!" | "-") unary | primary
primary     -> INT | STRING | BOOL | IDENT | "(" expression ")"

type        -> "Int" | "String" | "Bool"
```

## AST Requirements

Use dataclasses for AST nodes.

Create clear node types for at least:

### Program

- Program

### Statements

- LetDecl
- MutDecl
- AssignStmt
- PrintStmt
- IfStmt
- BlockStmt

### Expressions

- IntLiteral
- StringLiteral
- BoolLiteral
- Identifier
- BinaryExpr
- UnaryExpr
- GroupingExpr

## Parser Requirements

- Use recursive descent parsing.
- Respect operator precedence.
- Preserve source line and column information where useful for diagnostics.
- Raise `AegisSyntaxError` for invalid syntax.
- Error messages must be clear enough to identify the unexpected token or missing syntax.
- Existing lexer and CLI tests must continue to pass.

## Statement Rules

### let declaration

```aegis
let score: Int = 85
```

### mut declaration

```aegis
mut count: Int = 0
```

### assignment

```aegis
count = count + 1
```

### print statement

```aegis
print("hello")
```

### if / else

```aegis
if score >= 80 {
    print("pass")
} else {
    print("fail")
}
```

### block

```aegis
{
    let x: Int = 1
    print(x)
}
```

## Expression Rules

The parser must respect precedence.

Example:

```aegis
1 + 2 * 3
```

Must parse as:

```text
1 + (2 * 3)
```

Example:

```aegis
(1 + 2) * 3
```

Must parse as:

```text
(1 + 2) * 3
```

Example:

```aegis
!true == false
```

Must parse as:

```text
(!true) == false
```

## Required Tests

Add or update tests in `tests/test_parser.py`.

Test at least:

1. Parses let declaration
2. Parses mut declaration
3. Parses assignment
4. Parses print statement
5. Parses if without else
6. Parses if with else
7. Parses nested block
8. Parses integer, string, and boolean literals
9. Parses identifiers
10. Parses binary expressions
11. Respects arithmetic precedence
12. Respects comparison and equality precedence
13. Parses unary expressions
14. Parses grouped expressions
15. Raises `AegisSyntaxError` for missing expression
16. Raises `AegisSyntaxError` for missing closing brace
17. Raises `AegisSyntaxError` for invalid statement start

## Example Program

This should parse successfully:

```aegis
let name: String = "Aegis"
let score: Int = 85

if score >= 80 {
    print("pass")
} else {
    print("fail")
}
```

## Verification

After implementation, this must pass:

```bash
./scripts/verify.sh
```

Also run:

```bash
python -m pytest tests/test_parser.py
```

## Constraints

- Do not implement type checking in this task.
- Do not implement runtime execution in this task.
- Do not change lexer behavior unless required to support parser correctness.
- Do not add semicolons.
- Do not add functions.
- Do not add loops.
- Do not add arrays.
- Do not add structs, enums, Result, Option, contracts, or effects.
- Do not change the AegisLang syntax without updating this task and AGENTS.md.
