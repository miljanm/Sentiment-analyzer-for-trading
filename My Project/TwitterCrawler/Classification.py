'''
Created on 8 Nov 2013

@author: miljan
'''

from FeatureDetection import detectFeatures
from NaiveBayes import classifyTweet
import pprint, csv


"""
Function which takes a given pairname, accesses the appropriate files
and marks all the important features present in the given tweets.
It produces an output csv file with feature vector added at the end
of each tweet.
"""
def analyzeTweets(pairname):
    # list of tweets in the set
    l_tweets = []
    # Read all the data from the designated file
    path1 = "NewData/" + pairname + "/" + pairname + "test1.csv"
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            l_tweets.append(row)
    
    # get feature vectors for all the tweets
    for tweet in l_tweets:
        l_features = detectFeatures(tweet[2], pairname)
        tweet.append(l_features)
#     pprint.pprint(l_tweets)
    # write the result to a csv file
    resultFile = open("NewData/" + pairname + "/" + pairname + "output1.csv",'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(l_tweets)


def classify(pairname):
    featureVectors = []
    path1 = "NewData/" + pairname + "/" + pairname + "output1.csv"
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            featureVectors.append(row[4])
    
    classifications = []
    for i in featureVectors:
        classifications.append(classifyTweet(i, pairname))
    pprint.pprint(classifications)
            

if __name__ == '__main__':
#     analyzeTweets('EURUSD')
    classify('EURUSD')
    
    
    
    
    
    
    
    
    
    
    
    
    