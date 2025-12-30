import requests
import json

# Fake "database" of documents
DOCUMENTS = [
    "Python is a high-level programming language created by Guido van Rossum.",
    "RAG stands for Retrieval Augmented Generation, combining search with LLMs.",
    "Ollama allows you to run large language models locally on your machine.",
    "Vector databases store embeddings for semantic search.",
]

def simple_search(query, documents):
    """Super simple keyword search (we'll improve this later)"""
    # In real RAG, you'd use embeddings and vector similarity
    # For now, just keyword matching
    
    results = []
    query_lower = query.lower()
    
    for doc in documents:
        if any(word in doc.lower() for word in query_lower.split()):
            results.append(doc)
    
    return results[:2]  # Return top 2 matches

def rag_query(question, model="llama3.1:8b"):
    """Simple RAG: search docs, then ask LLM with context"""
    
    # 1. Search for relevant documents
    relevant_docs = simple_search(question, DOCUMENTS)
    
    # 2. Build prompt with context
    context = "\n".join(relevant_docs)
    prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
    
    # 3. Query LLM
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    return result['response']

# Test it!
if __name__ == "__main__":
    questions = [
        "What is RAG?",
        "Who created Python?",
        "What does Ollama do?",
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        answer = rag_query(q)
        print(f"A: {answer}")