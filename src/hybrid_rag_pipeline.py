from prompts import build_prompt, build_context
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from hybrid import hybrid_retriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def hybrid_rag_pipeline(query):
    # Build hybrid retriever
    retriever_hybrid = hybrid_retriever(parquet_path='data/processed/processed_data.parquet', index_path='data/processed/faiss_index', k=5)

    # Prompt template
    prompt = ChatPromptTemplate.from_template(
    """
    You must answer using ONLY the information in the context.

    - If the answer is present, extract and summarize it clearly.
    - Do NOT say "I don't know" if the answer exists in the context.
    - Only say "I don't know" if the context truly does not contain the answer.

    Context:
    {context}

    Question:
    {input}

    Answer:
    """
    )

    # LLM
    load_dotenv()

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"))

    # Pipeline
    rag_chain = (
        {
            "context": retriever_hybrid | build_context,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(query)

answer = hybrid_rag_pipeline("Nintendo switch screen protector")
print(answer)