import os

from dotenv import load_dotenv


class EnvConfig:
    def __init__(self):
        load_dotenv()
        self.db_uri = os.getenv("MONGODB_URI")
        self.db = os.getenv("MONGODB_DATABASE")
        self.db_coll_keys = os.getenv("MONGODB_COLLECTION_KEYS")
        self.db_coll_transactions = os.getenv("MONGODB_COLLECTION_TRANSACTIONS")