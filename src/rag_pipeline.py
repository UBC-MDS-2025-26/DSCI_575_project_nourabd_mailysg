import os
#PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #finding project root
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"))