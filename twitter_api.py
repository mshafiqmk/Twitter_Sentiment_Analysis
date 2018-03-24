import re
import tweepy
from textblob import TextBlob
from configobj import ConfigObj

config = ConfigObj('config.ini')


class twitterClient(object):
    """
    Generic Twitter class for the app
    """

    def __init__(self, query, retweets_only=False, with_sentiment=False):
        # twitter apps keys and tokens
        consumer_key = config['CONSUMER_KEY']
        consumer_secret = config['CONSUMER_SECRET']
        access_token = config['ACCESS_TOKEN']
        access_token_secret = config['ACCESS_TOKEN_SECRET']

        # authenticating the user
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
            self.query = query
            self.with_sentiment = with_sentiment
            self.tweet_count_max = 100  # To prevent Rate Limiting
            self.retweets_only = retweets_only
        except:
            print("Error: Authentication Failed!")

    def set_query(self, query=''):
        self.query = query

    def set_retweets_checking(self, retweets_only='false'):
        self.retweets_only = retweets_only

    def set_with_sentiment(self, with_sentiment='false'):
        self.with_sentiment = with_sentiment

    def cleaning_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


    def get_tweet_sentiment(self, tweet):
        cleaned_tweet = self.cleaning_tweet(tweet)
        analysis = TextBlob(cleaned_tweet)

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


    def get_tweets(self):
        tweets = []

        try:
            recvd_tweets = self.api.search(q=self.query,
                                           count=self.tweet_count_max)

            if not recvd_tweets:
                pass

            for tweet in recvd_tweets:
                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.screen_name

                if self.with_sentiment == 1:
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                else:
                    parsed_tweet['sentiment'] = 'unavailable'

                if tweet.retweet_count > 0 and self.retweets_only == 1:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                elif not self.retweets_only:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
            print(tweets)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))