# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver

class GrouponSpider(scrapy.Spider):
    name = "groupon"
    allowed_domains = ["groupon.es"]
    start_urls = (
        'http://www.groupon.es/getaways',
    )

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
    	res = self.driver.get(response.url)
    	self.driver.find_element_by_id("already-registered-link").click()
    	self.driver.find_element_by_xpath('//*[@id="search_getaways_widget"]/ul/li[1]/div[2]/a').click()
    	self.driver.find_element_by_xpath('//*[@id="show_more_deals"]').click()
    	import ipdb; ipdb.set_trace()
        pass
