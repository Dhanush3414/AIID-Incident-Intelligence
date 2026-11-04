import pandas as pd
from pathlib import Path

# Load the transformed dataset
file_path = Path("data/processed/incidents_transformed.csv")
df = pd.read_csv(file_path)

print("=" * 70)
print("AIID FEATURE ENGINEERING")
print("=" * 70)

# 1. Create report availability feature
df["Has_Reports"] = df["report_count"] > 0

# 2. Create developer and deployer availability features
df["Has_Developer"] = (
    df["developer"].notna()
    & df["developer"].astype(str).str.strip().ne("")
)

df["Has_Deployer"] = (
    df["deployer"].notna()
    & df["deployer"].astype(str).str.strip().ne("")
)

# 3. Create harm information availability feature
df["Has_Harm_Information"] = (
    df["Lives Lost"].notna()
    | df["Injuries"].notna()
)

# 4. Create incident age group from the main date field
df["date"] = pd.to_datetime(df["date"], errors="coerce")

df["Incident_Age_Group"] = pd.cut(
    df["date"].dt.year,
    bins=[-float("inf"), 2010, 2015, 2020, 2023, float("inf")],
    labels=[
        "Before 2011",
        "2011-2015",
        "2016-2020",
        "2021-2023",
        "2024 onwards"
    ]
)

# 5. Display feature summaries
print("\n1. REPORT AVAILABILITY")
print(df["Has_Reports"].value_counts(dropna=False).to_string())

print("\n2. DEVELOPER AVAILABILITY")
print(df["Has_Developer"].value_counts(dropna=False).to_string())

print("\n3. DEPLOYER AVAILABILITY")
print(df["Has_Deployer"].value_counts(dropna=False).to_string())

print("\n4. HARM INFORMATION AVAILABILITY")
print(df["Has_Harm_Information"].value_counts(dropna=False).to_string())

print("\n5. INCIDENT AGE GROUP")
print(df["Incident_Age_Group"].value_counts(sort=False, dropna=False).to_string())

# 6. Save the feature-engineered dataset separately
output_path = Path("data/processed/incidents_feature_engineered.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n6. OUTPUT")
print("File:", output_path)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nFeature engineering completed successfully.")