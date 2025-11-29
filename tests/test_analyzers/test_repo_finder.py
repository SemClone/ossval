"""Tests for repository finder."""

import pytest

from ossval.analyzers.repo_finder import _normalize_git_url


def test_normalize_git_url():
    """Test git URL normalization."""
    assert _normalize_git_url("git+https://github.com/user/repo") == "https://github.com/user/repo.git"
    assert _normalize_git_url("git@github.com:user/repo") == "https://github.com/user/repo.git"
    assert _normalize_git_url("https://github.com/user/repo.git") == "https://github.com/user/repo.git"

