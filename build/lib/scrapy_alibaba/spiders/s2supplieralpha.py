# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
# import the class Spider3Item from the items file in scrapy_alibaba directory
from scrapy_alibaba.items import Spider2Item
from time import sleep


class Alibaba_s2(scrapy.Spider):
    name = 'spider2'
    allowed_domains = ['alibaba.com']
    start_urls = ['https://www.alibaba.com/suppliers/supplier-A_1.html']
    
    def parse(self, response):
        #empty list to iterate through in for loop
        alpha_supplier_urls = []
        #scraped URL stems from the website (they dont include www.alibaba.com)
        alpha_s_path_url = response.xpath("//span[@id='PagesBoxPageAll']/a/@href").extract()
        #adding the https://www.alibaba.com to all the scraped URLS
        for url in alpha_s_path_url:
            alpha_supplier_urls.append('https://www.alibaba.com'+url)
            print(url)
            
        for url in alpha_supplier_urls:    
            yield scrapy.Request(url, callback=self.parse_2)
            
        
    def parse_2(self, response):
        category_urls = response.xpath("//div[@class='colRmargin']/div[contains(@class,'column one4')]/a/@href").extract()
        category_name = response.xpath("//div[@class='colRmargin']/div[contains(@class,'column one4')]/a/text()").extract()
        
        result = zip(category_name)
        for category_name in result:
            item = Spider2Item()
            item['alphabet'] = category_name
            yield item

   