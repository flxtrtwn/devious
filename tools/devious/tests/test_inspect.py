"""Tests for devious inspect subcommand."""
from pathlib import Path

from click.testing import CliRunner
from devious.cli import cli


def test_files() -> None:
    runner = CliRunner()
    result = runner.invoke(  # pyright: ignore reportUnknownMemberType
        cli, ["inspect", "files", str(Path(__file__).parent.resolve())]
    )
    assert "test_inspect.py" in result.stdout
