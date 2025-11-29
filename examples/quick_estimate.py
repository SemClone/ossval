"""Example: Quick cost estimate."""

from ossval import quick_estimate
from ossval.models import Region, ProjectType


def main():
    """Quick estimate example."""
    # Estimate cost for a compiler project
    result = quick_estimate(
        sloc=50000,
        region=Region.US_SF,
        project_type=ProjectType.COMPILER,
    )
    
    print("Quick Cost Estimate")
    print("=" * 50)
    print(f"SLOC: 50,000")
    print(f"Region: US San Francisco")
    print(f"Project Type: Compiler")
    print()
    print(f"Estimated Cost: ${result['cost_usd']:,.0f}")
    print(f"  Range: ${result['cost_usd_low']:,.0f} - ${result['cost_usd_high']:,.0f}")
    print(f"Effort: {result['effort_person_years']:.1f} person-years")
    print(f"Methodology: {result['methodology']}")


if __name__ == "__main__":
    main()

