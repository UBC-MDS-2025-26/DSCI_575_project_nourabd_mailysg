"""
Module that implements a hybrid RAG pipeline
for the Amazon video game product search assistant.

Pipeline includes:
    - hyrbid retriever (40% BM25 and 60% semantic)
    - context builder (src/context_builder.py)
    - prompt template (src/prompts.py)
    - LLM (llama-3.1-8b-instant) called using Groq API

Functions:
    - get_retriever: Returns a hyrbid retriever for hybrid search
    - hybrid_rag_pipeline: Returns the full hybrid RAG pipeline
"""
import os
import sys
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.prompts import prompt
from src.bm25 import load_documents, load
from src.semantic import load_index
from src.context_builder import build_context
from src.hybrid import hybrid_retriever


def hybrid_rag_pipeline(retriever, query):
    # LLM
    load_dotenv()

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"))

    # Pipeline
    rag_chain = (
        {
            "context": retriever | build_context,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(query)

def get_retriever():
    vector_retriever = load_index('data/processed/faiss_index')
    bm25_retriever = load('data/processed/bm25_index', 'retriever')
    return hybrid_retriever(vector_retriever, bm25_retriever)




