from langchain_community.retrievers import BM25Retriever
import pickle
import pandas as pd
from tokenizer import create_documents, tokenize


def load_documents(parquet_path):
    doc_list = create_documents()
    return doc_list


def build_index(doc_list, k=5):
     # Fit BM25 retriever
    retriever = BM25Retriever.from_documents(doc_list, k)

    # Retrieve index
    bm25_index = retriever.vectorizer

    return bm25_index

def save_index(bm25_index, path):
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

def bm25_search(bm25_index, query):
    # Query search
    tokenized_query = tokenize(query)
  
    # scores = bm25_index.get_scores(tokenized_query)

    # results_dict = {'score': [], 
    #               'item_title': [], 
    #               'features': [], 
    #               'description': [], 
    #               'store': [], 
    #               'categories': [],
    #               'item_type': [], 
    #               'review_title': [],
    #               'rated': [], 
    #               'date_first_available':[],
    #               'text': [],
    #               'average_rating': [], 
    #               'rating_number': [], 
    #               'price': []}
    
    # for document, score in zip(doc_list, scores):
    #     results_dict['score'].append(score)
    #     for (key,value) in document.metadata.items():
    #         results_dict[key].append(value)
    # return pd.DataFrame(results_dict).sort_values('score', ascending=False)
        

example = bm25_search('2','nintendo switch screen protector')
print(example)

