'''
Created on 30 Jan 2014

@author: miljan
'''

import csv, os
from Classification import classify
from HeuristicClassification import heuristic_classify
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
        # flag to mark when there is nothing new to write/classify
        passFlag = 0
        
        # -------- PRICE WRITING --------
        
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
            passFlag = 1
        # remove the temp file
        try:
            os.remove(pathToPrices)
        except OSError as e:
            print 'removal ' + str(e)
            pass
        
        if not passFlag:
            # write the prices read to the live prices file
            fileToWrite = open("NewData/" + pair + "/CascadingTests/" + pair + "LivePrices.csv","a") 
            wr = csv.writer(fileToWrite, dialect='excel')
            wr.writerows(prices)
            fileToWrite.close()
            # write the prices read to the main database
            fileToWrite = open("NewData/"+ pair +"/"+ pair +"Prices.csv","a") 
            wr = csv.writer(fileToWrite, dialect='excel')
            wr.writerows(prices)
            fileToWrite.close()
        passFlag = 0
        # -------- TWEET WRITING --------
         
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
            passFlag = 1
        # remove the temp file
        try:
            os.remove(pathToTweets)
        except OSError as e:
            print 'removal ' + str(e)
            pass
        
        if not passFlag:
            # write the tweets read to the main database
            fileToWrite = open("NewData/"+ pair +"/"+ pair +"Raw.csv","a") 
            wr = csv.writer(fileToWrite, dialect='excel')
            wr.writerows(tweets)
            fileToWrite.close()        
            
            # -------- ML CLASSIFICATION --------
             
            # send tweets to be classified by ML algorithms and put into temp file
            outfile = "NewData/" + pair + "/CascadingTests/" + pair + "temp.csv"
            classify(pair, tweets, outfile)  
            
            # -------- HEURISTIC CLASSIFICATION --------
            
            # read intermediate classifications results
            fileToRead = "NewData/" + pair + "/CascadingTests/" + pair + "temp.csv"
            tweets = []
            try:
                with open(fileToRead, 'rb') as csvfile1:
                    reader1 = csv.reader(csvfile1, delimiter=',')
                    for row in reader1:
                        tweets.append(row)
            except IOError as e:
                print 'opening ' + str(e)
            # remove the temp file
            try:
                os.remove(fileToRead)
            except OSError as e:
                print 'removal ' + str(e)
                pass
                
            # final file for the processed data
            outfile = "NewData/" + pair + "/CascadingTests/" + pair + "LiveResults.csv"
            heuristic_classify('EURUSD', tweets, outfile)
         
    print 'done'

if __name__ == '__main__':
    analyzeFeed()
    
    
    
    
    
    
    
    
    
    
    
    
    
    