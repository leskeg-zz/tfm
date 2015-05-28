# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GrouponParserItem(scrapy.Item):
	# define the fields for your item here like:
	timestamp = scrapy.Field()
	url = scrapy.Field()
	title = scrapy.Field()
	price = scrapy.Field()
	discount = scrapy.Field()
	description = scrapy.Field()
	options = scrapy.Field()
	place = scrapy.Field()
	address = scrapy.Field()
	location = scrapy.Field()
	stars = scrapy.Field()

class GrouponRegionParserItem(scrapy.Item):
	url_list = scrapy.Field()
	region = scrapy.Field()