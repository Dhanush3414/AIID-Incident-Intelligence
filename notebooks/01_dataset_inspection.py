import pandas as pd
from pathlib import Path

file_path = Path("data/raw/AIID_Excel_Export-20261019.xlsx")

# Load the main incident sheet
df = pd.read_excel(
    file_path,
    sheet_name="Incidents",
    header=2
)

# Remove completely empty rows and columns
df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")

print("=" * 70)
print("AIID MISSING-VALUE PATTERN ANALYSIS")
print("=" * 70)

# 1. Check missing values in important columns
important_columns = [
    "Incident ID",
    "date",
    "title",
    "description",
    "Risk Domain",
    "Risk Subdomain",
    "Harm Domain",
    "AI Harm Level",
    "AI Technology",
    "Technical Failure",
    "AI System Description",
    "Lives Lost",
    "Injuries"
]

print("\n1. MISSING VALUES IN IMPORTANT COLUMNS")

for column in important_columns:
    if column in df.columns:
        missing = df[column].isna().sum()
        percentage = df[column].isna().mean() * 100

        print(
            f"{column}: {missing} missing "
            f"({percentage:.2f}%)"
        )

# 2. Check whether important taxonomy fields are missing together
taxonomy_columns = [
    "Risk Domain",
    "Risk Subdomain",
    "Harm Domain",
    "AI Harm Level"
]

print("\n2. COMBINED TAXONOMY MISSINGNESS")

available_taxonomy = [
    column for column in taxonomy_columns
    if column in df.columns
]

all_missing = df[available_taxonomy].isna().all(axis=1)
all_present = df[available_taxonomy].notna().all(axis=1)

print("All selected taxonomy fields missing:", all_missing.sum())
print("All selected taxonomy fields present:", all_present.sum())
print("Partially populated taxonomy records:",
      len(df) - all_missing.sum() - all_present.sum())

# 3. Compare records with and without Risk Domain
print("\n3. RECORDS WITH RISK DOMAIN")

risk_present = df[df["Risk Domain"].notna()]
risk_missing = df[df["Risk Domain"].isna()]

print("Records with Risk Domain:", len(risk_present))
print("Records without Risk Domain:", len(risk_missing))

print("\nExamples with Risk Domain:")
print(
    risk_present[
        ["Incident ID", "title", "Risk Domain", "Risk Subdomain"]
    ].head(5).to_string(index=False)
)

print("\nExamples without Risk Domain:")
print(
    risk_missing[
        ["Incident ID", "title", "Risk Domain", "Risk Subdomain"]
    ].head(5).to_string(index=False)
)

# 4. Examine the year distribution
print("\n4. YEAR DISTRIBUTION")

print(
    df["year"]
    .value_counts(dropna=False)
    .sort_index()
    .tail(15)
    .to_string()
)

# 5. Check whether dates are valid
print("\n5. DATE VALIDITY")

print("Missing dates:", df["date"].isna().sum())
print("Invalid dates:", pd.to_datetime(df["date"], errors="coerce").isna().sum())

print("\nAnalysis complete. No data has been modified or saved.")