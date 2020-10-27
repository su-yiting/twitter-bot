import tweepy
import logging
import time
import datetime
import os
from os import environ

now = datetime.datetime.now()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

print('This is a twitter bot')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def retrieve_hastags(file_name):
    with open(file_name, 'r') as f_read:
        hastags_name = [hastag.strip() for hastag in f_read]
    f_read.close()
    return hastags_name


FILE_NAME_FAV = 'last_fav_tweet_id.txt'


def retweet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} -filter:retweets"
        tweets = api.search(q=search_query, lang="en", tweet_mode='extended')
        n = 0
        for tweet in tweets:
            if n > 3:
                break
            hashtags = [i['text'].lower()
                        for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#')
                                 for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                if set(hashtags) & set(need_hashtags):
                    if tweet.user.id != api.me().id:
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        n += 1
                        time.sleep(60)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=True)
    else:
        logger.error(
            "Hashtag search terms needs to be of type list", exc_info=True)
        return


retrieve_hashtags = retrieve_hastags(FILE_NAME_FAV)
for h in retrieve_hashtags:
    retrieve_hashtag = ['#'+h]
    retweet_tweets_with_hashtag(api, retrieve_hashtag)
    time.sleep(100)
