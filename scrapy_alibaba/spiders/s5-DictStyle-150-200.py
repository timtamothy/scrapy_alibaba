# -*- coding: utf-8 -*-
import scrapy
from time import sleep
import pandas as pd

class Alibaba_S5(scrapy.Spider):
    name = 'spider5D'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        df = pd.read_csv('/home/swang/scrapy_read/supplier_names_https.csv')
        url_list = df.contacts_url.tolist()
        for url in url_list[150000:200000]:                
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        sleep(1)
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
        
        for table_row in table_rows:
            category = table_row.xpath('th/text()').extract_first()
            if table_row.xpath('td/text()').extract_first() is not None:
                value = table_row.xpath('td/text()').extract_first()
            else:
                value = 0
            data[category] = value
        
        yield data