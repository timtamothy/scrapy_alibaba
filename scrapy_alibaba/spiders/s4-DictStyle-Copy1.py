# -*- coding: utf-8 -*-
import scrapy
from time import sleep
import pandas as pd
#scrapy crawl s4health -o /Users/swang/scrapy_alibaba/scrapy_write/healths4.csv

class Alibaba_S4(scrapy.Spider):
    name = 's4health'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        df = pd.read_csv('/Users/swang/scrapy_alibaba/scrapy_read/health_clean.csv')
        url_list = df.supplier_url.tolist()
        for url in url_list:                
            yield scrapy.Request(url, callback=self.parse, #meta = {'proxy': '95.211.175.167:13150'}
                                )
        

    def parse(self, response):
        
        supplier_url = response.request.url
        supplier_name = response.xpath("//span[@class='title-text']/text()").extract()
        if response.xpath("//div[@class='total-score']/text()") is not None:
            rating = response.xpath("//div[@class='total-score']/text()").extract()
        else:
            rating = 'None'
        markets = []    
        market = response.xpath("//div[@class='main-markets']//div/text()").extract()
        if market is not None:
            for i in market:
                markets.append(i.replace(',', ', '))
        fulfillment = response.xpath('//table/tr[1]/td[2]/div/div/div/text()').extract()        
                
        
        data = {}
        data['supplier_url'] = supplier_url
        data['supplier_name'] = supplier_name
        data['rating'] = rating
        data['market'] = markets
        data['supplier_type'] = fulfillment
        
        sleep(.2)
        yield data 
        