from pathlib import Path

import joblib
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

model_dir = project_root / "models" / "classification"
tfidf_dir = project_root / "models" / "tfidf"

# Load the trained model and TF-IDF vectorizer
model = joblib.load(
    model_dir / "risk_domain_classifier.joblib"
)

vectorizer = joblib.load(
    tfidf_dir / "tfidf_vectorizer.joblib"
)


def predict_risk_domain(title, description):
    """
    Predict the Risk Domain of a new AI incident.
    """

    title = str(title).strip()
    description = str(description).strip()

    if not title and not description:
        raise ValueError(
            "Please provide an incident title or description."
        )

    incident_text = title + " " + description

    # Convert text using the existing TF-IDF vectorizer
    text_vector = vectorizer.transform([incident_text])

    # Predict Risk Domain
    predicted_domain = model.predict(text_vector)[0]

    # Get model confidence scores
    probabilities = model.predict_proba(text_vector)[0]

    confidence = max(probabilities) * 100

    return predicted_domain, confidence


if __name__ == "__main__":

    print("=" * 65)
    print("AI INCIDENT INTELLIGENCE")
    print("Risk Domain Prediction")
    print("=" * 65)

    title = input("\nEnter incident title: ").strip()

    description = input(
        "Enter incident description: "
    ).strip()

    try:
        predicted_domain, confidence = predict_risk_domain(
            title,
            description
        )

        print("\n" + "=" * 65)
        print("PREDICTION RESULT")
        print("=" * 65)

        print("\nIncident Title:", title)

        print("\nPredicted Risk Domain:")
        print(predicted_domain)

        print(
            f"\nModel confidence score: {confidence:.2f}%"
        )

        print("\n" + "=" * 65)

    except ValueError as error:
        print("\nError:", error)