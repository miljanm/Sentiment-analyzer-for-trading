'''
Created on 3 Dec 2013

@author: miljan
'''

# kill server:
# kill -9 `fuser -n tcp 5000`

# from flask import Flask, jsonify, request  # @UnusedImport
# import urllib
# import tweepy, pprint, sys
# 
# def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
# 
# app = Flask(__name__)
#  
# @app.route('/')
# def hello_world():
#     pairsFile = open("Pairs.txt","r");
#     pairs = pairsFile.readlines()
#     pairsFile.close();
#     querystring = [x.strip().replace('/','') for x in pairs[1:]]
#     querystring.extend([urllib.quote(x.strip(), '') for x in pairs[1:]])
#     # querystring.extend([x.strip().replace('/','%2F') for x in pairs[1:]])
# #     print querystring
#      
#     auth = tweepy.OAuthHandler('lLynvl98Pv08mftQwdbLg', '1NeHl8w5Ceh46XpLuxN7xebDSQNc2NsWlSEdzlVc4')
#     auth.set_access_token('205479111-RS1reCmhxidi3GZWV29wN7kj6tjcxTDuStDnuLwU', 'WVj2SjUSQv12Cp3rs27MvoYCZ7IEOpK2Nu41e4AtTc')
#     api = tweepy.API(auth)
#          
#     class CustomStreamListener(tweepy.StreamListener):
#         def on_status(self, status):
#             pprint.pprint([status.user.name,removeNonAscii(status.text),status.lang])
#             return 'Hi'
#                  
#          
#         def on_error(self, status_code):
#             print >> sys.stderr, 'Encountered error with status code:', status_code
#             return True # Don't kill the stream
#          
#         def on_timeout(self):
#             print >> sys.stderr, 'Timeout...'
#             return True # Don't kill the stream
#      
#     sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
#     sapi.filter(track=querystring, languages=['en'])
# 
# 
# 
# # @app.route('/brandrank/api/v1.0/query/debugmode/<path:encoded>', methods = ['GET'])
# # def start_engine2(encoded):
# #     return 'Hello world!'
#           
# if __name__ == '__main__':
#     app.debug = True
#     app.run()

import subprocess
from flask import Flask, make_response, Response, jsonify, request  # @UnusedImport
import urllib, time
import tweepy, pprint, sys

app = Flask(__name__)

# @app.route('/')
# def index():
    
#     tweetList = []
#     
#     class CustomStreamListener(tweepy.StreamListener):
#         def on_status(self, status):
#             pprint.pprint([status.user.name,removeNonAscii(status.text),status.lang])
#             yield status.lang
#             tweetList.append(status.lang)
# #             return 'Hi'
# #             yield '%s<br/>\n' % status.lang
#                        
#         def on_error(self, status_code):
#             print >> sys.stderr, 'Encountered error with status code:', status_code
#             return True # Don't kill the stream
#           
#         def on_timeout(self):
#             print >> sys.stderr, 'Timeout...'
#             return True # Don't kill the stream
# 
#     pairsFile = open("Pairs.txt","r");
#     pairs = pairsFile.readlines()
#     pairsFile.close();
#     querystring = [x.strip().replace('/','') for x in pairs[1:]]
#     querystring.extend([urllib.quote(x.strip(), '') for x in pairs[1:]])
#     # querystring.extend([x.strip().replace('/','%2F') for x in pairs[1:]])
# #     print querystring
#      
#     auth = tweepy.OAuthHandler('lLynvl98Pv08mftQwdbLg', '1NeHl8w5Ceh46XpLuxN7xebDSQNc2NsWlSEdzlVc4')
#     auth.set_access_token('205479111-RS1reCmhxidi3GZWV29wN7kj6tjcxTDuStDnuLwU', 'WVj2SjUSQv12Cp3rs27MvoYCZ7IEOpK2Nu41e4AtTc')
#     api = tweepy.API(auth)
#     
#     def inner():
#         sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
#         sapi.filter(track=querystring, languages=['en'])
    
#     def inner():
#         proc = subprocess.Popen(
#             ['dmesg'],             #call something with a lot of output so we can see it
#             shell=True,
#             stdout=subprocess.PIPE
#         )
# 
#         for line in iter(proc.stdout.readline,''):
#             yield line.rstrip() + '<br/>\n'
#         for x in range(10):
#             time.sleep(1)
#             yield '%s<br/>\n' % x
#          
#         sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
#         sapi.filter(track=querystring, languages=['en'])
#         for x in range(10):
#             time.sleep(1)
#             yield '%s<br/>\n' % x
#         while 1:
#             if tweetList:
#                 tweet = tweetList.pop()
#                 yield tweet
#     return Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show t
#     def inner():
#         proc = subprocess.Popen(
#             "./StreamingAPI.py",             #call something with a lot of output so we can see it
#             shell=True,
#             stdout=subprocess.PIPE
#         )
#         while 1:
#             for line in iter(proc.stdout.readline,''):
#                 time.sleep(1)                           # Don't need this just shows the text streaming
#                 yield line.rstrip() + '<br/>\n'
# 
#     return Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show th$
@app.route('/')
def index():
    def inner():     
        proc = subprocess.Popen(
                    ['python','./StreamingAPI.py'],
                    shell=False,
                    stdout=subprocess.PIPE
                )
        for line in iter(proc.stdout.readline,''):
            yield '%s<br/>\n' % line
#         for x in range(5):
#             time.sleep(1)
#             yield '%s<br/>\n' % x
    return Response(inner(), mimetype='text/html')  # text/html is required 


@app.route("/simple.png")
def simple():
    import datetime
    import StringIO
    import random
    import Plot
     
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
     
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == '__main__':
    app.run(debug=True)

