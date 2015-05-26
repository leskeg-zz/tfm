# -*- coding: utf-8 -*-
from __future__ import print_function
from pymongo import MongoClient
import codecs
import ipdb
import nltk
import tokenizers
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib

# Making a Connection with MongoClient
client = MongoClient()
# Getting a Database
db = client.tfm
# Getting a Collection
collection = db.result

# Getting interesting data
titles = []
descriptions = []
prices = []
discounts = []
stars = []
for element in collection.find():
	titles.append(element['title'])
	descriptions.append(element['description'])
	prices.append(element['price'])
	discounts.append(element['discount'])
	stars.append(element['stars'])

# stars = list( collection.find( {}, { 'stars':1, '_id':0 } ))


# Load nltk's Spanish stopwords
stopwords1 = nltk.corpus.stopwords.words('spanish')
# Reading stopwords from file
stopwords2 = codecs.open('stopwords.txt', encoding='utf-8').read().splitlines()
# Merging stopwords excluding duplicates
stopwords = list(set(stopwords1) | set(stopwords2))

#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
# totalvocab_stemmed = []
# totalvocab_tokenized = []
# for i in descriptions:
# 	allwords_stemmed = tokenizers.tokenize_and_stem(i) #for each item in 'descriptions', tokenize/stem
# 	totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list

# 	allwords_tokenized = tokenizers.tokenize_only(i)
# 	totalvocab_tokenized.extend(allwords_tokenized)

# vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, \
	tokenizer=tokenizers.tokenize_only, analyzer='word', min_df=0.1)

tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions) #fit the vectorizer to descriptions
# print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()
dist = 1 - cosine_similarity(tfidf_matrix)

num_clusters = 5
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

#uncomment the below to save your model 
#since I've already run my model I am loading from the pickle

#joblib.dump(km,  'doc_cluster.pkl')

# km = joblib.load('doc_cluster.pkl')
# clusters = km.labels_.tolist()

ads = { 'title': titles, 'description': descriptions, 'price': prices, 'discount': discounts, 'stars': stars, 'cluster': clusters }
frame = pd.DataFrame(ads, index = [clusters] , columns = [ 'title', 'description', 'price', 'discount', 'stars', 'cluster'])
frame['cluster'].value_counts() #number of films per cluster (clusters from 0 to 4)


'''
price_grouped = frame['price'].groupby(frame['cluster']) #groupby cluster for aggregation purposes
discount_grouped = frame['discount'].groupby(frame['cluster']) #groupby cluster for aggregation purposes
stars_grouped = frame['price'].groupby(frame['stars'])
print(price_grouped.mean()) #average rank (1 to 100) per cluster
print(discount_grouped.mean()) #average rank (1 to 100) per cluster
print(stars_grouped.mean()) #average rank (1 to 100) per cluster

stars_grouped2 = frame['description'].groupby(frame['stars'])
stars_grouped2.get_group(4)
ipdb.set_trace()


# totalvocab_tokenized = []
# for description in frame.ix[0]['description'].values.tolist():
# 	allwords_tokenized = tokenizers.tokenize_only(description)
# 	totalvocab_tokenized.extend(allwords_tokenized)

# tokenizers.wordFrequency(totalvocab_tokenized,stopwords)
'''

print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='\n\r')
    
    for ind in order_centroids[i, :5]: #replace 5 with n words per cluster
        # print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
        print(' %s' % terms[ind], end='')
    print() #add whitespace
    print() #add whitespace
    
    print("Cluster %d titles:" % i, end='\n\r')
    for title in frame.ix[i]['title'].values.tolist():
        print(' %s.' % title, end='\n\r')
    print() #add whitespace
    print() #add whitespace
    
print()
print()

ipdb.set_trace()