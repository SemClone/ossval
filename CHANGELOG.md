# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-11-29

### Added
- **Core Functionality**
  - Open Source Software Value Calculator for estimating development cost savings
  - COCOMO II estimation model implementation for accurate cost calculations
  - Support for analyzing OSS dependencies across multiple ecosystems
  - Quick estimation mode for rapid assessments
  - Detailed analysis mode with SLOC metrics

- **Input Format Support**
  - requirements.txt (Python)
  - package.json (Node.js)
  - package-lock.json (Node.js)
  - Cargo.toml/Cargo.lock (Rust)
  - go.mod/go.sum (Go)
  - pom.xml (Maven)
  - build.gradle (Gradle)
  - Pipfile/Pipfile.lock (Python)
  - pyproject.toml/poetry.lock (Python)
  - CycloneDX SBOM (JSON/XML)
  - SPDX SBOM (JSON/YAML/Tag-Value)
  - Simple text list of packages
  - yarn.lock (Node.js)

- **Package Ecosystems**
  - PyPI (Python)
  - npm (Node.js)
  - Cargo (Rust)
  - Go modules
  - RubyGems
  - Maven (Java)

- **CLI Features**
  - Interactive command-line interface
  - Multiple output formats (JSON, CSV, human-readable text)
  - Region-based salary calculations for accurate cost estimates
  - Project type detection and cost multipliers
  - Custom methodology support (COCOMO II, SLOCCount)
  - Cache management commands

- **Analysis Features**
  - Repository URL discovery from package metadata
  - SLOC (Source Lines of Code) analysis using pygount
  - Complexity analysis using radon for Python code
  - Package health metrics evaluation
  - Project type detection (web, mobile, embedded, etc.)
  - Regional salary data for 10+ regions worldwide
  - Effort and duration calculations

- **Infrastructure**
  - Persistent caching system using diskcache for improved performance
  - Asynchronous operations for efficient processing
  - Comprehensive error handling and logging
  - Modular architecture with pluggable parsers and estimators

- **Developer Tools**
  - Comprehensive test suite with pytest
  - Test coverage reporting with pytest-cov
  - Type hints throughout the codebase
  - Code quality tools (ruff, mypy)
  - Async test support with pytest-asyncio

- **CI/CD and Documentation**
  - GitHub Actions workflows for continuous integration
    - Automated testing on Ubuntu and macOS
    - Python 3.13 support
    - License compliance checking
    - PR validation
    - Automated PyPI publishing on release
  - CONTRIBUTING.md with contribution guidelines
  - SECURITY.md with vulnerability reporting process
  - Comprehensive README with usage examples
  - Project URLs for PyPI integration

### Fixed
- Git URL normalization for SSH format repositories
- Async test compatibility in CI/CD pipeline
- Proper dev dependency installation in GitHub Actions

### Security
- Dependency vulnerability scanning
- License compliance checking for all dependencies
- Security policy for responsible disclosure

### Performance
- Disk-based caching for API responses and analysis results
- Parallel processing for multiple package analysis
- Efficient SLOC counting with pygount
- Optimized repository URL discovery

[Unreleased]: https://github.com/SemClone/ossval/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/SemClone/ossval/releases/tag/v1.0.1