from pathlib import Path
import pandas as pd

# Project paths
project_root = Path(__file__).resolve().parent.parent
raw_file = project_root / "data" / "raw" / "AIID_Excel_Export-20261019.xlsx"

print("=" * 70)
print("AIID REPORTS DATASET INSPECTION")
print("=" * 70)

# Load the Reports sheet
reports = pd.read_excel(
    raw_file,
    sheet_name="Reports",
    header=1
)

print("\n1. DATASET DIMENSIONS")
print("-" * 70)
print(f"Rows: {reports.shape[0]}")
print(f"Columns: {reports.shape[1]}")

print("\n2. COLUMN NAMES")
print("-" * 70)
for column in reports.columns:
    print(column)

print("\n3. DATA TYPES")
print("-" * 70)
print(reports.dtypes)

print("\n4. MISSING VALUES")
print("-" * 70)
missing_values = reports.isnull().sum()
missing_values = missing_values[missing_values > 0]
print(missing_values if not missing_values.empty else "No missing values found.")

print("\n5. DUPLICATE RECORDS")
print("-" * 70)
print(f"Completely duplicated rows: {reports.duplicated().sum()}")

print("\n6. FIRST FIVE RECORDS")
print("-" * 70)
print(reports.head().to_string(index=False))

print("\n7. POTENTIAL INCIDENT-LINKING COLUMNS")
print("-" * 70)

link_columns = [
    column for column in reports.columns
    if any(
        keyword in str(column).lower()
        for keyword in ["incident", "report", "id"]
    )
]

if link_columns:
    print("Potential linking columns:")
    for column in link_columns:
        print(f"\n{column}")
        print(reports[column].head(10).to_list())
else:
    print("No obvious linking columns found. Inspect the column names manually.")

print("\n" + "=" * 70)
print("REPORTS DATASET INSPECTION COMPLETED")
print("=" * 70)