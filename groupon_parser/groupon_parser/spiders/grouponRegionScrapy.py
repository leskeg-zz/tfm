# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from groupon_parser.items import GrouponRegionParserItem
from datetime import datetime
from dateutil import tz
import ipdb
import re

class GrouponSpider(scrapy.Spider):
	name = "grouponRegionScrapy"
	allowed_domains = ["groupon.es"]
	start_urls = (
		'http://www.groupon.es/getaways',
	)

	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self, response):
		browser = self.driver
		browser.get(response.url)
		
		try:
			browser.find_element_by_id("already-registered-link").click()
		except:
			browser.find_element_by_xpath('//*[@id="continue"]').click()

		browser.find_element_by_xpath('//*[@id="search_getaways_widget"]/ul/li[1]/div[2]/a').click()

		region_list = browser.find_element_by_id('destination_filters').find_elements_by_tag_name('a')

		for region in region_list[1:]:
			region.click()

			while True:
				try:
					browser.find_element_by_xpath('//*[@id="show_more_deals"]').click()
				except:
					break

			item = GrouponRegionParserItem()
			item['region'] = region.text
			item['url_list'] = [element.find_element_by_tag_name('a').get_attribute('href') \
				for element in browser.find_elements_by_tag_name("figure")]

			yield item