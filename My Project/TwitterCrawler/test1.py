# # '''
# # Created on 07.10.2013.
# # 
# # @author: Miljan
# # '''
# # 
# # # import nltk
# # # x = nltk.word_tokenize('The cat sat on the mat')
# # # print x
# # #  
# # # from sklearn import datasets
# # # iris = datasets.load_iris()
# # # print type(iris.data)
# # # print 'target:'
# # # print iris.target
# # #  
# # # from sklearn.naive_bayes import GaussianNB
# # # gnb = GaussianNB()
# # # y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
# # # print("Number of mislabeled points : %d" % (iris.target != y_pred).sum())
# # # print y_pred
# # 
# # import csv
# #  
# # path = '/home/miljan/Documents/TwitterCrawler/Historic/GBPUSD/GBPUSDTesting.csv'
# # features = []
# # target = []
# # with open(path, 'rb') as csvfile:
# #     reader = csv.reader(csvfile, delimiter=',')
# #     for row in reader:
# #         features.append(row[4:-1])
# #         target.append(row[-1])
# # print 'features: '+str(len(features[1]))
# # print target
# # # target = []
# # # with open(path1, 'rb') as csvfile1:
# # #     reader1 = csv.reader(csvfile1, delimiter=',')
# # #     for row in reader1:
# # #         target.append(row[4])
# # # print 'target: ' + str(len(target))
# # # 
# # # print len(features[0])
# # # # print '------------------'
# # # # print target
# # #   
# # import numpy as np
# # features = np.array(features, dtype='int32')
# # target = np.array(target, dtype='int32')
# # from sklearn.naive_bayes import GaussianNB
# # gnb = GaussianNB()
# # y_pred = gnb.fit(features, target).predict(features)
# # # print y_pred
# # # print target
# # print("Number of mislabeled points : %d" % (target!= y_pred).sum())
# # 
# # # import ystockquote, datetime
# # # #read the currency pairs from textfile
# # # pairsFile = open("Pairs.txt","r");
# # # pairs = pairsFile.readlines()
# # # pairsFile.close();
# # # print pairs
# # # for pairCounter in range(1,len(pairs)):
# # #     currentPair = pairs[pairCounter].replace('/',"").replace('\r\n','').upper()
# # #     fileToWrite=open("NewData/"+currentPair.upper()+"/"+currentPair.upper()+"Prices.csv","a")
# # #     print fileToWrite
# # #     print ystockquote.get_price(currentPair+"=X")
# # #     fileToWrite.write(ystockquote.get_price(currentPair+"=X")+","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ ", \n")
# # 
# # 
# # 
# # 
# # # path = '/home/miljan/workspace/Laurentiu Project/TwitterCrawler/NewData/OTHER/prices.csv'
# # # prices = []
# # # with open(path, 'rb') as csvfile:
# # #     reader = csv.reader(csvfile, delimiter=',')
# # #     for row in reader:
# # #         list = row[0].split(',')
# # #         prices.append(list[0])
# # #         
# # # # print prices
# # # 
# # # 
# # # import numpy as np
# # # from sklearn import gaussian_process
# # # def f(x):
# # #     return x * np.sin(x)
# # # 
# # # X = np.array(prices,dtype='float64')
# # # # X = np.atleast_2d([1., 3., 5., 6., 7., 8.]).T
# # # y = f(X).ravel()
# # # x = np.atleast_2d(np.linspace(0, 10, 1000)).T
# # # gp = gaussian_process.GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-1)
# # # gp.fit(X, y)
# # # y_pred, sigma2_pred = gp.predict(x, eval_MSE=True)
# # # print y_pred
# # # # print sigma2_pred
# # import csv,pprint
# # 
# # # get negation words
# # negationsWords = open("negations.txt","r");
# # negations = negationsWords.readlines()
# # negationsWords.close()
# # negations = negations[0].split()
# # 
# # 
# # counter = 0
# # tweets = []
# # path1 = "Historic/EURUSD/EURUSD.csv"
# # with open(path1, 'rb') as csvfile1:
# #     reader1 = csv.reader(csvfile1, delimiter=',')
# #     for row in reader1:
# #         sentence = row[2].split()
# #         for neg in negations:
# #             if neg in sentence:
# #                 counter+=1
# #                 tweets.append(row[2])
# #                 break
# # print counter
# # pprint.pprint(tweets)
# 
# import csv, pprint, ast
# 
# tweets = []
# path1 = "output.csv"
# with open(path1, 'rb') as csvfile1:
#     reader1 = csv.reader(csvfile1, delimiter=',')
#     for row in reader1:
#         tweets.append(row)
# pprint.pprint(ast.literal_eval(tweets[0][4]))

import nltk

def gender_features(word):
    return {'last_letter': word[-1]}


from nltk.corpus import names
import random
names = ([(name, 'male') for name in names.words('male.txt')] +
         [(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)

featuresets = [(gender_features(n), g) for (n,g) in names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
import pprint
pprint.pprint(train_set)

a = classifier.classify(gender_features('Neo'))
print a




