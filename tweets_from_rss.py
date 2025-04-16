name: Tweet Amazon Deals

on:
  workflow_dispatch:
  schedule:
    - cron: "30 5 * * *"

jobs:
  tweet:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: Install dependencies
        run: pip install -r amazon-deals-feed/requirements.txt

      - name: Run Tweet Script
        run: |
          cd amazon-deals-feed
          python tweet_from_rss.py
        env:
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_SECRET: ${{ secrets.TWITTER_ACCESS_SECRET }}
