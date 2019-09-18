# -*- coding: utf-8 -*-
import scrapy
from time import sleep
import pandas as pd

class Alibaba_S5(scrapy.Spider):
    name = 's5health'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        df = pd.read_csv('/Users/swang/scrapy_alibaba/scrapy_read/health_clean.csv')
        url_list = df.contacts_url.tolist()
        for url in url_list:                
            yield scrapy.Request(url, callback=self.parse #meta = {'proxy': '95.211.175.167:13150'}
                                )

    def parse(self, response):
        contact_url = response.request.url
        contact_name = response.xpath('//div[@class="contact-name"]/text()').extract()
        contact_dept = response.xpath('//div[@class="contact-department"]/text()').extract()
        
        table_rows = response.xpath('//*[contains(@class, "info-table")]//tr')
        data = {}
        data['contact_url'] = contact_url
        data['contact_name'] = contact_name
        data['contact_dept'] = contact_dept
        data['Telephone:'] = None
        data['Mobile Phone:'] = None
        data['Fax:'] = None
        data['Address:'] = None
        data['Zip:'] = None
        data['Country/Region:'] = None
        data['Province/State:'] = None
        data['City:'] = None
        
        for table_row in table_rows:
            category = table_row.xpath('th/text()').extract_first()
            if table_row.xpath('td/text()').extract_first() is not None:
                value = table_row.xpath('td/text()').extract_first()
            else:
                value = 0
            data[category] = value
        
        yield data
        sleep(.250)