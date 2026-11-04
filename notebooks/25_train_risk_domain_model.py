from pathlib import Path

import joblib
import pandas as pd

from scipy.sparse import load_npz
from sklearn.linear_model import LogisticRegression

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

processed_dir = project_root / "data" / "processed"
tfidf_dir = project_root / "models" / "tfidf"
model_dir = project_root / "models" / "classification"

model_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load labels and TF-IDF matrices
# --------------------------------------------------

train_df = pd.read_csv(
    processed_dir / "classification_train.csv"
)

X_train_tfidf = load_npz(
    tfidf_dir / "X_train_tfidf.npz"
)

y_train = train_df["Risk Domain"]

print("=" * 70)
print("AI INCIDENT RISK DOMAIN CLASSIFICATION")
print("=" * 70)

print("\nTraining records:", len(y_train))
print("Number of TF-IDF features:", X_train_tfidf.shape[1])
print("Number of classes:", y_train.nunique())

# --------------------------------------------------
# 3. Initialize Logistic Regression
# --------------------------------------------------

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)

# --------------------------------------------------
# 4. Train the model
# --------------------------------------------------

print("\nTraining Logistic Regression model...")

model.fit(
    X_train_tfidf,
    y_train
)

print("Model training completed successfully.")

# --------------------------------------------------
# 5. Display learned classes
# --------------------------------------------------

print("\nRisk Domain classes learned:")
for index, risk_domain in enumerate(model.classes_, start=1):
    print(f"{index}. {risk_domain}")

# --------------------------------------------------
# 6. Save the trained model
# --------------------------------------------------

model_file = model_dir / "risk_domain_classifier.joblib"

joblib.dump(
    model,
    model_file
)

print("\nModel saved to:")
print(model_file)

print("\n" + "=" * 70)
print("MODEL TRAINING COMPLETED")
print("=" * 70)