import scrapy
import urllib.request
import datetime
import os
import json

class CrimesDF(scrapy.Spider):
    name = 'crimes'
    allowed_domains = "http://www.ssp.df.gov.br/"
    start_urls = ["http://www.ssp.df.gov.br/dados-por-regiao-administrativa/"]
    cities = []

    def parse(self, response):
        crime_table = response.xpath(
            '/html/body/div[8]/div/div/div/div[2]/table[2]/tbody//tr')
        
        for i, city in enumerate(crime_table):
            if (i > 1):
                city_name = city.xpath('./td[1]/strong/text()').get().replace('/', " ")
                self.cities.append(city_name)

                # Get a list of all tds of the row (collumns)
                td_list = city.xpath('.//td')

                # Initial year of the data
                year = 2018

                for j in range(16, len(td_list) + 1, 2):
                    data_url = city.xpath(f'./td[{j}]/a/@href').get()

                    if(data_url is not None):
                        # Download and save the excel table
                        urllib.request.urlretrieve(str(data_url), f'./data/{str(year)}/{city_name}.xlsx')

                    year += 1
