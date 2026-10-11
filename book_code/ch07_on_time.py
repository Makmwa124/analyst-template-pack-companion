"""Chapter 7: one metric name, four definitions."""
import sqlite3
import pandas as pd

con = sqlite3.connect("data/saltbush.db")
d = pd.read_sql("""
    SELECT DISTINCT d.*, p.region
    FROM deliveries d
    JOIN depots p ON p.depot_code = d.depot_code
""", con)

# Northern region, consignments promised in April to June 2026
in_q2 = d.promised_date.between("2026-04-01", "2026-06-30")
nth = d[(d.region == "Northern") & in_q2]

# A missing delivered_at is never on time
on_time = nth.delivered_at.str[:10] <= nth.promised_date

# Version 1, the operations dashboard: on time out of delivered
delivered = nth.status == "Delivered"
v1 = (on_time & delivered).sum() / delivered.sum()

# Version 2, the SLA report: failed attempts count as late
attempted = nth.status.isin(["Delivered", "Failed attempt"])
v2 = (on_time & attempted).sum() / attempted.sum()

# Version 3, agreed: everything due and not cancelled counts
due = nth.status != "Cancelled"
v3 = (on_time & due).sum() / due.sum()

# Version 4, an old spreadsheet: cancellations counted as late
v4 = on_time.sum() / len(nth)

print(f"Consignments in scope: {len(nth):,}")
for name, value in [("1 Ops dashboard", v1), ("2 SLA report", v2),
                    ("3 Agreed", v3), ("4 Spreadsheet", v4)]:
    print(f"{name:<16} {value:.1%}")
