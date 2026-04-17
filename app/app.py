import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.semantic import load_index, semantic_search
from src.bm25 import load, bm25_score
from src.save_to_df import results_to_df, top_k_to_df
from src.tokenizer import create_documents
from src.hybrid import hybrid_retriever,hybrid_results


st.set_page_config(page_title="Video Game Search", layout="wide")
st.title("\U0001F3AE Amazon Video Game Product Search")
st.markdown("Search for video game products using keyword (BM25) or semantic search.")  # ← add here
st.divider()

search, rag = st.tabs(["Search Only (Milestone 1)", "RAG Mode"])

# load index on demand - separately depending on which radio button selected due to RAM restrictions
@st.cache_resource
def get_semantic():
    return load_index('data/processed/faiss_index')

@st.cache_resource
def get_bm25():
    return load('data/processed/bm25_index', 'bm25_index')

@st.cache_resource
def get_docs():
    return create_documents('data/processed/processed_data.parquet')

@st.cache_resource
def get_bm25_retriever():
    return load('data/processed/bm25_index', 'retriever')

@st.cache_resource
def get_hybrid(_vector_retriever, _bm25_retriever):
    return hybrid_retriever(_vector_retriever, _bm25_retriever)

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
        
# Search tab
with search :
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
                bm25_index = get_bm25()
                docs = get_docs()
                results = bm25_score(bm25_index, query, docs, count=1, query_nb=1)
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

# RAG tab :
with rag :
    # query input box
    rag_query = st.text_input("Search for a product...", placeholder="e.g. Headphones")

    if rag_query:
        with st.spinner("Searching..."):
            vector_store = get_semantic()
            bm25_retriever = get_bm25_retriever()
            retriever = get_hybrid(vector_store, bm25_retriever)
            results = hybrid_results(rag_query, retriever)
            df = top_k_to_df(rag_query, results, top_n=3)

            st.markdown(f"**Top {len(df)} results for:** *{rag_query}*")

            for i, row in df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['Product title'].title()}")
                        st.markdown("**Review:**")
                        st.write(row['Review'])
                    with col2:
                        st.markdown(rating_to_stars(row['Rating']), unsafe_allow_html=True)
                        col_up, col_down = st.columns(2)
                        with col_up:
                            if st.button("\U0001F44D", key=f"hybrid_up_{i}"):
                                save_feedback(rag_query, row['Product title'], "thumbs_up", mode='hybrid')
                                st.success("Thanks for your feedback!")
                        with col_down:
                            if st.button("\U0001F44E", key=f"hybrid_down_{i}"):
                                save_feedback(rag_query, row['Product title'], "thumbs_down", mode='hybrid')
                                st.success("Thanks for your feedback!")

