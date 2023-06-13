import base64
import secrets

from ecdsa import NIST256p, SigningKey
from faker import Faker
from faker.providers import date_time


class Generator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()
        self.fake.add_provider(date_time)


    def seed_transactions(self):
        # seed the transactions collection
        docs = [{
            'amount': self.fake.random_number(digits=5),
            'sender_address': secrets.token_hex(10),
            'recipient_address': secrets.token_hex(10),
            'timestamp': self.fake.date_time_this_decade()
        }
            for _ in range(100000)
        ]
        self.db.insert_transactions(docs)

    def seed_keys(self):
        docs = [{'bin': SigningKey.generate(curve=NIST256p).to_string()} for _ in range(100)]
        self.db.insert_keys(docs)
