"""Tests for the AegisLang recursive descent parser."""

import pytest

from aegis.ast_nodes import (
    AssignStmt,
    BinaryExpr,
    BlockStmt,
    BoolLiteral,
    GroupingExpr,
    Identifier,
    IfStmt,
    IntLiteral,
    LetDecl,
    MutDecl,
    PrintStmt,
    StringLiteral,
    UnaryExpr,
)
from aegis.errors import AegisSyntaxError
from aegis.lexer import tokenize
from aegis.parser import Parser, parse


def first_statement(source: str):
    return parse(source).statements[0]


def test_parses_let_declaration() -> None:
    statement = first_statement("let score: Int = 85")

    assert isinstance(statement, LetDecl)
    assert statement.name == "score"
    assert statement.type_name == "Int"
    assert statement.initializer == IntLiteral(85, 1, 18)
    assert (statement.line, statement.column) == (1, 1)


def test_parses_mut_declaration() -> None:
    statement = first_statement("mut enabled: Bool = true")

    assert isinstance(statement, MutDecl)
    assert statement.name == "enabled"
    assert statement.type_name == "Bool"
    assert isinstance(statement.initializer, BoolLiteral)


def test_parses_assignment() -> None:
    statement = first_statement("count = count + 1")

    assert isinstance(statement, AssignStmt)
    assert statement.name == "count"
    assert isinstance(statement.value, BinaryExpr)


def test_parses_print_statement() -> None:
    statement = first_statement('print("hello")')

    assert isinstance(statement, PrintStmt)
    assert statement.expression == StringLiteral("hello", 1, 7)


def test_parses_if_without_else() -> None:
    statement = first_statement('if true { print("yes") }')

    assert isinstance(statement, IfStmt)
    assert statement.condition == BoolLiteral(True, 1, 4)
    assert len(statement.then_branch.statements) == 1
    assert statement.else_branch is None


def test_parses_if_with_else() -> None:
    statement = first_statement(
        'if false { print("yes") } else { print("no") }'
    )

    assert isinstance(statement, IfStmt)
    assert isinstance(statement.else_branch, BlockStmt)
    assert len(statement.else_branch.statements) == 1


def test_parses_nested_block() -> None:
    statement = first_statement("{ { let x: Int = 1 } print(x) }")

    assert isinstance(statement, BlockStmt)
    assert isinstance(statement.statements[0], BlockStmt)
    assert isinstance(statement.statements[0].statements[0], LetDecl)
    assert isinstance(statement.statements[1], PrintStmt)


def test_parses_integer_string_and_boolean_literals() -> None:
    program = parse(
        'let number: Int = 1 let text: String = "a" let flag: Bool = false'
    )

    assert isinstance(program.statements[0].initializer, IntLiteral)
    assert isinstance(program.statements[1].initializer, StringLiteral)
    assert isinstance(program.statements[2].initializer, BoolLiteral)


def test_parses_identifier() -> None:
    statement = first_statement("print(value)")

    assert statement.expression == Identifier("value", 1, 7)


def test_parses_binary_expression_left_associatively() -> None:
    expression = first_statement("print(10 - 3 - 2)").expression

    assert isinstance(expression, BinaryExpr)
    assert expression.operator == "-"
    assert isinstance(expression.left, BinaryExpr)
    assert expression.left.operator == "-"
    assert expression.right == IntLiteral(2, 1, 16)


def test_respects_arithmetic_precedence() -> None:
    expression = first_statement("print(1 + 2 * 3)").expression

    assert isinstance(expression, BinaryExpr)
    assert expression.operator == "+"
    assert isinstance(expression.right, BinaryExpr)
    assert expression.right.operator == "*"


def test_respects_comparison_and_equality_precedence() -> None:
    expression = first_statement("print(1 + 2 >= 3 == false)").expression

    assert isinstance(expression, BinaryExpr)
    assert expression.operator == "=="
    assert isinstance(expression.left, BinaryExpr)
    assert expression.left.operator == ">="
    assert isinstance(expression.left.left, BinaryExpr)
    assert expression.left.left.operator == "+"


def test_parses_unary_expressions() -> None:
    expression = first_statement("print(!true == -1)").expression

    assert isinstance(expression, BinaryExpr)
    assert isinstance(expression.left, UnaryExpr)
    assert expression.left.operator == "!"
    assert isinstance(expression.right, UnaryExpr)
    assert expression.right.operator == "-"


def test_parses_grouped_expression() -> None:
    expression = first_statement("print((1 + 2) * 3)").expression

    assert isinstance(expression, BinaryExpr)
    assert expression.operator == "*"
    assert isinstance(expression.left, GroupingExpr)
    assert isinstance(expression.left.expression, BinaryExpr)


def test_parser_class_accepts_lexer_tokens() -> None:
    program = Parser(tokenize("print(1)")).parse_program()

    assert len(program.statements) == 1
    assert isinstance(program.statements[0], PrintStmt)


def test_parses_example_program() -> None:
    program = parse(
        '''let name: String = "Aegis"
let score: Int = 85

if score >= 80 {
    print("pass")
} else {
    print("fail")
}
'''
    )

    assert [type(statement) for statement in program.statements] == [
        LetDecl,
        LetDecl,
        IfStmt,
    ]


def test_raises_for_missing_expression() -> None:
    with pytest.raises(AegisSyntaxError) as error:
        parse("let score: Int =")

    assert "expected expression" in str(error.value)
    assert (error.value.line, error.value.column) == (1, 17)


def test_raises_for_missing_closing_brace() -> None:
    with pytest.raises(AegisSyntaxError) as error:
        parse("if true { print(1)")

    assert "expected '}' after block" in str(error.value)
    assert (error.value.line, error.value.column) == (1, 19)


def test_raises_for_invalid_statement_start() -> None:
    with pytest.raises(AegisSyntaxError) as error:
        parse("else { print(1) }")

    assert "unexpected token 'else' at start of statement" in str(error.value)
    assert (error.value.line, error.value.column) == (1, 1)


def test_raises_for_missing_print_parenthesis() -> None:
    with pytest.raises(AegisSyntaxError) as error:
        parse("print(1")

    assert "expected ')' after print expression" in str(error.value)
