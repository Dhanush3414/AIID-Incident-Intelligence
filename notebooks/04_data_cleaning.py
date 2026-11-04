import pandas as pd
from pathlib import Path

# Define file paths
input_path = Path("data/raw/AIID_Excel_Export-20261019.xlsx")
output_path = Path("data/processed/incidents_cleaned.csv")

# Create the processed-data directory if it does not exist
output_path.parent.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("AIID INCIDENT DATA CLEANING")
print("=" * 70)

# 1. Load the original Incidents sheet
df = pd.read_excel(
    input_path,
    sheet_name="Incidents",
    header=2
)

print("\n1. ORIGINAL DATASET")
print("Shape:", df.shape)

# 2. Remove completely empty rows and columns
df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")

print("\n2. AFTER REMOVING COMPLETELY EMPTY ROWS AND COLUMNS")
print("Shape:", df.shape)

# 3. Standardize column names
df.columns = df.columns.astype(str).str.strip()

# 4. Remove duplicate incident records using Incident ID
duplicate_ids = df["Incident ID"].duplicated().sum()

print("\n3. DUPLICATE INCIDENT IDs")
print("Duplicate IDs found:", duplicate_ids)

if duplicate_ids > 0:
    df = df.drop_duplicates(
        subset=["Incident ID"],
        keep="first"
    )

print("Shape after duplicate check:", df.shape)

# 5. Convert date column
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

print("\n4. DATE VALIDATION")
print("Missing dates after conversion:", df["date"].isna().sum())

# Stop if any dates unexpectedly become invalid
if df["date"].isna().any():
    raise ValueError(
        "Some dates could not be converted. Inspect them before proceeding."
    )

# 6. Validate essential columns
essential_columns = [
    "Incident ID",
    "date",
    "year",
    "title",
    "description"
]

print("\n5. ESSENTIAL COLUMN VALIDATION")

for column in essential_columns:
    missing_count = df[column].isna().sum()
    print(f"{column}: {missing_count} missing values")

# Stop if essential fields are missing
if df[essential_columns].isna().any().any():
    raise ValueError(
        "Essential columns contain missing values. Inspect before proceeding."
    )

# 7. Preserve missing taxonomy values
taxonomy_columns = [
    "Risk Domain",
    "Risk Subdomain",
    "Harm Domain",
    "AI Harm Level"
]

print("\n6. TAXONOMY MISSING VALUES")

for column in taxonomy_columns:
    print(f"{column}: {df[column].isna().sum()} missing values")

# 8. Save the cleaned dataset
df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\n7. CLEANED DATASET SAVED")
print("File:", output_path)
print("Final shape:", df.shape)

print("\nData cleaning completed successfully.")
print("Original Excel file remains unchanged.")
