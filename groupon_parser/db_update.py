# -*- coding: utf-8 -*-
from ipdb import set_trace
import json
import sys
sys.path.insert(0, '../clustering')
from mongo import collection_result, collection_region

with open(sys.argv[1],'r') as data_file:
	ads = json.load(data_file)

for ad in ads:
	if collection_result.find_one({ 'url': ad['url'] }):
		pass
	else:
		pass
		# collection_result.insert_one( ad )
	set_trace()
