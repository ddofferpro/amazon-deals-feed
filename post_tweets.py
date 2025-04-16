import tweepy
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Twitter API credentials from GitHub Secrets
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(consumer_key=API_KEY,
                                consumer_secret=API_SECRET_KEY,
                                access_token=ACCESS_TOKEN,
                                access_token_secret=ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to post tweet
def post_tweet(content):
    try:
        api.update_status(content)
        print(f"Tweet posted: {content}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

# Function to read RSS feed and post tweets
def post_from_rss():
    try:
        tree = ET.parse('rss.xml')
        root = tree.getroot()

        for item in root.findall(".//item"):
            title = item.find('title').text
            link = item.find('link').text
            content = f"{title} - {link}"
            post_tweet(content)

    except Exception as e:
        print(f"Error reading RSS feed: {e}")

if __name__ == "__main__":
    post_from_rss()
