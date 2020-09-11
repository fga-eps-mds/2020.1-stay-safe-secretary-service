from itemadapter import ItemAdapter
from utils.treat_dataDF import load_data
import datetime

# db_data = {
#     "_id": 1,
#     "capture_data": "04/08/2020",
#     "period": {
#         "start": "01/2020",
#         "end": "07/2020"
#     },
#     "cities": []
# }

class DfPipeline:
    data = []

    def process_item(self, item, spider):
        return item


    def close_spider(self, spider):
        for year in spider.data['years']:
            db_data = {}
            db_data["cities"] = load_data(spider.data['cities'], year)
            db_data['period'] = {
                'year': year
            }

            date = datetime.datetime.now()

            db_data['capture_data'] = f'{date.strftime("%d")}/{date.strftime("%m")}/{date.strftime("%Y")}'

            self.data.append(db_data)

        print(self.data)

            # TODO: Salvar no Banco
