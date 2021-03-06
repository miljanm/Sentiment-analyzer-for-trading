'''
Created on 8 Nov 2013

@author: miljan
'''


from Classifiers import __produceFeaturesDictionary
import pickle, csv
from FeatureDetection import detectFeatures, readFeaturesData


"""
Classify a given tweet vector for a specific pair.
NB 1 or 2 or SVM (nr. 3) is used, depending on 'classifier' parameter.
Returns a list of 2 elements: [classification, confidence] if NB otherwise 
just [classification].
"""
def __classifyTweet(tweetVector, pairname, classifier):  
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
        raise Exception("Wrong classifier number given in NaiveBayes.__classifyTweet()")
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
#         l_featureVector = ast.literal_eval(tweetVector)
        prediction = classifier.predict(tweetVector)
        return [prediction]
            

"""
Function which takes name of the fx pair and input and output files.
It classifies all the tweets in the input file of the given pair
and write results to the specified outfile.
"""
def classify(pairname, data, outfile):
    # read in the feature data
    l_topBigrams50, l_topBigrams45 = readFeaturesData(pairname)
    
    # number of items with confidence less than required percentage
    ltcounter = 0
    # append classifications to tweets
    for i in data:
#         if i[5]:
#             print "there is something here"
#         else:
#             print "nothing here"
        # detect the features in the tweet text
        l_features = detectFeatures(i[2], pairname, 1, l_topBigrams50)
        i.append(l_features)
        classification = __classifyTweet(i[4], pairname, 1)
        # cascading code
        # use NB1 and accept if confidence > 0.9
        if classification[1] > 0.9:
            i.append(i[3])
            i[3] = str(classification[0]) + 'nb1'
        # otherwise relegate to NB2 and accept if confidence > 0.7
        else:
            l_features = detectFeatures(i[2], pairname, 2, l_topBigrams45)
            i[4] = l_features 
            classification = __classifyTweet(i[4], pairname, 2)
            if classification[1] > 0.7:
                i.append(i[3])
                i[3] = str(classification[0]) + 'nb2'
            # if confidence is less than 0.5 don't classify it
            elif classification[1] < 0.5:
                i.append(i[3])
                i[3] = 'lt0.5'
                ltcounter += 1
            # otherwise classify with svm if between 0.7 and 0.5 confidence in NB
            else:
#                 print type(i[4])
                classification = __classifyTweet(i[4], pairname, 3)
                i.append(i[3])
                i[3] = str(int(classification[0])) + 's'
        print str(pairname) + ' ' + str(i[3])
    print 'unclassified: ' + str(ltcounter)
    
    # write classifications to a specified file
#     resultFile = open("NewData/" + pairname + "/CascadingTests/" + pairname + outfile,'wb')
    resultFile = open(outfile, 'wb')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(data)
    resultFile.close()



if __name__ == '__main__':
    pass
#     pair = 'EURUSD'
#     outfile = "NewData/" + pair + "/CascadingTests/" + pair + "output2.csv"
#     classify('EURUSD', 'test1.csv', outfile)
    
    
    