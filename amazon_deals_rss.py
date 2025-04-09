import requests
from bs4 import BeautifulSoup
from datetime import datetime

AFFILIATE_TAG = "dd1430e-21"
AMAZON_DEALS_URL = "https://www.amazon.in/gp/goldbox"

def extract_deals():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(AMAZON_DEALS_URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    items = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/dp/" in href:
            parts = href.split("/dp/")
            if len(parts) > 1:
                product_id = parts[1].split("/")[0].split("?")[0][:10]
                affiliate_url = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
                title = link.text.strip() or f"Amazon Deal {product_id}"
                items.append({
                    "title": title,
                    "link": affiliate_url,
                    "guid": affiliate_url,
                    "description": "Top Amazon deal"
                })

    return items[:10]  # Limit to top 10 deals

def create_rss(deals):
    rss_items = ""
    for item in deals:
        rss_items += f"""
        <item>
            <title>{item['title']}</title>
            <link>{item['link']}</link>
            <description>{item['description']}</description>
            <guid>{item['guid']}</guid>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>Amazon Deals Feed</title>
        <link>{AMAZON_DEALS_URL}</link>
        <description>Today's top Amazon deals with affiliate links</description>
        {rss_items}
    </channel>
    </rss>
    """

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_feed)
    print("✅ RSS feed generated!")

if __name__ == "__main__":
    deals = extract_deals()
    if deals:
        create_rss(deals)
    else:
        print("❌ No deals found.")

