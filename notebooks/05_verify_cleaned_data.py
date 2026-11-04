import pandas as pd
from pathlib import Path

# Path to the cleaned dataset
file_path = Path("data/processed/incidents_cleaned.csv")

print("=" * 70)
print("CLEANED DATASET VERIFICATION")
print("=" * 70)

# 1. Check whether the file exists
print("\n1. FILE EXISTENCE")
print("File exists:", file_path.exists())

if not file_path.exists():
    raise FileNotFoundError(f"Dataset not found: {file_path}")

# 2. Load the cleaned dataset
df = pd.read_csv(file_path)

print("\n2. DATASET DIMENSIONS")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 3. Display column names
print("\n3. COLUMN NAMES")
print(df.columns.tolist())

# 4. Check duplicate records
print("\n4. DUPLICATE CHECK")
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Incident IDs:", df["Incident ID"].duplicated().sum())

# 5. Check essential missing values
print("\n5. ESSENTIAL COLUMN MISSING VALUES")

essential_columns = [
    "Incident ID",
    "date",
    "year",
    "title",
    "description"
]

print(df[essential_columns].isnull().sum().to_string())

# 6. Inspect the first five records
print("\n6. FIRST FIVE RECORDS")
print(df.head().to_string(index=False))

# 7. Confirm taxonomy missing values
print("\n7. TAXONOMY MISSING VALUES")

taxonomy_columns = [
    "Risk Domain",
    "Risk Subdomain",
    "Harm Domain",
    "AI Harm Level"
]

print(df[taxonomy_columns].isnull().sum().to_string())

print("\nVerification completed.")
