import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
from src.save_to_df import results_to_df
from src.tokenizer import create_documents
from src.config import PARQUET_DATA, FAISS_INDEX, SEMANTIC_RESULTS
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.save_to_df import results_to_df
from src.tokenizer import create_documents


def load_documents(parquet_path):
    """Load LangChain documents from parquet"""
    doc_list = create_documents(parquet_path)
    print(f"Loaded {len(doc_list)} documents")
    return doc_list


def build_index(docs, model_name='all-MiniLM-L6-v2', batch_size=5000):
    """Build FAISS index from documents"""
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
    
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        vector_store.add_documents(documents=batch)
        print(f"Indexed {min(i + batch_size, len(docs))}/{len(docs)}")
    
    return vector_store, embeddings


def save_index(vector_store, path):
    """Save FAISS index to disk"""
    vector_store.save_local(path)
    print(f"Index saved to {path}")


def load_index(path, model_name='all-MiniLM-L6-v2'):
    """Load FAISS index from disk"""
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"Index loaded from {path}")
    return vector_store


def semantic_search(vector_store, query, k=5):
    """Search FAISS index and return results"""
    results = vector_store.similarity_search_with_score(query, k=k)
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)
    for i, (doc, score) in enumerate(results):
        print(f"\nResult {i+1} [SIM={score:.4f}]")
        print(f"Title:  {doc.metadata['item_title']}")
        print(f"Rating: {doc.metadata['average_rating']}")
        print(f"Review: {doc.page_content[:150]}...")
    return results

#running analysis on 10 queries

if __name__ == "__main__":
    queries = [
        # Easy
        "nintendo switch screen protector",
        "gaming headset with microphone",
        "xbox 360 wireless controller",
        "fifa 16 game for playstation",
        # Medium
        "playstation games for sports lovers",
        "competitive multiplayer game for large groups",
        "comfortable headset for long gaming sessions",
        "ps4 controller with good battery life",
        # Complex
        "best wireless gaming headset for ps5 with good microphone under $100",
        "good single player story game for a beginner who just got their first playstation under $50"
    ]
    
    # build and save index (run once)
    # comment out these lines once you have generated faiss_index data 
    docs = load_documents(PARQUET_DATA)
    vector_store, _ = build_index(docs)
    save_index(vector_store, FAISS_INDEX)

    vector_store = load_index(FAISS_INDEX)

    # run queries and save results
    all_results = []
    for query in queries:
        results = semantic_search(vector_store, query, k=50)
        df = results_to_df(query, results, top_n=5)
        all_results.append(df)

    # save to csv
    final_df = pd.concat(all_results)
    final_df.to_csv(SEMANTIC_RESULTS, index=False)
    print("10 query results saved to results/semantic_results.csv")