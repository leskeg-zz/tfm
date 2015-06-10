# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ipdb import set_trace
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.manifold import MDS

from tokenizers import tokenize_only
from stopwords import stopwords
from mongo import result, regions
from toptoolbar import TopToolbar, plot



'''
********************************************************************
Clustering
********************************************************************
'''

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, tokenizer=tokenize_only, min_df=0.1)
#fit the vectorizer to descriptions
tfidf_matrix = tfidf_vectorizer.fit_transform(result['description'])
# print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()

num_clusters = 4
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

result['cluster'] = clusters
frame = pd.DataFrame(result, index = [clusters] , columns = [ 'title', 'description', 'price', 'discount', 'stars', 'cluster'])

#number of ads per cluster (clusters from 0 to 4)
print frame['cluster'].value_counts()

#set up cluster names using a dict
cluster_names = {}

#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

print "Top terms per cluster:\n\r"
for i in range(num_clusters):
    cluster_names[i] = ', '.join([terms[ind] for ind in order_centroids[i, :8]])
    print "\n\rCluster " + str(i) + " words: " + cluster_names[i]

    print "Cluster " + str(i) + " titles:"
    for title in frame.ix[i]['title'].values.tolist():
        print title


'''
********************************************************************
Aggregation
********************************************************************
'''

price_grouped = frame['price'].groupby(frame['cluster']) #groupby cluster for aggregation purposes
print '\nAverage price per cluster:'
print(price_grouped.mean()) 

discount_grouped = frame['discount'].groupby(frame['cluster'])
print '\nAverage discount per cluster:'
print(discount_grouped.mean())

price_stars_grouped = frame['price'].groupby(frame['stars'])
print '\nNumber of advertisements per stars:'
print(price_stars_grouped.count())
print '\nAverage price per stars:'
print(price_stars_grouped.mean())
print '\nMinimum price per stars:'
print(price_stars_grouped.min())
print '\nMaximum price per stars:'
print(price_stars_grouped.max())

discount_stars_grouped = frame['discount'].groupby(frame['stars'])
print '\nAverage discount per stars:'
print(discount_stars_grouped.mean())
print '\nMinimum discount per stars:'
print(discount_stars_grouped.min())
print '\nMaximum discount per stars:'
print(discount_stars_grouped.max())

vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, tokenizer=tokenize_only, min_df=0.3)
# vectorizer = CountVectorizer(stop_words=stopwords, tokenizer=tokenize_only, min_df=0.4)
description_stars_grouped = frame['description'].groupby(frame['stars'])
print '\nTop terms per stars:'
for i in range(1,6):
  matrix = vectorizer.fit_transform(description_stars_grouped.get_group(i).values)
  frequency_top_terms = zip(vectorizer.get_feature_names(), np.asarray(matrix.sum(axis=0)).ravel())
  elements = sorted(frequency_top_terms, key=lambda frequency_top_terms: frequency_top_terms[1], reverse=True)[:8]
  print str(i) + ' stars: ' + '%s' % ', '.join([element[0] for element in elements])

print '\nTop terms per regions:'
for region_name in regions:
  if len(regions[ region_name ]):
    matrix = vectorizer.fit_transform(regions[ region_name ])
    frequency_top_terms = zip(vectorizer.get_feature_names(), np.asarray(matrix.sum(axis=0)).ravel())
    elements = sorted(frequency_top_terms, key=lambda frequency_top_terms: frequency_top_terms[1], reverse=True)[:8]
    print region_name + ': ' + '%s' % ', '.join([element[0] for element in elements])

'''
********************************************************************
Graphical Representation
********************************************************************
'''

#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
dist = 1 - cosine_similarity(tfidf_matrix)
pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
xs, ys = pos[:, 0], pos[:, 1]

#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=result['title'])) 

#group by cluster
groups = df.groupby('label')

# Plot 
fig, ax = plt.subplots(figsize=(16,9)) #set plot size
ax.margins(0.2) # Optional, just adds 2% padding to the autoscaling
plot(groups,fig,ax,cluster_names,cluster_colors)