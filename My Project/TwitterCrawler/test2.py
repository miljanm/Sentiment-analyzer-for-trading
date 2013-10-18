'''
Created on 18 Oct 2013

@author: miljan
'''
# test1 3.91038128762278E+017
import datetime
tweets_ids = [1,2]
if len(tweets_ids) > 0:
    controlIdFile = open("NewData/maximum_id.csv","w")
    if controlIdFile:
        print 'success'
    print controlIdFile
try:
    controlIdFile.write(str(max(tweets_ids)))
    controlIdFile.close()
except Exception as fileEx:
    print(str(fileEx) +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")

print 'done'