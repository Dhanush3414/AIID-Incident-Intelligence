import pandas as pd
from pathlib import Path

# Load cleaned dataset
file_path = Path("data/processed/incidents_cleaned.csv")
df = pd.read_csv(file_path)

print("=" * 70)
print("AIID DATA TRANSFORMATION - DATE FEATURES")
print("=" * 70)

# 1. Convert date columns to datetime
date_columns = ["date", "Date Modified"]

for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

print("\n1. DATE CONVERSION")
for column in date_columns:
    if column in df.columns:
        print(f"\n{column}")
        print("Data type:", df[column].dtype)
        print("Missing values:", df[column].isna().sum())

# 2. Verify year against the main incident date
df["date_year_check"] = df["date"].dt.year

year_mismatches = (
    df["year"] != df["date_year_check"]
).sum()

print("\n2. YEAR VALIDATION")
print("Year/date mismatches:", year_mismatches)

# 3. Create new date-based features
df["Incident_Date_Year"] = df["date"].dt.year
df["Incident_Date_Month"] = df["date"].dt.month
df["Incident_Date_Month_Name"] = df["date"].dt.month_name()
df["Incident_Date_Quarter"] = df["date"].dt.quarter
df["Incident_Date_Day"] = df["date"].dt.day
df["Incident_Date_Day_Name"] = df["date"].dt.day_name()

print("\n3. NEW DATE FEATURES")
new_columns = [
    "Incident_Date_Year",
    "Incident_Date_Month",
    "Incident_Date_Month_Name",
    "Incident_Date_Quarter",
    "Incident_Date_Day",
    "Incident_Date_Day_Name"
]

print(df[new_columns].head(10).to_string(index=False))

# 4. Check the distribution of incidents by year
print("\n4. INCIDENTS BY YEAR")
print(
    df["Incident_Date_Year"]
    .value_counts()
    .sort_index()
    .to_string()
)

# 5. Check the distribution of incidents by month
print("\n5. INCIDENTS BY MONTH")
print(
    df["Incident_Date_Month_Name"]
    .value_counts()
    .to_string()
)

# 6. Save the transformed dataset separately
output_path = Path("data/processed/incidents_transformed.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n6. TRANSFORMED DATASET SAVED")
print("File:", output_path)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("\nDate transformation completed successfully.")