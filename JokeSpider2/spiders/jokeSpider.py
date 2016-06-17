# -*- coding: UTF-8 -*-
"""
Created on 2016/6/2

@author: mavericks
"""

from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import Jokespider2Item

import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class jSpider(CrawlSpider):
    name = "j"
    #redis_key = "j:start_urls"
    allowed_domains = ['haha365.com']
    start_urls = ['http://www.haha365.com/joke/index_v_1.htm']
    base_url = 'http://www.haha365.com'

    def parse(self, response):
        selector = Selector(response)
        content_links = selector.xpath('//ul[@class="text_doublelist1"]/li/a[last()]/@href').extract()
        next_link = selector.xpath('//p[@id="pages"]/a[last()]/@href').extract()[0]
        next_url = (self.base_url + next_link).strip()
        yield Request(url=next_url, callback=self.parse)
        for content_link in content_links:
            link_url = self.base_url + content_link
            yield Request(url=link_url, callback=self.parse_content)

    def parse_content(self, response):
        selector = Selector(response)
        try:
            contents = selector.xpath('//div[@id="endtext"]/p/text()').extract()
            if len(contents) == 0:
                contents = selector.xpath('//div[@id="endtext"]/text()').extract()
            c = ''
            for content in contents:
                c += content
            item = Jokespider2Item()
            item['content'] = c
            item['url'] = response.url
            yield item
        except Exception, e:
            yield "null"




