from pathlib import Path
import pandas as pd
import json
import re

project_root = Path(__file__).resolve().parent.parent

raw_file = (
    project_root
    / "data"
    / "raw"
    / "AIID_Excel_Export-20261019.xlsx"
)

incidents = pd.read_excel(
    raw_file,
    sheet_name="Incidents",
    header=2
)

reports = pd.read_excel(
    raw_file,
    sheet_name="Reports",
    header=1
)

incidents = incidents.dropna(how="all")
reports = reports.dropna(how="all")

print("=" * 70)
print("INSPECTING EMBEDDED RELATIONSHIP INFORMATION")
print("=" * 70)

# --------------------------------------------------
# 1. Inspect report-related fields in the Incidents sheet
# --------------------------------------------------

print("\n1. REPORT-RELATED INCIDENT COLUMNS")
print("-" * 70)

for column in incidents.columns:
    if "report" in str(column).lower():
        print(f"\nColumn: {column}")
        print("Data type:", incidents[column].dtype)
        print("Sample values:")
        print(incidents[column].head(10).to_list())

# --------------------------------------------------
# 2. Inspect the Entities field
# --------------------------------------------------

print("\n2. ENTITIES FIELD INSPECTION")
print("-" * 70)

if "Entities" in incidents.columns:

    entities_column = incidents["Entities"].dropna()

    print("Non-missing Entities values:", len(entities_column))

    if not entities_column.empty:
        sample_value = entities_column.iloc[0]

        print("\nSample Entities value:")
        print(str(sample_value)[:1500])

        print("\nDoes the sample contain an incident ID reference?")
        print(
            bool(
                re.search(
                    r"incident[_ ]?id|report[_ ]?number",
                    str(sample_value),
                    flags=re.IGNORECASE
                )
            )
        )

# --------------------------------------------------
# 3. Inspect report URL and title patterns
# --------------------------------------------------

print("\n3. REPORT URL AND TITLE INSPECTION")
print("-" * 70)

for column in ["URL", "Title", "Description"]:
    if column in reports.columns:
        print(f"\n{column}:")
        print(
            reports[column]
            .dropna()
            .astype(str)
            .head(5)
            .to_list()
        )

# --------------------------------------------------
# 4. Search column names for relationship indicators
# --------------------------------------------------

print("\n4. RELATIONSHIP FIELD SEARCH")
print("-" * 70)

for sheet_name, dataframe in [
    ("Incidents", incidents),
    ("Reports", reports),
]:

    print(f"\n{sheet_name}:")

    for column in dataframe.columns:
        column_text = str(column).lower()

        if any(
            keyword in column_text
            for keyword in [
                "incident",
                "report",
                "reference",
                "related",
                "link",
                "mapping",
                "entity"
            ]
        ):
            print("-", column)

print("\n" + "=" * 70)
print("EMBEDDED RELATIONSHIP INSPECTION COMPLETED")
print("=" * 70)