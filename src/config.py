from pathlib import Path

# Project root path
ROOT_DIR = Path(__file__).resolve().parent.parent 

# Data folder path
DATA_DIR = ROOT_DIR / "data"

# Raw data folder path
RAW_DATA_DIR = DATA_DIR / "raw"
USER_DATA = RAW_DATA_DIR / "Video_Games.jsonl"
META_DATA = RAW_DATA_DIR / "meta_Video_Games.jsonl"

# Processed data folder path
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PARQUET_DATA = PROCESSED_DATA_DIR / "processed_data.parquet"

# Index folder path
BM25_INDEX = PROCESSED_DATA_DIR / "bm25_index"
FAISS_INDEX = PROCESSED_DATA_DIR / "faiss_index"

# Results folder path
RESULTS_DIR = ROOT_DIR / "results"
BM25_RESULTS = RESULTS_DIR / "bm25_results.csv"
SEMANTIC_RESULTS = RESULTS_DIR / "semantic_results.csv"
