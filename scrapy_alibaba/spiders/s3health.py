# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy_alibaba.items import Spider3Item
from time import sleep
import csv
import re
cleanr = re.compile('<.*?>') 

class Alibaba_s3(scrapy.Spider):
    name = 's3health'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        url_list=['https://www.alibaba.com/trade/search?indexArea=company_en&f1=y&n=38&viewType=L&SearchText=health', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.53.3.54991f13iJy8SE&indexArea=company_en&keyword=health&viewType=L&n=38&category=16&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.2.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=100003172&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.3.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=100009383&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.4.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=100003100&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.5.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=201900027&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.6.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=100003119&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.7.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=100009304&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.8.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=100009267&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.9.38ac1f13A6aaFT&indexArea=company_en&n=38&viewType=L&keyword=health&category=100002660&f1=y', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.3.69a61f13aqKFS9&viewType=L&n=38&f1=y&category=100009254&indexArea=company_en&keyword=health']
            
        for url in url_list:                
            yield scrapy.Request(url, callback=self.parse)

        #meta = {'proxy': '95.211.175.167:13150'}    
    def parse(self, response):
        parser = scrapy.Selector(response)
        sobox = parser.xpath("//div[@class='item-main']")
        
        data = {}
        
        for sbox in sobox:
            supplier = sbox.xpath(".//h2[@class='title ellipsis']/a/text()").extract() 
            gold_status = sbox.xpath(".//div[@class='company']/a[1]/text()[2]").extract_first()
            
            #gold_clean = []
            #for n in gold_status:
            #     gold_clean.append(n.strip())
            
            gold_years = sbox.xpath(".//div[@class='s-gold-supplier-year-icon']/text()").extract_first()
            
            #if sbox.xpath(".//div[@class='value ellipsis ph']/@title") is not None:
            main_product = sbox.xpath(".//div[@class='value ellipsis ph']/@title").extract_first()
            #main_product = re.sub(cleanr, "", main_product.astype(str)).replace(',', ', ')
            
            #mainProduct = []
            #for i in main_product:
            #    cleanproduct = i.strip().replace(',', ', ')
            #    cleanproduct = re.sub(cleanr, '', cleanproduct)
            #    mainProduct.append(cleanproduct)
            supplier_url = sbox.xpath(".//h2[contains(@class,'title ellipsis')]/a/@href").extract_first()
            supplier_url = supplier_url.replace('http','https')
            contacts_url = sbox.xpath(".//a[@class='cd']/@href").extract_first()
            contacts_url = contacts_url.replace('http','https')
            
            data['category'] = "Health"
            data['business_supplier'] = supplier
            data['gold_status'] = gold_status
            data['gold_years'] = gold_years
            data['main_products'] = main_product
            data['supplier_url'] = supplier_url
            data['contacts_url'] = contacts_url
            
            yield data
            
        
        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        next_page = "https:" + next_page
           
        
        sleep(.100)
            
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
