#!/usr/bin/env python
'''
Created on 9 Oct 2013

@author: miljan
'''
import twitter
import datetime
import re
import time
import os
import ystockquote
from socket import error as SocketError

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

#read the currency pairs from textfile
pairsFile = open("Pairs.txt","r");
pairs = pairsFile.readlines()
pairsFile.close()

#build query string to be used within searching api
querystring = ''
#replace newlines and / signs
for pair in pairs[1:]:
    querystring += pair.replace('\r\n','').replace('/','') 
    if(pair != pairs[len(pairs) -1]):
        querystring += " OR "

############################################
#Get Yahoo! Finance Quotes                 #
############################################
for pairCounter in range(1,len(pairs)):
    currentPair = pairs[pairCounter].replace('/',"").replace('\r\n','').upper()
    fileToWrite=open("NewData/"+currentPair.upper()+"/"+currentPair.upper()+"TemporaryPrices.csv","a")
    try: 
        quote = ystockquote.get_price(currentPair+"=X")
        print quote
    except SocketError as e:
        fileToWriteError=open("Errors.txt","a")
        fileToWriteError.write('Socket error' +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")
        fileToWriteError.write(e)
        print e
        fileToWriteError.close()
    except Exception as e:
        fileToWriteError=open("Errors.txt","a")
        fileToWriteError.write('Other error' +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")
        fileToWriteError.write(e)
        print e
        fileToWriteError.close()
    fileToWrite.write(quote+","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ ", \n")
        
#read control_maximum file and get maximum id to use as a filter
try:
    control = open("NewData/maximum_id.csv","r")
    maxid = control.readline()
    control.close()
except Exception as fileEx:
    maxid="0"
    fileToWriteError=open("Errors.txt","a")
    fileToWriteError.write(str(fileEx) +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")

#initialize searching
twitter_search = twitter.Twitter(domain='api.twitter.com', api_version='1.1',  auth=twitter.oauth.OAuth('205479111-RS1reCmhxidi3GZWV29wN7kj6tjcxTDuStDnuLwU', 'WVj2SjUSQv12Cp3rs27MvoYCZ7IEOpK2Nu41e4AtTc', 'lLynvl98Pv08mftQwdbLg', '1NeHl8w5Ceh46XpLuxN7xebDSQNc2NsWlSEdzlVc4'))

#hold the query results
twitter_result = []

#run twitter search api
try:
    twitter_result.append(twitter_search.search.tweets(q=querystring,lang="en",count=100,result_type="recent",since_id=str(long(float(maxid)))))
except ValueError:
    fileToWriteErrorConnection=open("Errors.txt","a")
    fileToWriteErrorConnection.write(str(ValueError) +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")
        

#build tweet_id array eg 23123122219978
tweets_ids = [long(r['id_str']) for result in twitter_result for r in result['statuses']]

#build tweets array
tweets = [r['text'] for result in twitter_result for r in result['statuses']]

#build tweet dates array
timestamp = [time.strptime(r['created_at'],'%a %b %d %H:%M:%S +0000 %Y') for result in twitter_result for r in result['statuses']]

#build tweets users array
tweets_users = [r['user']['name'] for result in twitter_result for r in result['statuses']]



for counter in range(0,len(tweets)):
    if tweets_ids[counter] > long(float(maxid)):
        ###########################
        #   Tweet  clensing       #
        ###########################
        #remove hashtags, user tags and user retweets
        tweets[counter]=re.sub(r'(?<=#)\w+| #|(?<=@)\w+| @ |(?<=RT)\w+|RT',"", tweets[counter])
        #convert tweet to lowecase 
        tweets[counter] = tweets[counter].lower()
        tweets[counter]= re.sub(r'[^\w:.$]'," ",tweets[counter])
        #remove links
        tweets[counter] = re.sub(r'http\\w+',"",tweets[counter])
        tweets[counter]= re.sub(r'http:.{15}',"",tweets[counter])
        tweets[counter]= re.sub(r'http:.{10}',"",tweets[counter])

        ###############################
        # Writing to appropriate File #
        ###############################
        for pairCounter in range(1,len(pairs)):
            currentPair = pairs[pairCounter].replace('/',"").replace('\r\n',"").lower()
            if currentPair in tweets[counter]:
                if not os.path.isdir("NewData/"+currentPair.upper()):
                    os.makedirs("NewData/"+currentPair.upper())
                try:
                    fileToWrite=open("NewData/"+currentPair.upper()+"/"+currentPair.upper()+"TemporaryRaw.csv","a")
                except Exception as fileEx:
                    fileToWriteError=open("Errors.txt","a")
                    fileToWriteError.write(str(fileEx) +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")
                tweets_users[counter] = removeNonAscii(tweets_users[counter])
                tweets[counter] = removeNonAscii(tweets[counter])
                fileToWrite.write(str(tweets_ids[counter]) +","+tweets_users[counter]+","
                                  +tweets[counter]+","+time.strftime('%d/%m/%Y %H:%M:%S',timestamp[counter])+"\n")
                fileToWrite.close()

print 'Collected: ' + str(len(tweets_ids)) + ' tweet(s)!'
#Write maximum id to file
if len(tweets_ids) > 0:
    controlIdFile = open("NewData/maximum_id.csv","w")
    try:
        controlIdFile.write(str(max(tweets_ids)))
        controlIdFile.close()
    except Exception as fileEx:
        fileToWriteError=open("Errors.txt","a")
        fileToWriteError.write(str(fileEx) +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")

print 'done'