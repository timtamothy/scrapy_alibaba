# -*- coding: utf-8 -*-
import scrapy
import csv
import os


class AlibabaCrawlerSpider(scrapy.Spider):
    name = 'alibaba_crawl_copy'
    #allowed_domains = ['alibaba.com']
    #start_urls = ['https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=headphones&viewtype=G&tab=']
    
    #search_text = "headphones"
    
    #def start_requests(self):
    #Read keywords from keywords file and construct the search URL
    # The meta is used to send our search text into the parser as metadata
       # start_urls = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=headphones&viewtype=G&tab='
       # search_text = "headphones"
       # url = start_urls
       # yield scrapy.Request(url, callback = self.parse, meta = {"search_text": search_text})
    
    def start_requests(self):
        urls = ['https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=headphones&viewtype=G&tab=']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
    

    def parse(self, response):
        """Function to process alibaba search results page"""
        #search_keyword = response.meta["search_text"]
        parser = scrapy.Selector(response)
        products = parser.xpath("//div[@class='item-main']")
    
        #iterating over search results  
        for product in products:
        #Defining the XPaths
            XPATH_PRODUCT_NAME = ".//div[@class='item-info']//h2[contains(@class,'title')]//a/@title"
            XPATH_PRODUCT_PRICE =  ".//div[@class='item-info']//div[@class='price']/b/text()"
            XPATH_PRODUCT_MIN_ORDER = ".//div[@class='item-info']//div[@class='min-order']/b/text()"
            XPATH_SELLER_YEARS = ".//div[@class='item-info']//div[@class='stitle']//div[contains(@class,'s-gold-supplier-year-icon')]//text()"
        #".//div[@class='item-info']//div[@class='stitle util-ellipsis']//div[contains(@class,'supplier-year')]//text()"
        #XPATH_SELLER_NAME = 
        #".//div[@class='item-info']//div[@class='stitle util-ellipsis']//a/@title"
            XPATH_SUPPLIER = ".//div[@class='item-info']//div[@class='stitle']//a/@title"
            XPATH_SELLER_RESPONSE_RATE = ".//div[@class='item-info']//div[@class='sstitle']//div[@class='num']/i/text()"
            XPATH_TRANSACTION_LEVEL = ".//div[@class='item-info']//div[@class='sstitle']//a[@class='diamond-level-group']//i[contains(@class,'diamond-level-one')]"
            XPATH_TRANSACTION_LEVEL_FRACTION = ".//div[@class='item-info']//div[@class='sstitle']//a[@class='diamond-level-group']//i[contains(@class,'diamond-level-half-filled')]"        
            XPATH_PRODUCT_LINK = ".//div[@class='item-info']//h2/a/@href"
            
        

            raw_product_name = products.xpath(XPATH_PRODUCT_NAME).extract()
            raw_product_price = products.xpath(XPATH_PRODUCT_PRICE).extract_first().strip()
            raw_minimum_order = products.xpath(XPATH_PRODUCT_MIN_ORDER).extract()
            raw_seller_years = products.xpath(XPATH_SELLER_YEARS).extract_first()
            #raw_seller_name = products.xpath(XPATH_SELLER_NAME).extract()
            raw_supplier_name = products.xpath(XPATH_SUPPLIER).extract()
            raw_seller_response_rate = products.xpath(XPATH_SELLER_RESPONSE_RATE).extract()
            raw_transaction_level = products.xpath(XPATH_TRANSACTION_LEVEL).extract()
            raw_product_link = products.xpath(XPATH_PRODUCT_LINK).extract()
        
            #getting the fraction part
            raw_transaction_level_fraction = products.xpath(XPATH_TRANSACTION_LEVEL_FRACTION)

            # cleaning the data
            product_name = ''.join(raw_product_name).strip() if raw_product_name else None
            product_price = ''.join(raw_product_price).strip() if raw_product_price else None
            minimum_order = ''.join(raw_minimum_order).strip() if raw_minimum_order else None
            seller_years_on_alibaba = ''.join(raw_seller_years).strip() if raw_seller_years else None
            supplier_name = ''.join(raw_supplier_name).strip() if raw_supplier_name else None
            seller_response_rate = ''.join(raw_seller_response_rate).strip() if raw_seller_response_rate else None
            #getting actual transaction levels by adding the fraction part
            transaction_level = len(raw_transaction_level)+.5 if raw_transaction_level_fraction else len(raw_transaction_level)
            product_link = "https:"+raw_product_link[0] if raw_product_link else None

            yield {
                'product_name':product_name,
                'product_price':product_price,
                'minimum_order':minimum_order,
                'seller_years_on_alibaba':seller_years_on_alibaba,
                'supplier_name':supplier_name,
                'seller_response_rate':seller_response_rate,
                'transaction_level':transaction_level,
                'product_link':product_link,
                #'search_text':search_keyword
                }

