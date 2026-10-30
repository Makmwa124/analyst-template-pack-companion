# The Analyst's Template Pack: companion files

Free templates and practice files for the book **The Analyst's Template Pack: Project Briefs, Data Dictionaries, QA Checklists and Handover Docs, with a Worked Example for Every One** by Mathew Kariuki.

The book gives you eleven templates that cover an analysis project from the first conversation to the handover, and shows each one completed for a single project at Saltbush Freight, a fictional regional freight company in South Australia. This repository holds the blank templates as Word and Excel files, the completed Saltbush examples, the Saltbush practice database, and every SQL query and Python script from the book.

## Download

Click the green **Code** button above, then **Download ZIP**. Unzip it somewhere sensible, such as your Documents folder.

## What's here

| Path | What it is |
| --- | --- |
| `templates/blank/` | The eleven templates, ready to copy and fill in: `01_project_brief.docx`, `02_kickoff_questions.docx`, `03_data_dictionary.xlsx`, `04_metric_definition_card.docx`, `05_source_register.xlsx`, `06_data_request.docx`, `07_qa_checklist.xlsx`, `08_peer_review_checklist.docx`, `09_assumptions_decisions_log.xlsx`, `10_findings_summary.docx`, `11_handover_document.docx` |
| `templates/examples/` | The same templates completed for the Saltbush project, as shown in the book |
| `data/saltbush.db` | The Saltbush Freight practice database (SQLite): deliveries, depots, customers, TMS monthly summary, linehaul timetable |
| `data/*.csv` | The same tables as CSV files |
| `book_code/` | Every code example by chapter (`ch06_profile.py`, `ch07_on_time.sql`, `ch10_qa_checks.py`, `ch13_findings.py` ...), `run_sql.py` to run any `.sql` file, and `run_all.py` to run them all |
| `scripts/new_project.py` | Sets up a new project folder with the standard layout and copies in the blank templates (Chapter 15) |
| `scripts/make_data.py` | The script that generated the practice data (fixed random seed) |

The Excel templates use only standard formulas (such as COUNTIF, COUNTBLANK, COUNTA, IF and SUM) and drop-down lists, so they work in Excel, LibreOffice Calc and Google Sheets. Each workbook has a Guide sheet. Yellow cells are for you to fill in.

## Quick start

The templates need nothing but Word and Excel (or any program that opens .docx and .xlsx files). Copy the ones you need from `templates/blank/` into your project folder.

To run the code:

1. Install Python, then run:

   ```
   pip install -r requirements.txt
   ```

2. In VS Code, choose **File > Open Folder** and open this folder.
3. Run any example from this folder, for example:

   ```
   python book_code/ch10_qa_checks.py
   python book_code/run_sql.py book_code/ch07_on_time.sql
   python book_code/run_all.py
   ```

4. To start a new project with the standard folders and templates:

   ```
   python scripts/new_project.py "My project name" --root projects
   ```

Scripts that write files save them to an `output` folder. Tested with Python 3.13 and pandas 3.0. The data was generated with a fixed random seed, so your output will match the book exactly.

## Get the book

Paperback and Kindle editions are on Amazon.

## About

Saltbush Freight and every person, customer and number in its data are fictional. The templates, data and code are free to use, adapt and share for learning and at work. The book itself is © 2026 Mathew Kariuki.

Spotted a problem with a template, an example or the data? Please open an issue.
