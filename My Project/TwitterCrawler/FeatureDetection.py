'''
Created on 28 Oct 2013

@author: miljan
'''
import csv, pprint  # @UnusedImport
from FeatureExtraction import createBigrams, createUnigrams
import itertools


"""
Method which reads the top50 and top45 bigrams files for the given pair.
"""
def readFeaturesData(pairname):
    # read the top 50 bigrams for the given pair
    l_topBigrams50 = []
    path1 = "NewData/" + pairname + "/Features/" + pairname + "Bigrams50.csv"
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            l_topBigrams50.append([row[0],row[1]])
    
    # read the top45 + 7 bigrams for the given pair
    l_topBigrams45 = []
    path1 = "NewData/" + pairname + "/Features/" + pairname + "Bigrams45.csv"
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            l_topBigrams45.append([row[0],row[1]])
            
    return [l_topBigrams50, l_topBigrams45]

"""
Function which takes a tweet concerning a certain fx pair and 
detects what top features does it contain.
Classifier 1 - NAIVE BAYES #1 uses top50 bigrams + 2 up/down unigrams
Classifier 2 - NAIVE BAYES #2 uses top45 bigrams + 7 unigrams
Classifier 3 - SVM
"""
def detectFeatures(sentence, pairname, classifier, l_topBigrams):
    # NAIVE BAYES #1 uses top50 bigrams + 2 up/down unigrams
    if classifier == 1:                    
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
        #####UPTREND#####
        uptrendVariations = ['uptrend','upside','upward']
        isUptrend = 0
        #####DOWNTREND#####
        downtrendVariations = ['downtrend','downside','downward']
        isDowntrend = 0
        
        for i in unigrams:
            if i in uptrendVariations:
                isUptrend = 1
            if i in downtrendVariations:
                isDowntrend = 1

        l_matches[50] = isUptrend
        l_matches[51] = isDowntrend
        
    # NAIVE BAYES #2 and SVM uses top45 bigrams + 7 unigrams
    elif classifier == 2:          
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
        ######Sell Unigram Variations######
        sellVariations = ['sell','short','bear','bearish','sold']
        sellUnigram = 0
        #####Buy unigram variations#######
        buyVariations = ['buy','long','bull','bullish','bought']
        buyUnigram = 0    
        ####INSTITUTION LIST####
        institutionList = ['ubs', 'morgan', 'goldman','sachs','commerzbank','credit suisse','barclays','deutsche']
        containsInstitution = 0
        #####UPTREND#####
        uptrendVariations = ['uptrend','upside','upward']
        isUptrend = 0
        #####DOWNTREND#####
        downtrendVariations = ['downtrend','downside','downward']
        isDowntrend = 0
        # does it contain the term 'closed'
        isClosed = 0
        # does it have occurences of financial references
        hasOccurences = 0
        count = 0
        for i in sentence:
            if i == '$':
                count += 1
                if count >= 2:
                    hasOccurences = 1
        
        for i in unigrams:
            if i in sellVariations:
                sellUnigram = 1
            if i in buyVariations:
                buyUnigram = 1            
            if i in uptrendVariations:
                isUptrend = 1
            if i in downtrendVariations:
                isDowntrend = 1
            if i == 'closed':
                isClosed = 1
            if i in institutionList:
                containsInstitution = 1
     
        l_matches[45] = sellUnigram
        l_matches[46] = buyUnigram
        l_matches[47] = isClosed
        l_matches[47] = containsInstitution
        l_matches[50] = isUptrend
        l_matches[51] = isDowntrend
        l_matches[51] = hasOccurences        

    else:
        raise Exception("Wrong classifier number given to detectFeatures()")    
    return l_matches

 
"""
Function used to analyse a training set for the given pairname,
and create a feature vector for each of the tweets in the training set.
"""   
def __analyzeTrainingSet(pairname, classifier, outfile):
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
    
    # read in the feature data
    l_topBigrams50, l_topBigrams45 = readFeaturesData(pairname)

    # get feature vectors for all the tweets and append label at the end
    for tweet,label in itertools.izip(l_tweets,l_classes):
        if classifier == 1:
            l_features = detectFeatures(tweet[2], pairname, classifier, l_topBigrams50)
        elif classifier == 2:
            l_features = detectFeatures(tweet[2], pairname, classifier, l_topBigrams45)
        else:
            raise Exception('Unknown classifier number in __analyzeTrainingSet!')
        tweet.append(l_features)
        tweet.append(label)
    #write results to a csv file
    resultFile = open("NewData/" + pairname + "/TrainingSets/" + pairname + outfile,'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(l_tweets)
    

if __name__ == '__main__': 
    pass   
    #read the currency pairs from textfile
#     pairsFile = open("Pairs.txt","r");
#     pairs = pairsFile.readlines()
#     pairsFile.close()
#     pairs = [pair.replace('/','').strip() for pair in pairs[1:]]
#     pairnames = ['GBPUSD', 'USDJPY', 'AUDUSD', 'USDCHF', 'USDCAD']
#     for pair in pairnames:
#         __analyzeTrainingSet(pair, 1, 'TrainingFeaturesTop50+updown.csv')
#         __analyzeTrainingSet(pair, 2, 'TrainingFeaturesTop45+7unigrams.csv')






