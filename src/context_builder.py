"""
A module for building context from retrieved documents for RAG pipelines.

Functions:
    build_context: Converts retrieved LangChain documents into structured 
    prompt-ready context block for the LLM.
"""

def build_context(docs, max_chars=3000):
    """Convert retrieved documents into a prompt ready context block"""
    context = []
    total_length = 0

    for doc in docs:
        context_parts = (f"Product: {doc.metadata.get('item_title', 'N/A')}\n"
        f"Rating: {doc.metadata.get('average_rating', 'N/A')}/5\n"
        f"Price: {doc.metadata.get('price', 'N/A')}\n"
        f"Description: {doc.metadata.get('description', 'N/A')[:150]}\n"
        f"Review Title: {doc.metadata.get('review_title', 'N/A')}\n"
        f"Review: {doc.metadata.get('text', 'N/A')[:200]}")

        if total_length + len(context_parts) > max_chars:
            break   

        context.append(context_parts)
        total_length += len(context_parts)               
    
    return "\n\n".join(context)