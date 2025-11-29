"""Tests for CycloneDX parser."""

import json
import tempfile
from pathlib import Path

from ossval.parsers.cyclonedx import CycloneDXParser


def test_can_parse_cyclonedx_json(tmp_path):
    """Test that parser can identify CycloneDX JSON."""
    parser = CycloneDXParser()
    
    # Create a minimal CycloneDX JSON
    test_file = tmp_path / "sbom.json"
    data = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "components": [
            {
                "type": "library",
                "name": "requests",
                "version": "2.31.0",
                "purl": "pkg:pypi/requests@2.31.0",
            }
        ],
    }
    test_file.write_text(json.dumps(data))
    
    assert parser.can_parse(str(test_file)) is True


def test_parse_cyclonedx_json(tmp_path):
    """Test parsing CycloneDX JSON."""
    parser = CycloneDXParser()
    
    test_file = tmp_path / "sbom.json"
    data = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "components": [
            {
                "type": "library",
                "name": "requests",
                "version": "2.31.0",
                "purl": "pkg:pypi/requests@2.31.0",
            },
            {
                "type": "application",  # Should be skipped
                "name": "my-app",
                "version": "1.0.0",
            },
        ],
    }
    test_file.write_text(json.dumps(data))
    
    result = parser.parse(str(test_file))
    
    assert len(result.packages) == 1
    assert result.packages[0].name == "requests"
    assert result.packages[0].ecosystem == "pypi"

