"""
Module that creates a web search tool to be used in the hybrid RAG pipeline (src/hybrid_rag_pipeline.py)
"""

import os
from tavily import TavilyClient
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def web_search(query: str) -> str:
    """ONLY use this tool when the user query contains words like 
    "new", "latest" or "recent".
    """
    if any(word in query.lower() for word in ["new", "latest", "recent"]):
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        enriched_query = f'best video game {query} 2026'
        results = tavily_client.search(enriched_query, max_results=3, include_domains=["metacritic.com", "ign.com", "store.steampowered.com", "amazon.com"])
        snippets = [r["content"] for r in results.get("results", [])]
        return "\n".join(snippets)[:100]
    return "Look in context"
