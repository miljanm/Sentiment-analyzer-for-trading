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
# Main bigrams
import nltk, pprint, string

def createBigrams(sentence, dict_bigram):
    # create tokens from the given sentence
    tokens = nltk.word_tokenize(sentence)
    
    # Get stopwords from a text file
    stopwordsFile = open("stopwords.txt","r");
    stopwords = stopwordsFile.readlines()
    stopwordsFile.close()
    stopwords = [word.strip('\r\n') for word in stopwords]
    
    # get negation words
    negationsWords = open("negations.txt","r");
    negations = negationsWords.readlines()
    negationsWords.close()
    negations = negations[0].split()
    
#     print tokens
    # remove stopwords from the sentence
    tokens = [token for token in tokens if token not in stopwords]
#     print tokens
    # remove punctuation from tokens
    tokens = [s.translate(None, string.punctuation) for s in tokens]
#     print tokens
    # remove numerics and empty string
    tokens = [x for x in tokens if (x and not (x.isdigit() or x[0] == '-' and x[1:].isdigit()))]
#     print tokens
    
    # create bigrams from tokens
    bigrams = nltk.bigrams(tokens)
#     print bigrams
#     print '-----------------------------------------'
    for big in bigrams:
        if big == ('pips', 'pips'):
            continue
        if big in dict_bigram:
            dict_bigram[big] = dict_bigram[big] + 1
        else:
            dict_bigram[big] = 1
    return dict_bigram
    
    


 
import csv
tweets = []
path1 = "Historic/EURUSD/EURUSD.csv"
path2 = "NewData/EURUSD/EURUSDRaw.csv"
with open(path1, 'rb') as csvfile1:
    reader1 = csv.reader(csvfile1, delimiter=',')
    for row in reader1:
        tweets.append(row[2])

with open(path2, 'rb') as csvfile1:
    reader1 = csv.reader(csvfile1, delimiter=',')
    for row in reader1:
        tweets.append(row[2])

# get a dict of bigrams that stores bigrams and their frequency as values
d_bigrams = {}
for tweet in tweets:
    d_bigrams = createBigrams(tweet, d_bigrams)

# create a list from the dict
csvData = []
for (col1, col2), col3 in d_bigrams.iteritems():
    csvData.append([col1, col2, col3])
# sort the items from the dict by value
from operator import itemgetter
csvData = sorted(csvData, key=itemgetter(2))

# write all sorted pairs to a csv file
f = open('output.csv', 'w')
f.writelines(','.join(str(j) for j in i) + '\n' for i in csvData)
f.close()

pprint.pprint(csvData[-10:])

# createBigrams('closed sell 0.25 lots $eurusd 1.30739 for  40.0 pips  total for today  51.0 pips')