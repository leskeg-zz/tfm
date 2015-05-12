# -*- coding: utf-8 -*-
import scrapy


class GrouponSpider(scrapy.Spider):
    name = "groupon"
    allowed_domains = ["groupon.es"]
    start_urls = (
        'http://www.groupon.es/',
    )

    def parse(self, response):
        pass
