# -*- coding: utf-8 -*-
from pymongo import MongoClient
import ipdb
import nltk
import tokenizers
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import codecs

# Making a Connection with MongoClient
client = MongoClient()
# Getting a Database
db = client.tfm
# Getting a Collection
collection = db.result

# Getting interesting data
titles = collection.find().distinct("title")
descriptions = collection.find().distinct("description")

# Load nltk's Spanish stopwords
stopwords1 = nltk.corpus.stopwords.words('spanish')
# Reading stopwords from file
stopwords2 = codecs.open('stopwords.txt', encoding='utf-8').read().splitlines()
# Merging stopwords excluding duplicates
stopwords = list(set(stopwords1) | set(stopwords2))

#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in descriptions:
	allwords_stemmed = tokenizers.tokenize_and_stem(i) #for each item in 'descriptions', tokenize/stem
	totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list

	allwords_tokenized = tokenizers.tokenize_only(i)
	totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words=stopwords,
                                 use_idf=True, tokenizer=tokenizers.tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions) #fit the vectorizer to descriptions
ipdb.set_trace()
# print(tfidf_matrix.shape)
