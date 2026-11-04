from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "processed"
    / "incidents_feature_engineered.csv"
)

df = pd.read_csv(input_file)

print("=" * 70)
print("AIID ANALYSIS READINESS CHECK")
print("=" * 70)

# 1. Dataset dimensions
print("\n1. DATASET OVERVIEW")
print("-" * 70)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Unique Incident IDs:", df["Incident ID"].nunique())

# 2. Check important analysis fields
analysis_columns = [
    "Incident ID",
    "date",
    "year",
    "title",
    "description",
    "report_count",
    "Risk Domain",
    "Risk Subdomain",
    "Responsible Entity",
    "Intent",
    "Timing",
    "AI Harm Level",
    "Location Region",
    "deployer",
    "developer",
]

print("\n2. ANALYSIS FIELD AVAILABILITY")
print("-" * 70)

for column in analysis_columns:
    if column in df.columns:
        missing = df[column].isna().sum()
        available = len(df) - missing
        percentage = available / len(df) * 100

        print(
            f"{column}: "
            f"{available}/{len(df)} available "
            f"({percentage:.2f}%)"
        )
    else:
        print(f"{column}: NOT FOUND")

# 3. Evaluate candidate classification targets
print("\n3. CANDIDATE CLASSIFICATION TARGETS")
print("-" * 70)

candidate_targets = [
    "Risk Domain",
    "Risk Subdomain",
    "Responsible Entity",
    "Intent",
    "Timing",
    "AI Harm Level",
]

for column in candidate_targets:
    if column in df.columns:
        valid = df[column].notna().sum()
        unique = df[column].nunique()

        print(
            f"{column}: "
            f"{valid} labelled records, "
            f"{unique} distinct non-missing classes"
        )

# 4. Check class balance for selected targets
print("\n4. CLASS DISTRIBUTIONS")
print("-" * 70)

for column in ["Risk Domain", "Intent", "Timing"]:
    if column in df.columns:
        print(f"\n{column}:")

        print(
            df[column]
            .fillna("Unclassified")
            .value_counts()
            .head(10)
            .to_string()
        )

# 5. Check whether text fields are available
print("\n5. TEXT FIELD READINESS")
print("-" * 70)

for column in ["title", "description"]:
    if column in df.columns:
        lengths = df[column].fillna("").astype(str).str.len()

        print(f"\n{column}")
        print("Empty records:", (lengths == 0).sum())
        print("Average character length:", round(lengths.mean(), 2))
        print("Median character length:", round(lengths.median(), 2))

# 6. Final checks
print("\n6. FINAL VALIDATION")
print("-" * 70)

print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Incident IDs:", df["Incident ID"].duplicated().sum())
print("Missing titles:", df["title"].isna().sum())
print("Missing descriptions:", df["description"].isna().sum())

print("\n" + "=" * 70)
print("ANALYSIS READINESS CHECK COMPLETED")
print("=" * 70)