# Qualitative Evaluation

## Query Set

| Easy (Keyword-based) |	Medium (Semantic-based)	| Complex|
|----|----|---|
|nintendo switch screen protector| playstation games for sports lovers |best wireless gaming headset for ps5 with good microphone under $100|
| gaming headset with microphone|competitive multiplayer game for large groups |good single player story game for a beginner who just got their first playstation under $50|
|xbox 360 wireless controller|comfortable headset for long gaming sessions|
|fifa 16 game for playstation|ps4 controller with good battery life|

## Results 

- Results for the BM25 search on the query set can be found in [bm25_results.csv](bm25_results.csv).

>For example, the results for the first query are as follows:
![bm25_results.png](img/bm25_results.png)

- Results for the semantic search on the query set can be found in [semantic_results.csv](semantic_results.csv).

>For example, the results for the first query are as follows:
![semantic_results.png](img/semantic_results.png)

For both search implementations, the results are sorted in order of relevance, i.e the first product is the one that is the most recommended (highest score for BM25 and lowest score for semantic search).