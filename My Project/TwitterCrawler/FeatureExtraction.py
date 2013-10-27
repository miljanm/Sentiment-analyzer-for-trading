'''
Created on 27 Oct 2013

@author: miljan
'''

# Main bigrams
import nltk, pprint, string, csv  # @UnusedImport
from operator import itemgetter


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
    
def createBigrams(sentence, dict_bigram):
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
        return dict_bigram
    # remove stopwords from the sentence
    tokens = [token for token in tokens if token not in stopwords]
    # remove punctuation from tokens
    tokens = [s.translate(None, string.punctuation) for s in tokens]
    # remove numerics and empty strings
    tokens = [x for x in tokens if (x and not (x.isdigit() or x[0] == '-' and x[1:].isdigit()))]

    
    # create bigrams from tokens
    bigrams = nltk.bigrams(tokens)
    # update dict of bigrams
    for big in bigrams:
        if big == ('pips', 'pips'):
            continue
        if big in dict_bigram:
            dict_bigram[big] = dict_bigram[big] + 1
        else:
            dict_bigram[big] = 1
    return dict_bigram
    
    

def getTop50Bigrams(pairname):
         
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
        d_bigrams = createBigrams(tweet, d_bigrams)
       
    # create a list from the dict
    csvData = []
    for (col1, col2), col3 in d_bigrams.iteritems():
        csvData.append([col1, col2, col3])
    # sort the items from the dict by value
    csvData = sorted(csvData, key=itemgetter(2))
       
    # write all sorted pairs to a csv file
    f = open("NewData/" + pairname + "/" + pairname + "Bigrams.csv", 'w')
    f.writelines(','.join(str(j) for j in i) + '\n' for i in csvData)
    f.close()

    
    # ------------------------------------------------------------
    # Generate top 50 bigrams
    # ------------------------------------------------------------
    
    features = []
    path2 = "NewData/" + pairname + "/" + pairname + "Bigrams.csv"
    with open(path2, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            features.append(row)
     
    accepted = ['indecisive','support','resistance','rally','rallies','uptrend','upwards','sell','buy','bought','sold','bull','bullish','bear','bearish','long','short','upside','downtrend','downside','downward']    
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
     
    f = open("NewData/" + pairname + "/" + pairname + "Bigrams50.csv", 'w')
    f.writelines(','.join(str(j) for j in i) + '\n' for i in firstFifty)
    f.close()
     
    print pairname
    counter = 1
    for l in firstFifty:
        print str(counter) + str(l)
        counter += 1
    print '------------------------------------------'
    
    
if __name__ == '__main__':
    for pair in allPairs:
        getTop50Bigrams(pair)
    
    