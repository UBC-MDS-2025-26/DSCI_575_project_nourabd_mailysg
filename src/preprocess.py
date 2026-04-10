"""
A module that creates helper functions to preprocess and create the corpus to be used for semantic and BM25 search.

Functions:
- preprocess
- create_corpus
"""

import re

def preprocess(text):
    """
    This function preprocesses the given text.

    The preprocessing steps include :
        - transform text to lowercase letters
        - removes all elements that aren't lowercase letters, numbers or whitespace
        - if the given text is a list, transforms it into a string
    
    """
    if type(text) == list :
        processed_text = ''
        for element in text :
            element = element.lower()
            element = re.sub(r"[^a-z0-9\s]", "", element)
            processed_text += element + ' '
        return processed_text
    elif type(text) == str :
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text
    else:
        return text
    
def create_corpus(merged):
    """This function creates the corpus by preprocessing given columns."""
    for column in ['item_title', 'features', 'description','store','categories','item_type', 'rated','date_first_available', 'review_title','text']:   
        merged[column] = merged[column].apply(lambda x : preprocess(x))
        print(f'{column} : done')
    merged.to_parquet('../data/processed/processed_data.parquet', engine='pyarrow', compression='snappy')
    print(f'Preprocessing done')









