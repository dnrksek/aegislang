"""Token definitions for AegisLang."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import TypeAlias


class TokenKind(Enum):
    """Kinds of tokens recognized by the AegisLang lexer."""

    # Keywords.
    LET = auto()
    MUT = auto()
    IF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    PRINT = auto()

    # Type names.
    INT = auto()
    STRING_TYPE = auto()
    BOOL = auto()

    # Identifiers and literals.
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()

    # Operators.
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    BANG = auto()

    # Punctuation.
    COLON = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    EOF = auto()


TokenLiteral: TypeAlias = int | str | bool | None


@dataclass(frozen=True, slots=True)
class Token:
    """A source token and its location."""

    kind: TokenKind
    lexeme: str
    literal: TokenLiteral
    line: int
    column: int
