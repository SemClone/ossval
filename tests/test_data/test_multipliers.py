"""Tests for multiplier data."""

from datetime import datetime, timedelta

from ossval.data.multipliers import (
    get_complexity_multiplier,
    get_halstead_multiplier,
    get_maturity_multiplier,
    get_project_type_multiplier,
)
from ossval.models import ComplexityLevel, GitHistoryMetrics, HalsteadMetrics, ProjectType


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


def test_get_maturity_multiplier_none():
    """Test maturity multiplier with no git history."""
    multiplier = get_maturity_multiplier(None)
    assert multiplier == 1.0


def test_get_maturity_multiplier_young_project():
    """Test maturity multiplier for young project."""
    git_history = GitHistoryMetrics(
        commit_count=100,
        contributor_count=3,
        age_days=180,  # 6 months
        age_years=0.5,
        first_commit_date=datetime.now() - timedelta(days=180),
        last_commit_date=datetime.now(),
        release_count=2,
        commits_per_month=20.0,
        avg_files_per_commit=2.5,
        high_churn_files=5,
        bus_factor=2,
    )

    multiplier = get_maturity_multiplier(git_history)

    # Young project should have multiplier close to 1.0
    assert 1.0 <= multiplier <= 1.3


def test_get_maturity_multiplier_mature_project():
    """Test maturity multiplier for mature project."""
    git_history = GitHistoryMetrics(
        commit_count=25000,  # Many commits
        contributor_count=150,  # Many contributors
        age_days=3650,  # 10 years
        age_years=10.0,
        first_commit_date=datetime.now() - timedelta(days=3650),
        last_commit_date=datetime.now(),
        release_count=50,
        commits_per_month=208.0,
        avg_files_per_commit=5.0,
        high_churn_files=100,
        bus_factor=5,
    )

    multiplier = get_maturity_multiplier(git_history)

    # Mature, large project should have high multiplier
    assert multiplier >= 2.0
    # But capped at 2.5
    assert multiplier <= 2.5


def test_get_maturity_multiplier_medium_project():
    """Test maturity multiplier for medium-sized project."""
    git_history = GitHistoryMetrics(
        commit_count=2000,
        contributor_count=15,
        age_days=1095,  # 3 years
        age_years=3.0,
        first_commit_date=datetime.now() - timedelta(days=1095),
        last_commit_date=datetime.now(),
        release_count=10,
        commits_per_month=55.0,
        avg_files_per_commit=3.0,
        high_churn_files=20,
        bus_factor=3,
    )

    multiplier = get_maturity_multiplier(git_history)

    # Medium project should have multiplier between 1.2 and 1.8
    assert 1.2 <= multiplier <= 1.8


def test_get_halstead_multiplier_none():
    """Test Halstead multiplier with no metrics."""
    multiplier = get_halstead_multiplier(None)
    assert multiplier == 1.0


def test_get_halstead_multiplier_low_difficulty():
    """Test Halstead multiplier for low difficulty code."""
    halstead = HalsteadMetrics(
        vocabulary=20,
        length=50,
        calculated_length=45.0,
        volume=250.0,
        difficulty=5.0,  # Low difficulty
        effort=1250.0,
        time_seconds=69.4,
        bugs=0.08,
    )

    multiplier = get_halstead_multiplier(halstead)

    # Low difficulty should give multiplier < 1.0
    assert 0.8 <= multiplier < 1.0


def test_get_halstead_multiplier_medium_difficulty():
    """Test Halstead multiplier for medium difficulty code."""
    halstead = HalsteadMetrics(
        vocabulary=50,
        length=150,
        calculated_length=140.0,
        volume=900.0,
        difficulty=15.0,  # Medium difficulty
        effort=13500.0,
        time_seconds=750.0,
        bugs=0.3,
    )

    multiplier = get_halstead_multiplier(halstead)

    # Medium difficulty should give multiplier around 1.0
    assert 0.95 <= multiplier <= 1.05


def test_get_halstead_multiplier_high_difficulty():
    """Test Halstead multiplier for high difficulty code."""
    halstead = HalsteadMetrics(
        vocabulary=100,
        length=500,
        calculated_length=480.0,
        volume=3500.0,
        difficulty=50.0,  # High difficulty
        effort=175000.0,
        time_seconds=9722.2,
        bugs=1.17,
    )

    multiplier = get_halstead_multiplier(halstead)

    # High difficulty should give multiplier > 1.5
    assert multiplier >= 1.5
    # Capped at 1.8
    assert multiplier <= 1.8


def test_get_halstead_multiplier_very_high_difficulty():
    """Test Halstead multiplier for very high difficulty code."""
    halstead = HalsteadMetrics(
        vocabulary=200,
        length=1000,
        calculated_length=950.0,
        volume=10000.0,
        difficulty=100.0,  # Very high difficulty
        effort=1000000.0,
        time_seconds=55555.5,
        bugs=3.33,
    )

    multiplier = get_halstead_multiplier(halstead)

    # Very high difficulty should be capped at 1.8
    assert multiplier == 1.8


def test_maturity_multiplier_age_component():
    """Test that age affects maturity multiplier."""
    # Create identical git histories except for age
    young_git = GitHistoryMetrics(
        commit_count=1000,
        contributor_count=10,
        age_days=365,  # 1 year
        age_years=1.0,
        first_commit_date=datetime.now() - timedelta(days=365),
        last_commit_date=datetime.now(),
        release_count=5,
        commits_per_month=83.0,
        avg_files_per_commit=2.0,
        high_churn_files=10,
        bus_factor=2,
    )

    old_git = GitHistoryMetrics(
        commit_count=1000,
        contributor_count=10,
        age_days=3650,  # 10 years
        age_years=10.0,
        first_commit_date=datetime.now() - timedelta(days=3650),
        last_commit_date=datetime.now(),
        release_count=5,
        commits_per_month=8.3,
        avg_files_per_commit=2.0,
        high_churn_files=10,
        bus_factor=2,
    )

    young_mult = get_maturity_multiplier(young_git)
    old_mult = get_maturity_multiplier(old_git)

    # Older project should have higher multiplier
    assert old_mult > young_mult


def test_maturity_multiplier_contributor_component():
    """Test that contributor count affects maturity multiplier."""
    few_contributors = GitHistoryMetrics(
        commit_count=1000,
        contributor_count=3,  # Few contributors
        age_days=1095,
        age_years=3.0,
        first_commit_date=datetime.now() - timedelta(days=1095),
        last_commit_date=datetime.now(),
        release_count=5,
        commits_per_month=30.0,
        avg_files_per_commit=2.0,
        high_churn_files=10,
        bus_factor=1,
    )

    many_contributors = GitHistoryMetrics(
        commit_count=1000,
        contributor_count=200,  # Many contributors
        age_days=1095,
        age_years=3.0,
        first_commit_date=datetime.now() - timedelta(days=1095),
        last_commit_date=datetime.now(),
        release_count=5,
        commits_per_month=30.0,
        avg_files_per_commit=2.0,
        high_churn_files=10,
        bus_factor=10,
    )

    few_mult = get_maturity_multiplier(few_contributors)
    many_mult = get_maturity_multiplier(many_contributors)

    # More contributors should mean higher complexity/multiplier
    assert many_mult > few_mult

