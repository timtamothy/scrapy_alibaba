# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
import pandas as pd

chomedriver = webdriver.Chrome(executable_path = '/Users/swang/scrapy_alibaba/chromedriver')

df = pd.read_csv('/Users/swang/scrapy_alibaba/supplier_BCleanhttps.csv')
url_list = df.contacts_url.tolist()
url = url[0]

chromedriver.get(url)
sleep(3)

view_details = chromedriver.find_element_by_xpath('//div[@class="sens-mask"]/a') 
view_details.click()
sleep(3)

sign_in_tab = chromedriver.find_element_by_xpath('//li[@class="sc-hd-prefix2-tab-trigger"]/a')
sign_in_tab.click()
sleep(3)












class Alibaba_S6(scrapy.Spider):
    name = 'seleniumspider'
    allowed_domains = ['alibaba.com']
    df = pd.read_csv('/Users/swang/scrapy_alibaba/supplier_BCleanhttps.csv')
    url_list = df.contacts_url.tolist()
    start_urls = url_list
    
    def __init__(self, **kwargs):
        print kwargs
        self.sel = selenium('localhost', 4444, )

    def parse(self, response):
      
        contact_url = response.request.url
        contact_name = response.xpath('//div[@class="contact-name"]/text()').extract()
        contact_dept = response.xpath('//div[@class="contact-department"]/text()').extract()
        
        table_rows = response.xpath('//*[contains(@class, "info-table")]//tr')
        data = {}
        data['contact_url'] = contact_url
        data['contact_name'] = contact_name
        data['contact_dept'] = contact_dept
        for table_row in table_rows:
            category = table_row.xpath('th/text()').extract_first()
            if table_row.xpath('td/text()').extract_first() is not None:
                value = table_row.xpath('td/text()').extract_first()
            else:
                value = 0
            data[category] = value
        
        yield data
        sleep(.500)