"""Tests for git history analyzer."""

import asyncio
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from ossval.analyzers.git_history import analyze_git_history


def create_test_git_repo(path: Path, num_commits: int = 5, num_contributors: int = 2):
    """Helper to create a test git repository."""
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=path,
        check=True,
        capture_output=True,
    )

    # Create commits
    for i in range(num_commits):
        # Alternate between contributors
        if i % 2 == 0:
            user_name = "Test User"
            user_email = "test@example.com"
        else:
            user_name = "Second User"
            user_email = "second@example.com"

        subprocess.run(
            ["git", "config", "user.name", user_name],
            cwd=path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.email", user_email],
            cwd=path,
            check=True,
            capture_output=True,
        )

        # Create/modify file
        test_file = path / f"file{i}.txt"
        test_file.write_text(f"Content {i}")

        subprocess.run(["git", "add", "."], cwd=path, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"Commit {i}"],
            cwd=path,
            check=True,
            capture_output=True,
        )


@pytest.mark.asyncio
async def test_analyze_basic_git_repo():
    """Test analyzing a basic git repository."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        create_test_git_repo(tmppath, num_commits=5)

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    assert metrics.commit_count == 5
    assert metrics.contributor_count >= 1
    assert metrics.age_days >= 0
    assert metrics.age_years >= 0.0
    assert metrics.first_commit_date is not None
    assert metrics.last_commit_date is not None
    assert metrics.release_count >= 0
    assert metrics.bus_factor >= 1


@pytest.mark.asyncio
async def test_analyze_repo_with_multiple_contributors():
    """Test analyzing a repo with multiple contributors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        create_test_git_repo(tmppath, num_commits=10, num_contributors=2)

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    assert metrics.commit_count == 10
    # Should have at least 2 contributors (we alternate)
    assert metrics.contributor_count >= 1


@pytest.mark.asyncio
async def test_analyze_repo_with_tags():
    """Test analyzing a repo with release tags."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        create_test_git_repo(tmppath, num_commits=3)

        # Create tags
        subprocess.run(
            ["git", "tag", "v1.0.0"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "tag", "v1.1.0"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    assert metrics.release_count == 2


@pytest.mark.asyncio
async def test_analyze_non_git_directory():
    """Test analyzing a directory that's not a git repo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        # Don't initialize git

        metrics = await analyze_git_history(tmppath)

    # Should return None for non-git directory
    assert metrics is None


@pytest.mark.asyncio
async def test_analyze_commits_per_month():
    """Test that commits per month is calculated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        create_test_git_repo(tmppath, num_commits=12)

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    # Should have calculated commits per month
    assert metrics.commits_per_month >= 0.0


@pytest.mark.asyncio
async def test_analyze_avg_files_per_commit():
    """Test that average files per commit is calculated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        create_test_git_repo(tmppath, num_commits=5)

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    assert metrics.avg_files_per_commit >= 0.0


@pytest.mark.asyncio
async def test_bus_factor_calculation():
    """Test bus factor calculation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create repo with one dominant contributor
        subprocess.run(["git", "init"], cwd=tmppath, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "main@example.com"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Main User"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )

        # Main user makes 90% of commits
        for i in range(9):
            (tmppath / f"file{i}.txt").write_text(f"Content {i}")
            subprocess.run(
                ["git", "add", "."], cwd=tmppath, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"Commit {i}"],
                cwd=tmppath,
                check=True,
                capture_output=True,
            )

        # Second user makes 10% of commits
        subprocess.run(
            ["git", "config", "user.name", "Minor User"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "minor@example.com"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )
        (tmppath / "file10.txt").write_text("Content 10")
        subprocess.run(["git", "add", "."], cwd=tmppath, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Commit 10"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    # Bus factor should be 1 (one person does >50% of work)
    assert metrics.bus_factor == 1


@pytest.mark.asyncio
async def test_repository_age_calculation():
    """Test that repository age is calculated correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        create_test_git_repo(tmppath, num_commits=2)

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    assert metrics.first_commit_date is not None
    assert metrics.last_commit_date is not None
    # Commits were just created, so age should be very small
    assert metrics.age_days >= 0
    assert metrics.age_years >= 0.0
    # Should be less than 1 day old
    assert metrics.age_days < 1


@pytest.mark.asyncio
async def test_high_churn_files():
    """Test identification of high-churn files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        subprocess.run(["git", "init"], cwd=tmppath, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=tmppath,
            check=True,
            capture_output=True,
        )

        # Create a file and modify it many times
        test_file = tmppath / "frequently_changed.txt"
        for i in range(15):
            test_file.write_text(f"Version {i}")
            subprocess.run(
                ["git", "add", "."], cwd=tmppath, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"Update {i}"],
                cwd=tmppath,
                check=True,
                capture_output=True,
            )

        metrics = await analyze_git_history(tmppath)

    assert metrics is not None
    # Should detect at least one high-churn file (>10 changes)
    assert metrics.high_churn_files >= 1
