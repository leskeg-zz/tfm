# -*- coding: utf-8 -*-
import nltk
import re
from ipdb import set_trace
# Load nltk's SnowballStemmer
stemmer = nltk.stem.snowball.SnowballStemmer("spanish")
# tagger = nltk.tag.DefaultTagger("spanish")
# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed
def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize( ' '.join(re.findall(r'[\w]+', text, re.UNICODE)) ,language='spanish') for word in nltk.word_tokenize(sent,language='spanish')]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.match('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize( ' '.join(re.findall(r'[\w]+', text, re.UNICODE)) ,language='spanish') for word in nltk.word_tokenize(sent,language='spanish')]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.match('[a-zA-Z]', token):
            filtered_tokens.append(token.lower())
    return filtered_tokens

#strip any proper nouns (NNP) or plural proper nouns (NNPS) from a text
# def strip_proppers_POS(text):
#     tagged = nltk.tag.pos_tag(text.split()) #use NLTK's part of speech tagger
#     non_propernouns = [word for word,pos in tagged if pos != 'NNP' and pos != 'NNPS']
#     return non_propernouns

# def wordFrequency(tokens, stopwords):
#     dictFreq = {}
#     for token in tokens:
#         if not token in stopwords:
#             dictFreq[token] = tokens.count(token)

#     ans = sorted(dictFreq, key=dictFreq.__getitem__, reverse=True)
#     ipdb.set_trace()
#     return