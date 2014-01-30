'''
Created on 17 Oct 2013

@author: miljan
'''

# import numpy as np  # @UnusedImport
# import matplotlib  # @UnresolvedImport @UnusedImport
# import nltk
# import pprint
# from nltk.book import *  # @UnusedWildImport
# import csv


# --------------------------------------------------------------------
# Create collocations (most frequent bigrams) by analyzing corpus of tweets for the given pair.

# currentPair = 'GBPUSD'
# tweets = []
# path="Historic/"+currentPair.upper()+"/"+currentPair.upper()+".csv"
# with open(path, 'rb') as csvfile1:
#     reader1 = csv.reader(csvfile1, delimiter=',')
#     for row in reader1:
#         tweets.append(row[2])
# print 'target: ' + str(len(tweets))
# tweets = nltk.Text(nltk.word_tokenize('. '.join(tweets))) # they have to be tokenized in order to work
# print tweets.collocations()
# print 'done'


# --------------------------------------------------------------------
# Create vocabulary and play with frequencies

# fdist1 = FreqDist(tweets)
# print fdist1
# vocabulary = fdist1.keys()
# pprint.pprint(vocabulary[:50])
# fdist1.plot(50,cumulative=True)
# v = sorted(set(text1))
# long_words = [w for w in v if len(w) > 4 and fdist1[w] > 500]
# pprint.pprint(long_words)

# --------------------------------------------------------------------
# Reuters corpus of tagged news

# from nltk.corpus import reuters
# print reuters.categories()
# print reuters.fileids('money-fx')
# print reuters.raw(['test/14849'])

# --------------------------------------------------------------------
