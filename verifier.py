import json

from bson import ObjectId
from ecdsa import NIST256p, SigningKey

from deps.config import EnvConfig
from deps.db_client import MongoDBClient
from deps.mongolock import MongoLock


def handler(event, context):
    conf = EnvConfig()
    mongo = MongoDBClient(conf)
    lock_key = MongoLock(client=mongo.client,
                         db=mongo.database, collection='key_locks')

    page = event['page']
    page_size = event['page_size']
    worker = context.aws_request_id
    lock_timeout = (context.get_remaining_time_in_millis()/1000) % 60

    key_doc = mongo.get_least_used_key()
    private_key = SigningKey.from_string(key_doc['bin'], curve=NIST256p)
    key_id: ObjectId = key_doc['_id']

    transactions = mongo.get_unsigned_transactions_page(
        page_number=page,
        page_size=page_size)

    with lock_key(str(key_id), worker, timeout=lock_timeout):
        for tr in transactions:
            signature = private_key.sign(str(tr).encode())
            tr['signature'] = {'value': signature,
                               'verifying_key': private_key.verifying_key.to_string(),
                               'key_id': key_id}
        result = mongo.update_transactions(docs=transactions)

    return {'statusCode': 200, 'body': result}


if __name__ == '__main__':
    handler({'page': 2, 'page_size': 100}, None)
