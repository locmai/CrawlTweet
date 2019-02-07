import tweepy
import json
import pandas as pd
import csv
import time

# Default variables
MAX_POST_COUNT = 10
SINCE_ID = 1079764115688747009
DATASET_FILENAME = "data.csv"
TWITTER_ID_HEADER = "social/twitter_id"

CONSUMER_API_KEY = ""
CONSUMER_SECRET_KEY = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

print("Starting ...")

auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)


def get_user_tweets(user_id, count=MAX_POST_COUNT):
    # Retrieve user timeline's tweets
    user_timeline = api.user_timeline(
        user_id=user_id, count=count, since_id=SINCE_ID)

    # Get all statuses, extract the IDs
    status_list = [status.__dict__ for status in user_timeline]
    id_list = [status['id'] for status in status_list]

    # Retrieve the full list of statuses with extended mode (each status has full text)
    full_text_tweet_list = [api.get_status(
        status_id, tweet_mode='extended').__dict__ for status_id in id_list]
    return full_text_tweet_list


def extract_status_info(status):
    # Get the values from the key items
    name = status['user'].__dict__['name']
    screen_name = status['user'].__dict__['screen_name']
    id_str = status['user'].__dict__['id_str']
    created_date = status['created_at']
    text = status['full_text']
    retweet_count = status['retweet_count']
    favorite_count = status['favorite_count']
    geo = status['geo']
    if text.lower().startswith("rt @") == True:
        retweet = "True"
    else:
        retweet = "False"
    return name, screen_name, id_str, created_date, text, retweet_count, favorite_count, geo, retweet


# Get the start time
start = time.time()

counting = 0

twitter_data = pd.read_csv(DATASET_FILENAME)[TWITTER_ID_HEADER].dropna()

with open('result.csv', 'w', newline='') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    writer.writerow(['name', 'screen_name', 'id_str', 'created_date',
                     'text', 'retweet_count', 'favorite_count', 'geo', 'retweet'])

    for twitter_id in twitter_data.values:

        counting += 1

        print(f'Processing ID: {twitter_id} .Number: {counting}')

        try:
            tweets = get_user_tweets(int(twitter_id))

            for tweet in tweets:
                writer.writerow(extract_status_info(tweet))

            print(f'Done processing for ID: {twitter_id}. Number: {counting}')

        except tweepy.TweepError:
            print(
                f'Failed to get the info from user ({twitter_id}), number {counting}, skipping...')

# Print out the execution time
end = time.time()

print(end - start)
