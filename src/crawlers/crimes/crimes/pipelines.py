"""
Import scrapy, pymongo and utils functions to treat data.
"""
import datetime
import pymongo

from utils.dates import get_capture_data

class CrimesPipeline:
    """
    Crime spiders pipeline.
    """
    def __init__(self, mongo_uri, mongo_db):
        """
        Init the spider with .
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = ''
        self.client = None
        self.database = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        Get the settings MONGO_URI and MONGO_DATABASE.
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        """
        Create the client and get the database at MongoDB.
        """
        self.collection_name = spider.name
        self.client = pymongo.MongoClient(self.mongo_uri, 27017)
        self.database = self.client[self.mongo_db]
        self.database[self.collection_name].drop()

    def process_item(self, item, spider):
        """
        Save the monthly city data on database.
        """
        # Check if the document already exists on database and get the reference
        db = self.database[self.collection_name].find_one({ 
            'period': item['period']
        })

        # If the document doesn't exist yet, create it
        if db == None:
            db = self.database[self.collection_name].insert_one({
                'capture_data': get_capture_data(datetime.datetime.now()),
                'period': item['period'],
                'cities': []
            })

            # Get the reference of the created document
            db = self.database[self.collection_name].find_one({
                '_id': db.inserted_id
            })

        # Add the monthly city data to the array of cities on database
        new_city_data = {
            "$push": { 
                "cities": { 'name': item['city'], 'crimes': item['monthly_data'] }
            }
        }
        self.database[self.collection_name].update_one(db, new_city_data)

        return item

    def close_spider(self, spider):
        """
        Close database.
        """
        self.client.close()