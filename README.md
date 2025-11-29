# OSSVAL - Open Source Software Valuation

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/ossval.svg)](https://badge.fury.io/py/ossval)

Calculate the development cost savings from using open source software by analyzing SBOMs or package lists. Provides comprehensive cost estimation using COCOMO II and SLOCCount models with regional salary data, project type detection, and comprehensive source code analysis.

## Features

* **Multi-Ecosystem Support**: PyPI, npm, Cargo, Maven, Go, RubyGems, and more
* **Cost Estimation Models**: COCOMO II and SLOCCount with configurable parameters
* **Regional Salary Data**: 18+ regions with accurate cost calculations
* **Project Type Detection**: Automatic classification with appropriate multipliers
* **Source Code Analysis**: SLOC counting, complexity analysis, and health metrics
* **Multiple Input Formats**: SBOMs (CycloneDX, SPDX) and lockfiles (requirements.txt, package.json, etc.)
* **Comprehensive Output**: Text, JSON, and CSV formats with detailed breakdowns

## Installation

```bash
pip install ossval
```

## Quick Start

```bash
# Analyze an SBOM file
ossval analyze sbom.json

# Specify region for salary calculations
ossval analyze sbom.json --region us_sf

# Output to JSON
ossval analyze sbom.json --format json --output results.json

# Quick estimate from SLOC
ossval estimate --sloc 50000 --region us_sf --type compiler
```

## Usage

### CLI Usage

```bash
# Analyze an SBOM or lockfile
ossval analyze pyproject.toml

# With specific region
ossval analyze package.json --region us_sf

# Output formats
ossval analyze sbom.json --format json --output results.json

# Skip repository cloning (faster, but no SLOC analysis)
ossval analyze sbom.json --no-clone

# List supported formats
ossval formats list

# Cache management
ossval cache clear
ossval cache info
```


## Examples

### Analyze Python Project

```bash
ossval analyze pyproject.toml --region global_average
```

### Analyze npm Project

```bash
ossval analyze package-lock.json --format json --output npm-analysis.json
```

### Compare Regions

```bash
ossval analyze sbom.json --region us_sf > us_sf_results.txt
ossval analyze sbom.json --region global_average > global_results.txt
```

### Quick Cost Estimate

```bash
ossval estimate --sloc 100000 --region us_sf --type framework
# Output:
# Estimated cost: $16,754,251
#   Range: $11,727,975 - $25,131,376
#   Effort: 22.1 person-years
#   Methodology: COCOMO II
```

## Integration with SEMCL.ONE

OSSVAL is a core component of the SEMCL.ONE ecosystem, enabling comprehensive OSS valuation and cost analysis:

* Works with **purl2src** for repository URL discovery from Package URLs
* Integrates with **purl2notices** for complete legal compliance workflows
* Supports **SBOM** analysis from CycloneDX and SPDX formats
* Complements **osslili** for license analysis and compliance checking

## Methodology

### COCOMO II Model

The primary cost estimation model uses COCOMO II with:
- **Effort Calculation**: `Effort = a × (KSLOC)^b × EAF × Complexity × Project_Type`
- **Cost Calculation**: `Cost = Effort × Monthly_Salary × Region_Multiplier`
- **Configurable Parameters**: Scale factors, effort adjustment factors, and multipliers

### SLOCCount Model

Alternative simpler model:
- **Effort Calculation**: Based on SLOC and language-specific productivity rates
- **Cost Calculation**: `Cost = Effort × Annual_Salary`

### Project Type Detection

Automatic classification based on keywords and repository analysis:
- Compiler, Framework, Library, Networking, Database, Machine Learning, and more
- Each type has specific effort multipliers

---

## Contributing

We welcome contributions! Please see the repository for details on:

* Development setup
* Submitting pull requests
* Reporting issues

## Support

For support and questions:

- [GitHub Issues](https://github.com/SemClone/ossval/issues) - Bug reports and feature requests
- [SEMCL.ONE Community](https://semcl.one) - Ecosystem support and discussions

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

---

_Part of the SEMCL.ONE ecosystem for comprehensive OSS compliance and code analysis._
