"""
Import scrapy and utils functions.
"""
import urllib.request
import scrapy
from utils.handle_folders import create_folder

class CrimesDF(scrapy.Spider):
    """
    Spider of SSP-DF.
    """
    name = 'crimes_df'
    allowed_domains = "http://www.ssp.df.gov.br/"
    start_urls = ["http://www.ssp.df.gov.br/dados-por-regiao-administrativa/"]

    data = {
        'years': [],
        'cities': [],
    }

    def parse(self, response):
        """
        Function to get all the excel files and save.
        """
        crime_table = response.xpath(
            '/html/body/div[8]/div/div/div/div[2]/table[2]/tbody//tr')

        create_folder('data')

        for i, city in enumerate(crime_table):
            if i > 1:
                city_name = city.xpath(
                    './td[1]/strong/text()').get().replace('/', " ")
                self.data['cities'].append(city_name)

                # Get a list of all tds of the row (collumns)
                td_list = city.xpath('.//td')

                # Initial year of the data
                year = 2018

                for j in range(16, len(td_list) + 1, 2):
                    data_url = city.xpath(f'./td[{j}]/a/@href').get()

                    if year not in self.data['years']:
                        create_folder(f'data/{str(year)}')
                        self.data['years'].append(year)

                    if data_url is not None:
                        # Download and save the excel table
                        urllib.request.urlretrieve(
                            str(data_url),
                            f'./data/{str(year)}/{city_name}.xlsx')

                    year += 1
