"""Diagnostic errors for AegisLang."""


class AegisSyntaxError(Exception):
    """A syntax error tied to a location in AegisLang source code."""

    def __init__(self, message: str, line: int, column: int) -> None:
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"SyntaxError at line {line}, column {column}: {message}")
