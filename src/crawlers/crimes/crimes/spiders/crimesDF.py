"""
Import scrapy and utils functions.
"""
import urllib.request
import scrapy

from utils.handle_folders import create_folder
from utils.handle_folders import delete_folder
from utils.treat_data_df import get_data_from_excel
from ..items import CrimesItem


class CrimesDF(scrapy.Spider):
    """
    Spider of SSP-DF.
    """
    name = 'crimes_df'
    allowed_domains = "http://www.ssp.df.gov.br/"
    start_urls = ["http://www.ssp.df.gov.br/dados-por-regiao-administrativa/"]

    def parse(self, response):
        """
        Function to get all the excel files and save.
        """
        cities_table = response.xpath('//*[@id="conteudo"]/table[2]/tbody//tr')

        create_folder('data')

        for i, city in enumerate(cities_table):
            if i > 1:
                city_name = city.xpath(
                    './td[1]/strong/text()').get().replace('/', " ")

                # Get a list of all columns of the city row
                columns_table = city.xpath('.//td')

                # Initial year of the data
                year = 2018

                # Download the annual excel table of a city
                for excel_table in range(16, len(columns_table) + 1, 2):
                    data_url = city.xpath(f'./td[{excel_table}]/a/@href').get()

                    if data_url is not None:
                        # Download and save the excel table
                        urllib.request.urlretrieve(
                            str(data_url),
                            f'./data/{city_name}.xlsx')

                        annual_city_data = get_data_from_excel(city_name)
                        # Iterate over the annual_city_data and get the data by month
                        for month, monthly_data in enumerate(annual_city_data):
                            # Go to the method process_item on pipeline
                            # to save a monthly data of a city on database.
                            yield CrimesItem(
                                city=city_name,
                                period=f'{month+1}/{year}',
                                monthly_data=monthly_data
                            )

                    year += 1

        delete_folder('data')
