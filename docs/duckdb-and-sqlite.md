# DuckDB and SQLite

This document introduces **DuckDB** and **SQLite**, two file-based relational databases used in analytics.

Both use SQL.
They serve different purposes.

## DuckDB: Analytics-Oriented SQL Engine

DuckDB is:

- file-based
- designed for analytics
- optimized for columnar queries
- tightly integrated with dataframes and files

DuckDB is especially good for:

- analytics workloads
- querying CSV, Parquet, and DataFrames
- local data exploration
- teaching SQL for analytics

## Why We Use DuckDB

DuckDB:

- performs well on analytic queries
- works naturally with pandas
- supports modern SQL features
- avoids server setup

## SQLite vs DuckDB (Conceptual Comparison)

SQLite:

- application storage
- transactional workloads
- embedded everywhere

DuckDB:

- analytics and exploration
- columnar execution
- data science workflows

Both:

- use SQL
- store data locally
- are excellent learning tools

## How This Transfers to Hosted Databases

Skills learned with SQLite and DuckDB transfer directly to:

- PostgreSQL
- MySQL
- SQL Server
- cloud data warehouses

The SQL concepts are the same.
Only scale and deployment differ.



## SQLite: The Embedded Relational Database

SQLite is:

- file-based
- embedded
- extremely widely deployed

It is commonly used in:

- browsers
- mobile apps
- desktop software
- internal tools

SQLite emphasizes:

- simplicity
- reliability
- portability

For many applications, it replaces the need for a server database.


## Use Cases

- SQLite shows how pervasive relational data is
- DuckDB is ideal for analytics workflows
- File-based databases are realistic proxies
- SQL skills transfer across systems

Assist with:

- querying relational data
- combining SQL and Python
- producing analytic results from structured tables
