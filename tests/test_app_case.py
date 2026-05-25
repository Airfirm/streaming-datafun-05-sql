# tests/test_app_case.py
#
# Simple, clear pytest examples.
# Show how to test file-writing functions without touching
# the real project folder, and how to avoid slow sleeps.
#
# Assumptions:
# - module is importable
# - pytest running from project root
#
# Run:
#   uv run pytest

from datafun_05_sql import case_duckdb_retail, case_sqlite_retail


def test_case_duckdb_retail_exists() -> None:
    """Test that the duckdb retail case module exists."""
    assert case_duckdb_retail is not None


def test_case_sqlite_retail_exists() -> None:
    """Test that the sqlite retail case module exists."""
    assert case_sqlite_retail is not None
