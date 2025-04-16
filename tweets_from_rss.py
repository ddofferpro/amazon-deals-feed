import feedparser
import tweepy
import os

# Twitter Auth
api_key = os.environ["TWITTER_API_KEY"]
api_secret = os.environ["TWITTER_API_SECRET"]
access_token = os.environ["TWITTER_ACCESS_TOKEN"]
access_secret = os.environ["TWITTER_ACCESS_SECRET"]

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# Parse RSS
feed = feedparser.parse("https://yourusername.github.io/yourrepo/rss.xml")

for entry in feed.entries[:5]:  # Change number of tweets if needed
    title = entry.title
    link = entry.link
    tweet = f"{title}\n{link}"
    try:
        api.update_status(tweet)
        print(f"✅ Tweeted: {tweet}")
    except Exception as e:
        print(f"❌ Error: {e}")
