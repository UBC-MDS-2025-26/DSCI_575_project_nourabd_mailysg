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


def hybrid_retriever(data_path='data/processed'):
    """Build hybrid retriever using 40% BM25 and 60% semantic weighting"""
    
    print('Loading semantic retriever...')
    vector_retriever = load_index(f'{data_path}/faiss_index').as_retriever()
    print('Loading BM25 retriever...')
    bm25_retriever = load(f'{data_path}/bm25_index', 'retriever')

    # Create the ensemble
    print('Creating hybrid retriever...')
    retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.4, 0.6]
    )
    return retriever


def hybrid_results(query, retriever):
    """Implement hybrid retriever to get top k results for query"""
    print("Searching query...")
    # Invoke to get combined results
    results = retriever.invoke(query)
    return results


retriever = hybrid_retriever()
results = hybrid_results('headphones', retriever)
print(results)