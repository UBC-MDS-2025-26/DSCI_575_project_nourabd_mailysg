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

##  RAG Evaluation

To view all RAG query results, refer to [milestone2_rag.ipynb](https://github.com/UBC-MDS/DSCI_575_project_nourabd_mailysg/blob/main/notebooks/milestone2_rag.ipynb).

### 1. **Query** : nintendo switch screen protector
**RAG response:**
> Based on the given context, I would recommend the following products:
> 1. **evoretro Screen Protector Compatible for Nintendo Switch Lite**: This product has a rating of 4.6/5 and is priced at $12.5. It has received great reviews for its ease of installation, durability, and high accuracy response. Many reviewers have mentioned that it fits perfectly on the Switch Lite and provides great protection against damage.
>
>       Review Excerpts:
>       - "Easy application and it fits perfectly."
>       - "It looks great on the switch, you cant even tell theres a screen protector on it."
>       - "Works great, easy to apply and lasts forever."
>
>2. **Yonntech 3 Pack Screen Protector for Nintendo Switch Lite**: This product has a rating of 4.6/5 but the price is not mentioned. It has received great reviews for its ease of application and ability to protect the screen. Some reviewers have mentioned that it doesn't completely cover the screen, but it still does its job well.
>
>       Review Excerpts:
>       - "Easy to apply, it doesnt completely cover the screen for the switch lite."
>       - "They do their job, easy to apply."
>
>3. **2 PCS Screen Protectors Anti Blue Light for Nintendo Switch OLED**: This product has a rating of 4.6/5 and the price is not mentioned. It has received great reviews for its fit and functionality. One reviewer mentioned that it fits perfectly on their Switch OLED.
>
>       Review Excerpts:
>       - "Fits perfect."
>
>Please note that the prices of some products are not mentioned, so you may need to check the current prices on Amazon to make a final decision.

**Evaluation** : 
- Overall, the recommendations fit all the query aspects and the reviews of the product suggest that they are relevant.
- The answer is very clear and detailed, listing the rating, price and excerpts of reviews.

### 2. **Query** : gaming headset with microphone
**RAG response:**
>Based on your query, I have found a few products that match your requirements. Since the prices are not specified, I will focus on the ratings and reviews.
>
> 1. **Ideazon GH100 Gaming Headset**: This product has a rating of 4.4/5 and has received positive reviews for its sound quality. Although the mic is uncomfortable and the cord broke easily, it's still a good option to consider.
>
> 2. **Lesozoh A10 Gaming Headset**: This product has a rating of 3.8/5 and is priced at $27.97. Reviews praise its excellent performance, high-definition speaker, and vibration unit. However, the mic is not working for some users.
>
> 3. **Gaming Headset Headphones with Microphone**: This product has a rating of 3.9/5 but the reviews are mixed. Some users praise its comfort, good mic, and RGB light, while others mention that the wires break easily and the product came broken.
>
> Considering the ratings and reviews, I would recommend the **Ideazon GH100 Gaming Headset** as the top choice. Although it has some drawbacks, it seems to be a good option for sound quality. However, if you're looking for a more affordable option, the **Lesozoh A10 Gaming Headset** is worth considering, despite the mic issues.



**Evaluation** : 
- The query specifically asks for headsets with microphone but the products listed have revies that specifically point out microphone issues.
- Overall, the response is clear and explains each choice clearly, even giving multiple choices based on what a user might be looking for (price range...).

### 3. **Query** : competitive multiplayer game for large groups

**RAG response:**
>Based on the context provided, I would recommend the "Ace of Spades Battle Builder" as a competitive multiplayer game for large groups.
>
>Here's why:
>
>- The game allows up to 32 players in a single match, which is a large group.
>- The game description mentions that it's a "first-person shooter that lets you create your battleground, destroy it, then create it again" which implies competitive gameplay.
>- Although one of the reviews mentions that the game crashes, another review states that it's an "awesome game" that's like "Minecraft meets Counter-Strike", which suggests that it's a game worth considering.
>
>While there are some concerns about the game's stability, it seems to offer the competitive multiplayer experience that you're looking for.

**Evaluation** : 
- Only a single product is recommended here but it seems to be a really good fit for the query.
- The response also contains a many details as to how the products corresponds to the different aspects of the query.

### 4. **Query:** ps4 controller with good battery life
**RAG response:**
>Based on the reviews and ratings provided, I highly recommend the **"Pickle Power 2 Pack 2000mah PS4 PS4 Pro Battery Replacement"** product (Rating: 4.4/5, Price: $17.89). This product is specifically designed to replace the batteries in your PS4 controller, and the reviews suggest that it greatly improves the battery life of the controller.
>
>Multiple reviewers have stated that the batteries work perfectly, last most of the day, and are a great upgrade to extend the controller's life. Some reviewers have even mentioned that the batteries work as well as the original ones and have increased their playtime significantly.
>
>While the other products reviewed do have good battery life, they are not specifically designed as battery replacements, and the reviews do not provide the same level of detail and satisfaction as the Pickle Power product.
>
>The other products that may be worth considering are:
>
>* **Vidppluing Wireless Controller for PS4** (Rating: 4.2/5) - This product has a good rating, but the price is not specified, and there is limited information available.
>* **Usergaing Replacement for PS4 Controller** (Rating: 5.0/5) - This product has a great rating, but the price is not specified, and there is limited information available.
>* **Gamepad Controlador** (Rating: 3.0/5) - This product has a poor battery life, and I would not recommend it.
>
>Overall, based on the reviews and ratings provided, I believe that the Pickle Power 2 Pack 2000mah PS4 PS4 Pro Battery Replacement is the best option for a PS4 controller with good battery life.
*Evaluation** : 
- The products listed don't really match what the query is asking for. Instead of controller options, the products listed are replacement batteries for a controller.
- One of the products is also the opposite of what the query requires (poor battery life).

### 5. **Query**: good single player story game for a beginner who just got their first playstation under $50
|Dimension | What to assess | yes/no |
|----------|----------------|--------|
|Accuracy|Is the answer factually correct based on the reviews?||
|Completeness|Does the answer address all aspects of the question?||
|Fluency|Is the answer natural, clear, and easy to read?||

### Summary of Results

#### Key Observations and Overall Performance
The RAG pipeline performs well on keyword based queries (like query 1), where it returned relevant products in a clear and detailed manner. However, on semantic based queries which are broader or more nuanced, it struggles to find truly relevant products (like query 4) that respond to every aspect of the query. Overall, the pipeline does return good recommendations but the quality of the products depends on how the query is defined.

#### Limitations of Hybrid RAG Workflow
The hybrid retriever struggles to distinguish between products that are related to the query and those that satisfy all its aspects (like in query 4).

The pipeline also sometimes returns products that directly contradict the query (like in query 4), which might be caused by the hybrid retriever not being able to fully grasp the meaning of the documents it passes to the context for the LLM.

#### Suggestions
Refining the LLM prompt to specifically skip products that directly contradict the query, whether through the product itself (query 4) or the reviews (query 1).
Adding a ranking step after running the hybrid retriever to reorder the products before adding them as context for the LLM might help make the recommendations more relevant to the query.