from rag.rag_pipeline import add_relevance_categories
from rag.rag_pipeline import (
    load_faiss_index,
    retrieve_similar_incidents,
    generate_investigation_report
)


def main():

    # Step 1: Load saved FAISS index and metadata
    print("Loading saved RAG resources...")

    index, df = load_faiss_index()

    # Step 2: Define a new incident
    incident_title = (
        "AI Chatbot Provides Misleading Medical Advice"
    )

    incident_description = """
    An AI-powered chatbot provided misleading medical
    recommendations to a patient. The patient relied on
    the generated information, which created potential
    health risks. The reliability and safety of the
    chatbot's medical responses are being investigated.
    """

    print("\nNEW INCIDENT")
    print("Title:", incident_title)

    # Step 3: Retrieve historical incidents
    query = incident_title + "\n" + incident_description

    retrieved_incidents = retrieve_similar_incidents(
        query=query,
        df=df,
        index=index,
        top_k=5
    )

    print("\nRETRIEVED HISTORICAL INCIDENTS")

    print(
        retrieved_incidents[
            [
                "Incident ID",
                "Title",
                "Risk Domain",
                "Similarity Score"
            ]
        ].to_string(index=False)
    )

    retrieved_incidents = add_relevance_categories(
    retrieved_incidents
    )

    print("\nRETRIEVAL RELEVANCE ANALYSIS")

    print(
    retrieved_incidents[
        [
            "Incident ID",
            "Relevance Level",
            "Similarity Score"
        ]
    ].to_string(index=False)
    )

    # Step 4: Generate investigation report
    report = generate_investigation_report(
        incident_title=incident_title,
        incident_description=incident_description,
        retrieved_incidents=retrieved_incidents
    )

    # Step 5: Display final report
    print("\n" + "=" * 70)
    print("AI INCIDENT INVESTIGATION REPORT")
    print("=" * 70)

    print(report)

    print("\n" + "=" * 70)
    print("RAG INVESTIGATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()