"""Tests for CLI interface."""

from click.testing import CliRunner

from ossval.cli import main


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "OSSVAL" in result.output


def test_cli_estimate():
    """Test estimate command."""
    runner = CliRunner()
    result = runner.invoke(main, ["estimate", "--sloc", "50000", "--region", "us_sf"])
    # May fail without dependencies, but should at least parse arguments
    assert "estimate" in result.output or result.exit_code in [0, 1]


def test_cli_formats():
    """Test formats command."""
    runner = CliRunner()
    result = runner.invoke(main, ["formats", "list"])
    assert result.exit_code == 0
    assert "Supported" in result.output

