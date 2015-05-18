# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from groupon_parser.items import GrouponParserItem
from datetime import datetime
from dateutil import tz

class GrouponSpider(scrapy.Spider):
	name = "groupon"
	allowed_domains = ["groupon.es"]
	start_urls = (
		'http://www.groupon.es/getaways',
	)

	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self, response):
		browser = self.driver
		browser.get(response.url)
		browser.find_element_by_id("already-registered-link").click()
		browser.find_element_by_xpath('//*[@id="search_getaways_widget"]/ul/li[1]/div[2]/a').click()

		while True:
			try:
				browser.find_element_by_xpath('//*[@id="show_more_deals"]').click()
			except:
				break

		ads_list = []
		ads = browser.find_element_by_id('flash_deals').find_elements_by_tag_name('a')
		total_ads = len(ads[2:-1])
		ads_counter = 1

		url = ads[2].get_attribute('href')
		place = ads[2].parent.find_element_by_class_name('deal-location').text
		ads_list.append({'url': url, 'place': place})
		
		print str(ads_counter) + '/' + str(total_ads) + '\t' + place + '\t' + url

		for element in ads[3:]:
			url = element.get_attribute('href')

			try:
				place = element.find_element_by_class_name('deal-location').text
			except:
				place = ''

			if '/deals/' in url and '/ga-' in url:
				ads_list.append({'url': url, 'place': place})
				ads_counter+=1
				print str(ads_counter) + '/' + str(total_ads) + '\t' + place + '\t' + url

		for ad in ads_list:
			browser.set_page_load_timeout(5)
			try:
				browser.get(ad['url'])
			except:
				pass
			
			item = GrouponParserItem()
			item['url'] = ad['url']
			item['timestamp'] = datetime.now(tz.tzlocal()).strftime("%y-%m-%d %H:%M:%S:%f%z")

			try:
				item['title'] = browser.find_element_by_xpath('//*[@id="global-container"]/div[4]/section[2]/div/div/section/div/hgroup/h1').text
			except:
				item['title'] = ''

			try:
				item['price'] = browser.find_element_by_xpath('//*[@id="deal-hero-price"]').text
			except:
				item['price'] = ''

			try:
				item['discount'] = browser.find_element_by_xpath('//*[@id="purchase-cluster"]/div[3]/table/tbody/tr[2]/td[2]').text
			except:
				item['discount'] = ''

			try:
				item['description'] = browser.find_element_by_xpath('//*[@id="tabs-1"]/div/article[1]/div').text
			except:
				item['description'] = ''

			try:
				item['options'] = browser.find_element_by_xpath('//*[@id="tabs-1"]/div/article[2]/div[2]').text
			except:
				item['options'] = ''

			try:
				item['address'] = browser.find_element_by_xpath('//*[@id="redemption-locations"]/li/div[2]/p[2]').text
			except:
				item['address'] = ''

			try:
				item['stars'] = int( item['description'][ item['description'].index('*')-1 ] )
			except:
				item['stars'] = ''

			yield item

		browser.close()