from pathlib import Path
import pandas as pd

# Locate the original workbook
project_root = Path(__file__).resolve().parent.parent

raw_file = (
    project_root
    / "data"
    / "raw"
    / "AIID_Excel_Export-20261019.xlsx"
)

print("=" * 70)
print("AIID DATA DICTIONARY INSPECTION")
print("=" * 70)

# Read the Data Dictionary sheet without assuming its header position
dictionary = pd.read_excel(
    raw_file,
    sheet_name="Data Dictionary",
    header=None
)

print("\n1. DATASET DIMENSIONS")
print("-" * 70)
print(f"Rows: {dictionary.shape[0]}")
print(f"Columns: {dictionary.shape[1]}")

print("\n2. COMPLETE DATA DICTIONARY")
print("-" * 70)

with pd.option_context(
    "display.max_rows", None,
    "display.max_columns", None,
    "display.max_colwidth", 120,
    "display.width", 200
):
    print(dictionary.to_string(index=False, header=False))

print("\n" + "=" * 70)
print("DATA DICTIONARY INSPECTION COMPLETED")
print("=" * 70)