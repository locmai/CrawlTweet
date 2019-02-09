import tweepy
import json
import pandas as pd
import csv
import time

# Default variables
MAX_POST_COUNT = 10
SINCE_ID = None
DATASET_FILENAME = "data.csv"
RESULT_FILENAME = "users.csv"
TWITTER_ID_HEADER = "social/twitter_id"

CONSUMER_API_KEY = ""
CONSUMER_SECRET_KEY = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

print("Starting ...")

auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)


def extract_user_info(user):
    name = user['name']
    screen_name = user['screen_name']
    id_str = user['id_str']
    created_date = user['created_at']
    description = user['description']
    statuses_count = user['statuses_count']
    followers_count = user['followers_count']
    friends_count = user['friends_count']
    return name, screen_name, id_str, created_date, description, statuses_count, followers_count, friends_count


counting = 0

twitter_data = pd.read_csv(DATASET_FILENAME)[TWITTER_ID_HEADER].dropna()

with open(RESULT_FILENAME, 'w', newline='') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    writer.writerow(['name', 'screen_name', 'id_str', 'created_at',
                     'description', 'statuses_count', 'followers_count', 'friends_count'])

    for twitter_id in twitter_data.values:

        counting += 1

        print(f'Processing ID: {twitter_id} .Number: {counting}')

        try:
            start = time.time()
            user = api.get_user(user_id=twitter_id).__dict__
            writer.writerow(extract_user_info(user))
            end = time.time() - start
            print(
                f'Done processing for ID: {twitter_id}. Number: {counting} in {end} seconds')

        except tweepy.TweepError:
            print(
                f'Failed to get the info from user ({twitter_id}), number {counting}, skipping...')
