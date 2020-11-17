# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""
Crimes Item to be processed, the item must follow the pattern below:
    CrimesItem(
        city: 'Águas Claras', 
        period: '1/2020',
        monthly_data: [
            { 'nature': 'Latrocínio', 'quantity': 5 },
            { 'nature': 'Roubo a Pedestre', 'quantity': 7 },
            { 'nature': 'Roubo de Veículo', 'quantity': 10 },
            ...
        ]
    )
"""
class CrimesItem(scrapy.Item):
    city = scrapy.Field()
    period = scrapy.Field()
    monthly_data = scrapy.Field()

    pass
