# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = False

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15'

options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15")



class Alibaba_S6(scrapy.Spider):
    name = 'seleniumspider3'
    allowed_domains = ['alibaba.com']
    start_urls = ['https://login.alibaba.com']
   
    

    def parse(self, response):
        chromedriver = webdriver.Chrome(options=options, executable_path = '/home/swang/chromedriver')
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

        df = pd.read_csv('/home/swang/scrapy_read/supplier_names_https.csv')
        url_list = df.contacts_url.tolist()
        start_urls = url_list
        for url in start_urls[0:10]:
            chromedriver.get(url)
            
            sleep(1)
            #view_details = chromedriver.find_element_by_xpath('//div[@class="sens-mask"]/a')
            view_details = chromedriver.find_element_by_xpath('//table/tr[1]/td/div/a')
            view_details.click()
            #sleep(.300)
                                                              
            tele = chromedriver.find_element_by_xpath('//table[@class="info-table"]//tr/td')
            phone = tele.text
            data['Url'] = url
            data['Telephone:'] = phone
            yield data

        

    
