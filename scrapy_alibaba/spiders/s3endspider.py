# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
# import the class Spider3Item from the items file in scrapy_alibaba directory
from scrapy_alibaba.items import Spider3Item
from time import sleep
import csv


class Alibaba_s3(scrapy.Spider):
    name = 'spider11end'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        with open('/Users/swang/scrapy_alibaba/supplier_alpha_urls.csv', 'rt', encoding='utf8') as file:
            reader = csv.reader(file, delimiter=' ', quotechar='|')
            next(reader)
            url_list=[]
            for row in reader:
                for url in row:
                    url_list.append(url)
        for url in url_list[11000000:]:                
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # instatiate the ItemLoader with your specific item class
        #load = ItemLoader(item=Spider3Item(), response=response)
        download_delay = .300
        
        parser = scrapy.Selector(response)
        sbox = parser.xpath("//div[@class='item-main']")
        
        
        supplier = sbox.xpath(".//h2[@class='title ellipsis']/a/text()").extract() 
        gold_status = sbox.xpath(".//div[@class='company']/a[1]/text()[2]").extract()
        gold_clean = []
        for n in gold_status:
            gold_clean.append(n.strip())
        gold_years = sbox.xpath(".//div[@class='s-gold-supplier-year-icon']/text()").extract()
        main_product = sbox.xpath(".//div[@class='value ellipsis ph']/@title").extract()
        for i in main_product:
            i = i.replace(',',', ')
        supplier_url = sbox.xpath(".//h2[contains(@class,'title ellipsis')]/a/@href").extract()
        contacts_url = sbox.xpath(".//a[@class='cd']/@href").extract()
        
        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        next_page = next_page.replace('http','https')
    
        result = zip(supplier, gold_clean, gold_years, main_product, supplier_url, contacts_url)
        
        for supplier, gold_clean, gold_years, main_product, supplier_url, contacts_url in result:
            item = Spider3Item()
            item['business_supplier'] = supplier
            item['gold_status'] = gold_clean
            item['gold_years'] = gold_years
            item['main_products'] = main_product
            item['supplier_url'] = supplier_url
            item['contacts_url'] = contacts_url
            yield item
        
        sleep(.300)
            
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
