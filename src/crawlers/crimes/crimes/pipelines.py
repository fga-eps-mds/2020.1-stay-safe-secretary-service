from itemadapter import ItemAdapter
from utils.treat_dataDF import load_data
import datetime
import pymongo
from scrapy.utils.project import get_project_settings
from utils.handle_folders import delete_folder

class CrimesPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.collection_name = spider.name
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        for year in spider.data['years']:
            db_data = {}

            date = datetime.datetime.now()
            db_data['capture_data'] = f'{date.strftime("%d")}/{date.strftime("%m")}/{date.strftime("%Y")}'
            
            db_data['period'] = {
                'year': year
            }

            db_data["cities"] = load_data(spider.data['cities'], year)

            self.db[self.collection_name].insert_one(db_data)

            delete_folder(f'data/{str(year)}')

        delete_folder('data')

        self.client.close()

