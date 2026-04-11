import streamlit as st
import pandas as pd
import sys
import os
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.semantic import load_index, semantic_search
from src.save_to_df import results_to_df

st.set_page_config(page_title="Video Game Search", layout="wide")
st.title("\U0001F3AE Video Game Product Search")

# load index on demand - separately depending on which radio button selected due to RAM restrictions
@st.cache_resource
def get_semantic():
    return load_index('data/processed/faiss_index')

@st.cache_resource
def get_bm25():
    with open('data/processed/bm25_index/bm25_index.pkl', 'rb') as f:
        bm25_index = pickle.load(f)
    # load only needed cols to avoid RAM crash
    df = pd.read_parquet('data/processed/processed_data.parquet', 
                         columns=['item_title', 'text', 'average_rating', 'parent_asin'])
    return bm25_index, df

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

        if mode == "Semantic":
            vector_store = get_semantic()
            results = semantic_search(vector_store, query, k=50)
            df = results_to_df(query, results, top_n=3)

            for i, row in df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['Product title']}")
                        st.write(row['Review'])
                    with col2:
                        st.markdown(rating_to_stars(row['Rating']), unsafe_allow_html=True)
                        st.metric("Score", round(row['Score'], 2))
                        col_up, col_down = st.columns(2)
                
                        with col_up:
                            if st.button("\U0001F44D", key=f"sem_up_{i}"):
                                save_feedback(query, row['Product title'], "thumbs_up", mode)
                                st.success("Thanks for your feedback!")
                        with col_down:
                            if st.button("\U0001F44E", key=f"sem_down_{i}"):
                                save_feedback(query, row['Product title'], "thumbs_down", mode)
                                st.success("Thanks for your feeback!")

        elif mode == "BM25":
            bm25_index, df = get_bm25()
            tokenized_query = query.split()
            scores = bm25_index.get_scores(tokenized_query) #computes scores on all 400k docs, causes memory crash especially 
            #when semantic search index also loaded into memory already 
            top_indices = scores.argsort()[::-1][:30]
            seen_asins = set()
            count = 0
            for idx in top_indices:
                row = df.iloc[idx]
                asin = row['parent_asin']
                if asin not in seen_asins:
                    seen_asins.add(asin)
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"### {row['item_title']}")
                            st.write(str(row['text'])[:200])
                        with col2:
                            st.markdown(rating_to_stars(row['average_rating']), unsafe_allow_html=True)
                            st.metric("Score", round(float(scores[idx]), 2))
                            col_up, col_down = st.columns(2)
                            with col_up:
                                if st.button("\U0001F44D", key=f"bm25_up_{idx}"):
                                    save_feedback(query, row['item_title'], "thumbs_up", mode)
                                    st.success("Thanks for your feedback!")
                            with col_down:
                                if st.button("\U0001F44E", key=f"bm25_down_{idx}"):
                                    save_feedback(query, row['item_title'], "thumbs_down", mode)
                                    st.success("Thanks for your feedback!")
                    count += 1
                if count == 3:
                    break