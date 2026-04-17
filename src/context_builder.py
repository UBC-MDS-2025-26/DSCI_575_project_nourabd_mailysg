"""
A module for building context from retrieved documents for RAG pipelines.

Functions:
    build_context: Converts retrieved LangChain documents into structured 
    prompt-ready context block for the LLM.
"""

def build_context(docs):
    """Convert retrieved documents into a prompt ready context block"""
    return "\n\n".join(
        f"Product: {doc.metadata.get('item_title', 'N/A')}\n"
        f"Rating: {doc.metadata.get('average_rating', 'N/A')}/5\n"
        f"Price: {doc.metadata.get('price', 'N/A')}\n"
        f"Description: {doc.metadata.get('description', 'N/A')[:200]}\n"
        f"Review Title: {doc.metadata.get('review_title', 'N/A')}\n"
        f"Review: {doc.metadata.get('text', 'N/A')[:300]}"
        for doc in docs)