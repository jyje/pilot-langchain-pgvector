"""
pgVector and LangChain Example Application

This package contains example code for working with pgVector and LangChain
to store and search vector embeddings in a PostgreSQL database.
"""

__version__ = "0.1.0"

from .config import DATABASE_URL, VECTOR_DIMENSION, COLLECTION_NAME
from .vector_example import RandomEmbeddings, create_sample_documents

__all__ = [
    "DATABASE_URL",
    "VECTOR_DIMENSION",
    "COLLECTION_NAME",
    "RandomEmbeddings",
    "create_sample_documents",
]
