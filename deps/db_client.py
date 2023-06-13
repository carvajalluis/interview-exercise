from math import ceil

from pymongo import ReturnDocument, UpdateOne
from pymongo.mongo_client import MongoClient


class MongoDBClient:
    def __init__(self, config):
        # Load MongoDB connection variables from environment variables
        self.config = config
        self.database = self.config.db
        self.client = MongoClient(self.config.db_uri)
        self.db = self.client[self.database]
        self.coll_keys = self.db.get_collection(self.config.db_coll_keys)
        self.coll_trans = self.db.get_collection(
            self.config.db_coll_transactions)

    def insert_keys(self, docs):
        # stores a list of keys
        # TODO: replace with KMS and usage collection
        self.coll_keys.insert_many(documents=docs)

    def insert_transactions(self, docs):
        # stores a list of transactions
        self.coll_trans.insert_many(documents=docs)

    def get_least_used_key(self):
        # retrives the key that has not been used yet
        doc = self.coll_keys.find_one_and_update(
            # TODO: filter locked  records. 
            filter=dict(),
            update={'$inc': {'last_used': 1}},
            sort=[('last_used', 1), ('_id', -1)],
            return_document=ReturnDocument.AFTER)

        return doc

    def get_unsigned_transactions_pages(self, batch_size):
        # Gets the count of unsifned transactions
        result = self.coll_trans.count_documents(
            filter={'signature': None},
        )
        return ceil(result / batch_size)

    def get_unsigned_transactions_page(self, page_number, page_size):
        # get a batch of unsigned transactions
        skip_count = (page_number - 1) * page_size
        cursor = self.coll_trans.aggregate(
            pipeline=[{'$match': {'signature': None}},
                      {'$skip': skip_count},
                      {'$limit': page_size},
                      {'$sort': {'_id': 1}}])

        transactions = list(cursor)
        return transactions

    def update_transactions(self, docs):
        # update all transactions in a list
        # to store the corresponding signature
        bulk_operations = []
        for transaction in docs:
            filter_query = {'_id': transaction['_id']}
            update_query = {'$set': {'signature': transaction['signature']}}
            bulk_operations.append(UpdateOne(filter_query, update_query))

        result = self.coll_trans.bulk_write(bulk_operations)

        return {'Matched': result.matched_count,
                'Modified': result.modified_count}
