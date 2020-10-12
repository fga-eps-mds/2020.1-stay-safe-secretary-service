"""
Import scrapy, pymongo and utils functions to treat data.
"""
import datetime
import pymongo

from utils.treat_data_df import get_data_from_excel
from utils.treat_data_sp import get_cities_data_by_year
from utils.handle_folders import delete_folder
from utils.dates import get_capture_data

class DfPipeline:
    """
    Pipeline of spider crimes_df.
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
        Get the annual city data, treat the data per month and save on database.
        """
        annual_city_data = get_data_from_excel(item['city'])

        for month, monthly_data in enumerate(annual_city_data):
            # Check if the document already exists on database and get the reference
            db = self.database[self.collection_name].find_one({ 
                'period': f'{month+1}/{item["year"]}'
            })

            if db == None:
                # If the document doesn't exist, create the document
                db = self.database[self.collection_name].insert_one({
                    'capture_data': get_capture_data(datetime.datetime.now()),
                    'period': f'{month+1}/{item["year"]}',
                    'cities': []
                })

                # Get the reference to the new document
                db = self.database[self.collection_name].find_one({
                    '_id': db.inserted_id
                })

            # Add the monthly city data to the array of cities on database
            new_city_data = {
                "$push": { 
                    "cities": { 'name': item['city'], 'crimes': monthly_data }
                }
            }
            self.database[self.collection_name].update_one(db, new_city_data)

        return item

    def close_spider(self, spider):
        """
        Close database and delete data folder.
        """
        delete_folder('data')
        self.client.close()


class SpPipeline:
    """
    Pipeline of spider crimes_sp.
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

    def process_item(self, item, spider):
        """
        Treating the data per year and save on database.
        """
        for year, month in item['years'].items():
            db_data = {}

            date = datetime.datetime.now()
            db_data['capture_data'] = f'{date.strftime("%d")}/{date.strftime("%m")}/{date.strftime("%Y")}'
            
            db_data['period'] = {
                'start': f'01/{year}',
                'end': '{0:0=2d}'.format(month) + f'/{year}'
            }

            db_data['cities'] = get_cities_data_by_year(year=year, cities=item['cities'], cities_data=spider.data)
            
            self.database[self.collection_name].insert_one(db_data)

        return item

    def close_spider(self, spider):
        """
        Closing database.
        """
        self.client.close()