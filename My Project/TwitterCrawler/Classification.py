'''
Created on 8 Nov 2013

@author: miljan
'''

from FeatureDetection import detectFeatures
from NaiveBayes import classifyTweet
import pprint, csv  # @UnusedImport


"""
Function which takes a given pairname, accesses the appropriate files
and marks all the important features present in the given tweets.
It produces an output csv file with feature vector added at the end
of each tweet.
"""
def analyzeTweets(pairname,infile, outfile):
    # list of tweets in the set
    l_tweets = []
    # Read all the data from the designated file
    path1 = "NewData/" + pairname + "/" + pairname + infile
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            l_tweets.append(row)
    
    # get feature vectors for all the tweets
    for tweet in l_tweets:
        l_features = detectFeatures(tweet[2], pairname, 1)
        tweet.append(l_features)
#     pprint.pprint(l_tweets)
    # write the result to a csv file
    resultFile = open("NewData/" + pairname + "/" + pairname + outfile,'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(l_tweets)

"""
Function which takes name of the fx pair and input and output files.
It classifies all the tweets in the input file of the given pair
and write results to the specified outfile.
"""
def classify(pairname,infile, outfile):
    data = []
    path1 = "NewData/" + pairname + "/" + pairname + infile
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            data.append(row)
    
    # append classifications to tweets
    for i in data:
        classification = classifyTweet(i[4], pairname)
        i.append(classification[0])
    
    # write classifications to a specified file
    resultFile = open("NewData/" + pairname + "/" + pairname + outfile,'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(data)
            

if __name__ == '__main__':
#     analyzeTweets('EURUSD', '_NFPtest8Nov.csv', '_NFPtest8NovFeatures.csv')
    classify('EURUSD', '_NFPtest8NovFeatures.csv', '_NFPtest8NovClassified.csv')
    
    
    
    
    
    
    
    
    
    
    
    
    