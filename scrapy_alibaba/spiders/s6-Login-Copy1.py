# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.chrome.options import Options
options = Options()
#options.headless = True
from selenium.common.exceptions import NoSuchElementException

class Alibaba_S6(scrapy.Spider):
    name = 'seleniumspiderA'
    allowed_domains = ['alibaba.com']
    start_urls = ['https://login.alibaba.com']
   
    

    def parse(self, response):
        chromedriver = webdriver.Chrome(executable_path = '/Users/swang/scrapy_alibaba/chromedriver')
        login_url = 'https://login.alibaba.com'
        chromedriver.get(login_url)
        
        email = chromedriver.find_element_by_id('fm-login-id')
        email.send_keys('butterbuttscoffee@yahoo.com')

        password = chromedriver.find_element_by_id('fm-login-password')
        password.send_keys('jigglypuff1')
        sleep(1)
        
        sign_in = chromedriver.find_element_by_id('fm-login-submit')
        sign_in.click()

        sleep(2)
        
        data = {}

        df = pd.read_csv('/Users/swang/scrapy_alibaba/Scrapy Data/supplier_names_https.csv')
        url_list = df.contacts_url.tolist()
        start_urls = url_list
        for url in start_urls[0:25000]:
            chromedriver.get(url)
            
            
            try:
                view_details = chromedriver.find_element_by_xpath('//div[@class="sens-mask"]/a')
            except NoSuchElementException:
                data['Url'] = url
                data['Telephone:'] = "No Contacts"
            else:
                view_details.click()
                sleep(.300)
             
            
                try:
                    tele = chromedriver.find_element_by_xpath('//table[@class="info-table"]//tr/td')
                except NoSuchElementException:
                    data['Url'] = url
                    data['Telephone:'] = "No Telephone"
                else:
                    data['Url'] = url
                    phone = tele.text
                    data['Telephone:'] = phone

            yield data

        

    
