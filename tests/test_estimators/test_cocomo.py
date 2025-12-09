"""Tests for COCOMO II estimator."""

from datetime import datetime, timedelta

from ossval.estimators.cocomo import COCOMO2Estimator
from ossval.models import (
    ComplexityLevel,
    ComplexityMetrics,
    GitHistoryMetrics,
    HalsteadMetrics,
    Package,
    Region,
    SLOCMetrics,
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
    # New multipliers should default to 1.0 when no git/halstead data
    assert result.maturity_multiplier == 1.0
    assert result.halstead_multiplier == 1.0


def test_cocomo_zero_sloc():
    """Test COCOMO with zero SLOC."""
    estimator = COCOMO2Estimator()

    package = Package(name="test", sloc=None)

    result = estimator.estimate(package, Region.US_SF)

    assert result.cost_usd == 0
    assert result.effort_person_months == 0
    assert result.maturity_multiplier == 1.0
    assert result.halstead_multiplier == 1.0


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


def test_cocomo_with_git_history():
    """Test COCOMO estimation with git history metrics."""
    estimator = COCOMO2Estimator()

    git_history = GitHistoryMetrics(
        commit_count=10000,
        contributor_count=50,
        age_days=1825,  # 5 years
        age_years=5.0,
        first_commit_date=datetime.now() - timedelta(days=1825),
        last_commit_date=datetime.now(),
        release_count=20,
        commits_per_month=166.0,
        avg_files_per_commit=3.0,
        high_churn_files=30,
        bus_factor=3,
    )

    package = Package(
        name="test",
        sloc=SLOCMetrics(
            total=10000,
            code_lines=8000,
            comment_lines=1500,
            blank_lines=500,
            by_language={"python": 8000},
        ),
        git_history=git_history,
    )

    result = estimator.estimate(package, Region.US_SF)

    assert result.cost_usd > 0
    # Mature project should have maturity multiplier > 1.0
    assert result.maturity_multiplier > 1.0


def test_cocomo_with_halstead_metrics():
    """Test COCOMO estimation with Halstead metrics."""
    estimator = COCOMO2Estimator()

    halstead = HalsteadMetrics(
        vocabulary=100,
        length=500,
        calculated_length=480.0,
        volume=3500.0,
        difficulty=30.0,  # High difficulty
        effort=105000.0,
        time_seconds=5833.3,
        bugs=1.17,
    )

    package = Package(
        name="test",
        sloc=SLOCMetrics(
            total=10000,
            code_lines=8000,
            comment_lines=1500,
            blank_lines=500,
            by_language={"python": 8000},
        ),
        halstead=halstead,
    )

    result = estimator.estimate(package, Region.US_SF)

    assert result.cost_usd > 0
    # High difficulty should increase multiplier
    assert result.halstead_multiplier > 1.0


def test_cocomo_with_all_metrics():
    """Test COCOMO estimation with all new metrics."""
    estimator = COCOMO2Estimator()

    git_history = GitHistoryMetrics(
        commit_count=20000,
        contributor_count=150,
        age_days=3650,  # 10 years
        age_years=10.0,
        first_commit_date=datetime.now() - timedelta(days=3650),
        last_commit_date=datetime.now(),
        release_count=50,
        commits_per_month=166.0,
        avg_files_per_commit=5.0,
        high_churn_files=100,
        bus_factor=5,
    )

    halstead = HalsteadMetrics(
        vocabulary=150,
        length=800,
        calculated_length=750.0,
        volume=6000.0,
        difficulty=40.0,
        effort=240000.0,
        time_seconds=13333.3,
        bugs=2.0,
    )

    package = Package(
        name="test",
        sloc=SLOCMetrics(
            total=50000,
            code_lines=40000,
            comment_lines=8000,
            blank_lines=2000,
            by_language={"python": 40000},
        ),
        complexity=ComplexityMetrics(
            cyclomatic_complexity_avg=15.0,
            complexity_level=ComplexityLevel.COMPLEX,
        ),
        git_history=git_history,
        halstead=halstead,
    )

    result_with_metrics = estimator.estimate(package, Region.US_SF)

    # Create same package without git history and halstead
    package_basic = Package(
        name="test",
        sloc=SLOCMetrics(
            total=50000,
            code_lines=40000,
            comment_lines=8000,
            blank_lines=2000,
            by_language={"python": 40000},
        ),
        complexity=ComplexityMetrics(
            cyclomatic_complexity_avg=15.0,
            complexity_level=ComplexityLevel.COMPLEX,
        ),
    )

    result_basic = estimator.estimate(package_basic, Region.US_SF)

    # Estimate with all metrics should be significantly higher
    assert result_with_metrics.cost_usd > result_basic.cost_usd
    assert result_with_metrics.maturity_multiplier > 1.5
    assert result_with_metrics.halstead_multiplier > 1.0
    # Total effort should reflect all multipliers
    assert result_with_metrics.effort_person_months > result_basic.effort_person_months


def test_cocomo_confidence_increases_with_metrics():
    """Test that confidence increases when more metrics are available."""
    estimator = COCOMO2Estimator()

    # Package with only SLOC
    package_minimal = Package(
        name="test",
        sloc=SLOCMetrics(
            total=10000,
            code_lines=8000,
            comment_lines=1500,
            blank_lines=500,
            by_language={"python": 8000},
        ),
    )

    # Package with all metrics
    package_complete = Package(
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
        halstead=HalsteadMetrics(
            vocabulary=50,
            length=150,
            calculated_length=140.0,
            volume=900.0,
            difficulty=15.0,
            effort=13500.0,
            time_seconds=750.0,
            bugs=0.3,
        ),
        git_history=GitHistoryMetrics(
            commit_count=1000,
            contributor_count=10,
            age_days=730,
            age_years=2.0,
            first_commit_date=datetime.now() - timedelta(days=730),
            last_commit_date=datetime.now(),
            release_count=10,
            commits_per_month=41.0,
            avg_files_per_commit=2.0,
            high_churn_files=10,
            bus_factor=2,
        ),
    )

    result_minimal = estimator.estimate(package_minimal, Region.US_SF)
    result_complete = estimator.estimate(package_complete, Region.US_SF)

    # Confidence should be higher with more data
    assert result_complete.confidence > result_minimal.confidence

