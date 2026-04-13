"""
If the web app crashes due to memory constraints (low RAM), 
use OPTION 2 in the get_bm25() function.
"""

import streamlit as st
import pandas as pd
import sys
import os
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.semantic import load_index, semantic_search
from src.bm25 import load_index as load_bm25_index
from src.bm25 import bm25_search
from src.save_to_df import results_to_df
from src.tokenizer import create_documents
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever

st.set_page_config(page_title="Video Game Search", layout="wide")
st.title("\U0001F3AE Amazon Video Game Product Search")
st.markdown("Search for video game products using keyword (BM25) or semantic search.")  # ← add here
st.divider()

# load index on demand - separately depending on which radio button selected due to RAM restrictions
@st.cache_resource
def get_semantic():
    return load_index('data/processed/faiss_index')

@st.cache_resource
def get_bm25():
     # OPTION 1: full data 

    bm25_index = load_bm25_index('data/processed/bm25_index')
    docs = create_documents('data/processed/processed_data.parquet')
    
    #OPTION 2: small sample (for low RAM machines), uncomment below code and comment out above code block

    # df = pd.read_parquet('data/processed/processed_data.parquet').head(10000)
    # docs = []
    # for record in df.itertuples(index=True):
    #     document = Document(
    #         page_content=f"{record.item_title} {record.features} {record.description} {record.store} {record.categories} {record.item_type} {record.rated} {record.date_first_available} {record.review_title} {record.text}",
    #         metadata={
    #             "item_title": record.item_title,
    #             "features": record.features,
    #             "description": record.description,
    #             "store": record.store,
    #             "categories": record.categories,
    #             "item_type": record.item_type,
    #             "review_title": record.review_title,
    #             "rated": record.rated,
    #             "date_first_available": record.date_first_available,
    #             "text": record.text,
    #             "average_rating": record.average_rating,
    #             "rating_number": record.rating_number,
    #             "price": record.price,
    #             "parent_asin": record.parent_asin
    #         }
    #     )
    #     docs.append(document)
    # retriever = BM25Retriever.from_documents(docs, k=3) #rebuilding index with smaller sample of docs
    # bm25_index = retriever.vectorizer

    return bm25_index, docs

# star rating function
def rating_to_stars(rating):
    if pd.isna(rating):
        return "No rating"
    rating = float(rating)
    filled = round(rating)
    empty = 5 - filled
    stars_html = '<span style="color: gold; font-size: 20px;">'
    stars_html += '&#9733;' * filled
    stars_html += '&#9734;' * empty
    stars_html += f'</span> ({rating})'
    return stars_html

# thumbs up/thumbs down feedback 
def save_feedback(query, item_title, feedback, mode):
    feedback_path = 'results/feedback.csv'
    new_row = pd.DataFrame([{
        "query": query,
        "item_title": item_title,
        "feedback": feedback,
        "mode": mode}])
    if os.path.exists(feedback_path):
        new_row.to_csv(feedback_path, mode='a', header=False, index=False)
    else:
        new_row.to_csv(feedback_path, index=False)

# radio button, model selection
mode = st.radio("Search Mode", ["Semantic", "BM25"], horizontal=True)

# query input box
query = st.text_input("Search for a product...")

# results from models
if query:
    with st.spinner("Searching..."):
        #semantic search
        if mode == "Semantic":
            vector_store = get_semantic()
            results = semantic_search(vector_store, query, k=50)
            df = results_to_df(query, results, top_n=3)

            st.markdown(f"**Top {len(df)} results for:** *{query}*")

            for i, row in df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['Product title'].title()}")
                        st.markdown("**Review:**")
                        st.write(row['Review'])
                    with col2:
                        st.markdown(rating_to_stars(row['Rating']), unsafe_allow_html=True)
                        st.metric("Similarity score", round(row['Score'], 2))
                        col_up, col_down = st.columns(2)
                
                        with col_up:
                            if st.button("\U0001F44D", key=f"sem_up_{i}"):
                                save_feedback(query, row['Product title'], "thumbs_up", mode)
                                st.success("Thanks for your feedback!")
                        with col_down:
                            if st.button("\U0001F44E", key=f"sem_down_{i}"):
                                save_feedback(query, row['Product title'], "thumbs_down", mode)
                                st.success("Thanks for your feeback!")
        #BM25
        elif mode == "BM25":
            bm25_index, docs = get_bm25()
            results = bm25_search(bm25_index, query, docs, count=1, query_nb=1)
            df = results_to_df(query, results, top_n=3)

            st.markdown(f"**Top {len(df)} results for:** *{query}*")

            for i, row in df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['Product title'].title()}")
                        st.markdown("**Review:**")
                        st.write(row['Review'])
                    with col2:
                        st.markdown(rating_to_stars(row['Rating']), unsafe_allow_html=True)
                        st.metric("Similarity score", round(row['Score'], 2))
                        col_up, col_down = st.columns(2)
                        with col_up:
                            if st.button("\U0001F44D", key=f"bm25_up_{i}"):
                                save_feedback(query, row['Product title'], "thumbs_up", mode)
                                st.success("Thanks for your feedback!")
                        with col_down:
                            if st.button("\U0001F44E", key=f"bm25_down_{i}"):
                                save_feedback(query, row['Product title'], "thumbs_down", mode)
                                st.success("Thanks for your feedback!")