# Qualitative Evaluation

## Query Set

| Easy (Keyword-based) |	Medium (Semantic-based)	| Complex|
|----|----|---|
|nintendo switch screen protector| playstation games for sports lovers |best wireless gaming headset for ps5 with good microphone under $100|
| gaming headset with microphone|competitive multiplayer game for large groups |good single player story game for a beginner who just got their first playstation under $50|
|xbox 360 wireless controller|comfortable headset for long gaming sessions|
|fifa 16 game for playstation|ps4 controller with good battery life|

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

#### Easy (Keyword-based) Queries
- **Query** : nintendo switch screen protector

|Rank|BM25 Results|Semantic Results|Rating|
|---|---|---|---|
|1|syncwire screen protector for nintendo switch 2 pack premium tempered glass screen protector film for nintendo switch|evoretro screen protector compatible for nintendo switch lite  ultra clear heavy duty tempered glass protection kit with high accuracy response and premium protection 2pack|BM25 : 4.7 Semantic : 4.6|
|2|heystop case compatible with nintendo switch dockable soft tpu protective case cover for nintendo switch with switch tempered glass screen protector and 6 thumb grip caps|nintendo switch screen protector taken ultral slim hd clear antibubble screen protector film for nintendo switch 2 pack|BM25 : 4.4 Semantic : 4.0|
|3|evoretro screen protector compatible for nintendo switch lite  ultra clear heavy duty tempered glass protection kit with high accuracy response and premium protection 2pack|rinogear 2pack screen protector for nintendo switch screen protector case friendly accessories flexible full coverage clear tpu film| BM25 : 4.6 Semantic : 4.0|
|4|xinruisen 3pack screen protector for nintendo switch oled 2021 tempered glass screen protector for nintendo switch oled new model 7inch screen protective glass cover protection for switch oled| smartdevil screen protector for nintendo switch lite 2019antiblue light tempered glass protect eyesight 9h hardness compatible nintendo switch lite 2 pack|BM25 : 4.6 Semantic : 4.6|
|5|nintendo switch screen protector taken ultral slim hd clear antibubble screen protector film for nintendo switch 2 pack| screen protector tempered glass for nintendo switch lite 2020 antifall and scratch|BM25 : 4.0 Semantic : 4.4|

- **Query** : gaming headset with microphone

|Rank|BM25 Results|Semantic Results|Rating|
|---|---|---|---|
|1|ienza pc headset  pc gaming headset compatible for xbox one xb1 or playstation 4 ps4 converter talkback  chat cable|sades arcmage 35mm stereo gaming headset with mic gold|BM25 : 4.0 Semantic : 2.1|
|2|gtheos 24ghz wireless gaming headphones for pc ps4 ps5 mac nintendo switch bluetooth 52 gaming headset with detachable noise canceling microphone stereo sound 35mm wired mode for xbox series|wired gaming headset with micsades 709 35mm stero over ear headphone for pc laptop notebook tablet smartphone by afuntablue|BM25 : 4.3 Semantic : 3.3|
|3|gaming headset for ps4 ps5 pc gaming headphones stereo 71 surround sound 35mm audio jack over ear headset with microphone wired gaming headset with 50mm drivers for xbox laptop|ps4 gaming headset  xbox one headset xbox one s headset with microphone votron over ear stereo gaming headphones with led light noise reduction for xbox one ps4 pc mac ipad psp headphones| BM25 : 4.2 Semantic : 3.9|
|4|hyperx cloud alpha gaming headset  dual chamber drivers  durable aluminum frame  detachable microphone  works with pc ps4 ps4 pro xbox one xbox one s hxhscardam renewed|dland gaming headset with mic led light for laptop computer cellphone ps4 so on35mm wired noise isolation  volume control|BM25 : 4.4 Semantic : 3.5|
|5|ps4 gaming headset for pc xbox one ps5 phoinikas g2000 wired over ear headphones with detachable noise cancelling mic bluetooth wireless earphones for phone tablet oneclick 71 sound up to 12h|gaming headset for ps4|BM25 : 3.6 Semantic : 3.5|


#### Medium (Semantic-based) Queries

- **Query** : competitive multiplayer game for large groups

|Rank|BM25 Results|Semantic Results|Rating|
|---|---|---|---|
|1|mario and sonic at the olympic winter games  nintendo wii|tom clancys rainbow six siege  playstation 4|BM25 : 4.5 Semantic : 4.4|
|2|12 switch  nintendo switch|12 switch  nintendo switch|BM25 : 4.6 Semantic : 4.6|
|3|hasbro family fun pack  playstation 4 download code|splatoon 2 starter pack  nintendo switch| BM25 : 4.0 Semantic : 4.5|
|4|powera wired controller for nintendo switch  zelda breath of the wild|rise of nations  pc|BM25 : 4.4 Semantic : 3.5|
|5|ps4 accel world vs sword art online english subs for playstation 4|dead space 3  pc origin online game code|BM25 : 4.6 Semantic : 4.3|

#### Complex Queries