"""
A module that creates helper functions to preprocess and create the corpus to be used for semantic and BM25 search.

Functions:
- load_data
- create_features
- merged
- preprocess
- create_corpus
"""

import re
import json
import pandas as pd


def load_data(name, file):
    """Load json files and create a list of records"""
    
    record_list = []
    with open(file, 'r') as fp:
        for line in fp:
            record = json.loads(line.strip())
            record_list.append(record)
    print(f'{name} loaded!')
    return record_list

def create_features(meta_data):
    """Add and edit meta data fields"""

    # Extract item type, ESRB rating and date first available from detail field
    meta_data['item_type'] = meta_data['details'].map(lambda x : x['Type of item'] if 'Type of item' in x.keys() else None)
    meta_data['rated'] = meta_data['details'].map(lambda x : x['Rated'] if 'Rated' in x.keys() else None)
    meta_data['date_first_available'] = meta_data['details'].map(lambda x : x['Date First Available'] if 'Date First Available' in x.keys() else None)

    # Change price field type
    meta_data['price']=meta_data['price'].astype(str)

    return meta_data
    

def merged(sample_size=400000):
    """Merge meta data and user dataframes"""

    # Load the data
    print('Loading user reviews ...')
    user_reviews = pd.DataFrame(load_data('User reviews','data/raw/Video_Games.jsonl'))
    print('Loading meta data ...')
    meta_data = pd.DataFrame(load_data('Meta data','data/raw/meta_Video_Games.jsonl'))

    # Add new features to meta data 
    meta_data = create_features(meta_data)
    
    # Keep only useful fields 
    proc_meta_data = meta_data.drop(columns=['main_category','images','videos','bought_together','details','author','subtitle']).rename(columns={'title':'item_title'}) 

    # Keep only verified purcahses and useful fields
    proc_user_reviews = user_reviews[user_reviews['verified_purchase']==True].drop(columns=['rating','images','asin','timestamp','user_id','helpful_vote','verified_purchase']).rename(columns={'title':'review_title'}) 

    print('Merging dataframes...')

    #Merge dataframes
    merged = pd.merge(proc_meta_data, 
                  proc_user_reviews, 
                  on='parent_asin', 
                  how='inner')
    print('Dataframes merged!')

    return merged[:sample_size]



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
    print("Preprocessing data ...")
    count = 1
    for column in ['item_title', 'features', 'description','store','categories','item_type', 'rated','date_first_available', 'review_title','text']:   
        merged[column] = merged[column].apply(lambda x : preprocess(x))
        print(f'... {count}/10 columns done ...')
        count +=1
    merged.to_parquet('data/processed/processed_data.parquet', engine='pyarrow', compression='snappy')
    print(f'Preprocessing done!')

merged_df = merged()
create_corpus(merged_df)



