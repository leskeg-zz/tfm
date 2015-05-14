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

		while True:
			try:
				self.driver.find_element_by_xpath('//*[@id="show_more_deals"]').click()
			except:
				break

		link_list = self.driver.find_element_by_id('flash_deals').find_elements_by_tag_name('a')

		for link in link_list[2:]:
			url = link.get_attribute('href')
			res = self.driver.get(url)
			import ipdb;ipdb.set_trace()

		# self.driver.find_element_by_id('deal_tiles').find_elements_by_tag_name('a')[1].get_attribute('href')
		pass
