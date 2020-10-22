import scrapy
import requests
from ..items import CoordinatesItem


class MapsSP(scrapy.Spider):
    name = 'maps_sp'
    allowed_domains = "https://www.ssp.sp.gov.br/"
    start_urls = ["https://www.ssp.sp.gov.br/estatistica/pesquisa.aspx"]

    def parse(self, response):
        payload = {
            'city': "City",
            'state': "São Paulo", 
            'contry': "Brazil", 
            'polygon_geojson': "1", 
            'format': "jsonv2" }

        cities_table = response.xpath('//*[@id="conteudo_ddlMunicipios"]/option')
        for city in cities_table[1:]:
            city_str = city.xpath("./text()").get().strip()
            
            payload.update({'city': city_str})

            r = requests.get("https://nominatim.openstreetmap.org/search.php", params=payload)
            json_city = r.json()[0]
            coordinates = json_city.get('geojson').get('coordinates')[0]

            yield CoordinatesItem(
                state="São Paulo",
                city=city_str,
                coordinates=coordinates)