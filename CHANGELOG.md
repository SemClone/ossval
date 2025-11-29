# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions workflows for CI/CD pipeline
  - Test workflow with matrix testing (Ubuntu/macOS, Python 3.13)
  - License checking workflow for dependency compliance
  - PR validation workflow
  - PyPI publishing workflow for releases
- Project governance documentation
  - CONTRIBUTING.md with contribution guidelines
  - SECURITY.md with security policy and vulnerability reporting
- Project URLs in pyproject.toml for better PyPI integration
  - Homepage, Repository, Documentation, Bug Tracker, Source Code links

### Fixed
- Git URL normalization in `repo_finder.py` to correctly handle SSH URLs
- GitHub Actions test failures by installing all dev dependencies including pytest-asyncio
- Async test support configuration in pyproject.toml

### Changed
- Updated test workflow to use `pip install -e ".[dev]"` instead of manually installing test dependencies

## [0.1.0] - 2025-11-28

### Added
- Initial release of OSS Value Calculator
- Core functionality for calculating development cost savings from OSS dependencies
- Support for multiple input formats:
  - requirements.txt (Python)
  - package.json (Node.js)
  - CycloneDX SBOM
  - SPDX SBOM
  - Simple text list
- COCOMO II estimation model for cost calculations
- CLI interface with multiple output formats (JSON, CSV, text)
- Caching system for improved performance
- Regional salary data for accurate cost estimates
- Project type detection and multipliers
- Comprehensive test suite with pytest

### Features
- Quick estimation mode for rapid assessments
- Detailed analysis with SLOC metrics
- Support for various package ecosystems (PyPI, npm, cargo, go, rubygems, maven)
- Repository URL discovery from package metadata
- Complexity analysis for code quality assessment
- Health metrics for package maintenance status

[Unreleased]: https://github.com/SemClone/ossval/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SemClone/ossval/releases/tag/v0.1.0