import json
from datetime import datetime
import xml.sax.saxutils as saxutils

AFFILIATE_TAG = "dd1430e-21"
AMAZON_DEALS_URL = "https://www.amazon.in/gp/goldbox"

def xml_escape(text):
    return saxutils.escape(text)

def generate_rss():
    try:
        with open("deals.json", "r", encoding="utf-8") as f:
            deals = json.load(f)
    except FileNotFoundError:
        print("❌ deals.json not found. Run scraper first.")
        return

    rss_items = ""
    for deal in deals[:10]:  # Top 10 deals
        title = xml_escape(deal.get("title", "Amazon Deal"))
        link = xml_escape(deal.get("link", "#"))
        guid = link
        description = xml_escape(deal.get("description", "Top Amazon deal"))

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
    <title>{xml_escape("Amazon Deals Feed")}</title>
    <link>{xml_escape(AMAZON_DEALS_URL)}</link>
    <description>{xml_escape("Today's top Amazon deals with affiliate links")}</description>
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
