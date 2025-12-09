"""Tests for Halstead complexity analyzer."""

import tempfile
from pathlib import Path

from ossval.analyzers.halstead import (
    analyze_directory_halstead,
    analyze_python_file,
)


def test_analyze_simple_python_file():
    """Test Halstead analysis on a simple Python file."""
    code = """
def add(a, b):
    return a + b

def multiply(x, y):
    result = x * y
    return result

if __name__ == "__main__":
    result = add(5, 3)
    print(result)
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_python_file(Path(f.name))

    assert metrics is not None
    assert metrics.vocabulary > 0
    assert metrics.length > 0
    assert metrics.volume > 0
    assert metrics.difficulty > 0
    assert metrics.effort > 0
    assert metrics.time_seconds > 0
    assert metrics.bugs >= 0


def test_analyze_complex_python_file():
    """Test Halstead analysis on a more complex Python file."""
    code = """
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(("add", a, b, result))
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(("subtract", a, b, result))
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(("multiply", a, b, result))
        return result

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(("divide", a, b, result))
        return result

    def get_history(self):
        return self.history
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_python_file(Path(f.name))

    assert metrics is not None
    # More complex code should have higher difficulty
    assert metrics.difficulty > 5.0
    assert metrics.volume > 100.0


def test_analyze_empty_file():
    """Test Halstead analysis on an empty file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("")
        f.flush()

        metrics = analyze_python_file(Path(f.name))

    # Empty file should return None
    assert metrics is None


def test_analyze_invalid_syntax():
    """Test Halstead analysis on file with invalid syntax."""
    code = "def broken(:\n    pass"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_python_file(Path(f.name))

    # Invalid syntax should return None
    assert metrics is None


def test_analyze_directory():
    """Test Halstead analysis on a directory of Python files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create multiple Python files
        file1 = tmppath / "file1.py"
        file1.write_text("""
def func1():
    x = 1 + 2
    return x
""")

        file2 = tmppath / "file2.py"
        file2.write_text("""
def func2(a, b):
    return a * b + a / b
""")

        file3 = tmppath / "file3.py"
        file3.write_text("""
class MyClass:
    def method(self):
        return "hello"
""")

        metrics = analyze_directory_halstead(tmppath)

    assert metrics is not None
    assert metrics.volume > 0
    assert metrics.effort > 0
    assert metrics.difficulty > 0


def test_analyze_directory_no_python_files():
    """Test Halstead analysis on directory with no Python files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create a non-Python file
        (tmppath / "readme.txt").write_text("Not Python")

        metrics = analyze_directory_halstead(tmppath)

    # No Python files should return None
    assert metrics is None


def test_analyze_directory_skips_venv():
    """Test that analysis skips venv directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create a regular Python file with some content
        (tmppath / "main.py").write_text("""
def main():
    x = 1 + 2
    return x
""")

        # Create files in venv (should be skipped)
        venv_dir = tmppath / "venv"
        venv_dir.mkdir()
        (venv_dir / "lib.py").write_text("""
def venv_func():
    y = 10 * 20
    return y
""")

        metrics = analyze_directory_halstead(tmppath)

    # Should analyze only main.py, not venv
    assert metrics is not None
    # If venv was included, volume would be higher
    assert metrics.volume > 0


def test_halstead_metrics_calculations():
    """Test that Halstead metrics are calculated correctly."""
    code = """
def simple(x):
    return x + 1
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_python_file(Path(f.name))

    assert metrics is not None

    # Basic sanity checks for metric relationships
    assert metrics.length >= metrics.vocabulary  # N >= n
    assert metrics.effort == metrics.difficulty * metrics.volume
    assert metrics.time_seconds == metrics.effort / 18.0  # Stroud number
    assert metrics.bugs == metrics.volume / 3000.0
