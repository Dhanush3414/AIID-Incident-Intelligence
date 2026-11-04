from similar_incidents import (
    load_incidents,
    build_similarity_index,
    find_similar_incidents,
)


# --------------------------------------------------
# Step 1: Load historical incidents
# --------------------------------------------------

print("\nLoading historical incidents...")

df = load_incidents()

print("Total historical incidents:", len(df))
print("\nDataset preview:")

print(
    df[
        ["Incident ID", "title", "Risk Domain"]
    ].head()
)


# --------------------------------------------------
# Step 2: Build the similarity index
# --------------------------------------------------

print("\nBuilding TF-IDF similarity index...")

vectorizer, incident_vectors = build_similarity_index(df)

print("Historical incident vectors:", incident_vectors.shape)


# --------------------------------------------------
# Step 3: Search for similar incidents
# --------------------------------------------------

title = "AI chatbot provides misleading medical information"

description = (
    "An AI-powered chatbot generated inaccurate medical "
    "advice that could mislead users."
)

print("\nSearching for similar historical incidents...")

results = find_similar_incidents(
    title=title,
    description=description,
    df=df,
    vectorizer=vectorizer,
    incident_vectors=incident_vectors,
    top_n=5,
)


# --------------------------------------------------
# Step 4: Display results
# --------------------------------------------------

print("\nTOP 5 SIMILAR HISTORICAL INCIDENTS")
print("=" * 60)

for index, row in results.iterrows():

    print(f"\nResult {index + 1}")
    print("Incident ID:", row["Incident ID"])
    print("Title:", row["title"])
    print("Risk Domain:", row["Risk Domain"])
    print("Similarity:", str(row["Similarity (%)"]) + "%")

    print(
        "Description:",
        str(row["description"])[:300]
    )

    print("-" * 60)