# -*- coding: utf-8 -*-
from ipdb import set_trace
from pymongo import MongoClient

# Making a Connection with MongoClient
client = MongoClient()
# Getting a Database
db = client.tfm
# Getting a Collection
collection_result = db.result
collection_region = db.region

# Getting interesting data
titles = []
descriptions = []
prices = []
discounts = []
stars = []
for element in collection_result.find():
	titles.append(element['title'])
	descriptions.append(element['description'])
	prices.append(element['price'])
	discounts.append(element['discount'])
	stars.append(element['stars'])

result = 	{ 	
			'title': titles,
			'description': descriptions, 
			'price': prices,
			'discount': discounts,
			'stars': stars 
			}

regions = {}

for region in collection_region.find():
  descriptions = []
  for url in region['url_list']:
    ad = collection_result.find_one({ 'url': url })
    if ad:
      descriptions.append(ad['description'])
  regions[ region['region'] ] = descriptions
