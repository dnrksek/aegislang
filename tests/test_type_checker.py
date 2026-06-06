"""Bootstrap smoke tests for the type checker module."""

import aegis.type_checker


def test_type_checker_module_is_available() -> None:
    assert aegis.type_checker.__doc__
