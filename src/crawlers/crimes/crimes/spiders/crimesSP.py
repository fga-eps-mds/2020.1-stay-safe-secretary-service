import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from scrapy.selector import Selector

class CrimesSP(scrapy.Spider):
    name = "crimes_sp"
    allowed_domains = ['https://www.ssp.sp.gov.br/']
    start_urls = ['https://www.ssp.sp.gov.br/estatistica/pesquisa.aspx']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        
        cities_list = response.xpath('//*[@id="conteudo_ddlMunicipios"]//option')

        self.driver.find_element_by_xpath('//*[@id="conteudo_btnMensal"]').click()

        crimes_nature = {
            'LATROCÍNIO': "Latrocinio",
            'TOTAL DE ESTUPRO (4)': 'Estupro',
            'ROUBO - OUTROS': 'Roubos',
            'ROUBO DE VEÍCULO': 'Roubo de Veiculo',
            'FURTO - OUTROS': 'Furtos',
            'FURTO DE VEÍCULO': 'Furto de Veiculo',
        }

        data = {}
        for i in range (1, len(cities_list)-1):
            select_regions = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo_ddlRegioes"]'))))
            select_regions.select_by_value('0')
            
            select_cities = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo_ddlMunicipios"]'))))
            select_cities.select_by_value(str(i))
            
            source = self.driver.page_source
            selector = Selector(text=source)

            city_name = selector.xpath('//*[@id="conteudo_lkMunicipio"]/text()').get().replace(' | ', '')

            city_data = []
            for j in range(0, 3):
                city_year_data = {}

                table_crimes_year = selector.xpath(f'//*[@id="conteudo_repAnos_gridDados_{str(j)}"]/tbody//tr')

                annual_crimes_registers = []
                for k, crime in enumerate(table_crimes_year):
                    if k > 0:
                        crimes_data = {}
                        crime_nature = crime.xpath('./td[1]/text()').get()
                        if crime_nature in crimes_nature.keys():
                            crimes_data['crime_nature'] = crimes_nature[crime_nature]
                            crimes_data['quantity'] = int(crime.xpath(f'./td[14]/text()').get().replace('.', ''))

                            annual_crimes_registers.append(crimes_data)

                city_year_data['year'] = int(selector.xpath(f'//*[@id="conteudo_repAnos_lbAno_{str(j)}"]/text()').get())
                city_year_data['crimes_data'] = annual_crimes_registers

                city_data.append(city_year_data)

            data[city_name] = city_data
        
        self.driver.close()