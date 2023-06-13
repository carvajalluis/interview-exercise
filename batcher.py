import json

from deps.config import EnvConfig
from deps.db_client import MongoDBClient


def handler(event, _):
    conf = EnvConfig()
    db = MongoDBClient(conf)

    batch_size = event['batch_size']
    pages_count = db.get_unsigned_transactions_pages(batch_size=batch_size)
    pages = [{'page': x, 'page_size': batch_size} for x in range(1, pages_count)]
    return {'body':pages}

if __name__ == '__main__':
    handler({'batch_size': 1000}, None)
