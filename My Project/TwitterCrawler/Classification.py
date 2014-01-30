'''
Created on 8 Nov 2013

@author: miljan
'''

from FeatureDetection import detectFeatures
from Classifiers import __produceFeaturesDictionary
import pprint, pickle, ast, csv  # @UnusedImport


"""
Function which takes a given pairname, accesses the appropriate files
and marks all the important features present in the given tweets.
It produces an output csv file with feature vector added at the end
of each tweet.
"""
def analyzeTweets(pairname,infile, outfile):
    # list of tweets in the set
    l_tweets = []
    # Read all the data from the designated file
    path1 = "NewData/" + pairname + "/" + pairname + infile
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            l_tweets.append(row)
    
    # get feature vectors for all the tweets
    for tweet in l_tweets:
        l_features = detectFeatures(tweet[2], pairname, 1)
        tweet.append(l_features)
#     pprint.pprint(l_tweets)
    # write the result to a csv file
    resultFile = open("NewData/" + pairname + "/" + pairname + outfile,'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(l_tweets)


"""
Classify a given tweet vector for a specific pair.
NB 1 or 2 or SVM (nr. 3) is used, depending on 'classifier' parameter.
Returns a list of 2 elements: [classification, confidence] if NB otherwise 
just [classification].
"""
def classifyTweet(tweetVector, pairname, classifier):  
    nbFlag = 0  
    # unpickle the classifier
    if classifier == 1:
        classif = "NaiveBayes1.pickle"
        nbFlag = 1
    elif classifier == 2:
        classif = "NaiveBayes2.pickle"
        nbFlag = 1
    elif classifier == 3:
        classif = "svm.pickle"
    else:
        raise Exception("Wrong classifier number given in NaiveBayes.classifyTweet()")
    f = open("NewData/" + pairname + "/Classifiers/" + pairname + classif)
    classifier = pickle.load(f)
    f.close()
    
    if nbFlag == 1:
        # produce feature set from the feature string literal
        d_featureVector = __produceFeaturesDictionary(tweetVector)
        # get the probability distribution of classed
        probDist = classifier.prob_classify(d_featureVector)
        # get the class with highest probability
        maxClass = probDist.max()
        return [maxClass,probDist.prob(maxClass)]
    else: # it's an svm
        l_featureVector = ast.literal_eval(tweetVector)
        prediction = classifier.predict(l_featureVector)
        return [prediction]


"""
Function which takes name of the fx pair and input and output files.
It classifies all the tweets in the input file of the given pair
and write results to the specified outfile.
"""
def classify(pairname,infile, outfile, classifier):
    data = []
    path1 = "NewData/" + pairname + "/" + pairname + infile
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            data.append(row)
    
    # append classifications to tweets
    for i in data:
        classification = classifyTweet(i[4], pairname, classifier)
        i.append(classification[0])
    
    # write classifications to a specified file
    resultFile = open("NewData/" + pairname + "/" + pairname + outfile,'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(data)
            

if __name__ == '__main__':
#     analyzeTweets('EURUSD', '_NFPtest8Nov.csv', '_NFPtest8NovFeatures.csv')
    classify('EURUSD', '_NFPtest8NovFeatures.csv', '_NFPtest8NovClassified.csv', 1)
    
    
    
    
    
    
    
    
    
    
    
    
    