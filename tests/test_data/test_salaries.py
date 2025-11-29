"""Tests for salary data."""

from ossval.data.salaries import get_monthly_rate, get_regional_salary
from ossval.models import Region


def test_get_regional_salary():
    """Test getting regional salary data."""
    salary_data = get_regional_salary(Region.US_SF)
    assert "base_salary" in salary_data
    assert "overhead_multiplier" in salary_data
    assert salary_data["base_salary"] > 0


def test_get_monthly_rate():
    """Test calculating monthly rate."""
    rate = get_monthly_rate(Region.US_SF)
    assert rate > 0
    # Should be roughly (220000 / 12) * 2.3 ≈ 42,000
    assert 40000 < rate < 50000

