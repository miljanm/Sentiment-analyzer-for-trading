'''
Created on 28 Oct 2013

@author: miljan
'''
import csv, pprint  # @UnusedImport
from FeatureExtraction import createBigrams
import itertools

"""
Function which takes a tweet concerning a certain fx pair and 
detects what top features does it contain.
"""
def detectFeatures(sentence, pairname):

    l_topBigrams = []
    path1 = "NewData/" + pairname + "/" + pairname + "Bigrams50.csv"
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            l_topBigrams.append([row[0],row[1]])
            
#     pprint.pprint(l_topBigrams)
    
    # get bigrams from the given tweet
    l_bigrams = createBigrams(sentence)
    # initialise an empty list to mark found features
    l_matches = [0] * 50
    # check for found bigrams in the top bigrams list
    for bigram in l_bigrams:
        l_temp = list(bigram)
        if l_temp in l_topBigrams:
            l_matches[l_topBigrams.index(l_temp)] = 1
#     pprint.pprint(l_bigrams)
#     pprint.pprint(l_matches)
    
    return l_matches

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
    pprint.pprint(l_tweets)
    # write the result to a csv file
    resultFile = open("NewData/" + pairname + "/" + pairname + "output1.csv",'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(l_tweets)
 
"""
Function used to analyze a training set for the given pairname,
and create a feature vector for each of the tweets in the training set.
"""   
def analyzeTrainingSet(pairname):
    # list of tweets in the set
    l_tweets = []
    # list of class labels for all tweets in the set
    l_classes = []
    # Read all the data from the training set
    path1 = "NewData/" + pairname + "/" + pairname + "TrainingSet.csv"
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            l_tweets.append(row[:4])
            l_classes.append(row[4])
    
    # get feature vectors for all the tweets and append label at the end
    for tweet,label in itertools.izip(l_tweets,l_classes):
        l_features = detectFeatures(tweet[2], pairname)
        tweet.append(l_features)
        tweet.append(label)
    #write results to a csv file
    resultFile = open("NewData/" + pairname + "/" + pairname + "TrainingFeatures.csv",'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(l_tweets)
    

    
analyzeTrainingSet('EURUSD') 








