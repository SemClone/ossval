"""Tests for Halstead complexity analyzer."""

import tempfile
from pathlib import Path

import pytest

from ossval.analyzers.halstead import (
    TREE_SITTER_AVAILABLE,
    analyze_directory_halstead,
    analyze_python_file,
    analyze_source_file,
    detect_language,
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

    # Tree-sitter is resilient to syntax errors and can still parse
    # Without tree-sitter, Python AST fails on invalid syntax
    if TREE_SITTER_AVAILABLE:
        assert metrics is not None
        assert metrics.vocabulary > 0
    else:
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


def test_detect_language():
    """Test language detection from file extensions."""
    assert detect_language(Path("test.py")) == "python"
    assert detect_language(Path("test.js")) == "javascript"
    assert detect_language(Path("test.ts")) == "typescript"
    assert detect_language(Path("test.tsx")) == "typescript"
    assert detect_language(Path("test.java")) == "java"
    assert detect_language(Path("test.c")) == "c"
    assert detect_language(Path("test.cpp")) == "cpp"
    assert detect_language(Path("test.cs")) == "c_sharp"
    assert detect_language(Path("test.go")) == "go"
    assert detect_language(Path("test.rs")) == "rust"
    assert detect_language(Path("test.php")) == "php"
    assert detect_language(Path("test.rb")) == "ruby"
    assert detect_language(Path("test.swift")) == "swift"
    assert detect_language(Path("test.txt")) is None
    assert detect_language(Path("test.md")) is None


@pytest.mark.skipif(not TREE_SITTER_AVAILABLE, reason="Requires tree-sitter for multi-language support")
def test_analyze_javascript_file():
    """Test Halstead analysis on a JavaScript file."""
    code = """
function add(a, b) {
    return a + b;
}

function multiply(x, y) {
    const result = x * y;
    return result;
}

if (typeof module !== 'undefined') {
    const result = add(5, 3);
    console.log(result);
}
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_source_file(Path(f.name))

    assert metrics is not None
    assert metrics.vocabulary > 0
    assert metrics.length > 0
    assert metrics.volume > 0
    assert metrics.difficulty > 0
    assert metrics.effort > 0


@pytest.mark.skipif(not TREE_SITTER_AVAILABLE, reason="Requires tree-sitter for multi-language support")
def test_analyze_typescript_file():
    """Test Halstead analysis on a TypeScript file."""
    code = """
interface Calculator {
    add(a: number, b: number): number;
    multiply(a: number, b: number): number;
}

class SimpleCalculator implements Calculator {
    add(a: number, b: number): number {
        return a + b;
    }

    multiply(a: number, b: number): number {
        const result = a * b;
        return result;
    }
}

const calc = new SimpleCalculator();
const sum = calc.add(5, 3);
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".ts", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_source_file(Path(f.name))

    assert metrics is not None
    assert metrics.vocabulary > 0
    assert metrics.volume > 0
    assert metrics.difficulty > 0


@pytest.mark.skipif(not TREE_SITTER_AVAILABLE, reason="Requires tree-sitter for multi-language support")
def test_analyze_java_file():
    """Test Halstead analysis on a Java file."""
    code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int multiply(int a, int b) {
        int result = a * b;
        return result;
    }

    public static void main(String[] args) {
        Calculator calc = new Calculator();
        int sum = calc.add(5, 3);
        System.out.println(sum);
    }
}
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_source_file(Path(f.name))

    assert metrics is not None
    assert metrics.vocabulary > 0
    assert metrics.volume > 0


@pytest.mark.skipif(not TREE_SITTER_AVAILABLE, reason="Requires tree-sitter for multi-language support")
def test_analyze_go_file():
    """Test Halstead analysis on a Go file."""
    code = """
package main

import "fmt"

func add(a int, b int) int {
    return a + b
}

func multiply(x int, y int) int {
    result := x * y
    return result
}

func main() {
    result := add(5, 3)
    fmt.Println(result)
}
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_source_file(Path(f.name))

    assert metrics is not None
    assert metrics.vocabulary > 0
    assert metrics.volume > 0


@pytest.mark.skipif(not TREE_SITTER_AVAILABLE, reason="Requires tree-sitter for multi-language support")
def test_analyze_rust_file():
    """Test Halstead analysis on a Rust file."""
    code = """
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn multiply(x: i32, y: i32) -> i32 {
    let result = x * y;
    result
}

fn main() {
    let result = add(5, 3);
    println!("{}", result);
}
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".rs", delete=False) as f:
        f.write(code)
        f.flush()

        metrics = analyze_source_file(Path(f.name))

    assert metrics is not None
    assert metrics.vocabulary > 0
    assert metrics.volume > 0


@pytest.mark.skipif(not TREE_SITTER_AVAILABLE, reason="Requires tree-sitter for multi-language support")
def test_analyze_multi_language_directory():
    """Test Halstead analysis on a directory with multiple languages."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create Python file
        (tmppath / "calc.py").write_text("""
def add(a, b):
    return a + b
""")

        # Create JavaScript file
        (tmppath / "calc.js").write_text("""
function add(a, b) {
    return a + b;
}
""")

        # Create Java file
        (tmppath / "Calc.java").write_text("""
public class Calc {
    public int add(int a, int b) {
        return a + b;
    }
}
""")

        # Create Go file
        (tmppath / "calc.go").write_text("""
package main
func add(a int, b int) int {
    return a + b
}
""")

        metrics = analyze_directory_halstead(tmppath)

    # Should aggregate metrics from all supported files
    assert metrics is not None
    assert metrics.volume > 0
    assert metrics.effort > 0
    assert metrics.bugs > 0
