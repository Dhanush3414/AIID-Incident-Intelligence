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
print("AIID WORKBOOK RELATIONSHIP INSPECTION")
print("=" * 70)

# Display workbook sheet names
excel_file = pd.ExcelFile(raw_file)

print("\n1. WORKBOOK SHEETS")
print("-" * 70)

for sheet in excel_file.sheet_names:
    print(sheet)

# Inspect the first few rows of each relevant sheet
sheets_to_inspect = {
    "Incidents": 2,
    "Reports": 1,
    "Entities": 1,
    "Coverage Map": None
}

for sheet_name, header_row in sheets_to_inspect.items():

    print(f"\n{'=' * 70}")
    print(f"SHEET: {sheet_name}")
    print("=" * 70)

    if header_row is None:
        data = pd.read_excel(
            raw_file,
            sheet_name=sheet_name,
            header=None,
            nrows=8
        )
    else:
        data = pd.read_excel(
            raw_file,
            sheet_name=sheet_name,
            header=header_row,
            nrows=5
        )

    print("\nColumns:")
    print(data.columns.tolist())

    print("\nSample records:")
    print(data.head(5).to_string(index=False))

print("\n" + "=" * 70)
print("WORKBOOK RELATIONSHIP INSPECTION COMPLETED")
print("=" * 70)