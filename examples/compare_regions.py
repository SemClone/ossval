"""Example: Compare costs across different regions."""

from ossval import quick_estimate
from ossval.models import Region, ProjectType


def main():
    """Compare cost estimates across regions."""
    sloc = 100000
    project_type = ProjectType.FRAMEWORK
    
    regions = [
        Region.US_SF,
        Region.US_NYC,
        Region.UK,
        Region.GERMANY,
        Region.INDIA,
        Region.GLOBAL_AVERAGE,
    ]
    
    print(f"Cost Comparison for {sloc:,} SLOC ({project_type.value})")
    print("=" * 60)
    
    for region in regions:
        result = quick_estimate(sloc, region, project_type)
        print(f"{region.value:20} ${result['cost_usd']:>15,.0f}")


if __name__ == "__main__":
    main()

