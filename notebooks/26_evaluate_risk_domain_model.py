from pathlib import Path

import joblib
import pandas as pd

from scipy.sparse import load_npz
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

# Project paths
project_root = Path(__file__).resolve().parent.parent

processed_dir = project_root / "data" / "processed"
tfidf_dir = project_root / "models" / "tfidf"
model_dir = project_root / "models" / "classification"
results_dir = project_root / "results" / "analysis"

results_dir.mkdir(parents=True, exist_ok=True)

# Load test dataset
test_df = pd.read_csv(
    processed_dir / "classification_test.csv"
)

# Load TF-IDF test matrix
X_test_tfidf = load_npz(
    tfidf_dir / "X_test_tfidf.npz"
)

# Load trained model
model = joblib.load(
    model_dir / "risk_domain_classifier.joblib"
)

# Actual and predicted labels
y_test = test_df["Risk Domain"]

y_pred = model.predict(X_test_tfidf)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)

precision_weighted = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall_weighted = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1_weighted = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1_macro = f1_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

# Display results
print("=" * 70)
print("AI INCIDENT RISK DOMAIN MODEL EVALUATION")
print("=" * 70)

print("\nTest records:", len(y_test))

print("\nOVERALL EVALUATION METRICS")
print("-" * 40)

print(f"Accuracy:           {accuracy:.4f}")
print(f"Weighted Precision: {precision_weighted:.4f}")
print(f"Weighted Recall:    {recall_weighted:.4f}")
print(f"Weighted F1-score:  {f1_weighted:.4f}")
print(f"Macro F1-score:     {f1_macro:.4f}")

print("\nCLASSIFICATION REPORT")
print("-" * 70)

report = classification_report(
    y_test,
    y_pred,
    zero_division=0
)

print(report)

# Save classification report
report_dict = classification_report(
    y_test,
    y_pred,
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report_dict).transpose()

report_df.to_csv(
    results_dir / "risk_domain_classification_report.csv",
    index=True
)

# Generate confusion matrix
labels = model.classes_

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

cm_df.index.name = "Actual Risk Domain"
cm_df.columns.name = "Predicted Risk Domain"

cm_df.to_csv(
    results_dir / "risk_domain_confusion_matrix.csv"
)

# Save overall metrics
metrics_df = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Weighted Precision",
        "Weighted Recall",
        "Weighted F1-score",
        "Macro F1-score"
    ],
    "Score": [
        accuracy,
        precision_weighted,
        recall_weighted,
        f1_weighted,
        f1_macro
    ]
})

metrics_df.to_csv(
    results_dir / "risk_domain_evaluation_metrics.csv",
    index=False
)

print("\nCONFUSION MATRIX")
print("-" * 70)
print(cm_df)

print("\nEvaluation results saved to:")
print(results_dir / "risk_domain_classification_report.csv")
print(results_dir / "risk_domain_confusion_matrix.csv")
print(results_dir / "risk_domain_evaluation_metrics.csv")

print("\n" + "=" * 70)
print("MODEL EVALUATION COMPLETED")
print("=" * 70)