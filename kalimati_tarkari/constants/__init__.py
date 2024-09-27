import os
from datetime import date
from dotenv import load_dotenv

from pathlib import Path
from urllib.parse import quote_plus


load_dotenv()
username = os.getenv('username')
password = os.getenv('password')

# Escape the username and password according to RFC 3986
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

DATABASE_NAME = os.getenv('DB_NAME')

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

MONGODB_URL_KEY =  f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.tofa7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


PIPELINE_NAME: str = "kalimati"
ARTIFACT_DIR: str = "artifact"


TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

FILE_NAME: str = "final_data.csv"
MODEL_FILE_NAME = "model.pkl"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = os.getenv('COLLECTION_NAME')
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.10

