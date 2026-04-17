import os
#PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #finding project root
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.context_builder import build_context

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"))

#load existing faiss index 
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local(
    'data/processed/faiss_index',
    embeddings,
    allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5})

#prompt template


#semantic rag chain 
#temporary placeholders for prompt testing in notebook
prompt = None 
semantic_rag_chain = None


semantic_rag_chain = (
    {
        "context": retriever | build_context,
        "input": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
    )