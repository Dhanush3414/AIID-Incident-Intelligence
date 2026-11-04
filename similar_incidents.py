from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "incidents_feature_engineered.csv"
)


# --------------------------------------------------
# Load historical incident data
# --------------------------------------------------

def load_incidents():
    """Load historical AI incidents for similarity retrieval."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Incident dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE, low_memory=False)

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
            f"Missing required columns: {missing_columns}"
        )

    # Keep only records with a title or description.
    df = df.dropna(
        subset=["title", "description"],
        how="all"
    ).copy()

    df["title"] = df["title"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)

    # Combine title and description for text matching.
    df["combined_text"] = (
        df["title"].str.strip()
        + " "
        + df["description"].str.strip()
    ).str.strip()

    df = df[df["combined_text"].ne("")].copy()

    return df.reset_index(drop=True)


# --------------------------------------------------
# Build the text similarity index
# --------------------------------------------------

def build_similarity_index(df):
    """Convert historical incident text into TF-IDF vectors."""

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=10000,
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True,
    )

    incident_vectors = vectorizer.fit_transform(
        df["combined_text"]
    )

    return vectorizer, incident_vectors


# --------------------------------------------------
# Retrieve similar incidents
# --------------------------------------------------

def find_similar_incidents(
    title,
    description,
    df,
    vectorizer,
    incident_vectors,
    top_n=5,
):
    """Return historical incidents most similar to the input."""

    query = f"{title.strip()} {description.strip()}".strip()

    if not query:
        raise ValueError(
            "Enter an incident title or description."
        )

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        incident_vectors
    ).flatten()

    # Rank incidents by similarity, highest first.
    ranked_indices = similarities.argsort()[::-1]

    results = df.iloc[ranked_indices].copy()
    results["Similarity (%)"] = (
        similarities[ranked_indices] * 100
    ).round(2)

    # Return only the requested number of records.
    results = results.head(top_n)

    display_columns = [
        "Incident ID",
        "title",
        "description",
        "Risk Domain",
        "Similarity (%)",
    ]

    return results[display_columns].reset_index(drop=True)