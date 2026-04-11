"""
A module that tokenizes the data using langchain wrapper.

Functions:
- create_documents
- tokenize
"""
import pickle
import pandas as pd
from langchain_core.documents import Document


def create_documents(parquet_path='data/processed/processed_data.parquet', doc_list_path='data/processed/doc_list.pkl'):
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
    df = pd.read_parquet(parquet_path)

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
                "parent_asin" : record.parent_asin
                }
    )   
        # Add document to list                                                                                      
        doc_list.append(document)

    # Return list of documents
    return doc_list
    
def tokenize(text):
    """Tokenize given corpus using default Langchain method"""
    if isinstance(text, Document):
        text = [document.page_content for document in text]
        tokenized_corpus = [token.split() for token in text] 
    else:
        tokenized_corpus = text.split()
    return tokenized_corpus
  
    
def save_tokenized_corpus(tokenized_corpus):
    """Save tokenized corpus"""
    with open('data/processed/tokenized_corpus.pkl', 'wb') as f:
        pickle.dump(tokenized_corpus, f)

