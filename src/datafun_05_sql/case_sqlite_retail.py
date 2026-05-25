"""case_sqlite_retail.py - Project script (example).

Author: Denise Case
Date: 2026-02

Purpose:
- Read csv files into a SQLite database.
- SQLite does NOT have a built-in COPY-from-CSV like DuckDB.
  We create tables using SQL, then load CSV data using Python.
- Use Python to automate SQL scripts (stored in files).
- Log the pipeline process.

Paths (relative to repo root):
   SQL:  sql/sqlite/*.sql
   CSV:  data/retail/store.csv
   CSV:  data/retail/sale.csv
   DB:   artifacts/sqlite/retail.sqlite

OBS:
  Don't edit this file - it should remain a working example.
"""

# === DECLARE IMPORTS ===

import csv
import logging
from pathlib import Path
import sqlite3
from typing import Final

# External (must be listed in pyproject.toml)
from datafun_toolkit.logger import get_logger, log_header

# === CONFIGURE LOGGER ONCE PER MODULE (FILE) ===

LOG: logging.Logger = get_logger("P05", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS ===

ROOT_DIR: Final[Path] = Path.cwd()

DATA_DIR: Final[Path] = ROOT_DIR / "data" / "retail"
SQL_DIR: Final[Path] = ROOT_DIR / "sql" / "sqlite"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts" / "sqlite"
DB_PATH: Final[Path] = ARTIFACTS_DIR / "retail.sqlite"

STORE_CSV: Final[Path] = DATA_DIR / "store.csv"
SALE_CSV: Final[Path] = DATA_DIR / "sale.csv"

# === DECLARE HELPER FUNCTION:  READ SQL FROM PATH ===


def read_sql(sql_path: Path) -> str:
    """Read a SQL file from disk.

    Every pathlib Path object has a built-in read_text() method.
    We tell it to use UTF-8 encoding so that it works on all platforms.

    Args:
        sql_path (Path): Path to the SQL file.

    Returns:
        str: The contents of the SQL file as a string.
    """
    return sql_path.read_text(encoding="utf-8")


# === DECLARE HELPER FUNCTION:  RUN SQL ACTION (NO RESULTS) ===


def run_sql_script(con: sqlite3.Connection, sql_path: Path) -> None:
    """Execute a SQL action script file (DDL or cleanup).

    SQLite uses executescript() call.

    Args:
        con (sqlite3.Connection): SQLite connection object.
        sql_path (Path): Path to the SQL file to be executed.

    Returns:
        None
    """
    LOG.info(f"RUN SQL script: {sql_path}")
    sql_text = read_sql(sql_path)
    con.executescript(sql_text)
    LOG.info(f"DONE SQL script: {sql_path}")


# === DECLARE HELPER FUNCTION:  RUN SQL QUERY (LOG RESULTS) ===


def run_sql_query(con: sqlite3.Connection, sql_path: Path) -> None:
    """Execute a SQL query script file (SELECT or other queries that return results).

    Args:
        con (sqlite3.Connection): SQLite connection object.
        sql_path (Path): Path to the SQL file to be executed.

    Returns:
        str: The query results as a formatted string.
    """
    LOG.info("")
    LOG.info(f"RUN SQL query: {sql_path}")
    sql_text = read_sql(sql_path)

    result = con.execute(sql_text)
    rows = result.fetchall()
    columns = [col[0] for col in result.description]

    LOG.info("====================================")
    LOG.info(sql_path.name)
    LOG.info("====================================")
    LOG.info(", ".join(columns))

    for row in rows:
        LOG.info(", ".join(str(value) for value in row))


# ============================================================
# HELPER: LOAD CSV DATA INTO SQLITE TABLES
# ============================================================


def load_store_csv(con: sqlite3.Connection, csv_path: Path) -> None:
    """Load store.csv into the store table."""
    LOG.info("LOAD CSV -> table store: %s", csv_path)

    with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        rows = []
        for r in reader:
            rows.append((r["store_id"], r["store_name"], r["city"], r["region"]))

    con.executemany(
        """
        INSERT INTO store (store_id, store_name, city, region)
        VALUES (?, ?, ?, ?);
        """,
        rows,
    )

    LOG.info("DONE loading store rows: %d", len(rows))


def load_sale_csv(con: sqlite3.Connection, csv_path: Path) -> None:
    """Load sale.csv into the sale table."""
    LOG.info("LOAD CSV -> table sale: %s", csv_path)

    with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        rows = []
        for r in reader:
            rows.append(
                (
                    r["sale_id"],
                    r["store_id"],
                    r["product_category"],
                    int(r["quantity"]),
                    float(r["amount"]),
                    r["sale_date"],
                )
            )

    con.executemany(
        """
        INSERT INTO sale (sale_id, store_id, product_category, quantity, amount, sale_date)
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        rows,
    )

    LOG.info("DONE loading sale rows: %d", len(rows))


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the pipeline."""
    log_header(LOG, "P05 Pipeline Example (SQLite)")

    LOG.info("START main()")
    LOG.info(f"ROOT_DIR: {ROOT_DIR}")
    LOG.info(f"DATA_DIR: {DATA_DIR}")
    LOG.info(f"SQL_DIR: {SQL_DIR}")
    LOG.info(f"DB_PATH: {DB_PATH}")

    # Make sure the artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # Open a SQLite connection
    con = sqlite3.connect(str(DB_PATH))

    try:
        # ----------------------------------------------------
        # STEP 0: Set up SQLite Settings/PRAGMAs (pragmas stands for "practical regulations")
        # ----------------------------------------------------
        # Enforce foreign keys in SQLite (off by default).
        con.execute("PRAGMA foreign_keys = ON;")

        # ----------------------------------------------------
        # STEP 1: CLEAN (optional, common practice during development)
        # ----------------------------------------------------
        run_sql_script(con, SQL_DIR / "case_retail_clean.sql")

        # ----------------------------------------------------
        # STEP 2: BOOTSTRAP (create tables, load CSV data)
        # ----------------------------------------------------
        run_sql_script(con, SQL_DIR / "case_retail_bootstrap.sql")
        load_store_csv(con, STORE_CSV)
        load_sale_csv(con, SALE_CSV)
        con.commit()
        LOG.info("COMMIT: data load complete")

        # ----------------------------------------------------
        # STEP 3: RUN BASIC QUERIES
        # ----------------------------------------------------
        run_sql_query(con, SQL_DIR / "case_retail_query_store_count.sql")
        run_sql_query(con, SQL_DIR / "case_retail_query_sales_count.sql")
        run_sql_query(con, SQL_DIR / "case_retail_query_sales_aggregate.sql")
        run_sql_query(con, SQL_DIR / "case_retail_query_sales_by_category.sql")

        # ----------------------------------------------------
        # STEP 4: RUN KPI QUERY (ACTION-DRIVEN)
        # ----------------------------------------------------
        run_sql_query(con, SQL_DIR / "case_retail_query_kpi_revenue.sql")

    finally:
        # Regardless of success or failure, always close the connection
        con.close()

    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
