import os

from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()


def scrape_user_tweets(username: str = "", num_of_tweets: int = 5, mock: bool = False):
    """Scrape user's original tweets"""
    tweet_list = []

    if mock:
        twitter_gist = "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json"
        tweets = requests.get(twitter_gist, timeout=5).json()

        for tweet in tweets:
            tweet_dict = {
                "text": tweet["text"],
                "url": f"https://twitter.com/{username}/status/{tweet['id']}"
            }
            tweet_list.append(tweet_dict)
    # else:
    #     twitter_client = tweepy.Client(
    #         bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    #         consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    #         consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    #         access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    #         access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    #     )
    #
    #     user_id = twitter_client.get_user(username=username).data.id
    #     tweets = twitter_client.get_users_tweets(
    #         id=user_id,
    #         max_results=num_of_tweets,
    #         exclude=["retweets", "replies"]
    #     )
    #
    #     for tweet in tweets.data:
    #         tweet_dict = {
    #             "text": tweet["text"],
    #             "url": f"https://twitter.com/{username}/status/{tweet['id']}"
    #         }
    #         tweet_list.append(tweet_dict)

    return tweet_list
