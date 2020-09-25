import os
from pymongo import MongoClient
from settings import logger


client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client['stay-safe']

def get_all():
    try:
        data = db.crimes_df.find({})
        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()
        return str(error), 400
