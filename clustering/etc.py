import numpy as np




regions = {}

for region in collection_region.find():
  descriptions = []
  for url in region['url_list']:
    ad = collection_result.find_one({ 'url': url })
    if ad:
      descriptions.append(ad['description'])
  regions[ region['region'] ] = descriptions

vectorizer = CountVectorizer(stop_words=stopwords, min_df=0.4, max_df=0.9)
matrix = vectorizer.fit_transform(regions['Norte'])
my_tuple = zip(vectorizer.get_feature_names(), np.asarray(matrix.sum(axis=0)).ravel())
sorted(my_tuple, key=lambda my_tuple: my_tuple[1], reverse=True)

ipdb.set_trace()

Getting interesting data
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

stars = list( collection.find( {}, { 'stars':1, '_id':0 } ))

# not super pythonic, no, not at all.
# use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in descriptions:
	allwords_stemmed = tokenizers.tokenize_and_stem(i) #for each item in 'descriptions', tokenize/stem
	totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list

	allwords_tokenized = tokenizers.tokenize_only(i)
	totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)






# uncomment the below to save your model 
# since I've already run my model I am loading from the pickle

joblib.dump(km,  'doc_cluster.pkl')

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()


found = collection_region.find_one({ 'region': region['region'] })
	if found:
		url_list = list(set(found['url_list']) | set(region['url_list']))
		collection_region.update({'_id': found['_id']},{'$addToSet':{'url_list':{ '$each': region['url_list'] }}})
	else:
		collection_region.insert_one( region )