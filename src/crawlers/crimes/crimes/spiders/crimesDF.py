"""
Import scrapy and utils functions.
"""
import urllib.request
import scrapy

from utils.handle_folders import create_folder
from ..items import DfItem

class CrimesDF(scrapy.Spider):
    """
    Spider of SSP-DF.
    """
    name = 'crimes_df'
    allowed_domains = "http://www.ssp.df.gov.br/"
    start_urls = ["http://www.ssp.df.gov.br/dados-por-regiao-administrativa/"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'crimes.pipelines.DfPipeline': 300,
        }
    }

    def parse(self, response):
        """
        Function to get all the excel files and save.
        """
        data_table = response.xpath('//*[@id="conteudo"]/table[2]/tbody//tr')

        create_folder('data')

        for i, city in enumerate(data_table):
            if i > 1:
                city_name = city.xpath(
                    './td[1]/strong/text()').get().replace('/', " ")

                # Get a list of all columns of the city row
                columns_table = city.xpath('.//td')

                # Initial year of the data
                year = 2018

                # Download the annual excel table of a city
                # and process the item to save on database.
                for excel_table in range(16, len(columns_table) + 1, 2):
                    data_url = city.xpath(f'./td[{excel_table}]/a/@href').get()

                    if data_url is not None:
                        # Download and save the excel table
                        urllib.request.urlretrieve(
                            str(data_url),
                            f'./data/{city_name}.xlsx')

                        # Create a new DfItem and process it for each annual table of a city
                        spiderItem = DfItem(year=year, city=city_name)
                        yield spiderItem

                    year += 1
