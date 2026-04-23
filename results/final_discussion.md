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

**Query 4: Affordable wireless controller with good battery life**

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

### Option 2 - Tool integration
We decided to integrate a web search tool (Tavily API) to the hybrid RAG pipeline (see [src/hybrid_rag_pipeline.py](../src/hybrid_rag_pipeline.py)). To do this, we added an agent to the RAG pipeline that calls on the tool to get missing or up-to-date information about products it recommends (see [src/tools.py](../src/tools.py) for web search tool implementation).

### Attempt 1 - Adjusted prompt:
We first tried to let the agent decide when to use the web tool by only adding the tool calling conditions to the prompt (no added logic to the [`web_search`](../src/tools.py) function).
>Prompt used :
>
>You are a helpful Amazon video game product shopping assistant.
>The context contains real Amazon product reviews and metadata (product title, rating, price, description etc.).
>
>- Use the context first before anything else
>- Recommend specific products that match the user's query (AT MOST 3 products)
>- Use web_search for additional details on products already in the context (e.g release year)
>- ONLY recommend products from the web when the user explicitly uses words like "new", "latest", "recent"
>- Support your recommendation with concise and relevant evidence from the reviews and ratings
>- Only say you don't know if the context truly does not contain relevant information

#### **Query 1 : new release single player game**

>*Response:*
>
>  The Defiant 
>-  Price:  $59.99
>-  Rating:  4.7/5
>-  Release year:  2026
>-  Why it matches:  The Defiant is a new release single player game that offers a gripping story and challenging gameplay.
>
> STALKER 2 Cost of Hope 
>-  Price:  $59.99
>-  Rating:  4.5/5
>-  Release year:  2026
>-  Why it matches:  STALKER 2 Cost of Hope is a new release single player game that offers a deep experience with a personalized story and challenging gameplay.
>
> Alan Wake 2 
>-  Price:  $59.99
>-  Rating:  4.5/5
>-  Release year:  2025
>-  Why it matches:  Alan Wake 2 is a new release single player game that offers a gripping story and devastatingly effective art style, making it one of the best single-player games of recent years.

*Discussion:* All 3 recommended products meet the user's query requirements (new release and single player). However some product information seems to have been hallucinated. For example, the release date and price given for the Defiant video game are false (the game has not been released yet and no price is listed). Similarly, the release date for the third result is not accurate (the real release date is 2023). 

#### **Query 2 : pink wireless controller**

>*Response:*
>
> Xbox 360 Wireless Controller - Pink 
>-  Price:  $42.87
>-  Rating:  4.0/5
>-  Release year:  2007
>-  Why it matches:  The product matches the user's query because it is a pink wireless controller for the Xbox 360, which is a type of gaming console that the user may be interested in. The product's price is also listed as $42.87, and it has a rating of 4.0 out of 5 stars.

*Discussion:* The recommended product matches the user query requirements and the real product can be found here (can be found here [https://www.amazon.ca/Xbox-360-Wireless-Controller-Pink/dp/B000VSDON6](https://www.amazon.ca/Xbox-360-Wireless-Controller-Pink/dp/B000VSDON6)).

#### **Query 3 : recent single player games under 20$**

>*Response:*
>
> Expedition 33 
>-  Price:  $19.99
>-  Rating:  4.5/5
>-  Release year:  (2022)
>-  Why it matches:  A single-player focused survival game with a strong narrative and engaging gameplay.
>
> Bloodborne 
>-  Price:  $19.99
>-  Rating:  5/5
>-  Release year:  (2015)
>-  Why it matches:  A challenging action RPG with a dark atmosphere and intense combat.
>
> RE4 remake 
>-  Price:  $19.99
>-  Rating:  4.5/5
>-  Release year:  (2023)
>-  Why it matches:  A re-imagining of the classic Resident Evil 4 game with updated graphics and gameplay.
>
> Sekiro (Note: This game is not under 20$ but I have to recommend it) 
>-  Price:  $59.99
>-  Rating:  4.5/5
>-  Release year:  (2019)
>-  Why it matches:  A challenging action-adventure game set in feudal Japan with a strong focus on stealth and strategy.

*Discussion:* The response contains 4 product recommendations when the prompt specifically mentions at most 3 should be added and the extra recommendation does not match the user's price requirement. The user query also specifies they are looking for recent games but neither Sekiro (2019) or Bloodborne (2015) can be considered as recent.

#### Overall Attempt Results
Overall, we have that the pipeline works better on simple queries (query 2) than more complex queries with many constraints (like price limits or recency constrains). We also have that the agent either hallucinates (gives false information about products) or does not follow all the instructions set out in the prompt. Hence, letting the agent decide when to call the tool is not the best solution.

### Attempt 2 - Logic for tool calling:
We then decided added in a condition to the [`web_search`](../src/tools.py) function that only calls the web search API if the user explicitly asks for up-to-date information (words like "new", "latest", "recent"). We also pass an enriched query (`'best video game {query} 2026'`)to the web search to add more context as well as limit the domains that can be searched to ones related to video game products ([metacritic.com](https://www.metacritic.com), [ign.com](https://www.ign.com/ca), [store.steampowered.com](https://store.steampowered.com), [amazon.com](https://www.amazon.com)). The original prompt was used here (from Milestone 2).

#### **Query 1 : new release single player game**

>*Response:*
>
>  Based on the context, I would recommend the following new release single player game:
>
> * **Darwin's Paradox** - April 2 - (PS5, Switch 2, Xbox, PC)
> * **People of Note** - April 7 - (PS5, Switch 2, Xbox, PC)
> * **ChainStaff** - April 8 - (PS5, Switch, Xbox, PC)
>
>These games seem to fit the user's query for a new release single player game, with no mention of multiplayer or co-op gameplay.

*Discussion:* All 3 recommended products meet the user's query requirements (new release and single player). The details about the products that are given are also accurate. 

#### **Query 2 : pink wireless controller**

>*Response:*
>
> Based on the context, I would recommend the following products that match the user's query:
>
>1. **Xbox 360 Wireless Controller Pink**: This product has a high rating of 4.0/5, is priced at $42.87, and is described as a "high-performance wireless gaming" controller >with a 30-foot range and up to 40 hours of life. Many reviewers have praised its quality, durability, and aesthetics, with one reviewer stating it's "worth it" and another >saying it's the "perfect controller for gamer girls."
>2. **Ralan Pink Wireless Controller**: This product has a high rating of 4.6/5, is priced at $29.99, and is described as a "super cute controller" with colorful LED lighting >and a smooth feel. Reviewers have praised its quality, feel, and versatility, with one reviewer stating it's the "best feel out of most gaming controllers" they've bought.
>
>Both of these products are wireless controllers that match the user's query, and they have high ratings and positive reviews from customers.

*Discussion:* Both the products are good matches for the user query.

#### **Query 3 : recent single player games under 20$**

>*Response:*
>
>Based on the context provided, I would recommend the following recent single player games under $20:
>
>* Championship Manager 2008 UK (price: $5 or less)
>* Medieval Crafter: Blacksmith (mentioned in the web_search results)
>* Masters of Albion (mentioned in the web_search results)
>* Tides of Tomorrow (mentioned in the web_search results)
>* DRAGON BALL FighterZ - DAIMA Pack (mentioned in the web_search results, although the price is not specified)
>
>These games meet the criteria of being recent single player games and are available for under $20. However, please note that the prices may vary depending on the platform and availability.

*Discussion:* Not all the query requirements (recent, under 20$, single player) are met by the products. For example, the Tides of Tomorrow and Masters of Albion (from the web search) are above the price cap of 20$. Similarly, the Championship Manager is not a recent game. However, both DRAGON BALL FighterZ - DAIMA Pack and Medieval Crafter: Blacksmith are great matches for the query.

#### Overall Attempt Results
Overall, we have that the pipeline quite well on simple queries (Query 2) and manages to give information that is more reliable than previously. While it does handle simple constraints quite well (Query 1), when we start combining multiple requirements, the recommendations start suffering (Query 3).

### Conclusion
We have that the web search tool added to the pipeline allows users to access up-to-date information about products. This can be especially important for video games since it is quite common for users to be more interested in the latest releases.

## Step 3: Improve Documentation and Code Quality
### Documentation Update
- Added instructions for creating Tavily API ([README](../README.md#setting-up))
- Added a usage example of the app ([README](../README.md#usage-example))
- Added description of web search implementation ([README](../README.md#web-search-tool))
- Added workflow descriptions ([README](../README.md#rag-workflow))
- Added instructions for local testing ([README](../README.md#local-testing-with-sample-of-dataset))

### Code Quality Changes
- Remove temporary files (`requirements.txt` and `retrieval_metrics.py`)
- Added a [config](src/config.py) file and removed hardcoded paths
- All functions include a docstrings (already implemented in previous Milestones)
- Updated [environment.yml](environment.yml) with new packages (tavily-python)

## Step 4: Cloud Deployment Plan

We would deploy the app on **AWS** in the following way:

### 1. Data Storage

**Raw data** (Video_Games.jsonl, meta_Video_Games.jsonl): 

- Store in **Amazon S3** bucket (e.g. `s3://videogame-search/raw/`)
- S3 is ideal for large data (our files are 500 MB and 2.6 GB) that will not be frequently accessed once the index files are built
- They are only needed during preprocessing so S3 is cost-effective and an ideal object storage for raw JSONL dumps like ours

**Processed Data** (`processed_data.parquet` ~ 129K products after processing):

- Store in S3 bucket in dedicated `processed/` folder `s3://videogame-search/processed/`
- Parquet makes it so that only required columns are read into memory, which is also less computationally expensive

**Vector Index** (index.faiss and index.pkl):

- Stored in S3 (`s3://videogame-search/indexes/faiss/`) and downloaded to EC2 local disk at startup, then loaded into RAM
- FAISS requires a local file path and full index in RAM for fast similarity search. Loading once at startup is faster than reading from S3 on every query
- Avoids rebuilding the index on every deployment

**BM25 Index** (bm25_index.pkl and retriever.pkl):
- Stored in S3 as a pickle file and loaded into memory at startup(`s3://videogame-search/indexes/bm25/`)
- Storing both the raw BM25Okapi object and the LangChain BM25Retriever separately allows the app to use the retriever for hybrid RAG without rebuilding from the documents

Since each EC2 instance loads the indexes into RAM at startup and caches them with `@st.cache_resource`, the indexes persist in memory across all user sessions on that instance, which helps avoid having to reload the index from S3 everytime there is a user request.

### 2. Compute

**Where will the app run**?

- Streamlit app would run on an **AWS EC2** instance 
- We would use `r6i.xlarge` which offers 32GB RAM, more than enough to handle the FAISS (198.2 MB for faiss & 2.26 GB for pkl) and BM25 indexes (4.87 MB for index & 2.75 GB for retriever) simultaneously while accounting for other overhead RAM and potential python operations
- By optimizing memory with this instance size, we ensure low-latency retrieval for users

**How will we handle multiple users?**

- To handle multiple concurrent users, we would deploy the app behind an **AWS Application Load Balancer**, which would distribute traffic across multiple EC2 instances.
- We would use **Auto-Scaling** so that we have additional EC2 instances running under high load
- Each instance loads its own copy of the indexes from S3 at app startup, which will help multiple users run the workflow/query the app at the same time without interference

**How will we handle LLM inference?**

- In our case, we would continue using the **Groq API**(`llama-3.1-8b-instant`)for LLM inference rather than self-hosting a LLM model
- This avoids the cost and complexity of running a GPU instance all the time, for a tool that is only used when a user queries
- Groq API provides fast inference with a pay-per-use model, which is more cost-effective for a recommendation tool like this one that has  variable levels of traffic
- Alternatively, if there is an issue of slow response times, we could self-host the model on **AWS SageMaker**

### 3. Streaming/Updates

**Incorporating New Products in Production**

- For new product reviews, they would be ingested via a weekly **AWS Glue** ETL job that:
    1. Downloads new JSONL files from the Amazon Reviews dataset to S3
    2. Runs the preprocessing pipeline (`preprocess.py`) to update the parquet
    3. Uploads the updated parquet to `s3://videogame-search/processed/`
- For large batches that make it hard for a single EC2 to handle all the data, EMR with PySpark would be used for distributed preprocessing.

**Keeping our Pipeline Up-to-Date**

- We would rebuild the FAISS and BM25 indexes on a weekly schedule via an EC2 instance, by running `semantic.py` and `bm25.py` on the latest parquet from S3
- Once rebuilt, new index files are uploaded to S3 under a versioned path (e.g. s3://videogame-search/indexes/2026-04-22/)
- EC2 instances are restarted to load the updated indexes
- Since product catalogs don't change by the minute, periodic batch re-indexing on a weekly basis is adequate and more cost-effective than dynamic real-time index updates