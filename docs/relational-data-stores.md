# Relational Data Stores (P05)

This document introduces **relational data stores** and explains why they matter for data analytics.

Relational databases are one of the most important technologies in data work.
They appear in enterprise systems, analytics pipelines, and everyday software.

---

## What Is a Relational Data Store?

A relational data store:
- organizes data into **tables**
- each table has **rows** (records) and **columns** (fields)
- uses **keys** to relate tables to one another

Relationships allow data to be:
- structured
- queried efficiently
- joined across tables

---

## Tables, Rows, and Columns

Key vocabulary:

- **Table**: a collection of related records
- **Row**: one record (one entity or event)
- **Column**: one attribute of that record

Example:
- a `customers` table
- one row per customer
- columns like `customer_id`, `name`, `email`

---

## Keys and Relationships

Relational databases rely on keys:

- **Primary key**: uniquely identifies a row
- **Foreign key**: references a primary key in another table

These keys make it possible to:
- connect data across tables
- avoid duplication
- maintain consistency

---

## File-Based vs Hosted Databases

Relational databases come in two broad forms:

### File-Based
- stored in a single file
- run locally
- easy to copy and version
- no server required

Examples:
- SQLite
- DuckDB

### Hosted / Server-Based
- run as services
- support many users
- common in production systems

Examples:
- PostgreSQL
- MySQL
- SQL Server
- Oracle

File-based systems may act as **proxies** for hosted systems.

---

## Why File-Based Databases Are Used

File-based databases:
- remove setup complexity
- behave like real databases
- support standard SQL
- work well with Python

This makes them ideal for:
- analytics
- experimentation
- local projects
