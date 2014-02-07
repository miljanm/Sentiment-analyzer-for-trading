'''
Created on 9 Nov 2013

@author: miljan
'''

import matplotlib.dates as dt
import matplotlib.pyplot as plot
from mpl_toolkits.axes_grid1 import host_subplot
import csv, pprint  # @UnusedImport
from datetime import datetime
import numpy as np
import operator

"""
Function which takes a date in the format provided from fx quotes
from yahoo finance and returns a matplotlib date object for plotting.
"""
def _formatDate(dateString):
    try:
        date_object = datetime.strptime(dateString, '%d/%m/%Y %H:%M:%S')
    except Exception as e:
        print e
        return 'FAIL'
    return dt.date2num(date_object)

"""
Function which returns a numpy array with price data for the 
requested pair.
"""
def getPriceData(pairname, rangeA):
    data = []
    temp = []
    path = "NewData/" + pairname + "/CascadingTests/" + pairname + "LivePrices.csv"
    with open(path, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            temp.append(row)
    
    temp.sort(key=operator.itemgetter(1))
    if rangeA > len(temp): 
        rangeA = len(temp)
    for i in temp[-rangeA:]:
        date = _formatDate(i[1])
        # guard against improperly formatted time strings
        if date == 'FAIL':
            continue
        arr = np.array([float(i[0]),date])
        data.append(arr)
    # convert price/dates pairs to numpy array
    return np.array(data)

"""
Function which returns a numpy array with sentiment data for the 
requested pair.
"""
def getSentimentData(pairname, infile, rangeA):
    data = []
    temp = []
    path = "NewData/" + pairname + "/CascadingTests/" + pairname + infile
    with open(path, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            temp.append(row)
    
    temp.sort(key=operator.itemgetter(5))
    if rangeA > len(temp): 
        rangeA = len(temp)
    for i in temp[-rangeA:]:
        date = _formatDate(i[5])
        # guard against improperly formatted time strings
        if date == 'FAIL':
            continue
        
        if i[3][0] == '-':
            if i[3][1] == '1':
                classif = -1
        elif i[3][0] == '0':
            classif = 0
        elif i[3][0] == '1':
            classif = 1
        else: 
            continue
        arr = np.array([classif,date])
        data.append(arr)
    
    # make continuous time series for the sentiment
    # sentiment read at any point in data represents sentiment up to that point
    for i in xrange(1,len(data)):
        data[i][0] += data[i-1][0]
    return np.array(data)


"""
Function which plots the price data correlated with sentiment data.
"""
def plotPrediction(np_price_data, np_sentiment_data):
#     # plot the prices 
#     fig, ax = plot.subplots()
#     plot.plot_date(np_price_data[-3000:-1000,1],np_price_data[-3000:-1000,0],'-')
# #     plot.plot_date(np_price_data[:,1],np_price_data[:,0],'-')
#     plot.plot_date(np_sentiment_data[:,1],np_sentiment_data[:,0],'-')
#     ax.autoscale_view()
#     ax.grid(True)
#     fig.autofmt_xdate()
#     plot.show()
    

#     fig, ax = plot.subplots()
    host = host_subplot(111)
    par = host.twinx()

    host.set_xlabel("Time")
    host.set_ylabel("Pair Price")
    par.set_ylabel("Sentiment")
      
#     p1, = host.plot_date(np_price_data[-3000:-1000,1],np_price_data[-3000:-1000,0],'-',label='Pair Price')
    p1, = host.plot_date(np_price_data[:,1],np_price_data[:,0],'-',label='Pair Price')
    p2, = par.plot_date(np_sentiment_data[:,1],np_sentiment_data[:,0],'-',label='Sentiment')
    
    host.autoscale_view()
    host.grid(True)
#     par.set_ylim([-2000,500])
#     fig.autofmt_xdate()
#     matplotlib.pyplot.autofmt_xdate()
    plot.xticks(rotation=40)
    
     
    leg = plot.legend(loc='lower right')
      
    host.yaxis.get_label().set_color(p1.get_color())
    leg.texts[0].set_color(p1.get_color())
       
    par.yaxis.get_label().set_color(p2.get_color())
    leg.texts[1].set_color(p2.get_color())
     
#     plot.show()
    
    fig = plot.gcf()
    fig.set_size_inches(18.5,10.5)
    plot.savefig('testFeb1.png',dpi=100)

def main():
    pair = 'USDJPY'
    np_sentiment_data = getSentimentData(pair, 'LiveResults.csv', 1000)
    print np_sentiment_data
    np_price_data = getPriceData(pair, 1200)
    print np_price_data
    plotPrediction(np_price_data, np_sentiment_data)
    
if __name__ == '__main__':
    main()
    
    
    
    