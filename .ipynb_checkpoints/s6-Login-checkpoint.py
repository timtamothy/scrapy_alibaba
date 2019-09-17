# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
import pandas as pd


class Alibaba_S6(scrapy.Spider):
    name = 'seleniumspider'
    allowed_domains = ['alibaba.com']
   

    def start_requests(self):
        chromedriver = webdriver.Chrome(executable_path = '/Users/swang/scrapy_alibaba/chromedriver')
        login_url = 'https://login.alibaba.com'
        chromedriver.get(login_url)
        sleep(3)
        
        email = chromedriver.find_element_by_id('fm-login-id')
        email.send_keys('captainapollo@gmail.com')
        sleep(2)

        password = chromedriver.find_element_by_id('fm-login-password')
        password.send_keys('Heaven1')
        sleep(2)
        
        sign_in = chromedriver.find_element_by_id('fm-login-submit')
        sign_in.click()

        sleep(3)

        df = pd.read_csv('/Users/swang/scrapy_alibaba/supplier_BCleanhttps.csv')
        url_list = df.contacts_url.tolist()
        start_urls = url_list
            for url in start_urls[0:3]:
                yield scrapy.Request(url=url, cookies=driver.get_cookies(), callback=self.parse)

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
        for table_row in table_rows:
            category = table_row.xpath('th/text()').extract_first()
            if table_row.xpath('td/text()').extract_first() is not None:
                value = table_row.xpath('td/text()').extract_first()
            else:
                value = 0
            data[category] = value
        
        yield data
        

        
# Code for pop up logins:
#view_details = chromedriver.find_element_by_xpath('//div[@class="sens-mask"]/a') 
#view_details.click()
#sleep(3)

#sign_in_tab = chromedriver.find_element_by_xpath('//li[@class="sc-hd-prefix2-tab-trigger"]/a')
#sign_in_tab.click()
#sleep(3)

#chromedriver.switch_to.frame('alibaba-login-box')

