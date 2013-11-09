'''
Created on 27 Oct 2013

@author: miljan

Module works on the corpus for every fx pair and chooses top 50
bigrams to be used in later classification.

'''

import nltk, pprint, string, csv  # @UnusedImport
from operator import itemgetter

"""
Function which takes a tweets, filters it and creates bigrams from it.
Returns a list of bigrams.
""" 
def createBigrams(sentence):
    allPairs = ['GBPUSD','EURUSD','AUDUSD','USDCAD','USDCHF','USDJPY']
    # Get stopwords from a text file
    stopwordsFile = open("stopwords.txt","r");
    stopwords = stopwordsFile.readlines()
    stopwordsFile.close()
    stopwords = [word.strip('\r\n') for word in stopwords]
    # correct misspelled tweets from a couple of sources
    sentence = sentence.replace('sho ', 'short ')
    # create tokens from the given sentence
    tokens = nltk.word_tokenize(sentence)
    #remove tweets with multiple pairs
    counter = 0
    for pair in allPairs:
        if pair.lower() in tokens:
            counter += 1
    if counter > 1:
        return []
    # remove stopwords from the sentence
    tokens = [token for token in tokens if token not in stopwords]
    # remove punctuation from tokens
    tokens = [s.translate(None, string.punctuation) for s in tokens]
    # remove numerics and empty strings
    tokens = [x for x in tokens if (x and not (x.isdigit() or x[0] == '-' and x[1:].isdigit()))]
    # create bigrams from tokens
    bigrams = nltk.bigrams(tokens)
    return bigrams
    
"""
Function which takes a tweets, filters it and creates unigrams from it.
Returns a list of unigrams.
"""    
def createUnigrams(sentence):
    allPairs = ['GBPUSD','EURUSD','AUDUSD','USDCAD','USDCHF','USDJPY']
    # Get stopwords from a text file
    stopwordsFile = open("stopwords.txt","r");
    stopwords = stopwordsFile.readlines()
    stopwordsFile.close()
    stopwords = [word.strip('\r\n') for word in stopwords]
    # correct misspelled tweets from a couple of sources
    sentence = sentence.replace('sho ', 'short ')
    # create tokens from the given sentence
    tokens = nltk.word_tokenize(sentence)
    #remove tweets with multiple pairs
    counter = 0
    for pair in allPairs:
        if pair.lower() in tokens:
            counter += 1
    if counter > 1:
        return []
    # remove stopwords from the sentence
    tokens = [token for token in tokens if token not in stopwords]
    # remove punctuation from tokens
    tokens = [s.translate(None, string.punctuation) for s in tokens]
    # remove numerics and empty strings
    tokens = [x for x in tokens if (x and not (x.isdigit() or x[0] == '-' and x[1:].isdigit()))]
    return tokens

"""
Function to generate a file with all the bigrams that are found
in the premade corpus of tweets for the given pair.
"""
def __getAllCorpusBigrams(pairname):
    # ------------------------------------------------------------
    # Create a list of all bigrams from the corpus
    # ------------------------------------------------------------
    
    # get tweets from historic and new data together
    tweets = []
    path1 = "Historic/" + pairname + "/" + pairname + ".csv"
    path2 = "NewData/" + pairname + "/" + pairname + "Raw.csv"
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
        l_bigrams = createBigrams(tweet)
        # go through bigrams list and update the dictionary
        for big in l_bigrams:
            if big == ('pips', 'pips'):
                continue
            if big in d_bigrams:
                d_bigrams[big] = d_bigrams[big] + 1
            else:
                d_bigrams[big] = 1
               
    # create a list from the dict
    csvData = []
    for (col1, col2), col3 in d_bigrams.iteritems():
        csvData.append([col1, col2, col3])
    # sort the list items from the dict by value (2d sort)
    csvData = sorted(csvData, key=itemgetter(2))
       
    # write all sorted pairs to a csv file
    f = open("NewData/" + pairname + "/" + pairname + "Bigrams.csv", 'w')
    f.writelines(','.join(str(j) for j in i) + '\n' for i in csvData)
    f.close()

 
"""
Function which creates a csv file containing top 50 bigrams for the
given fx pair.
Features are filtered based on high sentiment words.    
"""
def __getTop50Bigrams(pairname):
    # ------------------------------------------------------------
    # Generate top 50 bigrams
    # ------------------------------------------------------------
    
    features = []
    path2 = "NewData/" + pairname + "/" + pairname + "Bigrams.csv"
    with open(path2, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            features.append(row)
     
#     accepted = ['indecisive','support','resistance','rally','rallies','uptrend','upwards','sell','buy','bought','sold','bull','bullish','bear','bearish','long','short','upside','downtrend','downside','downward']    
    accepted = ['indecisive','support','resistance','rally','rallies','sell','buy','bought','sold','bull','bullish','bear','bearish','long','short']    
    notAccepted = ['term', 'ibfx2','ibfx','usd','ibfx617','ibfx619','ibfxlive','fcto','t','fxmgm','ubs', 'morgan', 'goldman','sachs','commerzbank','deutsche']
    firstFifty = []
    # get bigrams that match desired terms, and remove those that also contain unwanted terms
    for feat in reversed(features):
        # boolean to mark if there are unwanted terms
        contd = False
        for nac in notAccepted:
            if nac in feat:
                contd = True
        if contd: continue
        for accept in accepted:
            if accept in feat:
                firstFifty.append(feat)
                break
        if len(firstFifty) >= 50:
            break
     
    f = open("NewData/" + pairname + "/" + pairname + "Bigrams50v2.csv", 'w')
    f.writelines(','.join(str(j) for j in i) + '\n' for i in firstFifty)
    f.close()
     
    print pairname
    counter = 1
    for l in firstFifty:
        print str(counter) + str(l)
        counter += 1
    print '------------------------------------------'
    
    
if __name__ == '__main__':
    
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

    allPairs = ['GBPUSD','EURUSD','AUDUSD','USDCAD','USDCHF','USDJPY']
    
#     for pair in allPairs:
#         getTop50Bigrams(pair)
    __getTop50Bigrams('EURUSD')
    