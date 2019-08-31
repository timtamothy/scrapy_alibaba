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
       
        next_urls = response.xpath("//span[@id='PagesBoxPageAll']/a/@href").extract()
            for i in next_urls:
                i = 'https://www.alibaba.com'+i
        category_urls = response.xpath("//div[@class='colRmargin']/div[contains(@class,'column one4')]/a/@href").extract()
        category_name = response.xpath("//div[@class='colRmargin']/div[contains(@class,'column one4')]/a/text()").extract()
        
        
        print(next_urls)
        
        result = zip(category_name)
        for category_name in result:
            item = Spider2Item()
            item['alphabet'] = category_name
            yield item
        
        
        if next_url is not None:
            yield scrapy.Request(full_url, callback=self.parse)
        else:
            for url in category_urls:
                print(url)
    

   