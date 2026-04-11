import pandas as pd


def results_to_df(query, results, top_n=5):
    """Convert search results to dataframe, while removing duplicate product results to single query"""
    rows = []
    seen_asins = set()
    for doc, score in results:
        asin = doc.metadata['parent_asin']
        if asin not in seen_asins:
            seen_asins.add(asin)
            rows.append({
                "query": query,
                "Product title": doc.metadata['item_title'],
                "Review": doc.metadata['text'][:200],
                "Rating": doc.metadata['average_rating'],
                "Score": round(score, 4)
            })
        if len(rows) == top_n:
            break
    return pd.DataFrame(rows)