"""Chapter 10: run the automated QA checks and print the results.

Usage: python book_code/ch10_qa_checks.py [table]
(the table defaults to deliveries)
"""
import sqlite3
import sys
from datetime import date
from pathlib import Path
import pandas as pd

TABLE = sys.argv[1] if len(sys.argv) > 1 else "deliveries"
con = sqlite3.connect("data/saltbush.db")

# Each check: an ID matching the QA checklist, a query that returns
# one number, and the largest number that still counts as a pass.
CHECKS = [
    ("C01", "Rows minus TMS total",
     """SELECT (SELECT COUNT(*) FROM {t})
             - (SELECT SUM(consignments_booked)
                FROM tms_monthly_summary)""", 0),
    ("C02", "Exact duplicate rows",
     """SELECT COUNT(*)
             - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM {t}))
        FROM {t}""", 0),
    ("C03", "IDs with conflicting rows",
     """SELECT COUNT(*) FROM (
            SELECT consignment_id FROM (SELECT DISTINCT * FROM {t})
            GROUP BY consignment_id HAVING COUNT(*) > 1)""", 0),
    ("C04", "Unknown depot codes",
     """SELECT COUNT(*) FROM {t}
        WHERE depot_code NOT IN (SELECT depot_code FROM depots)""", 0),
    ("C05", "Weights of zero or less",
     "SELECT COUNT(*) FROM {t} WHERE weight_kg <= 0", 0),
    ("C06", "Delivered before booked",
     "SELECT COUNT(*) FROM {t} WHERE delivered_at < booked_at", 0),
    ("C07", "Delivered, no delivery time",
     """SELECT COUNT(*) FROM {t}
        WHERE status = 'Delivered' AND delivered_at IS NULL""", 0),
    ("C08", "Blank postcodes",
     "SELECT COUNT(*) FROM {t} WHERE postcode IS NULL", 400),  # ~2%
]

results = []
for check_id, name, sql, max_ok in CHECKS:
    value = con.execute(sql.format(t=TABLE)).fetchone()[0]
    results.append({
        "check_id": check_id,
        "check": name,
        "value": value,
        "max_ok": max_ok,
        "result": "Pass" if value <= max_ok else "Fail",
    })

report = pd.DataFrame(results)
print(report.to_string(index=False))
failed = (report.result == "Fail").sum()
print(f"\n{failed} of {len(report)} checks failed")

Path("output").mkdir(exist_ok=True)
report.insert(0, "run_date", date.today().isoformat())
report.to_csv(f"output/qa_results_{TABLE}.csv", index=False)
