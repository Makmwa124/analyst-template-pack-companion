"""Chapter 13: the one chart in the findings summary (black and white friendly)."""
import sqlite3
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

con = sqlite3.connect("data/saltbush.db")
con.executescript(open("book_code/ch10_clean_view.sql").read())
d = pd.read_sql("""
    SELECT c.booked_at, c.promised_date, c.delivered_at
    FROM deliveries_clean c
    JOIN depots p ON p.depot_code = c.depot_code
    WHERE p.region = 'Northern' AND c.status <> 'Cancelled' AND c.exclude_from_otd = 0
      AND c.promised_date BETWEEN '2026-01-01' AND '2026-06-30'
""", con)
d["on_time"] = d.delivered_at.str[:10] <= d.promised_date
d["after"] = d.booked_at >= "2026-03-02"
d["late_booking"] = d.booked_at.str[11:16] > "16:30"
rates = d.groupby(["late_booking", "after"]).on_time.mean().mul(100).round(1)
print(rates.to_string())

labels = ["Booked by 16:30", "Booked after 16:30"]
before = [rates[(False, False)], rates[(True, False)]]
after = [rates[(False, True)], rates[(True, True)]]
fig, ax = plt.subplots(figsize=(6, 3.2), dpi=200)
x = range(len(labels))
b1 = ax.bar([i - 0.2 for i in x], before, width=0.38, color="#b8b8b8", label="Before 2 March")
b2 = ax.bar([i + 0.2 for i in x], after, width=0.38, color="#333333", label="From 2 March")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f"{bar.get_height():.1f}%", ha="center", fontsize=9)
ax.set_xticks(list(x), labels)
ax.set_ylim(0, 110)
ax.set_ylabel("On-time rate (%)")
ax.set_title("Northern on-time delivery by booking time, Jan to Jun 2026", fontsize=10, loc="left")
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="upper right")
fig.text(0.01, 0.01, "Source: FleetTrack deliveries extract (S01), on-time per card OTD-01.", fontsize=7)
fig.tight_layout(rect=(0, 0.04, 1, 1))
Path("output").mkdir(exist_ok=True)
fig.savefig("output/fig13_1_booking_time.png")
