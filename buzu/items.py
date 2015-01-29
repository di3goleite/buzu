# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BuzuItem(scrapy.Item):
    route = scrapy.Field()
    source = scrapy.Field()
    terminals = scrapy.Field()
    schedule = scrapy.Field()
