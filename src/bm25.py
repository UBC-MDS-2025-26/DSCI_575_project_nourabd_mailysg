from langchain_community.retrievers import BM25Retriever
import pickle
import pandas as pd
from tokenizer import create_documents, tokenize
from save_to_df import results_to_df

def load_documents(parquet_path):
    """Load document list needed for search"""
    doc_list = create_documents(parquet_path)
    return doc_list


def build_index(doc_list, k=5):
     # Fit BM25 retriever
    retriever = BM25Retriever.from_documents(doc_list)

    # Retrieve index
    bm25_index = retriever.vectorizer

    return bm25_index

def save_index(bm25_index,path):
    #Save index as pickle file
    with open(f'{path}/bm25_index.pkl', 'wb') as f:
        pickle.dump(bm25_index, f)
    print(f"Index saved to {path}")

def load_index(path):
    #Load index as pickle file
    with open(f'{path}/bm25_index.pkl', 'rb') as f:
        bm25_index = pickle.load(f)
    print(f"Index loaded from {path}")
    return bm25_index

def bm25_search(bm25_index, query, doc_list):
    # Query search
    tokenized_query = tokenize(query)
  
    scores = bm25_index.get_scores(tokenized_query)

    results_dict = sorted(zip(doc_list, scores), key=lambda x: x[1], reverse=True)

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

    # build and save index (run once)
    # comment out these lines once you have generated faiss_index data 
    docs = load_documents('data/processed/processed_data.parquet')
    # bm25_index = build_index(docs)
    # save_index(bm25_index, 'data/processed/bm25_index')

    bm25_index = load_index('data/processed/bm25_index')

    # run queries and save results
    all_results = []
    for query in queries:
        results = bm25_search(bm25_index, query, docs)
        df = results_to_df(query, results, top_n=5)
        all_results.append(df)

final_df = pd.concat(all_results)
final_df.to_csv('results/bm25_results.csv', index=False)
print("10 query results saved to results/bm25_results.csv")