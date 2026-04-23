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

Llama recommended Smart Boys Winter Wonderland, 51 Worldwide Games and Super Mario Maker 2, which are all suitable games for young children and are well-rated. However, Smart Boys Winter Wonderland is for Nintendo DS not Switch, which Llama missed and Qwen was able to identify in its reasoning. Because of this, Qwen correctly focused only on confirmed Switch titles (51 Worldwide Games and Super Mario Maker), making it more accurate than LLama. On the other hand, Llama's output is a lot more concise and user-friendly and it did still recommend other suitable switch games, despite the one mismatch.

**Query 2: Comfortable gaming headsets**

Both models agreed on Fantech and Rehoc as the top comfort options, both rated 5/5. Qwen produced a more structured output with clear bullet points for each product this time, but after a long prose showing us it's thought process, which is not necessary here for a user-facing app interface. They both cited comfort evidence from the reviews. Llama's output structure was also good but it recommended the Arctis 9x replacement earpads as a third option which is misleading since these are replacement parts, not a full headset, although it did flag this caveat in its response. It would have been better if it flagged this but then omitted it from it's list of recommendations. Tailoring the prompt so that the LLM does not include other similar products could be a solution for Llama here. Otherwise, the models perform quite similarly.

**Query 3:What are some good racing games for Xbox?**

Both models recommended Forza 3 and Tony Stewart's All-American Racing. Qwen also included Enthusia Professional Racing (4.7/5). It's expected that Qwen will do somehwat better given the size of the model is much bigger (32 billion paramaters as opposed to 8 billion). However Llama's more concise two product recommendation is better for a user-facing assistant. In this case, it's better to present fewer but more confident options rather than overwhelming the user with choices, including products with missing price data, which makes comaprison to other options harder. Also, the user will get the retrieved documents displayed in the app anyways, so a repition from the LLM is less preferable. The goal is instead to have the LLM return the best 1 or 2 matches with a summary of reviews/keywords from the reviews that match the query. A concise justification is also fine, which we believe LLama is better at doing.

**Query 4: Affordabe wireless controller with good battery life**

The Feirsh Switch Controller ($24.99, 4.4/5, 7-day battery life) was listed as the best match by both models. Llama also suggested the Joyork controller as a secondary option for users on a tighter budget (which it extracted from reviews, not price). Qwen's filtering excluded Joyork entirely, which makes sense since price information on this product is unknown. Again, the user can consider alternatives from the retrieved documents displayed in the app so this is not a primary concern. Overall, it seems like both models are performing similarly in terms of recommendations.


**Query 5: What gaming accessories would improve my setup under $50?**

Both models recommended the Cooler Master Mouse Pad ($17.96, 4.3/5) and Eureka Ergonomic Bundle ($29.99, 4.5/5), which match the query's budget requirement and are well-rated. Llama's response was more concise and focused, recommending exactly two products with clear 
justification. Qwen provided additional commentary on an out-of-budget product (The Handheld game console for $70.99) which is unnecessary and irrelevant to the query where the user is looking for something under 50. Llama's more direct approach in answering the query is better here.

### Key observations

- Qwen model may need a different worded prompt so that its outputs are more concise and not always walking you through every step of its thinking, through the <think> tags. This approach is not suitable for a user search system that displays both the LLM output and retrived products. The web interface would become too crowded with this model.
- Qwen performs slightly better on filtering products with missing metadata and queries that refer to specific details (e.g. platform specific games like Nintendo Switch).This quality difference is expected given its larger parameter count (32B vs 8B).
- Overall, relative to the parameter increase from Llama to Qwen, the quality difference in recommendations is marginal. They both esentially recommend the same products in most queries, whilst flagging the same issues where there is missing context/metadata
- Llama's concise format aligns better with our app's design goal: returning best product recommendation with a summary of review evidence and a brief justification, without having a very long output that is tedious for users to read.

### Chosen Model with Rationale:

Based on these results, we'll be keeping `llama-3.1-8b-instant` as the default model due to the very marginal increase in quality of product recommendations. Qwen3-32B's was better at filtering out products with missing metadata in some of the queries but it's prose-heavy outputs are not suitable for our user-facing web app, where responses are displayed alongisde the retrieved products already. Llama's concise, structured format is more desirable in our case as mentioned above. However, we acknowledge that future improvements could include prompt adjustment to improve LLama's handling of products with missing fields like price, and also better filter out irrelevant products (e.g. headphone replacement parts), so that it performs better on more complex queries.

## Step 2: Additional Feature


## Step 3: Improve Documentation and Code Quality


## Step 4: Cloud Deployment Plan

We would deploy the app on **AWS** in the following way:

### 1. Data Storage

**Raw data** (Video_Games.jsonl, meta_Video_Games.jsonl): 

- Store in **Amazon S3** bucket
- S3 is ideal for large data (our files are 500 MB and 2.6 GB) that will not be frequently accessed once the index files are built
- They are only needed during preprocessing so S3 is cost-effective and an ideal object storage for raw JSONL dumps like ours

**Processed Data** (processed_data.parquet):

- Store in S3 bucket in dedicated `processed/` folder
- Only required columns are loaded using parquet

**Vector Index** (index.faiss and index.pkl):

- Stored in S3 and downloaded to EC2 local disk at startup, then loaded into RAM
- FAISS requires a local file path and full index in RAM for fast similarity search. Loading once at startup is faster than reading from S3 on every query
- Avoids rebuilding the index on every deployment

**BM25 Index** (bm25_index.pkl and retriever.pkl):
- Stored in S3 as a pickle file and loaded into memory at startup

Since each EC2 instance loads the indexes into RAM at startup and caches them with `@st.cache_resource`, the indexes persist in memory across all user sessions on that instance, which helps avoid having to reload the index from S3 everytime there is a user request.

### 2. Compute

**Where will the app run**?

- Streamlit app would run on an **AWS EC2** instance 
- We would use `r6i.xlarge` which offers 32GB RAM, more than enough to handle the FAISS and BM25 indexes simultaneously while accounting for other overhead RAM and potential python operations
- By optimizing memory with this instance memory size, we ensure low-latency retrieval for users
- Port 8080 would be opened in the security group to allow public access

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

- For new product reviews, we would use a Python ETL script on an EC2 instance that runs every week
- This would download new JSONL data from the Amazon reviews dataset, preprocess it and append new products to the processed parquet file 
- This data would be updated in the parquet and continue being stored in AWS S3 bucket
- For large batches that make it hard for single EC2 to handle all the data, EMR with Spark would be used for distributed preprocessing.

**Keeping our Pipeline Up-to-Date**

- We would rebuild the FAISS and BM25 indexes using the same EC2 instance on a weekly or monthly schedule
- Once rebuilt, the new index files are uploaded to S3 and the running EC2 instances are restarted to load the updated indexes
- Since product catalogs don't change by the minute, periodic batch re-indexing on a weekly basis is adequate and more cost-effective than dynamic real-time index updates.