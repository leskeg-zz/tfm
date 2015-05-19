# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from groupon_parser.items import GrouponParserItem
from datetime import datetime
from dateutil import tz
import ipdb

class GrouponSpider(scrapy.Spider):
	name = "grouponScrapy"
	allowed_domains = ["groupon.es"]
	start_urls = (
		# 'http://www.groupon.es/getaways',
		'http://www.groupon.es/travel/almeria/hotels',
	)

	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self, response):
		browser = self.driver
		browser.get(response.url)
		try:
			browser.find_element_by_id("already-registered-link").click()
			browser.find_element_by_xpath('//*[@id="search_getaways_widget"]/ul/li[1]/div[2]/a').click()
		except:
			pass

		while True:
			try:
				browser.find_element_by_xpath('//*[@id="show_more_deals"]').click()
			except:
				break

		# url_list = browser.find_element_by_id('flash_deals').find_elements_by_tag_name('a')[2:]
		ad_list = browser.find_elements_by_class_name("deal-card")
		# url_list = [url.find_element_by_tag_name('a').get_attribute('href') for url in ad_list]
		# try:
		# 	banner = browser.find_element_by_xpath('//*[@id="gallery_banner"]/a')
		# 	ad_list.remove( banner )
		# except:
		# 	pass

		for index,element in enumerate(ad_list):
			url = element.find_element_by_tag_name('a').get_attribute('href')
			# ipdb.set_trace()
			try:
				location = browser.find_element_by_xpath('//*[@id="flash_deals"]/div/div[2]/div[1]/figure['+ str(index+1) +']/figcaption/p').text
			except:
				try:
					location = element.find_element_by_class_name('deal-location').text
				except:
					location = ''

			yield scrapy.http.Request(url = url, meta = {'location': location}, callback=self.parse_ad)

		browser.close()
		


	def parse_ad(self, response):
		item = GrouponParserItem()
		item['url'] = response.url
		item['timestamp'] = datetime.now(tz.tzlocal()).strftime("%y-%m-%d %H:%M:%S:%f%z")
		item['location'] = response.meta['location']
		ipdb.set_trace()

		try:
			item['title'] = ''.join(response.xpath('//*[@id="global-container"]/div[4]/section[2]/div/div/section/div/hgroup/h1/text()').extract()).strip().replace('\n','')
		except:
			item['title'] = ''

		try:
			item['price'] = ''.join(response.xpath('//*[@id="deal-hero-price"]/span[2]/text()').extract()).strip().replace('\n','')
		except:
			item['price'] = ''

		try:
			item['discount'] = ''.join(response.xpath('//*[@id="purchase-cluster"]/div[3]/table/tbody/tr[2]/td[2]/text()').extract()).strip().replace('\n','')
		except:
			item['discount'] = ''

		try:
			item['description'] = ''.join(response.xpath('//*[@id="tabs-1"]/div/article[1]/div//text()').extract()).strip().replace('\n','')
		except:
			item['description'] = ''

		try:
			item['options'] = ''.join(response.xpath('//*[@id="tabs-1"]/div/article[2]/div[2]//text()').extract()).strip().replace('\n','')
		except:
			item['options'] = ''

		try:
			item['address'] = ''.join(response.xpath('//*[@id="redemption-locations"]/li/div[2]/p[2]/text()').extract()).strip().replace('\n','')
		except:
			item['address'] = ''

		try:
			item['place'] = ''.join(response.xpath('//*[@id="redemption-locations"]/li/div[2]/p[1]/strong/text()').extract()).strip().replace('\n','')
		except:
			item['place'] = ''

		try:
			item['stars'] = int( item['description'][ item['description'].index('*')-1 ] )
		except:
			item['stars'] = ''

		yield item