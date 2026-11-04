import ollama

# Test LLM connection
print("Testing LLM connection...")

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain AI incidents in one sentence."
        }
    ]
)

print("\nLLM Response:")
print(response["message"]["content"])


# Test embedding model
print("\nTesting embedding model...")

embedding_response = ollama.embed(
    model="nomic-embed-text",
    input="An AI chatbot generates misleading medical information."
)

embedding = embedding_response["embeddings"][0]

print("\nEmbedding generated successfully!")
print("Embedding dimensions:", len(embedding))
print("First 5 values:", embedding[:5])
