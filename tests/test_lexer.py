"""Tests for the AegisLang lexer."""

import pytest

from aegis.errors import AegisSyntaxError
from aegis.lexer import Lexer, tokenize
from aegis.token import TokenKind


def kinds(source: str) -> list[TokenKind]:
    return [token.kind for token in tokenize(source)]


def test_lexes_immutable_integer_declaration() -> None:
    tokens = tokenize("let score: Int = 85")

    assert [token.kind for token in tokens] == [
        TokenKind.LET,
        TokenKind.IDENTIFIER,
        TokenKind.COLON,
        TokenKind.INT,
        TokenKind.EQUAL,
        TokenKind.INTEGER,
        TokenKind.EOF,
    ]
    assert tokens[1].lexeme == "score"
    assert tokens[5].literal == 85
    assert (tokens[0].line, tokens[0].column) == (1, 1)
    assert (tokens[5].line, tokens[5].column) == (1, 18)


def test_lexes_string_literal() -> None:
    tokens = Lexer('let message: String = "hello"').tokenize()

    string = tokens[-2]
    assert string.kind is TokenKind.STRING
    assert string.lexeme == '"hello"'
    assert string.literal == "hello"


def test_lexes_boolean_literals() -> None:
    tokens = tokenize("true false")

    assert [token.kind for token in tokens] == [
        TokenKind.TRUE,
        TokenKind.FALSE,
        TokenKind.EOF,
    ]
    assert [token.literal for token in tokens[:-1]] == [True, False]


def test_lexes_if_else_block_tokens() -> None:
    assert kinds('if true { print("pass") } else { print("fail") }') == [
        TokenKind.IF,
        TokenKind.TRUE,
        TokenKind.LEFT_BRACE,
        TokenKind.PRINT,
        TokenKind.LEFT_PAREN,
        TokenKind.STRING,
        TokenKind.RIGHT_PAREN,
        TokenKind.RIGHT_BRACE,
        TokenKind.ELSE,
        TokenKind.LEFT_BRACE,
        TokenKind.PRINT,
        TokenKind.LEFT_PAREN,
        TokenKind.STRING,
        TokenKind.RIGHT_PAREN,
        TokenKind.RIGHT_BRACE,
        TokenKind.EOF,
    ]


def test_lexes_all_operators() -> None:
    assert kinds("+ - * / = == != < <= > >= !") == [
        TokenKind.PLUS,
        TokenKind.MINUS,
        TokenKind.STAR,
        TokenKind.SLASH,
        TokenKind.EQUAL,
        TokenKind.EQUAL_EQUAL,
        TokenKind.BANG_EQUAL,
        TokenKind.LESS,
        TokenKind.LESS_EQUAL,
        TokenKind.GREATER,
        TokenKind.GREATER_EQUAL,
        TokenKind.BANG,
        TokenKind.EOF,
    ]


def test_ignores_whitespace_and_tracks_locations() -> None:
    tokens = tokenize(" \t\r\n  mut\t_private: Bool")

    assert [token.kind for token in tokens] == [
        TokenKind.MUT,
        TokenKind.IDENTIFIER,
        TokenKind.COLON,
        TokenKind.BOOL,
        TokenKind.EOF,
    ]
    assert (tokens[0].line, tokens[0].column) == (2, 3)
    assert (tokens[1].line, tokens[1].column) == (2, 7)


def test_ignores_line_comments() -> None:
    tokens = tokenize("let x: Int = 1 // ignored\nprint(x)")

    assert [token.lexeme for token in tokens] == [
        "let",
        "x",
        ":",
        "Int",
        "=",
        "1",
        "print",
        "(",
        "x",
        ")",
        "",
    ]
    assert (tokens[6].line, tokens[6].column) == (2, 1)


def test_rejects_invalid_character_with_location() -> None:
    with pytest.raises(AegisSyntaxError) as error:
        tokenize("let @")

    assert error.value.line == 1
    assert error.value.column == 5
    assert "unexpected character '@'" in str(error.value)


def test_rejects_unterminated_string_with_location() -> None:
    with pytest.raises(AegisSyntaxError) as error:
        tokenize('\n  "never closed')

    assert error.value.line == 2
    assert error.value.column == 3
    assert "unterminated string" in str(error.value)


def test_appends_eof_to_empty_source() -> None:
    tokens = tokenize("")

    assert len(tokens) == 1
    assert tokens[0].kind is TokenKind.EOF
    assert tokens[0].lexeme == ""
    assert tokens[0].literal is None
    assert (tokens[0].line, tokens[0].column) == (1, 1)


def test_identifiers_are_ascii_only() -> None:
    assert kinds("user_name _private x1") == [
        TokenKind.IDENTIFIER,
        TokenKind.IDENTIFIER,
        TokenKind.IDENTIFIER,
        TokenKind.EOF,
    ]

    with pytest.raises(AegisSyntaxError):
        tokenize("café")
