'''
Created on 30 Jan 2014

@author: miljan
'''

import csv, os
from Classification import classify
from os import error as OSError

def analyzeFeed():
    #read the currency pairs from textfile
    pairsFile = open("Pairs.txt","r");
    pairs = pairsFile.readlines()
    pairsFile.close()
    pairList = []
    for pair in pairs[1:]:
        pairList.append(pair.replace('\r\n','').replace('/',''))
           
    for pair in pairList:
        # read the temporary csv containing new prices
        prices = []
        pathToPrices = "NewData/" + pair + "/" + pair + "TemporaryPrices.csv"
        try:
            with open(pathToPrices, 'rb') as csvfile1:
                reader1 = csv.reader(csvfile1, delimiter=',')
                for row in reader1:
                    prices.append([row[0],row[1]])
        except IOError as e:
            print 'opening ' + str(e)
        # write the prices read to the main database
        fileToWrite = open("NewData/"+ pair +"/"+ pair +"Prices.csv","a") 
        wr = csv.writer(fileToWrite, dialect='excel')
        wr.writerows(prices)
        fileToWrite.close()
        # remove the temp file
        try:
            os.remove(pathToPrices)
        except OSError as e:
            print 'removal ' + str(e)
            pass
         
        # read the temporary csv file containg new tweets
        tweets = []
        pathToTweets = "NewData/" + pair + "/" + pair + "TemporaryRaw.csv"
        try:
            with open(pathToTweets, 'rb') as csvfile1:
                reader1 = csv.reader(csvfile1, delimiter=',')
                for row in reader1:
                    tweets.append(row)
        except IOError as e:
            print 'opening ' + str(e)
        # write the tweets read to the main database
        fileToWrite = open("NewData/"+ pair +"/"+ pair +"Raw.csv","a") 
        wr = csv.writer(fileToWrite, dialect='excel')
        wr.writerows(tweets)
        fileToWrite.close()        
        # remove the temp file
        try:
            os.remove(pathToTweets)
        except OSError as e:
            print 'removal ' + str(e)
            pass
         
        # send tweets to be classified
        outfile = "NewData/" + pair + "/CascadingTests/" + pair + "LiveResults.csv"
        classify(pair, tweets, outfile)  
         
    print 'done'

if __name__ == '__main__':
    analyzeFeed()
    
    
    
    
    
    
    
    
    
    
    
    
    
    