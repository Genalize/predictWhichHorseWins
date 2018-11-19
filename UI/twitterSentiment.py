
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import datetime 



class TwitterClient(object):
    def __init__(self):
        consumer_key = 'AqJ8PdzJcTSL7i9Q05WLN2yHY'
        consumer_secret = 'PWrjXVeelOZK8PnlFs2vI6QIal30S0hrD9s1lC6md5zcA1lfHv'
        access_token = '2700875707-Oi3ms8qd5OBEFgWJnFNy8UK5MPoxmwVrypYM5U0'
        access_token_secret = 'IwmgmDSiZgWvk38F1WHIJqEfhCXAj7Qzv4y30qWEYyiuP'
        # attempt autheitication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        except:
            print("Error Authentication")



    def clean_tweet(self, tweet):
        """Clean tweets using regex
        """
        return tweet.lower()


    def get_tweet_sentiment(self, tweet):
        """Method to classify the tweet using textblob's 
        sentiment method
        """
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'



    def get_tweets(self, query, count = 1000):
        try:
            fetched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query).items(count)]
            # return tweets
            return fetched_tweets

        except tweepy.TweepError as e:
            print("Error: " + str(e))



def mainAnalysis(query, filters):

    api = TwitterClient()
    fetched_tweets = api.get_tweets(query)

    endTime = datetime.datetime.now()
    startTime = endTime - datetime.timedelta(days=1)

    filteredTweets = []

    for i in fetched_tweets:
        if i.created_at > startTime and i.created_at < endTime:
            filteredTweets.append(i)

    # parse the fetched tweets one by one
    # filter tweets according to horse seeds
    print(len(filteredTweets))

    tweets = []
    if filteredTweets is not None:

        for tweet in filteredTweets:

            parsed_tweet = {}

            parsed_tweet['text'] = api.clean_tweet(tweet.text)

            if any(i in parsed_tweet['text'] for i in filters):
                # print(parsed_tweet['text'])

                parsed_tweet['sentiment'] = api.get_tweet_sentiment(tweet.text)

                # check for rewteets
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

                # otherwise append directly
                else:
                    tweets.append(parsed_tweet)


    
    if not len(tweets) == 0:
        
        positive = [i for i in tweets if i['sentiment'] == 'positive']
        percentPositive = 100*(len(positive)/len(tweets))
       
    
        # pick +ve tweets from tweets
        
        # # pick neutral tweets from tweets
        # neutral = [i for i in tweets if i['sentiment'] == 'neutral']

        # # percentage of neutral tweets
        # print("Percentage of neutral Tweets about" + query +": {}%".format(100*len(neutral)/len(tweets)))
    
        # pick -ve tweets from tweets
        negative = [i for i in tweets if i['sentiment'] == 'negative']
        percentNegative = 100*(len(negative)/len(tweets))
        # print("Percentage of -ve Tweets about " + query +": {}%".format(percentNegative))
        

    # print("\n\nPositive Tweets:")
    # for tweet in positive[:10]:
    #     print(tweet['text'])

    # print("\n\nNegative Tweets:")
    # for tweet in negative[:10]:
    #     print(tweet['text'])
        totalTweets = len(tweets)
        return percentPositive, percentNegative, totalTweets