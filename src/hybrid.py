"""
A module that implements hybrid search using BM25 and semantic search.

Functions:
- hybrid_retriever
- hybrid_results
"""
from langchain_classic.retrievers import EnsembleRetriever
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.bm25 import load
from src.semantic import load_index


def hybrid_retriever(vector_retriever, bm25_retriever):
    """Build hybrid retriever using 40% BM25 and 60% semantic weighting"""
    
    print('Creating hybrid retriever...')
    vector_retriever = vector_retriever.as_retriever()

    # Create the ensemble
    retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.4, 0.6]
    )
    print('Completed hybrid retriever!')
    return retriever


def hybrid_results(query, retriever):
    """Implement hybrid retriever to get top k results for query"""
    print("Searching query...")
    # Invoke to get combined results
    results = retriever.invoke(query)
    return results


vector_retriever = load_index('data/processed/faiss_index')
bm25_retriever = load('data/processed/bm25_index', 'retriever')
retriever = hybrid_retriever(vector_retriever, bm25_retriever)
results = hybrid_results('headphones', retriever)
print(results)