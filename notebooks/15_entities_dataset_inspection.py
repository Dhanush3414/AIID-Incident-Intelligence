from pathlib import Path
import pandas as pd

# Locate the project root and original dataset
project_root = Path(__file__).resolve().parent.parent

raw_file = (
    project_root
    / "data"
    / "raw"
    / "AIID_Excel_Export-20261019.xlsx"
)

print("=" * 70)
print("AIID ENTITIES DATASET INSPECTION")
print("=" * 70)

# Load the Entities worksheet
entities = pd.read_excel(
    raw_file,
    sheet_name="Entities",
    header=1
)

# 1. Dataset dimensions
print("\n1. DATASET DIMENSIONS")
print("-" * 70)
print(f"Rows: {entities.shape[0]}")
print(f"Columns: {entities.shape[1]}")

# 2. Column names
print("\n2. COLUMN NAMES")
print("-" * 70)
print(entities.columns.tolist())

# 3. Data types
print("\n3. DATA TYPES")
print("-" * 70)
print(entities.dtypes)

# 4. Missing values
print("\n4. MISSING VALUES")
print("-" * 70)
print(entities.isnull().sum())

# 5. Duplicate records
print("\n5. DUPLICATE RECORDS")
print("-" * 70)
print(f"Completely duplicated rows: {entities.duplicated().sum()}")

# 6. First ten records
print("\n6. FIRST TEN RECORDS")
print("-" * 70)
print(entities.head(10).to_string(index=False))

# 7. Unique values and counts
print("\n7. UNIQUE VALUE COUNTS")
print("-" * 70)

for column in entities.columns:
    print(f"\nColumn: {column}")
    print(f"Unique values: {entities[column].nunique(dropna=True)}")
    print(entities[column].value_counts(dropna=False).head(10))

print("\n" + "=" * 70)
print("ENTITIES DATASET INSPECTION COMPLETED")
print("=" * 70)