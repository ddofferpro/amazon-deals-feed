import os
import feedparser
import tweepy

# Load secrets from environment variables
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Load and parse the RSS feed
feed_url = "https://ddofferpro.github.io/amazon-deals-feed/rss.xml"  # replace with your actual GitHub Pages URL
feed = feedparser.parse(feed_url)

# Loop through the top 5 deals and tweet them
for entry in feed.entries[:5]:
    tweet = f"{entry.title}\n{entry.link}"
    try:
        api.update_status(tweet)
        print("Tweeted:", tweet)
    except Exception as e:
        print("Error tweeting:", e)
