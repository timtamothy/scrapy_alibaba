# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
# import the class Spider4Item from the items file in scrapy_alibaba directory
from scrapy_alibaba.items import Spider4Item
from time import sleep
import csv
import pandas as pd

class Alibaba_S4(scrapy.Spider):
    name = 'spider4profile'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        df = pd.read_csv('/Users/swang/scrapy_alibaba/supplier_BCleanhttps.csv')
        url_list = df.supplier_url.tolist()
        for url in url_list:                
            yield scrapy.Request(url, callback=self.parse)
            sleep(.500)

    def parse(self, response):
        
        supplier_url = response.request.url
        supplier_name = response.xpath("//span[@class='title-text']/text()").extract()
        if response.xpath("//div[@class='total-score']/text()") is not None:
            rating = response.xpath("//div[@class='total-score']/text()").extract()
        else:
            rating = 'None'
        
        #transactions = response.xpath("//div[@class='transaction-detail-content']/text()").extract_first()
        
        data = {}
        data['supplier_url'] = supplier_url
        data['supplier_name'] = supplier_name
        data['rating'] = rating
    
        yield data 
        sleep(.300)