# Qualitative Evaluation

## Query Set

| Easy (Keyword-based) |	Medium (Semantic-based)	| Complex|
|----|----|---|
|nintendo switch screen protector| playstation games for sports lovers |best wireless gaming headset for ps5 with good microphone under $100|
| gaming headset with microphone|competitive multiplayer game for large groups |good single player story game for a beginner who just got their first playstation under $50|
|xbox 360 wireless controller|comfortable headset for long gaming sessions|
|fifa 16 game for playstation|ps4 controller with good battery life|

**Note**: The semantic search was not able to produce 5 unique items for some queries (see semantic_results.csv). This is likely due to two reasons: (1) our dataset is a 400k sample of the full 3.9M Amazon video game product dataset, which may underrepresent certain product queries, and (2) many records in the dataset correspond to different user reviews of the same product. We deduplicated results by product ID (`parent_asin`) to ensure unique products are returned, which reduces the number of available results for some queries. BM25 does not have this issue as keyword matching naturally surfaces a wider variety of products.

## Results 

### Result retrieval
- Results for the BM25 search on the query set can be found in [bm25_results.csv](bm25_results.csv).

>For example, the results for the first query are as follows:
![bm25_results.png](img/bm25_results.png)

- Results for the semantic search on the query set can be found in [semantic_results.csv](semantic_results.csv).

>For example, the results for the first query are as follows:
![semantic_results.png](img/semantic_results.png)

For both search implementations, the results are sorted in order of relevance, i.e the first product is the one that is the most recommended (highest score for BM25 and lowest score for semantic search).

### Result comparison

#### Easy (Keyword-based) Queries :

1. **Query** : nintendo switch screen protector

|Rank|BM25 Results|Semantic Results|Match quality|
|---|---|---|---|
|1|syncwire screen protector for nintendo switch 2 pack premium tempered glass screen protector film for nintendo switch|evoretro screen protector compatible for nintendo switch lite  ultra clear heavy duty tempered glass protection kit with high accuracy response and premium protection 2pack|**BM25** : Excellent match <br> **Semantic**  : Good match (Lite specific)|
|2|heystop case compatible with nintendo switch dockable soft tpu protective case cover for nintendo switch with switch tempered glass screen protector and 6 thumb grip caps|nintendo switch screen protector taken ultral slim hd clear antibubble screen protector film for nintendo switch 2 pack|**BM25** : Partial match (bundle that includes product) <br> **Semantic**  : Excellent match|
|3|evoretro screen protector compatible for nintendo switch lite  ultra clear heavy duty tempered glass protection kit with high accuracy response and premium protection 2pack|rinogear 2pack screen protector for nintendo switch screen protector case friendly accessories flexible full coverage clear tpu film| **BM25** : Good match (Lite specific) <br> **Semantic**  : Partial match (bundle that includes product)|
|4|xinruisen 3pack screen protector for nintendo switch oled 2021 tempered glass screen protector for nintendo switch oled new model 7inch screen protective glass cover protection for switch oled| smartdevil screen protector for nintendo switch lite 2019antiblue light tempered glass protect eyesight 9h hardness compatible nintendo switch lite 2 pack|**BM25** : Good match (OLED specific)  <br> **Semantic** : Good match (Lite specific)|
|5|nintendo switch screen protector taken ultral slim hd clear antibubble screen protector film for nintendo switch 2 pack| screen protector tempered glass for nintendo switch lite 2020 antifall and scratch|**BM25** : Excellent match  <br> **Semantic**  : Good match (Lite specific)|

**Comments** :
- Both search methods perform quite well, with all the results corresponding to the intended product. 
- However, both methods highly recommend bundles (BM25 : 2 , Semantic : 3) which contain more than just the screen protector.
- Semantic search tends to recommend Switch Lite products which is not specified in the query.
- **Best method** : BM25 since most of the products it recommends are directly relevant to the query
    
---
2. **Query** : gaming headset with microphone

|Rank|BM25 Results|Semantic Results|Match quality|
|---|---|---|---|
|1|ienza pc headset  pc gaming headset compatible for xbox one xb1 or playstation 4 ps4 converter talkback  chat cable|sades arcmage 35mm stereo gaming headset with mic gold|**BM25** : Partial match (no mention of microphone) <br> **Semantic**  : Excellent match |
|2|gtheos 24ghz wireless gaming headphones for pc ps4 ps5 mac nintendo switch bluetooth 52 gaming headset with detachable noise canceling microphone stereo sound 35mm wired mode for xbox series|wired gaming headset with micsades 709 35mm stero over ear headphone for pc laptop notebook tablet smartphone by afuntablue|**BM25** : Excellent match <br> **Semantic**  : Excellent match |
|3|gaming headset for ps4 ps5 pc gaming headphones stereo 71 surround sound 35mm audio jack over ear headset with microphone wired gaming headset with 50mm drivers for xbox laptop|ps4 gaming headset  xbox one headset xbox one s headset with microphone votron over ear stereo gaming headphones with led light noise reduction for xbox one ps4 pc mac ipad psp headphones| **BM25** : Excellent match <br> **Semantic**  : Excellent match|
|4|hyperx cloud alpha gaming headset  dual chamber drivers  durable aluminum frame  detachable microphone  works with pc ps4 ps4 pro xbox one xbox one s hxhscardam renewed|dland gaming headset with mic led light for laptop computer cellphone ps4 so on35mm wired noise isolation  volume control|**BM25** : Excellent match <br> **Semantic**  : Excellent match|
|5|ps4 gaming headset for pc xbox one ps5 phoinikas g2000 wired over ear headphones with detachable noise cancelling mic bluetooth wireless earphones for phone tablet oneclick 71 sound up to 12h|gaming headset for ps4|**BM25** : Excellent match <br> **Semantic**  : Partial match (no mention of microphone)|

**Comments** :

- Both search methods perform quite well, with all the results corresponding to the requirements of the query for the product. 
- BM25's best result is not a great match for the intended product.
- **Best method** : Semantic search since the order in which the products are recommended make sense (the last recommendation is the worst match, while BM25 first recommendation is the worst match).


**Conclusion** :
Overall, the results are consistent with keyword-based search (BM25) performing better on keyword based queries.

---
#### Medium (Semantic-based) Queries

1. **Query** : competitive multiplayer game for large groups

|Rank|BM25 Results|Semantic Results|Match quality|
|---|---|---|---|
|1|mario and sonic at the olympic winter games  nintendo wii|tom clancys rainbow six siege  playstation 4|**BM25** : Partial match (not designed for large groups) <br> **Semantic**  : Excellent match |
|2|12 switch  nintendo switch|12 switch  nintendo switch|**BM25** : Good match (not ideal for large groups) <br> **Semantic**  : Good match (not ideal for large groups) |
|3|hasbro family fun pack  playstation 4 download code|splatoon 2 starter pack  nintendo switch|**BM25** : Excellent match  <br> **Semantic**  : Excellent match |
|4|powera wired controller for nintendo switch  zelda breath of the wild|rise of nations  pc|**BM25** : Bad match (not a game) <br> **Semantic**  :  Partial match (note designed for large groups) |
|5|ps4 accel world vs sword art online english subs for playstation 4|dead space 3  pc origin online game code|**BM25** : Partial match (not designed for large groups) <br> **Semantic**  : Partial match (note designed for large groups) |

**Comments** :

- BM25 struggles to recommend products that match the products requirement 
- Semantic search performs better but struggles to fulfill all the product equirements (focuses more on the competitive than the large group aspect)
- **Best method** : Semantic search since it matches the query requirements better.

2. **Query:** ps4 controller with good battery life

|Rank|BM25 Results|Semantic Results|Match quality|
|---|---|---|---|
|1|lip1922s 2200mah 37v lithium battery replacement for sony ps4 pro dual shock 4 cuhzct2e cuhzct2u wireless controller 2pack|wireless gaming controller for ps4 geeklin wireless gamepad remote joystick for ps4ps3androidiospc with upgraded joystick headset jack and dual vibration| **BM25:** Not a good match (batteries not controller returned) <br> **Semantic:** Good match|
|2|extremerate multicolors luminated dpad thumbstick trigger home face buttons for ps4 controller dtfs dtf 20 led kit for ps4 slim pro cuhzct2 controller  controller not included|kujian wireless controller for ps4 high performance double shock game controller compatible with playstation 4slimpropc gaming controller with sensitive touch pad motion sensornebula series| **BM25:** Bad match <br> **Semantic:** Good match|
|3|rechargeable batteries for ps4 controller farsail 1pack 2000mah lip1522 ps4 battery replacement with big and small plug for playstation 4 ps4 dualshock 4 wireless controller|playstation 3 doubleshock iii wireless controller black| **BM25:** Bad match (battery replacement) <br> **Semantic:** Partial match (PS3 instead of PS4)|
|4|seivi 2 pack 2000mah lip1522 replacement battery compatible with playstation 4 ps4 dualshock 4 cuhzct1e cuhzct1h cuhzct1u wireless controller big and small plug|sades ps4 controller| **BM25:** Bad match <br> **Semantic:** Good match|
|5|kujian wireless controller for ps4 high performance double shock game controller compatible with playstation 4slimpropc gaming controller with sensitive touch pad motion sensornebula series|replacement for ps4 controller wireless controller for ps4props3slimpc dedicated game joystick controller dual vibration audio function| **BM25**: Good match (controller) <br> **Good Match:** Good match|

**Comments:**

- BM25 seems to misinterpret "battery life" as a keyword/phrase and instead returns repalcement battery parts and accessories instead of recommending actual controllers. Only 1 out of 5 BM25 results is a controller. User's intent/product feature: 'good battery life', is clearly not captured by BM25.
- Semantic search does much better with this query. It returns controllers in 4 out of 5 results however, none of the results explicitly mention battery life as a feature. After looking at the reviews, the second and third best controllers recommended by semantic search have a bad reviews, where battery life is mentioned to last for 5 minutes.
- **Best method:** Overall, semantic search does better compared to BM25, since it returns the product being asked for, but the quality of the product recommendation is questionable and definitely requires improvement.

---
#### Complex Queries

- **Query**: good single player story game for a beginner who just got their first playstation under $50

|Rank|BM25 Results|Semantic Results|Match quality|
|---|---|---|---|
|1| battlefield 3  playstation 3| saiyuki journey west| **BM25:** Partial match (playstation game but not story/beginner friendly) <br> **Semantic:** Partial Match (story game, but expensive) |
|2|dead space 3  pc origin online game code | beyond the beyond	 | **BM25:** Bad match (PC game not playstation) <br> **Semantic:** Partial Match (story game, above $50)|
|3| call of duty ghosts  ps3 digital code | tom clancys ghost recon breakpoint standard edition  xbox one digital code| **BM25**: Partial match (moderate level game, cheap) <br> **Semantic:** Bad match (wrong platform) |
|4| cold fear  playstation 2 | shin megami tensei v steelbook launch edition  nintendo switch | **BM25:** Bad match (horror, expensive) <br> **Semantic:** Bad match (nintendo not playstation) |
|5| grim adventures of billy  mandy | call of duty black ops iii  standard edition  playstation 4 | **BM25:** Partial Match (not story game) <br> **Semantic:** Partial match (story, beginner, expensive) |

**Comments:**

- This query is a lot more difficult to handle for both models. It has multiple constraints: single player, story-driven, beginner friendly, playstation platform, under $50.
- BM25 sometimes matches on "playstation" keyword but returns shooter games (Battlefield, Call of Duty) which tend to not be story-driven or beginner friendly. Overall, BM25 produces only partially relevant results.
- Semantic search understands "story game" better, returning RPGs(Role Playing Game), but fails on the price criteria (beinf under $50). It tends to return more expensive games and even games that are not for the intended playstation platform (returns nintendo, xbox.)
- Both methods don't do well with the price and platform requirement. Semantic search does better at recommended story-driven video games.
- **Best method:** None. This query likely requires more complex methods like hybrid search, RAG or post-retrieval filtering to handle price constraints, platform type, difficulty level and type of game (story vs combat etc.).

## Summary of Insights

### Strengths and Weaknesses

**BM25:**

- Strengths:
  - Performs well on exact keyword queries (e.g. "nintendo switch screen protector", "gaming headset with microphone") where the product name or type appears directly in the query
  - Fast + reliable for specific product searches
  - Returns diverse results for product queries (i.e. nintendo switch screen protector, BM25 returned different brands)
- Weaknesses:
  - Interprets queries very literally, failing to understand when keyword is related to criteria within product and not name of product itself. E.g "battery life" returns battery parts instead of controllers with good battery life. That means that this method fails to understand user intent or product attributes beyond keyword matching.
  - Because it is key-word focused, it doesn't do well on semantic or conceptual queries (e.g. "competitive multiplayer game for large groups")
  - Cannot handle specific criteria requirements like price or platform

**Semantic Search:**

- Strengths:
  - Compared to BM25, it has a better understanding of user intent and conceptual queries. For example, it returns competitive multiplayer games for "competitive multiplayer game for large groups" even when exact game titles are not mentioned in the query.
  - Does better on attribute-based queries that describe a product (e.g. "comfortable headset for long gaming sessions", 
  "ps4 controller with good battery life").
- Weaknesses:
  - Like BM25, cannot filter by price or platform metadata
  - Does not return many unique results. Many queries only had 1 result returned for semantic search, whereas BM25 always returned top 5 when specified.
  - It's much slower than BM25 at scale
  - Product quality is not guaranteed. Some of the reviews (e.g. controller battery life), were not great, so the model is better at capturing similarity between product and query but cannot always distinguish between good vs bad reviewed products.

### Challenging Query Types for Both Methods

- Complex query types showed the worst performance with both models.
- Queries with a price restriction (e.g. under $50) were very difficult for both methods. Neither method could filter by price meta-data. Post-retrieval filtering may be required.
- Same difficulties also seen for platform type (e.g. specifying ps4 but getting results specific to xbox or nintendo)
- Multi-constraint queries combining product type, price, platform and experience level simultaneously (as seen above).
- For BM25, semantic/conceptual queries were also challenging, when the user describes a product attribute or intent rather than a product name, BM25 falls back to literal keyword matching which returned irrelevant results.

### Where Advanced Methods Would Help

- **Hybrid Search**: Combining BM25 and semantic search would leverage strengths of both. Exact keyword matching for product names and semantic understanding for attributes and user intent/requirements. It would be more accurate but also better at capturing what user is looking for exactly.
- **Post-retrieval Metadata Filtering**: Filtering results by price, platform and rating after retrieval would improve complex query results with many specific criteria specified by the user.
- **RAG**: With RAG, the LLM agent could synthesize information from multiple retrieved reviews, which would be better for recommedning good qualtiy, well-reviewed products. With this model, the products being recommended are more trustworthy in terms of their function/performance.
- **Reranking**: Uses a true relevance score after the documents/products have been retrieved and reorders them so that the items being recommended to the user are actually more relevant to the query, not just more similar. This way the products that best satisfy all query requirements are being recommended in a more meaningful order.