import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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

#context building
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

#prompt template 
