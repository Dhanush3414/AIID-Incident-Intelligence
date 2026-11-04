from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "processed"
    / "classification_dataset.csv"
)

output_dir = project_root / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load the prepared dataset
# --------------------------------------------------

df = pd.read_csv(input_file)

print("=" * 70)
print("AI INCIDENT CLASSIFICATION: TRAIN-TEST SPLIT")
print("=" * 70)

print("\nOriginal dataset shape:", df.shape)

# --------------------------------------------------
# 3. Define features and target
# --------------------------------------------------

X = df["text"]
y = df["Risk Domain"]

print("\nTotal labelled incidents:", len(df))
print("Number of Risk Domain classes:", y.nunique())

# --------------------------------------------------
# 4. Split into training and testing sets
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTRAINING SET")
print("-" * 70)
print("Training records:", len(X_train))

print("\nTESTING SET")
print("-" * 70)
print("Testing records:", len(X_test))

# --------------------------------------------------
# 5. Check class distribution
# --------------------------------------------------

print("\nTRAINING CLASS DISTRIBUTION")
print("-" * 70)
print(y_train.value_counts().sort_index().to_string())

print("\nTESTING CLASS DISTRIBUTION")
print("-" * 70)
print(y_test.value_counts().sort_index().to_string())

# --------------------------------------------------
# 6. Save the split datasets
# --------------------------------------------------

train_df = df.loc[X_train.index].copy()
test_df = df.loc[X_test.index].copy()

train_file = output_dir / "classification_train.csv"
test_file = output_dir / "classification_test.csv"

train_df.to_csv(
    train_file,
    index=False,
    encoding="utf-8-sig"
)

test_df.to_csv(
    test_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nSAVED FILES")
print("-" * 70)
print("Training data:", train_file)
print("Testing data:", test_file)

# --------------------------------------------------
# 7. Validate the split
# --------------------------------------------------

assert len(train_df) + len(test_df) == len(df)
assert set(train_df["Incident ID"]).isdisjoint(
    set(test_df["Incident ID"])
)

print("\nValidation passed:")
print("- No incident IDs overlap between training and testing sets.")
print("- All labelled records are accounted for.")

print("\n" + "=" * 70)
print("TRAIN-TEST SPLIT COMPLETED")
print("=" * 70)