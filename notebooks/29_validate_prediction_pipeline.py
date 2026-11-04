from pathlib import Path

import joblib
import pandas as pd

# Project paths
project_root = Path(__file__).resolve().parent.parent

model_dir = project_root / "models" / "classification"
tfidf_dir = project_root / "models" / "tfidf"

# Load saved model and vectorizer
model = joblib.load(
    model_dir / "risk_domain_classifier.joblib"
)

vectorizer = joblib.load(
    tfidf_dir / "tfidf_vectorizer.joblib"
)


def predict_risk_domain(title, description):
    """Predict the Risk Domain of an AI incident."""

    title = str(title).strip()
    description = str(description).strip()

    if not title and not description:
        raise ValueError(
            "Incident title and description cannot both be empty."
        )

    incident_text = f"{title} {description}"

    text_vector = vectorizer.transform([incident_text])

    predicted_domain = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]

    confidence = max(probabilities) * 100

    return predicted_domain, confidence


# Sample incidents for pipeline testing
test_incidents = [
    {
        "title": "AI chatbot spreads false information",
        "description": (
            "A chatbot generates inaccurate information "
            "in response to user questions."
        )
    },
    {
        "title": "AI system discriminates against applicants",
        "description": (
            "An automated hiring system unfairly rejects "
            "qualified candidates from a particular group."
        )
    },
    {
        "title": "AI voice cloning used for financial fraud",
        "description": (
            "Criminals use synthetic audio to impersonate "
            "a company executive and request money transfers."
        )
    },
    {
        "title": "Facial recognition produces incorrect matches",
        "description": (
            "A facial recognition system incorrectly identifies "
            "individuals, causing problems for affected people."
        )
    },
    {
        "title": "AI system exposes private user information",
        "description": (
            "An AI application reveals confidential personal "
            "information in responses to unrelated users."
        )
    }
]

valid_domains = set(model.classes_)

results = []

print("=" * 75)
print("AI INCIDENT INTELLIGENCE - PIPELINE VALIDATION")
print("=" * 75)

for index, incident in enumerate(test_incidents, start=1):

    try:
        predicted_domain, confidence = predict_risk_domain(
            incident["title"],
            incident["description"]
        )

        is_valid = predicted_domain in valid_domains

        results.append({
            "Test_ID": index,
            "Title": incident["title"],
            "Predicted_Risk_Domain": predicted_domain,
            "Confidence_Percent": round(confidence, 2),
            "Valid_Prediction": is_valid
        })

        print(f"\nTest {index}")
        print("-" * 50)
        print("Title:", incident["title"])
        print("Predicted Domain:", predicted_domain)
        print(f"Confidence: {confidence:.2f}%")
        print("Valid Prediction:", is_valid)

    except Exception as error:
        print(f"\nTest {index} failed: {error}")

# Save validation results
results_dir = project_root / "results" / "analysis"
results_dir.mkdir(parents=True, exist_ok=True)

results_df = pd.DataFrame(results)

output_file = results_dir / "prediction_pipeline_validation.csv"

results_df.to_csv(output_file, index=False)

print("\n" + "=" * 75)
print("PIPELINE VALIDATION SUMMARY")
print("=" * 75)

print("Total test cases:", len(test_incidents))
print("Successful predictions:", len(results_df))
print(
    "Valid domain predictions:",
    int(results_df["Valid_Prediction"].sum())
    if not results_df.empty else 0
)

print("\nResults saved to:")
print(output_file)

print("\nVALIDATION COMPLETED")