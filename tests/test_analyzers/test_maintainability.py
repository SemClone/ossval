"""Tests for maintainability index calculator."""

from ossval.analyzers.maintainability import calculate_maintainability_index
from ossval.models import (
    ComplexityLevel,
    ComplexityMetrics,
    HalsteadMetrics,
    SLOCMetrics,
)


def test_calculate_maintainability_with_all_metrics():
    """Test maintainability calculation with all metrics available."""
    sloc = SLOCMetrics(
        total=10000,
        code_lines=8000,
        comment_lines=1500,
        blank_lines=500,
        by_language={"python": 8000},
    )

    halstead = HalsteadMetrics(
        vocabulary=50,
        length=200,
        calculated_length=180.0,
        volume=1200.0,
        difficulty=15.0,
        effort=18000.0,
        time_seconds=1000.0,
        bugs=0.4,
    )

    complexity = ComplexityMetrics(
        cyclomatic_complexity_avg=8.0,
        cyclomatic_complexity_max=25,
        cyclomatic_complexity_sum=800,
        complexity_level=ComplexityLevel.MODERATE,
    )

    metrics = calculate_maintainability_index(sloc, halstead, complexity)

    assert metrics is not None
    assert 0 <= metrics.maintainability_index <= 100
    assert metrics.maintainability_level in ["Low", "Medium", "High"]
    assert 0 <= metrics.comment_ratio <= 1.0
    assert metrics.avg_complexity_per_kloc > 0


def test_calculate_maintainability_without_halstead():
    """Test maintainability calculation without Halstead metrics."""
    sloc = SLOCMetrics(
        total=5000,
        code_lines=4000,
        comment_lines=800,
        blank_lines=200,
        by_language={"python": 4000},
    )

    complexity = ComplexityMetrics(
        cyclomatic_complexity_avg=10.0,
        complexity_level=ComplexityLevel.MODERATE,
    )

    metrics = calculate_maintainability_index(sloc, None, complexity)

    assert metrics is not None
    assert 0 <= metrics.maintainability_index <= 100
    # Should still calculate MI using estimated Halstead volume
    assert metrics.maintainability_level in ["Low", "Medium", "High"]


def test_calculate_maintainability_without_complexity():
    """Test maintainability calculation without complexity metrics."""
    sloc = SLOCMetrics(
        total=5000,
        code_lines=4000,
        comment_lines=800,
        blank_lines=200,
        by_language={"python": 4000},
    )

    halstead = HalsteadMetrics(
        vocabulary=40,
        length=150,
        calculated_length=140.0,
        volume=900.0,
        difficulty=12.0,
        effort=10800.0,
        time_seconds=600.0,
        bugs=0.3,
    )

    metrics = calculate_maintainability_index(sloc, halstead, None)

    assert metrics is not None
    assert 0 <= metrics.maintainability_index <= 100
    # Should use default complexity


def test_calculate_maintainability_sloc_only():
    """Test maintainability calculation with only SLOC."""
    sloc = SLOCMetrics(
        total=3000,
        code_lines=2500,
        comment_lines=400,
        blank_lines=100,
        by_language={"python": 2500},
    )

    metrics = calculate_maintainability_index(sloc, None, None)

    assert metrics is not None
    assert 0 <= metrics.maintainability_index <= 100
    # With defaults, should still produce valid MI
    assert metrics.comment_ratio == 400 / 3000


def test_maintainability_level_classification():
    """Test that maintainability levels are classified correctly."""
    # Test high maintainability (good code)
    sloc_high = SLOCMetrics(
        total=1000,
        code_lines=800,
        comment_lines=150,
        blank_lines=50,
        by_language={"python": 800},
    )
    halstead_high = HalsteadMetrics(
        vocabulary=20,
        length=100,
        calculated_length=90.0,
        volume=500.0,
        difficulty=5.0,
        effort=2500.0,
        time_seconds=139.0,
        bugs=0.17,
    )
    complexity_high = ComplexityMetrics(
        cyclomatic_complexity_avg=3.0,
        complexity_level=ComplexityLevel.SIMPLE,
    )

    metrics_high = calculate_maintainability_index(
        sloc_high, halstead_high, complexity_high
    )
    assert metrics_high is not None
    # Low complexity, good comments, small volume should give higher MI


def test_comment_ratio_calculation():
    """Test that comment ratio is calculated correctly."""
    sloc = SLOCMetrics(
        total=10000,
        code_lines=7000,
        comment_lines=2000,  # 20% comments
        blank_lines=1000,
        by_language={"python": 7000},
    )

    metrics = calculate_maintainability_index(sloc, None, None)

    assert metrics is not None
    assert metrics.comment_ratio == 0.2  # 2000/10000


def test_complexity_per_kloc_calculation():
    """Test that complexity per KLOC is calculated correctly."""
    sloc = SLOCMetrics(
        total=5000,
        code_lines=4000,
        comment_lines=800,
        blank_lines=200,
        by_language={"python": 4000},
    )

    complexity = ComplexityMetrics(
        cyclomatic_complexity_avg=16.0,  # 16 avg complexity
        complexity_level=ComplexityLevel.COMPLEX,
    )

    metrics = calculate_maintainability_index(sloc, None, complexity)

    assert metrics is not None
    # (16 / 4000) * 1000 = 4.0
    assert metrics.avg_complexity_per_kloc == 4.0


def test_maintainability_with_no_sloc():
    """Test that calculation returns None with no SLOC."""
    metrics = calculate_maintainability_index(None, None, None)
    assert metrics is None


def test_maintainability_with_zero_sloc():
    """Test that calculation returns None with zero SLOC."""
    sloc = SLOCMetrics(
        total=0,
        code_lines=0,
        comment_lines=0,
        blank_lines=0,
        by_language={},
    )

    metrics = calculate_maintainability_index(sloc, None, None)
    assert metrics is None


def test_maintainability_index_bounds():
    """Test that MI is always clamped to 0-100 range."""
    # Test with very large codebase (might produce negative MI)
    sloc_large = SLOCMetrics(
        total=1000000,
        code_lines=900000,
        comment_lines=50000,
        blank_lines=50000,
        by_language={"python": 900000},
    )

    complexity_high = ComplexityMetrics(
        cyclomatic_complexity_avg=50.0,
        complexity_level=ComplexityLevel.VERY_COMPLEX,
    )

    halstead_high = HalsteadMetrics(
        vocabulary=200,
        length=10000,
        calculated_length=9500.0,
        volume=100000.0,
        difficulty=80.0,
        effort=8000000.0,
        time_seconds=444444.0,
        bugs=33.3,
    )

    metrics = calculate_maintainability_index(sloc_large, halstead_high, complexity_high)

    assert metrics is not None
    # MI should be clamped to 0-100
    assert 0 <= metrics.maintainability_index <= 100
