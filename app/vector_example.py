import os
import random
import numpy as np
from typing import List, Tuple
from dotenv import load_dotenv

from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.embeddings.base import Embeddings

# Load environment variables
load_dotenv()

# Database connection information
DATABASE_URL = "postgresql://postgres:password@localhost:15432/vectordb"

class RandomEmbeddings(Embeddings):
    """Embedding class that generates random vectors"""

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Convert text list to vector list"""
        return [self._generate_random_vector() for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        """Convert query text to vector"""
        return self._generate_random_vector()

    def _generate_random_vector(self) -> List[float]:
        """Generate random normalized vector"""
        vector = np.random.normal(0, 1, self.dimension)
        normalized_vector = vector / np.linalg.norm(vector)
        return normalized_vector.tolist()

def create_sample_documents() -> List[Document]:
    """Create sample documents"""
    sample_texts = [
        "Machine learning is a field of artificial intelligence.",
        "Deep learning is a learning method based on neural networks.",
        "Natural language processing is technology that enables computers to understand human language.",
        "Computer vision is technology that analyzes images and videos.",
        "Reinforcement learning is a method of learning through rewards.",
        "Data science is the discipline of finding insights from data.",
        "Big data refers to large volumes of complex data.",
        "Cloud computing provides computing services through the internet.",
        "Blockchain is a distributed ledger technology.",
        "Internet of Things (IoT) is technology that connects physical objects to networks."
    ]

    documents = []
    for i, text in enumerate(sample_texts):
        doc = Document(
            page_content=text,
            metadata={
                "id": i + 1,
                "category": "technology",
                "source": "sample_data"
            }
        )
        documents.append(doc)

    return documents

def main():
    print("=== Vector Storage and Search Example using pgVector and LangChain ===\n")

    # Initialize embedding model (using random vectors)
    embeddings = RandomEmbeddings(dimension=1536)

    # Initialize PGVector vector store
    try:
        vector_store = PGVector(
            connection_string=DATABASE_URL,
            embedding_function=embeddings,
            collection_name="documents",
            distance_strategy="cosine"
        )
        print("✅ pgVector connection successful!")
    except Exception as e:
        print(f"❌ pgVector connection failed: {e}")
        return

    # 1. Create and store sample documents
    print("\n1. Storing sample documents in vector database...")
    sample_documents = create_sample_documents()

    try:
        # Add documents to vector store
        vector_store.add_documents(sample_documents)
        print(f"✅ {len(sample_documents)} documents stored successfully!")
    except Exception as e:
        print(f"❌ Document storage failed: {e}")
        return

    # 2. Perform similarity search
    print("\n2. Performing similarity search...")

    # Search queries
    queries = [
        "Tell me about artificial intelligence and machine learning",
        "What are data analysis technologies?",
        "Explain cloud and distributed systems"
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n--- Search {i}: '{query}' ---")

        try:
            # Similarity search (top 3 results)
            similar_docs = vector_store.similarity_search(
                query=query,
                k=3
            )

            print("Search results:")
            for j, doc in enumerate(similar_docs, 1):
                print(f"  {j}. {doc.page_content}")
                print(f"     Metadata: {doc.metadata}")

            # Search with scores
            similar_docs_with_scores = vector_store.similarity_search_with_score(
                query=query,
                k=3
            )

            print("Similarity scores:")
            for j, (doc, score) in enumerate(similar_docs_with_scores, 1):
                print(f"  {j}. Score: {score:.4f}")

        except Exception as e:
            print(f"❌ Search failed: {e}")

    # 3. Metadata filtering search
    print("\n3. Metadata filtering search...")

    try:
        filtered_docs = vector_store.similarity_search(
            query="Tell me about technology",
            k=5,
            filter={"category": "technology"}
        )

        print("Filtered search results:")
        for i, doc in enumerate(filtered_docs, 1):
            print(f"  {i}. {doc.page_content}")

    except Exception as e:
        print(f"❌ Filtered search failed: {e}")

    # 4. Direct vector search
    print("\n4. Direct search with random vector...")

    try:
        # Generate random vector
        random_vector = embeddings.embed_query("random search")

        # Search directly with vector
        similar_docs = vector_store.similarity_search_by_vector(
            embedding=random_vector,
            k=3
        )

        print("Random vector search results:")
        for i, doc in enumerate(similar_docs, 1):
            print(f"  {i}. {doc.page_content}")

    except Exception as e:
        print(f"❌ Vector search failed: {e}")

    print("\n=== Example completed ===")

if __name__ == "__main__":
    main()
