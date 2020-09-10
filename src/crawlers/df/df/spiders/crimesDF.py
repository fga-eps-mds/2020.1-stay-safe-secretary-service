import scrapy
import urllib.request
import datetime
import os
import ipdb
import json

class CrimesDF(scrapy.Spider):
    name = 'crimes'
    allowed_domains = "http://www.ssp.df.gov.br/"
    start_urls = ["http://www.ssp.df.gov.br/dados-por-regiao-administrativa/"]

    def parse(self, response):
        crime_table = response.xpath(
            '/html/body/div[8]/div/div/div/div[2]/table[2]/tbody//tr')
        
        for i, city in enumerate(crime_table):
           
            if (i > 1):
                city_name = city.xpath('./td[1]/strong/text()').get().replace('/', " ")
                city_url_2020 = city.xpath('./td[20]/a/@href').get()

                urllib.request.urlretrieve(str(city_url_2020), f'./excel/{city_name}.xlsx')
