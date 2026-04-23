"""
Module that implements a semantic RAG pipeline
for the Amazon video game product search assistant.

Pipeline includes:
    - FAISS semantic retriever
    - context builder (src/context_builder.py)
    - prompt template (src/prompts.py)
    - LLM (llama-3.1-8b-instant) called using Groq API

Functions:
    - get_retriever: Returns a FAISS retriever for semantic search
    - get_semantic_rag_chain: Returns the full semantic RAG pipeline
"""
import os
import sys

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.context_builder import build_context
from src.prompts import prompt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #finding project root

load_dotenv()

#llm API call
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"))

#embeddings + vector store 
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local(
    os.path.join(PROJECT_ROOT, 'data/processed/faiss_index'),
    embeddings,
    allow_dangerous_deserialization=True
)

#retriever
def get_retriever(k=5): #using top 5 docs
    """Return FAISS retriever"""
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k})

#semantic rag chain 
def get_semantic_rag_chain():
    """Return semantic RAG chain"""
    retriever = get_retriever()
    return (
        {
            "context": retriever | build_context,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
