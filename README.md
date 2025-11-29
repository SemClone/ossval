# OSSVAL: Open Source Software Valuation

Calculate the development cost savings from using open source software by analyzing SBOMs or package lists.

## Installation

```bash
pip install ossval
```

## Quick Start

### CLI Usage

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

### Python API

```python
from ossval import analyze, quick_estimate
from ossval.models import AnalysisConfig, Region

# Full analysis
result = await analyze("sbom.json", AnalysisConfig(region=Region.US_SF))
print(f"Total value: ${result.summary['total_cost_usd']:,.0f}")

# Quick estimate
estimate = quick_estimate(sloc=50000, region=Region.US_SF)
print(f"Estimated cost: ${estimate['cost_usd']:,.0f}")
```

## Supported Formats

- **SBOM Formats**: CycloneDX (JSON/XML), SPDX (JSON/tag-value)
- **Lockfiles**: requirements.txt, package.json, Cargo.toml, go.mod, pom.xml, and more
- **Simple Text**: One package per line

## Features

- ✅ COCOMO II and SLOCCount cost estimation models
- ✅ Regional salary data for 18+ regions
- ✅ Project type detection and multipliers
- ✅ SLOC counting with pygount
- ✅ Complexity analysis with radon
- ✅ GitHub health metrics integration
- ✅ Critical package identification
- ✅ Multiple output formats (text, JSON, CSV)

## Documentation

See [SPEC.md](SPEC.md) for complete documentation.

## License

Apache 2.0
