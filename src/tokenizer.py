"""
A module that tokenizes the data using langchain wrapper.

Functions:
- create_documents
- tokenize
"""
import pickle
import pandas as pd
from langchain_core.documents import Document
import os


def create_documents(file):
    """
    This function tokenizes the given text into Langchain documents.

    For best search results, the following fields from the given records 
    are added to the page content part of the document:
        - item_title
        - features
        - description
        - store
        - categories
        - item_type
        - rated
        - date_first_available
        - review_title
        - text

    More information about these fields can be found in notebooks/milestone1_exploration.ipynb.
    """

    # Read in the parquet file
    df = pd.read_parquet(file)

    # Create list to store documents
    doc_list = []

    # For every record in our preprocessed corpus 
    for record in df.itertuples(index=True):

        # Create document with information in record
        document = Document(
        page_content=f"{record.item_title} {record.features} {record.description} {record.store} {record.categories} {record.item_type} {record.rated} {record.date_first_available} {record.review_title} {record.text}",
        metadata={"item_title" : record.item_title,
                "features" : record.features,
                "description" : record.description,
                "store" : record.store,
                "categories" : record.categories,
                "item_type" : record.item_type,
                "review_title" : record.review_title,
                "rated" : record.rated,
                "date_first_available" : record.date_first_available,
                "review_title" : record.review_title,
                "text" : record.text,
                "average_rating": record.average_rating,
                "rating_number" : record.rating_number,
                "price" : record.price, 
                "parent_asin": record.parent_asin
                }
    )   
        # Add document to list                                                                                      
        doc_list.append(document)

    # Save document list as a pickle file for further use
    with open('data/processed/doc_list.pkl', 'wb') as f:
        pickle.dump(doc_list, f)

    # Return list of documents
    return doc_list
    



def tokenize():
    """Tokenize given corpus using default Langchain method"""

    # Check if document list already exists
    if not os.path.isfile('data/processed/doc_list.pkl') :
        create_documents('data/processed/processed_data.parquet')
    
    # Open document list 
    with open("data/processed/doc_list.pkl", "rb") as f:
        doc_list = pickle.load(f)

    # Tokenize corpus using the default Langchain tokenizer
    raw_corpus = [document.page_content for document in doc_list]
    tokenized_corpus = [text.split() for text in raw_corpus] 
  
    # Save tokenized corpus as pickle
    with open('data/processed/tokenized_corpus.pkl', 'wb') as f:
        pickle.dump(tokenized_corpus, f)


