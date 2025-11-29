"""Tests for package.json parser."""

from ossval.parsers.package_json import PackageJsonParser


def test_can_parse_package_json(sample_package_json):
    """Test that parser can identify package.json."""
    parser = PackageJsonParser()
    assert parser.can_parse(sample_package_json) is True


def test_parse_package_json(sample_package_json):
    """Test parsing package.json."""
    parser = PackageJsonParser()
    result = parser.parse(sample_package_json)

    assert len(result.packages) >= 2
    # Check that express and lodash are parsed
    names = [pkg.name for pkg in result.packages]
    assert "express" in names
    assert "lodash" in names

