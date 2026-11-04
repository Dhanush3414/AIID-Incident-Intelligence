from rag.rag_pipeline import (
    load_historical_incidents,
    generate_embeddings,
    build_faiss_index
)


def main():

    # Step 1: Load historical incidents
    df = load_historical_incidents()

    print("\nDataset preview:")
    print(df[["Incident ID", "title"]].head())

    # Step 2: Generate embeddings in batches
    batch_size = 32
    all_embeddings = []

    texts = df["incident_text"].tolist()

    print("\nGenerating embeddings in batches...")

    for start in range(0, len(texts), batch_size):

        batch = texts[start:start + batch_size]

        embeddings = generate_embeddings(batch)

        all_embeddings.append(embeddings)

        print(
            f"Processed {min(start + batch_size, len(texts))}"
            f" / {len(texts)} incidents"
        )

    # Step 3: Combine all embeddings
    import numpy as np

    embeddings = np.vstack(all_embeddings)

    print("\nFinal embedding shape:", embeddings.shape)

    # Step 4: Build FAISS index
    index = build_faiss_index(embeddings)

    print("\nRAG embedding pipeline completed!")
    print("Total indexed incidents:", index.ntotal)


if __name__ == "__main__":
    main()