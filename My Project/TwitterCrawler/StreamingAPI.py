#!/usr/bin/python
'''
Created on 15 Oct 2013

@author: miljan
'''
import sys
import tweepy
import pprint
import urllib

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
#         pprint.pprint([status.user.name,removeNonAscii(status.text),status.lang])
#         pprint.pprint(status.lang)
        print removeNonAscii(status.text)
        sys.stdout.flush()
#         yield status.lang    
    
    def on_error(self, status_code):
        print 'Encountered error with status code:' + status_code
        sys.stdout.flush()
        return True # Don't kill the stream
    
    def on_timeout(self):
        print 'Timeout...'
        sys.stdout.flush()
        return True # Don't kill the stream

# print "hi1"
# sys.stdout.flush()
pairsFile = open("Pairs.txt","r");
pairs = pairsFile.readlines()
pairsFile.close();
querystring = [x.strip().replace('/','') for x in pairs[1:]]
querystring.extend([urllib.quote(x.strip(), '') for x in pairs[1:]])
# querystring.extend([x.strip().replace('/','%2F') for x in pairs[1:]])
# print querystring
# sys.stdout.flush()

def streamTweets():
    auth = tweepy.OAuthHandler('lLynvl98Pv08mftQwdbLg', '1NeHl8w5Ceh46XpLuxN7xebDSQNc2NsWlSEdzlVc4')
    auth.set_access_token('205479111-RS1reCmhxidi3GZWV29wN7kj6tjcxTDuStDnuLwU', 'WVj2SjUSQv12Cp3rs27MvoYCZ7IEOpK2Nu41e4AtTc')
    api = tweepy.API(auth)
            
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(track=querystring, languages=['en'])
#     for g in generator:
#         print g
    
if __name__ == '__main__':
    streamTweets()





