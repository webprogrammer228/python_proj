from pymongo import MongoClient
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

#подключение к бд

load_dotenv()
mongo_user = os.environ.get('MONGODB_USERNAME')
mongo_password = os.environ.get('MONGODB_PASSWORD')
mongo_host = os.environ.get('MONGODB_HOSTNAME')
mongo_db = os.environ.get('MONGODB_DATABASE')

print(mongo_user, mongo_password, mongo_host, mongo_db)

client = MongoClient('mongodb://' + quote_plus(mongo_user) + ':' + quote_plus(os.environ.get('MONGODB_PASSWORD')) + '@' + mongo_host + ':27017/' + mongo_db)
db = client[mongo_db]