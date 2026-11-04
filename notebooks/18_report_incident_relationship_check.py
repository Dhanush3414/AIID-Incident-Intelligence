from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

raw_file = (
    project_root
    / "data"
    / "raw"
    / "AIID_Excel_Export-20261019.xlsx"
)

print("=" * 70)
print("REPORT-TO-INCIDENT RELATIONSHIP CHECK")
print("=" * 70)

# Load the relevant sheets
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

# Remove fully empty rows
incidents = incidents.dropna(how="all")
reports = reports.dropna(how="all")

print("\n1. INCIDENT IDENTIFIERS")
print("-" * 70)

print("Incident rows:", len(incidents))
print("Unique Incident IDs:", incidents["Incident ID"].nunique())
print("Incident ID missing values:", incidents["Incident ID"].isna().sum())

print("\n2. REPORT IDENTIFIERS")
print("-" * 70)

print("Report rows:", len(reports))
print("Unique Report Numbers:", reports["Report Number"].nunique())
print("Report Number missing values:", reports["Report Number"].isna().sum())

print("\n3. POSSIBLE RELATIONSHIP COLUMNS")
print("-" * 70)

keywords = ["incident", "report", "entity", "id", "url"]

print("\nIncident columns:")
for column in incidents.columns:
    if any(word in str(column).lower() for word in keywords):
        print("-", column)

print("\nReport columns:")
for column in reports.columns:
    if any(word in str(column).lower() for word in keywords):
        print("-", column)

print("\n4. REPORT COUNT VALIDATION")
print("-" * 70)

if "report_count" in incidents.columns:
    total_linked_reports = incidents["report_count"].sum()

    print("Sum of incident report_count:", total_linked_reports)
    print("Number of report records:", len(reports))

    print(
        "Difference (report records - summed report_count):",
        len(reports) - total_linked_reports
    )

    print(
        "\nNote: A difference does not necessarily indicate an error. "
        "The export may include unlinked reports or use different counting rules."
    )

print("\n5. CHECK FOR POSSIBLE DIRECT ID MATCH")
print("-" * 70)

incident_ids = set(
    incidents["Incident ID"].dropna().astype(str).str.strip()
)

report_numbers = set(
    reports["Report Number"].dropna().astype(str).str.strip()
)

matches = incident_ids.intersection(report_numbers)

print("Exact identifier matches:", len(matches))
print("Sample matches:", list(matches)[:10])

print("\n" + "=" * 70)
print("RELATIONSHIP CHECK COMPLETED")
print("=" * 70)