# SQL and Python Together (P05)

This document explains how **SQL and Python** are combined in professional data analytics workflows.

Both languages are essential.
They serve different but complementary roles.

## Why We Use Both SQL and Python

SQL is best for:

- filtering
- joining
- grouping
- aggregating
- shaping relational data

Python is best for:

- orchestration
- automation
- file handling
- configuration
- analysis and visualization

Professional analytics workflows use **both**.

## Separation of Responsibilities

A common best practice:

- SQL handles **data logic**
- Python handles **program logic**

This separation improves:

- readability
- reuse
- testing
- collaboration

## SQL in `.sql` Files

In professional projects:

- SQL is often stored in `.sql` files
- queries are versioned and reviewed
- logic is reused across scripts

Benefits:

- easier to read than embedded strings
- easier to test
- easier to maintain

## Parameterized Queries

When SQL needs inputs (dates, limits, IDs):

- use **parameterized queries**
- do not insert values directly into SQL text

Why:

- safer
- reusable
- clearer intent

Vocabulary to know:

- parameterized query
- placeholder
- bound parameter

## Python as the Orchestrator

Python typically:

- reads SQL files
- opens database connections
- binds parameters
- executes queries
- receives results as tables or dataframes
- saves outputs

This pattern scales from:

- example projects
- to analytics teams
- to production pipelines

## DataFrames and SQL

Modern analytics workflows often:

- run SQL
- return results into a pandas DataFrame
- continue analysis in Python

This allows analysts to:

- use the best tool at each step
- stay flexible
- work efficiently
