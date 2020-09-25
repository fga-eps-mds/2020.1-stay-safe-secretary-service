"""
Import scrapy, selenium functions and SpItem.
"""
import scrapy
import time
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from scrapy.selector import Selector
from ..items import SpItem


class CrimesSP(scrapy.Spider):
    """
    Spider of SSP-SP.
    """
    name = "crimes_sp"
    allowed_domains = ['https://www.ssp.sp.gov.br/']
    start_urls = ['https://www.ssp.sp.gov.br/estatistica/pesquisa.aspx']

    custom_settings = {
        'ITEM_PIPELINES': {
            'crimes.pipelines.SpPipeline': 300,
        }
    }

    data = {}

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def parse(self, response):
        """
        Function to get all crimes statistics and save on data attribute.
        """
        self.driver.get(response.url)
        time.sleep(2)
        
        cities_list = response.xpath('//*[@id="conteudo_ddlMunicipios"]//option')
        time.sleep(2)

        self.driver.find_element_by_xpath('//*[@id="conteudo_btnMensal"]').click()
        time.sleep(2)

        crimes_nature = {
            'LATROCÍNIO': "Latrocinio",
            'TOTAL DE ESTUPRO (4)': 'Estupro',
            'ROUBO - OUTROS': 'Roubos',
            'ROUBO DE VEÍCULO': 'Roubo de Veiculo',
            'FURTO - OUTROS': 'Furtos',
            'FURTO DE VEÍCULO': 'Furto de Veiculo',
        }

        years = {}
        cities = []

        for i in range (1, len(cities_list)-1):
            select_regions = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo_ddlRegioes"]'))))
            select_regions.select_by_value('0')
            time.sleep(2)
            
            select_cities = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo_ddlMunicipios"]'))))
            select_cities.select_by_value(str(i))
            time.sleep(2)

            source = self.driver.page_source
            selector = Selector(text=source)
            time.sleep(1)

            city_name = selector.xpath('//*[@id="conteudo_lkMunicipio"]/text()').get().replace(' | ', '')
            cities.append(city_name)
            time.sleep(1)

            cities_data = {}
            # Iterate over the three years table of a city
            for j in range(0, 3):
                table_crimes_year = selector.xpath(f'//*[@id="conteudo_repAnos_gridDados_{str(j)}"]/tbody//tr')

                year = selector.xpath(f'//*[@id="conteudo_repAnos_lbAno_{str(j)}"]/text()').get()

                # Get the last month with data in a year
                if year not in years.keys():
                    months_data = selector.xpath(f'//*[@id="conteudo_repAnos_gridDados_{j}"]/tbody/tr[2]//td')

                    for month in range(1, 13):
                        month_quantity = months_data[month].xpath('./text()').get()
                        if month_quantity == '...':
                            month = month - 1
                            break
                    
                    years[year] = month

                annual_crimes_registers = []
                # Iterate over all crimes and save the crimes that are in crimes_nature list
                for k, crime in enumerate(table_crimes_year):
                    if k > 0:
                        crimes_data = {}
                        crime_nature = crime.xpath('./td[1]/text()').get()
                        if crime_nature in crimes_nature.keys():
                            crimes_data['crime_nature'] = crimes_nature[crime_nature]
                            crimes_data['quantity'] = int(crime.xpath(f'./td[14]/text()').get().replace('.', ''))

                            annual_crimes_registers.append(crimes_data)

                cities_data[year] = annual_crimes_registers

            self.data[city_name] = cities_data

        crawlerItem = SpItem()
        crawlerItem['years'] = years
        crawlerItem['cities'] = cities

        self.driver.close()

        yield crawlerItem