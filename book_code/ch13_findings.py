"""Chapter 13: the numbers behind the findings summary (uses deliveries_clean)."""
import sqlite3
import pandas as pd

con = sqlite3.connect("data/saltbush.db")
con.executescript(open("book_code/ch10_clean_view.sql").read())   # (re)create deliveries_clean
d = pd.read_sql("""
    SELECT c.*, p.region
    FROM deliveries_clean c
    JOIN depots p ON p.depot_code = c.depot_code
    WHERE c.status <> 'Cancelled'
      AND c.exclude_from_otd = 0
      AND c.promised_date BETWEEN '2026-01-01' AND '2026-06-30'
""", con)
d["on_time"] = d.delivered_at.str[:10] <= d.promised_date
d["period"] = d.booked_at.lt("2026-03-02").map({True: "Before (Jan-Feb)", False: "After (Mar-Jun)"})
d["late_booking"] = d.booked_at.str[11:16] > "16:30"

print("On-time rate by region, before and after the change")
print((d.pivot_table(index="region", columns="period", values="on_time", aggfunc="mean")
        [["Before (Jan-Feb)", "After (Mar-Jun)"]] * 100).round(1).to_string())

north = d[d.region == "Northern"]
print("\nNorthern: on-time rate by booking time")
print((north.pivot_table(index="late_booking", columns="period", values="on_time", aggfunc="mean")
        [["Before (Jan-Feb)", "After (Mar-Jun)"]] * 100).round(1)
      .rename(index={False: "Booked by 16:30", True: "Booked after 16:30"}).to_string())

after = north[north.period == "After (Mar-Jun)"]
share = after.late_booking.mean()
late_count = (~after.on_time).sum()
late_from_late_bookings = (~after.on_time & after.late_booking).sum()
print(f"\nNorthern, Mar-Jun: {len(after):,} consignments, {share:.1%} booked after 16:30")
print(f"Late consignments: {late_count:,}, of which booked after 16:30: "
      f"{late_from_late_bookings:,} "
      f"({late_from_late_bookings / late_count:.0%})")

# What if late bookings had been delivered on time as often as earlier ones?
early_rate = after.loc[~after.late_booking, "on_time"].mean()
what_if = (after.on_time.sum() - after.loc[after.late_booking, "on_time"].sum()
           + after.late_booking.sum() * early_rate) / len(after)
print(f"Northern Mar-Jun on-time: actual {after.on_time.mean():.1%}")
print(f"If late bookings matched earlier ones: {what_if:.1%}")
