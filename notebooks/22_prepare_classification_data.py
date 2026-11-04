from pathlib import Path

import pandas as pd

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "processed"
    / "incidents_feature_engineered.csv"
)

output_dir = project_root / "data" / "processed"
output_file = output_dir / "classification_dataset.csv"

output_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load the dataset
# --------------------------------------------------

df = pd.read_csv(input_file)

print("=" * 70)
print("CLASSIFICATION DATA PREPARATION")
print("=" * 70)

print("\nOriginal dataset shape:", df.shape)

# --------------------------------------------------
# 3. Select required columns
# --------------------------------------------------

required_columns = [
    "Incident ID",
    "title",
    "description",
    "Risk Domain",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns are missing: {missing_columns}"
    )

classification_df = df[required_columns].copy()

# --------------------------------------------------
# 4. Remove records without target labels
# --------------------------------------------------

original_count = len(classification_df)

classification_df = classification_df.dropna(
    subset=["Risk Domain"]
).copy()

print("\nRecords before removing unlabelled targets:", original_count)
print("Records after removing unlabelled targets:", len(classification_df))
print("Unlabelled records excluded:", original_count - len(classification_df))

# --------------------------------------------------
# 5. Handle missing text fields
# --------------------------------------------------

classification_df["title"] = (
    classification_df["title"]
    .fillna("")
    .astype(str)
    .str.strip()
)

classification_df["description"] = (
    classification_df["description"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Combine title and description into one text feature
classification_df["text"] = (
    classification_df["title"]
    + " "
    + classification_df["description"]
).str.strip()

# Remove records with no usable text
before_text_filter = len(classification_df)

classification_df = classification_df[
    classification_df["text"].str.len() > 0
].copy()

print(
    "Records removed due to empty text:",
    before_text_filter - len(classification_df)
)

# --------------------------------------------------
# 6. Validate target labels
# --------------------------------------------------

print("\nRisk Domain class counts:")
print(
    classification_df["Risk Domain"]
    .value_counts()
    .to_string()
)

print(
    "\nNumber of classes:",
    classification_df["Risk Domain"].nunique()
)

# --------------------------------------------------
# 7. Check duplicates
# --------------------------------------------------

print("\nDuplicate Incident IDs:", classification_df["Incident ID"].duplicated().sum())
print("Duplicate text-target pairs:", classification_df.duplicated(subset=["text", "Risk Domain"]).sum())

if classification_df["Incident ID"].duplicated().any():
    raise ValueError("Duplicate Incident IDs detected.")

if classification_df["Risk Domain"].isna().any():
    raise ValueError("Missing target labels remain.")

if (classification_df["text"].str.len() == 0).any():
    raise ValueError("Empty text records remain.")

# --------------------------------------------------
# 8. Save the prepared dataset
# --------------------------------------------------

classification_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nPrepared dataset saved to:")
print(output_file)

print("Final dataset shape:", classification_df.shape)

print("\n" + "=" * 70)
print("CLASSIFICATION DATA PREPARATION COMPLETED")
print("=" * 70)