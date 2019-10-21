import logging
import traceback
import tweepy
from typing import List
from tweepy.models import Status

import src.api.src.db.core as db
import src.api.src.db.twitter as twitter_db
from src.scrappers.twitter.secret import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_SECRET,
)
from src.scrappers.twitter.twitter_config import (
    JOKES_FROM_USERS,
    MAX_TWEETS_FOR_USER,
    TWITTER_LANG,
)


logger = logging.getLogger("jokeBot")


def init_twitter_handler() -> tweepy.API:

    api = None
    try:
        logger.debug("Init Twitter API")

        # create OAuthHandler object and set access
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        # create tweepy API object to fetch tweets
        api = tweepy.API(auth)

    except:
        logger.error("Error: Authentication Failed\n{}".format(traceback.format_exc()))

    return api


def get_tweets_from_user(
    api: tweepy.API, user_name: str, max_tweets: int
) -> List[dict, ...]:

    logger.debug("Getting jokes from twitter user: '{}'".format(user_name))

    # get twitter user by username (the one that appears in the url)
    twitter_user = api.get_user(user_name)

    # get list of tweets from user timeline (latest tweets)
    l_user_timeline = twitter_user.timeline(
        trim_user=True, exclude_replies=True, include_rts=False, count=max_tweets
    )

    # get all tweets from a user that does not contain https and save it into a list of dicts
    l_tweets = []
    for tweet in l_user_timeline:
        if (
            "https" not in tweet.text
        ):  # https not in text for only text jokes, not images
            d_tweet = {
                "hash_id": tweet.id_str,
                "user_name": user_name,
                "user_str_id": tweet.author.id_str,
                "joke": tweet.text,
            }

            l_tweets.append(d_tweet)

    logger.debug("Finished getting jokes from twitter user: '{}'".format(user_name))

    return l_tweets


def get_tweets(api: tweepy.API, query: str, max_tweets: int) -> List[Status, ...]:

    try:
        l_tweets = api.search(q=query, lang=TWITTER_LANG, count=max_tweets)
        for tweet in l_tweets:
            print(tweet.text)

    except tweepy.TweepError:
        # print error (if any)
        print("Error : " + str(traceback.format_exc()))
        l_tweets = []

    return l_tweets


def add_jokes_to_twitter_table() -> None:
    # init connection to twitter API
    twitter_api = init_twitter_handler()

    # init db connection
    conn = db.get_jokes_app_connection()

    # get a list of jokes from selected and curated twitter users
    l_jokes = []
    for twitter_user in JOKES_FROM_USERS:
        l_new_jokes = get_tweets_from_user(
            twitter_api, twitter_user, MAX_TWEETS_FOR_USER
        )
        l_jokes.extend(l_new_jokes)

    # input new jokes in the DB
    for d_new_joke in l_jokes:
        if not twitter_db.has_twitter_db_joke(conn, d_new_joke["hash_id"]):
            twitter_db.add_joke_to_twitter_table(conn, d_new_joke)
