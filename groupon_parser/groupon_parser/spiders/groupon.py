# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from groupon_parser.items import GrouponParserItem
# from datetime import datetime
# from dateutil import tz

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

		while True:
			try:
				self.driver.find_element_by_xpath('//*[@id="show_more_deals"]').click()
			except:
				break

		url_list = [element.get_attribute('href') for element in\
					self.driver.find_element_by_id('flash_deals').find_elements_by_tag_name('a')[2:]]

		for url in url_list:
			response = self.driver.get(url)
			import ipdb;ipdb.set_trace()
			self.parse_item(response)

		# self.driver.find_element_by_id('deal_tiles').find_elements_by_tag_name('a')[1].get_attribute('href')
		pass

	def parse_item(self, response):
		import ipdb;ipdb.set_trace()
		item = OfertaItem()
		item['url'] = response.url
		item['title'] = ''.join(response.xpath('//*[@id="global-container"]/div[4]/section[2]/div/div/section/div/hgroup/h1/text()').extract()).strip()
		# item['timestamp'] = datetime.now(tz.tzlocal()).strftime("%y-%m-%d %H:%M:%S:%f%z")
		# item['precio'] = ''.join(response.xpath('//*[@id="deal-hero-price"]//text()').extract()).strip()
		# item['texto'] = ''.join(response.xpath('//*[@id="tabs-1"]/div/article[1]/text()').extract()).strip()
		# item['opciones'] = ''.join(response.xpath('//*[@id="tabs-1"]/div/article[2]/div/ul[1]//text()').extract()).strip()
		yield item