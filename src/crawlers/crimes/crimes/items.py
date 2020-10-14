# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DfItem(scrapy.Item):
    year = scrapy.Field()
    city = scrapy.Field()
    
    pass

class SpItem(scrapy.Item):
    year = scrapy.Field()
    city = scrapy.Field()
    data = scrapy.Field()
    
    pass
