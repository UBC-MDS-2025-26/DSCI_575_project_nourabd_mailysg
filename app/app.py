import streamlit as st
import pandas as pd
import sys
import os
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.semantic import load_index, semantic_search
from src.save_to_df import results_to_df

st.set_page_config(page_title="🎮 Video Game Search", layout="wide")
st.title("🎮 Video Game Product Search")

# ── Load indexes on demand ────────────────────────────────────────
@st.cache_resource
def get_semantic():
    return load_index('data/processed/faiss_index')

@st.cache_resource
def get_bm25():
    with open('data/processed/bm25_index/bm25_index.pkl', 'rb') as f:
        bm25_index = pickle.load(f)
    df = pd.read_parquet('data/processed/processed_data.parquet')
    return bm25_index, df

# ── Search mode selector ──────────────────────────────────────────
mode = st.radio("Search Mode", ["Semantic", "BM25"], horizontal=True)

# ── Query input ───────────────────────────────────────────────────
query = st.text_input("🔍 Search for a product...")

# ── Results ───────────────────────────────────────────────────────
if query:
    with st.spinner("Searching..."):

        if mode == "Semantic":
            vector_store = get_semantic()
            results = semantic_search(vector_store, query, k=50)
            df = results_to_df(query, results, top_n=3)
            for _, row in df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['item_title']}")
                        st.write(row['review'])
                    with col2:
                        st.metric("Rating", f"⭐ {row['rating']}")
                        st.metric("Score", row['score'])

        elif mode == "BM25":
            bm25_index, df = get_bm25()
            tokenized_query = query.split()
            scores = bm25_index.get_scores(tokenized_query)
            top_indices = scores.argsort()[::-1][:3]
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
                            st.metric("Rating", f"⭐ {row['average_rating']}")
                            st.metric("Score", round(scores[idx], 4))
                    count += 1
                if count == 3:
                    break