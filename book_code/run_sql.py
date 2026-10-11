"""Run a .sql file against data/saltbush.db and print each result.
Usage (from the repository folder):
    python book_code/run_sql.py book_code/ch06_profile.sql
"""
import sqlite3
import sys
import pandas as pd

sql = open(sys.argv[1], encoding="utf-8").read()
con = sqlite3.connect("data/saltbush.db")
for stmt in [s.strip() for s in sql.split(";")]:
    code = "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--")).strip()
    if not code:
        continue
    cur = con.execute(stmt)
    if cur.description:                       # a query that returns rows
        cols = [c[0] for c in cur.description]
        print(pd.DataFrame(cur.fetchall(), columns=cols).to_string(index=False))
        print()
con.commit()
