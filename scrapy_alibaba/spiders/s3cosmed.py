# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy_alibaba.items import Spider3Item
from time import sleep
import csv
import re
cleanr = re.compile('<.*?>') 

class Alibaba_s3(scrapy.Spider):
    name = 's3cosmed'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        url_list=['https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.53.1.3ea96194xdhI7o&keyword=cosmetics&n=38&indexArea=company_en&viewType=L&f1=y&category=66', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.3.1f046194GWPoTx&f1=y&category=3306&n=38&indexArea=company_en&viewType=L&keyword=cosmetics', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.4.1f046194GWPoTx&f1=y&category=660103&n=38&indexArea=company_en&viewType=L&keyword=cosmetics', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.5.1f046194GWPoTx&f1=y&category=205846905&n=38&indexArea=company_en&viewType=L&keyword=cosmetics', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.6.1f046194GWPoTx&f1=y&category=100001117&n=38&indexArea=company_en&viewType=L&keyword=cosmetics', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.7.1f046194GWPoTx&f1=y&category=660101&n=38&indexArea=company_en&viewType=L&keyword=cosmetics', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.8.1f046194GWPoTx&f1=y&category=660204&n=38&indexArea=company_en&viewType=L&keyword=cosmetics', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.9.1f046194GWPoTx&f1=y&category=100000992&n=38&indexArea=company_en&viewType=L&keyword=cosmetics', 'https://www.alibaba.com/trade/search?spm=a2700.supplier-normal.48.10.1f046194GWPoTx&f1=y&category=100000993&n=38&indexArea=company_en&viewType=L&keyword=cosmetics']
            
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
            
            data['category'] = "Cosmetics"
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
