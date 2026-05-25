# datafun-05-sql

[![Python](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=white)](https://www.python.org/)

> Professional Python project: relational data and analytics.

## Project Planning

Python helps with relational data. We often have tabular data in csv or other spreadsheet-like files.
Python helps extract data from raw files, do basic cleaning and transformation steps,
and load the data into a new sink (place) like a relational datastore.

Data has been provided for the following topic domains in the data/ directory:

- retail (a store records many sales) - this is the example
- library (a library branch manages many checkouts)
- shelter (a shelter branch manages many animal adoptions)
- civic_event (a civic_event manages many people's attendance. NOTE: never name things "event" as that is a keyword like function or int)

Each has two tables in a 1 to Many (1:M) relationship.
Choose one domain that is NOT the retail example.

Explore the sample data.

- What _entities_ are you working with?
- What _attributes_ describe each entity?
- How are entities _related_ to one another?

Relational data is typically stored in tables and queried with **SQL**, an excellent language for querying structured data.
In analytics, SQL is used alongside Python to:

- filter and aggregate structured data,
- combine information from multiple related tables,
- answer questions efficiently and reproducibly.

In this project, we use a **file-based relational database** (DuckDB).
We store SQL queries in files and use Python to execute them and inspect results.

Use this project to think about:

- when SQL is a better tool than pure Python,
- how queries can be saved, reviewed, and reused,
- how Python and SQL complement each other in analytics workflows.

To complete the project, you will implement a second topic domain.

- You will create .sql files in the sql/duckdb/ folder (follow the retail examples).
- You will create a .py file in the src/datafun_05_sql folder (follow the retail example).

Note: Files must include your name or alias AND the domain like we do in the examples.

- Replace `case` in filenames with your name or alias.
- Replace `retail` in filenames with your domain (library, shelter, civic_event).

---

## 01: Set Up Machine (Once Per Machine)

Follow the detailed instructions at:
[**01. Set Up Your Machine**](https://denisecase.github.io/pro-analytics-02/01-set-up-machine/)

## 02: Set Up Project (Once Per Project)

1. Get Repository: Sign in to GitHub, open this repository in your browser, and click **Copy this template** to get a copy in **YOURACCOUNT**.

2. Configure Repository Settings:
   - Select your repository **Settings** (the gear icon way on the right).
   - Go to **Pages** tab / Enable GitHub Pages / Build and deployment / set **Source** to **GitHub Actions**
   - Go to **Advanced Security** tab / Dependabot / **Dependabot security updates** / **Enable**
   - Go to **Advanced Security** tab / Dependabot / **Grouped security updates** / **Enable**

3. Clone to local: Open a **machine terminal** in your **`Repos`** folder and clone your new repo.

```shell
git clone https://github.com/YOURACCOUNT/datafun-05-sql
```

4. Open project in VS Code: Change directory into the repo and open the project in VS Code by running `code .` ("code dot"):

```shell
cd datafun-05-sql
code .
```

5. Install recommended extensions.
   - When VS Code opens, accept the Extension Recommendations (click **`Install All`** or similar when asked).

6. Set up a project Python environment (managed by `uv`) and align VS Code with it.
   - Use VS Code menu option `Terminal` / `New Terminal` to open a **VS Code terminal** in the root project folder.
   - Run the following commands, one at a time, hitting ENTER after each:

   ```shell
   uv self update
   uv python pin 3.14
   uv sync --extra dev --extra docs --upgrade
   ```

If asked: "We noticed a new environment has been created. Do you want to select it for the workspace folder?" Click **"Yes"**.

If successful, you'll see a new `.venv` folder appear in the root project folder.

Optional (recommended): install and run pre-commit checks (repeat the git `add` and `commit` twice if needed):

```shell
uvx pre-commit install
git add -A
uvx pre-commit run --all-files
git add -A
uvx pre-commit run --all-files
```

Fore more detailed instructions and troubleshooting, see the pro guide at:
[**02. Set Up Your Project**](https://denisecase.github.io/pro-analytics-02/02-set-up-project/)

🛑 Do not continue until all REQUIRED steps are complete and verified.

## 03: Daily Workflow (Working With Python Project Code)

Follow the detailed instructions at:
[**03. Daily Workflow**](https://denisecase.github.io/pro-analytics-02/03-daily-workflow/)

Commands are provided below to:

1. Git pull
2. Run the pipeline
3. Build and serve docs
4. Save progress with Git add-commit-push
5. Update project files

VS Code should have only this project (datafun-05-sql) open.
Use VS Code menu option `Terminal` / `New Terminal` and run the following commands:

```shell
git pull
```

Run the Python source files:

```shell
uv run python -m datafun_05_sql.case_duckdb_retail
```

Run Python checks and tests (as available):

```shell
uv run ruff format .
uv run ruff check . --fix
uv run pytest --cov=src --cov-report=term-missing
```

Build and serve docs (hit **CTRL+c** in the VS Code terminal to quit serving):

```shell
uv run mkdocs build --strict
uv run mkdocs serve
```

While editing project code and docs, repeat the commands above to run files, check them, and rebuild docs as needed.

Save progress frequently (some tools may make changes; you may need to **re-run git `add` and `commit`** to ensure everything gets committed before pushing):

```shell
git add -A
git commit -m "update"
git push -u origin main
```

Additional details and troubleshooting are available in the [Pro-Analytics-02 Documentation](https://denisecase.github.io/pro-analytics-02/).

---

## Project Objectives

### Project Task 1. Personalize Your Documentation Links

Open [mkdocs.yaml](./mkdocs.yaml).
This file configures the associated project documentation website (powered by MkDocs)
Use CTRL+f to find each occurrence of the source GitHub account (e.g. `denisecase`).
Change each occurrence to point to your GitHub account instead (spacing and capitalization MUST match the URL of your GitHub account **exactly**.)

### Project Task 2. Personalize Your SQL and Python Files

Choose one of the custom domains in the data/ folder (e.g. library or shelter).

You will implement the same process as we did for retail using your domain.
For example, if you choose library, follow the example files in sql/duckdb/ (keep these as working examples):

- case_retail_bootstrap.sql
- case_retail_clean.sql
- case_retail_query_kpi_revenue.sql
- ...

If you do library, you would add a new file for each of those (~7) files like so:

- yourname_library_bootstrap.sql
- yourname_library_clean.sql
- yourname_library_query_kpi_checkouts.sql (or whatever KPI you want to explore)
- ....

1. Copy `case_duckdb_retail.py` to reflect your name or alias and your domain.
2. Edit this README.md file to add a new run command to execute your file instead.
3. Preview this README.md to make sure it still appears correctly.
   - Find README.md in the VS Code Explorer window (top icon on the left)
   - Right-click / Preview
   - Fix any issues.
4. Run the additional command to execute **your** Python script.

### Project Task 3. Implement Your Files

Use SQL files for relational logic and Python for orchestration and result inspection.

1. Read the example code carefully **before** starting.
2. Pick your sample data/ domain (topic).
3. Pick your database (either DuckDB recommended or SQLite)
4. You must perform analogous work for a new domain using at least one of the database choices.
5. You should create 7 or more sql files (see the sql/ folder) with your name/alias and domain/topic.
6. You should create 1 Python file that orchestrates the pipeline.

**Save often**: After making any useful progress, follow the steps to git add-commit-push.

When done, verify your GitHub repo has:

- project.log file (in the root folder)
- artifacts/ with the example database and your database
- sql/* folder has your files, correctly named and implemented
- src/* folder has your file, correctly named, situated, and implemented.
- README.md has been updated to include the commands you use to execute your files as needed.

Could you do this at work if you were given two or more csv files with related data?

What else will you work on to ensure you can demonstrate these capabilities?

---

## Notes

- You do not need to add to or modify `tests/`. They are provided for example only.
- You do not need to view or modify any of the supporting **config files**.
- Many of the repo files are silent helpers. Explore as you like, but nothing is required.
- You do NOT need to understand everything. Understanding builds naturally over time.
- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) with in a file.

## Resources

- [Pro-Analytics-02](https://denisecase.github.io/pro-analytics-02/) - guide to professional Python

## Citation

[CITATION.cff](./CITATION.cff) - TODO: update author and repository fields to reflect your creative work

## License

[MIT](./LICENSE)
