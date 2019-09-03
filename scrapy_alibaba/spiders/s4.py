# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
# import the class Spider4Item from the items file in scrapy_alibaba directory
from scrapy_alibaba.items import Spider4Item
from time import sleep
import csv
import pandas as pd


class Alibaba_s3(scrapy.Spider):
    name = 'spider4supplierprofile'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        df = pd.read_csv('/Users/swang/scrapy_alibaba/supplier_B_clean.csv')
        url_list = df.supplier_url.tolist()
        for url in url_list[0:10]:
            url = 'https://'+url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #parser = scrapy.Selector(response)
        supplier_url = response.request.url
        supplier_name = response.xpath("//span[@class='title-text']/text()").extract()
        
        
        if response.xpath("//div[@class='total-score']/text()") is not None:
            rating = response.xpath("//div[@class='total-score']/text()").extract()
        else:
            rating = None
        
        transactions = response.xpath("//div[@class='transaction-detail-content']/text()").extract_first()
        
        url = response.request.url
        #fulfilment = response.xpath("//div[contains(@class,'next-row')]/div/div[contains(@title,'Manufacturer')]/text()").extract()
        
        #product_post = response.xpath("//li[@class='nav-item']/a[@class='nav-link']/@href")[1].extract()
        
    
        result = zip(supplier_name, supplier_url, rating, transactions, url)
        
        for supplier_name, supplier_url, rating, transactions, url in result:
            item = Spider4Item()
            item['business_supplier2'] = supplier_name
            print('THIS IS THE SUPPLIER URL INSIDE THE ZIP:' + supplier_url)
            item['supplier_url2'] = supplier_url
            item['rating'] = rating
            item['transactions'] = transactions
            item['url'] = url
            #item['trade_assurance'] = trade_clean
            #item['fulfilment'] = fulfilment
            yield item
        
        sleep(.300)
            
        #if next_page is not None:
            #yield scrapy.Request(next_page, callback=self.parse)
