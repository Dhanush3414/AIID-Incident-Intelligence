from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# 1. Load the feature-engineered dataset
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "processed"
    / "incidents_feature_engineered.csv"
)

df = pd.read_csv(input_file)

print("=" * 70)
print("RISK DOMAIN CLASSIFICATION TARGET ANALYSIS")
print("=" * 70)

# --------------------------------------------------
# 2. Select labelled incidents
# --------------------------------------------------

target_column = "Risk Domain"

labelled_df = df.dropna(subset=[target_column]).copy()

print("\n1. DATASET SUMMARY")
print("-" * 70)

print("Total incidents:", len(df))
print("Labelled incidents:", len(labelled_df))
print("Unlabelled incidents:", df[target_column].isna().sum())
print(
    "Label coverage:",
    round(len(labelled_df) / len(df) * 100, 2),
    "%"
)

# --------------------------------------------------
# 3. Count incidents in each Risk Domain
# --------------------------------------------------

class_counts = labelled_df[target_column].value_counts()

class_summary = pd.DataFrame({
    "Risk Domain": class_counts.index,
    "Incident Count": class_counts.values
})

class_summary["Percentage"] = (
    class_summary["Incident Count"]
    / len(labelled_df)
    * 100
)

print("\n2. CLASS DISTRIBUTION")
print("-" * 70)

print(
    class_summary.to_string(
        index=False,
        formatters={"Percentage": "{:.2f}%".format}
    )
)

# --------------------------------------------------
# 4. Identify classes with fewer examples
# --------------------------------------------------

print("\n3. CLASS BALANCE CHECK")
print("-" * 70)

print("Number of classes:", len(class_counts))
print("Largest class:", class_counts.max())
print("Smallest class:", class_counts.min())
print("Average records per class:", round(class_counts.mean(), 2))

print("\nClasses with fewer than 50 records:")

small_classes = class_counts[class_counts < 50]

if small_classes.empty:
    print("None")
else:
    print(small_classes.to_string())

# --------------------------------------------------
# 5. Visualize class distribution
# --------------------------------------------------

plt.figure(figsize=(12, 7))

sns.barplot(
    data=class_summary,
    x="Incident Count",
    y="Risk Domain"
)

plt.title("AI Incident Distribution by Risk Domain")
plt.xlabel("Number of Incidents")
plt.ylabel("Risk Domain")
plt.tight_layout()

# Save the plot
output_dir = project_root / "results" / "analysis"
output_dir.mkdir(parents=True, exist_ok=True)

plot_file = output_dir / "risk_domain_class_distribution.png"

plt.savefig(plot_file, dpi=300, bbox_inches="tight")
plt.show()

print("\n4. OUTPUT")
print("-" * 70)
print("Chart saved to:", plot_file)

print("\n" + "=" * 70)
print("CLASSIFICATION TARGET ANALYSIS COMPLETED")
print("=" * 70)