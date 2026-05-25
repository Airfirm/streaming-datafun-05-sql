# P05 Glossary: Relational Data, SQL, and Analytics

This glossary defines **core vocabulary** used in Project 05 and beyond.

You are not expected to memorize these terms.
You _are_ expected to recognize them, use them correctly, and know when to ask good questions about them.

These terms may be frequently used in professional work.

## Relational Data

**Relational data** - Data organized into tables (rows and columns) with defined relationships between tables.

## Table Structure

**Table** - A structured collection of related records.

**Row (Record)** - One observation, entity, or event in a table.

**Column (Field)** - One attribute or variable describing the records in a table.

## Keys and Relationships

**Primary Key** - A column (or set of columns) that uniquely identifies each row in a table.

**Foreign Key** - A column that references the primary key of another table to create a relationship.

**Relationship** - A logical connection between tables, typically established using keys.

## SQL (Structured Query Language)

**SQL** - A declarative language used to query and manipulate relational data.

**Declarative Language** - A language where you describe _what_ result you want, not _how_ to compute it.

## Core SQL Concepts

| Clause      | Purpose                                      |
|-------------|----------------------------------------------|
| **SELECT**  | Chooses which columns to return.             |
| **FROM**    | Specifies the table(s) being queried.        |
| **WHERE**   | Filters rows based on conditions.            |
| **GROUP BY**| Groups rows so aggregate functions can be applied. |
| **ORDER BY**| Sorts query results.                         |
| **LIMIT**   | Restricts the number of rows returned.       |


## Aggregation

**Aggregate Function** - A function that summarizes multiple rows into a single value
(e.g., `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).

**Aggregation** - The process of summarizing data across rows.

## Joins

**JOIN** - Combines rows from two or more tables based on a related column.

**INNER JOIN** - Returns rows that match in both tables.

**LEFT JOIN** - Returns all rows from the left table and matching rows from the right table.

## Parameterized Queries

**Parameterized Query** - A SQL query that uses placeholders for values supplied at execution time.

**Placeholder** - A marker (such as `?`) in SQL that will be replaced with a bound value.

**Bound Parameter** - A value passed separately to the database engine to fill a placeholder.

**SQL Injection** - A security risk caused by inserting untrusted values directly into SQL text
(prevented by parameterized queries).

## Databases and Engines

**Database**
An organized collection of structured data managed by a database engine.

**Database Engine**
Software that stores, retrieves, and manages data (e.g., SQLite, DuckDB).

## File-Based Databases

**File-Based Database**
A database stored in a single file on disk rather than running as a server.

**SQLite**
A lightweight, embedded, file-based relational database used widely in applications.

**DuckDB**
A file-based, analytics-oriented SQL engine designed for data analysis workflows.

## Python and SQL Together

**Orchestration**
Using Python to control execution flow, manage inputs, and run SQL.

**DataFrame**
A tabular data structure (commonly from pandas) used for analysis in Python.

**Bridge (Python–SQL)**
The connection layer where Python executes SQL and retrieves results.

## Analytics Workflow Concepts

**Exploratory Data Analysis (EDA)**
Initial investigation of data to understand structure, quality, and patterns.

**Pipeline**
A sequence of steps that move data from input to output.

**Reusable Query**
A SQL query designed to be run multiple times with different parameters.

## Governance and Responsibility

**Data Provenance**
Information about where data comes from and how it was obtained.

**Data Governance**
Rules and practices for responsible data use, access, and management.

**Read-Only Access**
Opening data for inspection without modifying it.
