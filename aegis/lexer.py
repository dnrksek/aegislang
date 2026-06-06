"""Lexical analysis for AegisLang."""

from aegis.errors import AegisSyntaxError
from aegis.token import Token, TokenKind, TokenLiteral


_KEYWORDS = {
    "let": TokenKind.LET,
    "mut": TokenKind.MUT,
    "if": TokenKind.IF,
    "else": TokenKind.ELSE,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
    "print": TokenKind.PRINT,
    "Int": TokenKind.INT,
    "String": TokenKind.STRING_TYPE,
    "Bool": TokenKind.BOOL,
}

_SINGLE_CHARACTER_TOKENS = {
    "+": TokenKind.PLUS,
    "-": TokenKind.MINUS,
    "*": TokenKind.STAR,
    "/": TokenKind.SLASH,
    "=": TokenKind.EQUAL,
    "<": TokenKind.LESS,
    ">": TokenKind.GREATER,
    "!": TokenKind.BANG,
    ":": TokenKind.COLON,
    "(": TokenKind.LEFT_PAREN,
    ")": TokenKind.RIGHT_PAREN,
    "{": TokenKind.LEFT_BRACE,
    "}": TokenKind.RIGHT_BRACE,
}

_DOUBLE_CHARACTER_TOKENS = {
    "==": TokenKind.EQUAL_EQUAL,
    "!=": TokenKind.BANG_EQUAL,
    "<=": TokenKind.LESS_EQUAL,
    ">=": TokenKind.GREATER_EQUAL,
}


class Lexer:
    """Convert AegisLang source text into tokens."""

    def __init__(self, source: str) -> None:
        self.source = source
        self._start = 0
        self._current = 0
        self._line = 1
        self._column = 1
        self._start_line = 1
        self._start_column = 1
        self._tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        """Scan the complete source and return its tokens, including EOF."""
        while not self._at_end():
            self._start = self._current
            self._start_line = self._line
            self._start_column = self._column
            self._scan_token()

        self._tokens.append(
            Token(TokenKind.EOF, "", None, self._line, self._column)
        )
        return self._tokens

    def _scan_token(self) -> None:
        character = self._advance()

        if character in " \t\r\n":
            return

        if character == "/" and self._peek() == "/":
            self._skip_comment()
            return

        if character == '"':
            self._scan_string()
            return

        if _is_ascii_digit(character):
            self._scan_integer()
            return

        if _is_identifier_start(character):
            self._scan_identifier()
            return

        pair = character + self._peek()
        if pair in _DOUBLE_CHARACTER_TOKENS:
            self._advance()
            self._add_token(_DOUBLE_CHARACTER_TOKENS[pair])
            return

        kind = _SINGLE_CHARACTER_TOKENS.get(character)
        if kind is not None:
            self._add_token(kind)
            return

        raise AegisSyntaxError(
            f"unexpected character {character!r}",
            self._start_line,
            self._start_column,
        )

    def _scan_string(self) -> None:
        while self._peek() != '"' and not self._at_end():
            self._advance()

        if self._at_end():
            raise AegisSyntaxError(
                "unterminated string",
                self._start_line,
                self._start_column,
            )

        self._advance()
        value = self.source[self._start + 1 : self._current - 1]
        self._add_token(TokenKind.STRING, value)

    def _scan_integer(self) -> None:
        while _is_ascii_digit(self._peek()):
            self._advance()

        lexeme = self.source[self._start : self._current]
        self._add_token(TokenKind.INTEGER, int(lexeme))

    def _scan_identifier(self) -> None:
        while _is_identifier_part(self._peek()):
            self._advance()

        lexeme = self.source[self._start : self._current]
        kind = _KEYWORDS.get(lexeme, TokenKind.IDENTIFIER)
        literal: TokenLiteral = None
        if kind is TokenKind.TRUE:
            literal = True
        elif kind is TokenKind.FALSE:
            literal = False
        self._add_token(kind, literal)

    def _skip_comment(self) -> None:
        while self._peek() != "\n" and not self._at_end():
            self._advance()

    def _add_token(self, kind: TokenKind, literal: TokenLiteral = None) -> None:
        lexeme = self.source[self._start : self._current]
        self._tokens.append(
            Token(kind, lexeme, literal, self._start_line, self._start_column)
        )

    def _advance(self) -> str:
        character = self.source[self._current]
        self._current += 1
        if character == "\n":
            self._line += 1
            self._column = 1
        else:
            self._column += 1
        return character

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        return self.source[self._current]

    def _at_end(self) -> bool:
        return self._current >= len(self.source)


def tokenize(source: str) -> list[Token]:
    """Tokenize AegisLang source text."""
    return Lexer(source).tokenize()


def _is_ascii_letter(character: str) -> bool:
    return "a" <= character <= "z" or "A" <= character <= "Z"


def _is_ascii_digit(character: str) -> bool:
    return "0" <= character <= "9"


def _is_identifier_start(character: str) -> bool:
    return _is_ascii_letter(character) or character == "_"


def _is_identifier_part(character: str) -> bool:
    return _is_identifier_start(character) or _is_ascii_digit(character)
