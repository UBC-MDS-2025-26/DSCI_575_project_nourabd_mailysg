import streamlit as st
import pandas as pd
from src.semantic import load_index, semantic_search

st.set_page_config(page_title="Video Game Search", layout="wide")
st.title(" Video Game Product Search")


@st.cache_resource
def get_retriever():
    return load_index('data/processed/faiss_index')

vector_store = get_retriever()


mode = st.radio("Search Mode", ["Semantic", "BM25", "Hybrid"], horizontal=True)


query = st.text_input("Search for a product...")


if query:
    if mode == "Semantic":
        results = semantic_search(vector_store, query, k=3)
        rows = []
        for doc, score in results:
            rows.append({
                "Product Title": doc.metadata['item_title'],
                "Review": doc.page_content[:200] + "...",
                "Rating": doc.metadata['average_rating'],
                "Price": doc.metadata['price'],
                "Score": round(score, 4)
            })
        st.dataframe(pd.DataFrame(rows))

    elif mode == "BM25":
        results = bm25_search(bm25_retriever, query)
        st.dataframe(results[['item_title', 'text', 'average_rating', 'price', 'score']].head(3))

