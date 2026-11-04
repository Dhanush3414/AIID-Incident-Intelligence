from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

processed_dir = project_root / "data" / "processed"
output_dir = project_root / "models" / "tfidf"

output_dir.mkdir(parents=True, exist_ok=True)

train_file = processed_dir / "classification_train.csv"
test_file = processed_dir / "classification_test.csv"

# --------------------------------------------------
# 2. Load training and testing datasets
# --------------------------------------------------

train_df = pd.read_csv(train_file)
test_df = pd.read_csv(test_file)

X_train = train_df["text"].fillna("").astype(str)
X_test = test_df["text"].fillna("").astype(str)

print("=" * 70)
print("TF-IDF TEXT VECTORIZATION")
print("=" * 70)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# --------------------------------------------------
# 3. Initialize TF-IDF
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=10000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True
)

# Fit only on training data
X_train_tfidf = vectorizer.fit_transform(X_train)

# Transform testing data without fitting again
X_test_tfidf = vectorizer.transform(X_test)

# --------------------------------------------------
# 4. Inspect the resulting matrices
# --------------------------------------------------

print("\nTF-IDF RESULTS")
print("-" * 70)

print("Training matrix shape:", X_train_tfidf.shape)
print("Testing matrix shape:", X_test_tfidf.shape)

print("Vocabulary size:", len(vectorizer.vocabulary_))

print(
    "Training matrix non-zero values:",
    X_train_tfidf.nnz
)

print(
    "Testing matrix non-zero values:",
    X_test_tfidf.nnz
)

# --------------------------------------------------
# 5. Save the TF-IDF matrices
# --------------------------------------------------

save_npz(
    output_dir / "X_train_tfidf.npz",
    X_train_tfidf
)

save_npz(
    output_dir / "X_test_tfidf.npz",
    X_test_tfidf
)

# --------------------------------------------------
# 6. Save the vocabulary
# --------------------------------------------------

vocabulary_df = pd.DataFrame(
    sorted(
        vectorizer.vocabulary_.items(),
        key=lambda item: item[1]
    ),
    columns=["Term", "Feature_Index"]
)

vocabulary_df.to_csv(
    output_dir / "tfidf_vocabulary.csv",
    index=False,
    encoding="utf-8-sig"
)

# --------------------------------------------------
# 7. Save the fitted vectorizer
# --------------------------------------------------

import joblib

joblib.dump(
    vectorizer,
    output_dir / "tfidf_vectorizer.joblib"
)

print("\nSAVED FILES")
print("-" * 70)

print("Training matrix: X_train_tfidf.npz")
print("Testing matrix: X_test_tfidf.npz")
print("Vocabulary: tfidf_vocabulary.csv")
print("Fitted vectorizer: tfidf_vectorizer.joblib")

print("\n" + "=" * 70)
print("TF-IDF VECTORIZATION COMPLETED")
print("=" * 70)