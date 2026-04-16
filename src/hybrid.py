from langchain_classic.retrievers import EnsembleRetriever

from .bm25 import load_documents, retriever
from .semantic import load_index

# Load documents
docs = load_documents('data/processed/processed_data.parquet')

# Initialize individual retrievers
bm25_retriever = retriever(docs, k=5)
vector_store = load_index('data/processed/faiss_index')
vector_retriever = vector_store.as_retriever()

# Create the ensemble
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]  # Example: asigning 40% importance to BM25, 60% to Semantic Search
)

# Invoke to get combined results
results = ensemble_retriever.invoke("headphones")
print(results)