"""femi_duckdb_civic_event.py - Civic event DuckDB pipeline.

Author: Oluwafemi Salawu
Date: 2026-05

Purpose:
- Read civic event CSV files into a DuckDB database.
- Use civic_event.csv and attendance.csv from data/civic_event/.
- Create DuckDB tables for civic events and attendance records.
- Analyze civic event attendance, attendee types, contributions, and event activity.
- Log the pipeline process.

Data Source:
- data/civic_event/civic_event.csv
- data/civic_event/attendance.csv

Project Purpose:
- Analyze community and civic event participation.
- Identify which events had the most attendees.
- Compare attendee types such as Member and Guest.
- Summarize contribution amounts by event and attendee type.
- Store results in a local DuckDB database for repeatable analysis.

Output:
- artifacts/duckdb/civic_event.duckdb
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header
import duckdb

# === CONFIGURE LOGGER ONCE PER MODULE ===

LOG: logging.Logger = get_logger("P05", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS ===

ROOT_DIR: Final[Path] = Path.cwd()

DATA_DIR: Final[Path] = ROOT_DIR / "data" / "civic_event"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts" / "duckdb"
DB_PATH: Final[Path] = ARTIFACTS_DIR / "civic_event.duckdb"

CIVIC_EVENT_CSV: Final[Path] = DATA_DIR / "civic_event.csv"
ATTENDANCE_CSV: Final[Path] = DATA_DIR / "attendance.csv"


# ============================================================
# VALIDATION HELPERS
# ============================================================


def verify_input_files() -> None:
    """Verify required CSV input files exist before running the pipeline.

    Raises:
        FileNotFoundError: If an expected input file is missing.
    """
    expected_files = [CIVIC_EVENT_CSV, ATTENDANCE_CSV]

    for file_path in expected_files:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required input file: {file_path}")

    LOG.info("All required input files found")


def initialize_artifacts_folder() -> None:
    """Create the DuckDB artifacts folder if it does not already exist."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG.info("Artifacts folder ready: %s", ARTIFACTS_DIR)


# ============================================================
# DATABASE SETUP
# ============================================================


def create_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Create civic event database tables.

    Args:
        con: DuckDB connection object.
    """
    LOG.info("Creating civic event database tables")

    con.execute(
        """
        DROP TABLE IF EXISTS attendance;
        DROP TABLE IF EXISTS civic_event;

        CREATE TABLE civic_event (
            civic_event_id VARCHAR PRIMARY KEY,
            event_name VARCHAR NOT NULL,
            location VARCHAR NOT NULL,
            organizer VARCHAR NOT NULL
        );

        CREATE TABLE attendance (
            attendance_id VARCHAR PRIMARY KEY,
            civic_event_id VARCHAR NOT NULL,
            attendee_type VARCHAR NOT NULL,
            checked_in INTEGER NOT NULL,
            contribution REAL NOT NULL,
            attend_date DATE NOT NULL
        );
        """
    )

    LOG.info("Civic event database tables created")


def load_csv_data(con: duckdb.DuckDBPyConnection) -> None:
    """Load civic event CSV files into DuckDB tables.

    Args:
        con: DuckDB connection object.
    """
    LOG.info("Loading civic event CSV data")

    con.execute(
        f"""
        INSERT INTO civic_event
        SELECT *
        FROM read_csv_auto('{CIVIC_EVENT_CSV.as_posix()}', header=true);
        """
    )

    con.execute(
        f"""
        INSERT INTO attendance
        SELECT *
        FROM read_csv_auto('{ATTENDANCE_CSV.as_posix()}', header=true);
        """
    )

    LOG.info("CSV data loaded into DuckDB tables")


# ============================================================
# QUERY HELPERS
# ============================================================


def run_query(
    con: duckdb.DuckDBPyConnection,
    title: str,
    sql_text: str,
) -> None:
    """Run a SQL query and log the results.

    Args:
        con: DuckDB connection object.
        title: Query title to show in the logs.
        sql_text: SQL query text.
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


def run_basic_queries(con: duckdb.DuckDBPyConnection) -> None:
    """Run basic count and quality-check queries.

    Args:
        con: DuckDB connection object.
    """
    run_query(
        con,
        "Civic event count",
        """
        SELECT COUNT(*) AS civic_event_count
        FROM civic_event;
        """,
    )

    run_query(
        con,
        "Attendance record count",
        """
        SELECT COUNT(*) AS attendance_record_count
        FROM attendance;
        """,
    )

    run_query(
        con,
        "Total contribution amount",
        """
        SELECT ROUND(SUM(contribution), 2) AS total_contribution
        FROM attendance;
        """,
    )


def run_civic_event_analytics_queries(con: duckdb.DuckDBPyConnection) -> None:
    """Run civic event business intelligence queries.

    Args:
        con: DuckDB connection object.
    """
    run_query(
        con,
        "Attendance and contributions by event",
        """
        SELECT
            e.civic_event_id,
            e.event_name,
            e.location,
            e.organizer,
            COUNT(a.attendance_id) AS attendance_count,
            SUM(a.checked_in) AS checked_in_count,
            ROUND(SUM(a.contribution), 2) AS total_contribution,
            ROUND(AVG(a.contribution), 2) AS avg_contribution
        FROM civic_event AS e
        LEFT JOIN attendance AS a
            ON e.civic_event_id = a.civic_event_id
        GROUP BY
            e.civic_event_id,
            e.event_name,
            e.location,
            e.organizer
        ORDER BY total_contribution DESC;
        """,
    )

    run_query(
        con,
        "Attendance by attendee type",
        """
        SELECT
            attendee_type,
            COUNT(*) AS attendance_count,
            SUM(checked_in) AS checked_in_count,
            ROUND(SUM(contribution), 2) AS total_contribution,
            ROUND(AVG(contribution), 2) AS avg_contribution
        FROM attendance
        GROUP BY attendee_type
        ORDER BY attendance_count DESC;
        """,
    )

    run_query(
        con,
        "Events by location",
        """
        SELECT
            location,
            COUNT(*) AS event_count
        FROM civic_event
        GROUP BY location
        ORDER BY event_count DESC;
        """,
    )

    run_query(
        con,
        "Highest contribution attendance records",
        """
        SELECT
            a.attendance_id,
            e.event_name,
            e.location,
            a.attendee_type,
            a.checked_in,
            a.contribution,
            a.attend_date
        FROM attendance AS a
        INNER JOIN civic_event AS e
            ON a.civic_event_id = e.civic_event_id
        ORDER BY a.contribution DESC
        LIMIT 10;
        """,
    )

    run_query(
        con,
        "Civic event KPI summary",
        """
        SELECT
            COUNT(*) AS total_attendance_records,
            COUNT(DISTINCT civic_event_id) AS active_events,
            SUM(checked_in) AS total_checked_in,
            ROUND(SUM(contribution), 2) AS total_contribution,
            ROUND(AVG(contribution), 2) AS avg_contribution
        FROM attendance;
        """,
    )


# ============================================================
# MAIN FUNCTION
# ============================================================


def main() -> None:
    """Run the complete civic event DuckDB pipeline."""
    log_header(LOG, "P05 Civic Event Pipeline Example (DuckDB)")

    LOG.info("START main()")
    LOG.info("ROOT_DIR: %s", ROOT_DIR)
    LOG.info("DATA_DIR: %s", DATA_DIR)
    LOG.info("ARTIFACTS_DIR: %s", ARTIFACTS_DIR)
    LOG.info("DB_PATH: %s", DB_PATH)
    LOG.info("CIVIC_EVENT_CSV: %s", CIVIC_EVENT_CSV)
    LOG.info("ATTENDANCE_CSV: %s", ATTENDANCE_CSV)

    verify_input_files()
    initialize_artifacts_folder()

    con = duckdb.connect(str(DB_PATH))

    try:
        create_tables(con)
        load_csv_data(con)

        run_basic_queries(con)
        run_civic_event_analytics_queries(con)

    finally:
        con.close()
        LOG.info("DuckDB connection closed")

    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
