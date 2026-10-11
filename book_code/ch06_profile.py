"""Chapter 6: draft a data dictionary from a table."""
import sqlite3
from pathlib import Path
import pandas as pd


def profile_table(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Return one row per column: the facts a data dictionary needs."""
    rows = []
    for col in df.columns:
        s = df[col]
        non_null = s.dropna()
        examples = ", ".join(str(v) for v in non_null.unique()[:3])
        rows.append({
            "table": table_name,
            "column": col,
            "type": str(s.dtype),
            "rows": len(s),
            "missing": int(s.isna().sum()),
            "pct_missing": round(100 * s.isna().mean(), 1),
            "distinct": int(s.nunique()),
            "min": non_null.min() if len(non_null) else None,
            "max": non_null.max() if len(non_null) else None,
            "examples": examples,
            # the human columns, left for you to write
            "description": "",
            "business_rules": "",
            "owner": "",
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    con = sqlite3.connect("data/saltbush.db")
    deliveries = pd.read_sql("SELECT * FROM deliveries", con)
    draft = profile_table(deliveries, "deliveries")

    counts = ["column", "type", "missing", "pct_missing", "distinct"]
    print(draft[counts].to_string(index=False))
    print()
    print(draft[["column", "min", "max"]].to_string(index=False))

    Path("output").mkdir(exist_ok=True)
    draft.to_excel("output/draft_data_dictionary.xlsx", index=False)
