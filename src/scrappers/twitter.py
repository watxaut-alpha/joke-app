import logging
import traceback
import tweepy

from src.scrappers.secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET


logger = logging.getLogger('jokeBot')


def init_twitter_handler():

    api = None
    try:
        # create OAuthHandler object and set access
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        # create tweepy API object to fetch tweets
        api = tweepy.API(auth)

    except:
        logger.error("Error: Authentication Failed\n{}".format(traceback.format_exc()))

    return api


def get_tweets_from_user(api, user_name, max_tweets):

    # get twitter user by username (the one that appears in the url)
    twitter_user = api.get_user(user_name)

    # get list of tweets from user timeline (latest tweets)
    l_user_timeline = twitter_user.timeline(trim_user=True, exclude_replies=True, include_rts=False, count=max_tweets)

    # get all tweets from a user that does not contain https and save it into a list of dicts
    l_tweets = []
    for tweet in l_user_timeline:
        if "https" not in tweet.text:  # https not in text for only text jokes, not images
            d_tweet = {
                "id": tweet.id_str,
                "author": user_name,
                "author_id": tweet.author.id_str,
                "text": tweet.text
            }

            l_tweets.append(d_tweet)

    return l_tweets


def get_tweets(api, query, max_tweets):

    try:
        l_tweets = api.search(q=query, lang="es", count=max_tweets)
        for tweet in l_tweets:
            print(tweet.text)

    except tweepy.TweepError as e:
        # print error (if any)
        print("Error : " + str(traceback.format_exc()))

# twitter_api = init_twitter_handler()
#
# query = "chistes"
# max_tweets = 50
# get_tweets(twitter_api, query, max_tweets)
#
# u = twitter_api.get_user("EresChiste")
#
# # https not in text for only text jokes
# u.timeline(trim_user=True, exclude_replies=True, include_rts=False, count=100)
# l = []
# for i in t:
#     if not "https" in i.text:
#         l.append(i.text)
