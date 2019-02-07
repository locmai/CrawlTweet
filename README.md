# Crawling in Twitter's skin

A quick demonstration for crawling the public contents on Twitter.

## Prerequisite

- Python 3.7 or above
- pip,virtualenv or pipenv installed

## Step-by-step

First, you need to go to the website https://developer.twitter.com/ , sign up and apply for a Twitter developer account. Then input the needed information. I asked for the permissions to get the public data for education purpose only.

The process might take 2 to 3 days.

Next, install the required packages by **pipenv** :

```bash
pipenv install
```

Or by **pip** with **virtualenv**:

```bash
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
```

Go to the website https://developer.twitter.com/en/apps and create a new application, input
the name, description, the homepage url (could be your Facebook account or personal website) and the purposes of your application (100 characters required)

Then go to your App details,
navigate to
**Keys and tokens** tab to get the consumer API keys and the access token keys.

Then replace them in the code:

```python
CONSUMER_API_KEY = "<YOUR-KEY>"
CONSUMER_SECRET_KEY = "<YOUR-KEY>"
ACCESS_KEY = "<YOUR-KEY>"
ACCESS_SECRET = "<YOUR-KEY>"
```

Then run:

```bash
python crawl.py
```

## Others

### MAX_POST_COUNT

Specifies the number of statuses to retrieve from each user.

**Default:** 10

### SINCE_ID

Returns only statuses with an ID greater than (that is, more recent than) the specified ID.

**Default:** 1079764115688747009

### DATASET_FILENAME

Name of your data file.

**Default:** data.csv

### TWITTER_ID_HEADER

Header of the data set for the Twitter ID column. In this example, I set the default as "social/twitter_id" at line 60:

```python
twitter_data = pd.read_csv('data.csv')['social/twitter_id'].dropna()
```

**Default:** "social/twitter_id"

### Returned data

I returned the following data:

```json
[
  "name",
  "screen_name",
  "id_str",
  "created_date",
  "text",
  "retweet_count",
  "favorite_count",
  "geo",
  "retweet"
]
```

You could add more keys or refer to the **keys.json** file for the list of keys provided.

### Code explanation

Initiate the Twitter API object for calling the API with the Authentication info provided above.

```python
auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)
```

Define the **get_user_tweets()** function to get the full list of public statuses on the user's timeline with extended tweet mode (Tweet statuses with full text).

```python
def get_user_tweets(user_id, count=MAX_POST_COUNT):
    # Retrieve user timeline's tweets
    user_timeline = api.user_timeline(
        user_id=user_id, count=count, since_id=1079764115688747009)

    # Get all statuses, extract the IDs
    status_list = [status.__dict__ for status in user_timeline]
    id_list = [status['id'] for status in status_list]

    # Retrieve the full list of statuses with extended mode (each status has full text)
    full_text_tweet_list = [api.get_status(
        status_id, tweet_mode='extended').__dict__ for status_id in id_list]
    return full_text_tweet_list
```

Define the **extract_status_info()** function so we can loop through the status list and extract all the needed information.
