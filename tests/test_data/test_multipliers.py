"""Tests for multiplier data."""

from ossval.data.multipliers import (
    get_complexity_multiplier,
    get_project_type_multiplier,
)
from ossval.models import ComplexityLevel, ProjectType


def test_get_project_type_multiplier():
    """Test getting project type multipliers."""
    # Library should be baseline (1.0)
    assert get_project_type_multiplier(ProjectType.LIBRARY) == 1.0
    
    # Compiler should have higher multiplier
    compiler_mult = get_project_type_multiplier(ProjectType.COMPILER)
    assert compiler_mult > 1.0
    
    # Script should have lower multiplier
    script_mult = get_project_type_multiplier(ProjectType.SCRIPT)
    assert script_mult < 1.0


def test_get_complexity_multiplier():
    """Test getting complexity multipliers."""
    # Moderate should be baseline (1.0)
    assert get_complexity_multiplier(ComplexityLevel.MODERATE) == 1.0
    
    # Trivial should be lower
    assert get_complexity_multiplier(ComplexityLevel.TRIVIAL) < 1.0
    
    # Very complex should be higher
    assert get_complexity_multiplier(ComplexityLevel.VERY_COMPLEX) > 1.0

