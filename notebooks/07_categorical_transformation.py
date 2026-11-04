
import pandas as pd
import ast
from pathlib import Path

# Load transformed dataset
file_path = Path("data/processed/incidents_transformed.csv")
df = pd.read_csv(file_path)

print("=" * 70)
print("AIID DATA TRANSFORMATION - LIST CONVERSION")
print("=" * 70)

# Columns containing list-like values
list_columns = [
    "Sector of Deployment",
    "Infrastructure Sectors",
    "AI Goal",
    "AI Technology",
    "AI Technology (Potential)",
    "Technical Failure",
    "Technical Failure (Potential)",
    "AI Task",
    "AI Methods",
    "Data Inputs"
]

# Safely convert string representations of lists
def convert_to_list(value):
    if pd.isna(value):
        return None

    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)

            if isinstance(parsed, list):
                return parsed

        except (ValueError, SyntaxError):
            pass

    return value


# Create new columns without changing the original columns
for column in list_columns:
    if column in df.columns:
        new_column = column + "_List"
        df[new_column] = df[column].apply(convert_to_list)

print("\n1. TRANSFORMATION RESULTS")

for column in list_columns:
    new_column = column + "_List"

    if new_column in df.columns:
        print(f"\n{new_column}")
        print("Non-missing values:", df[new_column].notna().sum())
        print("Sample values:")
        print(df[new_column].dropna().head(3).to_string(index=False))

# Check empty lists separately
print("\n2. EMPTY LIST COUNTS")

for column in list_columns:
    new_column = column + "_List"

    if new_column in df.columns:
        empty_count = df[new_column].apply(
            lambda value: isinstance(value, list) and len(value) == 0
        ).sum()

        print(f"{new_column}: {empty_count}")

# Save the transformed dataset
output_path = Path("data/processed/incidents_transformed.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n3. DATASET SAVED")
print("File:", output_path)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nList conversion completed successfully.")