import re
import numpy

def price_average(value_list):
	# acc = 0.0
	# div = 0
	# for value in value_list:
	# 	try:
	# 		acc += value
	# 		div += 1
	# 	except:
	# 		if value isinstance(s, basestring) and acc:
	# 			try:
	# 				value = re.findall('\d+', value)[0]
	# 				div += 1
	# 			except:
	# 				pass

	# return acc/div
	return numpy.mean[value_list]