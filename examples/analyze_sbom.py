"""Example: Analyze an SBOM file."""

import asyncio

from ossval import analyze
from ossval.models import AnalysisConfig, Region


async def main():
    """Example analysis of an SBOM file."""
    # Configure analysis
    config = AnalysisConfig(
        region=Region.US_SF,
        clone_repos=True,
        use_cache=True,
        concurrency=4,
    )

    # Analyze SBOM
    result = await analyze("path/to/sbom.json", config)

    # Print summary
    print(f"Total OSS Value: ${result.summary['total_cost_usd']:,.0f}")
    print(f"Packages Analyzed: {result.summary['analyzed_packages']}")

    # Export results
    result.to_json("results.json")
    result.to_csv("results/")


if __name__ == "__main__":
    asyncio.run(main())

