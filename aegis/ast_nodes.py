"""Abstract syntax tree nodes for AegisLang."""

from dataclasses import dataclass
from typing import TypeAlias


class Statement:
    """Base class for statement nodes."""


class Expression:
    """Base class for expression nodes."""


@dataclass(frozen=True, slots=True)
class Program:
    """A complete AegisLang source program."""

    statements: list[Statement]


@dataclass(frozen=True, slots=True)
class LetDecl(Statement):
    """An immutable variable declaration."""

    name: str
    type_name: str
    initializer: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class MutDecl(Statement):
    """A mutable variable declaration."""

    name: str
    type_name: str
    initializer: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class AssignStmt(Statement):
    """An assignment to an existing variable."""

    name: str
    value: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class PrintStmt(Statement):
    """A print statement."""

    expression: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class IfStmt(Statement):
    """A conditional statement with an optional else branch."""

    condition: Expression
    then_branch: "BlockStmt"
    else_branch: "BlockStmt | None"
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class BlockStmt(Statement):
    """A sequence of statements enclosed in braces."""

    statements: list[Statement]
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class IntLiteral(Expression):
    """An integer literal expression."""

    value: int
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class StringLiteral(Expression):
    """A string literal expression."""

    value: str
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class BoolLiteral(Expression):
    """A boolean literal expression."""

    value: bool
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class Identifier(Expression):
    """A variable reference expression."""

    name: str
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class BinaryExpr(Expression):
    """An infix binary expression."""

    left: Expression
    operator: str
    right: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class UnaryExpr(Expression):
    """A prefix unary expression."""

    operator: str
    operand: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class GroupingExpr(Expression):
    """A parenthesized expression."""

    expression: Expression
    line: int
    column: int


StatementNode: TypeAlias = (
    LetDecl | MutDecl | AssignStmt | PrintStmt | IfStmt | BlockStmt
)
ExpressionNode: TypeAlias = (
    IntLiteral
    | StringLiteral
    | BoolLiteral
    | Identifier
    | BinaryExpr
    | UnaryExpr
    | GroupingExpr
)
