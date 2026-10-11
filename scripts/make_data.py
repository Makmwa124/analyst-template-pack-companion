"""Generate the Saltbush Freight practice database (fictional data, fixed seed)."""
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(14)
OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

depots = pd.DataFrame({
    "depot_code": ["ADL", "MBR", "MTG", "PAG", "PPI", "WHY"],
    "depot_name": ["Wingfield", "Murray Bridge", "Mount Gambier", "Port Augusta", "Port Pirie", "Whyalla"],
    "region": ["Metro", "South East", "South East", "Northern", "Northern", "Northern"],
    "linehaul_from_adl": [0, 1, 1, 1, 1, 1],
})

first = ["Coorong", "Flinders", "Barossa", "Eyre", "Clare", "Limestone", "Spencer", "Gawler", "Riverland",
         "Yorke", "Onkaparinga", "Fleurieu", "Mallee", "Saltbush", "Wakefield", "Torrens"]
second = ["Hardware", "Produce", "Pharmacy", "Auto Parts", "Farm Supply", "Electrical", "Office Supplies",
          "Wines", "Building Supplies", "Pet Supplies", "Medical", "Outdoor"]
names = sorted({f"{a} {b}" for a in first for b in second})
rng.shuffle(names)
n_cust = 180
customers = pd.DataFrame({
    "customer_id": [f"C{1000 + i}" for i in range(n_cust)],
    "customer_name": names[:n_cust],
    "segment": rng.choice(["Retail", "Trade", "Agriculture", "Health"], n_cust, p=[0.4, 0.3, 0.2, 0.1]),
})

# deliveries
days = pd.date_range("2026-01-01", "2026-06-30", freq="D")
rows = []
depot_weights = {"ADL": 0.46, "MBR": 0.10, "MTG": 0.12, "PAG": 0.13, "PPI": 0.11, "WHY": 0.08}
cid = 4_100_000
for d in days:
    if d.weekday() == 6:
        continue
    base = 150 if d.weekday() < 5 else 35
    n = rng.poisson(base)
    for _ in range(n):
        cid += 1
        depot = rng.choice(list(depot_weights), p=list(depot_weights.values()))
        hour = rng.choice(np.arange(7, 19), p=np.array([2, 5, 8, 10, 11, 10, 11, 12, 11, 9, 7, 4]) / 100)
        minute = int(rng.integers(0, 60))
        booked = d + pd.Timedelta(hours=int(hour), minutes=minute)
        service = "Express" if rng.random() < 0.18 else "Standard"
        lead = 1 if (service == "Express" or depot == "ADL") else 2
        promised = (booked.normalize() + pd.tseries.offsets.BDay(lead)).normalize()
        # on-time mechanics
        p_late = 0.04 if depot == "ADL" else 0.055
        if depot_weights and depot in ("PAG", "PPI", "WHY"):
            cutoff = pd.Timedelta(hours=18) if d < pd.Timestamp("2026-03-02") else pd.Timedelta(hours=16, minutes=30)
            if booked - booked.normalize() > cutoff:
                p_late = 0.80
        late = rng.random() < p_late
        u = rng.random()
        if u < 0.012:
            status = "Cancelled"
        elif u < 0.035:
            status = "Failed attempt"
        else:
            status = "Delivered"
        delivered = pd.NaT
        if status == "Delivered":
            day = promised + (pd.tseries.offsets.BDay(1) if late else pd.Timedelta(0))
            if not late and rng.random() < 0.06:
                day = promised - pd.tseries.offsets.BDay(1)
                if day <= booked.normalize():
                    day = promised
            delivered = pd.Timestamp(day) + pd.Timedelta(hours=int(rng.integers(8, 17)), minutes=int(rng.integers(0, 60)))
        if status == "Delivered" and d >= pd.Timestamp("2026-06-26") and late:
            status, delivered = "In transit", pd.NaT
        weight = round(float(rng.lognormal(2.3, 0.9)), 1)
        rows.append({
            "consignment_id": f"SB{cid}",
            "customer_id": customers.customer_id.iloc[int(rng.integers(0, n_cust))],
            "depot_code": depot,
            "service_level": service,
            "booked_at": booked.strftime("%Y-%m-%d %H:%M"),
            "promised_date": promised.strftime("%Y-%m-%d"),
            "delivered_at": None if pd.isna(delivered) else delivered.strftime("%Y-%m-%d %H:%M"),
            "status": status,
            "weight_kg": weight,
            "cartons": int(max(1, round(weight / 9 + rng.integers(0, 3)))),
            "postcode": str({"ADL": 5000, "MBR": 5253, "MTG": 5290, "PAG": 5700, "PPI": 5540, "WHY": 5600}[depot] + int(rng.integers(0, 40))),
        })
deliv = pd.DataFrame(rows)

# --- the mess real extracts carry ---
rng.choice(deliv.index, 40, replace=False)              # (kept so later random draws are unchanged)
pag_rows = deliv.index[deliv.depot_code == "PAG"]
idx = np.random.default_rng(99).choice(pag_rows, 40, replace=False)
deliv.loc[idx, "depot_code"] = "PAU"                    # keying error for Port Augusta, not in depots
neg = rng.choice(deliv.index, 6, replace=False)
deliv.loc[neg, "weight_kg"] = -deliv.loc[neg, "weight_kg"]   # negative weights
nopc = rng.choice(deliv.index, 210, replace=False)
deliv.loc[nopc, "postcode"] = None
deliv_ok = deliv[deliv.status == "Delivered"].index
back = rng.choice(deliv_ok, 9, replace=False)
for i in back:   # delivered before booked (device clock errors)
    b = pd.Timestamp(deliv.at[i, "booked_at"])
    deliv.at[i, "delivered_at"] = (b - pd.Timedelta(hours=int(rng.integers(2, 30)))).strftime("%Y-%m-%d %H:%M")
dups = deliv.sample(150, random_state=14)                 # re-imported scans
deliv = pd.concat([deliv, dups]).sort_values(["booked_at", "consignment_id"]).reset_index(drop=True)

# the official monthly summary from the TMS (counts unique consignments)
uniq = deliv.drop_duplicates()
tms = (uniq.assign(month=uniq.booked_at.str[:7]).groupby("month").size()
       .rename("consignments_booked").reset_index())

db = OUT / "saltbush.db"
db.unlink(missing_ok=True)
with sqlite3.connect(db) as con:
    depots.to_sql("depots", con, index=False)
    customers.to_sql("customers", con, index=False)
    deliv.to_sql("deliveries", con, index=False)
    tms.to_sql("tms_monthly_summary", con, index=False)
deliv.to_csv(OUT / "deliveries.csv", index=False)
depots.to_csv(OUT / "depots.csv", index=False)
customers.to_csv(OUT / "customers.csv", index=False)
tms.to_csv(OUT / "tms_monthly_summary.csv", index=False)
print(len(deliv), "delivery rows written to", db.name)

# S05: linehaul timetable history (from the Linehaul Manager's spreadsheet)
linehaul = pd.DataFrame({
    "route": ["Adelaide to Northern (PAG, PPI, WHY)", "Adelaide to Northern (PAG, PPI, WHY)",
              "Adelaide to Mount Gambier (MTG)", "Adelaide to Murray Bridge (MBR)"],
    "effective_from": ["2025-01-01", "2026-03-02", "2025-01-01", "2025-01-01"],
    "effective_to": ["2026-03-01", None, None, None],
    "departs_adelaide": ["18:00", "16:30", "17:30", "18:30"],
    "reason": ["", "Contractor changed driver shifts", "", ""],
})
linehaul.to_csv(OUT / "linehaul_timetable.csv", index=False)
with sqlite3.connect(db) as con:
    linehaul.to_sql("linehaul_timetable", con, index=False)
