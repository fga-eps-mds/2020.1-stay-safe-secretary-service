"""
Import scrapy, selenium functions and SpItem.
"""
import scrapy
import time
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from scrapy.selector import Selector

from utils.crimes_nature import crimes_nature_sp
from utils.treat_data_sp import get_city_data_by_month
from ..items import CrimesItem


class CrimesSP(scrapy.Spider):
    """
    Spider of SSP-SP.
    """
    name = "crimes_sp"
    allowed_domains = ['https://www.ssp.sp.gov.br/']
    start_urls = ['https://www.ssp.sp.gov.br/estatistica/pesquisa.aspx']

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Remote('http://selenium:4444/wd/hub', options=options)

    def parse(self, response):
        """
        Function to get all crimes statistics and save on data attribute.
        """
        self.driver.get(response.url)
        time.sleep(2)
        
        cities_list = response.xpath('//*[@id="conteudo_ddlMunicipios"]//option')
        time.sleep(2)

        # Click on "Ocorrências Registradas por Mês" button
        self.driver.find_element_by_xpath('//*[@id="conteudo_btnMensal"]').click()
        time.sleep(2)

        for city in range (1, len(cities_list)-1):
            # Select "Todos" on "Regiões" dropdown
            select_regions = Select(WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="conteudo_ddlRegioes"]'))))
            select_regions.select_by_value('0')
            time.sleep(2)
            
            # Select a city on "Munícipios" dropdown
            select_cities = Select(WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="conteudo_ddlMunicipios"]'))))
            select_cities.select_by_value(str(city))
            time.sleep(2)

            source = self.driver.page_source
            selector = Selector(text=source)
            time.sleep(1)

            city_name = selector.xpath(
                '//*[@id="conteudo_lkMunicipio"]/text()').get().replace(' | ', '')
            time.sleep(1)

            # Iterate over the three years of city data
            for table in range(0, 3):
                table_crimes_year = selector.xpath(
                    f'//*[@id="conteudo_repAnos_gridDados_{str(table)}"]/tbody//tr')

                year = selector.xpath(
                    f'//*[@id="conteudo_repAnos_lbAno_{str(table)}"]/text()').get()

                annual_city_data = []
                # Iterate over all crimes and save the crimes that are in crimes_nature_sp list
                for i, crime in enumerate(table_crimes_year):
                    if i > 0:
                        crime_data = {}

                        # Get a crime and check if it are in crimes_nature_sp list
                        crime_nature = crime.xpath('./td[1]/text()').get()
                        if crime_nature in crimes_nature_sp.keys():
                            crime_data['nature'] = crimes_nature_sp[crime_nature]

                            monthly_quantity = []
                            # Get the crime quantity of all months
                            for month in range(2, 14):
                                crime_quantity = crime.xpath(
                                    f'./td[{month}]/text()').get()

                                # Check if the monthly data doesn't exist yet
                                if crime_quantity == '...':
                                    break
                                
                                crime_quantity = int(crime_quantity.replace('.', ''))
                                monthly_quantity.append(crime_quantity)

                            crime_data['quantities'] = monthly_quantity

                            annual_city_data.append(crime_data)
                
                # Iterate over the annual_city_data and get the data by month
                for month in range(len(annual_city_data[0]['quantities'])):
                    monthly_data = get_city_data_by_month(annual_city_data, month)

                    # Go to the method process_item on pipeline
                    # to save a monthly data of a city on database.
                    yield CrimesItem(
                        city=city_name,
                        period=f'{month+1}/{year}',
                        monthly_data=monthly_data
                    )

        self.driver.close()
