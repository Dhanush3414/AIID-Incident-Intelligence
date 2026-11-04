from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Project paths
project_root = Path(__file__).resolve().parent.parent

results_dir = project_root / "results" / "analysis"
figures_dir = project_root / "results" / "figures"

figures_dir.mkdir(parents=True, exist_ok=True)

# Load saved evaluation results
metrics_df = pd.read_csv(
    results_dir / "risk_domain_evaluation_metrics.csv"
)

report_df = pd.read_csv(
    results_dir / "risk_domain_classification_report.csv",
    index_col=0
)

cm_df = pd.read_csv(
    results_dir / "risk_domain_confusion_matrix.csv",
    index_col=0
)

# --------------------------------------------------
# 1. CONFUSION MATRIX HEATMAP
# --------------------------------------------------

plt.figure(figsize=(14, 10))

sns.heatmap(
    cm_df,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Risk Domain Classification - Confusion Matrix")
plt.xlabel("Predicted Risk Domain")
plt.ylabel("Actual Risk Domain")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig(
    figures_dir / "risk_domain_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# --------------------------------------------------
# 2. F1-SCORE BY RISK DOMAIN
# --------------------------------------------------

class_report = report_df.loc[
    report_df.index.isin([
        "AI system safety, failures, and limitations",
        "Discrimination and Toxicity",
        "Human-Computer Interaction",
        "Malicious Actors & Misuse",
        "Misinformation",
        "Privacy & Security",
        "Socioeconomic & Environmental Harms"
    ])
].copy()

class_report = class_report.sort_values("f1-score")

plt.figure(figsize=(12, 7))

sns.barplot(
    data=class_report.reset_index(),
    x="f1-score",
    y="index"
)

plt.title("F1-Score by Risk Domain")
plt.xlabel("F1-score")
plt.ylabel("Risk Domain")
plt.xlim(0, 1)
plt.tight_layout()

plt.savefig(
    figures_dir / "risk_domain_f1_scores.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# --------------------------------------------------
# 3. OVERALL EVALUATION METRICS
# --------------------------------------------------

plt.figure(figsize=(10, 6))

sns.barplot(
    data=metrics_df,
    x="Metric",
    y="Score"
)

plt.title("Overall Risk Domain Model Performance")
plt.xlabel("Evaluation Metric")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(
    figures_dir / "overall_model_metrics.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("=" * 70)
print("MODEL PERFORMANCE VISUALIZATION COMPLETED")
print("=" * 70)

print("\nVisualizations saved to:")
print(figures_dir)

for image_file in sorted(figures_dir.glob("*.png")):
    print(image_file.name)