# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.1] - 2025-12-08

### Added
- **Advanced Code Complexity Metrics**
  - Halstead complexity metrics (vocabulary, length, volume, difficulty, effort, time, bugs)
  - Automated complexity analysis from code AST without user input
  - Support for calculating estimated bugs based on Halstead volume

- **Git Repository History Analysis**
  - Commit count and contributor tracking
  - Repository age calculation (days and years)
  - Release/tag counting for maturity assessment
  - Commit frequency analysis (commits per month)
  - File churn detection (frequently modified files)
  - Bus factor calculation (key contributor dependency)
  - Average files changed per commit metric

- **Maintainability Index**
  - Microsoft's Maintainability Index calculation (0-100 scale)
  - Combines Halstead volume, cyclomatic complexity, LOC, and comment ratio
  - Automatic classification (Low/Medium/High maintainability)
  - Comment ratio tracking
  - Complexity per KLOC calculation

- **Enhanced Cost Estimation**
  - Maturity multiplier (1.0x - 2.5x) based on project age, contributors, and commits
  - Halstead-based complexity multiplier (0.8x - 1.8x) based on code difficulty
  - Improved confidence scoring incorporating all available metrics
  - More accurate estimates for mature, large-scale projects

- **Testing**
  - 50+ new unit tests for all analyzers
  - Comprehensive git history analyzer tests (9 tests)
  - Halstead complexity analyzer tests (8 tests)
  - Maintainability calculator tests (10 tests)
  - Enhanced multiplier tests (13 tests)
  - End-to-end integration tests (4 tests)
  - Total test suite: 87 tests, all passing

### Changed
- COCOMO II estimator now incorporates maturity and Halstead multipliers
- SLOCCount estimator updated with new multiplier support
- Cost estimates now include maturity_multiplier and halstead_multiplier fields
- Confidence scores adjusted to account for additional metrics

### Improved
- More accurate cost estimates for mature projects with extensive history
- Better handling of complex codebases through Halstead metrics
- Realistic valuation for framework-level projects (e.g., ReactJS)

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

[Unreleased]: https://github.com/SemClone/ossval/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/SemClone/ossval/compare/v1.0.1...v1.2.1
[1.0.1]: https://github.com/SemClone/ossval/releases/tag/v1.0.1