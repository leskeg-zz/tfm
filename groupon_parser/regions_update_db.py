# -*- coding: utf-8 -*-
from ipdb import set_trace
import json
import sys
sys.path.insert(0, '../clustering')
from mongo import collection_region

with open(sys.argv[1],'r') as data_file:
	regions = json.load(data_file)

for region in regions:
	collection_region.find_one_and_update({'region': region['region']},{'$addToSet':{'url_list':{ '$each': region['url_list'] }}}, upsert=True)
	# found = collection_region.find_one({ 'region': region['region'] })
	# if found:
		# url_list = list(set(found['url_list']) | set(region['url_list']))
		# collection_region.update({'_id': found['_id']},{'$addToSet':{'url_list':{ '$each': region['url_list'] }}})
	# else:
		# collection_region.insert_one( region )