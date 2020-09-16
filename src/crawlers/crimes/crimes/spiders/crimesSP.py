import scrapy
import time
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
        cities_list = []
        self.driver.get(response.url)
        table = self.driver.find_element_by_xpath('//*[@id="conteudo_ddlMunicipios"]')
        table_items = table.find_elements_by_tag_name('option')
        
        for i in range (1, len(table_items) - 1):
            select_regions = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo_ddlRegioes"]'))))
            select_regions.select_by_value('0')
            
            select_cities = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo_ddlMunicipios"]'))))
            select_cities.select_by_value(str(i))

            time.sleep(2)
            
            source = self.driver.page_source
            sel = Selector(text=source) 
            data = sel.xpath('//*[@id="conteudo_lkMunicipio"]').get()
            
            import ipdb; ipdb.set_trace()
        
        self.driver.close()