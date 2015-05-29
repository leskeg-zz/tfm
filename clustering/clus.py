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

import mpld3
import os  # for os.path.basename
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS

class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}
















# Making a Connection with MongoClient
client = MongoClient()
# Getting a Database
db = client.tfm
# Getting a Collection
collection_result = db.result
collection_region = db.region


regions = {}

for region in collection_region.find():
  descriptions = []
  for url in region['url_list']:
    ad = collection_result.find_one({ 'url': url })
    if ad:
      descriptions.append(ad['description'])
  regions[ region['region'] ] = descriptions

ipdb.set_trace()


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
'''
stars_grouped2 = frame['description'].groupby(frame['stars'])
# ipdb.set_trace()
# stars_grouped2.get_group(4).values

#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

#set up cluster names using a dict
cluster_names = {}

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

    cluster_names[i] = ', '.join([terms[ind] for ind in order_centroids[i, :5]])

print()
print()

# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]
print()
print()



#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles)) 

#group by cluster
groups = df.groupby('label')

#define custom css to format the font and to remove the axis labeling
css = """
text.mpld3-text, div.mpld3-tooltip {
  font-family:Arial, Helvetica, sans-serif;
}

g.mpld3-xaxis, g.mpld3-yaxis {
display: none; }

svg.mpld3-figure {
margin-left: -100px;}
"""

# Plot 
fig, ax = plt.subplots(figsize=(18,10)) #set plot size
ax.margins(0.2) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, 
                     label=cluster_names[name], mec='none', 
                     color=cluster_colors[name])
    ax.set_aspect('auto')
    labels = [i for i in group.title]
    
    #set tooltip using points, labels and the already defined 'css'
    tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
                                       voffset=10, hoffset=10, css=css)
    #connect tooltip to fig
    mpld3.plugins.connect(fig, tooltip, TopToolbar())    
    
    #set tick marks as blank
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])
    
    #set axis as blank
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    
ax.legend(numpoints=1) #show legend with only one dot

# mpld3.show() #show the plot

#uncomment the below to export to html
#html = mpld3.fig_to_html(fig)
#print(html)










ipdb.set_trace()