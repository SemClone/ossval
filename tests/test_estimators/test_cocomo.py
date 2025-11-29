"""Tests for COCOMO II estimator."""

from ossval.estimators.cocomo import COCOMO2Estimator
from ossval.models import (
    ComplexityLevel,
    ComplexityMetrics, Package, Region, SLOCMetrics
)


def test_cocomo_estimate_basic():
    """Test basic COCOMO II estimation."""
    estimator = COCOMO2Estimator()
    
    package = Package(
        name="test",
        sloc=SLOCMetrics(
            total=10000,
            code_lines=8000,
            comment_lines=1500,
            blank_lines=500,
            by_language={"python": 8000},
        ),
        complexity=ComplexityMetrics(
            cyclomatic_complexity_avg=10.0,
            complexity_level=ComplexityLevel.MODERATE,
        ),
    )
    
    result = estimator.estimate(package, Region.US_SF)
    
    assert result.cost_usd > 0
    assert result.effort_person_months > 0
    assert result.methodology == "COCOMO II"
    assert result.region == Region.US_SF
    assert result.cost_usd_low < result.cost_usd < result.cost_usd_high


def test_cocomo_zero_sloc():
    """Test COCOMO with zero SLOC."""
    estimator = COCOMO2Estimator()
    
    package = Package(name="test", sloc=None)
    
    result = estimator.estimate(package, Region.US_SF)
    
    assert result.cost_usd == 0
    assert result.effort_person_months == 0


def test_cocomo_custom_parameters():
    """Test COCOMO with custom parameters."""
    estimator = COCOMO2Estimator(a=3.0, b=1.1, eaf=1.2)
    
    package = Package(
        name="test",
        sloc=SLOCMetrics(
            total=10000,
            code_lines=8000,
            comment_lines=1500,
            blank_lines=500,
            by_language={"python": 8000},
        ),
    )
    
    result = estimator.estimate(package, Region.US_SF)
    assert result.cost_usd > 0

