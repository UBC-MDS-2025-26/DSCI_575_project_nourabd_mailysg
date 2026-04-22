# Final Milestone Discussion 

## Experimenting with different LLM models:

**Models Compared:**
- **Model 1 (from Milestone 2):** `llama-3.1-8b-instant` (Llama 3.1 8B by Meta, 8 billion parameters, accessed via Groq API)
- **Model 2:** `qwen/qwen3-32b` (Qwen3 32B by Alibaba, 32 billion parameters, accessed via Groq API)

We chose to compare Qwen3-32B because it comes from a different company and model family than Llama, which allows us to compare how different model architectures perform. It is also much larger, with 32 Billion parameters compared to the oriignal Llama model with 8 billion, so we expect it to produce more high quality reasoning in its outputs.

**Prompt:**

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