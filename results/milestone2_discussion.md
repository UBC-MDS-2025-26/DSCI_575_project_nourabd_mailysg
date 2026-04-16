## LLM Model Choice Rationale

**Model:** `llama-3.1-8b-instant` with Groq API

We chose to leverage the Groq API due to hardware restrictions that come with running our data. We are operating using 8-16 GB RAM computers, a lot of which will already be used up by the FAISS and BM25 index files, so we anticipated that loading even a small model locally would be problematic. With the Groq API, the model can run on Groq's servers rather than locally so local RAM will not be consumed, regardless of the model's size. 

Llama 3.1 8B uses 8 billion paramaters, which is fairly high compared to other HuggingFace models, thus, the model will likely produce more accurate, contextually aware video game product recommendations.

Additionally, running the RAG pipeline with an API means that others can reproduce it without needing a GPU, they simply need a free API token, which is easy to get. Refer to the [Readme](https://github.com/UBC-MDS/DSCI_575_project_nourabd_mailysg) for instructions on how to obtain your Groq API key.