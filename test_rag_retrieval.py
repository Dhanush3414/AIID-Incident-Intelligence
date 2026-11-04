from pathlib import Path

from rag.rag_pipeline import (
    load_historical_incidents,
    generate_embeddings,
    build_faiss_index,
    retrieve_similar_incidents,
    save_faiss_index,
    load_faiss_index
)

import numpy as np


def main():

    index_path = Path("models/rag/aiid_faiss.index")
    metadata_path = Path("models/rag/aiid_incidents_metadata.pkl")

    # Load existing index if available
    if index_path.exists() and metadata_path.exists():

        index, df = load_faiss_index()

    else:

        print("No saved index found. Building a new index...")

        df = load_historical_incidents()

        texts = df["incident_text"].tolist()

        batch_size = 32
        all_embeddings = []

        for start in range(0, len(texts), batch_size):

            batch = texts[start:start + batch_size]

            embeddings = generate_embeddings(batch)

            all_embeddings.append(embeddings)

            print(
                f"Processed {min(start + batch_size, len(texts))}"
                f" / {len(texts)} incidents"
            )

        embeddings = np.vstack(all_embeddings)

        index = build_faiss_index(embeddings)

        save_faiss_index(index, df)

    # Test retrieval
    query = """
    An AI chatbot provided misleading medical advice
    to a patient, resulting in potential health risks.
    """

    results = retrieve_similar_incidents(
        query=query,
        df=df,
        index=index,
        top_k=5
    )

    print("\nTOP 5 RETRIEVED HISTORICAL INCIDENTS")

    print(
        results[
            [
                "Incident ID",
                "Title",
                "Risk Domain",
                "Similarity Score"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()