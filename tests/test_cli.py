"""Tests for the placeholder AegisLang CLI."""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[1]
EXAMPLE = PROJECT_ROOT / "examples" / "hello.aegis"


def run_cli(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "aegis", command, str(EXAMPLE)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_check_command_is_wired() -> None:
    result = run_cli("check")

    assert result.returncode == 0
    assert result.stdout.strip() == "OK"
    assert result.stderr == ""


def test_run_command_is_wired() -> None:
    result = run_cli("run")

    assert result.returncode == 0
    assert result.stdout.strip() == "AegisLang run placeholder"
    assert result.stderr == ""
