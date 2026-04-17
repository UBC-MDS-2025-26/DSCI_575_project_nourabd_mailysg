## LLM Model Choice Rationale

**Model:** `llama-3.1-8b-instant` with Groq API

We chose to leverage the Groq API due to hardware restrictions that come with running our data. We are operating using 8-16 GB RAM computers, a lot of which will already be used up by the FAISS and BM25 index files, so we anticipated that loading even a small model locally would be problematic. With the Groq API, the model can run on Groq's servers rather than locally so local RAM will not be consumed, regardless of the model's size. 

Llama 3.1 8B uses 8 billion paramaters, which is fairly high compared to other HuggingFace models, thus, the model will likely produce more accurate, contextually aware video game product recommendations.

Additionally, running the RAG pipeline with an API means that others can reproduce it without needing a GPU, they simply need a free API token, which is easy to get. Refer to the [Readme](https://github.com/UBC-MDS/DSCI_575_project_nourabd_mailysg) for instructions on how to obtain your Groq API key.


## Prompt Experimentation

3 prompts were tested in [milestone2_rag.ipynb](https://github.com/UBC-MDS/DSCI_575_project_nourabd_mailysg/blob/main/notebooks/milestone2_rag.ipynb).

From this exploration, we decided that prompt 2 produced the best quality output for our users. It provides better justification, comparison against other products and a summary of the reviews that are relevant to the user's query, compared to prompt 1, which used minimal instructions, and ouputs less information but still recommends the same product. The additional information from prompt 2 is a quick useful summary which allows the user to understand how the game compares to others, instead of manually reviewing the retrieved documents themselves. However, if they wish to do so, the top 3 products will still be displayed in the app.

Prompt 3 included an additional instruction 'recommend up to 3 products that match the user's query'. This is useful for queries that ask for multiple products however, it recommends top 3 products even when a query asks for 'the best product' which could cause more confusion and require more manual effort from the user when deciding which product to choose.

Prompt 2 provides the best balance of specificity, concise comparison with evidence and a good quality product recommendation.

### Chosen Prompt

> You are a helpful Amazon video game product shopping assistant.
> Answer the question using ONLY the information in the context given.
> The context contains real Amazon product reviews and metadata (product title, rating, price, description etc.).
> 
> - Recommend specific products that match the user's query
> - Support your recommendation with evidence from the reviews and ratings
> - Consider important product aspects like price and rating
> - Be concise and relevant with your recommendations
> - Only say you don't know if the context truly does not contain relevant information

To view all prompts, refer to [milestone2_rag.ipynb](https://github.com/UBC-MDS/DSCI_575_project_nourabd_mailysg/blob/main/notebooks/milestone2_rag.ipynb).