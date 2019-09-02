# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
import csv
import os

from scrapy_alibaba.items import ScrapyAlibabaItem


class AlibabaCrawlerSpider(scrapy.Spider):
    name = 'alibaba_draf1'
    
    def start_requests(self):
        urls = ['https://www.alibaba.com/products/doors.html?spm=a2700.galleryofferlist.pagination.1.2669189flzhOGI&IndexArea=product_en&page='+str(i) for i in range(1, 101)]

        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
            

    def parse(self, response):
        parser = scrapy.Selector(response)
        products = parser.xpath("//div[@class='item-main']")
    
        #Defining the XPaths
        XPATH_PRODUCT_NAME = ".//div[@class='item-info']//h2[contains(@class,'title')]//a/@title"
            #XPATH_PRODUCT_PRICE =  ".//div[@class='item-info']//div[@class='price']/b/text()"
            #XPATH_PRODUCT_MIN_ORDER = ".//div[@class='item-info']//div[@class='min-order']/b/text()"
        XPATH_SELLER_YEARS = ".//div[@class='item-info']//div[@class='stitle']//div[contains(@class,'s-gold-supplier-year-icon')]//text()"
        XPATH_SUPPLIER = ".//div[@class='item-info']//div[@class='stitle']//a/@title"
            #XPATH_SELLER_RESPONSE_RATE = ".//div[@class='item-info']//div[@class='sstitle']//div[@class='num']/i/text()"
            #XPATH_TRANSACTION_LEVEL = ".//div[@class='item-info']//div[@class='sstitle']//a[@class='diamond-level-group']//i[contains(@class,'diamond-level-one')]"
            #XPATH_TRANSACTION_LEVEL_FRACTION = ".//div[@class='item-info']//div[@class='sstitle']//a[@class='diamond-level-group']//i[contains(@class,'diamond-level-half-filled')]"        
            #XPATH_PRODUCT_LINK = ".//div[@class='item-info']//h2/a/@href"
        XPATH_GOLD = ".//div[@class='item-info']//div[@class='sstitle']//div[@class='supplier']//a/i"
            
        

        product_name = products.xpath(XPATH_PRODUCT_NAME).extract()
            #raw_product_price = products.xpath(XPATH_PRODUCT_PRICE).extract()
            #raw_minimum_order = products.xpath(XPATH_PRODUCT_MIN_ORDER).extract()
        
        supplier_name = products.xpath(XPATH_SUPPLIER).extract()
            #raw_seller_response_rate = products.xpath(XPATH_SELLER_RESPONSE_RATE).extract()
            #raw_transaction_level = products.xpath(XPATH_TRANSACTION_LEVEL).extract()
            #raw_product_link = products.xpath(XPATH_PRODUCT_LINK).extract()
        gold_status = products.xpath(XPATH_GOLD).extract()
        
            #getting the fraction part
            #raw_transaction_level_fraction = products.xpath(XPATH_TRANSACTION_LEVEL_FRACTION)

            # cleaning the data
        #product_name = '; '.join(raw_product_name).strip() if raw_product_name else None
            #product_price = ', '.join(raw_product_price).strip() if raw_product_price else None
            #minimum_order = ''.join(raw_minimum_order).strip() if raw_minimum_order else None
            
        #raw_seller_years = products.xpath(XPATH_SELLER_YEARS).extract()
        #seller_years_on_alibaba = ''.join(raw_seller_years).strip() if raw_seller_years else None
        #supplier_name = '; '.join(raw_supplier_name).strip() if raw_supplier_name else None
            #seller_response_rate = ''.join(raw_seller_response_rate).strip() if raw_seller_response_rate else None
            #getting actual transaction levels by adding the fraction part
            #transaction_level = len(raw_transaction_level)+.5 if raw_transaction_level_fraction else len(raw_transaction_level)
            #product_link = "https:"+raw_product_link[0] if raw_product_link else None

        
        result = zip(product_name, supplier_name, gold_status) #raw_seller_years)
        
        for product, supplier, gold in result:
            item = ScrapyAlibabaItem()
            item['product'] = product
            item['supplier'] = supplier
            item['gold'] = gold
            #item['years'] = years
            yield item
        
        

