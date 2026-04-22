# Final Discussion 

## Step 1: Improve Your Workflow

### Dataset Scaling

- Our workflow uses all unique video game products (129,039 unique products after preprocssing) from the Amazon Datset. We implemneted this in Milestone 2
- We also added a sampling option for low RAM machines, see README for more instructions.

### LLM Experiment

**Models Compared:**
- **Model 1 (from Milestone 2):** `llama-3.1-8b-instant` (Llama 3.1 8B by Meta, 8 billion parameters, accessed via Groq API)
- **Model 2:** `qwen/qwen3-32b` (Qwen3 32B by Alibaba, 32 billion parameters, accessed via Groq API)

We chose to compare Qwen3-32B because it comes from a different company and model family than Llama, which allows us to compare how different model architectures perform. It is also much larger, with 32 Billion parameters compared to the oriignal Llama model with 8 billion, so we expect it to produce more high quality reasoning in its outputs.

**Prompt Used:**

Both models were tested with identical retrieved context and the following prompt (same as Milestone 2 prompt):

> You are a helpful Amazon video game product shopping assistant.
> Answer the question using ONLY the information in the context given.
> The context contains real Amazon product reviews and metadata (product title, rating, price, description etc.).
> 
> - Recommend specific products that match the user's query
> - Support your recommendation with evidence from the reviews and ratings
> - Consider important product aspects like price and rating
> - Be concise and relevant with your recommendations
> - Only say you don't know if the context truly does not contain relevant information

To see both model outputs in detail on all 5 queries, naviagte to `notebooks/final_exploration.ipynb`

### Result Comparison

**Query 1: What Nintendo Switch games are good for young children?**

It seems like both models struggled with this query, with limited information on nintendo switch games suitable for children in the data. However, the Qwen model provides more of a justification and walks you through it's thinking (even has <think> tags), flagging that most results were for Nintendo DS or Xbox instead of Switch, before it recommends Mario Kart 8. Llama is better at being concise and saying that it doesnt have enough information or lacks context, which i feel is more appropriate for a user-facing assistant. It also suggested Mario Kart 8, but with some hesitancy. So, although Qwen's transparency is nice and detailed, it's not suitable for the purpose of this app.

**Query 2: Comfortable gaming headsets**

Both models recommended similar products (afuntablue and huhd headsets). Qwen again showed explicit reasoning before its answer, producing a more informative response and clearly distinguishing between full headset options and replacement earpads. Llama's response was also good but included a strange comment about replacement earpads being a "premium option", yet mentioning it is priced at $11.98. Overall, both suggested the same set of suitable products, matching the user's query. However, similar to query 1's output, the exessive detail in Qwen's response is unappealing. LLama states the product, it's overall rating, a summary of what the reviews are saying and any additional comments at the end, whereas Qwen's output is more prose-like and tedious to read.

**Query 3:What are some good racing games for Xbox?**

Both models recommended TrackMania Turbo as a good Xbox racing game. Llama also suggested The Need for Speed as an Option, but flagged that there is no Xbox version available, suggesting it for users who may have an alternative gaming platform. Qwen also flagged this but didn't recommend it, it's final recommendation only had TrackMania Turbo for Xbox One, so it performed better than Llama here, in terms of matching the user's query on racing games for Xbox. Llama was again more concise but less accurate. This is expected with the parameter difference between the models (8 billion vs 32 billion).

**Query 4: Affordabe wireless controller with good battery life**

The Feirsh Switch Controller was recommended as the best match by both LLama and Qwen. Etpark Switch Wireless Pro Controller was also suggested by Llama even though its price is not listed, although reviews do praise its battery life, so not all aspects of the query were captured here by LLama. Qwen's reasoning showed that it didn't recommend EtPark because affordability was unclear, so it again did better in this aspect.

**Query 5: What gaming accessories would improve my setup under $50?**

The Eureka Ergonomic Gaming Desk Setup Accessories Bundle ($29.99, 4.5/5) is communicated as the most suitable option by both models. Qwen lists many other alternatives but also flags them as having low ratings or missing price data. Similarly, Llama included the Enhance GXM3 Gaming Mouse despite its price being unavilable (same issue as previous query).

### Key observations

- Qwen model may need a different worded prompt so that its outputs are more concise and not always walking you through every step of its thinking, which is not suitable for a user search system that displays both LLM output and retrived products. The web interface would become too crowded with this approach. Additionally, the <think> tags are also not suitable for a user-facing app and may be confusing.
- Qwen seems slightly better on more complex queries.
- Llama was more concise in acknowledging limitations and recommending procuts. However, it could benefit from prompt adjustment, where instead of acknowleding limitations and still recommending products, the products with missing metadata are simply filtered out.
- In terms of accuracy, Qwen is slightly better and more focused with its recommendations, but this is expected given it has many more parameters (32 billion).
- For the parameter increase, the quality difference is marginal, they both esentially recommend the same products in most queries, whilst flagging the same issues where there is missing context/metadata.

### Chosen Model with Rationale:

Based on these results, we'll be keeping `llama-3.1-8b-instant` as the default model due to the very marginal increase in suitability amongst product recommendations. Qwen3-32B's was better at filtering out products with missing metadata in some of the queries but it's prose-heavy outputs are not suitable for our user-facing web app, where responses are displayed alongisde the retrieved products already. Llama's concise, structured format is more desirable in our case. However, we acknowledge that future improvements could include prompt adjustment to improve LLama's handling of proudcts with missing fields like price, so that it performs better on more complex queries. 

## Step 2: Additional Feature


## Step 3: Improve Documentation and Code Quality


## Step 4: Cloud Deployment Plan

We would deploy the app on **AWS** in the following way:

### 1. Data Storage

**Raw data** (Video_Games.jsonl, meta_Video_Games.jsonl): 

- Store in **Amazon S3** bucket
- S3 is ideal for large data that will not be frequently accessed once the index files are built
- Cost-effective and durable object storage for raw JSONL dumps like our raw files

**Processed Data** (processed_data.parquet):

- Store in S3 bucket in dedicated `procssed/` folder
- Only required columns are loaded using parquet

**Vector Index** (index.faiss and index.pkl):

- Also Stored in S3 and loaded into EC2 local disk memory at app startup
- FAISS requires full index in RAM for fast similarity search. Loading from EC2 instance's local disk is faster than reading from s3 on every user query.
- Avoids rebuilding index on every deployment

**BM25 Index** (bm25_index.pkl and retriever.pkl)
- Stored in S3 as a pickle file and loaded into memory at startup

Both indexes are cached in memory using Streamlit's `@st.cache_resource` to avoid reloading on every user query request.

### 2. Compute

**Where will the app run**?

- Streamlit app would run on an **AWS EC2** instance 
- We would use `r6i.xlarge` which offers 32GB RAM, more than enough to handle the FAISS and BM25 indexes simultaneously while accounting for other overhead RAM and potential python operation
- By optimizing memory with this instance memory size, we ensure low-latency retrieval for users

**How will we handle multiple users?**

- To handle multiple concurrent users, we would deploy the app behind an **AWS Application Load Balancer** 
- We would use **Auto-Scaling** so that we have additional EC2 instances running under high load
- Each instance loads its own copy of the indexes from S3 at app startup, which will help multiple users run the workflow/query the app at the same time without interference

**How will we handle LLM inference?**

- In our case, we would continue using the **Groq API** for LLM inference rather than self-hosting a LLM model
- This avoids the cost and complexity of running a GPU instance all the time
- Groq API provides fast inference with a pay-per-use model, which is more cost-effective for a recommendation tool like this one that has  variable levels of traffic
- Alternatively, if there is an issue of slow response times, we could self-host the model on **AWS SageMaker**

### 3. Streaming/Updates

**Incorporating New Products in Production**

- For new product reviews, we would use an ETL job that runs every week, using **AWS Glue**
- This would download new JSONL data from the Amazon reviews dataset, preprocess it and append new products to the processed parquet file 
- This data would be updated in the parquet and continue being stored in AWS S3 bucket

**Keeping our Pipleine Up-to-Date**

- We would rebuild the FAISS and BM25 indexes from scratch on a weekly or monthly basis using an **AWS Batch** job
- Once rebuilt, the new index files are uploaded to S3 and the running EC2 instances are restarted to load the updated indexes