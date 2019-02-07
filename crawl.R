library(twitteR)

# Default variables
MAX_POST_COUNT = 10
SINCE_ID = 1079764115688747009
DATASET_FILENAME = "data.csv"
TWITTER_ID_HEADER = "social/twitter_id"

# Authentication info
CONSUMER_API_KEY = ""
CONSUMER_SECRET_KEY = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

setup_twitter_oauth(CONSUMER_API_KEY,CONSUMER_SECRET_KEY,ACCESS_KEY,ACCESS_SECRET)
  
get_user_tweets <- function(user_id, count) {
  user_timeline <- userTimeline(user=user_id, n=count, sinceID=SINCE_ID)
  sample <- statusFactory$new(user_timeline[1])
  print(sample$getText())
}

extract_status_info <-function(status) {
  print(status)
}

TEST_ID = 3026622545

get_user_tweets(TEST_ID,10)
