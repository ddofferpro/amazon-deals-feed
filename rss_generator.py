import json
from datetime import datetime
import html

AFFILIATE_TAG = "dd1430e-21"

def generate_rss():
    try:
        with open("deals.json", "r", encoding="utf-8") as f:
            deals = json.load(f)
    except FileNotFoundError:
        print("❌ deals.json not found. Run scraper first.")
        return

    if not deals:
        print("❌ No deals found in deals.json.")
        return

    # Use the first deal's link as the main feed link
    main_link = deals[0].get("link", "https://www.amazon.in")

    rss_items = ""
    for deal in deals[:10]:  # Top 10 deals
        title = html.escape(deal.get("title", "Amazon Deal").replace("₹", "Rs"))
        link = deal.get("link", "#")
        guid = link
        description = html.escape(deal.get("description", "Top Amazon deal").replace("₹", "Rs"))

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
    <link>{main_link}</link>
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
