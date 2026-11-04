
import ollama
import faiss
import numpy as np
import pandas as pd
import time

from pathlib import Path


# =========================================================
# 1. PROJECT CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "incidents_feature_engineered.csv"
)

INDEX_DIR = BASE_DIR / "models" / "rag"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:3b"

EMBEDDING_DIMENSION = 768

INDEX_PATH = INDEX_DIR / "aiid_faiss.index"
METADATA_PATH = INDEX_DIR / "aiid_incidents_metadata.pkl"


# =========================================================
# 2. LOAD HISTORICAL INCIDENTS
# =========================================================

def load_historical_incidents():

    print("Loading historical AI incidents...")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    required_columns = [
        "Incident ID",
        "title",
        "description",
        "Risk Domain"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = df.dropna(
        subset=["title", "description"]
    ).copy()

    df["title"] = df["title"].astype(str).str.strip()
    df["description"] = (
        df["description"].astype(str).str.strip()
    )

    df = df[
        (df["title"] != "") &
        (df["description"] != "")
    ].reset_index(drop=True)

    df["incident_text"] = (
        "Incident Title: " + df["title"] +
        "\nIncident Description: " + df["description"]
    )

    print("Historical incidents loaded:", len(df))

    return df


# =========================================================
# 3. GENERATE EMBEDDINGS
# =========================================================

def generate_embeddings(texts):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=texts,
        keep_alive="10m"
    )

    embeddings = np.array(
        response["embeddings"],
        dtype=np.float32
    )

    faiss.normalize_L2(embeddings)

    return embeddings


# =========================================================
# 4. BUILD FAISS INDEX
# =========================================================

def build_faiss_index(embeddings):

    print("Building FAISS vector index...")

    index = faiss.IndexFlatIP(
        EMBEDDING_DIMENSION
    )

    index.add(embeddings)

    print("FAISS index created!")
    print("Total indexed incidents:", index.ntotal)

    return index


# =========================================================
# 5. RETRIEVE SIMILAR HISTORICAL INCIDENTS
# =========================================================

def retrieve_similar_incidents(
    query,
    df,
    index,
    top_k=5
):

    print("\nSearching for relevant historical incidents...")

    query_response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=query,
        keep_alive="10m"
    )

    query_embedding = np.array(
        query_response["embeddings"],
        dtype=np.float32
    )

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        incident = df.iloc[idx]

        results.append({
            "Incident ID": incident["Incident ID"],
            "Title": incident["title"],
            "Description": incident["description"],
            "Risk Domain": incident["Risk Domain"],
            "Similarity Score": round(float(score), 4)
        })

    return pd.DataFrame(results)


# =========================================================
# 6. SAVE FAISS INDEX AND METADATA
# =========================================================

def save_faiss_index(index, df):

    print("\nSaving FAISS index and metadata...")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    df.to_pickle(METADATA_PATH)

    print("FAISS index saved:", INDEX_PATH)
    print("Metadata saved:", METADATA_PATH)


# =========================================================
# 7. LOAD SAVED FAISS INDEX
# =========================================================

def load_faiss_index():

    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Saved FAISS index or metadata not found."
        )

    print("Loading saved FAISS index...")

    index = faiss.read_index(str(INDEX_PATH))
    df = pd.read_pickle(METADATA_PATH)

    if index.ntotal != len(df):
        raise ValueError(
            "FAISS index and metadata counts do not match."
        )

    if index.d != EMBEDDING_DIMENSION:
        raise ValueError(
            "FAISS index embedding dimension is incorrect."
        )

    print("FAISS index loaded:", index.ntotal)
    print("Metadata loaded:", len(df))

    return index, df


# =========================================================
# 8. SIMILARITY-BASED RELEVANCE CATEGORIZATION
# =========================================================

def classify_relevance(similarity_score):

    if similarity_score >= 0.85:
        return "High Similarity"

    elif similarity_score >= 0.70:
        return "Moderate Similarity"

    elif similarity_score >= 0.55:
        return "Low Similarity"

    else:
        return "Weak Similarity"


def add_relevance_categories(retrieved_incidents):

    retrieved_incidents = retrieved_incidents.copy()

    retrieved_incidents["Relevance Level"] = (
        retrieved_incidents["Similarity Score"]
        .apply(classify_relevance)
    )

    return retrieved_incidents


# =========================================================
# 9. GENERATE OPTIMIZED RAG INVESTIGATION REPORT
# =========================================================


def generate_investigation_report(
    incident_title,
    incident_description,
    retrieved_incidents
):

    print("\nGenerating evidence-grounded investigation report...")

    generation_start = time.perf_counter()

    # Prepare historical evidence
    evidence = []

    for _, incident in retrieved_incidents.iterrows():

        description = str(
            incident["Description"]
        )[:250]

        evidence.append(
            f"""
Incident ID: {incident['Incident ID']}
Title: {incident['Title']}
Recorded Risk Domain: {incident['Risk Domain']}
Text Similarity Score: {incident['Similarity Score']:.4f}
Description: {description}
"""
        )

    evidence_text = "\n".join(evidence)

    # Evidence-grounded investigation prompt
    prompt = f"""
You are a professional AI Incident Investigation Assistant.

Your task is to investigate the new incident using the
provided historical evidence.

NEW INCIDENT
Title: {incident_title}

Description:
{incident_description}


HISTORICAL INCIDENTS
{evidence_text}


Prepare an investigation report using the following sections.

1. INCIDENT SUMMARY
Summarize the reported incident using only the supplied details.

2. HISTORICAL EVIDENCE AND RELEVANCE

Evaluate each historical incident individually.

Use these relevance categories:

- DIRECTLY RELEVANT:
  Same or closely related application, failure type and harm.

- INDIRECTLY RELEVANT:
  Different application or context, but a meaningful
  connection to the same safety concern or failure mechanism.

- WEAKLY RELEVANT:
  Only general textual or thematic similarity.

- UNRELATED:
  No meaningful connection to the new incident.

IMPORTANT:
A high text similarity score does not automatically mean
an incident is directly relevant.

For every historical incident:
- Preserve its exact Incident ID and title.
- Preserve its recorded Risk Domain.
- Explain why it is relevant or unrelated.
- Do not invent details absent from its description.

3. POTENTIAL ROOT CAUSES

List possible technical, operational and governance causes.

Clearly label all causes as hypotheses.

For each hypothesis, mention the evidence required
to verify it.

Do not present assumptions as confirmed findings.

4. RISK ASSESSMENT

Discuss potential impacts on:
- Users and affected individuals
- Organizations and service providers
- Public trust and AI system reliability

Only describe impacts reasonably supported by the
new incident description.

5. PREVENTIVE RECOMMENDATIONS

Provide practical recommendations, such as:
- Human expert review for high-risk outputs
- Domain-specific testing and validation
- Output monitoring and incident reporting
- Clear limitations and escalation mechanisms

Explain which identified risk each recommendation addresses.

6. EVIDENCE GAPS AND CONCLUSION

Identify information that is still required.

Distinguish:
- Confirmed information from the incident description
- Historical evidence
- Unverified hypotheses

End with a concise investigation conclusion.


STRICT EVIDENCE RULES:

- Never invent historical facts or Incident IDs.
- Never change recorded Risk Domains.
- Never interpret similarity scores as probabilities.
- Never assume similarity proves causation.
- Never classify an incident as directly relevant
  based only on matching words.
- If historical evidence is insufficient, explicitly
  state that it is insufficient.
- Do not claim that a root cause has been confirmed
  without supporting evidence.
- Maintain a professional and objective tone.
"""

    # Generate report using local LLM
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence-grounded AI safety investigator. "
                    "Evaluate historical evidence carefully. "
                    "Distinguish direct relevance from thematic similarity. "
                    "Never invent facts or unsupported conclusions."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.1,
            "num_predict": 400,
            "num_ctx": 4096,
            "num_batch": 128
        },
        keep_alive="10m"
    )

    report = response["message"]["content"]

    generation_time = (
        time.perf_counter() - generation_start
    )

    print(
        f"\nReport generation time: "
        f"{generation_time:.2f} seconds"
    )

    # Display generation performance
    eval_count = response.get("eval_count")
    eval_duration = response.get("eval_duration")

    if eval_count is not None:
        print("Generated tokens:", eval_count)

    if eval_count and eval_duration:
        tokens_per_second = (
            eval_count / (eval_duration / 1_000_000_000)
        )

        print(
            f"Generation speed: "
            f"{tokens_per_second:.2f} tokens/second"
        )

    return report
