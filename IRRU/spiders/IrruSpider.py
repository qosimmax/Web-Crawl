# -*- coding: utf-8 -*-
# Spider class
# start spider in command line with: scrapy crawl IRR.RU

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
import re
from IRRU.items import IrruItem


class IrruSpider(CrawlSpider):
    name = "IRR.RU"
    allowed_domains = ["irr.ru"]
    start_urls = [
        "http://irr.ru/real-estate/commercial/search/currency=RUR/sourcefrom=0/date_create=yesterday/page_len60/",
        "http://irr.ru/real-estate/commercial/search/currency=RUR/sourcefrom=1/date_create=yesterday/page_len60/",
        "http://irr.ru/real-estate/commercial-sale/search/currency=RUR/sourcefrom=0/date_create=yesterday/page_len60/",
        "http://irr.ru/real-estate/commercial-sale/search/currency=RUR/sourcefrom=1/date_create=yesterday/page_len60/",
    ]

    def parse_start_url(self, response):
        return self.parse_links(response)

    def parse_links(self, response):
        # parse links
        for link in LinkExtractor(allow=('/real-estate/.+/.+advert\\d+\\.html$',)).extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_items)
        # go to next page if exists
        for link in LinkExtractor(allow=("/page\\d/$",)).extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_links)

    # parse titles
    def parse_items(self, response):
        m = re.search("advertId\\s+=\\s+(\\d+);", response.body)
        for h1 in response.xpath('//h1[@class="productName"]/text()').extract():
            item = IrruItem()
            item['title'] = h1
            if m:
                item['id'] = m.group(0)
            yield item

