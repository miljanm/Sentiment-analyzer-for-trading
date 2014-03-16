'''
Created on 12 Mar 2014

@author: miljan
'''

'''
Main method in this class which does complete sentiment reevaluation 
including subsequent multiple tweets per same user and retweets.
'''
def reevaluateSentiment(pairname, data):
    data = reevaluateMultipleTweets(pairname, data)
    data = reevaluateRetweets(pairname, data)
    return data

'''
Method which reads the tweet data and assigns sentiment value
of (+/-)0.5 to each tweet that was retweeted. 
Retweeted tweets are marked by starting : in their text.
'''
def reevaluateRetweets(painame, data):
    for i in data:
        charToCompare = i[2].split()[0]
        if (len(charToCompare) > 1): charToCompare = charToCompare[0]
        if (charToCompare == ':'):
            sentiment = str(i[3])
            if (sentiment[0] == '1'): i[3] = 0.5
            elif (sentiment[0] == '-' and sentiment[1] == '1'): i[3] = -0.5 
    return data

    
'''
Method which takes in tweets data, and reevaluates the
sentiment based on the following formula:
-if there are 2 tweets from the same author with the same sentiment
first one will have full sentiment, second one half of that and
following one will be zero.
-same thing applies for both positive and negative sentiment
'''
def reevaluateMultipleTweets(pairname, data):
    counter = 0
    length = len(data)
    while (counter < length):
        username = data[counter][1]
        sentiment = __sentimentToInt__(data[counter][3])
        # break if the array is finished
        if (counter < length - 1):
            usernameNext = data[counter+1][1]
            sentimentNext = __sentimentToInt__(data[counter+1][3])
        else:
            break
        updatedFlag = 0
        # go through tweets with same username and apply diminishing value
        # to sentiment for same sentiment direction subsequent tweets
        counter +=1
        while (username == usernameNext):
            counter += 1
            if (sentiment == sentimentNext):
                # calculate new sentiment
                if (updatedFlag == 1): newSentiment = 0 # previous one was updated, all subsequent are 0
                elif (sentiment == -1): newSentiment = -0.5
                elif (sentiment == 1): newSentiment = 0.5
                else: newSentiment = 0
                # update next sentiment in the main list
                data[counter-1][3] = newSentiment
                updatedFlag = 1
            else:
                updatedFlag = 0
                sentiment = sentimentNext

            # get next element data
            if (counter < length - 1):
                usernameNext = data[counter][1]
                sentimentNext = __sentimentToInt__(data[counter][3])
            else:
                # break if the array is finished
                break
    return data

'''
Helper method to return actual float value of sentiment
'''
def __sentimentToInt__(sentiment):
    sentiment = str(sentiment)
    if (sentiment[0]) == '1': return 1
    elif (sentiment[0]) == '-': return -1
    else: return 0
    

if __name__ == '__main__':
#     data = []
#     pair = "AUDUSD"
#     pathToTweets = "/home/miljan/workspace/GUI/war/PairData/" + pair + "/" + pair + "LiveResults.csv"
#     try:
#         with open(pathToTweets, 'rb') as csvfile1:
#             reader1 = csv.reader(csvfile1, delimiter=',')
#             for row in reader1:
#                 data.append(row)
#     except IOError as e:
#         print e
#          
#     data = reevaluateSentiment(pair, data)
#     for counter, i in enumerate(data):
#         print counter, i[3] 
    pass
    