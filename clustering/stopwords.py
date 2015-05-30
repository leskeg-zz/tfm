# -*- coding: utf-8 -*-
import nltk
import codecs
# Load nltk's Spanish stopwords
stopwords1 = nltk.corpus.stopwords.words('spanish')
# Reading stopwords from file
stopwords2 = codecs.open('stopwords.txt', encoding='utf-8').read().splitlines()
# Merging stopwords excluding duplicates
stopwords = list(set(stopwords1) | set(stopwords2))