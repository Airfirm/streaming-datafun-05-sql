"""femi_sqlite_library.py - Library checkout SQLite pipeline.

Author: Oluwafemi Salawu
Date: 2026-05

Purpose:
- Read library CSV files into a SQLite database.
- Use branch.csv and checkout.csv from data/library/.
- Create SQLite tables for library branches and material checkouts.
- Load CSV data using Python.
- Query the database to gain library business intelligence.

Data Source:
- data/library/branch.csv
- data/library/checkout.csv

Project Purpose:
- Analyze library checkout activity by branch and material type.
- Identify which branches have the most checkouts.
- Identify which material types are checked out most often.
- Summarize fine amounts and checkout durations.
- Store results in a local SQLite database for repeatable analysis.

Output:
- artifacts/sqlite/library.sqlite
"""

# === DECLARE IMPORTS ===

import csv
import logging
from pathlib import Path
import sqlite3
from typing import Final

from datafun_toolkit.logger import get_logger, log_header

# === CONFIGURE LOGGER ONCE PER MODULE ===

LOG: logging.Logger = get_logger("P05", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS ===

ROOT_DIR: Final[Path] = Path.cwd()

DATA_DIR: Final[Path] = ROOT_DIR / "data" / "library"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts" / "sqlite"
DB_PATH: Final[Path] = ARTIFACTS_DIR / "library.sqlite"

BRANCH_CSV: Final[Path] = DATA_DIR / "branch.csv"
CHECKOUT_CSV: Final[Path] = DATA_DIR / "checkout.csv"


# ============================================================
# DATABASE SETUP
# ============================================================


def create_tables(con: sqlite3.Connection) -> None:
    """Create the library database tables.

    Args:
        con: SQLite connection object.
    """
    LOG.info("Creating library database tables")

    con.executescript(
        """
        DROP TABLE IF EXISTS checkout;
        DROP TABLE IF EXISTS branch;

        CREATE TABLE branch (
            branch_id TEXT PRIMARY KEY,
            branch_name TEXT NOT NULL,
            city TEXT NOT NULL,
            system_name TEXT NOT NULL
        );

        CREATE TABLE checkout (
            checkout_id TEXT PRIMARY KEY,
            branch_id TEXT NOT NULL,
            material_type TEXT NOT NULL,
            duration_days INTEGER NOT NULL,
            fine_amount REAL NOT NULL,
            checkout_date TEXT NOT NULL,
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
        );
        """
    )

    LOG.info("Library database tables created")


# ============================================================
# LOAD CSV DATA INTO SQLITE TABLES
# ============================================================


def load_branch_csv(con: sqlite3.Connection, csv_path: Path) -> None:
    """Load branch.csv into the branch table.

    Args:
        con: SQLite connection object.
        csv_path: Path to branch.csv.
    """
    LOG.info("LOAD CSV -> table branch: %s", csv_path)

    with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        rows = []
        for row in reader:
            rows.append(
                (
                    row["branch_id"],
                    row["branch_name"],
                    row["city"],
                    row["system_name"],
                )
            )

    con.executemany(
        """
        INSERT INTO branch (branch_id, branch_name, city, system_name)
        VALUES (?, ?, ?, ?);
        """,
        rows,
    )

    LOG.info("DONE loading branch rows: %d", len(rows))


def load_checkout_csv(con: sqlite3.Connection, csv_path: Path) -> None:
    """Load checkout.csv into the checkout table.

    Args:
        con: SQLite connection object.
        csv_path: Path to checkout.csv.
    """
    LOG.info("LOAD CSV -> table checkout: %s", csv_path)

    with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        rows = []
        for row in reader:
            rows.append(
                (
                    row["checkout_id"],
                    row["branch_id"],
                    row["material_type"],
                    int(row["duration_days"]),
                    float(row["fine_amount"]),
                    row["checkout_date"],
                )
            )

    con.executemany(
        """
        INSERT INTO checkout (
            checkout_id,
            branch_id,
            material_type,
            duration_days,
            fine_amount,
            checkout_date
        )
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        rows,
    )

    LOG.info("DONE loading checkout rows: %d", len(rows))


# ============================================================
# QUERY HELPERS
# ============================================================


def run_query(
    con: sqlite3.Connection,
    title: str,
    sql_text: str,
) -> list[sqlite3.Row]:
    """Run a SQL query and log the results.

    Args:
        con: SQLite connection object.
        title: Query title to show in the logs.
        sql_text: SQL query text.

    Returns:
        list[sqlite3.Row]: Query result rows.
    """
    LOG.info("")
    LOG.info("====================================")
    LOG.info(title)
    LOG.info("====================================")

    result = con.execute(sql_text)
    rows = result.fetchall()

    columns = [col[0] for col in result.description]
    LOG.info(", ".join(columns))

    for row in rows:
        LOG.info(", ".join(str(value) for value in row))

    return rows


def run_basic_queries(con: sqlite3.Connection) -> None:
    """Run basic count and quality-check queries.

    Args:
        con: SQLite connection object.
    """
    run_query(
        con,
        "Branch count",
        """
        SELECT COUNT(*) AS branch_count
        FROM branch;
        """,
    )

    run_query(
        con,
        "Checkout count",
        """
        SELECT COUNT(*) AS checkout_count
        FROM checkout;
        """,
    )

    run_query(
        con,
        "Total fine amount",
        """
        SELECT ROUND(SUM(fine_amount), 2) AS total_fine_amount
        FROM checkout;
        """,
    )


def run_library_analytics_queries(con: sqlite3.Connection) -> None:
    """Run library business intelligence queries.

    Args:
        con: SQLite connection object.
    """
    run_query(
        con,
        "Checkouts by branch",
        """
        SELECT
            b.branch_id,
            b.branch_name,
            b.city,
            COUNT(c.checkout_id) AS checkout_count,
            ROUND(SUM(c.fine_amount), 2) AS total_fines
        FROM branch AS b
        LEFT JOIN checkout AS c
            ON b.branch_id = c.branch_id
        GROUP BY
            b.branch_id,
            b.branch_name,
            b.city
        ORDER BY checkout_count DESC;
        """,
    )

    run_query(
        con,
        "Checkouts by material type",
        """
        SELECT
            material_type,
            COUNT(*) AS checkout_count,
            ROUND(AVG(duration_days), 2) AS avg_duration_days,
            ROUND(SUM(fine_amount), 2) AS total_fines
        FROM checkout
        GROUP BY material_type
        ORDER BY checkout_count DESC;
        """,
    )

    run_query(
        con,
        "Average checkout duration by branch",
        """
        SELECT
            b.branch_name,
            ROUND(AVG(c.duration_days), 2) AS avg_duration_days
        FROM checkout AS c
        INNER JOIN branch AS b
            ON c.branch_id = b.branch_id
        GROUP BY b.branch_name
        ORDER BY avg_duration_days DESC;
        """,
    )

    run_query(
        con,
        "Highest fine checkouts",
        """
        SELECT
            c.checkout_id,
            b.branch_name,
            c.material_type,
            c.duration_days,
            c.fine_amount,
            c.checkout_date
        FROM checkout AS c
        INNER JOIN branch AS b
            ON c.branch_id = b.branch_id
        ORDER BY c.fine_amount DESC, c.duration_days DESC
        LIMIT 10;
        """,
    )

    run_query(
        con,
        "Library KPI summary",
        """
        SELECT
            COUNT(*) AS total_checkouts,
            COUNT(DISTINCT branch_id) AS active_branches,
            ROUND(SUM(fine_amount), 2) AS total_fines,
            ROUND(AVG(fine_amount), 2) AS avg_fine_amount,
            ROUND(AVG(duration_days), 2) AS avg_duration_days
        FROM checkout;
        """,
    )


# ============================================================
# VALIDATION HELPERS
# ============================================================


def verify_input_files() -> None:
    """Verify required CSV input files exist before running pipeline.

    Raises:
        FileNotFoundError: If an expected input file is missing.
    """
    expected_files = [BRANCH_CSV, CHECKOUT_CSV]

    for file_path in expected_files:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required input file: {file_path}")

    LOG.info("All required input files found")


def initialize_artifacts_folder() -> None:
    """Create the SQLite artifacts folder if needed."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG.info("Artifacts folder ready: %s", ARTIFACTS_DIR)


# ============================================================
# MAIN FUNCTION
# ============================================================


def main() -> None:
    """Run the complete library SQLite pipeline."""
    log_header(LOG, "P05 Library Pipeline Example (SQLite)")

    LOG.info("START main()")
    LOG.info("ROOT_DIR: %s", ROOT_DIR)
    LOG.info("DATA_DIR: %s", DATA_DIR)
    LOG.info("ARTIFACTS_DIR: %s", ARTIFACTS_DIR)
    LOG.info("DB_PATH: %s", DB_PATH)
    LOG.info("BRANCH_CSV: %s", BRANCH_CSV)
    LOG.info("CHECKOUT_CSV: %s", CHECKOUT_CSV)

    verify_input_files()
    initialize_artifacts_folder()

    con = sqlite3.connect(str(DB_PATH))

    try:
        con.execute("PRAGMA foreign_keys = ON;")

        create_tables(con)

        load_branch_csv(con, BRANCH_CSV)
        load_checkout_csv(con, CHECKOUT_CSV)

        con.commit()
        LOG.info("COMMIT: library data load complete")

        run_basic_queries(con)
        run_library_analytics_queries(con)

    finally:
        con.close()
        LOG.info("SQLite connection closed")

    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
