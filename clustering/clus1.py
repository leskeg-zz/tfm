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
titles = list( collection.find( {}, { 'title':1, '_id':0 } ))
descriptions = collection.distinct("description")

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

ads = { 'title': titles, 'description': descriptions, 'cluster': clusters }
frame = pd.DataFrame(ads, index = [clusters] , columns = [ 'title', 'description', 'cluster'])
frame['cluster'].value_counts() #number of films per cluster (clusters from 0 to 4)
# grouped = frame['rank'].groupby(frame['cluster']) #groupby cluster for aggregation purposes
# grouped.mean() #average rank (1 to 100) per cluster


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
        print(' %s.' % title['title'], end='\n\r')
    print() #add whitespace
    print() #add whitespace
    
print()
print()

ipdb.set_trace()