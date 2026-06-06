"""Bootstrap smoke tests for the interpreter module."""

import aegis.interpreter


def test_interpreter_module_is_available() -> None:
    assert aegis.interpreter.__doc__
