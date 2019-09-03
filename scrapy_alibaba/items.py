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
    
    
class Spider2Item(scrapy.Item):
    category_url = scrapy.Field()
    

class Spider3Item(scrapy.Item):
    # define fields for your items:
    business_supplier = scrapy.Field()
    gold_status = scrapy.Field()
    gold_years = scrapy.Field()
    #trade_assurance = scrapy.Field()
    main_products = scrapy.Field()
    supplier_url = scrapy.Field()
    contacts_url = scrapy.Field()
    
class Spider4Item(scrapy.Item):
    business_supplier2 = scrapy.Field()
    supplier_url2 = scrapy.Field()
    rating = scrapy.Field()
    transactions = scrapy.Field()
    fulfilment = scrapy.Field()
    url = scrapy.Field()
    #all_products = scrapy.Field()
    
    
class Spider5Item(scrapy.Item):
    contact_url = scrapy.Field()
    contact_name = scrapy.Field()
    address = scrapy.Field()
    zipcode = scrapy.Field()
    country = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    website = scrapy.Field() 
    