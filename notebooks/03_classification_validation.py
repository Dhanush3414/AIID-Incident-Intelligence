import pandas as pd
from pathlib import Path

file_path = Path("data/raw/AIID_Excel_Export-20261019.xlsx")

# Load the Incidents sheet
df = pd.read_excel(
    file_path,
    sheet_name="Incidents",
    header=2
)

print("=" * 70)
print("AIID CLASSIFICATION VALIDATION")
print("=" * 70)

# 1. Inspect Data Sources
print("\n1. DATA SOURCES DISTRIBUTION")
print(df["Data Sources"].value_counts(dropna=False).to_string())

# 2. Check Risk Domain availability by Data Sources
print("\n2. RISK DOMAIN MISSING VALUES BY DATA SOURCE")

risk_missing = (
    df.groupby("Data Sources", dropna=False)["Risk Domain"]
    .agg(
        Total="size",
        Missing=lambda s: s.isna().sum(),
        Available=lambda s: s.notna().sum()
    )
)

risk_missing["Missing Percentage"] = (
    risk_missing["Missing"] / risk_missing["Total"] * 100
).round(2)

print(risk_missing.to_string())

# 3. Check Harm Domain availability by Data Sources
print("\n3. HARM DOMAIN MISSING VALUES BY DATA SOURCE")

harm_missing = (
    df.groupby("Data Sources", dropna=False)["Harm Domain"]
    .agg(
        Total="size",
        Missing=lambda s: s.isna().sum(),
        Available=lambda s: s.notna().sum()
    )
)

harm_missing["Missing Percentage"] = (
    harm_missing["Missing"] / harm_missing["Total"] * 100
).round(2)

print(harm_missing.to_string())

# 4. Check whether Year matches the date
print("\n4. YEAR CONSISTENCY CHECK")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = pd.to_numeric(df["year"], errors="coerce")

derived_year = df["date"].dt.year

mismatch = (
    df["year"].notna()
    & derived_year.notna()
    & (df["year"] != derived_year)
)

print("Missing dates:", df["date"].isna().sum())
print("Missing year values:", df["year"].isna().sum())
print("Year/date mismatches:", mismatch.sum())

if mismatch.any():
    print("\nExamples of mismatched records:")
    print(
        df.loc[mismatch, ["Incident ID", "date", "year", "title"]]
        .head(10)
        .to_string(index=False)
    )

# 5. Validate report counts
print("\n5. REPORT COUNT VALIDATION")

df["report_count"] = pd.to_numeric(
    df["report_count"],
    errors="coerce"
)

print("Missing report counts:", df["report_count"].isna().sum())
print("Negative report counts:", (df["report_count"] < 0).sum())
print("Zero report counts:", (df["report_count"] == 0).sum())

print("\nValidation complete. No data has been modified.")

# 6. Inspect incident with zero report count

print("\n6. INCIDENT WITH ZERO REPORTS")

zero_reports = df[df["report_count"] == 0]

if not zero_reports.empty:
    columns_to_display = [
        "Incident ID",
        "date",
        "year",
        "title",
        "deployer",
        "developer",
        "report_count"
    ]

    print(
        zero_reports[columns_to_display].to_string(index=False)
    )
else:
    print("No incidents with zero reports found.")

