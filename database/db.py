import os
from pymongo import MongoClient


client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client['stay-safe']
