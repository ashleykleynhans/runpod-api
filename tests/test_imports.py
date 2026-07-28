"""Tests that all Python scripts in the project parse successfully."""
import ast
import os
import pytest


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _collect_python_files():
    """Yield paths to all .py files outside .venv and __pycache__."""
    skip_dirs = {'.venv', '.git', '__pycache__', '.idea', '.claude', '.github', 'rpapi'}
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(root, f)


@pytest.mark.parametrize("filepath", list(_collect_python_files()))
def test_file_parses(filepath):
    """Verify that every .py file parses without SyntaxError."""
    with open(filepath) as fh:
        source = fh.read()
    ast.parse(source, filename=filepath)
