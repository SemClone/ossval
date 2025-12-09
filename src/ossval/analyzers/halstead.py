"""Halstead complexity metrics analyzer."""

import ast
from pathlib import Path
from typing import Dict, Optional, Set

from ossval.models import HalsteadMetrics


class HalsteadAnalyzer(ast.NodeVisitor):
    """AST visitor to compute Halstead metrics for Python code."""

    def __init__(self):
        """Initialize the analyzer."""
        self.operators: Set[str] = set()
        self.operands: Set[str] = set()
        self.operator_count = 0
        self.operand_count = 0

    def visit_BinOp(self, node):
        """Visit binary operators (+, -, *, /, etc.)."""
        self.operators.add(node.op.__class__.__name__)
        self.operator_count += 1
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        """Visit unary operators (not, -, +, ~)."""
        self.operators.add(node.op.__class__.__name__)
        self.operator_count += 1
        self.generic_visit(node)

    def visit_Compare(self, node):
        """Visit comparison operators (==, !=, <, >, etc.)."""
        for op in node.ops:
            self.operators.add(op.__class__.__name__)
            self.operator_count += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """Visit boolean operators (and, or)."""
        self.operators.add(node.op.__class__.__name__)
        self.operator_count += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        """Visit function calls."""
        self.operators.add("Call")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Visit assignments."""
        self.operators.add("Assign")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        """Visit augmented assignments (+=, -=, etc.)."""
        self.operators.add(f"AugAssign_{node.op.__class__.__name__}")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_If(self, node):
        """Visit if statements."""
        self.operators.add("If")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_For(self, node):
        """Visit for loops."""
        self.operators.add("For")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """Visit while loops."""
        self.operators.add("While")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_Return(self, node):
        """Visit return statements."""
        self.operators.add("Return")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """Visit function definitions."""
        self.operators.add("FunctionDef")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visit class definitions."""
        self.operators.add("ClassDef")
        self.operator_count += 1
        self.generic_visit(node)

    def visit_Name(self, node):
        """Visit variable names."""
        self.operands.add(node.id)
        self.operand_count += 1
        self.generic_visit(node)

    def visit_Constant(self, node):
        """Visit constants (numbers, strings, etc.)."""
        self.operands.add(str(node.value))
        self.operand_count += 1
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Visit attribute access."""
        self.operands.add(node.attr)
        self.operand_count += 1
        self.generic_visit(node)


def analyze_python_file(file_path: Path) -> Optional[HalsteadMetrics]:
    """
    Analyze a single Python file for Halstead metrics.

    Args:
        file_path: Path to Python file

    Returns:
        HalsteadMetrics if successful, None otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        analyzer = HalsteadAnalyzer()
        analyzer.visit(tree)

        # Halstead metrics formulas
        n1 = len(analyzer.operators)  # Unique operators
        n2 = len(analyzer.operands)  # Unique operands
        N1 = analyzer.operator_count  # Total operators
        N2 = analyzer.operand_count  # Total operands

        if n1 == 0 or n2 == 0:
            return None

        vocabulary = n1 + n2
        length = N1 + N2
        calculated_length = n1 * (n1 / 2 if n1 > 0 else 0) + n2 * (n2 / 2 if n2 > 0 else 0)
        volume = length * (vocabulary.bit_length() if vocabulary > 0 else 0)
        difficulty = (n1 / 2.0) * (N2 / n2 if n2 > 0 else 0)
        effort = difficulty * volume
        time_seconds = effort / 18.0  # Stroud number
        bugs = volume / 3000.0  # Expected bugs

        return HalsteadMetrics(
            vocabulary=vocabulary,
            length=length,
            calculated_length=calculated_length,
            volume=volume,
            difficulty=difficulty,
            effort=effort,
            time_seconds=time_seconds,
            bugs=bugs,
        )

    except Exception:
        return None


def analyze_directory_halstead(repo_path: Path) -> Optional[HalsteadMetrics]:
    """
    Analyze all Python files in a directory for aggregate Halstead metrics.

    Args:
        repo_path: Path to repository

    Returns:
        Aggregated HalsteadMetrics if successful, None otherwise
    """
    total_volume = 0.0
    total_difficulty = 0.0
    total_effort = 0.0
    total_time = 0.0
    total_bugs = 0.0
    file_count = 0

    for py_file in repo_path.rglob("*.py"):
        if "venv" in str(py_file) or "node_modules" in str(py_file):
            continue

        metrics = analyze_python_file(py_file)
        if metrics:
            total_volume += metrics.volume
            total_difficulty += metrics.difficulty
            total_effort += metrics.effort
            total_time += metrics.time_seconds
            total_bugs += metrics.bugs
            file_count += 1

    if file_count == 0:
        return None

    avg_difficulty = total_difficulty / file_count

    return HalsteadMetrics(
        vocabulary=0,  # Not meaningful at aggregate level
        length=0,  # Not meaningful at aggregate level
        calculated_length=0,  # Not meaningful at aggregate level
        volume=total_volume,
        difficulty=avg_difficulty,
        effort=total_effort,
        time_seconds=total_time,
        bugs=total_bugs,
    )
