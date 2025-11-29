"""Multipliers for project types and complexity levels."""

from ossval.models import ComplexityLevel, ProjectType

# Project type multipliers (salary and effort)
# Effort multiplier = sqrt(salary multiplier) - expertise affects salary more than raw effort
PROJECT_TYPE_MULTIPLIERS: dict[ProjectType, dict[str, float]] = {
    ProjectType.SCRIPT: {"salary": 0.7, "effort": 0.84},
    ProjectType.LIBRARY: {"salary": 1.0, "effort": 1.0},
    ProjectType.FRAMEWORK: {"salary": 1.15, "effort": 1.07},
    ProjectType.COMPILER: {"salary": 1.5, "effort": 1.22},
    ProjectType.DATABASE: {"salary": 1.4, "effort": 1.18},
    ProjectType.OPERATING_SYSTEM: {"salary": 1.5, "effort": 1.22},
    ProjectType.CRYPTOGRAPHY: {"salary": 1.6, "effort": 1.26},
    ProjectType.MACHINE_LEARNING: {"salary": 1.4, "effort": 1.18},
    ProjectType.NETWORKING: {"salary": 1.2, "effort": 1.10},
    ProjectType.EMBEDDED: {"salary": 1.25, "effort": 1.12},
    ProjectType.GRAPHICS: {"salary": 1.3, "effort": 1.14},
    ProjectType.SCIENTIFIC: {"salary": 1.2, "effort": 1.10},
    ProjectType.DEVTOOLS: {"salary": 1.1, "effort": 1.05},
}

# Complexity multipliers based on cyclomatic complexity
COMPLEXITY_MULTIPLIERS: dict[ComplexityLevel, float] = {
    ComplexityLevel.TRIVIAL: 0.7,
    ComplexityLevel.SIMPLE: 0.9,
    ComplexityLevel.MODERATE: 1.0,
    ComplexityLevel.COMPLEX: 1.3,
    ComplexityLevel.VERY_COMPLEX: 1.7,
}


def get_project_type_multiplier(project_type: ProjectType, multiplier_type: str = "effort") -> float:
    """Get multiplier for a project type."""
    multipliers = PROJECT_TYPE_MULTIPLIERS.get(project_type, PROJECT_TYPE_MULTIPLIERS[ProjectType.LIBRARY])
    return multipliers.get(multiplier_type, 1.0)


def get_complexity_multiplier(complexity_level: ComplexityLevel) -> float:
    """Get multiplier for a complexity level."""
    return COMPLEXITY_MULTIPLIERS.get(complexity_level, 1.0)

