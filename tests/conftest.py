"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_requirements_txt(tmp_path):
    """Create a sample requirements.txt file."""
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(
        """requests==2.31.0
numpy>=1.24.0
pandas==2.1.0
"""
    )
    return str(requirements_file)


@pytest.fixture
def sample_package_json(tmp_path):
    """Create a sample package.json file."""
    package_json = tmp_path / "package.json"
    package_json.write_text(
        """{
  "name": "test-project",
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
"""
    )
    return str(package_json)

