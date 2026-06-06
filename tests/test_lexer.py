"""Bootstrap smoke tests for the lexer module."""

import aegis.lexer


def test_lexer_module_is_available() -> None:
    assert aegis.lexer.__doc__
