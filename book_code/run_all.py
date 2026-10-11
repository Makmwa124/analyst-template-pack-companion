"""Run every code example in the book, in order, from the repository folder:
    python book_code/run_all.py
"""
import subprocess
import sys

STEPS = [
    ["book_code/ch06_profile.py"],
    ["book_code/run_sql.py", "book_code/ch06_profile.sql"],
    ["book_code/ch07_on_time.py"],
    ["book_code/run_sql.py", "book_code/ch07_on_time.sql"],
    ["book_code/ch10_qa_checks.py"],
    ["book_code/run_sql.py", "book_code/ch10_clean_view.sql"],
    ["book_code/run_sql.py", "book_code/ch10_join_check.sql"],
    ["book_code/ch10_qa_checks.py", "deliveries_clean"],
    ["book_code/ch13_findings.py"],
    ["book_code/ch13_chart.py"],
    ["book_code/run_sql.py", "book_code/appB_failed_attempts.sql"],
]
for step in STEPS:
    print(f"\n===== {' '.join(step)} =====")
    subprocess.run([sys.executable, *step], check=True)
