# -*- coding: utf-8 -*-
"""
#####################################################################################################

Purpose         : Sentimental analysis using Twitter data
Created by      : Sathiya Raj Subburayan
Created date    : 4/21/2019

Other comments  :

Required packages/modules   : 
    
conda install -c conda-forge tweepy(pip install tweepy) 
conda install -c conda-forge textblob(pip install textblob)
python -m textblob.download_corpora

Modification history:
#####################################################################################################
Date        Modified by         Modifications
#####################################################################################################


#####################################################################################################
"""

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
  
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'DrEDXNfdfYimDdSEBWZwPappq'
        consumer_secret = 'm8oIMeSHb4IFZZynsRa4rGn1owpv1TRs1TSaYKS3nRNK8RPn9t'
        access_token = '145192517-iIlC3w3AYUk13IXpDZ6yzwENQEHkt0H3nRE7Idan'
        access_token_secret = 'JJ0N8fy7v3rgAJa4GS3ZAsHQGZTj6ZxupuLETLIJOPm1L'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient()
    analysisAbout = 'CSK'   # input your keyword to analysis
    # calling function to get tweets
    tweets = api.get_tweets(query = analysisAbout, count = 200)
    print("\nAnalysis about: "+analysisAbout+"\n")
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    #print("Neutral tweets percentage: {} %".format(100*len(tweets - ntweets - ptweets)/len(tweets)))
    print("Neutral tweets percentage: {} %".format(100 - ((100*len(ptweets)/len(tweets)) + 100*len(ntweets)/len(tweets))))
  
    # printing first 10 positive tweets 
    print("\n\nFirst 10 Positive tweets:") 
    for tweet in ptweets[:10]: 
        print("\n==> "+tweet['text']) 
  
    # printing first 10 negative tweets 
    print("\n\nFirst 10 Negative tweets:") 
    for tweet in ntweets[:10]: 
        print("\n==> "+tweet['text']) 
  
if __name__ == "__main__": 
    # calling main function 
    main() 