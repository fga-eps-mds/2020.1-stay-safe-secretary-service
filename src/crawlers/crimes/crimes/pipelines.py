"""
Import scrapy, pymongo and utils functions to load data.
"""
import datetime
import pymongo
from utils.treat_data_df import load_data
from utils.treat_data_sp import get_cities_data_by_year
from utils.handle_folders import delete_folder

class CrimesPipeline:
    """
    Pipeline of spider Crimes DF.
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

    def close_spider(self, spider):
        """
        Treating the data per year and save on database.
        """
        for year in spider.data['years']:
            db_data = {}

            date = datetime.datetime.now()
            db_data['capture_data'] = f'{date.strftime("%d")}/{date.strftime("%m")}/{date.strftime("%Y")}'

            db_data['period'] = {
                'year': year
            }

            db_data["cities"] = load_data(spider.data['cities'], year)

            self.database[self.collection_name].insert_one(db_data)

            delete_folder(f'data/{str(year)}')

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