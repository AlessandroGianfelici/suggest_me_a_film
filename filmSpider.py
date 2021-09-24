
  
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
import io
from bs4 import BeautifulSoup
from datetime import datetime

class MySpider(CrawlSpider):
    
    name = 'mymovies'
    allowed_domains = ['mymovies.it']
    start_urls = [r'https://www.mymovies.it']
    rules = (# Extract and follow all links!

        Rule(LinkExtractor(), callback='parse_item', follow=True), )
    def parse_item(self, response):
        
        if "mymovies.it/film" in response.url:
            soup = BeautifulSoup(response.body, 'html.parser')
            all_paragraph = soup.get_text()
            txt_name = os.path.join("film", response.url.split("/")[-1] + '.txt')
            s = io.StringIO(all_paragraph)
            with open(txt_name, 'w') as f:
                for line in s:
                    f.write(line)

        self.log('crawling'.format(response.url))