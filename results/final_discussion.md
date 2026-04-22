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

Llama recommended Smart Boys Winter Wonderland, 51 Worldwide Games and Super Mario Maker 2, all suitable games for young children and well-rated. However, Smart Boys Winter Wonderland is for Nintendo DS not Switch, which Llama missed and Qwen was able to identify in its reasoning. Because of this, Qwen correctly focued only on confirmed Switch titles (51 Worldwide Games and Super Mario Maker), making it more accurate than LLama. On the other hand, Llama's output is a lot more concise and user-friendly and it did still recommend other suitable switch games.

**Query 2: Comfortable gaming headsets**

Both models agreed on Fantech and Rehoc as the top comfort options, both rated 5/5. Qwen produced a more structured output with clear bullet points for each product this time, but after a long prose showing us it's thought process, which is not necessary here for a user-facing app interface. They both cited comfort evidence from the reviews. Llama's structure was also good but it recommended the Arctis 9x replacement earpads as a third option which is misleading since these are replacement parts, not a full headset, although it did flag this caveat in its response. Tailoring the prompt so that the LLM does not include other similar products could be a solution for Llama here. Otherwise, the models perform quite similarly.

**Query 3:What are some good racing games for Xbox?**

Both models recommended Forza 3 and Tony Stewart's All-American Racing. Qwen also included Enthusia Professional Racing (4.7/5) which Llama missed. It's expected that Qwen will do somehwat better given the size of the model is much bigger (32 billion paramaters as opposed to 8 billion). However Llama's more concise two product recommendation is better for a user-facing assistant. In this case, it's better to present fewer but more confident options rather 
than overwhelming the user with choices including products with missing price that can't be easily compared to other options. Also, the user will get the retrieved documents displayed in the app anyways, so a repition from the LLM is less preferable. The goal is instead to have the LLM return the best with a summary of reviews alongisde a concise justification, which we believe LLama is better at doing.

**Query 4: Affordabe wireless controller with good battery life**

The Feirsh Switch Controller ($24.99, 4.4/5, 7-day battery life) was listed as the best match by both models. Llama also suggested the Joyork controller as a secondary option for users on a tighter budget (which it extracted from reviews, not price). Qwen's filtering excluded Joyork entirely, which makes sense since price information on this product is unknown. Again, the user can consider alternatives from the retrieved documents displayed in the app so this is not a primary concern. Overall, it seems like both models are performing similarly in terms of recommendations.


**Query 5: What gaming accessories would improve my setup under $50?**

Both models recommended the Cooler Master Mouse Pad ($17.96, 4.3/5) and Eureka Ergonomic Bundle ($29.99, 4.5/5), which match the query's budget requirement and are well-rated. Llama's response was more concise and focused, recommending exactly two products with clear 
justification. Qwen provided additional commentary on an out-of-budget product (The Handheld game console for $70.99) which is unnecessary. Llama's more direct approach in answering the query is better here.

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