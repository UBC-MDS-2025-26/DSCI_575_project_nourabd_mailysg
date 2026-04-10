from langchain_community.retrievers import BM25Retriever
import pickle
import pandas as pd

def bm25_search(query):

    # Retrieve document list
    with open("notebooks/small_doc_list.pkl", "rb") as f:
        doc_list = pickle.load(f)

    # Fit BM25 retriever
    retriever = BM25Retriever.from_documents(doc_list, k=5)

    # Retrieve index
    bm25_index = retriever.vectorizer

    #Save index as pickle file
    with open('bm25_index.pkl', 'wb') as f:
        pickle.dump(bm25_index, f)

    # Get tokenized corpus
    raw_corpus = [document.page_content for document in doc_list]
    tokenized_corpus = [text.split() for text in raw_corpus] # Using the default Langchain tokenizer

    # Save tokenized corpus as pickle
    with open('tokenized_corpus.pkl', 'wb') as f:
        pickle.dump(tokenized_corpus, f)

    # Query search
    tokenized_query = query.split()

    scores = bm25_index.get_scores(tokenized_query)

    results_dict = {'score': [], 
                  'item_title': [], 
                  'features': [], 
                  'description': [], 
                  'store': [], 
                  'categories': [],
                  'item_type': [], 
                  'review_title': [],
                  'rated': [], 
                  'date_first_available':[],
                  'text': [],
                  'average_rating': [], 
                  'rating_number': [], 
                  'price': []}
    
    for document, score in zip(doc_list, scores):
        results_dict['score'].append(score)
        for (key,value) in document.metadata.items():
            results_dict[key].append(value)
    return pd.DataFrame(results_dict).sort_values('score', ascending=False)
        

example = bm25_search('nintendo switch screen protector')
print(example)

