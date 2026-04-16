"""
A module that implements hybrid search using BM25 and semantic search.

Functions:
- hybrid_retriever
- hybrid_results
"""
from langchain_classic.retrievers import EnsembleRetriever
from .bm25 import load_documents, bm25_retriever
from .semantic import load_index


def hybrid_retriever(parquet_path='data/processed/processed_data.parquet', index_path='data/processed/faiss_index', k=5):
    """Build hybrid retriever using 40% BM25 and 60% semantic weighting"""
    # Load documents
    docs = load_documents(parquet_path)

    # Initialize individual retrievers
    print('Creating BM25 retriever...')
    bm25 = bm25_retriever(docs, k=k)
    print('Creating semantic retriever...')
    vector_store = load_index(index_path)
    vector_retriever = vector_store.as_retriever()

    # Create the ensemble
    print('Creating hybrid retriever...')
    retriever = EnsembleRetriever(
        retrievers=[bm25, vector_retriever],
        weights=[0.4, 0.6]
    )
    return retriever


def hybrid_results(query, parquet_path='data/processed/processed_data.parquet', index_path='data/processed/faiss_index', k=5):
    """Implement hybrid retriever to get top k results for query"""
    print("Searching query...")
    retriever = hybrid_retriever(parquet_path, index_path, k)
    # Invoke to get combined results
    results = retriever.invoke(query)
    return results
