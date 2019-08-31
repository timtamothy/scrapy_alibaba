# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
# import the class Spider2Item from the items file in scrapy_alibaba directory
from scrapy_alibaba.items import Spider2Item

class Alibaba_s1(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['alibaba.com']
    
    def start_requests(self):
        #define all alphabetical urls
        alpha_urls = ['https://www.alibaba.com/suppliers/supplier-A.html',
                      'https://www.alibaba.com/suppliers/supplier-B.html',
                      'https://www.alibaba.com/suppliers/supplier-C.html',
                      'https://www.alibaba.com/suppliers/supplier-D.html',
                      'https://www.alibaba.com/suppliers/supplier-E.html',
                      'https://www.alibaba.com/suppliers/supplier-F.html',
                      'https://www.alibaba.com/suppliers/supplier-G.html',
                      'https://www.alibaba.com/suppliers/supplier-H.html',
                      'https://www.alibaba.com/suppliers/supplier-I.html',
                      'https://www.alibaba.com/suppliers/supplier-J.html',
                      'https://www.alibaba.com/suppliers/supplier-K.html',
                      'https://www.alibaba.com/suppliers/supplier-L.html',
                      'https://www.alibaba.com/suppliers/supplier-M.html',
                      'https://www.alibaba.com/suppliers/supplier-N.html',
                      'https://www.alibaba.com/suppliers/supplier-O.html',
                      'https://www.alibaba.com/suppliers/supplier-P.html',
                      'https://www.alibaba.com/suppliers/supplier-Q.html',
                      'https://www.alibaba.com/suppliers/supplier-R.html',
                      'https://www.alibaba.com/suppliers/supplier-S.html',
                      'https://www.alibaba.com/suppliers/supplier-T.html',
                      'https://www.alibaba.com/suppliers/supplier-U.html',
                      'https://www.alibaba.com/suppliers/supplier-V.html',
                      'https://www.alibaba.com/suppliers/supplier-W.html',
                      'https://www.alibaba.com/suppliers/supplier-X.html',
                      'https://www.alibaba.com/suppliers/supplier-Y.html',
                      'https://www.alibaba.com/suppliers/supplier-Z.html',
                      'https://www.alibaba.com/suppliers/supplier-0-9.html'
                     ]
        for url in alpha_urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        #empty list to iterate through in for loop
        alpha_supplier_urls = []
        alpha_supplier_urls.append(response.request.url)
        #scraped URL stems from the website (they dont include www.alibaba.com)
        alpha_s_path_url = response.xpath("//span[@id='PagesBoxPageAll']/a/@href").extract()
        #adding the https://www.alibaba.com to all the scraped URLS
        for url in alpha_s_path_url:
            alpha_supplier_urls.append('https://www.alibaba.com'+url)
        for url in alpha_supplier_urls:
            yield scrapy.Request(url, callback=self.parse_2)
            
        
    def parse_2(self, response):
        category_urls = response.xpath("//div[@class='colRmargin']/div[contains(@class,'column one4')]/a/@href").extract()
        #category_name = response.xpath("//div[@class='colRmargin']/div[contains(@class,'column one4')]/a/text()").extract()
        result = zip(category_urls)
        for ccategory_urls in result:
            item = Spider2Item()
            #item['category_name'] = category_name
            item['category_url'] = category_urls
            yield item

   