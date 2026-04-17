"""
A module that implements BM25 search on a list of 10 queries.

Functions:
- load_documents
- bm25_retriever
- build_index
- save_index
- load_index
- bm25_score
- bm25_invoke

"""

from langchain_community.retrievers import BM25Retriever
import pickle
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.tokenizer import create_documents, tokenize
from src.save_to_df import results_to_df


def load_documents(parquet_path):
    """Load document list needed for search"""
    print("Creating document list...")
    doc_list = create_documents(parquet_path)
    print("Document list created!")
    return doc_list


def bm25_retriever(doc_list, k=5):
    """Build the BM25 retriever"""
    print("Building BM25 retriever...")
    retriever = BM25Retriever.from_documents(doc_list, k=k)
    print("Completed retriever build!")
    return retriever


def build_index(retriever):
    """Build the BM25 index"""
    print("Building index...")
    # Retrieve index
    bm25_index = retriever.vectorizer
    print("Completed index build!")

    return bm25_index


def save(file, path, type):
    """Save file as pickle file"""
    print(f"Saving {type}...")

    with open(f'{path}/{type}.pkl', 'wb') as f:
        pickle.dump(file, f)

    print(f"{type} saved to {path}")


def load(path, type):
    """Load index from pickle file"""
    print(f"Loading {type}...")

    with open(f'{path}/{type}.pkl', 'rb') as f:
        file = pickle.load(f)

    print(f"{type} loaded from {path}")

    return file


def bm25_score(bm25_index, query, doc_list, count=False, query_nb=False):
    """Implement BM25 search on given query to return score"""
    if count == 1:
        print("Searching query...")

    # Tokenize query
    tokenized_query = tokenize(query)

    # Get BM25 scores
    scores = bm25_index.get_scores(tokenized_query)
    results_dict = sorted(zip(doc_list, scores), key=lambda x: x[1], reverse=True)

    if count and query_nb:
        print(f"{count}/{query_nb} queries searched")

    return results_dict


def bm25_invoke(retriever, query):
    """Implement BM25 search on given query to return top k results"""
    print("Searching query...")
    result = retriever.invoke(query)
    return result


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

    # build and save index and retriever(run once)
    # comment out these lines once you have generated bm25_index and retriver data
    retriever = bm25_retriever(docs, k=1)
    save(retriever, 'data/processed/bm25_index', 'retriever')

    bm25_index = build_index(retriever)
    save(bm25_index, 'data/processed/bm25_index', 'bm25_index')

    # Load index
    bm25_index = load('data/processed/bm25_index', 'bm25_index')
    retriever = load('data/processed/bm25_index', 'retriever')

    # run queries and save results
    all_results = []
    count = 1
    query_nb = len(queries)
    for query in queries:
        results = bm25_score(bm25_index, query, docs, count, query_nb)
        count += 1
        df = results_to_df(query, results, top_n=5)
        all_results.append(df)

    # Save to csv
    final_df = pd.concat(all_results)
    final_df.to_csv('results/bm25_results.csv', index=False)
    print("10 query results saved to results/bm25_results.csv")
