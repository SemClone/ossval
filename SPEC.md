# OSSVAL: Open Source Software Valuation

## Project Overview

**Purpose**: A Python tool that calculates the development cost savings from using open source software by analyzing SBOMs or package lists. The tool quantifies the dollar value of OSS dependencies, helping organizations understand their reliance on open source and identify critical packages that deserve funding or contribution.

**Target Users**: 
- Open source program offices (OSPOs)
- Engineering leadership demonstrating OSS value to executives
- Organizations evaluating business continuity risks
- Foundations advocating for OSS funding

**Usage Modes**:
1. CLI tool (`ossval analyze sbom.json`)
2. Python library (`from ossval import analyze`)

---

## Core Features

### 1. Input Parsing

**Supported SBOM Formats**:
- CycloneDX (JSON, XML)
- SPDX (JSON, tag-value format)

**Supported Lockfiles/Package Lists** (top 12 ecosystems):
| Ecosystem | Files |
|-----------|-------|
| Python/PyPI | `requirements.txt`, `Pipfile.lock`, `poetry.lock`, `pyproject.toml` |
| JavaScript/npm | `package.json`, `package-lock.json`, `yarn.lock` |
| Java/Maven | `pom.xml` |
| Java/Gradle | `build.gradle`, `gradle.lockfile` |
| Rust/Cargo | `Cargo.toml`, `Cargo.lock` |
| Go | `go.mod`, `go.sum` |
| Ruby/Gems | `Gemfile`, `Gemfile.lock` |
| PHP/Composer | `composer.json`, `composer.lock` |
| C#/NuGet | `*.csproj`, `packages.config` |
| Swift | `Package.swift`, `Package.resolved` |
| C/C++ Conan | `conanfile.txt`, `conan.lock` |
| C/C++ vcpkg | `vcpkg.json` |

**Simple Text Format**:
```
# One package per line, formats:
requests==2.31.0          # pip style
lodash@4.17.21            # npm style
com.google.guava:guava:32.1.2  # maven style
tokio                     # name only (will lookup latest)
```

### 2. Cost Estimation Model

**Primary Model**: COCOMO II (Constructive Cost Model)

```
Effort (person-months) = a × (KSLOC)^b × EAF × Complexity_Multiplier × Project_Type_Multiplier

Where:
- a = 2.94 (calibration constant)
- b = 1.0997 (scale factor)
- KSLOC = thousands of source lines of code
- EAF = Effort Adjustment Factor (product of cost drivers, default 1.0)

Cost (USD) = Effort × Monthly_Fully_Loaded_Rate
```

**Alternative Model**: SLOCCount (simpler)
```
Effort = 2.4 × (KSLOC)^1.05
```

### 3. Regional Salary Data

Base annual salaries (USD) for mid-senior software engineers:

| Region | Base Salary | Overhead Multiplier |
|--------|-------------|---------------------|
| US - San Francisco | $220,000 | 2.3 |
| US - NYC | $200,000 | 2.2 |
| US - Seattle | $210,000 | 2.1 |
| US - Other | $160,000 | 2.0 |
| Canada | $130,000 | 1.9 |
| UK | $95,000 | 1.85 |
| Germany | $90,000 | 1.9 |
| France | $75,000 | 2.0 |
| Netherlands | $85,000 | 1.85 |
| Switzerland | $140,000 | 2.0 |
| Israel | $110,000 | 1.8 |
| Japan | $70,000 | 1.7 |
| Australia | $115,000 | 1.85 |
| India | $30,000 | 1.5 |
| China | $50,000 | 1.6 |
| Brazil | $35,000 | 1.7 |
| Latin America (other) | $28,000 | 1.5 |
| Eastern Europe | $45,000 | 1.5 |
| Global Average | $75,000 | 1.8 |

**Fully Loaded Monthly Rate** = (Annual Salary / 12) × Overhead Multiplier

**Future Enhancement**: Query live salary data from levels.fyi API or similar sources.

### 4. Project Type Multipliers

Different software types require different expertise levels and command different rates:

| Project Type | Salary Multiplier | Effort Multiplier | Detection Keywords |
|--------------|-------------------|-------------------|-------------------|
| Script | 0.7 | 0.84 | `-utils`, `-helper`, simple patterns |
| Library | 1.0 (baseline) | 1.0 | default |
| Framework | 1.15 | 1.07 | `framework`, `react`, `django`, `rails` |
| Compiler/Interpreter | 1.5 | 1.22 | `compiler`, `llvm`, `parser`, `hermes`, `v8` |
| Database | 1.4 | 1.18 | `database`, `sql`, `redis`, `mongo` |
| Operating System | 1.5 | 1.22 | `kernel`, `driver`, `systemd` |
| Cryptography | 1.6 | 1.26 | `crypto`, `ssl`, `tls`, `encryption` |
| Machine Learning | 1.4 | 1.18 | `tensorflow`, `pytorch`, `sklearn` |
| Networking | 1.2 | 1.10 | `http`, `grpc`, `proxy`, `socket` |
| Embedded | 1.25 | 1.12 | `embedded`, `firmware`, `rtos` |
| Graphics/Games | 1.3 | 1.14 | `opengl`, `vulkan`, `graphics`, `game` |
| Scientific | 1.2 | 1.10 | `scipy`, `numerical`, `simulation` |
| DevTools | 1.1 | 1.05 | `lint`, `format`, `debugger`, `ci` |

**Note**: Effort multiplier = sqrt(Salary multiplier) — expertise affects salary more than raw effort.

### 5. Complexity Multipliers

Based on cyclomatic complexity analysis:

| Complexity Level | Avg CC Range | Effort Multiplier |
|------------------|--------------|-------------------|
| Trivial | 1-5 | 0.7 |
| Simple | 6-10 | 0.9 |
| Moderate | 11-20 | 1.0 (baseline) |
| Complex | 21-50 | 1.3 |
| Very Complex | >50 | 1.7 |

### 6. Code Analysis

**SLOC Counting**:
- Use `pygount` library for multi-language SLOC counting
- Count code lines, comment lines, blank lines separately
- Track by language within each package

**Complexity Analysis**:
- Use `radon` for Python cyclomatic complexity
- For other languages: use tree-sitter based analysis or default to "moderate"
- Calculate average, max, and sum of cyclomatic complexity

**Repository Discovery**:
- Query package registries for repository URLs
- PyPI: `https://pypi.org/pypi/{name}/json` → `info.project_urls.Source`
- npm: `https://registry.npmjs.org/{name}` → `repository.url`
- Cargo: `https://crates.io/api/v1/crates/{name}` → `crate.repository`
- Go: Infer from module path (e.g., `github.com/user/repo`)
- RubyGems: `https://rubygems.org/api/v1/gems/{name}.json` → `source_code_uri`

**Cloning Strategy**:
- Shallow clone (`git clone --depth 1`) for SLOC analysis
- Cache analyzed results to disk
- Support async/parallel cloning (configurable concurrency)

### 7. Health Metrics (for Criticality Ranking)

Fetch from GitHub API when repository URL points to GitHub:

| Metric | Source | Use |
|--------|--------|-----|
| Stars | GitHub API | Popularity indicator |
| Forks | GitHub API | Community engagement |
| Contributors count | GitHub API | Bus factor approximation |
| Open issues | GitHub API | Maintenance burden |
| Last commit date | GitHub API | Activity indicator |
| Created date | GitHub API | Project maturity |
| License | GitHub API | Compliance |
| Has funding | GitHub API | Sustainability signal |
| Security policy | GitHub API | Security posture |

**Criticality Score** (for prioritization):
A package is "critical" if:
- High value (top 20% by cost OR >1% of total)
- AND has risk factors:
  - Bus factor ≤ 2 contributors
  - No commits in 6+ months
  - No funding mechanism

---

## Output Formats

### 1. Text/Terminal (Rich)

```
════════════════════════════════════════════════════════════════
                    OSSVAL Analysis Report
                    Generated: 2024-01-15 14:30:22
════════════════════════════════════════════════════════════════

Executive Summary
──────────────────────────────────────────────────────────────

💰 Total OSS Value: $47,832,500
   Estimate Range: $33,482,750 - $71,748,750

⏱️  Development Effort: 142.3 person-years (1,708 person-months)

📊 Total Source Lines: 8,432,100

📦 Packages Analyzed: 847 / 852
   ⚠ 5 packages had analysis errors

Top 10 Packages by Value
──────────────────────────────────────────────────────────────
  #  Package                        Value (USD)      % of Total
  1  linux-kernel                   $12,450,000         26.0%
  2  chromium                        $8,230,000         17.2%
  3  tensorflow                      $4,120,000          8.6%
  ...

Value by Language
──────────────────────────────────────────────────────────────
  C               $18,500,000 (38.7%) ███████████████████
  Python           $9,200,000 (19.2%) █████████
  JavaScript       $7,100,000 (14.8%) ███████
  ...

⚠ Critical Packages Requiring Attention
──────────────────────────────────────────────────────────────
  Package         Value        Contributors  Last Commit  Risk Factors
  core-js         $890,000     1             2y ago       Low bus factor, Inactive
  left-pad        $12,000      1             4y ago       Low bus factor, No funding
  ...

──────────────────────────────────────────────────────────────
Methodology: COCOMO II | Region: us_sf | Source: cyclonedx
```

### 2. JSON Output

```json
{
  "meta": {
    "tool": "ossval",
    "version": "0.1.0",
    "analyzed_at": "2024-01-15T14:30:22Z",
    "source_file": "sbom.json",
    "source_type": "cyclonedx",
    "config": {
      "region": "us_sf",
      "clone_repos": true,
      "methodology": "cocomo2"
    }
  },
  "summary": {
    "total_packages": 852,
    "analyzed_packages": 847,
    "failed_packages": 5,
    "total_sloc": 8432100,
    "total_effort_person_months": 1708,
    "total_effort_person_years": 142.3,
    "total_cost_usd": 47832500,
    "total_cost_usd_low": 33482750,
    "total_cost_usd_high": 71748750
  },
  "by_language": {
    "c": 18500000,
    "python": 9200000,
    "javascript": 7100000
  },
  "by_ecosystem": {
    "pypi": 9200000,
    "npm": 7100000,
    "cargo": 3400000
  },
  "by_project_type": {
    "library": 25000000,
    "framework": 12000000,
    "compiler": 5000000
  },
  "packages": [
    {
      "name": "requests",
      "version": "2.31.0",
      "ecosystem": "pypi",
      "language": "python",
      "project_type": "library",
      "repository_url": "https://github.com/psf/requests",
      "sloc": {
        "total": 15420,
        "code_lines": 12300,
        "comment_lines": 2100,
        "by_language": {"python": 15420}
      },
      "complexity": {
        "cyclomatic_complexity_avg": 8.5,
        "cyclomatic_complexity_max": 45,
        "complexity_level": "simple"
      },
      "health": {
        "stars": 50000,
        "contributors_count": 450,
        "last_commit_date": "2024-01-10T12:00:00Z",
        "bus_factor": 12,
        "is_actively_maintained": true
      },
      "cost_estimate": {
        "effort_person_months": 42.5,
        "effort_person_years": 3.54,
        "cost_usd": 1890000,
        "cost_usd_low": 1323000,
        "cost_usd_high": 2835000,
        "methodology": "COCOMO II",
        "confidence": 0.85
      }
    }
  ],
  "critical_packages": [
    {
      "name": "core-js",
      "cost_usd": 890000,
      "risk_factors": ["low_bus_factor", "inactive"]
    }
  ],
  "errors": [],
  "warnings": ["Package xyz: could not find repository URL"]
}
```

### 3. CSV Output

Two files:

**summary.csv**:
```csv
metric,value
total_packages,852
analyzed_packages,847
total_sloc,8432100
total_effort_person_months,1708
total_cost_usd,47832500
total_cost_usd_low,33482750
total_cost_usd_high,71748750
```

**packages.csv**:
```csv
name,version,ecosystem,language,project_type,sloc,complexity_level,cost_usd,cost_usd_low,cost_usd_high,effort_months,contributors,last_commit,is_critical
requests,2.31.0,pypi,python,library,15420,simple,1890000,1323000,2835000,42.5,450,2024-01-10,false
core-js,3.35.0,npm,javascript,library,45000,moderate,890000,623000,1335000,20.1,1,2022-03-15,true
```

---

## CLI Interface

```bash
# Basic usage
ossval analyze sbom.json

# Specify region for salary calculations
ossval analyze sbom.json --region us_sf

# Output formats
ossval analyze sbom.json --format json --output results.json
ossval analyze sbom.json --format csv --output results/
ossval analyze sbom.json --format text  # default, to stdout

# Analysis options
ossval analyze sbom.json --no-clone      # Don't clone repos, use registry metadata
ossval analyze sbom.json --no-cache      # Don't use cached results
ossval analyze sbom.json --concurrency 8 # Parallel clone jobs

# Quick estimate without SBOM
ossval estimate --sloc 50000 --region us_sf --type compiler

# List supported formats
ossval formats

# Clear cache
ossval cache clear
ossval cache info
```

**CLI Options**:

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--region` | `-r` | `global_average` | Region for salary calculation |
| `--format` | `-f` | `text` | Output format: text, json, csv |
| `--output` | `-o` | stdout | Output file/directory |
| `--clone/--no-clone` | | `--clone` | Clone repos for accurate SLOC |
| `--cache/--no-cache` | | `--cache` | Use disk cache |
| `--cache-dir` | | `~/.cache/ossval` | Cache directory |
| `--concurrency` | `-c` | 4 | Max parallel operations |
| `--github-token` | | env `GITHUB_TOKEN` | GitHub API token |
| `--verbose` | `-v` | | Verbose output |
| `--quiet` | `-q` | | Minimal output |

---

## Library API

```python
from ossval import analyze, quick_estimate, parse_sbom
from ossval.models import AnalysisConfig, Region, ProjectType

# Quick estimate
result = quick_estimate(
    sloc=50000,
    region=Region.US_SF,
    project_type=ProjectType.COMPILER
)
print(f"Estimated cost: ${result['cost_usd']:,.0f}")

# Full analysis from file
result = analyze(
    "path/to/sbom.json",
    config=AnalysisConfig(
        region=Region.US_SF,
        clone_repos=True,
        use_cache=True,
    )
)
print(f"Total value: ${result.total_cost_usd:,.0f}")

# Analyze from package list
packages = parse_sbom("""
requests==2.31.0
numpy==1.26.0
pandas==2.1.0
""")
result = analyze(packages, config=AnalysisConfig(region=Region.GERMANY))

# Access individual packages
for pkg in result.packages:
    if pkg.cost_estimate:
        print(f"{pkg.name}: ${pkg.cost_estimate.cost_usd:,.0f}")

# Get critical packages
for pkg in result.critical_packages:
    print(f"⚠ {pkg.name} needs attention: ${pkg.cost_estimate.cost_usd:,.0f}")

# Export results
result.to_json("results.json")
result.to_csv("results/")
```

---

## Project Structure

```
ossval/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── ossval/
│       ├── __init__.py           # Public API exports
│       ├── cli.py                # Click CLI implementation
│       ├── core.py               # Main orchestration (analyze function)
│       ├── models.py             # Pydantic data models
│       ├── parsers/
│       │   ├── __init__.py
│       │   ├── base.py           # Abstract parser class
│       │   ├── cyclonedx.py      # CycloneDX parser
│       │   ├── spdx.py           # SPDX parser
│       │   ├── requirements.py   # Python requirements.txt
│       │   ├── package_json.py   # npm package.json
│       │   ├── cargo.py          # Rust Cargo.toml/lock
│       │   ├── go_mod.py         # Go go.mod
│       │   ├── maven.py          # Maven pom.xml
│       │   ├── gradle.py         # Gradle files
│       │   ├── gemfile.py        # Ruby Gemfile
│       │   ├── composer.py       # PHP composer.json
│       │   ├── nuget.py          # C# NuGet
│       │   ├── swift.py          # Swift Package.swift
│       │   ├── conan.py          # C/C++ Conan
│       │   └── simple.py         # Plain text package list
│       ├── analyzers/
│       │   ├── __init__.py
│       │   ├── sloc.py           # SLOC counting with pygount
│       │   ├── complexity.py     # Complexity analysis with radon
│       │   ├── repo_finder.py    # Repository URL discovery
│       │   └── health.py         # GitHub health metrics
│       ├── estimators/
│       │   ├── __init__.py
│       │   ├── base.py           # Abstract estimator
│       │   ├── cocomo.py         # COCOMO II implementation
│       │   ├── sloccount.py      # SLOCCount model
│       │   └── hybrid.py         # Combined approach
│       ├── data/
│       │   ├── __init__.py
│       │   ├── salaries.py       # Regional salary data
│       │   ├── multipliers.py    # Project type & complexity multipliers
│       │   └── project_types.py  # Project type detection patterns
│       ├── output/
│       │   ├── __init__.py
│       │   ├── text.py           # Rich terminal output
│       │   ├── json.py           # JSON formatter
│       │   └── csv.py            # CSV formatter
│       └── cache.py              # Disk caching with diskcache
├── tests/
│   ├── conftest.py
│   ├── test_parsers/
│   ├── test_analyzers/
│   ├── test_estimators/
│   ├── test_cli.py
│   └── fixtures/
│       ├── cyclonedx_sample.json
│       ├── spdx_sample.json
│       └── requirements.txt
└── examples/
    ├── analyze_sbom.py
    ├── compare_regions.py
    └── sample_sboms/
```

---

## Dependencies

```toml
[project]
dependencies = [
    "click>=8.1.0",           # CLI framework
    "pydantic>=2.0.0",        # Data models
    "httpx>=0.25.0",          # Async HTTP client
    "rich>=13.0.0",           # Terminal formatting
    "gitpython>=3.1.0",       # Git operations
    "pygount>=1.6.0",         # SLOC counting
    "radon>=6.0.0",           # Python complexity analysis
    "diskcache>=5.6.0",       # Disk caching
    "toml>=0.10.0",           # TOML parsing (Cargo.toml, etc.)
    "aiofiles>=23.0.0",       # Async file operations
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

---

## Configuration File (Optional)

Support `~/.config/ossval/config.toml` or `.ossval.toml` in project:

```toml
[defaults]
region = "us_sf"
clone_repos = true
concurrency = 8

[cache]
enabled = true
ttl_days = 30
directory = "~/.cache/ossval"

[api_keys]
github_token = "ghp_xxx"  # Or use env var GITHUB_TOKEN

[salary_overrides]
# Override default salaries for specific regions
us_sf = 250000
custom_region = 180000

[project_type_overrides]
# Override multipliers for specific project types
blockchain = 1.45
```

---

## Future Enhancements (v2)

1. **Live salary data**: Query levels.fyi or similar APIs for current salary data
2. **Business continuity risk score**: Combine cost with health metrics for risk assessment
3. **Trend analysis**: Track value over time across SBOM versions
4. **Dependency graph**: Visualize transitive dependencies and their costs
5. **Comparison reports**: Compare two SBOMs (before/after, prod/dev)
6. **License risk overlay**: Flag packages with problematic licenses
7. **Funding recommendations**: Suggest packages that should receive funding
8. **Integration**: GitHub Action, GitLab CI, Jenkins plugin
9. **Web UI**: Dashboard for exploring results
10. **Multi-language complexity**: Tree-sitter based complexity for all languages

---

## Testing Strategy

1. **Unit tests**: Each parser, analyzer, estimator in isolation
2. **Integration tests**: Full pipeline with sample SBOMs
3. **Fixtures**: Real-world SBOM samples from popular projects
4. **Mocking**: Mock GitHub API, package registries for deterministic tests
5. **Snapshot tests**: JSON output structure stability

---

## Error Handling

- Gracefully handle missing repositories (use registry estimates)
- Continue analysis even if some packages fail
- Report warnings without stopping execution
- Provide clear error messages with suggestions
- Log detailed errors for debugging (--verbose)

---

## Performance Considerations

- Async HTTP requests for API calls
- Parallel git clones (configurable concurrency)
- Disk caching with configurable TTL
- Shallow clones only (--depth 1)
- Skip large binary files in SLOC counting
- Rate limiting for GitHub API (respect 5000/hour limit)
