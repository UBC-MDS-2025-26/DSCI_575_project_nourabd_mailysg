"""
Module that creates a web search tool to be used in the hybrid RAG pipeline (src/hybrid_rag_pipeline.py)
"""

import os
from tavily import TavilyClient
from langchain.tools import tool
from dotenv import load_dotenv


@tool
def web_search(query, max_results=3):
    """ONLY use this to get find missing information (price, release date) for a product
    that already exists in the context. ONLY recommend a product from the web if the user's 
    query explicitly requests up-to-date information .
    """
    load_dotenv()
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    results = tavily_client.search(query, max_results=max_results)
    snippets = [r["content"] for r in results.get("results", [])]

    return "\n".join(snippets)



