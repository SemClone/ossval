"""Tests for requirements.txt parser."""

from ossval.parsers.requirements import RequirementsParser


def test_can_parse_requirements_txt(sample_requirements_txt):
    """Test that parser can identify requirements.txt."""
    parser = RequirementsParser()
    assert parser.can_parse(sample_requirements_txt) is True


def test_parse_requirements_txt(sample_requirements_txt):
    """Test parsing requirements.txt."""
    parser = RequirementsParser()
    result = parser.parse(sample_requirements_txt)

    assert len(result.packages) == 3
    assert result.packages[0].name == "requests"
    assert result.packages[0].version == "2.31.0"
    assert result.packages[0].ecosystem == "pypi"

