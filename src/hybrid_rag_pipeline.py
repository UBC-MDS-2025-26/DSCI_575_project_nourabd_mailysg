"""
Module that implements a hybrid RAG pipeline
for the Amazon video game product search assistant.

Pipeline includes:
    - hybrid retriever (40% BM25 and 60% semantic)
    - context builder (src/context_builder.py)
    - prompt template (src/prompts.py)
    - LLM (llama-3.1-8b-instant) called using Groq API
    - agent that uses the LLM and a web search tool (src/tools.py)

Functions:
    - get_retriever: Returns a hybrid retriever for hybrid search
        - Run bm25.py and semantic.py scripts before pipeline to ensure
        that faiss_index and retriever are saved
    - hybrid_rag_pipeline: Returns the full hybrid RAG pipeline
"""
import os
import sys
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain.agents import create_agent

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.prompts import prompt
from src.bm25 import load
from src.semantic import load_index
from src.context_builder import build_context
from src.hybrid import hybrid_retriever
from src.tools import web_search
from src.config import FAISS_INDEX, BM25_INDEX


def get_retriever():
    """Return hybrid retriever"""
    vector_retriever = load_index(FAISS_INDEX) 
    bm25_retriever = load(BM25_INDEX, 'retriever')
    return hybrid_retriever(vector_retriever, bm25_retriever)


def hybrid_rag_pipeline(retriever, query):
    """Return hybrid RAG pipeline that can call on a web search tool"""

    load_dotenv()
    
    # LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"))
    
    # agent
    agent = create_agent(
            model=llm,
            tools=[web_search],
            system_prompt="""
            You are a helpful Amazon video game product shopping assistant.
            ONLY use the web_search tool when the user explicitly asks for 
            current or up-to-date information.
            """
            )

    # Pipeline
    rag_chain = (
        {
            "context": retriever | build_context,
            "input": RunnablePassthrough()
        }
        | prompt
        | agent
        | RunnableLambda(lambda x: x["messages"][-1].content)
        | StrOutputParser()
    )
    return rag_chain.invoke(query)

# To run the pipeline uncomment the following lines:
# retriever = get_retriever()
# print(hybrid_rag_pipeline(retriever, 'single player game'))


