"""Recursive descent parser for AegisLang."""

from collections.abc import Sequence

from aegis.ast_nodes import (
    AssignStmt,
    BinaryExpr,
    BlockStmt,
    BoolLiteral,
    Expression,
    GroupingExpr,
    Identifier,
    IfStmt,
    IntLiteral,
    LetDecl,
    MutDecl,
    PrintStmt,
    Program,
    Statement,
    StringLiteral,
    UnaryExpr,
)
from aegis.errors import AegisSyntaxError
from aegis.lexer import tokenize
from aegis.token import Token, TokenKind


_TYPE_NAMES = {
    TokenKind.INT: "Int",
    TokenKind.STRING_TYPE: "String",
    TokenKind.BOOL: "Bool",
}


class Parser:
    """Convert a token sequence into an AegisLang abstract syntax tree."""

    def __init__(self, tokens: Sequence[Token]) -> None:
        if not tokens:
            raise ValueError("parser requires a token sequence ending in EOF")
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Program:
        """Parse and return a complete program."""
        statements: list[Statement] = []
        while not self._at_end():
            statements.append(self._statement())
        return Program(statements)

    def parse_program(self) -> Program:
        """Parse a complete program (explicitly named alias for ``parse``)."""
        return self.parse()

    def _statement(self) -> Statement:
        if self._match(TokenKind.LET):
            return self._variable_declaration(mutable=False)
        if self._match(TokenKind.MUT):
            return self._variable_declaration(mutable=True)
        if self._match(TokenKind.PRINT):
            return self._print_statement()
        if self._match(TokenKind.IF):
            return self._if_statement()
        if self._match(TokenKind.LEFT_BRACE):
            return self._block_statement(self._previous())
        if self._match(TokenKind.IDENTIFIER):
            return self._assignment_statement(self._previous())

        token = self._peek()
        self._raise_at(
            token,
            f"unexpected token {self._describe(token)} at start of statement",
        )

    def _variable_declaration(self, *, mutable: bool) -> LetDecl | MutDecl:
        keyword = self._previous()
        name = self._consume(TokenKind.IDENTIFIER, "expected variable name")
        self._consume(TokenKind.COLON, "expected ':' after variable name")
        type_token = self._peek()
        if type_token.kind not in _TYPE_NAMES:
            self._raise_at(type_token, "expected type 'Int', 'String', or 'Bool'")
        self._advance()
        self._consume(TokenKind.EQUAL, "expected '=' after declared type")
        initializer = self._expression()
        node_type = MutDecl if mutable else LetDecl
        return node_type(
            name.lexeme,
            _TYPE_NAMES[type_token.kind],
            initializer,
            keyword.line,
            keyword.column,
        )

    def _assignment_statement(self, name: Token) -> AssignStmt:
        self._consume(TokenKind.EQUAL, "expected '=' after assignment target")
        value = self._expression()
        return AssignStmt(name.lexeme, value, name.line, name.column)

    def _print_statement(self) -> PrintStmt:
        keyword = self._previous()
        self._consume(TokenKind.LEFT_PAREN, "expected '(' after 'print'")
        expression = self._expression()
        self._consume(TokenKind.RIGHT_PAREN, "expected ')' after print expression")
        return PrintStmt(expression, keyword.line, keyword.column)

    def _if_statement(self) -> IfStmt:
        keyword = self._previous()
        condition = self._expression()
        opening_brace = self._consume(
            TokenKind.LEFT_BRACE, "expected '{' after if condition"
        )
        then_branch = self._block_statement(opening_brace)
        else_branch = None
        if self._match(TokenKind.ELSE):
            opening_brace = self._consume(
                TokenKind.LEFT_BRACE, "expected '{' after 'else'"
            )
            else_branch = self._block_statement(opening_brace)
        return IfStmt(
            condition,
            then_branch,
            else_branch,
            keyword.line,
            keyword.column,
        )

    def _block_statement(self, opening_brace: Token) -> BlockStmt:
        statements: list[Statement] = []
        while not self._check(TokenKind.RIGHT_BRACE) and not self._at_end():
            statements.append(self._statement())
        self._consume(TokenKind.RIGHT_BRACE, "expected '}' after block")
        return BlockStmt(statements, opening_brace.line, opening_brace.column)

    def _expression(self) -> Expression:
        return self._equality()

    def _equality(self) -> Expression:
        expression = self._comparison()
        while self._match(TokenKind.EQUAL_EQUAL, TokenKind.BANG_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expression = BinaryExpr(
                expression,
                operator.lexeme,
                right,
                operator.line,
                operator.column,
            )
        return expression

    def _comparison(self) -> Expression:
        expression = self._term()
        while self._match(
            TokenKind.GREATER,
            TokenKind.GREATER_EQUAL,
            TokenKind.LESS,
            TokenKind.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expression = BinaryExpr(
                expression,
                operator.lexeme,
                right,
                operator.line,
                operator.column,
            )
        return expression

    def _term(self) -> Expression:
        expression = self._factor()
        while self._match(TokenKind.PLUS, TokenKind.MINUS):
            operator = self._previous()
            right = self._factor()
            expression = BinaryExpr(
                expression,
                operator.lexeme,
                right,
                operator.line,
                operator.column,
            )
        return expression

    def _factor(self) -> Expression:
        expression = self._unary()
        while self._match(TokenKind.STAR, TokenKind.SLASH):
            operator = self._previous()
            right = self._unary()
            expression = BinaryExpr(
                expression,
                operator.lexeme,
                right,
                operator.line,
                operator.column,
            )
        return expression

    def _unary(self) -> Expression:
        if self._match(TokenKind.BANG, TokenKind.MINUS):
            operator = self._previous()
            operand = self._unary()
            return UnaryExpr(
                operator.lexeme,
                operand,
                operator.line,
                operator.column,
            )
        return self._primary()

    def _primary(self) -> Expression:
        if self._match(TokenKind.INTEGER):
            token = self._previous()
            assert isinstance(token.literal, int)
            return IntLiteral(token.literal, token.line, token.column)
        if self._match(TokenKind.STRING):
            token = self._previous()
            assert isinstance(token.literal, str)
            return StringLiteral(token.literal, token.line, token.column)
        if self._match(TokenKind.TRUE, TokenKind.FALSE):
            token = self._previous()
            assert isinstance(token.literal, bool)
            return BoolLiteral(token.literal, token.line, token.column)
        if self._match(TokenKind.IDENTIFIER):
            token = self._previous()
            return Identifier(token.lexeme, token.line, token.column)
        if self._match(TokenKind.LEFT_PAREN):
            opening_parenthesis = self._previous()
            expression = self._expression()
            self._consume(
                TokenKind.RIGHT_PAREN, "expected ')' after grouped expression"
            )
            return GroupingExpr(
                expression,
                opening_parenthesis.line,
                opening_parenthesis.column,
            )

        token = self._peek()
        self._raise_at(token, f"expected expression, found {self._describe(token)}")

    def _match(self, *kinds: TokenKind) -> bool:
        if any(self._check(kind) for kind in kinds):
            self._advance()
            return True
        return False

    def _consume(self, kind: TokenKind, message: str) -> Token:
        if self._check(kind):
            return self._advance()
        self._raise_at(self._peek(), message)

    def _check(self, kind: TokenKind) -> bool:
        return self._peek().kind is kind

    def _advance(self) -> Token:
        if not self._at_end():
            self._current += 1
        return self._previous()

    def _at_end(self) -> bool:
        return self._peek().kind is TokenKind.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    @staticmethod
    def _describe(token: Token) -> str:
        if token.kind is TokenKind.EOF:
            return "end of input"
        return repr(token.lexeme)

    @staticmethod
    def _raise_at(token: Token, message: str) -> None:
        raise AegisSyntaxError(message, token.line, token.column)


def parse(source: str) -> Program:
    """Tokenize and parse AegisLang source text."""
    return Parser(tokenize(source)).parse()
