import json
import html
from datetime import datetime

AFFILIATE_TAG = "dd1430e-21"
AMAZON_DEALS_URL = "https://www.amazon.in/gp/goldbox"

def generate_rss():
    try:
        with open("deals.json", "r", encoding="utf-8") as f:
            deals = json.load(f)
    except FileNotFoundError:
        print("❌ deals.json not found. Run scraper first.")
        return

    rss_items = ""
    for deal in deals[:10]:  # Top 10 deals
        title = html.escape(deal.get("title", "Amazon Deal"))
        link = html.escape(deal.get("link", "#"))
        guid = html.escape(link)
        description = html.escape(deal.get("description", "Top Amazon deal"))

        rss_items += f"""
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <description>{description}</description>
            <guid>{guid}</guid>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Amazon Deals Feed</title>
    <link>{html.escape(AMAZON_DEALS_URL)}</link>
    <description>Today's top Amazon deals with affiliate links</description>
    <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
    {rss_items}
</channel>
</rss>
"""

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_feed)

    print("✅ RSS file generated as rss.xml")

if __name__ == "__main__":
    generate_rss()
