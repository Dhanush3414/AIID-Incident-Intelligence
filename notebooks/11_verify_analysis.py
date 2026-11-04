import pandas as pd
from pathlib import Path

# Load cleaned dataset
file_path = Path("data/processed/incidents_cleaned.csv")
df = pd.read_csv(file_path)

print("=" * 70)
print("AI INCIDENT INTELLIGENCE - ANALYSIS VALIDATION")
print("=" * 70)

# 1. Total records
print("\n1. TOTAL INCIDENTS")
print("Total records:", len(df))
print("Unique Incident IDs:", df["Incident ID"].nunique())

# 2. Validate yearly incident counts
print("\n2. YEARLY INCIDENT COUNT VALIDATION")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

yearly_counts = (
    df.dropna(subset=["date"])
      .groupby(df["date"].dt.year)
      .size()
      .sort_index()
)

print(yearly_counts.to_string())
print("\nTotal incidents included in yearly counts:", yearly_counts.sum())

# 3. Validate risk-domain counts
print("\n3. RISK DOMAIN VALIDATION")

print(
    df["Risk Domain"]
      .value_counts(dropna=False)
      .to_string()
)

# 4. Validate risk-subdomain counts
print("\n4. TOP 10 RISK SUBDOMAINS")

print(
    df["Risk Subdomain"]
      .value_counts()
      .head(10)
      .to_string()
)

# 5. Validate monthly counts
print("\n5. MONTHLY DISTRIBUTION")

monthly_counts = (
    df.dropna(subset=["date"])
      .groupby(df["date"].dt.month)
      .size()
      .reindex(range(1, 13), fill_value=0)
)

monthly_counts.index = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

print(monthly_counts.to_string())

# 6. Check missing values in analysis columns
print("\n6. MISSING VALUES IN KEY ANALYSIS COLUMNS")

analysis_columns = [
    "Risk Domain",
    "Risk Subdomain",
    "Responsible Entity",
    "Intent",
    "Timing",
    "AI Harm Level",
    "Location Region",
    "developer"
]

print(df[analysis_columns].isnull().sum().to_string())

print("\nAnalysis validation completed.")