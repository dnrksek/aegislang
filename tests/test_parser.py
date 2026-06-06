"""Bootstrap smoke tests for the parser module."""

import aegis.parser


def test_parser_module_is_available() -> None:
    assert aegis.parser.__doc__
