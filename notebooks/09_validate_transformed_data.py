import pandas as pd
from pathlib import Path

# Load final feature-engineered dataset
file_path = Path("data/processed/incidents_feature_engineered.csv")
df = pd.read_csv(file_path)

print("=" * 70)
print("FINAL DATA TRANSFORMATION VALIDATION")
print("=" * 70)

# 1. Dataset dimensions
print("\n1. DATASET DIMENSIONS")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Duplicate checks
print("\n2. DUPLICATE CHECKS")
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Incident IDs:", df["Incident ID"].duplicated().sum())

# 3. Missing values in essential columns
essential_columns = [
    "Incident ID",
    "date",
    "year",
    "title",
    "description"
]

print("\n3. ESSENTIAL COLUMN VALIDATION")

for column in essential_columns:
    print(f"{column}: {df[column].isna().sum()} missing values")

# 4. Verify newly engineered features
new_features = [
    "Incident_Date_Year",
    "Incident_Date_Month",
    "Incident_Date_Month_Name",
    "Incident_Date_Quarter",
    "Incident_Date_Day",
    "Incident_Date_Day_Name",
    "Has_Reports",
    "Has_Developer",
    "Has_Deployer",
    "Has_Harm_Information",
    "Incident_Age_Group"
]

print("\n4. NEW FEATURE VALIDATION")

for column in new_features:
    if column in df.columns:
        print(f"{column}: Present")
    else:
        print(f"{column}: MISSING")

# 5. Validate date and year consistency
df["date"] = pd.to_datetime(df["date"], errors="coerce")

year_mismatches = (
    df["year"] != df["date"].dt.year
).sum()

print("\n5. DATE CONSISTENCY")
print("Year/date mismatches:", year_mismatches)

# 6. Check report counts
print("\n6. REPORT COUNT VALIDATION")
print("Missing report counts:", df["report_count"].isna().sum())
print("Negative report counts:", (df["report_count"] < 0).sum())
print("Zero-report incidents:", (df["report_count"] == 0).sum())

print("\nValidation completed.")