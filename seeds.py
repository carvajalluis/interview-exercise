from deps.config import EnvConfig
from deps.db_client import MongoDBClient
from seeds.generator import Generator


def main():
    conf = EnvConfig()
    db = MongoDBClient(conf)
    seeder = Generator(db)
    seeder.seed_transactions()
    seeder.seed_keys()
    
if __name__ == '__main__':
    main()