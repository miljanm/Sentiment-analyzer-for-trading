'''
Created on 30 Jan 2014

@author: miljan

With reference to Brill (1995) and Lager (1999) corrective rules for corpus tagging, we can use them 
in this case to make classifications of tweets due to specific sublanguage of the group that produced
this tweets. 
Rules such as:
% replace A by B if the current word is C and previous word is D
t12(A,B,C,D) # tag:A>B <- wd:C@[0] & wd:D@[-1]

can be written as:
% set class to be A if the current word is C and previous word is D
t12(A, B, C) # class:A <- wd:C@[0] & wd:D@[-1]

'''

from FeatureExtraction import createUnigrams
import csv

def heuristic_classify(pairname ,data, outfile):
    counter = 0
    for i in data:
        counter = counter + 1
#         print i[0], i[1], i[2]
        unigrams = createUnigrams(i[2])
#         print str(counter) + str(unigrams)
        # rule 1
        if unigrams and unigrams[0] == 'bought': 
            print 'r1 match@'+ str(counter)
            i[3] = 1
            continue
        # rule 2
        if unigrams and unigrams[0] == 'sold': 
            print 'r2 match@'+ str(counter)
            i[3] = -1
            continue
        # rule 3
        if unigrams and 'idea' in unigrams:
            print 'r3 match@'+ str(counter)
            i[3] = 0
            continue
        # rule 4 - closed sell stop - price is expected to reverse trend upwards 
        if unigrams and unigrams[0] == 'closed' and unigrams[1] == 'sell' and unigrams[2] == 'stop':
            print 'r4 match@'+ str(counter)
            i[3] = 1
            continue
        # rule 5 - closed buy stop - price is expected to reverse trend downwards 
        if unigrams and unigrams[0] == 'closed' and unigrams[1] == 'buy' and unigrams[2] == 'stop':
            print 'r5 match@'+ str(counter)
            i[3] = -1
            continue
        # rule 6 - sell stop, price is expected to break support
        if unigrams and unigrams[0] == 'sell' and unigrams[1] == 'stop': 
            print 'r6 match@'+ str(counter)
            i[3] = -1
            continue
        # rule 7 - buy stop, price is expected to break resistance
        if unigrams and unigrams[0] == 'buy' and unigrams[1] == 'stop': 
            print 'r7 match@'+ str(counter)
            i[3] = 1
            continue
        # rule 8 - sl hit/hit sl, direction is unknown
        if (unigrams and 'sl' in unigrams and unigrams[unigrams.index('sl')-1] == 'hit') or \
           (unigrams and 'sl' in unigrams and unigrams[unigrams.index('sl')+1] == 'hit'):
            print 'r8 match@'+ str(counter)
            i[3] = 0
            continue
        # rule 9 - opened ... buy/long lots
        if unigrams and 'opened' in unigrams and ('buy' in unigrams or 'long' in unigrams):
            print 'r9 match@'+ str(counter)
            i[3] = 1
            continue
        # rule 10 - opened ... sell/short lots
        if unigrams and 'opened' in unigrams and ('sell' in unigrams or 'short' in unigrams): 
            print 'r10 match@'+ str(counter)
            i[3] = -1
            continue
            
    resultFile = open(outfile, 'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(data)
    resultFile.close()
    
from Classification import classify        
if __name__ == '__main__':
    outfile = "NewData/EURUSD/CascadingTests/EURUSDoutput2.csv"
    fileToRead="NewData/EURUSD/CascadingTests/EURUSDtest1.csv"
    tweets = []
    try:
        with open(fileToRead, 'rb') as csvfile1:
            reader1 = csv.reader(csvfile1, delimiter=',')
            for row in reader1:
                tweets.append(row)
    except IOError as e:
        print 'opening ' + str(e)
    classify('EURUSD', tweets, outfile)
    
    
    outfile = "NewData/EURUSD/CascadingTests/EURUSDoutput2.csv"
    fileToRead="NewData/EURUSD/CascadingTests/EURUSDoutput2.csv"
    tweets = []
    try:
        with open(fileToRead, 'rb') as csvfile1:
            reader1 = csv.reader(csvfile1, delimiter=',')
            for row in reader1:
                tweets.append(row)
    except IOError as e:
        print 'opening ' + str(e)
    heuristic_classify('EURUSD', tweets, outfile)