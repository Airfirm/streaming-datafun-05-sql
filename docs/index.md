# Streaming Data Analytics with Python / SQL

## Dataset

For this custom project, I used two different datasets and two different database pipelines.

The first project file is `femi_sqlite_library.py`. This file uses the library dataset located in `data/library/`. The two CSV files are:

- `branch.csv`
- `checkout.csv`

The `branch.csv` file contains library branch information, including branch ID, branch name, city, and library system name. The `checkout.csv` file contains checkout activity, including checkout ID, branch ID, material type, checkout duration, fine amount, and checkout date.

The second project file is `femi_duckdb_civic_event.py`. This file uses the civic event dataset located in `data/civic_event/`. The two CSV files are:

- `civic_event.csv`
- `attendance.csv`

The `civic_event.csv` file contains event information, including civic event ID, event name, location, and organizer. The `attendance.csv` file contains event attendance activity, including attendance ID, civic event ID, attendee type, checked-in status, contribution amount, and attendance date.

Together, these projects show how Python and SQL can be used to load structured CSV data into databases and then query that data for useful insights.

### Signals

In the library project, the main signals include:

- branch location
- library system name
- material type
- checkout duration
- fine amount
- checkout date

These signals help identify which branches are being used, what materials are being checked out, how long materials are kept, and how much fine revenue is being generated.

In the civic event project, the main signals include:

- event name
- event location
- organizer
- attendee type
- checked-in status
- contribution amount
- attendance date

These signals help identify which events are attracting participation, whether attendees are members or guests, how many people checked in, and how much contribution money was collected.

I also created useful analytical signals through SQL queries, such as:

- total number of library branches
- total number of checkout records
- total fine amount
- checkouts by branch
- checkouts by material type
- average checkout duration
- total number of civic events
- total attendance records
- total contributions
- attendance by attendee type
- contributions by event
- checked-in count by event

These signals make the raw CSV data more useful for analysis.

### Experiments

For my modification experiments, I changed the original retail database examples into two custom projects.

For the SQLite experiment, I created `femi_sqlite_library.py`. Instead of loading retail store and sales data, I modified the code to point to the `data/library/` folder. I changed the database purpose so it analyzes library branches and checkout records. I also changed the output database name to `library.sqlite`.

For the DuckDB experiment, I created `femi_duckdb_civic_event.py`. Instead of loading retail data, I modified the code to point to the `data/civic_event/` folder. I changed the database purpose so it analyzes civic events, attendance records, attendee types, check-in activity, and contribution amounts. I also changed the output database name to `civic_event.duckdb`.

These experiments helped me practice changing an existing pipeline for a new business or organizational problem. I had to update the file paths, table names, database names, field names, SQL logic, and project purpose.

### Results

After running `femi_sqlite_library.py`, the script created a SQLite database file in the artifacts folder:

`artifacts/sqlite/library.sqlite`

The library pipeline loaded the branch and checkout CSV files into database tables. The query results showed information such as how many branches were included, how many checkout records were processed, which branches had the most checkout activity, which material types were checked out, and how much fine money was recorded.

After running `femi_duckdb_civic_event.py`, the script created a DuckDB database file in the artifacts folder:

`artifacts/duckdb/civic_event.duckdb`

The civic event pipeline loaded the civic event and attendance CSV files into database tables. The query results showed information such as how many civic events were included, how many attendance records were processed, which events had the most participation, which attendee types were represented, how many people checked in, and how much contribution money was collected.

One important observation is that the `.sqlite` and `.duckdb` files are database files, not normal text files. They may not open directly in VS Code like a `.csv` or `.py` file. The best way to verify them is by running the Python scripts and reviewing the query results in the terminal logs.

### Interpretation

These projects show how Python and SQL can work together to turn CSV files into useful data stores. Python automates the pipeline, while SQLite and DuckDB store the data and make it possible to query the information.

The library project provides business intelligence about library usage. It can help answer questions such as which branch has the most checkout activity, which material types are most popular, and where fines are being generated. A library system could use this information to understand patron behavior, plan resources, and identify branches or materials that may need more attention.

The civic event project provides business intelligence about community participation. It can help answer questions such as which events had the highest attendance, which attendee types participated the most, and which events collected the most contributions. A civic organization could use this information to evaluate event success, understand community engagement, and plan future outreach.

Overall, this system shows the value of combining data-at-rest with Python and SQL. Instead of only looking at raw CSV files, the data is loaded into databases where it can be organized, queried, summarized, and interpreted. This makes the analysis more repeatable, professional, and useful for decision-making.

---

To customize, modify:

- `docs/` (folder with Markdown files)
- `mkdocs.yaml` (in the root project folder)
  - scroll to the end for the `nav` section
