'''
Created on 28 Oct 2013

@author: miljan
'''

import nltk, csv, pprint, ast, pickle, numpy, random  # @UnusedImport


"""
Function which takes in an abstract syntax tree
which represents a list of features and creates
a dictionary out of it, so that it can be used 
in nltk.naiveBayes
"""
def __produceFeatures(ast_string):
    try:
        result = ast.literal_eval(ast_string)
    except Exception as e:  # @UnusedVariable
#         print e
        result = ast_string
    d_result = {}
    counter = 0
    for res in result:
        d_result['f' + str(counter)] = res
        counter += 1
    return d_result    
        
        
"""
Function which does a 5 fold cross-validation on a given train set
and displays the confusion matrix for each of the folds,
as well as overall accuracy and certainty measure if turned on
(which is how many classifications were confident above a set threshold)
"""        
def confusionMatrixClassifier(pairname, trainset):
    
    featureVectors = []
    labelSet = []
    all_Tweets = []
    
    # new set of features
    path1 = "NewData/" + pairname + "/TrainingSets/" + pairname + trainset
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            all_Tweets.append(row)
            featureVectors.append(row[4])
            labelSet.append(row[5])

    # old set of features
    #path1 = "Historic/" + pairname + "/" + pairname + "Testing.csv"
#     path1 = "NewData/" + pairname + "/" + pairname + "LaurentiuTesting.csv"
#     with open(path1, 'rb') as csvfile1:
#         reader1 = csv.reader(csvfile1, delimiter=',')
#         for row in reader1:
#             featureVectors.append(row[4:-1])
#             labelSet.append(row[-1])
    
    rang = xrange(1,500)
    # make the feature set
    featureSet = [(__produceFeatures(f),l,i) for (f,l,i) in zip(featureVectors,labelSet,rang)]  
#     random.shuffle(featureSet)
    print featureSet[300]
    print featureSet[300][0].values()
    featureSet, indexSet = [i[0:2] for i in featureSet], [i[2] for i in featureSet]
    print indexSet[300]
    
    counter1 = 0
    counter2 = 0
    counter3 = 0
    for i in labelSet:
        if i == '1':
            counter1 += 1
        elif i == '0':
            counter2 += 1
        else:
            counter3 += 1
    print [counter3,counter2,counter1]
    
    # cross-validation
    probabilities = []
    uncertainity = []
    for i in xrange(0,5):
        a = i*100
        b = (i*100)+100
         
        test_set = featureSet[a:b]
        train_set = featureSet[:a] + featureSet[b:]
        naiveBayes = nltk.NaiveBayesClassifier.train(train_set)
#         probabilities.append(nltk.classify.accuracy(naiveBayes, test_set))
# #         print naiveBayes.show_most_informative_features(5)
#     print probabilities
#     print 'Average :' + str(sum(probabilities)/5)

#     train_set, test_set = featureSet[0:300], featureSet[300:]
#     naiveBayes = nltk.NaiveBayesClassifier.train(train_set)
        test_set_features, test_set_labels = [i[0] for i in test_set], [i[1] for i in test_set]
        train_set_features, train_set_labels = [i[0] for i in train_set], [i[1] for i in train_set]  # @UnusedVariable
        
        # count the number of occurences of a class
        counter1 = 0
        counter2 = 0
        counter3 = 0
        print "1/0/-1"
        for i in train_set_labels:
            if i == '1':
                counter1 += 1
            elif i == '0':
                counter2 += 1
            else:
                counter3 += 1
        print [counter3,counter2,counter1]
        
        # count the number of occurences of a class
        counter1 = 0
        counter2 = 0
        counter3 = 0
        for i in test_set_labels:
            if i == '1':
                counter1 += 1
            elif i == '0':
                counter2 += 1
            else:
                counter3 += 1
        print [counter3,counter2,counter1]
    
        # Confusion matrix generation
        positionCounter = a
        totalCounter = 0
        zeroCounter = 0
        zeroWrong1 = 0
        zeroWrongM1 = 0
        oneWrong0 = 0
        oneWrongM1 = 0
        m1Wrong0 = 0
        m1Wrong1 = 0
        cor0 = 0
        corm1 = 0
        cor1 = 0
        errors = []
        unsure = 0
        known = []#[332,33,117,477,449,245,383,477,271,411,77,55,186,222,358,13,241,198,361,73]
        for i in xrange(len(test_set)):
            positionCounter += 1
            probDist = naiveBayes.prob_classify(test_set_features[i])
            guess = probDist.max()
            confidence = probDist.prob(guess)
            label = test_set_labels[i]
            if confidence < 0.5:
                unsure += 1
                continue
            if label != guess:
                totalCounter += 1
                if guess == '0':
                    zeroCounter += 1
                    if (label == '1'):
                        zeroWrong1 += 1
                    else:
                        zeroWrongM1 += 1
                if guess == '1':
                    zeroCounter += 1
                    if (label == '0'):
                        oneWrong0 += 1
                    else:
                        oneWrongM1 += 1
                if guess == '-1':
                    zeroCounter += 1
                    if (label == '0'):
                        m1Wrong0 += 1
                    else:
                        m1Wrong1 += 1
                if indexSet[positionCounter-1] not in known:
                    errors.append((label, indexSet[positionCounter-1],guess,confidence))
            else:
                if guess == '0':
                    cor0 += 1
                elif guess == '1':
                    cor1 += 1
                else:
                    corm1 += 1
        print "label/position/guess"
        pprint.pprint(errors)
        accuracy = (100-totalCounter)
        unsureness = (100-unsure)
        uncertainity.append(unsureness)
        probabilities.append(accuracy)
        print ""
        print "Errors total: " + str(totalCounter)
        print "Accuracy: " + str(accuracy) +"%"
        print "class -1/0/1/total"
        print "Class -1: " + str([corm1,m1Wrong0,m1Wrong1])
        print "Class 0: " + str([zeroWrongM1,cor0,zeroWrong1])
        print "Class 1: " + str([oneWrongM1,oneWrong0,cor1])
        print "Total: " + str([corm1+zeroWrongM1+oneWrongM1,m1Wrong0+cor0+oneWrong0,m1Wrong1+zeroWrong1+cor1])
        print "Unsure: " + str(unsure)
    print "Accuracy"
    print probabilities
    print numpy.mean(probabilities)
    print "Certainty"
    print uncertainity
    print numpy.mean(uncertainity)


    # train the classifier on the whole set
#     naiveBayes = nltk.NaiveBayesClassifier.train(featureSet)
    # storing the trained classifier for future use
#     f = open("NewData/" + pairname + "/Classifiers/" + pairname + "NaiveBayes.pickle", 'wb')
#     pickle.dump(naiveBayes, f)
#     f.close()



"""
Function which trains a classifier on a set of features and
training examples and pickles it.
"""        
def trainClassifier(pairname, trainset, pickleFilename):
    
    featureVectors = []
    labelSet = []
    
    # My set of features
    path1 = "NewData/" + pairname + "/TrainingSets/" + pairname + trainset
    with open(path1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',')
        for row in reader1:
            featureVectors.append(row[4])
            labelSet.append(row[5])

    # make the feature set
    featureSet = [(__produceFeatures(f),l) for (f,l) in zip(featureVectors,labelSet)]  

    # train the classifier on the whole set
    naiveBayes = nltk.NaiveBayesClassifier.train(featureSet)
    # storing the trained classifier for future use
    f = open("NewData/" + pairname + "/Classifiers/" + pairname + pickleFilename, 'wb')
    pickle.dump(naiveBayes, f)
    f.close()


"""
Classify a given tweet vector for a specific pair.
Naive bayes is used with a different set of features, depending on pair.
Returns a list of 2 elements: [classification, confidence]
"""
def classifyTweet(tweetVector, pairname, classifier):    
    # unpickle the classifier
    if classifier == 1:
        classif = "NaiveBayes1.pickle"
    elif classifier == 2:
        classif = "NaiveBayes2.pickle"
    elif classifier == 3:
        pass
    else:
        raise Exception("Wrong classifier number given in NaiveBayes.classifyTweet()")
    f = open("NewData/" + pairname + "/Classifiers/" + pairname + classif)
    classifier = pickle.load(f)
    f.close()
    # produce featureset from the feature string literal
    d_featureVector = __produceFeatures(tweetVector)
    # get the probability distribution of classed
    probDist = classifier.prob_classify(d_featureVector)
    # get the class with highest probability
    maxClass = probDist.max()
    return [maxClass,probDist.prob(maxClass)]





if __name__ == '__main__':
    #read the currency pairs from textfile
#     pairsFile = open("Pairs.txt","r");
#     pairs = pairsFile.readlines()
#     pairsFile.close()
#     pairs = [pair.replace('/','').strip() for pair in pairs[1:]]
    pairs = ['GBPUSD', 'USDJPY', 'AUDUSD', 'USDCHF', 'USDCAD']
    for pair in pairs:
#     pair = 'USDCAD'
        confusionMatrixClassifier(pair,'TrainingFeaturesTop45+7unigrams.csv')
#     confusionMatrixClassifier(pair,'TrainingFeaturesTop50+updown.csv')
#         trainClassifier(pair, 'TrainingFeaturesTop50+updown.csv','NaiveBayes1')
#         trainClassifier(pair, 'TrainingFeaturesTop45+7unigrams.csv','NaiveBayes2')
#     tweetVector = '[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'
#     a = classifyTweet(tweetVector, 'EURUSD')
#     print a
