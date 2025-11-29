"""Tests for simple text parser."""

from ossval.parsers.simple import SimpleParser


def test_can_parse_simple_text(tmp_path):
    """Test that parser can identify simple text format."""
    parser = SimpleParser()
    
    # Create a simple text file
    test_file = tmp_path / "packages.txt"
    test_file.write_text("requests==2.31.0\n")
    
    assert parser.can_parse(str(test_file)) is True


def test_parse_simple_text(tmp_path):
    """Test parsing simple text format."""
    parser = SimpleParser()
    
    test_file = tmp_path / "packages.txt"
    test_file.write_text(
        """requests==2.31.0
lodash@4.17.21
com.google.guava:guava:32.1.2
tokio
"""
    )
    
    result = parser.parse(str(test_file))
    
    assert len(result.packages) >= 3
    # Check pip format
    assert any(pkg.name == "requests" and pkg.ecosystem == "pypi" for pkg in result.packages)
    # Check npm format
    assert any(pkg.name == "lodash" and pkg.ecosystem == "npm" for pkg in result.packages)
    # Check maven format
    assert any("guava" in pkg.name and pkg.ecosystem == "maven" for pkg in result.packages)

