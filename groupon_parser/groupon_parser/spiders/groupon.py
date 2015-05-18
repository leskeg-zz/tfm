# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from groupon_parser.items import GrouponParserItem
from datetime import datetime
from dateutil import tz
from time import sleep

class GrouponSpider(scrapy.Spider):
	name = "groupon"
	allowed_domains = ["groupon.es"]
	start_urls = (
		'http://www.groupon.es/getaways',
	)

	def __init__(self):
		self.driver = webdriver.Firefox()
		# self.driver.set_page_load_timeout(5)

	def parse(self, response):
		self.driver.get(response.url)
		self.driver.find_element_by_id("already-registered-link").click()
		self.driver.find_element_by_xpath('//*[@id="search_getaways_widget"]/ul/li[1]/div[2]/a').click()

		while True:
			try:
				self.driver.find_element_by_xpath('//*[@id="show_more_deals"]').click()
			except:
				break

		url_list = [element.get_attribute('href') for element in\
					self.driver.find_element_by_id('flash_deals').find_elements_by_tag_name('a')[2:]]
		# import ipdb; ipdb.set_trace()

		for url in url_list:
			try:
				self.driver.get(url)
			except:
				pass

			item = GrouponParserItem()
			item['url'] = url
			item['title'] = self.driver.find_element_by_xpath('//*[@id="global-container"]/div[4]/section[2]/div/div/section/div/hgroup/h1').text
			item['timestamp'] = datetime.now(tz.tzlocal()).strftime("%y-%m-%d %H:%M:%S:%f%z")
			item['price'] = self.driver.find_element_by_xpath('//*[@id="deal-hero-price"]').text
			item['discount'] = self.driver.find_element_by_xpath('//*[@id="purchase-cluster"]/div[3]/table/tbody/tr[2]/td[2]').text
			item['description'] = self.driver.find_element_by_xpath('//*[@id="tabs-1"]/div/article[1]/div').text
			item['options'] = self.driver.find_element_by_xpath('//*[@id="tabs-1"]/div/article[2]/div[2]').text
			item['place'] = self.driver.find_element_by_xpath('//*[@id="redemption-locations"]/li/div[2]/p[2]').text
			# item['stars'] = datetime.now(tz.tzlocal()).strftime("%y-%m-%d %H:%M:%S:%f%z")
			# item['precio'] = ''.join(response.xpath('//*[@id="deal-hero-price"]//text()').extract()).strip()
			# item['texto'] = ''.join(response.xpath('//*[@id="tabs-1"]/div/article[1]/text()').extract()).strip()
			# item['opciones'] = ''.join(response.xpath('//*[@id="tabs-1"]/div/article[2]/div/ul[1]//text()').extract()).strip()
			yield item

			# self.driver.find_element_by_id('deal_tiles').find_elements_by_tag_name('a')[1].get_attribute('href')
