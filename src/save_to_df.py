import pandas as pd


def results_to_df(query, results, top_n=5):
    """Convert search results to deduplicated dataframe"""
    rows = []
    seen_asins = set()
    for doc, score in results:
        asin = doc.metadata['parent_asin']
        if asin not in seen_asins:
            seen_asins.add(asin)
            rows.append({
                "query": query,
                "item_title": doc.metadata['item_title'],
                "review": doc.page_content[:200],
                "rating": doc.metadata['average_rating'],
                "score": round(score, 4)
            })
        if len(rows) == top_n:
            break
    return pd.DataFrame(rows)