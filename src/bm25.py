"""
A module that implements BM25 search on a list of 10 queries.

Functions:
- load_documents
- build_index
- save_index
- load_index
- bm25_search

"""

from langchain_community.retrievers import BM25Retriever
import pickle
import pandas as pd
from .tokenizer import create_documents, tokenize
from .save_to_df import results_to_df

def load_documents(parquet_path):
    """Load document list needed for search"""
    print("Creating document list...")
    doc_list = create_documents(parquet_path)
    print("Document list created!")
    return doc_list


def build_index(doc_list):
    """Build the BM25 index"""
    print("Building index...")
    retriever = BM25Retriever.from_documents(doc_list)

    # Retrieve index
    bm25_index = retriever.vectorizer
    print("Completed index build!")

    return bm25_index

def save_index(bm25_index,path):
    """Save index as pickle file"""
    print(f"Saving index...")

    with open(f'{path}/bm25_index.pkl', 'wb') as f:
        pickle.dump(bm25_index, f)

    print(f"Index saved to {path}")

def load_index(path):
    """Load index from pickle file"""
    print(f"Loading index...")

    with open(f'{path}/bm25_index.pkl', 'rb') as f:
        bm25_index = pickle.load(f)

    print(f"Index loaded from {path}")

    return bm25_index

def bm25_search(bm25_index, query, doc_list, count=False, query_nb=False):
    """Implement BM25 search on given query"""
    if count==1 :
        print(f"Searching query...")

    # Tokenize query
    tokenized_query = tokenize(query)

    #Get BM25 scores
    scores = bm25_index.get_scores(tokenized_query)
    results_dict = sorted(zip(doc_list, scores), key=lambda x: x[1], reverse=True)

    if count and query_nb:
        print(f"{count}/{query_nb} queries searched")

    return results_dict
       

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

    # Load documents
    docs = load_documents('data/processed/processed_data.parquet')

    # build and save index (run once)
    # comment out these lines once you have generated bm25_index data 
    bm25_index = build_index(docs)
    save_index(bm25_index, 'data/processed/bm25_index')

    # Load index
    bm25_index = load_index('data/processed/bm25_index')

    # run queries and save results
    all_results = []
    count = 1
    query_nb = len(queries)
    for query in queries:
        results = bm25_search(bm25_index, query, docs, count, query_nb)
        count += 1
        df = results_to_df(query, results, top_n=5)
        all_results.append(df)

    # Save to csv
    final_df = pd.concat(all_results)
    final_df.to_csv('results/bm25_results.csv', index=False)
    print("10 query results saved to results/bm25_results.csv")
