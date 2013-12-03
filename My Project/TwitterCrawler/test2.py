'''
Created on 18 Oct 2013

@author: miljan
'''
# test1 3.91038128762278E+017
# import datetime
# tweets_ids = [1,2]
# if len(tweets_ids) > 0:
#     controlIdFile = open("NewData/maximum_id.csv","w")
#     if controlIdFile:
#         print 'success'
#     print controlIdFile
# try:
#     controlIdFile.write(str(max(tweets_ids)))
#     controlIdFile.close()
# except Exception as fileEx:
#     print(str(fileEx) +","+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "\n")
# 
# print 'done'

from sklearn import svm
import csv, pprint, ast, random
import numpy as np
from nltk import NaiveBayesClassifier
from NaiveBayes import __produceFeatures
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB  # @UnusedImport

def trainClassifier1(pairname, trainset, pickleFilename, classifier):
    
    cumulative = []
    for j in xrange(1,50):
        featureVectors = []
        labelSet = []
        
        # My set of features
        path1 = "NewData/" + pairname + "/TrainingSets/" + pairname + trainset
        with open(path1, 'rb') as csvfile1:
            reader1 = csv.reader(csvfile1, delimiter=',')
            for row in reader1:
                featureVectors.append(ast.literal_eval(row[4]))
                labelSet.append(ast.literal_eval(row[5]))
    
        featureSet = zip(featureVectors,labelSet)
        featureSet = np.array(featureSet)
        random.shuffle(featureSet)
        featureVectors = featureSet[:,0].tolist()
        labelSet = featureSet[:,1].tolist()
        
        if classifier == 'naiveBayes':
            featureSet = [(__produceFeatures(f),l) for (f,l) in zip(featureVectors,labelSet)]
    
        acc = []
        for i in xrange(0,5):
            a = i*100
            b = (i*100)+100
            
            if classifier == 'svm': 
                test_set = featureVectors[a:b]
                train_set = featureVectors[:a] + featureVectors[b:]
                test_labels = labelSet[a:b]
                train_labels = labelSet[:a] + labelSet[b:]
                clf = svm.LinearSVC()
                clf.fit(train_set, train_labels)
            elif classifier == 'naiveBayes':
                test_set = featureSet[a:b]
                train_set = featureSet[:a] + featureSet[b:]
                naiveBayes = NaiveBayesClassifier.train(train_set)
                test_set, test_labels = [i[0] for i in test_set], [i[1] for i in test_set]
            elif classifier == 'naiveBayes2':
                test_set = featureVectors[a:b]
                train_set = featureVectors[:a] + featureVectors[b:]
                test_labels = labelSet[a:b]
                train_labels = labelSet[:a] + labelSet[b:]
                clf = BernoulliNB()
                clf.fit(train_set, train_labels, )
                
            
            counter = 0
            for (case,label) in zip(test_set,test_labels):
                if classifier == 'svm' or classifier == 'naiveBayes2':
                    prediction = clf.predict(case) 
                elif classifier == 'naiveBayes':
                    probDist = naiveBayes.prob_classify(case)
                    prediction = probDist.max()
                if label != prediction:
                    counter += 1 
            acc.append(counter)
        print str(j)+". " + str(100-sum(acc)/5.0)
        cumulative.append(100-sum(acc)/5.0)  
    print "Total: " + str(sum(cumulative)/50.0) 
    return sum(cumulative)/50.0  
    
    
if __name__ == '__main__':
    pairs = ['EURUSD','GBPUSD', 'USDJPY', 'AUDUSD', 'USDCHF', 'USDCAD']
#     pairs = ['EURUSD']
    final  = [] 
    for pair in pairs:
        res = trainClassifier1(pair, 'TrainingFeaturesTop50+updown.csv', 'EURUSDsvm1.pickle', 'naiveBayes2')
        final.append([pair,res])
    pprint.pprint(final)