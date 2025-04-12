import json
import html
from datetime import datetime

AFFILIATE_TAG = "dd1430e-21"
DEFAULT_LINK = "https://www.amazon.in/deals?tag=" + AFFILIATE_TAG  # fallback

def sanitize(text):
    if not isinstance(text, str):
        return ""
    text = text.replace("₹", "Rs")       # Replace rupee symbol
    text = text.replace("&", "&amp;")    # Escape &
    text = html.escape(text)             # Escape other XML special chars
    return text

def generate_rss():
    try:
        with open("deals.json", "r", encoding="utf-8") as f:
            deals = json.load(f)
    except FileNotFoundError:
        print("❌ deals.json not found. Run scraper first.")
        return

    rss_items = ""
    top_link = DEFAULT_LINK  # Default if no deals
    for i, deal in enumerate(deals[:10]):  # Top 10 deals
        title = sanitize(deal.get("title", "Amazon Deal"))
        link = sanitize(deal.get("link", "#"))
        guid = link
        description = sanitize(deal.get("description", "Top Amazon deal"))

        if i == 0 and link != "#":
            top_link = link  # Use first deal link as <channel><link>

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
    <link>{top_link}</link>
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
