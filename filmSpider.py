
  
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
import io
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

path = os.path.dirname(__file__)
def select_or_create(path):
    try:
        os.stat(path)
    except FileNotFoundError:
        os.mkdir(path)
    return path

savepath = select_or_create(os.path.join(os.path.dirname(__file__), "film"))
film_data = pd.DataFrame()


class MySpider(CrawlSpider):
    
    name = 'mymovies'
    allowed_domains = ['mymovies.it']
    start_urls = [r'https://www.mymovies.it']
    rules = (# Extract and follow all links!

        Rule(LinkExtractor(), callback='parse_item', follow=True), )
    def parse_item(self, response):
        
        if "mymovies.it/film" in response.url:
            soup = BeautifulSoup(response.body, 'html.parser')
            
            all_paragraph = soup.find_all('p')
            mystring = ' '.join([par.get_text() for par in all_paragraph])
            text = " ".join(mystring.split())
            title = str(soup.find_all('title')[0]).replace(r'<title>', "").replace(" - MYmovies.it</title>", "")
            if 'Film' in title:
                film_data['title'] = [title]
                film_data['text'] = [text]
                film_data['url'] = [response.url]
                film_data.to_csv(os.path.join(savepath, title + '.csv'), index=0)

        self.log('crawling'.format(response.url))
