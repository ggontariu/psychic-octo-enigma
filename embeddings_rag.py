import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key"))

# Initialize ChromaDB
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_data"
))

# Get or create collection
collection = chroma_client.get_or_create_collection(name="rag_documents")

# Sample documents
DOCUMENTS = [
    "Python is a high-level programming language created by Guido van Rossum.",
    "RAG stands for Retrieval Augmented Generation, combining search with LLMs.",
    "Ollama allows you to run large language models locally on your machine.",
    "Vector databases store embeddings for semantic search.",
]

def generate_embedding(text):
    """Generate embedding using OpenAI"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def initialize_documents():
    """Add documents to ChromaDB with embeddings"""
    # Check if documents are already added
    if collection.count() == 0:
        print("Initializing documents in ChromaDB...")
        embeddings = []
        ids = []
        
        for i, doc in enumerate(DOCUMENTS):
            embedding = generate_embedding(doc)
            embeddings.append(embedding)
            ids.append(f"doc{i+1}")
        
        collection.add(
            embeddings=embeddings,
            documents=DOCUMENTS,
            ids=ids
        )
        print(f"Added {len(DOCUMENTS)} documents to ChromaDB")

# Example usage
if __name__ == "__main__":
    # Initialize documents in ChromaDB
    initialize_documents()
    
    # Generate embedding for a query
    query = "What is RAG?"
    query_embedding = generate_embedding(query)
    
    # Search for similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    
    print(f"\nQuery: {query}")
    print(f"\nSimilar documents found:")
    for i, doc in enumerate(results['documents'][0], 1):
        print(f"{i}. {doc}")

