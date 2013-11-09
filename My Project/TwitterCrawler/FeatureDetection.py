'''
Created on 28 Oct 2013

@author: miljan
'''
import csv, pprint  # @UnusedImport
from FeatureExtraction import createBigrams, createUnigrams
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
                
    # get bigrams from the given tweet
    l_bigrams = createBigrams(sentence)
    # initialise an empty list to mark found features
    l_matches = [0] * 52
    # check for found bigrams in the top bigrams list
    for bigram in l_bigrams:
        l_temp = list(bigram)
        if l_temp in l_topBigrams:
            l_matches[l_topBigrams.index(l_temp)] = 1
            
    # LOOK FOR UNIGRAMS
    unigrams = createUnigrams(sentence)
#     ######Sell Unigram Variations######
#     sellVariations = ['sell','short','bear','bearish','sold']
#     sellUnigram = 0
#     #####Buy unigram variations#######
#     buyVariations = ['buy','long','bull','bullish','bought']
#     buyUnigram = 0    
#     ####INSTITUTION LIST####
#     institutionList = ['ubs', 'morgan', 'goldman','sachs','commerzbank']
#     containsInstitution = 0
    #####UPTREND#####
    uptrendVariations = ['uptrend','upside','upward']
    isUptrend = 0
    #####DOWNTREND#####
    downtrendVariations = ['downtrend','downside','downward']
    isDowntrend = 0
#     isClosed = 0
#     hasOccurences = 0
#     count = 0
#     for i in sentence:
#         if i == '$':
# #             count += 1
# #             if count >= 2:
#             hasOccurences = 1
    
    for i in unigrams:
        if i in uptrendVariations:
            isUptrend = 1
        if i in downtrendVariations:
            isDowntrend = 1
#         if i == 'closed':
#             isClosed = 1
#         if i in sellVariations:
#             sellUnigram = 1
#         if i in buyVariations:
#             buyUnigram = 1
#         if i in institutionList:
#             containsInstitution = 1

#     l_matches[45] = sellUnigram
#     l_matches[46] = buyUnigram
#     l_matches[47] = isClosed
#     l_matches[47] = containsInstitution
    l_matches[50] = isUptrend
    l_matches[51] = isDowntrend
#     l_matches[51] = hasOccurences 
    
    return l_matches

 
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
    resultFile = open("NewData/" + pairname + "/" + pairname + "TrainingFeatures4.csv",'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(l_tweets)
    

if __name__ == '__main__':    
    #read the currency pairs from textfile
    pairsFile = open("Pairs.txt","r");
    pairs = pairsFile.readlines()
    pairsFile.close()
    pairs = [pair.replace('/','').strip() for pair in pairs[1:]]
#     for pair in pairs:
    analyzeTrainingSet('EURUSD')
#     print detectFeatures('closed sell $eurusd 0.1 lots at 1.5655', 'EURUSD')






