import pandas as pd
from pathlib import Path

file_path = Path("data/raw/AIID_Excel_Export-20261019.xlsx")

print("=" * 70)
print("AIID TAXONOMY AND DATA DICTIONARY INSPECTION")
print("=" * 70)

# 1. Inspect the exact sheet names
excel_file = pd.ExcelFile(file_path)

print("\n1. AVAILABLE EXCEL SHEETS")
for sheet in excel_file.sheet_names:
    print(repr(sheet))

# 2. Inspect the Data Dictionary
dictionary = pd.read_excel(
    file_path,
    sheet_name="Data Dictionary",
    header=None
)

print("\n2. DATA DICTIONARY - FIRST 20 ROWS")
print(dictionary.head(20).to_string(index=False, header=False))

# 3. Find the Coverage Map sheet automatically
coverage_sheet = next(
    (sheet for sheet in excel_file.sheet_names
     if "Coverage Map" in sheet),
    None
)

if coverage_sheet:
    coverage = pd.read_excel(
        file_path,
        sheet_name=coverage_sheet,
        header=None
    )

    print("\n3. COVERAGE MAP")
    print(coverage.to_string(index=False, header=False))
else:
    print("\n3. COVERAGE MAP SHEET NOT FOUND")

# 4. Inspect incident classifications
incidents = pd.read_excel(
    file_path,
    sheet_name="Incidents",
    header=2
)

print("\n4. RISK DOMAIN DISTRIBUTION")
print(incidents["Risk Domain"].value_counts(dropna=False).to_string())

print("\n5. RISK SUBDOMAIN - TOP 15")
print(
    incidents["Risk Subdomain"]
    .value_counts(dropna=False)
    .head(15)
    .to_string()
)

print("\n6. HARM DOMAIN DISTRIBUTION")
print(incidents["Harm Domain"].value_counts(dropna=False).to_string())

print("\n7. AI HARM LEVEL DISTRIBUTION")
print(incidents["AI Harm Level"].value_counts(dropna=False).to_string())

print("\nInspection complete. No data has been modified.")