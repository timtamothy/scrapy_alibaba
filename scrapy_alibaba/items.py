# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyAlibabaItem(scrapy.Item):
    # define the fields for your item here like:
    product = scrapy.Field()
    supplier = scrapy.Field()
    years = scrapy.Field()
    gold = scrapy.Field()
    #pass
